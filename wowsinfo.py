import re
import pymysql
import urllib
import json
import random
import time

import ship
import wgapi
import detoapi
import meme

# latest date
latest_date = bytes.decode(detoapi.get_latest_date())

# wows info bot works only if wowsinfo_flag = true
wowsinfo_flag = True


class ResponseWrapper:
    def __init__(self):
        self.type = ''
        self.reply_prompt = ''
        self.error_prompt = ''
        self.time = ''
        self.echo = ''
        self.deto = ''  # TODO rewrite it after rewrite deto part
        self.name_alter_prompt = ''
        self.clan_tag_with_brackets = ''
        self.nickname = ''
        self.info = ''
        self.category_display = ''
        self.meme = ''

    def to_string(self):
        s = self.reply_prompt
        if self.type == 'error':
            s += self.error_prompt
        elif self.type == '-time':
            s += self.time
        elif self.type == '-echo':
            s += self.echo
        elif self.type == '-deto':
            s += self.name_alter_prompt
            s += 'user {0}{1}\n'.format(self.clan_tag_with_brackets,
                                        self.nickname)
            s += self.deto
            s += self.meme
        elif self.type == '-info':
            s += self.name_alter_prompt
            s += 'user {0}{1}\n'.format(self.clan_tag_with_brackets,
                                        self.nickname)
            s += self.info
            s += self.category_display
            s += self.meme
        return s


def send_via_rw(bot, contact, rw):
    bot.SendTo(contact, rw.to_string())


def gain_clan_tag_with_brackets(account_id):
    clan_tag_with_brackets = ''
    player_clan_data = wgapi.get_player_clan_data(account_id)
    if player_clan_data:
        if player_clan_data['data'][str(account_id)]:
            clan_id = player_clan_data['data'][str(
                account_id)]['clan_id']
            if clan_id:
                clan_details = wgapi.get_clan_details(clan_id)
                if clan_details:
                    clan_tag_with_brackets = '[{0}]'.format(
                        clan_details['data'][str(clan_id)]['tag'])
    return clan_tag_with_brackets


def ship_belong_to_category(ship_id, ship_category):
    if ship_category.lower() == 'all':
        return True

    s_c = ''
    if ship_category.lower() == 'cv':
        s_c = 'AirCarrier'
    elif ship_category.lower() == 'bb':
        s_c = 'Battleship'
    elif ship_category.lower() == 'ca':
        s_c = 'Cruiser'
    elif ship_category.lower() == 'dd':
        s_c = 'Destroyer'

    if ship_id not in ship.ship_dict.keys():
        return False

    if ship.ship_dict[ship_id].type == s_c:
        return True
    else:
        return False


def gain_ship_detail_display(account_id, ship_category):
    player_ship_stats = wgapi.get_player_ship_stats(account_id)

    selected_ship_stats = []
    for s in player_ship_stats['data'][str(account_id)]:
        ship_id = s['ship_id']
        if ship_belong_to_category(ship_id, ship_category):
            selected_ship_stats.append(s)

    selected_ship_stats.sort(key=lambda s: s['pvp']['battles'], reverse=True)

    ship_detail_display = ''
    _len = len(selected_ship_stats)
    if _len > 3:
        _len = 3
    for i in range(0, _len):
        _ship_name = ship.ship_dict[selected_ship_stats[i]['ship_id']].name
        _battles = selected_ship_stats[i]['pvp']['battles']
        _wins = selected_ship_stats[i]['pvp']['wins']
        _damage_dealt = selected_ship_stats[i]['pvp']['damage_dealt']
        _wr = 0
        _avgdmg = 0
        if _battles != 0:
            _wr = _wins / _battles
            _avgdmg = _damage_dealt / _battles
        ship_detail_display += '\n{0}. {1}\nbattles {2} wr {3}% avgdmg {4}'.format(
            i + 1, _ship_name, format(_battles, ','), round(_wr*100, 2), format(round(_avgdmg), ','))
    return ship_detail_display


def onQQMessage(bot, contact, member, content):
    # bot control flag
    global wowsinfo_flag

    # -start / -stop
    # only response to -start / -stop from buddy
    # or even from specific buddy
    # if contact.ctype == 'buddy' and contact.name == '牛奶源':
    if contact.ctype == 'buddy':
        if content == '-start wowsinfo':
            wowsinfo_flag = True
            bot.SendTo(contact, 'wowsinfo start')
            return
        if content == '-stop wowsinfo':
            wowsinfo_flag = False
            bot.SendTo(contact, 'wowsinfo stop')
            return

    # check flag
    if wowsinfo_flag == False:
        return

    # init response wrapper
    rw = ResponseWrapper()

    # set reply prompt
    if contact.ctype == 'group':
        rw.reply_prompt = '@{0}\n'.format(member.name)

    # -time
    if re.match('-time', content):
        rw.type = '-time'
        rw.time = time.strftime(
            '%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        send_via_rw(bot, contact, rw)
        return

    # -echo
    if re.match('-echo', content):
        re_result = re.search(r'-echo(?:\s+)(.+)', content)
        if re_result:
            rw.type = '-echo'
            rw.echo = re_result.group(1)
            send_via_rw(bot, contact, rw)
            return
        else:
            rw.type = 'error'
            rw.error_prompt = 'usage: -echo <content>'
            send_via_rw(bot, contact, rw)
            return

    # -deto
    if re.match('-deto', content):

        # mapping user_name
        content = meme.user_name_mapping(content)

        # pick param from instruction
        re_result = re.search(r'-deto(?:\s+(\w+))', content)
        if re_result:

            # get user_name
            user_name = re_result.group(1)

            # check existence of user_name
            player_info = detoapi.query_player(user_name)
            if len(player_info) == 0:
                rw.type = 'error'
                rw.error_prompt = 'user {0} not found'.format(user_name)
                send_via_rw(bot, contact, rw)
                return

            # get player info
            id = player_info[0]['id']
            account_id = player_info[0]['account_id']
            nickname = player_info[0]['user_name']
            is_hidden = player_info[0]['is_hidden']
            rw.nickname = nickname

            # name alter prompt
            if nickname != user_name:
                rw.name_alter_prompt = 'user {0} not found, maybe you mean {1}?\n'.format(
                    user_name, nickname)

            if is_hidden == True:
                rw.type = 'error'
                rw.error_prompt = 'user {0} sets profile hidden'.format(
                    nickname)
                send_via_rw(bot, contact, rw)
                return

            # get clan tag with brackets
            rw.clan_tag_with_brackets = gain_clan_tag_with_brackets(
                account_id)

            # get deto statistics
            try:
                deto_total = int(detoapi.query_data(
                    'deto_total', id, latest_date))
                deto_total_rank = int(detoapi.query_data(
                    'deto_total_rank', id, latest_date))
                deto_total_ratio = float(detoapi.query_data(
                    'deto_total_ratio', id, latest_date))
                deto_total_ratio_rank = int(detoapi.query_data(
                    'deto_total_ratio_rank', id, latest_date))
                deto_period = int(detoapi.query_data(
                    'deto_period', id, latest_date))
                deto_period_rank = int(detoapi.query_data(
                    'deto_period_rank', id, latest_date))
                deto_period_ratio = float(detoapi.query_data(
                    'deto_period_ratio', id, latest_date))
                deto_period_ratio_rank = int(detoapi.query_data(
                    'deto_period_ratio_rank', id, latest_date))
            except:
                # query_data may return None due to net problem
                rw.type = 'error'
                rw.error_prompt = '❌Fail to fetch deto statistics.'
                send_via_rw(bot, contact, rw)

            # add meme
            rw.meme = meme.meme_mapping(nickname)

            rw.type = '-deto'
            rw.deto = '⬇️deto overall\n{0}(#{1}) {2}%(#{3})\n⬇️deto last week\n{4}(#{5}) {6}%(#{7})'.format(
                format(deto_total, ','), format(deto_total_rank, ','),
                round(deto_total_ratio * 100,
                      2), format(deto_total_ratio_rank, ','),
                format(deto_period, ','), format(deto_period_rank, ','),
                round(deto_period_ratio * 100, 2), format(deto_period_ratio_rank, ','))
            send_via_rw(bot, contact, rw)
            return

        rw.type = 'error'
        rw.error_prompt = 'usage: -deto <user_name>'
        send_via_rw(bot, contact, rw)
        return

    # -info
    if re.match('-info', content):

        # mapping user_name
        content = meme.user_name_mapping(content)

        # pick param from instruction
        re_result = re.search(r'-info(?:\s+-(\w+))?\s+(\w+)', content)
        if re_result:

            # check validity of ship_category
            ship_category = re_result.group(1)
            if ship_category:

                # invalid ship_category detected
                if ship_category.lower() not in ('cv', 'bb', 'ca', 'dd', 'all'):
                    rw.type = 'error'
                    rw.error_prompt = 'invalid category {0}'.format(
                        ship_category)
                    send_via_rw(bot, contact, rw)
                    return

            # check existence of user_name
            user_name = re_result.group(2)
            players = wgapi.get_players(user_name)
            if players:

                # non existence user_name
                if players['meta']['count'] == 0:
                    rw.type = 'error'
                    rw.error_prompt = 'user {0} not found'.format(user_name)
                    send_via_rw(bot, contact, rw)
                    return

                # get nickname and acount_id
                nickname = players['data'][0]['nickname']
                account_id = players['data'][0]['account_id']
                rw.nickname = nickname

                # name alter prompt
                if nickname != user_name:
                    rw.name_alter_prompt = 'user {0} not found, maybe you mean {1}?\n'.format(
                        user_name, nickname)

                # get player personal data
                player_personal_data = wgapi.get_player_personal_data(
                    account_id)
                if player_personal_data['meta']['count'] == 0:
                    rw.type = 'error'
                    rw.error_prompt = 'user {0} not found'.format(nickname)
                    send_via_rw(bot, contact, rw)
                    return
                if player_personal_data['meta']['hidden'] != None:
                    rw.type = 'error'
                    rw.error_prompt = rw.name_alter_prompt + \
                        'user {0} sets profile hidden'.format(nickname)
                    send_via_rw(bot, contact, rw)
                    return

                # get clan tag with brackets
                rw.clan_tag_with_brackets = gain_clan_tag_with_brackets(
                    account_id)

                # get pvp statistics
                stat_pvp = player_personal_data['data'][str(
                    account_id)]['statistics']['pvp']

                battles = stat_pvp['battles']
                wins = stat_pvp['wins']
                wr = 0
                if battles != 0:
                    wr = wins / battles

                main_battery_shots = stat_pvp['main_battery']['shots']
                main_battery_hits = stat_pvp['main_battery']['hits']
                mbhr = 0
                if main_battery_shots != 0:
                    mbhr = main_battery_hits / main_battery_shots

                damage_dealt = stat_pvp['damage_dealt']
                maxdmg = stat_pvp['max_damage_dealt']
                avgdmg = 0
                if battles != 0:
                    avgdmg = damage_dealt / battles

                # add category display
                if ship_category:
                    rw.category_display += '\n⬇️3 most played '
                    if ship_category.lower() == 'all':
                        rw.category_display += 'ship'
                    else:
                        rw.category_display += ship_category.upper()
                    rw.category_display += ' stat'
                    rw.category_display += gain_ship_detail_display(
                        account_id, ship_category)

                # add meme
                rw.meme = meme.meme_mapping(nickname)

                rw.type = '-info'
                rw.info = '⬇️pvp stat overview\nbattles {0} wr {1}% mbhr {2}%'.format(format(battles, ','), round(
                    wr * 100, 2), round(mbhr * 100, 2)) + '\n' + 'avgdmg {0} maxdmg {1}'.format(format(round(avgdmg), ','), format(maxdmg, ','))
                if nickname == 'momotxdi':
                    if random.randint(0, 1) != 0:
                        rw.info = '⬇️pvp stat overview\nbattles {0} wr {1}% mbhr {2}%'.format(format(battles, ','), round(
                            wr * 100, 2), round(mbhr * 100, 2)) + '\n' + 'avgdmg [too high cannot display] maxdmg {0}'.format(format(maxdmg, ','))
                send_via_rw(bot, contact, rw)
                return

        rw.type = 'error'
        rw.error_prompt = 'usage: -info [-(cv)|(bb)|(ca)|(dd)|(all)] <user_name>'
        send_via_rw(bot, contact, rw)
        return
