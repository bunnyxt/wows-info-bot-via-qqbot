import urllib
import json
import time

expected_values = None
expected_values_update_time = None


def get_expected_values():
    global expected_values
    url = 'https://asia.wows-numbers.com/personal/rating/expected/json/'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
    req = urllib.request.Request(url, headers=headers)
    r = urllib.request.urlopen(req)
    if r.status == 200:
        text = r.read()
        result = json.loads(text)
        if result:
            return result
        else:
            return None
    else:
        print('[Warning] requests in get_expected_values status code != 200')
        return None


def calc_ship_pr(ship_id, actualDmg, actualWins, actualFrags):
    global expected_values
    global expected_values_update_time

    now_time = int(time.time())
    if(now_time - expected_values_update_time > 600):
        expected_values = get_expected_values()
        expected_values_update_time = int(time.time())

    try:
        expectedDmg = expected_values['data'][str(
            ship_id)]['average_damage_dealt']
        expectedWins = expected_values['data'][str(ship_id)]['win_rate']
        expectedFrags = expected_values['data'][str(ship_id)]['average_frags']
    except:
        return 0

    rDmg = actualDmg / expectedDmg
    rWins = actualWins / expectedWins
    rFrags = actualFrags / expectedFrags

    nDmg = max(0, (rDmg - 0.4) / (1 - 0.4))
    nFrags = max(0, (rFrags - 0.1) / (1 - 0.1))
    nWins = max(0, (rWins - 0.7) / (1 - 0.7))

    PR = 700 * nDmg + 300 * nFrags + 150 * nWins
    print(PR)
    return PR


def calc_total_pr(account_id, player_ship_stats):
    pr_sum = 0
    battle_count = 0
    for s in player_ship_stats['data'][str(account_id)]:
        try:
            ship_id = s['ship_id']
            battles = s['pvp']['battles']
            damage_dealt = s['pvp']['damage_dealt']
            wins = s['pvp']['wins']
            frags = s['pvp']['frags']
            avgdmg = 0
            wr = 0
            avgfrag = 0
            if battles != 0:
                avgdmg = damage_dealt / battles
                wr = wins / battles
                avgfrag = frags / battles
            ship_pr = calc_ship_pr(ship_id, avgdmg, wr * 100, avgfrag)
            pr_sum += ship_pr * battles
            battle_count += battles
        except:
            pass
    total_pr = 0
    if battle_count != 0:
        total_pr = pr_sum / battle_count
    return total_pr


expected_values = get_expected_values()
expected_values_update_time = int(time.time())
