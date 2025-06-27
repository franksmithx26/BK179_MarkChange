import requests
import json
import base64
import re
class BK179CRACK:
    def __init__(self,cookie = ''):
        cookie_dict = self.__cookie_process(cookie)
        self.session = requests.Session()
        self.session.cookies.update(cookie_dict)
        print(cookie_dict)

    def __cookie_process(self, cookie):
        cookie_dict = {}
        if cookie:
            for item in cookie.split(';'):
                key, value = item.strip().split('=', 1)
                cookie_dict[key] = value
        return cookie_dict

    '''
    从服务端获取用户ID
    '''
    def get_uid(self):
        resp = self._get('https://www.bk179.com/volunteer/intelligence',params=[])
        rule = r'fenshu_info\\":{\\"id\\":(.*?),\\"userid\\"'
        uid = re.findall(rule,resp.content.decode('UTF-8'))[0]
        print('获取到的用户ID:', uid)
        return int(uid)

    def _post(self, url, data,Next_Action, Next_Router_State_Tree):
        headers = {
                'Host': 'www.bk179.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0',
                'Accept': 'text/x-component',
                'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Referer': 'https://www.bk179.com/',
                'Content-Type': 'text/plain;charset=UTF-8',
                'Origin': 'https://www.bk179.com',
                'DNT': '1',
                'Sec-GPC': '1',
                'Connection': 'keep-alive',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'Priority': 'u=0',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
        }
        headers['Next-Router-State-Tree'] = Next_Router_State_Tree
        headers['Next-Action'] = Next_Action
        response = self.session.post(url, data=data, headers=headers)
        return response

    def _get(self, url, params, Authorization=''):
        headers = {
            'Host': 'www.bk179.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0',
            'Accept': '*/*',
            'Referer': 'https://www.bk179.com/bigdata/listyear/weici',
            'Authorization': Authorization, 
            'DNT': '1',
            'Sec-GPC': '1',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Priority': 'u=0',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }
        response = self.session.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response

    '''
    登陆
    '''
    def login(self, username, password):
        url = 'https://www.bk179.com/login?redirect=/volunteer/intelligence' #其实好像全都可以
        payload_list = [{
            'username': username,
            'password': password,
            'remember': False
        }]
        response = self._post(url, data=json.dumps(payload_list),Next_Action='34717b724e7aafd045a17f29dbb050d17bf1c5e5',Next_Router_State_Tree='%5B%22%22%2C%7B%22children%22%3A%5B%22__PAGE__%22%2C%7B%7D%2C%22%2F%22%2C%22refresh%22%5D%7D%2Cnull%2Cnull%2Ctrue%5D')
        login_res = {}
        if not 'loginres' in response.content.decode('UTF-8').lower():
            print('登录失败，服务器未返回登陆结果')
            return False
        else:
            lines = response.content.decode('UTF-8').strip().split('\n')
            for line in lines:
                if line.startswith('1:'):
                    # 提取JSON字符串
                    result_json_str = line[2:]
                    result_data = json.loads(result_json_str)
                    login_res = result_data.get('loginRes', {})
                    break
            code = login_res.get('code')
            info = login_res.get('info')
            print('登录结果:', code, info)
            if code == 1:
                return True
            else:
                return False
    '''
    获取当前分数段
    '''
    def get_zone(self,mark):
        url = "https://www.bk179.com/api/bigdata/school/listyearFenduan"
        params = {
        'year': '2025',
        'kelei': 'li',
        'page': '1',
        'pagesize': '30',
        'gaokaofen': str(mark)
        }
        response = self._get(url,params=params,Authorization='0bce0e456e6f12e5e52dbfb8cd6e45a4')
        zone = response.json().get('data', {}).get('list', [])[0].get('paim',0)
        print('当前分数段:', zone)
        return zone

    '''
    更改当前分数
    '''
    def change_mark(self, mark, jiafen=0):
        zone = self.get_zone(mark)# 获取当前分数段
        url = 'https://www.bk179.com/volunteer/intelligence'
        id = self.get_uid()# 获取用户ID
        isadd = 0 #是否有加分
        if(jiafen > 0):isadd = 1
        payload_list = [{
            'addfen': jiafen,
            'gaokaofen': mark,
            'id': id,
            'isadd':isadd,
            'rank':zone
        }]
        response = self._post(url, data=json.dumps(payload_list),Next_Action='f260fdb71d52a679f2028d1988c20251b14000dc',Next_Router_State_Tree='%5B%22%22%2C%7B%22children%22%3A%5B%22volunteer%22%2C%7B%22children%22%3A%5B%22intelligence%22%2C%7B%22children%22%3A%5B%22__PAGE__%22%2C%7B%7D%2C%22%2Fvolunteer%2Fintelligence%22%2C%22refresh%22%5D%7D%5D%7D%5D%7D%2Cnull%2Cnull%2Ctrue%5D')
        if '分数设置成功' in response.content.decode('UTF-8'):
            print('分数设置成功',mark,zone)
            return True
        else:
            print('分数设置失败')
            return False
    
if __name__ == '__main__':
    username = ''
    password = ''
    cookie = 'appType=normal; appProvinceId=450000000000; acw_tc=0a03de3f17510475502397178e60f90e9c9ebb61b7e6f953b9576f56ed54f8'
    bk179 = BK179CRACK(cookie)
    bk179.login(username, password)
    bk179.change_mark(600) 