
import os

from flask import (flash, redirect, render_template, request,
                   send_from_directory, url_for)
from app import app
from flask import Flask, render_template, send_file,jsonify
from flask_sqlalchemy import SQLAlchemy




#赵文欣 数据库操作
# 配置 SQLite 数据库连接
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'portraits.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 初始化数据库对象
db = SQLAlchemy(app)
# 定义数据库模型
class Portrait(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    age = db.Column(db.String(255))
    gender = db.Column(db.String(50))
    nationality = db.Column(db.String(100))
    behavior = db.Column(db.Text)
# 创建表
with app.app_context():
    db.create_all()








#赵文欣 罗倍 人物画像生成

@app.route('/portraitGenerate', methods=['GET'])
#渲染主页
def portraitGenerate():
    # 渲染主页
    return render_template('./portraitGenerate/portraitGenerate.html')
#画像生成接口
@app.route('/generate_portrait', methods=['POST'])
def generate_portrait():
    # 获取前端传递的 JSON 数据
    data = request.get_json()
    num_people = data.get('num_people')
    nationality = data.get('nationality')

    # 模拟生成的静态属性和动态属性
    generated_portraits = []
    
    for i in range(num_people):
        portrait = {
            'name': f'人物{i + 1}',
            'age': f'{20 + i}岁',
            'gender': '男性' if i % 2 == 0 else '女性',
            'nationality': nationality,
            'behavior': '行为序列：走路 -> 跑步 -> 跳跃 -> 休息。'
        }
        generated_portraits.append(portrait)

    # 返回生成的内容
    return jsonify({'portraits': generated_portraits})

#画像保存到数据库中接口
@app.route('/save_portrait', methods=['POST'])
def save_portrait():
    # 获取生成的人物画像数据
    data = request.get_json()
    portraits = data.get('portraits', [])

    # 保存每个画像到数据库
    for portrait in portraits:
        new_portrait = Portrait(
            name=portrait['name'],
            age=portrait['age'],
            gender=portrait['gender'],
            nationality=portrait['nationality'],
            behavior=portrait['behavior']
        )
        db.session.add(new_portrait)

    # 提交到数据库
    db.session.commit()

    return jsonify({'message': '人物画像保存成功！'})






#孔超娜 博文生成接口


#渲染前端界面
@app.route('/blog_generate', methods=['GET'])
def blogGenerate():
    generated_blog = "这是一个生成的博文内容。"
    return render_template('./blogGenerate/blogGenerate.html', generated_text=generated_blog)
#获取数据库中人物名，在前端展示
@app.route('/get_portraits', methods=['GET'])
def get_portraits():
    # 查询所有人物画像
    portraits = Portrait.query.all()
    portrait_list = [{'id': portrait.id, 'name': portrait.name} for portrait in portraits]  # 获取ID和名称

    # 返回JSON格式的用户数据
    return jsonify(portrait_list)
 
# 接收前端请求并返回生成文本的路由
@app.route('/generate_text', methods=['POST'])
def generate_text():
    # 获取前端传递的 JSON 数据
    data = request.get_json()
    generation_type = data.get('generation_type')
    emotion = data.get('emotion')
    theme = data.get('theme')
    user = data.get('user')
    user_id = data.get('user')
    portrait = Portrait.query.filter_by(id=user).first()
    print(portrait.nationality)
    
    # 根据传递的参数生成文本
    generated_text = f"类型: {generation_type}, 情感: {emotion}, 主题: {theme}, 用户ID: {user} 的生成内容。"

    # 返回 JSON 数据给前端
    return jsonify({'generated_text': generated_text})







#李令迪 评论生成接口

#模拟热点新闻的数据
hot_news_list = [
    "热点1：新科技产品发布，引发广泛关注。",
    "热点2：经济政策调整，股市波动剧烈。",
    "热点3：体育赛事开幕，众多选手表现亮眼。"
]

# 渲染评论生成页面
@app.route('/comment_generate', methods=['GET'])
def commentGenerate():
    return render_template('./commentGenerate/commentGenerate.html')


# 爬取热点新闻接口
@app.route('/fetch_hot_news', methods=['GET'])
def fetch_hot_news():
    # 这里可以实现爬虫逻辑来获取实时的热点新闻
    # 目前是模拟热点新闻
    return jsonify({'hot_news': hot_news_list})


# 生成评论接口
@app.route('/generate_comment', methods=['GET'])
def generate_comment():
    # 生成一个静态评论
    static_comment = "这真是一个非常有趣的热点，大家对此议论纷纷，值得关注！"

    # 返回生成的评论
    return jsonify({'comment': static_comment})






#申文松 行为序列生成

# 渲染行为序列生成页面
@app.route('/behavior_generate', methods=['GET'])
def behaviorGenerate():
    return render_template('./behaviorGenerate/behaviorGenerate.html')

# 接收前端请求并返回生成的行为序列
@app.route('/generate_behavior_sequence', methods=['POST'])
def generate_behavior_sequence():
    # 获取前端传递的 JSON 数据
    data = request.get_json()
    user_id = data.get('user_id')
    portrait = Portrait.query.filter_by(id=user_id).first()
    if portrait:
        # 打印该用户的所有信息
        print(f"用户ID: {portrait.id}, 名字: {portrait.name}, 年龄: {portrait.age}, 性别: {portrait.gender}, 国籍: {portrait.nationality}, 行为序列: {portrait.behavior}")

    # 模拟生成的行为序列
    behavior_sequence1 = f"用户 {user_id} 的行为序列：走路 -> 跑步 -> 跳跃 -> 休息。"
    with open('app/1.txt', 'r', encoding='utf-8') as file:
        behavior_sequence = file.read()
    behavior_sequence_html = behavior_sequence.replace('\n', '<br>')
    # 返回生成的行为序列
    return jsonify({'behavior_sequence': behavior_sequence_html})

# 获取所有用户信息，并返回给前端下拉框
@app.route('/get_users', methods=['GET'])
def get_users():
    # 查询所有人物画像 (用户)
    portraits = Portrait.query.all()
    
    print(portraits)
    user_list = [{'id': portrait.id, 'name': portrait.name} for portrait in portraits]  # 获取ID和名称

    # 返回JSON格式的用户数据
    return jsonify(user_list)

@app.route('/datashow', methods=['GET'])
def dataShow():
    return render_template('./dataShow/dataShow.html')


@app.route('/get_portrait_data', methods=['GET'])
def get_portrait_data():
    portraits = Portrait.query.all()
    portrait_data = []
    for portrait in portraits:
        portrait_data.append({
            'id': portrait.id,
            'name': portrait.name,
            'age': portrait.age,
            'gender': portrait.gender,
            'nationality': portrait.nationality,
            'behavior': portrait.behavior
        })
    return jsonify(portrait_data)










@app.route("/", methods=["POST", "GET"])
@app.route("/index/", methods=["POST", "GET"])
def index():
    return render_template("./home/index.html")
# 登录路由
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    
    # 如果是 GET 请求，渲染登录页面
    return render_template('./upload/upload.html')
