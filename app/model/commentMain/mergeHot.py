import requests
from datetime import datetime
from urllib.parse import quote
from bs4 import BeautifulSoup
import pandas as pd
from app.model.commentMain.mimix.comment import extract_and_print_predictions
from app.model.commentMain.mimix.comment import stream_enc_dec_demo
from app.model.commentMain.mimix.comment import enc_dec_comment
from app.model.commentMain.mimix.comment import chat_comment
from app.model.commentMain.mimix.comment import stream_lm_demo
from app.model.commentMain.mimix.comment import lm_demo
from app.model.commentMain.mimix.utils import real_path, load_model_config


def hot_search():
    url = 'https://weibo.com/ajax/side/hotSearch'
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()['data']


def merge_event(num, cookie):
    data = hot_search()
    # print(data)
    if not data:
        print('获取微博热搜榜失败')
        return

    # 准备数据
    date_str = datetime.now().strftime('微博热搜榜 20%y年%m月%d日 %H:%M')
    top_item = f"置顶:{data['hotgov']['word'].strip('#')}"
    # print(date_str)
    # print(top_item)

    # results = [[date_str, "", ""], [top_item, "", ""]]
    results = []

    for i, rs in enumerate(data['realtime'][:num], 1):
        title = rs['word']
        heat = rs['num']
        link = f"https://s.weibo.com/weibo?q={quote(title)}&Refer=top"
        content = fetchUrl(link, cookie)
        results.append([title, heat, link, content])
        # print(f"{i}. {title} {heat} 链接：https://s.weibo.com/weibo?q={quote(title)}&Refer=top {content}")

    # 将数据转换为 DataFrame
    df = pd.DataFrame(results, columns=["标题", "热度", "链接", "博文"])

    # 保存到 Excel
    excel_filename = "weibo_hot_search.xlsx"
    df.to_excel(excel_filename, index=False)
    print(f"数据已保存到 {excel_filename}")
    return results


def fetchUrl(url_single, cookieSingle):
    url = url_single
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    }
    cookies = {
        "cookie": cookieSingle
    }

    response = requests.get(url, headers=headers, cookies=cookies)
    response.encoding = 'uft-8'
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # 先查找具有 node-type="feed_list_content_full" 的 <p> 标签
    div = soup.find('div', attrs={'action-type': 'feed_list_item'})
    content = div.find('p', attrs={'node-type': 'feed_list_content_full'})
    # 如果找不到，则查找 node-type="feed_list_content" 的 <p> 标签
    if not content:
        content = div.find('p', attrs={'node-type': 'feed_list_content'})

    # 如果找到了该标签，提取其文本内容
    text = ""
    if content:
        # 使用 .get_text() 来提取文本内容并替换掉 HTML 实体（如图片替换为表情符号）
        text = content.get_text(strip=True)
        # print(text)
    else:
        print("Content not found")
    return text


def gen_comment(num, cookie, model_conf="app/model/commentMain/conf/MimixLM-0.7b-sft_conf", mode="pred", stream=False):
    # 使用传入的参数创建一个简单的类来模拟 argparse 的 Namespace
    class Args:
        def __init__(self, model_conf, mode, stream):
            self.model_conf = model_conf
            self.mode = mode
            self.stream = stream

    # 创建一个 Args 实例来替代 argparse 的解析结果
    # Namespace(model_conf='conf/comment_base_conf', mode='pred', stream=False)
    args = Args(model_conf, mode, stream)

    conf_file = args.model_conf
    config = load_model_config(real_path(conf_file))
    if "convert_special_token" not in config:
        config["convert_special_token"] = False
    data = hot_search()
    # print(data)
    if not data:
        print('获取微博热搜榜失败')
        return

    # results = [[date_str, "", ""], [top_item, "", ""]]
    resContentComment = []
    numCur = 1
    for i, rs in enumerate(data['realtime'][:num], 1):
        title = rs['word']
        heat = rs['num']
        link = f"https://s.weibo.com/weibo?q={quote(title)}&Refer=top"
        content = fetchUrl(link, cookie)
        # print(f"{i}. {title} {heat} 链接：https://s.weibo.com/weibo?q={quote(title)}&Refer=top {content}")

        if args.mode == "pred":
            if config["task"] == "enc_dec":
                if args.stream == True:
                    config["beam_size"] = 1
                    stream_enc_dec_demo(config)
                else:
                    # enc_dec_demo(config)
                    inputText = content
                    outputText = enc_dec_comment(config, inputText)
                    res = extract_and_print_predictions(outputText)
                    return inputText, res
            elif config["task"] == "lm":
                if config.get("is_mimix_chat", False) == True:
                    config["convert_special_token"] = True
                    # chat(config)
                    inputText = "针对下面给出的博文，要求给出不超过20字的评论内容：" + content
                    # print(inputText)
                    outputText = chat_comment(config, inputText)
                    # print("结果输出：", outputText)
                    resContentComment.append([content, outputText])
                    print(numCur)
                    numCur += 1
                elif args.stream == True:
                    config["beam_size"] = 1
                    stream_lm_demo(config)
                else:
                    lm_demo(config)
    return resContentComment




if __name__ == '__main__':
    # 获取热搜的数量
    num = 1
    # https://weibo.com/hot/search
    cookie = "SCF=AobOS93b8R0367Y0xwjM6WQ8nvIO5ARwHGiPbTj3LnubAkYMNqidqEprD_6kq1032UzBLJVhib13UnW7Cb2-AdE.; SINAGLOBAL=2330144313882.294.1724727097129; UOR=,,www.google.com; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhMr3Win2kvud5VMOjpIORF5JpX5KMhUgL.FoMESh.ce0efS0z2dJLoIEXLxKBLB.eLBo2LxK-L12qLB-qLxK-L12qL1hnLxKqL1hML1hzLxKBLB.2L1hqt; ULV=1728616292918:6:1:1:1813712024768.559.1728616292857:1725417926685; XSRF-TOKEN=G7VfX3YC_pREi9qNjf5vg67M; ALF=1731943156; SUB=_2A25KF72kDeRhGeFM71sX8y3JzD6IHXVpbL9srDV8PUJbkNB-LXnukW1NQN51gyt83eTDhys4TMsFc8FwGaJd2qpa; WBPSESS=gjySmkdJtQeQkiLbjmJIjrH8jDoOUi22PfFStfGbCRBixVfnaGSALAWuQGWe6htvAHamMRjd76jFJqMAUUHznS9MKfE9YaULoI13SEBrb040iXG7wvvztuwoFukq19L267javGc3bouOzA6eDZ2Teg=="
    # merge_event(num, cookie)
    gen_comment(num, cookie, "conf/MimixLM-0.7b-sft_conf")
