import urllib
import json

def get_latest_date():
    r = urllib.request.urlopen(
        url='http://api.bunnyxt.com/deto/get_latest_date_string.php')
    if r.status == 200:
        text = r.read()
        return text
    else:
        print('[Warning] requests in {0} status code != 200'.format(
            "get_latest_date"))
        return None


def query_player(user_name):
    r = urllib.request.urlopen(
        url='http://api.bunnyxt.com/deto/query_player.php?user_name={0}'.format(user_name))
    if r.status == 200:
        text = r.read()
        result = json.loads(text)
        return result
    else:
        print('[Warning] requests in {0} status code != 200'.format(
            "query_player"))
        return None


def query_data(category, id, date):
    r = urllib.request.urlopen(
        url='http://api.bunnyxt.com/deto/query_data.php?category={0}&date={1}&id={2}'.format(category, date, id))
    if r.status == 200:
        text = r.read()
        return text
    else:
        print('[Warning] requests in {0} status code != 200'.format(
            "query_player"))
        return None
