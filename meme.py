import random

user_name_map = {
    ' /Emoji128054': '_Kill_All ',
    ' /Emoji128049': '_Clear_All ',
    ' /Emoji127746': 'HimeYamato ',
    'didi': 'Cyclopenta_pentalene '
}

meme_map = {
    '_Kill_All': [
        '\n"贝贝tql"',
        '\n"是🐶王！"'
    ],
    '_Clear_All': [
        '\n"啊，是🐱🐱guai，wsl"',
        '\n"吸吸吸吸吸🐱🐱"'
    ],
    'HimeYamato': [
        '\n"伞姐永远是我们老大"',
        '\n"🌂🌂mua！"'
    ],
    'momotxdi': [
        '\n"系统提示："',
        '\n"摸摸堂兄弟"'
    ],
    'Cyclopenta_pentalene': [
        '\n"tql"',
        '\n"dalao"',
        '\n"头爷爷带带我"',
        '\n"⬆️看见没这就是dalao"',
        '\n"卧槽牛逼啊"',
        '\n"落霞与孤呜起飞，秋水共长天一色"'
    ]
}


def user_name_mapping(content):
    for unkey in user_name_map.keys():
        if unkey in content:
            content = content.replace(unkey, user_name_map[unkey])
    return content


def meme_mapping(nickname):
    meme = ''
    if nickname in meme_map.keys():
        meme = meme_map[nickname][random.randint(
            0, len(meme_map[nickname]) - 1)]
    return meme
