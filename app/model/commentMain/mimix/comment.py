# -*- coding: utf-8 -*-
import os
import platform
from argparse import ArgumentParser
import sys
import time
from PIL import Image
from app.model.commentMain.mimix.predictor import EncDecGenerator, LMGenerator, TextEncoder
from app.model.commentMain.mimix.predictor import ImageEncoder, ClipMatcher
from app.model.commentMain.mimix.utils import real_path, load_model_config


def pretty_print(res):
    """
    Assume res = [{k1:v1,k2:v2,...,kn:[[s1, score1], [s2, score2]]}, {}, ... ]
    """
    for dic in res:
        info = [[k, dic[k]] for k in dic if not isinstance(dic[k], list)]
        info = " ".join("%s:%s" % (k, v) for k, v in info)
        if len(info) > 0:
            print(info)
        print("--------------------")
        for k in dic:
            if isinstance(dic[k], list):
                for a in dic[k]:
                    info = " ".join([str(x) for x in a])
                    print(info)


def enc_dec_demo(config):
    """
    """
    enc_dec_gen = EncDecGenerator(config)

    print("INPUT TEXT:")
    for line in sys.stdin:
        # "在一个阳光明媚的星期天下午，一对父母带着他们的两个孩子来到公园放风筝。天空湛蓝，白云萦绕，微风拂面，是放风筝的好天气\t生成积极评论"
        line = line.strip()

        if len(line) == 0:
            continue

        src_list = [line.strip().split("\t")[0]]

        prefix_list = None
        if "\t" in line:
            arr = line.strip().split("\t")
            src_list = [s for i, s in enumerate(arr) if i % 2 == 0]  # 迭代器: 索引，值
            prefix_list = [s for i, s in enumerate(arr) if i % 2 == 1]

        start = time.time()

        search_res = enc_dec_gen.predict(src_list, prefix_list=prefix_list)
        # [['好可爱的孩子 ', -7.8551836013793945], ['好可爱的宝宝 ', -8.14856243133545], ['好可爱的孩子，好想抱抱 ', -14.050756454467773]]]]

        # 将 search_res 写入 txt 文件
        with open("result.txt", "w", encoding="utf-8") as file:
            for sentence, scores in search_res:
                # file.write(f"Sentence: {sentence}\n")
                file.write("Comment:\n")
                for sub_item in scores:
                    file.write(f"  - {sub_item[0]} | {sub_item[1]}\n")
                # file.write("\n")  # 添加一个空行分隔不同的条目

        search_result = [{"src": x, "predict": y} for x, y in search_res]
        pretty_print(search_result)

        end = time.time()
        cost = end - start
        print("-----cost time: %s s-----" % cost)


def enc_dec_comment(config, text):
    enc_dec_gen = EncDecGenerator(config)

    # 使用 text 参数替代 sys.stdin 读取输入
    result = []

    # 分割多行输入的情况
    lines = text.splitlines()

    for line in lines:
        line = line.strip()

        if len(line) == 0:
            continue

        src_list = [line.strip().split("\t")[0]]

        prefix_list = None
        if "\t" in line:
            arr = line.strip().split("\t")
            src_list = [s for i, s in enumerate(arr) if i % 2 == 0]
            prefix_list = [s for i, s in enumerate(arr) if i % 2 == 1]

        start = time.time()

        # 调用预测函数，获取生成结果
        search_res = enc_dec_gen.predict(src_list, prefix_list=prefix_list)

        # 生成的结果直接添加到 result 列表中
        search_result = [{"src": x, "predict": y} for x, y in search_res]
        result.append(search_result)

        end = time.time()
        cost = end - start
        # print("-----cost time: %s s-----" % cost)

    # 返回最终的结果
    return result


def lm_demo(config):
    """
    """
    lm_gen = LMGenerator(config)

    print("INPUT TEXT:")
    for line in sys.stdin:
        line = line.strip()
        prefix_list = None
        if len(line) > 0:
            prefix_list = line.split("\t")

        start = time.time()
        search_res = lm_gen.predict(prefix_list=prefix_list)

        search_res = [{"src": x, "predict": y} for x, y in search_res]
        pretty_print(search_res)

        end = time.time()
        cost = end - start
        print("-----cost time: %s s-----" % cost)


def stream_enc_dec_demo(config):
    """
    """
    config["beam_size"] = 1
    enc_dec_gen = EncDecGenerator(config)

    print("INPUT TEXT:")
    for line in sys.stdin:
        line = line.strip()

        if len(line) == 0:
            continue

        src_list = [line.strip().split("\t")[0]]

        prefix_list = None
        if "\t" in line:
            prefix_list = [line.split("\t")[1]]

        start = time.time()
        search_res = enc_dec_gen.predict_stream(src_list, prefix_list=prefix_list)

        text = ""
        while True:
            try:
                _text = next(search_res)[0][1][0][0]
                print(_text[len(text):], end="", flush=True)
                text = _text
                # 将 search_res 写入 txt 文件
                with open("result.txt", "w", encoding="utf-8") as file:
                    file.write(text)
            except:
                break

        print()

        end = time.time()
        cost = end - start
        print("-----cost time: %s s-----" % cost)


def stream_lm_demo(config):
    """
    """
    config["beam_size"] = 1
    lm_gen = LMGenerator(config)

    print("INPUT TEXT:")
    for line in sys.stdin:
        line = line.strip()
        prefix_list = None
        if len(line) > 0:
            prefix_list = [line]

        start = time.time()
        search_res = lm_gen.predict_stream(prefix_list=prefix_list)

        text = ""
        while True:
            try:
                _text = next(search_res)[0][1][0][0]
                print(_text[len(text):], end="", flush=True)
                text = _text
            except:
                break

        print()

        end = time.time()
        cost = end - start
        print("-----cost time: %s s-----" % cost)


def chat(config):
    print("loading model...")
    max_history_len = config.get("max_history_len", 2000)
    max_history_turn = config.get("max_history_turn", 20)
    sysinfo = config.get("sysinfo", "")

    assert config["is_mimix_chat"] == True
    assert max_history_len < config["trg_max_len"]

    lm_gen = LMGenerator(config)
    history = []
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")
    print("Welcome to MimixAI.")
    while True:
        print("User:")
        user_input = input()
        if user_input == ":restart":
            if platform.system() == "Windows":
                os.system("cls")
            else:
                os.system("clear")
            print("Welcome to MimixAI.")
            history = []
            continue
        elif user_input == ":exit":
            break
        history.append(user_input)
        context = " _mimix_"
        for i, text in enumerate(history[::-1]):
            if i > max_history_turn:
                break
            if len(context) > max_history_len:
                break
            if i % 2 == 0:
                context = " _mimixuser_ " + text + context
            else:
                context = " _mimix_ " + text + context
        context = (sysinfo + context).strip()

        search_res = lm_gen.predict_stream(prefix_list=[context])
        resp = ""
        print("Mimix:")
        while True:
            try:
                _resp = next(search_res)[0][1][0][0].split("_mimix_")[-1].strip()
                print(_resp[len(resp):], end="", flush=True)
                resp = _resp
            except:
                break
        print()

        history.append(resp)


def chat_comment(config, text):
    """
    Chat function that accepts a text input and returns the result without entering a loop.
    """
    max_history_len = config.get("max_history_len", 2000)
    max_history_turn = config.get("max_history_turn", 20)
    sysinfo = config.get("sysinfo", "")

    assert config["is_mimix_chat"] == True
    assert max_history_len < config["trg_max_len"]

    lm_gen = LMGenerator(config)
    history = []

    # 直接接受一次 text 输入
    user_input = text

    history.append(user_input)
    context = " _mimix_"
    for i, history_text in enumerate(history[::-1]):
        if i > max_history_turn:
            break
        if len(context) > max_history_len:
            break
        if i % 2 == 0:
            context = " _mimixuser_ " + history_text + context
        else:
            context = " _mimix_ " + history_text + context
    context = (sysinfo + context).strip()

    # 调用模型进行预测
    search_res = lm_gen.predict_stream(prefix_list=[context])
    resp = ""
    while True:
        try:
            _resp = next(search_res)[0][1][0][0].split("_mimix_")[-1].strip()
            # print(_resp[len(resp):], end="", flush=True)
            resp = _resp
        except:
            break

    # 将结果返回，而不是继续循环
    return resp



def extract_and_print_predictions(result):
    for item in result:
        for res in item:
            predict_list = res['predict']
            for predict, score in predict_list:
                return predict
                # print(f"{predict}")


def run_interactive():
    """
    """
    parser = ArgumentParser()

    parser.add_argument("--model_conf", type=str)
    parser.add_argument("--mode", type=str, default="pred")
    parser.add_argument('--stream', action='store_true')
    parser.set_defaults(stream=False)

    # Namespace(model_conf='conf/comment_base_conf', mode='pred', stream=False)
    args = parser.parse_args(sys.argv[1:])

    conf_file = args.model_conf
    config = load_model_config(real_path(conf_file))
    if "convert_special_token" not in config:
        config["convert_special_token"] = False

    # print(parser, "---------", args, "--------", config)
    print("启动comment！！！！！！！")

    if args.mode == "pred":
        if config["task"] == "enc_dec":
            if args.stream == True:
                config["beam_size"] = 1
                stream_enc_dec_demo(config)
            else:
                # enc_dec_demo(config)
                inputText = "在美国加州的斯坦福医院，一台名为“MediBot”的医疗机器人创造了历史，成为全球首个完全独立执行心脏搭桥手术的人工智能。这台机器人利用深度学习和实时数据分析技术，在没有人类医生参与的情况下完成了手术。手术结果显示患者恢复良好，预计将在一周内出院。医疗专家认为，这一突破性事件将开启医疗行业的新纪元，未来医疗机器人可能在更多复杂手术中扮演关键角色。"
                outputText = enc_dec_comment(config, inputText)
                # print("结果未处理：", outputText)
                extract_and_print_predictions(outputText)
        elif config["task"] == "lm":
            if config.get("is_mimix_chat", False) == True:
                config["convert_special_token"] = True
                # chat(config)
                inputText = "20字评论下面的内容：在美国加州的斯坦福医院，一台名为“MediBot”的医疗机器人创造了历史，成为全球首个完全独立执行心脏搭桥手术的人工智能。这台机器人利用深度学习和实时数据分析技术，在没有人类医生参与的情况下完成了手术。手术结果显示患者恢复良好，预计将在一周内出院。医疗专家认为，这一突破性事件将开启医疗行业的新纪元，未来医疗机器人可能在更多复杂手术中扮演关键角色。"
                outputText = chat_comment(config, inputText)
                print("结果输出：", outputText)
            elif args.stream == True:
                config["beam_size"] = 1
                stream_lm_demo(config)
            else:
                lm_demo(config)


if __name__ == "__main__":
    run_interactive()
