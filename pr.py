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
    if(now_time - expected_values_update_time > 14400):
        expected_values = get_expected_values()
        expected_values_update_time = int(time.time())

    try:
        expectedDmg = expected_values['data'][str(
            ship_id)]['average_damage_dealt']
        expectedWins = expected_values['data'][str(
            ship_id)]['win_rate']
        expectedFrags = expected_values['data'][str(
            ship_id)]['average_frags']
    except:
        return 0

    rDmg = actualDmg / expectedDmg
    rWins = actualWins / expectedWins
    rFrags = actualFrags / expectedFrags

    nDmg = max(0, (rDmg - 0.4) / (1 - 0.4))
    nFrags = max(0, (rFrags - 0.1) / (1 - 0.1))
    nWins = max(0, (rWins - 0.7) / (1 - 0.7))

    PR = 700 * nDmg + 300 * nFrags + 150 * nWins
    return PR


def calc_total_pr(account_id, player_ship_stats):
    actualDmg = 0
    expectedDmg = 0
    actualWins = 0
    expectedWins = 0
    actualFrags = 0
    expectedFrags = 0

    for s in player_ship_stats['data'][str(account_id)]:
        try:
            ship_id = s['ship_id']
            battles = s['pvp']['battles']

            if battles == 0:
                continue

            try:
                expectedDmg += expected_values['data'][str(
                    ship_id)]['average_damage_dealt'] * battles
                expectedWins += expected_values['data'][str(
                    ship_id)]['win_rate'] * battles
                expectedFrags += expected_values['data'][str(
                    ship_id)]['average_frags'] * battles
            except:
                print("[ERROR]Fail to get excepted_values with ship id {0}!".format(ship_id))
                continue

            actualDmg += s['pvp']['damage_dealt']
            actualWins += s['pvp']['wins'] * 100
            actualFrags += s['pvp']['frags']

        except:
            pass

    rDmg = actualDmg / expectedDmg
    rWins = actualWins / expectedWins
    rFrags = actualFrags / expectedFrags

    nDmg = max(0, (rDmg - 0.4) / (1 - 0.4))
    nFrags = max(0, (rFrags - 0.1) / (1 - 0.1))
    nWins = max(0, (rWins - 0.7) / (1 - 0.7))

    PR = 700 * nDmg + 300 * nFrags + 150 * nWins
    return PR


expected_values = get_expected_values()
expected_values_update_time = int(time.time())
