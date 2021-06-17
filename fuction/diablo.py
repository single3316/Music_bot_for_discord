import requests
import bs4
import config
import discord


def get_category_name(cat):
    if cat == 'шлем':
        names = ['helm/', 'voodoo-mask/', 'spirit-stone/', 'wizard-hat/']
    elif cat == 'плечи':
        names = ['pauldrons/']
    elif cat == 'корпус':
        names = ['chest-armor/', 'cloak/']
    elif cat == 'запястья':
        names = ['bracers/']
    elif cat == 'кисти':
        names = ['gloves/']
    elif cat == 'пояс':
        names = ['belt/', 'mighty-belt/']
    elif cat == 'ноги':
        names = ['pants/']
    elif cat == 'боты':
        names = ['boots/']
    elif cat == 'ювелирка':
        names = ['amulet/', 'ring/']
    elif cat == 'доп':
        names = ['shield/', 'crusader-shield/', 'mojo/', 'orb/', 'quiver/', 'phylactery/']
    elif cat == 'спутник':
        names = ['enchantress-focus/', 'scoundrel-token/', 'templar-relic/']
    elif cat == 'оружие':
        names = ['axe-1h/', 'axe-2h/', 'dagger/', 'mace-1h/', 'mace-2h/', 'spear/', 'sword-1h/', 'sword-2h/',
                 'ceremonial-knife/',
                 'fist-weapon/', 'flail-1h/', 'flail-2h/', 'mighty-weapon-1h/', 'mighty-weapon-2h/', 'scythe-1h/',
                 'scythe-2h/',
                 'polearm/', 'staff/', 'daibo/', 'bow/', 'crossbow/', 'hand-crossbow/', 'wand/']
    elif cat == 'зелья':
        names = ['potion/']
    elif cat == 'прочее':
        names = ['blacksmith-plan/', 'jeweler-design/', 'page-of-training/', 'dye/', 'gem/', 'misc/']
    else:
        names = ['blacksmith-plan/', 'jeweler-design/', 'page-of-training/', 'dye/', 'gem/', 'misc/']
    return names


def parsing_item(item_name: str, category):
    for i in category:
        url = config.DIABLO_ITEM_URL + i
        r = requests.get(str(url))
        bs: bs4.BeautifulSoup = bs4.BeautifulSoup(r.text, "html.parser")
        blocks = bs.findAll("div", class_="item-details-text")
        for i in blocks:
            name = i.find('a').text
            if item_name.lower() in name.lower():
                return get_item_attribute('https://diablo3.blizzard.com/' + i.find('a').get('href'))


def get_item_attribute(url):
    print(url)
    text = ''
    r = requests.get(url)
    bs: bs4.BeautifulSoup = bs4.BeautifulSoup(r.text, "html.parser")
    details = bs.find(class_='detail-text')
    item_type = details.find('ul', class_='item-type').find('span').text.lower()[:3]
    image_url = bs.find('span', class_='icon-item-default').get('style').split()[1][4:-2]
    text += '\n**Минимальный уровень: ' + bs.find('span', class_='detail-level-number').text + '**\n\n'
    if item_type in 'компо':
        color = discord.Colour.dark_green()
        sett = details.find('ul', class_='item-itemset').findAll('li', class_='item-itemset-piece')
        text += '**Комплект состоит из**\n```'
        for i in sett:
            text += i.text[1:]
        text += '```'
        effects = details.find('ul', class_='item-itemset').findAll('span')
        text += '**Эффекты комплекта**\n```'
        h = 1
        for i in effects:
            if h >= 3:
                text += i.text + '\n'
            h += 1
        text += '```'
    elif item_type in 'легендарн':
        color = discord.Colour.dark_gold()
        effects = details.find('ul', class_='item-effects').find('span', class_='d3-color-ffff8000')
        if effects is not None:
            text += '**Эффект легендарочки**\n`' + effects.text + '`'
    elif item_type in 'редкий':
        color = 16705372
    elif item_type in 'магич':
        color = discord.Colour.blue()
    else:
        color = discord.Colour.light_gray()
    name = details.find('h2', class_='header-2').text
    embed = discord.Embed(description=text, title=name, colour=color)
    embed.set_image(url=image_url)
    return embed
