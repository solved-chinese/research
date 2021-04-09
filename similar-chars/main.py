import numpy as np
from PIL import Image, ImageDraw, ImageFont
from PIL import ImageChops

from hanzi_chaizi import HanziChaizi


def _generate_img_from_char(char, img_size=50, font_weight='Bold', color=255):
    margin = img_size // 40
    font_size = img_size - 2 * margin
    assert font_weight in ('Medium', 'Bold', 'Heavy')
    font_path = '/Users/george/Library/Fonts/SourceHanSansCN-{}.otf'.format(font_weight)
    chn_font = ImageFont.truetype(font_path, font_size)
    img = Image.new('L', (img_size, img_size), color=color)

    draw = ImageDraw.Draw(img)
    draw.text((margin, margin), char, fill=0, font=chn_font)

    return img


def _distance_between(img1, img2):
    diff_img = ImageChops.difference(img1, img2)
    distance = np.sum(np.array(diff_img))
    return distance


def find_similar_chars_by_img(target_char, debug=False):
    threshold = 50 * 50 ** 2
    result = []

    target_img = _generate_img_from_char(target_char)
    for compare_char in all_chars:
        if compare_char == target_char:
            continue
        compare_img = _generate_img_from_char(compare_char)
        dist = _distance_between(target_img, compare_img)
        if dist < threshold:
            result.append(compare_char)
            if debug:
                print('({} {}): {}'.format(target_char, compare_char, dist))

    return result


def find_similar_chars_by_structure(target_char, debug=False):
    result = []

    target_structure = splitter.query(target_char)
    for compare_char in all_chars:
        if compare_char == target_char:
            continue
        
        try:
            compare_structure = splitter.query(compare_char)
        except Exception:
            continue
        if len(compare_structure) != len(target_structure):
            continue # TODO: 可能存在不同结构数量的易混字

        for i in range(len(compare_structure)):
            if target_structure[i] == compare_structure[i] or \
                ambiguous_counterpart.get(target_structure[i]) == compare_structure[i] or \
                target_structure[i] == ambiguous_counterpart.get(compare_structure[i]):
                continue
            else:
                break
        else:
            result.append(compare_char)
            if debug:
                print('({} {})'.format(target_char, compare_char))

    return result




target_char = '话'

splitter = HanziChaizi()
# ambiguous = (('言', '辵'), ('人', '彳'))
ambiguous_counterpart = {'言': '辵', '人': '彳'} # order doesn't matter...?
with open('gb2312.txt', encoding='utf-8') as f:
    all_chars = list(f.readline().strip())

print('Target: {}'.format(target_char))
print(find_similar_chars_by_img(target_char))
print(find_similar_chars_by_structure(target_char))

# 时对 话适 问间
# 视见
