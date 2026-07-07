import re

with open(r'D:\PROJECTS\_AI\AIBook_Script\小云雀分镜（全集）\第8课-雾气里的照片_合并版.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix swapped labels: 03 should be "第一个发现", 04 should be "动手试一试"
# Current: "### 03. 动手试一试" with "第一个发现" content, "### 04. 第一个发现" with "动手试一试" content
content = content.replace('### 03. 动手试一试', '### 03. 第一个发现')
content = content.replace('### 04. 第一个发现', '### 04. 动手试一试')

# Extract header (基础设定 + 角色与风格)
header_match = re.search(r'(# 第8课.*?(?=## 分镜))', content, re.DOTALL)
header = header_match.group(1) if header_match else ''

# Extract all shots
shots_match = re.search(r'## 分镜\s*\n(.*?)(?=## 生成建议)', content, re.DOTALL)
shots_text = shots_match.group(1).strip() if shots_match else ''

# Split into individual shots
shot_pattern = r'(### \d{2}\..*?)(?=\n### \d{2}\.|$)'
shots = re.findall(shot_pattern, shots_text, re.DOTALL)

print(f"Found {len(shots)} shots")

# Upper: shots 0-5 (01-06), time 00:00-01:32
# Lower: shots 6-11 (07-12), time 01:32-03:00

upper_shots = shots[:6]
lower_shots = shots[6:]

# Upper time offsets: starts at 00:00
# Current upper times: 00:00-00:14, 00:14-00:28, 00:28-00:44, 00:44-01:00, 01:00-01:16, 01:16-01:32
upper_times = ['00:00-00:14', '00:14-00:28', '00:28-00:44', '00:44-01:00', '01:00-01:16', '01:16-01:32']
# Lower time offsets: starts at 01:32
# Current lower times: 01:32-01:48, 01:48-02:04, 02:04-02:22, 02:22-02:36, 02:36-02:50, 02:50-03:00
lower_times = ['01:32-01:48', '01:48-02:04', '02:04-02:22', '02:22-02:36', '02:36-02:50', '02:50-03:00']

def renumber_shots(shots_list, times, start_num=1):
    result = []
    for i, shot in enumerate(shots_list):
        num = f'{start_num + i:02d}'
        # Replace shot number and time
        shot = re.sub(r'### \d{2}\.', f'### {num}.', shot)
        shot = re.sub(r'\d{2}:\d{2}-\d{2}:\d{2}', times[i], shot)
        result.append(shot)
    return result

upper_renumbered = renumber_shots(upper_shots, upper_times)
lower_renumbered = renumber_shots(lower_shots, lower_times)

# Standard titles for upper
upper_titles = ['故事开场', '今天学什么', '第一个发现', '动手试一试', '规则出现', '换一种方式看']
# Standard titles for lower
lower_titles = ['核心知识揭示', '效果展示', '信息连接现实', '神奇时刻', '知识总结', '动手与预告']

def apply_titles(shots_list, titles):
    result = []
    for i, shot in enumerate(shots_list):
        # Replace title after shot number
        shot = re.sub(r'### \d{2}\. \S+', f'### {i+1:02d}. {titles[i]}', shot)
        result.append(shot)
    return result

upper_with_titles = apply_titles(upper_renumbered, upper_titles)
lower_with_titles = apply_titles(lower_renumbered, lower_titles)

# Build header for upper
upper_header = """# 第8课《雾气里的照片》上集分镜稿
> **非常重要，必须严格遵守：以上传的图片作为关键帧画面；人物形象必须跟人物角色板保持一致，包括多视角、表情、服装、身体比例、局部细节和角色气质。**
## 基础设定
- 年龄：3-9岁
- 时长：约1分32秒
- 比例：16:9
- 主题：噪声 = 干扰信号
- 核心知识：噪声是混在信息里的干扰；噪声让信息变模糊、不清晰；信息不清晰，判断就容易出错；AI也会被噪声影响，做出错误判断
- 故事：团团和点点进入《雾气里的照片》的情境，通过一个具体问题、一次动手观察和一次清楚总结，把本课知识变成小朋友能看懂、能复述的小故事。
## 角色与风格
- 团团：7岁男孩，黑灰短发，圆脸腮红，橙色上衣，蓝色背带裤，小书包，好奇活泼。
- 点点：白色云朵形AI机器人，深色屏幕脸，青蓝发光眼睛，胸口屏幕，头顶紫色天线。
- 本课新增角色/场景：雾蒙蒙的窗户，窗外风景模糊不清，适合儿童。
- 风格：儿童水彩绘本动画风，清透明亮，高清质感，色彩饱和，减少模糊笔触，角色与上传参考图一致。
- 负面：不要写实摄影、3D塑料感、暗黑恐怖、角色变形、多余手指、文字乱码、画面拥挤、低清晰度。
- 旁白要求：旁白讲话时，团团和点点的嘴不要动，不要做对口型或配合讲话动作；只保持倾听、观察或轻微点头即可。
- 配音要求：发音清晰，全部使用标准普通话。
## 分镜
"""

upper_content = upper_header + '\n'.join(upper_with_titles) + """

## 生成建议
每镜只保留一个主要动作，优先轻推近、横移、角色观察、图标弹出、知识卡点亮和柔和信息流。生成时引用团团、点点及本课新增角色图，保持形象一致。知识文字尽量短，建议后期叠字幕，避免乱码。旁白段落中团团和点点不要张嘴说话，只做观察、点头、指向、摆卡片等非对口型动作。"""

# Build header for lower
lower_header = """# 第8课《雾气里的照片》下集分镜稿
> **非常重要，必须严格遵守：以上传的图片作为关键帧画面；人物形象必须跟人物角色板保持一致，包括多视角、表情、服装、身体比例、局部细节和角色气质。**
## 基础设定
- 年龄：3-9岁
- 时长：约1分28秒
- 比例：16:9
- 主题：噪声 = 干扰信号
- 核心知识：噪声是混在信息里的干扰；噪声让信息变模糊、不清晰；信息不清晰，判断就容易出错；AI也会被噪声影响，做出错误判断；垃圾进，垃圾出——错误数据导致错误结果；信息越清晰、越准确，AI判断越靠谱
- 故事：团团和点点进入《雾气里的照片》的情境，通过一个具体问题、一次动手观察和一次清楚总结，把本课知识变成小朋友能看懂、能复述的小故事。
## 角色与风格
- 团团：7岁男孩，黑灰短发，圆脸腮红，橙色上衣，蓝色背带裤，小书包，好奇活泼。
- 点点：白色云朵形AI机器人，深色屏幕脸，青蓝发光眼睛，胸口屏幕，头顶紫色天线。
- 本课新增角色/场景：雾蒙蒙的窗户，窗外风景模糊不清，适合儿童。
- 风格：儿童水彩绘本动画风，清透明亮，高清质感，色彩饱和，减少模糊笔触，角色与上传参考图一致。
- 负面：不要写实摄影、3D塑料感、暗黑恐怖、角色变形、多余手指、文字乱码、画面拥挤、低清晰度。
- 旁白要求：旁白讲话时，团团和点点的嘴不要动，不要做对口型或配合讲话动作；只保持倾听、观察或轻微点头即可。
- 配音要求：发音清晰，全部使用标准普通话。
## 分镜
"""

lower_content = lower_header + '\n'.join(lower_with_titles) + """

## 生成建议
每镜只保留一个主要动作，优先轻推近、横移、角色观察、图标弹出、知识卡点亮和柔和信息流。生成时引用团团、点点及本课新增角色图，保持形象一致。知识文字尽量短，建议后期叠字幕，避免乱码。旁白段落中团团和点点不要张嘴说话，只做观察、点头、指向、摆卡片等非对口型动作。"""

with open(r'D:\PROJECTS\_AI\AIBook_Script\小云雀分镜稿\第8课-雾气里的照片_上集.md', 'w', encoding='utf-8') as f:
    f.write(upper_content)

with open(r'D:\PROJECTS\_AI\AIBook_Script\小云雀分镜稿\第8课-雾气里的照片_下集.md', 'w', encoding='utf-8') as f:
    f.write(lower_content)

print("Done! Upper and lower halves written.")
print(f"Upper shots: {len(upper_with_titles)}")
print(f"Lower shots: {len(lower_with_titles)}")
