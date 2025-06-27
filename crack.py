import requests
import json
import re
from typing import Tuple, Dict, Any, Optional

class BK179CRACK:
    """
    一个用于模拟“报考一起走”(www.bk179.com)网站用户操作的类。
    提供了登录、查询分数位次、修改分数等功能。
    """
    
    # --- 类常量定义 ---
    BASE_URL = "https://www.bk179.com"
    
    # Next.js Server Action IDs
    ACTION_ID_LOGIN = '34717b724e7aafd045a17f29dbb050d17bf1c5e5'
    ACTION_ID_CHANGE_MARK = 'f260fdb71d52a679f2028d1988c20251b14000dc'

    # Next.js Router State Trees (URL Encoded)
    STATE_TREE_LOGIN = '%5B%22%22%2C%7B%22children%22%3A%5B%22__PAGE__%22%2C%7B%7D%2C%22%2F%22%2C%22refresh%22%5D%7D%2Cnull%2Cnull%2Ctrue%5D'
    STATE_TREE_CHANGE_MARK = '%5B%22%22%2C%7B%22children%22%3A%5B%22volunteer%22%2C%7B%22children%22%3A%5B%22intelligence%22%2C%7B%22children%22%3A%5B%22__PAGE__%22%2C%7B%7D%2C%22%2Fvolunteer%2Fintelligence%22%2C%22refresh%22%5D%7D%5D%7D%5D%7D%2Cnull%2Cnull%2Ctrue%5D'
    
    # API Authorization (固定值)
    # 注意：这个值在实际应用中很可能会失效，因为它通常是动态生成的。
    AUTH_TOKEN_GET_ZONE = '0bce0e456e6f12e5e52dbfb8cd6e45a4'

    def __init__(self, cookie: str = ''):
        """
        初始化BK179CRACK实例。
        
        Args:
            cookie (str, optional): 包含初始cookie的字符串，例如从浏览器复制。默认为空。
        """
        self.session = requests.Session()
        if cookie:
            cookie_dict = self._parse_cookie_string(cookie)
            self.session.cookies.update(cookie_dict)
        # print(f"初始化Session，Cookies: {self.session.cookies.get_dict()}")

    def _parse_cookie_string(self, cookie: str) -> Dict[str, str]:
        """将分号分隔的cookie字符串解析为字典。"""
        cookie_dict = {}
        for item in cookie.split(';'):
            if '=' in item:
                key, value = item.strip().split('=', 1)
                cookie_dict[key] = value
        return cookie_dict

    # --- 底层HTTP请求方法 ---

    def _build_post_headers(self, next_action: str, next_router_state_tree: str, referer: str) -> Dict[str, str]:
        """构建用于Server Action的POST请求头。"""
        return {
            'Host': 'www.bk179.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0',
            'Accept': 'text/x-component',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Referer': referer,
            'Content-Type': 'text/plain;charset=UTF-8',
            'Origin': self.BASE_URL,
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Next-Action': next_action,
            'Next-Router-State-Tree': next_router_state_tree,
        }

    def _build_get_headers(self, authorization: str, referer: str) -> Dict[str, str]:
        """构建用于API查询的GET请求头。"""
        return {
            'Host': 'www.bk179.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0',
            'Accept': '*/*',
            'Referer': referer,
            'Authorization': authorization,
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        }

    def _post(self, url: str, data: str, headers: Dict[str, str]) -> requests.Response:
        """执行POST请求并处理常见异常。"""
        try:
            response = self.session.post(url, data=data, headers=headers)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"POST请求到 {url} 失败: {e}")
            raise  # 重新抛出异常，让调用者处理

    def _get(self, url: str, params: Dict[str, Any], headers: Dict[str, str]) -> requests.Response:
        """执行GET请求并处理常见异常。"""
        try:
            response = self.session.get(url, params=params, headers=headers)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"GET请求到 {url} 失败: {e}")
            raise

    # --- 核心业务逻辑方法 ---

    def login(self, username: str, password: str) -> Tuple[bool, str]:
        """
        模拟用户登录。

        Args:
            username (str): 用户名。
            password (str): 密码。

        Returns:
            Tuple[bool, str]: (是否成功, 消息文本)。
        """
        url = f"{self.BASE_URL}/login?redirect=/volunteer/intelligence"
        payload_list = [{"username": username, "password": password, "remember": False}]
        headers = self._build_post_headers(self.ACTION_ID_LOGIN, self.STATE_TREE_LOGIN, self.BASE_URL + "/")
        
        try:
            response = self._post(url, data=json.dumps(payload_list), headers=headers)
            content = response.content.decode('utf-8', errors='ignore')

            if 'loginRes' not in content:
                return False, "登录失败，服务器响应中未包含'loginRes'。"

            lines = content.strip().split('\n')
            for line in lines:
                if line.startswith('1:'):
                    result_data = json.loads(line[2:])
                    login_res = result_data.get('loginRes', {})
                    code = login_res.get('code')
                    info = login_res.get('info', '未知信息')
                    success = code == 1
                    return success, info
            
            return False, "解析登录响应失败，未找到结果行。"

        except Exception as e:
            return False, f"登录过程中发生异常: {str(e)}"

    def get_score_record_id(self) -> Optional[int]:
        """
        从“智能填报”页面获取当前分数记录的数据库ID。
        这是执行`change_mark`前必须调用的步骤。

        Returns:
            Optional[int]: 如果找到则返回ID，否则返回None。
        """
        url = f"{self.BASE_URL}/volunteer/intelligence"
        headers = self._build_get_headers(authorization="", referer=url) # GET请求通常不需要签名
        
        try:
            resp = self._get(url, params={}, headers=headers)
            content = resp.content.decode('utf-8', errors='ignore')
            
            # 正则表达式匹配 'fenshu_info':{"id":xxxx,"userid"...} 这样的结构
            rule = r'fenshu_info\\":{\\"id\\":(\d+),\\"userid\\"'
            match = re.search(rule, content)
            
            if match:
                record_id = int(match.group(1))
                # print(f'获取到的分数记录ID: {record_id}')
                return record_id
            else:
                print('警告: 未能在页面中找到分数记录ID。可能是用户首次使用，尚未设置分数。')
                return None
        except Exception as e:
            print(f"获取分数记录ID时发生异常: {e}")
            return None

    def get_rank_by_score(self, score: int) -> Optional[int]:
        """
        根据分数查询全省排名（位次）。

        Args:
            score (int): 高考分数。

        Returns:
            Optional[int]: 如果成功则返回排名，否则返回None。
        """
        url = f"{self.BASE_URL}/api/bigdata/school/listyearFenduan"
        params = {
            'year': '2025',
            'kelei': 'li',  # 注意：科类是硬编码的
            'page': '1',
            'pagesize': '30',
            'gaokaofen': str(score)
        }
        referer = f"{self.BASE_URL}/bigdata/listyear/weici"
        headers = self._build_get_headers(self.AUTH_TOKEN_GET_ZONE, referer)

        try:
            response = self._get(url, params=params, headers=headers)
            data = response.json()
            
            if data.get('data') and data['data'].get('list'):
                rank = data['data']['list'][0].get('paim')
                return int(rank) if rank is not None else None
            else:
                print(f"API未返回有效的排名数据: {data.get('info', '未知错误')}")
                return None
        except Exception as e:
            print(f"查询排名时发生异常: {e}")
            return None

    def change_score(self, score: int, bonus_score: int = 0) -> Tuple[bool, str]:
        """
        更新已登录用户的分数信息。

        Args:
            score (int): 新的高考分数。
            bonus_score (int, optional): 加分值。默认为0。

        Returns:
            Tuple[bool, str]: (是否成功, 消息文本)。
        """
        # 1. 获取排名
        rank = self.get_rank_by_score(score)
        if rank is None:
            return False, f"无法获取分数 {score} 对应的排名，操作中止。"

        # 2. 获取分数记录ID
        record_id = self.get_score_record_id()
        if record_id is None:
            return False, "无法获取用户分数记录ID，请确保用户已首次设置过分数。"

        # 3. 构造并发送请求
        url = f"{self.BASE_URL}/volunteer/intelligence"
        is_add = 1 if bonus_score > 0 else 0
        payload_list = [{
            'addfen': bonus_score,
            'gaokaofen': score,
            'id': record_id,
            'isadd': is_add,
            'rank': rank
        }]
        headers = self._build_post_headers(self.ACTION_ID_CHANGE_MARK, self.STATE_TREE_CHANGE_MARK, url)
        
        try:
            response = self._post(url, data=json.dumps(payload_list), headers=headers)
            content = response.content.decode('utf-8', errors='ignore')

            if '分数设置成功' in content:
                return True, f"分数设置成功: 分数={score}, 排名={rank}, 加分={bonus_score}"
            else:
                return False, "分数设置失败，服务器未返回成功标识。"
        except Exception as e:
            return False, f"更新分数时发生异常: {str(e)}"

if __name__ == '__main__':
    # --- 配置区 ---
    # 请填入你的真实账号信息
    USERNAME = ""
    PASSWORD = ""
    SCORE = 0  # 初始分数
    BONUS_SCORE = 0  # 初始加分
    # 建议从浏览器登录后，复制一个包含有效acw_tc的cookie
    INITIAL_COOKIE = 'appType=normal; appProvinceId=450000000000; acw_tc=0a03de3f17510475502397178e60f90e9c9ebb61b7e6f953b9576f56ed54f8'
    
    if not USERNAME or not PASSWORD or '...' in INITIAL_COOKIE:
        print("!!! 请在脚本中配置 USERNAME, PASSWORD 和 INITIAL_COOKIE !!!")
    else:
        # --- 执行流程 ---
        print("1. 初始化实例...")
        bk179_session = BK179CRACK(INITIAL_COOKIE)
        
        print("\n2. 尝试登录...")
        login_success, login_message = bk179_session.login(USERNAME, PASSWORD)
        print(f"登录结果: {login_message}")

        if login_success:
            print("\n3. 登录成功，尝试修改分数为 %s 分..." % SCORE)
            change_success, change_message = bk179_session.change_score(score=SCORE, bonus_score=BONUS_SCORE)
            print(f"修改分数结果: {change_message}")
        
        else:
            print("\n登录失败，无法执行后续操作。")