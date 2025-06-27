# app.py

from flask import Flask, request, jsonify, session
from crack import BK179CRACK  # 导入优化后的类
from flask_cors import CORS # 导入 CORS
import uuid
from typing import Dict, Any

# --- Flask 应用设置 ---
app = Flask(__name__)
CORS(app, supports_credentials=True) # 启用CORS
# 在生产环境中，应从环境变量或配置文件中加载此密钥
app.secret_key = 'y7oNaT7TcNGggcp93agQ'

# --- 会话管理 ---
# 这是一个简单的内存存储。在生产环境中，请替换为Redis、Memcached等持久化方案。
user_sessions: Dict[str, BK179CRACK] = {}

def get_bk179_instance() -> BK179CRACK:
    """
    为当前用户获取或创建BK179CRACK的实例。
    使用Flask的session来跟踪用户，并用一个全局字典来存储实例。
    """
    # 确保每个浏览器会话都有一个唯一的ID
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    
    session_id = session['session_id']

    # 如果内存中没有这个session_id对应的实例，则创建一个新的
    if session_id not in user_sessions:
        # 这里的初始cookie是通用的，登录后会被覆盖
        initial_cookie = 'appType=normal; appProvinceId=450000000000; acw_tc=0a03de3f17510475502397178e60f90e9c9ebb61b7e6f953b9576f56ed54f8'
        user_sessions[session_id] = BK179CRACK(cookie=initial_cookie)
        
    return user_sessions[session_id]

# --- API 辅助函数 ---

def create_api_response(success: bool, message: str, data: Any = None, status_code: int = 200) -> tuple:
    """
    创建一个标准格式的API JSON响应。
    """
    response = {
        "success": success,
        "message": message,
        "data": data if data is not None else {}
    }
    return jsonify(response), status_code

# --- API 路由 ---

@app.route('/api/login', methods=['POST'])
def api_login():
    """
    登录API接口。
    接收JSON: {"username": "xxx", "password": "xxx"}
    """
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return create_api_response(False, "请求参数错误，需要'username'和'password'", status_code=400)

    username = data['username']
    password = data['password']
    
    bk_instance = get_bk179_instance()
    
    try:
        success, message = bk_instance.login(username, password)
        return create_api_response(success, message)
    except Exception as e:
        # 捕获底层requests等库可能抛出的未处理异常
        return create_api_response(False, f"登录过程中发生服务器内部错误: {str(e)}", status_code=500)

@app.route('/api/change_score', methods=['POST'])
def api_change_score():
    """
    修改分数API接口。
    接收JSON: {"score": 550, "bonus_score": 0}
    """
    data = request.get_json()
    if not data or 'score' not in data or not isinstance(data['score'], int):
        return create_api_response(False, "请求参数错误，需要一个整数类型的'score'", status_code=400)

    score = data['score']
    bonus_score = data.get('bonus_score', 0)
    
    bk_instance = get_bk179_instance()

    # 检查用户是否已登录 (通过检查session中是否存在user-token)
    if 'user-token' not in bk_instance.session.cookies:
        return create_api_response(False, "用户未登录，请先调用/api/login", status_code=401)

    try:
        success, message = bk_instance.change_score(score, bonus_score)
        return create_api_response(success, message)
    except Exception as e:
        return create_api_response(False, f"修改分数过程中发生服务器内部错误: {str(e)}", status_code=500)

@app.route('/api/get_rank', methods=['GET'])
def api_get_rank():
    """
    查询分数位次API接口。
    通过URL参数接收: /api/get_rank?score=550
    """
    score_str = request.args.get('score')
    if not score_str or not score_str.isdigit():
        return create_api_response(False, "请求参数错误，需要一个整数类型的'score'", status_code=400)

    score = int(score_str)
    bk_instance = get_bk179_instance()
    
    if 'user-token' not in bk_instance.session.cookies:
        return create_api_response(False, "用户未登录，请先调用/api/login", status_code=401)
    
    try:
        rank = bk_instance.get_rank_by_score(score)
        if rank is not None:
            return create_api_response(True, "查询成功", data={"score": score, "rank": rank})
        else:
            return create_api_response(False, f"未能查询到分数 {score} 的排名")
    except Exception as e:
        return create_api_response(False, f"查询排名过程中发生服务器内部错误: {str(e)}", status_code=500)

@app.route('/api/get_score_id', methods=['GET'])
def api_get_score_id():
    """
    获取当前用户分数记录ID的API接口。
    """
    bk_instance = get_bk179_instance()
    
    if 'user-token' not in bk_instance.session.cookies:
        return create_api_response(False, "用户未登录，请先调用/api/login", status_code=401)
        
    try:
        record_id = bk_instance.get_score_record_id()
        if record_id is not None:
            return create_api_response(True, "获取成功", data={"score_record_id": record_id})
        else:
            return create_api_response(False, "未能获取分数记录ID，用户可能尚未设置分数")
    except Exception as e:
        return create_api_response(False, f"获取分数记录ID时发生服务器内部错误: {str(e)}", status_code=500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
