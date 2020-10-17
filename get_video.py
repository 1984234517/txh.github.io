import requests
from bs4 import BeautifulSoup
import lxml
import re

# # 根据用户输入的关键字得到目标视频的url地址,然后对得到的目标视频的url加上一个前缀url即为该视频解析后的url
# def get_aim_video_url(key_data,set_key=0):
#     url = 'https://v.qq.com/x/search/?q='+ key_data +'&stag=0&smartbox_ab='
#     header = {
#         'user-agent':'Mozilla/5.0(Windows NT 10.0; WOW64) AppleWebKit/537.36(KHTML,like Gecko) Chrome/74.0.3729.131 Safari/537.36'
#     }
#     respon = requests.get(url,headers=header)
#     print(respon)
#     soup = BeautifulSoup(respon.text,'lxml')
#     aim_a_list = soup.find_all('a', attrs={'_stat': 'video:poster_num'})
#     length = len((aim_a_list))
#     print(length)
#     set_url_item = {}
#     if length :
#         for i in range(length):
#             key = aim_a_list[i].text
#             set_url_item[key] = 'http://jx.598110.com/v/6.php?url='+aim_a_list[i].get('href')
#     print(set_url_item)
#     if set_key :
#         return {set_key: set_url_item.get(str(set_key))}
#     else:
#         return set_url_item

# 根据用户输入的关键字得到目标视频的url地址,然后对得到的目标视频的url加上一个前缀url即为该视频解析后的url
def get_aim_video_url(key_data, set_key=0):
    url = 'https://v.qq.com/x/search/?q=' + key_data + '&stag=0&smartbox_ab='
    header = {
        'user-agent': 'Mozilla/5.0(Windows NT 10.0; WOW64) AppleWebKit/537.36(KHTML,like Gecko) Chrome/74.0.3729.131 Safari/537.36'
    }
    respon = requests.get(url, headers=header)
    print(respon)
    url_re = re.compile(r'<a href="(.*?)".*?_stat="video:poster_tle">')
    url_data = url_re.findall(respon.text,re.S)
    print('第二个网页的url为',url_data[0])
    respon = requests.get(url_data[0],headers=header)
    kk_data = respon.text
    # print(kk_data)
    soup2 = BeautifulSoup(kk_data, 'lxml')
    url_data2 = soup2.find_all('a', attrs={'class': 'btn_primary btn_primary_md '})
    # 这里对url_data2进行判断是因为我们要区分vip电影和vip电视剧，vip电影只需要进行两次的url解析，但是vip电视剧需要三次的url解析
    # 所以在进行第二次url解析的时候，如果没有解析到任何数据的话，就说明搜索的是vip电影而不是vip电视剧
    if url_data2 :
        print('url_data的值为',url_data2)
        data_url = url_data2[0].get('href')
        print("得到的数据为",data_url)
        respon = requests.get(data_url, headers=header)
        respon.encoding = ('utf8')
        data_value = respon.text
    else:
        data_value = kk_data
    # 获取每集电视url中的cover参数
    analysis_url_cover_re = re.compile(r'cover_id":"(.*?)",')
    # 获取每集电视url中的nomal参数
    analysis_url_nomal_re = re.compile(r'nomal_ids":(.*?),"score"')
    analysis_url_nomal_re2 = re.compile(r'"V":"(.*?)","E":(.*?)}')
    # 获取总的集数包含预告片
    analysis_url_number_re = re.compile(r'"episode_updated":(.*?),"dire')
    analysis_url_number_re2 = re.compile(r'\d+')
    # 电视剧更新的集数
    analysis_url_updata_length = re.compile(r'\\"text\\":\\"更新至(\d+)集\\"},\\"tag_4',re.S)
    updata_length = analysis_url_updata_length.findall(data_value)
    print("更新的集数为",updata_length)
    analysis_url_cover = analysis_url_cover_re.search(data_value)
    try:
        analysis_url_cover = analysis_url_cover.group(1)
    except Exception as f:
        print("没有查到相关的信息，请重新输入想要查找的内容")
        return None
    analysis_url_nomal = analysis_url_nomal_re.findall(data_value,re.S)
    if len(analysis_url_nomal) == 0:
        return None
    analysis_url_nomal = analysis_url_nomal[0]
    #print('我的参数值为',analysis_url_nomal)
    analysis_url_nomal = analysis_url_nomal_re2.findall(analysis_url_nomal)
    #print('我的参数值为', len(analysis_url_nomal))
    try:
        analysis_url_number = analysis_url_number_re.findall(data_value,re.S)[0]
    except IndexError as f:
        print('出问题了',f)
        return ''
    #print('我的值为',analysis_url_number)
    analysis_url_number = analysis_url_number_re2.findall(analysis_url_number)

    print(analysis_url_cover,analysis_url_nomal,analysis_url_number)
    # 用来保存腾讯视频中视频的url
    tenxun_url_item = {}
    tenxun_url_list = []
    tenxun_url_list2 = []

    if analysis_url_number :
        analysis_url_number = int(analysis_url_number[0])
        for i in range(len(analysis_url_nomal)+1):
            tenxun_url_list.append(0)
        # 把更新的集数放到列表的第一项
        if updata_length:
            tenxun_url_list[0] = updata_length[0]
        else:
            tenxun_url_list[0] = '0'
        print("初始化的列表长度为",len(tenxun_url_list))
        for i in range(len(analysis_url_nomal)):
            # 拼接腾讯视频中视频的url
            '''https://jx.idc126.net/jx/?'''
            tenxun_url = 'https://jx.idc126.net/jx/?url=http://v.qq.com/x/cover/'+analysis_url_cover+'/'+analysis_url_nomal[i][0]+'.html'
            #print('合成的地址为',tenxun_url)
            print(i)
            tenxun_url_list[int(analysis_url_nomal[i][1])] = tenxun_url
        for i in range(len(tenxun_url_list)):
            if tenxun_url_list[i] != 0:
                tenxun_url_list2.append(tenxun_url_list[i])
        tenxun_url_list = tenxun_url_list2
        print('最后的集数是',len(tenxun_url_list))
        return tenxun_url_list
    else:

        tenxun_url = 'http://jx.598110.com/v/6.php?url=http://v.qq.com/x/cover/' + analysis_url_cover + '/' + \
                     analysis_url_nomal[0][0] + '.html'
        return ['1',tenxun_url]

#'http://jx.598110.com/v/6.php?url=https://v.qq.com/x/cover/vbb35hm6m6da1wc/r00318trm1s.html'
def get_aim_video(key_word):
    aim_url = get_aim_video_url(key_word)
    if aim_url:
        return aim_url
    else:
        print("没有查到相关的信息，请重新输入你的选择")
        return {}
if __name__ == '__main__':
    key_word = '陈情令'
    data = get_aim_video(key_word)
    print(data)