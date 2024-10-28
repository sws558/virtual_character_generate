import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime
import difflib
import random
from translate import Translator
translator = Translator(to_lang="zh")


#找经常使用的设备
def parse_device_preference(device_stats_str):
    device_usage = {}
    if device_stats_str and isinstance(device_stats_str, str):
        items = device_stats_str.split(', ')
        for item in items:
            if ': ' in item:
                device, count = item.split(': ')
                device_usage[device] = int(count)
    # 如果设备使用数据不为空，则返回使用次数最多的设备
    if device_usage:
        return max(device_usage, key=device_usage.get)
    return 'N/A'
#得到动态特征
def generate_formatted_user_data(user_id):
    # 查找对应的用户数据
    sample = next((item for item in data_dict if item.get('User ID') == user_id), None)
    if not sample:
        return f"No user found with ID {user_id}"

    device_preference = parse_device_preference(sample.get('Publish Tool', ''))

    # 生成用户数据字典
    formatted_data = {
        "Weekly Online Frequency": f"{sample.get('Average Weekly Online Days', 0)} days",
        "Online Time": sample.get('Most Frequent Post Time', 'N/A'),
        "Online Duration": f"{random.choice([0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4])}h",
        "Post Time": sample.get('Most Frequent Post Time', 'N/A'),
        "Weekly Post Count": f"{sample.get('Average Weekly Post Count', 0)} posts",
        "Weekly Likes": f"{random.choice(range(11))} likes",
        "Weekly Saves": f"{random.choice(range(11))} saves",
        "Weekly Comments": f"{random.choice(range(11))} comments",
        "Weekly Shares": f"{random.choice(range(11))} shares",
        "Browsing Speed": f"{random.choice([10, 15, 20])}s/post",
        "Browsing Depth": random.choice(["Summary", "Half", "Full"]),
        "Social Response Time": f"{random.choice([5, 30, 60, 120])} mins/comment",
        "Emotion Expression": sample.get('Preference', 'N/A'),
        "Notification Settings": random.choice(["Off", "On"]),
        "Acquisition Method": random.choice(["From Subscription", "From Recommendation"]),
        "Interaction Group Size": f"{random.choice([10, 15, 20, 25, 30, 35, 40])} people",
        "Device Preference": device_preference,
        "Average Monthly New Followers": f"{int((sample.get('Followers Count', 100) * 0.9) / (sample.get('Net Age Years', 1) * 12))} people",
        # "Multi-platform Usage": random.choice(["Single platform", "Multiple platforms"]),
        "Response Speed to External Events": f"{random.choice([0, 0.5, 1, 2, 3, 4])} days",
        "Usage Duration Change": sample.get('Usage Trend', 'N/A'),
        # "New Feature Adaptability": random.choice(["Quick", "Gradual", "Slow"]),
        # "Annual Profile Modifications": f"{random.choice([1, 2, 3, 4, 5, 6])} times",
        # "Topic Focus Depth": f"{random.choice([0.5, 1, 2, 3, 4])} days",
        # "Annual Environment Changes": f"{random.choice([1, 2, 3, 4, 5, 6, 7])} times"
    }

    return formatted_data

# 找相似性最大
def calculate_similarity(user_data, target_profile):
    # 提取职业相似度
    job_similarity = difflib.SequenceMatcher(None, str(user_data["work"]), target_profile["job_title"]).ratio()

    # 提取性别相似度
    gender_similarity = 1.0 if user_data["gender"] == target_profile["Gender"] else 0.0

    # 计算年龄差异
    try:
        birthdate = datetime.strptime(user_data["birthday"], "%Y-%m-%d")
        current_age = (datetime.now() - birthdate).days // 365
    except:
        current_age = None

    age_similarity = 1.0 - abs(current_age - int(target_profile["Age"])) / 100.0 if current_age else 0.0  # 正则化到0-1之间

    # 提取描述和微博内容的相似度 (使用 TF-IDF + 余弦相似度)
    user_description = str(user_data["description"]) + " " + str(user_data.get("weibos", ""))
    target_interests = target_profile["hobbies"] + " " + target_profile["topics_of_interest"]

    vectorizer = TfidfVectorizer().fit_transform([user_description, target_interests])
    interest_similarity = cosine_similarity(vectorizer[0:1], vectorizer[1:2])[0][0]

    # 综合计算相似度（可以调整权重）
    overall_similarity = (job_similarity * 0.5 +
                          gender_similarity * 0.1 +
                          age_similarity * 0.1 +
                          interest_similarity * 0.3)

    return overall_similarity
def find_sim_max_user(target_profile):
    # 读取CSV文件
    file_path = "weibo_combined_user_data.csv"
    df = pd.read_csv(file_path)
    # 对每个用户计算相似度
    df["similarity"] = df.apply(lambda row: calculate_similarity(row, target_profile), axis=1)

    # 找到相似度最高的用户
    most_similar_user = df.loc[df["similarity"].idxmax()]
    print(f"最相似的用户ID: {most_similar_user['id']}, 相似度: {most_similar_user['similarity']:.2f}")
    return most_similar_user['id']

#翻译
def translate_dict_values(data_dict, to_lang="zh"):
    translator = Translator(to_lang=to_lang)
    translated_dict = {}

    for key, value in data_dict.items():
        if isinstance(value, str):
            # 对字符串类型的值进行翻译
            if ', ' in value:  # 如果值中有多个项目，用逗号分隔
                parts = value.split(', ')
                translated_parts = [translator.translate(part) for part in parts]
                translated_value = ', '.join(translated_parts)
            else:
                translated_value = translator.translate(value)
        else:
            # 对非字符串类型的值，直接转换为字符串
            translated_value = str(value)

        translated_dict[key] = translated_value

    return translated_dict
#写出
def write_formatted_user_data_to_file(user_data, file):
    # 逐行写入格式化的用户数据
    for key, value in user_data.items():
        formatted_line = f"\t* {key}：{value}\n"
        file.write(formatted_line)

#总函数
def process_all_users(target_profile):
        print(f"正在处理动态特征，传入的静态特征为：{target_profile}")
        translated_info_dict = translate_dict_values(target_profile)
        # 查找最相似用户并生成动态特征
        user_id = find_sim_max_user(translated_info_dict)
        formatted_user_data = generate_formatted_user_data(user_id)
        # print(f"formatted_user_data:{formatted_user_data}")
        return formatted_user_data




# 读取微博数据的动态特征分析结果文件
file_path = 'user_statistics.csv'
data = pd.read_csv(file_path)
# Convert data to a list of dictionaries
data_dict = data.to_dict(orient='records')

# # 读取生成的静态文件里面的五个静态属性进行匹配
# file_path = '/home/code_project/项目爬虫/person_output(1).txt'
# output_file_path = './person_dynamic_output.txt'
#
# # 处理所有用户
# process_all_users(file_path, output_file_path)

# print(f"所有用户的动态特征已生成并写入 {output_file_path}")
