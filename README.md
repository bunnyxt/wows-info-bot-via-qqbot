> ## Special notice: QQbot will be unavailable due to SmartQQ stop service on Jan. 1st 2019 and this plugin will be unavailable too. Thanks for your support and help!

# wows-info-bot-via-qqbot

A qq bot to provide info(etc. player stat and deto) of online PC game World of Warships(WoWS) via qqbot.

## Introduction

wows info bot via qqbot(wows info bot as follows) is a plugin of [qqbot](https://github.com/pandolia/qqbot) which provide players' statistics info of online PC game World of Warships(WoWS). This bot monitor qq group members' discussion and do the response to specific instructions.

**Notice**: The statistics info fetches from [Wargaming Official API](https://developers.wargaming.net) and you must agree with [Wargaming API Terms Of Use](https://developers.wargaming.net/documentation/rules/agreement/). If you do not agree with the term above, you **SHOULD NOT** use this bot plugin.

Official QQ group for testing and feedback 891803204.

## Installation

This plugin is based on Python 3.6. Although qqbot just need Python 2.7/3.4+, some syntax and function features may not supported by former versions so Python 3.6 is strongly recommended, or you may need some time to fix problems before enjoy it.

To start wows info bot, you need to install [qqbot](https://github.com/pandolia/qqbot) first. You can use pip to install qqbot.

`pip install qqbot`

Then download files of this plugin and put them into plugin folder of qqbot at `~/.qqbot-tmp/plugins/`( ~ represents user folder, for example in win7 it should be `C:\Users\xxx` ).

Open `config.py.sample` file with notepad, fill in all the parameters surrounded by <>. In the latest version, you just need to fill in your wargaming application id(**Notice: NOT YOUR WARGAMING ACCOUNT ID**) which can apply from [Wargaming Developer's Room](https://developers.wargaming.net/applications/). After that, rename file to `config.py` before start this plugin.

Start qqbot and open another console. Use `qq plug wowsinfo` to start wows info bot.

More info related to qqbot plugin can be found in the qqbot [readme](https://github.com/pandolia/qqbot).

## Instructions Usage

You can send instruction to bot either directly or in a group which bot also joined except some special instruction. Of course you can change this and other details, even add new instructions on your own!

### -start & -stop

Use `-start wowsinfo` to start bot if bot closed before.(by default the bot has been started when start wows info bot plugin)

Use `-stop wowsinfo` to stop bot. **Notice**: This is used to start or stop this plugin, not qqbot. **These two instructions only works when send by bot's buddy, not in the group.**

### -time

Use `-time` to get system time. 

### -echo

Usage `-echo <content>`

Send content back, just like `echo` instruction in Linux.

### -deto

Usage `-deto <user_name>`

Show player detonation info(deto count & deto ratio last week & overall with rank number(marked with #)) fetched from [WOWS Detonation Ranking](http://deto.bunnyxt.com). **Only deto info of players from ASIA server available.**

You do not need to type in accurate user_name because it's case insensitive and has automatic completion. For example, input "himeuz" can find player "HimeUzuki" since no other player user_name start with "himeuz" and it's case insensitive.

### -info

Usage `-info [-cv|bb|ca|dd|all] [-r=eu|ru|na|asia] <user_name>`

Show player pvp statistics info(battles, win rate, main battery hit ratio, PR, average damage dealt, max damage dealt) and other detail info when given specific paramneters.

`-cv|bb|ca|dd|all`, show 3 most played ship(with type cv|bb|ca|dd or all ships) statistics info in pvp mode.

`-r=eu|ru|na|asia`, select player server which is asia on default.

For example, `-info -dd -r=asia himeuz` means that show general pvp statistics info and 3 most played distroyer statistics info of asia server player whose user_name like "himeuz" most.

## Meme Usage

You can change `meme.py` to add your user_name map and meme map.

### user_name_map

Since some players' user name too long or has other nickname known by others and this will not cause ambigious, you can use this nickname to query statistics of this player.

For example, in user_meme_map, `'didi': 'Cyclopenta_pentalene '` means that you can use `-info didi` instead of `-info Cyclopenta_pentalene`.

### meme_map

You can show some other words after display of statistics info to make fun. 

For example, in meme_map, 

```
'Cyclopenta_pentalene': [
    '\n"tql"',
    '\n"dalao"',
    '\n"头爷爷带带我"',
    '\n"⬆️看见没这就是dalao"',
    '\n"卧槽牛逼啊"',
    '\n"落霞与孤呜起飞，秋水共长天一色"'
]
```

means that after display player Cyclopenta_pentalene's info, one of these meme sentences will be shown.

Notice: These sentences should start with `\n` for starting a new line.

## Bonus Code

Try `-info momotxdi` several times and pay attention to `avgdmg` field!

## Special Thanks

- [Wargaming Developer's Room](https://developers.wargaming.net) for players' data.
- [pandolia](https://github.com/pandolia) and his project [qqbot](https://github.com/pandolia/qqbot) for wonderful bot framework on qq.
- [Hawkilo](https://asia.wows-numbers.com/player/2009240681,Hawkilo/) dalao for idea proposing and testing.
- [SweetFairyTale](https://github.com/SweetFairyTale) dalao for support and encouragement.
