import mysql.connector

# 创建 MySQL 连接
db = mysql.connector.connect(
    host="localhost",      # 数据库地址
    user="root",  # 数据库用户名
    password="123456",  # 数据库密码
    database="person_feature"   # 使用的数据库
)

# 创建游标对象
cursor = db.cursor()

# 读取person_output.txt文件并提取内容
with open('person_output.txt', 'r', encoding='utf-8') as file:
    content = file.read()

# 提取三个虚拟人的数据
persons_data = content.split("虚拟人静动态特征如下：")[1:]  # 分割文档，获取每个人物的块

for person_data in persons_data:
    # 提取每个人的特征
    lines = person_data.strip().split('\n')
    person_info = []
    for line in lines:
        line = line.strip()
        if line.startswith('* '):  # 检查行是否以 '*' 开头，表示有用的信息
            key_value = line.split('：')  # 使用中文冒号分割键值
            if len(key_value) == 2:
                key, value = key_value
                person_info.append(value)
    # 要插入的值
    values = tuple(person_info)

    # 插入数据的SQL语句
    sql = """
        INSERT INTO person_output (nikename, nation, personality, writing_tone, topics_of_interest, job_title, place_of_work, hobbies, age)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    # 执行插入操作
    cursor.execute(sql, values)
    db.commit()

    print("Data inserted successfully!")

# 关闭连接
cursor.close()
db.close()
