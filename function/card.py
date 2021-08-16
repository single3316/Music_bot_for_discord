import numpy as np
from PIL import Image, ImageDraw
from PIL import Image, ImageFont, ImageDraw
import requests


def create_personal_card(url, rank, score, level, name):
    save_img(url)
    cut_image("images/w.png")
    phon = Image.open('images/phon.png')
    av = Image.open('images/w.png')
    phon.paste(av, (50, 75), av)
    phon.save('images/w.png', 'png')
    im = Image.open('images/w.png')
    draw_rank = ImageDraw.Draw(im)
    font = ImageFont.truetype('font/main.otf', size=40)
    name_font = ImageFont.truetype('font/main.otf', size=50)
    draw_rank.text((340, 60), name, fill=('#00a8f0'), font=name_font)
    draw_rank.text((350, 160), f'Rating: {rank}', fill=('#00a8f0'), font=font)
    draw_rank.text((350, 260), f'Score: {score}/100', fill=('#00a8f0'), font=font)
    draw_rank.text((350, 210), f'Level: {level}', fill=('#00a8f0'), font=font)
    im.save('images/w.png','png')


def create_rating_card(user_list):
    wall = Image.open('images/vertical.png')
    draw_text = ImageDraw.Draw(wall)
    font = ImageFont.truetype('font/main.otf', size=50)
    draw_text.text((120, 20), 'rating',fill=('#00a8f0'), font=font)
    numb = ImageFont.truetype('font/main.otf', size=34)
    font = ImageFont.truetype('font/main.otf', size=26)
    h = 100
    for i in user_list:
        save_img(i[1])
        cut_image("images/w.png")
        av = Image.open('images/w.png')
        wall.paste(av, (60, h+20), av)
        draw_text.text((20, h+40), str(i[2]), fill=('#00a8f0'), font=numb)
        if h == 700:
            draw_text.text((200, h + 40), i[0]+' (ВЫ)', fill=('#00a8f0'), font=font)
        else:
            draw_text.text((200, h+40), i[0], fill=('#00a8f0'), font=font)
        h += 100
    wall.save('images/w.png', 'png')


def save_img(url, numb=None):
    try:
        resp = requests.get(url, stream=True).raw
    except requests.exceptions.RequestException:
        print('Error')
    try:
        img = Image.open(resp)
    except IOError:
        print("Unable to open image")
    img.save('images/w.png', 'png')


def cut_image(href):
    img = Image.open(href).convert("RGB")
    npImage = np.array(img)
    h, w = img.size
    alpha = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(alpha)
    draw.pieslice([0, 0, h, w], 0, 360, fill=255)
    npAlpha = np.array(alpha)
    npImage = np.dstack((npImage, npAlpha))
    Image.fromarray(npImage).save(href)
