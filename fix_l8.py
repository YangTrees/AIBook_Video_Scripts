import re

with open(r'D:\PROJECTS\_AI\AIBook_Script\小云雀分镜（全集）\第8课-雾气里的照片_合并版.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix important notice
old_notice = '**非常重要，必须严格遵守：关键帧画面风格必须跟故事板图片保持一致；人物形象必须跟人物角色板保持一致，包括多视角、表情、服装、身体比例、局部细节和角色气质。**'
new_notice = '**非常重要，必须严格遵守：以上传的图片作为关键帧画面；人物形象必须跟人物角色板保持一致，包括多视角、表情、服装、身体比例、局部细节和角色气质。**'
content = content.replace(old_notice, new_notice)

# Remove the second "### 08" block (duplicate 核心知识揭示)
pattern = r'\n### 08\. 核心知识揭示 01:32-01:48.*?(?=\n### 09\. 信息连接现实)'
content = re.sub(pattern, '', content, flags=re.DOTALL)

with open(r'D:\PROJECTS\_AI\AIBook_Script\小云雀分镜（全集）\第8课-雾气里的照片_合并版.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")
