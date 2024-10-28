import random

# 1、年龄：18-50
age = random.randint(18, 50)

# 28、网龄：（1-（年龄-5））
web_age = random.randint(1,(age-5))

# 2、性别
genders = ['male','female']
gender = genders[random.randint(0,1)]

# 3、学历(1)
edus = ['Junior high school degree','High school degree','Bachelor\'s degree','Bachelor\'s degree','Bachelor\'s degree','Bachelor\'s degree','Master\'s degree','Master\'s degree','Master\'s degree','PhD degree','PhD degree']
edu = edus[random.randint(0,9)]

# 4、情感(3)
emotions = ['happiness','enjoyment','sorrowful','infuriate','proud']
emotion = random.sample(emotions, 3)

# 5、语气(4)
tones = ['Moyan Style', 'News Style', 'Trump Style']
tone = random.sample(tones, 1)

# 6、是否使用缩略语
acronyms = ['yes','no']
acronym = acronyms[random.randint(0,1)]

# 7、留言长度:20-300
length1 = random.randint(20,300)
length = str(length1) + 'words'

# 8、文本内容比例：30-98%
text_proportion = random.randint(30,98)
text_proportions = str(text_proportion) + '%'

# 9、图片内容比例：0-（100-文本内容比例-1）%
pic_proportion = random.randint(0,(100-text_proportion-1))
pic_proportions = str(pic_proportion) + '%'

# 10、视频内容比例：（100-文本内容比例-图片内容比例）%
video_proportion = 100-text_proportion-pic_proportion
video_proportions = str(video_proportion) + '%'

# 11、引用来源（3）
sources = ['Other User Blogs','Newspapers','Native Audio Images','unquote']
source = random.sample(sources, 3)

# 12、交互对象（1）['朋友','粉丝']
interactions = ['strangers','celebrity']
interaction = random.sample(interactions, 1)
interaction.append('friends')
interaction.append('fans')

# 13、原创内容比例：30-98%
innovation_pro = random.randint(30,98)
innovation_pros = str(innovation_pro) + '%'

# 14、转发内容比例：100-原创内容比例 %
forwarding_pro = 100-innovation_pro
forwarding_pros = str(forwarding_pro) + '%'

# 15、关注内容（4）
att_contents = ['own profession','exercise','journey','music and dance','politically','news','self-improvement','philosophy','animal','hometown']
att_content = random.sample(att_contents, 4)

# 16、粉丝构成{'朋友':'','家人':'',其他:''}
mate = random.randint(30,98)
family = random.randint(0,(100-mate-1))
oth = 100-mate-family
fan_categories = {'friends': str(mate) + '%', 'family':  str(family) + '%', 'others':  str(oth) + '%'}

# 17、第三方应用的构成{'社交软件':'','学习软件':'','娱乐软件':'','其他':''}
social_ware = random.randint(20,98)
learn_ware = random.randint(0,(100-social_ware-2))
play_ware = random.randint(0,(100-social_ware-learn_ware-1))
oth1 = 100-social_ware-learn_ware-play_ware
software_categories = {'social software': str(social_ware) + '%','learning software': str(learn_ware) + '%','Recreational Software': str(play_ware) + '%','others': str(oth1) + '%'}

# 18、是否使用默认图片（1）
pics = ['yes','no']
pic = pics[random.randint(0,1)]

# 19、获得的@比率：30-90
at_pros = random.randint(30,90)
at_pro = str(at_pros) + '%'

# 20、提及用户（3）['朋友','粉丝']
user_mentions = ['family','strangers','celebrity']
user_mention = random.sample(user_mentions, 1)
user_mention.append('friends')
user_mention.append('fans')

# 27、社交软件偏好（1）
socials = ['Not use','only use one','use 2-3 social ware','use all social ware']
flag = random.randint(0,3)
social = socials[flag]

# 21、常用的社交平台（social）
platforms = ['WeChat','microblog','ins','facebook','Bilibili','YouTube']
platform = []
if flag==0:
    platform = ['nothing']
if flag==1:
    platform = platforms[random.randint(0,5)]
if flag==2:
    if random.randint(0,1):
        platform = random.sample(platforms, 2)
    else:
        platform = random.sample(platforms, 3)
if flag==3:
    platform = platforms

# 22、隐私设置（1）
privacys = ['up','down']
privacy = privacys[random.randint(0,1)]

# 23、社交账号状态{'在线':'30-98%',‘离线’:'100-在线%'}
online = random.randint(30,98)
outline = 100-online
state = {'online':str(online) + '%','offline':str(outline) + '%'}

# 24、列表数量 3-50
list_num = random.randint(3,50)

# 25、好友数量 10-2000
mate_num = random.randint(10,2000)

# 26、被回复比 30-98
reply_pros = random.randint(30,98)
reply_pro = str(reply_pros) + '%'

# 29、政治倾向（1）
politys = ['conservatism','liberalism','socialist']
polity = politys[random.randint(0,2)]

# 30、宗教信仰（1）
religions = ['yes','no']
religion = religions[random.randint(0,1)]

# 31、关注人数：5-1000
att_person_num = random.randint(5,1000)

# 32、粉丝人数：0-9000
fun_num = random.randint(0,9000)

# 33、发帖数量：网龄/2 - 网龄*300
post_num = random.randint(int(web_age/2),web_age*300)

# 34、点赞总数：网龄/5 - 网龄*3000
kudo_num = random.randint(int(web_age/5),web_age*3000)

# 35、评论总数：网龄/2 - 网龄*300
remark_num = random.randint(int(web_age/2),web_age*300)

# 36、收藏总数：网龄/3 - 网龄*300
save_num = random.randint(int(web_age/3),web_age*300)

# 37、分享总数：网龄/5 - 网龄*3000
share_num = random.randint(int(web_age/5),web_age*3000)

# 38、使用的第三方应用数量：10-50
sofeware_num = random.randint(10,50)

# 39、网上消费习惯(3)
consumes = ['Shopping Software Consumption','Software Membership','Gaming Consumption','Consumption in the live room','Concert software','takeaway software','invest in stocks']
consume = random.sample(consumes,3)

# 40、健康状况（1）
healths = ['well-being','well-being','well-being','well-being','sub-health','sub-health','sub-health','sub-health','sub-health','weak']
health = healths[random.randint(0,9)]

# 41、家庭成员构成（1）
familys = ['single parents','three-member family','three generations','four generations']
family = familys[random.randint(0,3)]

# 42、收入水平（1）
money_levels = ['ascend to the middle class','wealthy']
money_level = money_levels[random.randint(0,1)]

# 43、群聊身份（1）
group_identitys = ['bachelors','manager','Ordinary members']
group_identity = group_identitys[random.randint(0,2)]

# 44、投诉记录（1）
complaints = ['yes','no']
complaint = complaints[random.randint(0,1)]

# 45、会员（1）
insiders = ['yes','no']
insider = insiders[random.randint(0,1)]

# 46、发起话题概率 0-98%
postive_pros = random.randint(0,98)
postive_pro = str(postive_pros) + '%'

# 47、跟随话题概率 100-发起话题概率%
follow_pro = str(100-postive_pros) + '%'

# 48、是否是平台up主
uppers = ['yes','no']
upper = uppers[random.randint(0,1)]

# 49、是否合作发布内容
cooperations = ['yes','no']
cooperation = cooperations[random.randint(0,1)]

# 是否被举报过
ws = ['yes','no']
ws1 = ws[random.randint(0,1)]
# 是否举报过网上内容
we = ['yes','no']
we1 = we[random.randint(0,1)]
# 是否经常点踩
wr = ['yes','no']
wr1 = wr[random.randint(0,1)]
# 是否经常加入群聊
wt = ['yes','no']
wt1 = wt[random.randint(0,1)]
# 是否经常组建群聊
wf = ['yes','no']
wf1 = wf[random.randint(0,1)]

# 49个动态特征输出
'''
dynamic_characteristics = {'年龄':age,'国籍':nationality,'学历':edu,'情感':emotion,'语气':tone,'是否使用缩略语':acronym,
                           '留言长度':length,'文本内容比例':text_proportions,'图片内容比例':pic_proportions,'视频内容比例':video_proportions,
                           '引用来源':source,'交互对象':interaction,'原创内容比例':innovation_pros,'转发内容比例':forwarding_pros,'关注内容':att_content,
                           '粉丝构成':fan_categories,'第三方应用的构成':software_categories,'是否使用默认图片':pic,'获得的@比率':at_pro,'提及用户':user_mention,
                           '常用的社交平台':platform,'隐私设置':privacy,'社交账号状态':state,'列表数量':list_num,'好友数量':mate_num,
                           '被回复比':reply_pro,'社交软件偏好':social,'网龄':web_age,'政治倾向':polity,'宗教信仰':religion,
                           '关注人数':att_person_num,'粉丝人数':fun_num,'发帖数量':post_num,'点赞总数':kudo_num,'评论总数':remark_num,
                           '收藏总数':save_num,'分享总数':share_num,'使用的第三方应用数量':sofeware_num,'网上消费习惯':consume,'健康状况':health,
                           '家庭成员构成':family,'收入水平':money_level,'群聊身份':group_identity,'投诉记录':complaint,'会员':insider,
                           '发起话题概率':postive_pro,'跟随话题概率':follow_pro,'是否是平台up主':upper,'是否合作发布内容':cooperation
                           'Frequently reported':ws1,'reported online content':we,'frequently downvote':wr,'frequently join group chats':wt,'frequently create group chats':wf
                           }
                           'Tone':tone
'''
dynamic_characteristics = {'Age':age,'Gender':gender,'Qualifications':edu,'Use of abbreviations':acronym,'Tones and emotion':tones,
                           'Message Length':length,'Text-content ratio':text_proportions,'Picture-content ratio':pic_proportions,'Video-content ratio':video_proportions,
                           'Cited sources':source,'Interactive object':interaction,'Proportion of original content':innovation_pros,'Percentage of retweeted content':forwarding_pros,
                           'Fan Composition':fan_categories,'Composition of third-party applications':software_categories,'Whether to use the default image':pic,'Rates obtained@':at_pro,'References to users':user_mention,
                           'Popular social media platforms':platform,'Privacy Settings':privacy,'Social Account Status':state,'Number of lists':list_num,'Number of Friends':mate_num,
                           'response rate':reply_pro,'Social Software Preferences':social,'Net age':web_age,'political orientation':polity,'Religious beliefs':religion,
                           'Number of followers':att_person_num,'Number of fans':fun_num,'Number of posts':post_num,'Total number of likes':kudo_num,'Total comments':remark_num,
                           'Total collections':save_num,'Total shared':share_num,'Number of third-party apps used':sofeware_num,'Online consumption habits':consume,'Health status':health,
                           'Frequently reported':ws1,'reported online content':we,'frequently downvote':wr,'frequently join group chats':wt,'frequently create group chats':wf,
                           'Composition of family members':family,'Income level':money_level,'Group chat identity':group_identity,'Complaint records':complaint,'Member':insider,
                           'Probability of initiating a topic':postive_pro,'Follow topic probability':follow_pro,'Whether it is a platform uploader':upper,'Whether or not to collaborate on publishing content':cooperation
                           }


def generate_feature():
    formatted_output = "\n\t* ".join(f"{key}: {value}" for key, value in dynamic_characteristics.items())
    return formatted_output