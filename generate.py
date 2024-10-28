import pymysql
import torch
import json
import re
import shutil
import argparse
import os
from transformers import AutoTokenizer, AutoModelForCausalLM, HfArgumentParser, GenerationConfig
from peft import PeftModel
from typing import Union
import queue
import random
import requests  # 请求网页
import traceback
import jieba.analyse as ana
import jieba
import jieba.posseg as jp
from gensim import corpora, models
from generate_blog.generate_llama3 import generate_blog
from TextToImage.EnChImage import generate_img

root_path = "./blog"

def create_directory_and_file(user_id, topic, emotion):
    # 定义目录名称
    directory_name = f"user_{user_id}"

    # 获取当前目录并创建用户目录路径
    user_directory = os.path.join(root_path, directory_name)

    # 创建目录
    if not os.path.exists(user_directory):
        os.mkdir(user_directory)
        print(f"Directory '{directory_name}' created successfully.")
    else:
        print(f"Directory '{directory_name}' already exists.")

    topic_directory_name = f"topic_{topic}-emotion_{emotion}"
    topic_directory = os.path.join(user_directory, topic_directory_name)
    # 创建子目录
    if not os.path.exists(topic_directory):
        os.mkdir(topic_directory)
        print(f"Directory '{topic_directory_name}' created successfully.")
    else:
        print(f"Directory '{topic_directory_name}' already exists.")

    print(topic_directory)
    return topic_directory

def download_picture(html,file_path):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintoosh; Intel Mac OS X 10_14_68) '
                             'AppleWebKit/538.36 (KHTML, like Gecko) Chrome/76.0.3904.97 Safari/537.36'}
    pic_url = re.findall('"objURL":"(.*?)",', html, re.S)  # 找到符合正则规则的目标网站
    num = len(pic_url)

    txt_path = file_path + '/download_detail.txt'
    print('现在开始下载图片...')

    each = random.choice(pic_url)
    a = '正在下载，图片地址为:' + str(each) + '\n'
    # print(a)
    path = file_path + '/image'
    try:
        if not os.path.exists(path):
            pic = requests.get(each, headers=headers, timeout=10)
            with open(path + '.jpg', 'wb') as f:
                f.write(pic.content)
                f.close()
            with open(txt_path, 'a') as f:
                f.write(a)
                f.close()
    except:
        traceback.print_exc()
        print('【错误】当前图片无法下载')
    return path + '.jpg'

def get_input(nikename,topic,emtion):
    #读取数据库得到用户信息
    db = pymysql.connect(
        host="10.122.241.181"
        , user="root"
        , passwd="123456"
        , database="person_feature"
        , port=3306
    )

    # 创建游标并执行查询
    cursor = db.cursor()
    columns = ["job_title", "hobbies", "Tones_and_emotion"]  # 要查询的列名列表
    columns_str = ", ".join(columns)  # 将列名组合成字符串
    # SQL 查询，查找特定元素
    query = f"SELECT {columns_str} FROM person_output WHERE nikename = %s"
    cursor.execute(query, (nikename,))
    # 获取查询结果
    result = cursor.fetchone()  # 只获取一行，如果需要获取多行可以用 fetchall()
    print(result)

    #整理成输入提示
    job = result[0].strip()  # 去掉前后的空格
    hobbies = result[1].strip()  # 去掉前后的空格
    Tones_and_emotion = result[2].strip()

    hobby_list = hobbies.split(",")  # 以逗号分隔多个兴趣爱好
    hobby_list = [h.replace('and', '').strip() for h in hobby_list]
    print(hobby_list)
    target_hobby = random.choice(hobby_list)
    input = f'[job:{job};hobby:{target_hobby};topic:{topic};emotion:{emtion}]'
    print(input)
    return input,Tones_and_emotion

def generate(img,user,topic,emtion):
    # 根据参数调用不同的函数
    input, style = get_input(user, topic, emtion)#
    blog = generate_blog(input, style)
    direction_path = create_directory_and_file(user, topic, emtion)
    # 在用户目录下创建文件 blog.txt
    file_name = f"blog.txt"
    file_path = os.path.join(direction_path, file_name)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(blog)
    if img == 1:
        return blog
    if img == 2:
        dst_path = "./app/static/images/img.jpg"
        html = generate_img(blog)
        image_path = download_picture(html, direction_path)
        print(image_path)
        print(f"image written and saved to blog")
        if not os.path.exists(image_path):
            print(f"源文件 {image_path} 不存在")
            return blog

            # 检查目标文件夹是否存在，如果不存在则创建
        dst_folder = os.path.dirname(dst_path)
        if not os.path.exists(dst_folder):
            os.makedirs(dst_folder)
        # 复制文件
        try:
            shutil.copy(image_path, dst_path)
            print(f"图片已成功从 {image_path} 复制到 {dst_path}")
        except Exception as e:
            print(f"复制文件时出错: {e}")

        return blog

# generate_blog1,generate_img1=generate(img=2,user="平安北京朝阳", topic="Hometown",emtion="Pride",style="Moyan Style")  # 将会生成文本  News Style Trump Style

