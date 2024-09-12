from PIL import Image, ImageDraw, ImageFont
import random
import textwrap
import csv
import time
import os
import ctypes

from pandas.compat import platform

default_second = 30

directory = "."
dir_path = os.listdir(directory)

for item in dir_path:
    if item.endswith(".png"):
        os.remove(os.path.join(directory, item))

#=======================================================================#
memo = []
with open("vocabs.csv") as cs:
    iter = csv.reader(cs, delimiter=",")
    for x in iter:
        memo.append(x[1:])
memo = memo[1:]
change = 1
while 1:
    x = random.randint(0, len(memo)-1)
    now = memo[x]
    if now[0] == " ":
        continue
    screen_w, screen_h, total_h, max_w = 1600, 900, 0, 0
    screen_size = (screen_w, screen_h)
    background_color = (255, 255, 255, 255) #FFFFFF
    image = Image.new("RGB", screen_size, background_color)
    draw = ImageDraw.Draw(image)

    word_vocab = now[0]
    word_part_meaning = now[1] + ' ' + now[2]
    word_example = now[3].replace("(","").replace(")","")

    word_part_meaning_2 = ""
    word_example_2 = ""

    word_part_meaning_3 = ""
    word_example_3 = ""

    if x+1 < len(memo):
        if memo[x+1][0] == " ":
            now_2 = memo[x+1]
            word_part_meaning_2 = now_2[1] + ' ' + now_2[2]
            word_example_2 = now_2[3].replace("(","").replace(")","")
        if x+2 < len(memo):
            if memo[x+2][0] == " ":
                now_3 = memo[x+2]
                word_part_meaning_3 = now_3[1] + ' ' + now_3[2]
                word_example_3 = now_3[3].replace("(","").replace(")","")

    #=======================================================================#
    font_bold = ImageFont.truetype("EBGaramond-Bold.ttf", size=50)
    _, _, font_bold_size_w, font_bold_size_h = font_bold.getbbox(word_vocab)
    total_h += font_bold_size_h
    font_semibold = ImageFont.truetype("EBGaramond-SemiBold.ttf", size=30)
    font_italic = ImageFont.truetype("EBGaramond-Regular.ttf", size=30)
    for line in textwrap.wrap(word_part_meaning, width=80):
        _,_,temp_w,temp_h = font_semibold.getbbox(line)
        total_h += temp_h
        max_w = max(max_w, temp_w)
    for line in textwrap.wrap(word_example, width=80):
        _,_,temp_w,temp_h = font_italic.getbbox(line)
        total_h += temp_h
        max_w = max(max_w, temp_w)
    if x+1 < len(memo):
        if memo[x+1][0] == " ":
            for line in textwrap.wrap(word_part_meaning_2, width=80):
                _,_,temp_w,temp_h = font_semibold.getbbox(line)
                total_h += temp_h
                max_w = max(max_w, temp_w)
            for line in textwrap.wrap(word_example_2, width=80):
                _,_,temp_w,temp_h = font_italic.getbbox(line)
                total_h += temp_h
                max_w = max(max_w, temp_w)
            if x+2 < len(memo):
                if memo[x+2][0] == " ":
                    #total_h += 10
                    for line in textwrap.wrap(word_part_meaning_3, width=80):
                        _,_,temp_w,temp_h = font_semibold.getbbox(line)
                        total_h += temp_h
                        max_w = max(max_w, temp_w)
                    for line in textwrap.wrap(word_example_3, width=80):
                        _,_,temp_w,temp_h = font_italic.getbbox(line)
                        total_h += temp_h
                        max_w = max(max_w, temp_w)

    #=======================================================================#
    max_w += 30
    pos_w = screen_w - max_w
    pos_w /= 2
    pos_h = screen_h-total_h
    pos_h /= 2

    #=======================================================================#
    draw.text((pos_w, pos_h), word_vocab, font=font_bold, fill="black")
    pos_h += font_bold_size_h
    for line in textwrap.wrap(word_part_meaning, width=80):
        draw.text((pos_w, pos_h), line, font=font_semibold, fill="black")
        _,_,_,h = font_semibold.getbbox(line)
        pos_h += h
    for line in textwrap.wrap(word_example, width=80):
        draw.text((pos_w+30, pos_h), line, font=font_italic, fill="black")
        _,_,_,h = font_semibold.getbbox(line)
        pos_h += h
    if x+1 < len(memo):
        if memo[x+1][0] == " ":
            for line in textwrap.wrap(word_part_meaning_2, width=80):
                draw.text((pos_w, pos_h), line, font=font_semibold, fill="black")
                _,_,_,h = font_semibold.getbbox(line)
                pos_h += h
            for line in textwrap.wrap(word_example_2, width=80):
                draw.text((pos_w+30, pos_h), line, font=font_italic, fill="black")
                _,_,_,h = font_semibold.getbbox(line)
                pos_h += h
            if x+2 < len(memo):
                if memo[x+2][0] == " ":
                    for line in textwrap.wrap(word_part_meaning_3, width=80):
                        draw.text((pos_w, pos_h), line, font=font_semibold, fill="black")
                        _,_,_,h = font_semibold.getbbox(line)
                        pos_h += h
                    for line in textwrap.wrap(word_example_3, width=80):
                        draw.text((pos_w+30, pos_h), line, font=font_italic, fill="black")
                        _,_,_,h = font_semibold.getbbox(line)
                        pos_h += h

    #=======================================================================#
    image.save(f"./{change}.png", "PNG")
    if os.path.exists(f"./{change-1}.png"):
        os.remove(f"./{change-1}.png")

    if platform.system() == "Linux" :
        os.system("""
            qdbus org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript '
                var allDesktops = desktops();
                for (i=0;i<allDesktops.length;i++)
                {{
                    d = allDesktops[i];
                    d.wallpaperPlugin = "org.kde.image";
                    d.currentConfigGroup = Array("Wallpaper", "org.kde.image", "General");
                    d.writeConfig("Image", "file://{0}/{1}.png")
                }}
            '""".format(os.getcwd(),change))
    elif platform.system() == "Windows":
        ctypes.windll.user32.SystemParametersInfoW(20, 0, "{0}/{1}".format(os.getcwd(), change) , 0)

    change += 1
    time.sleep(default_second)
