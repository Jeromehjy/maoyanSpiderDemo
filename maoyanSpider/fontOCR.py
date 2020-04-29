import pytesseract
from PIL import Image, ImageDraw, ImageFont
import numpy
from fontTools.ttLib import TTFont

def font_convert(font_name):
    # 获取字体的映射规则
    base_font = TTFont(font_name)
    code_list = base_font.getGlyphOrder()[2:]
    # 创建一张图片 用来把字体画上去
    im = Image.new("RGB", (1800, 1800), (255, 255, 255))
    image_draw = ImageDraw.Draw(im)
    base_font = ImageFont.truetype(font_name,80)
    # 等分成一份
    count = 1
    # 等分成一份
    array_list = numpy.array_split(code_list, count)
    for i in range(len(array_list)):
        # 讲javascript的unicode码变成python总的unicode码
        new_list = [i.replace("uni", "\\u") for i in array_list[i]]
        text = "".join(new_list)
        text = text.encode('utf-8').decode('unicode_escape')
        # print('text:', text)
        # 把反向编码的 文字写在图片上            要使用的字体
        image_draw.text((0, 100 * i), text, font=base_font, fill="#000000")
    # im.save("font_2_str.jpg")
    # im.show()
    # im = Image.open("font_2_str.jpg")  # 可以将图片保存到本地，以便于手动打开图片查看
    # 识别图片中的文字
    result = pytesseract.image_to_string(im)
    # # 去除空白及换行
    result_str = result.replace(" ", "").replace("\n", "")
    # 将内容替换成网页的格式，准备去网页中进行替换
    html_code_list = [i.replace("uni", "&#x").lower() + ";" for i in code_list]
    # print(len(html_code_list))
    # print(len(result_str))
    return dict(zip(html_code_list, list(result_str)))
