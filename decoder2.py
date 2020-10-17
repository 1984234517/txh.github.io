import os,shutil,json,requests
from  binascii import hexlify, b2a_hex
from Crypto.Cipher import AES
import base64

class Encrypyed():
    def __init__(self):
        self.pub_key = '010001'
        self.modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        self.nonce = '0CoJUm6Qyw8W8jud'


    def create_secret_key(self,size):
        ''' 生成十六位的随机字符串'''
        return hexlify(os.urandom(size))[:16].decode('utf-8')

    def aes_encrypt(self,text, key):
        ''' AES加密'''
        iv = '0102030405060708'
        pad = 16 - len(text) % 16
        text = str(text) + pad * chr(pad)
        encryptor = AES.new(key.encode(), AES.MODE_CBC, iv.encode())
        result = encryptor.encrypt(text.encode("UTF8"))
        # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        rdd = base64.b64encode(result).decode("UTF8")
        return rdd

    def rsa_encrpt(self,text, pubKey, modulus):
        text = text[::-1]
        rs = pow(int(hexlify(text.encode('utf-8')), 16), int(pubKey, 16), int(modulus, 16))
        return format(rs, 'x').zfill(256)

    def work(self,text):
        text = json.dumps(text)
        i=self.create_secret_key(16)
        encText =self.aes_encrypt(text, self.nonce)
        encText=self.aes_encrypt(encText,i)
        encSecKey=self.rsa_encrpt(i,self.pub_key,self.modulus)
        print(str(encText))
        data = {'params': str(encText), 'encSecKey': encSecKey}
        return data

def main(key_value):
    # 查询符合条件歌曲的id
    url = 'https://music.163.com/weapi/cloudsearch/get/web?csrf_token='
    # # 歌曲的具体url
    # url = 'http://music.163.com/weapi/song/enhance/player/url?csrf_token='
    do = Encrypyed()
    post_data = {"hlpretag": '<span class="s-fc7">', "hlposttag": "</span>", "s": key_value, "type": "1", "offset": "0",
                 "total": "true", "limit": "100", "csrf_token": ""}
    data = do.work(post_data)
    # post_data1 = {"ids":"[191254]","br":192000,"csrf_token":""}
    # data = do.work(post_data1)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Referer': 'https://music.163.com/search/',
    }
    session = requests.Session()
    session.headers = headers
    # print(data)
    result = session.post(url, data=data,verify=False).json()
    # print(result)
    song_id_list = []
    if result !='':
        result_list = result['result']['songs']
        # print(result_list)
        for i in result_list:
            # print(i)
            key={}
            key['song_name'] = i['name']
            key['song_id'] = i['id']
            key['songer'] = i['ar'][0]['name']
            song_id_list.append(key)
    return song_id_list
if __name__ == '__main__':
    key_value = '周杰伦'
    kk = main(key_value)
    print(kk)