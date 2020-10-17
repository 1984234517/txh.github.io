import requests,urllib
import json

def get_url (url,data):
    data = urllib.parse.urlencode(data)
    url = url + '?' + data
    return url

def get_mid(url,key,number):
    mid_item = []
    song_name = []
    songer_item = []
    data = {
        'ct': '24',
        'new_json': '1',
        'remoteplace': 'txt.yqq.song',
        'searchid': '63682231781232894',
        't': '0',
        'aggr': '1',
        'cr': '1',
        'catZhida': '1',
        'lossless': '0',
        'flag_qc': '0',
        'p': '1',
        'n': number,
        'w': key,
        'format': 'json',
    }
    respond = requests.get(url,data)
    # print('源json文件为',respond.text)
    information = json.loads(respond.text)
    song = information.get('data').get('song').get('list')
    length = len(song)
    # print('长度为',length)
    for i in range(length):
        mid_item.append(song[i].get('mid'))
        song_name.append(song[i].get('title'))
        print(song[i].get('title'))
        songer_item.append(song[i].get('singer')[0].get('name'))
    return mid_item,song_name,songer_item

# 获取歌曲的下载地址
def get_song_url(url,mid):
    data1 = {
        '-': 'getplaysongvkey27834733422062374',
        'g_tk': '177848969',
        'hostUin': '0',
        'format': 'json',
        'inCharset': 'utf8',
        'outCharset': 'utf-8',
        'platform': 'yqq.json',
        'needNewCode': '0',
    }
    url_one = get_url(url, data1)
    # print("mid的长度为",len(mid))
    song_url = []
    for i in mid:
        data = {"req":{"module":"CDN.SrfCdnDispatchServer","method":"GetCdnDispatch","param":{"guid":"8147203620","calltype":0,"userip":""}},"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"8147203620","songmid":[i],"songtype":[0],"uin":"1984234517","loginflag":1,"platform":"20"}},"comm":{"uin":1984234517,"format":"json","ct":24,"cv":0} }
        print('数据为',data)
        url = url_one+'&data='+json.dumps(data)
        respond = requests.get(url=url)
        information = json.loads(respond.text)
        qian_url = information.get('req_0').get('data').get('sip')[0]
        information = information.get('req_0').get('data').get('midurlinfo')
        if information:
            information = information[0]
            hou_url = information.get('purl')
            url = qian_url+hou_url
            song_url.append(url)
            print("歌曲url为",url)
    return song_url
# 主函数
def get_song(song_key):
    url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?'
    number = 25
    song_infon = []
    mid_item,song_name,songer_item = get_mid(url,song_key,number)
    vkey_url = 'https://u.y.qq.com/cgi-bin/musicu.fcg'
    song_item = get_song_url(vkey_url, mid_item)
    for i in range(len(song_name)):
        result = {}
        print('歌曲信息为',song_item[i],song_name[i])
        result['song_url'] = song_item[i]
        result['song_name'] = song_name[i]
        result['songer'] = songer_item[i]
        song_infon.append(result)
    print(song_infon)
    return song_infon

if __name__ == '__main__':
    # key = '张杰'
    # url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?'
    # number = '100'
    # mid_item ,song_name= get_mid(url,key,number)
    # vkey_url = 'https://u.y.qq.com/cgi-bin/musicu.fcg'
    # get_song_url(vkey_url,mid_item)
    get_song('张杰')