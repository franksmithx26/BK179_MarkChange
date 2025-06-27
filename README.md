# BK179 API Server & Web UI

## 简介

本项目是一个完整的全栈应用，旨在演示如何通过Python模拟并封装对“报考一起走”网站 (`www.bk179.com`) 的操作，并提供一个简洁的Web界面来调用这些功能。

项目由两部分组成：

1.  **后端 API 服务 (`app.py`)**: 一个基于 Flask 的Python服务器，它使用 `crack.py` 模块与目标网站进行交互，并将登录、查询、修改分数等功能封装成RESTful API。
2.  **前端操作面板 (`index.html`)**: 一个独立的、响应式的Web UI界面。用户可以通过这个界面输入账号信息、调用后端API，并实时查看操作日志。


## 功能特性

-   **全栈实现**: 包含了从后端模拟到前端调用的完整流程。
-   **独立的会话管理**: 后端为每个API客户端维护独立的登录状态。
-   **简洁的Web UI**:
    -   单文件 `index.html`，无需构建，零依赖。
    -   可配置的API服务器地址，方便在本地开发和线上部署间切换。
    -   清晰的操作日志，实时反馈API请求和响应状态。
-   **易于部署**: 前端UI可以直接部署到 **GitHub Pages**，后端API可以部署在任何支持Python的服务器上。

## 快速开始

按照以下步骤，你可以在几分钟内运行整个项目。

### 1. 准备工作

-   确保你的系统已安装 Python 3.x 和 Git。
-   克隆本项目到本地：
    ```bash
    git clone https://github.com/franksmithx26/BK179_MarkChange.git
    cd BK179_MarkChange
    ```

### 2. 运行后端API服务器

后端服务是所有操作的基础。

1.  **安装依赖**:
    ```bash
    # (推荐在虚拟环境中操作)
    pip install -m requirements.txt
    ```

2.  **配置账号信息**:
    -   打开 `crack.py`文件。
    -   在文件底部的 `if __name__ == '__main__':` 部分，填入你在“报考一起走”网站注册的**真实用户名和密码**。

3.  **启动服务器**:
    ```bash
    python app.py
    ```
    服务器将启动并监听 `http://127.0.0.1:5000`。保持这个终端窗口运行。

### 3. 使用前端操作面板

现在，你可以通过前端UI与后端API进行交互。

1.  **打开 `index.html`**:
    -   在你的文件浏览器中，直接双击打开 `index.html` 文件，它会在你的默认浏览器中运行。

2.  **配置API地址**:
    -   UI界面默认连接的是公共API (`https://179api.gs4.fun/`)。为了连接你本地刚启动的服务器，请在UI中展开“API配置”部分。
    -   将API服务器地址修改为：`http://127.0.0.1:5000/`
    -   点击“保存并应用”。

3.  **操作流程**:
    -   在“用户登录”区域输入你的账号密码，点击**登录**。
    -   观察操作日志，确认登录成功。
    -   登录成功后，“API操作”区域会显示出来。你可以在这里**查询排名**或**修改分数**。
    -   所有操作的结果都会实时显示在日志中。

---

## 部署到线上

### 部署前端 UI (GitHub Pages)

`index.html` 文件被设计为可以轻松部署到任何静态网站托管服务，例如 GitHub Pages。

1.  **推送到GitHub**: 确保你的代码已提交并推送到GitHub仓库。
2.  **启用GitHub Pages**:
    -   在你的GitHub仓库页面，进入 `Settings` > `Pages`。
    -   在 `Source` 部分，选择 `Deploy from a branch`。
    -   选择你的主分支（如 `main`），文件夹设为 `/ (root)`，然后点击 `Save`。
3.  **访问**: 等待几分钟，GitHub会为你生成一个公开的网址（如 `https://franksmithx26.github.io/BK179_MarkChange/`）。任何人都可以通过这个网址访问你的操作面板。

### 部署后端 API

后端 `app.py` 需要部署在一个可以运行Python的服务器上（例如 Heroku, Vercel, Render, 或你自己的VPS）。部署后，你将获得一个公共的API地址，可以在前端UI中配置使用。

## 模块与文件说明

-   **`crack.py` / `crack_optimized.py`**:
    -   核心逻辑模块，封装了 `BK179CRACK` 类。
    -   负责处理所有与 `www.bk179.com` 的底层HTTP交互。
    -   包含了对 Next.js Server Actions 和 RESTful API 两种模式的模拟。

-   **`app.py`**:
    -   基于 Flask 的后端服务器。
    -   为每个用户创建和管理 `BK179CRACK` 实例。
    -   提供 `/api/login`, `/api/get_rank`, `/api/change_score` 等API接口。

-   **`index.html`**:
    -   一个自包含的前端应用，使用原生 JavaScript 和 Pico.css。
    -   提供了与后端API交互的用户界面。

## 注意事项

-   **硬编码值**: 项目中的 `Next-Action` ID、`Authorization` 签名等是硬编码的。如果目标网站更新，这些值可能需要手动更新。
-   **会话存储**: `app.py` 使用内存来存储用户会话，服务器重启会导致登录状态丢失。
-   **免责声明**: 本项目仅用于学习和技术研究目的。请勿用于任何非法用途。

## 许可证

本项目采用 [MIT](LICENSE) 许可证。