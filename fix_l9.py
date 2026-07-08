# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

src = r'D:\PROJECTS\_AI\AIBook_Script\小云雀分镜（全集）\第9课-红灯停绿灯行.md'
with open(src, 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Find shots section
idx1 = text.find('## 分镜')
idx2 = text.find('## 生成建议')
shots_section = text[idx1 + len('## 分镜'):idx2]
header = text[:idx1 + len('## 分镜')].strip()

# Parse each shot block
shots_section = re.sub(r'(?<!\n)(?=### \d{2}\.)', '\n', shots_section)
blocks = re.split(r'\n(?=### \d{2}\.)', shots_section.strip())
blocks = [b.strip() for b in blocks if b.strip() and '###' in b]

shots = []
for blk in blocks:
    first_line_m = re.match(r'(### \d{2}\.\s+.+?)\s+(\d{2}:\d{2}-\d{2}:\d{2})\s*$', blk.split('\n')[0])
    if not first_line_m:
        continue
    header_part = first_line_m.group(1)
    tc = first_line_m.group(2)
    rest = '\n'.join(blk.split('\n')[1:])
    hua_m = re.search(r'画面：(.+?)(?=\n台词/旁白：)', rest, re.DOTALL)
    pb_m = re.search(r'台词/旁白：(.+?)(?=\n关键帧：)', rest, re.DOTALL)
    kf_m = re.search(r'关键帧：(.*)$', rest, re.DOTALL)
    shots.append({
        'header': header_part,
        'tc': tc,
        'hua': hua_m.group(1).strip() if hua_m else '',
        'panbai': pb_m.group(1).strip() if pb_m else '',
        'keyframe': kf_m.group(1).strip() if kf_m else ''
    })

print(f"Parsed {len(shots)} shots")

# Split: upper = 1-6, lower = 7-9
upper_shots = shots[:6]
lower_shots = shots[6:]

# Time offsets: upper starts 00:00, lower starts 00:00
# Calculate actual durations from original timecodes
def parse_tc(tc_str):
    start, end = tc_str.split('-')
    sh, sm = int(start.split(':')[0]), int(start.split(':')[1])
    eh, em = int(end.split(':')[0]), int(end.split(':')[1])
    start_s = sh*60 + sm
    end_s = eh*60 + em
    return start_s, end_s, end_s - start_s

# Get durations
upper_durs = []
for s in upper_shots:
    _, _, d = parse_tc(s['tc'])
    upper_durs.append(d)

lower_durs = []
for s in lower_shots:
    _, _, d = parse_tc(s['tc'])
    lower_durs.append(d)

print(f"Upper: {len(upper_shots)} shots, {sum(upper_durs)}s total")
print(f"Lower: {len(lower_shots)} shots, {sum(lower_durs)}s total")

# Standard titles
upper_titles = ['故事开场', '今天学什么', '第一个发现', '动手试一试', '规则出现', '换一种方式看']
lower_titles = ['核心知识揭示', '效果展示', '信息连接现实', '神奇时刻', '知识总结', '动手与预告']

# If lower has only 3 shots, use first 3 of lower_titles
lower_titles_used = lower_titles[:len(lower_shots)]

def tc_fmt(s):
    return f'{int(s//60):02d}:{int(s%60):02d}'

# Build timecodes for upper (starts 00:00)
def build_tcs(durations):
    tcs = []
    cumsum = 0
    for d in durations:
        tcs.append(f'{tc_fmt(cumsum)}-{tc_fmt(cumsum+d)}')
        cumsum += d
    return tcs

upper_tcs = build_tcs(upper_durs)
lower_tcs = build_tcs(lower_durs)

# Build header for upper
upper_header = """# 第9课《红灯停绿灯行》上集分镜稿

> **非常重要，必须严格遵守：以上传的图片作为关键帧画面；人物形象必须跟人物角色板保持一致，包括多视角、表情、服装、身体比例、局部细节和角色气质。**

## 基础设定

- 年龄：3-9岁
- 时长：约1分43秒
- 比例：16:9
- 主题：条件判断 = 如果...那么...
- 核心知识：条件判断根据条件决定做什么；如果满足条件，就执行对应的动作；条件可以叠加（而且）；多个条件叠加让规则更复杂
- 故事：团团和点点进入《红灯停绿灯行》的情境，通过一个具体问题、一次动手观察和一次清楚总结，把本课知识变成小朋友能看懂、能复述的小故事。

## 角色与风格

- 团团：7岁男孩，黑灰短发，圆脸腮红，橙色上衣，蓝色背带裤，小书包，好奇活泼。
- 点点：白色云朵形AI机器人，深色屏幕脸，青蓝发光眼睛，胸口屏幕，头顶紫色天线。
- 本课新增角色/场景：十字路口场景，红绿灯装置可爱醒目，小汽车模型。
- 风格：儿童水彩绘本动画风，清透明亮，高清质感，色彩饱和，减少模糊笔触，角色与上传参考图一致。
- 负面：不要写实摄影、3D塑料感、暗黑恐怖、角色变形、多余手指、文字乱码、画面拥挤、低清晰度。
- 旁白要求：旁白讲话时，团团和点点的嘴不要动，不要做对口型或配合讲话动作；只保持倾听、观察或轻微点头即可。
- 配音要求：发音清晰，全部使用标准普通话，快语速朗读。

## 分镜
"""

upper_parts = []
for i, (s, t) in enumerate(zip(upper_shots, upper_tcs)):
    title = upper_titles[i] if i < len(upper_titles) else re.search(r'### \d{2}\.\s+([^\d]+)', s['header']).group(1).strip()
    upper_parts.append(f"### {i+1:02d}. {title} {t}\n画面：{s['hua']}\n台词/旁白：{s['panbai']}\n关键帧：{s['keyframe']}\n")

upper_content = upper_header + '\n'.join(upper_parts) + """

## 生成建议

每镜只保留一个主要动作，优先轻推近、横移、角色观察、图标弹出、知识卡点亮和柔和信息流。生成时引用团团、点点及本课新增角色图，保持形象一致。知识文字尽量短，建议后期叠字幕，避免乱码。旁白段落中团团和点点不要张嘴说话，只做观察、点头、指向、摆卡片等非对口型动作。"""

# Build header for lower
lower_header = """# 第9课《红灯停绿灯行》下集分镜稿

> **非常重要，必须严格遵守：以上传的图片作为关键帧画面；人物形象必须跟人物角色板保持一致，包括多视角、表情、服装、身体比例、局部细节和角色气质。**

## 基础设定

- 年龄：3-9岁
- 时长：约1分14秒
- 比例：16:9
- 主题：条件判断 = 如果...那么...
- 核心知识：条件判断根据条件决定做什么；如果满足条件，就执行对应的动作；条件可以叠加（而且）；多个条件叠加让规则更复杂；电脑靠无数个"如果...就..."运行
- 故事：团团和点点进入《红灯停绿灯行》的情境，通过一个具体问题、一次动手观察和一次清楚总结，把本课知识变成小朋友能看懂、能复述的小故事。

## 角色与风格

- 团团：7岁男孩，黑灰短发，圆脸腮红，橙色上衣，蓝色背带裤，小书包，好奇活泼。
- 点点：白色云朵形AI机器人，深色屏幕脸，青蓝发光眼睛，胸口屏幕，头顶紫色天线。
- 本课新增角色/场景：十字路口场景，红绿灯装置可爱醒目，小汽车模型。
- 风格：儿童水彩绘本动画风，清透明亮，高清质感，色彩饱和，减少模糊笔触，角色与上传参考图一致。
- 负面：不要写实摄影、3D塑料感、暗黑恐怖、角色变形、多余手指、文字乱码、画面拥挤、低清晰度。
- 旁白要求：旁白讲话时，团团和点点的嘴不要动，不要做对口型或配合讲话动作；只保持倾听、观察或轻微点头即可。
- 配音要求：发音清晰，全部使用标准普通话，快语速朗读。

## 分镜
"""

lower_parts = []
for i, (s, t) in enumerate(zip(lower_shots, lower_tcs)):
    title = lower_titles_used[i] if i < len(lower_titles_used) else re.search(r'### \d{2}\.\s+([^\d]+)', s['header']).group(1).strip()
    lower_parts.append(f"### {i+1:02d}. {title} {t}\n画面：{s['hua']}\n台词/旁白：{s['panbai']}\n关键帧：{s['keyframe']}\n")

lower_content = lower_header + '\n'.join(lower_parts) + """

## 生成建议

每镜只保留一个主要动作，优先轻推近、横移、角色观察、图标弹出、知识卡点亮和柔和信息流。生成时引用团团、点点及本课新增角色图，保持形象一致。知识文字尽量短，建议后期叠字幕，避免乱码。旁白段落中团团和点点不要张嘴说话，只做观察、点头、指向、摆卡片等非对口型动作。"""

with open(r'D:\PROJECTS\_AI\AIBook_Script\小云雀分镜稿\第9课-红灯停绿灯行_上集.md', 'w', encoding='utf-8') as f:
    f.write(upper_content)
with open(r'D:\PROJECTS\_AI\AIBook_Script\小云雀分镜稿\第9课-红灯停绿灯行_下集.md', 'w', encoding='utf-8') as f:
    f.write(lower_content)

print("\nUpper (6 shots):")
for i, (s, t) in enumerate(zip(upper_shots, upper_tcs)):
    print(f"  {i+1:02d}. {upper_titles[i]} {t}")
print(f"\nLower (3 shots):")
for i, (s, t) in enumerate(zip(lower_shots, lower_tcs)):
    print(f"  {i+1:02d}. {lower_titles_used[i]} {t}")

print("\nDone!")
