import os
import re

lessons = {
    17: ("小云雀分镜稿/第17课-学校里的AI同学_上集.md",
          "小云雀分镜稿/第17课-学校里的AI同学_下集.md"),
    18: ("小云雀分镜稿/第18课-小狗学握手_上集.md",
          "小云雀分镜稿/第18课-小狗学握手_下集.md"),
    19: ("小云雀分镜稿/第19课-贴标签的老师_上集.md",
          "小云雀分镜稿/第19课-贴标签的老师_下集.md"),
    20: ("小云雀分镜稿/第20课-没有标签的玩具箱_上集.md",
          "小云雀分镜稿/第20课-没有标签的玩具箱_下集.md"),
    21: ("小云雀分镜稿/第21课-点亮聪明灯_上集.md",
          "小云雀分镜稿/第21课-点亮聪明灯_下集.md"),
    22: ("小云雀分镜稿/第22课-从边边角角到整张脸_上集.md",
          "小云雀分镜稿/第22课-从边边角角到整张脸_下集.md"),
    23: ("小云雀分镜稿/第23课-音量旋钮决定谁更重要_上集.md",
          "小云雀分镜稿/第23课-音量旋钮决定谁更重要_下集.md"),
    24: ("小云雀分镜稿/第24课-慢慢调准的小箭头_上集.md",
          "小云雀分镜稿/第24课-慢慢调准的小箭头_下集.md"),
    25: ("小云雀分镜稿/第25课-会接话的鹦鹉2.0_上集.md",
          "小云雀分镜稿/第25课-会接话的鹦鹉2.0_下集.md"),
    26: ("小云雀分镜稿/第26课-给AI的清楚指令_上集.md",
          "小云雀分镜稿/第26课-给AI的清楚指令_下集.md"),
    27: ("小云雀分镜稿/第27课-从乱点点到清图画_上集.md",
          "小云雀分镜稿/第27课-从乱点点到清图画_下集.md"),
    28: ("小云雀分镜稿/第28课-会编故事的机器人_上集.md",
          "小云雀分镜稿/第28课-会编故事的机器人_下集.md"),
    29: ("小云雀分镜稿/第29课-不要随便给陌生人_上集.md",
          "小云雀分镜稿/第29课-不要随便给陌生人_下集.md"),
    30: ("小云雀分镜稿/第30课-同样努力却分数不同_上集.md",
          "小云雀分镜稿/第30课-同样努力却分数不同_下集.md"),
    31: ("小云雀分镜稿/第31课-超级搭档_上集.md",
          "小云雀分镜稿/第31课-超级搭档_下集.md"),
}

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def get_lines(content):
    return content.split('\n')

def find_line_index(lines, condition):
    for i, line in enumerate(lines):
        if condition(line):
            return i
    return -1

def merge_lessons(part1_path, part2_path):
    p1 = read_file(part1_path)
    p2 = read_file(part2_path)
    l1 = get_lines(p1)
    l2 = get_lines(p2)

    # Extract title - remove 上集/下集 and clean
    raw_title = l1[0]
    title = re.sub(r'上集|下集|·', '', raw_title).strip()

    result = []

    # 1. Title
    result.append(title)
    result.append('')

    # 2. Important note
    result.append('> **非常重要，必须严格遵守：以上传的图片作为关键帧画面；人物形象必须跟人物角色板保持一致，包括多视角、表情、服装、身体比例、局部细节和角色气质。不要生成新的角色和场景，都用我指定的参考图。**')
    result.append('')

    # 3. Find 基础设定, 角色与风格 sections in p1
    # Find where 分镜 starts in p1 (look for ## 分镜)
    fengjing_idx_p1 = find_line_index(l1, lambda l: l.strip() == '## 分镜')

    # If not found, look for first ### heading with a number (01, 02, etc)
    if fengjing_idx_p1 == -1:
        fengjing_idx_p1 = find_line_index(l1, lambda l: bool(re.match(r'^### \d', l.strip())))

    # Find where 基础设定 starts
    basic_start = find_line_index(l1, lambda l: '## 基础设定' in l)
    if basic_start == -1:
        basic_start = 0

    # Copy 基础设定 and 角色与风格 (skip title, empty lines, important note)
    # Start from 基础设定 line
    for i in range(basic_start, fengjing_idx_p1):
        line = l1[i].rstrip()
        result.append(line)
    result.append('')

    # 4. 分镜 section
    result.append('## 分镜')
    result.append('')
    result.append('---')

    # Find where p1 分镜 content ends (before 生成与剪辑建议)
    tips_idx_p1 = find_line_index(l1, lambda l: '## 生成与剪辑建议' in l)
    if tips_idx_p1 == -1:
        tips_idx_p1 = len(l1)

    # Copy p1 分镜 content (skip the ## 分镜 header itself)
    for i in range(fengjing_idx_p1 + 1, tips_idx_p1):
        line = l1[i].rstrip()
        if line:  # Skip empty lines that might be just whitespace
            result.append(line)
    result.append('')
    result.append('---')

    # Find where 分镜 starts in p2
    fengjing_idx_p2 = find_line_index(l2, lambda l: l.strip() == '## 分镜')
    if fengjing_idx_p2 == -1:
        fengjing_idx_p2 = find_line_index(l2, lambda l: bool(re.match(r'^### \d', l.strip())))

    # Find where p2 分镜 content ends
    tips_idx_p2 = find_line_index(l2, lambda l: '## 生成与剪辑建议' in l)
    if tips_idx_p2 == -1:
        tips_idx_p2 = len(l2)

    # Copy p2 分镜 content
    for i in range(fengjing_idx_p2, tips_idx_p2):
        line = l2[i].rstrip()
        if line:
            result.append(line)
    result.append('')
    result.append('---')

    # 5. 生成与剪辑建议 from p2
    result.append('## 生成与剪辑建议')
    result.append('')

    tips_start_p2 = find_line_index(l2, lambda l: '## 生成与剪辑建议' in l)
    if tips_start_p2 != -1:
        for i in range(tips_start_p2 + 2, len(l2)):
            line = l2[i].rstrip()
            if line:
                result.append(line)

    return '\n'.join(result)

def main():
    output_dir = "小云雀分镜（全集）"
    os.makedirs(output_dir, exist_ok=True)

    for lesson_num in sorted(lessons.keys()):
        part1_path, part2_path = lessons[lesson_num]
        print(f"Processing lesson {lesson_num}...", end=" ")

        try:
            merged = merge_lessons(part1_path, part2_path)

            title_match = re.search(r'第(\d+)课《([^》]+)》', merged)
            if title_match:
                filename = f"第{title_match.group(1)}课-{title_match.group(2)}.md"
            else:
                filename = f"第{lesson_num}课_合并.md"

            output_path = os.path.join(output_dir, filename)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(merged)
            print(f"OK -> {filename}")

        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()
