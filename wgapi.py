import urllib
import json
import config

wg_app_id = config.wg_app_id


def get_from_wg_api(name, url, realm):
    # change realm
    if realm == 'aisa':
        pass
    elif realm == 'eu':
        pass
    elif realm == 'ru':
        pass
    elif realm == 'na':
        realm = 'com'
    else:
        # default get asia data
        realm = 'asia'

    r = urllib.request.urlopen(
        url='https://api.worldofwarships.{0}/{1}'.format(realm, url))
    if r.status == 200:
        text = r.read()
        result = json.loads(text)
        if result['status'] == 'ok':
            return result
        else:
            print('[Warning] api return in {0} status != ok'.format(name))
            print(result)
            return None
    else:
        print('[Warning] requests in {0} status code != 200'.format(name))
        return None


def get_players(search, realm):
    name = 'wows/account/list/'
    url = 'wows/account/list/?application_id={0}&search={1}'.format(
        wg_app_id, search)
    return get_from_wg_api(name, url, realm)


def get_player_personal_data(account_id, realm):
    name = 'wows/account/info/'
    url = 'wows/account/info/?application_id={0}&account_id={1}'.format(
        wg_app_id, account_id)
    return get_from_wg_api(name, url, realm)


def get_player_clan_data(account_id, realm):
    name = 'wows/clans/accountinfo/'
    url = 'wows/clans/accountinfo/?application_id={0}&account_id={1}'.format(
        wg_app_id, account_id)
    return get_from_wg_api(name, url, realm)


def get_clan_details(clan_id, realm):
    name = 'wows/clans/info/'
    url = 'wows/clans/info/?application_id={0}&clan_id={1}'.format(
        wg_app_id, clan_id)
    return get_from_wg_api(name, url, realm)


def get_player_ship_stats(account_id, realm):
    name = 'wows/ships/stats/'
    url = 'wows/ships/stats/?application_id={0}&account_id={1}'.format(
        wg_app_id, account_id)
    return get_from_wg_api(name, url, realm)
