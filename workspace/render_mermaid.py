#!/usr/bin/env python3
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Setup Chrome options for headless operation
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1200,800")

# Create output directory
output_dir = "mermaid_images"
os.makedirs(output_dir, exist_ok=True)

# Mermaid charts data
charts_data = [
    {
        "name": "version_evolution",
        "code": '''graph LR
A["OAuth 1.0<br/>（已废弃）"] --> B["OAuth 2.0<br/>（当前主流）"]
B --> C["OAuth 2.1<br/>（草案阶段）"]
style A fill:#FFCDD2,stroke:#C62828
style B fill:#C8E6C9,stroke:#2E7D32
style C fill:#FFF9C4,stroke:#F9A825'''
    },
    {
        "name": "oauth2_workflow",
        "code": '''graph TB
A["4 种授权流程<br/>（Grant Types）"] --> B["① 授权码模式<br/>Authorization Code"]
A --> C["② 隐式授权模式<br/>Implicit"]
A --> D["③ 客户端凭证模式<br/>Client Credentials"]
A --> E["④ 密码模式<br/>Password"]
B --> F["Access Token"]
C --> F
D --> F
E --> F
F --> G["访问受保护资源"]
style A fill:#E3F2FD,stroke:#1565C0
style F fill:#C8E6C9,stroke:#2E7D32
style G fill:#FFF3E0,stroke:#E65100'''
    },
    {
        "name": "auth_code_flow",
        "code": '''sequenceDiagram
    autonumber
    participant User as 用户
    participant Client as 客户端应用
    participant AuthServer as 授权服务器
    participant ResServer as 资源服务器
    
    Client->>AuthServer: ① 发起令牌请求<br/>GET /authorize?client_id=...&response_type=code&scope=...&redirect_uri=...
    AuthServer->>AuthServer: ② 验证客户端 client_id
    AuthServer->>User: ③ 展示登录页面
    User->>AuthServer: ④ 提交用户名和密码
    AuthServer->>AuthServer: ⑤ 验证用户凭据
    AuthServer->>User: ⑥ 请求用户授权<br/>（展示权限范围，如：分享推文、读取个人信息）
    User->>AuthServer: ⑦ 用户同意授权
    AuthServer->>Client: ⑧ 返回授权码 authorization_code<br/>重定向到 redirect_uri
    Client->>AuthServer: ⑨ 用授权码换取令牌<br/>POST /token（authorization_code + client_id + client_secret）
    AuthServer->>AuthServer: ⑩ 验证 client_id、client_secret、authorization_code
    AuthServer->>Client: ⑪ 返回 Access Token
    Client->>ResServer: ⑫ 携带令牌请求受保护资源<br/>Authorization: Bearer [token]
    ResServer->>ResServer: ⑬ 验证令牌有效性
    ResServer->>Client: ⑭ 返回受保护的资源数据'''
    },
    {
        "name": "implicit_flow",
        "code": '''sequenceDiagram
    autonumber
    participant User as 用户
    participant Client as 客户端应用
    participant AuthServer as 授权服务器
    participant ResServer as 资源服务器
    
    Client->>AuthServer: ① 发起令牌请求<br/>response_type=token
    AuthServer->>AuthServer: ② 验证客户端
    AuthServer->>User: ③ 展示登录页面
    User->>AuthServer: ④ 提交凭据
    AuthServer->>AuthServer: ⑤ 验证凭据
    AuthServer->>User: ⑥ 请求授权
    User->>AuthServer: ⑦ 同意授权
    AuthServer->>Client: ⑧ 直接返回 Access Token<br/>（重定向到 redirect_uri）
    
    Note over Client,AuthServer: 没有第 ⑨⑩⑪ 步<br/>无需授权码换令牌
    
    Client->>ResServer: ⑨ 携带令牌请求资源
    ResServer->>Client: ⑩ 返回资源数据'''
    },
    {
        "name": "client_credentials_flow",
        "code": '''sequenceDiagram
    autonumber
    participant Client as 客户端应用
    participant AuthServer as 授权服务器
    participant ResServer as 资源服务器
    
    Note over Client,AuthServer: 没有用户参与
    
    Client->>AuthServer: ① 请求令牌<br/>POST /token<br/>client_id + client_secret<br/>grant_type=client_credentials
    AuthServer->>AuthServer: ② 验证客户端凭证
    AuthServer->>Client: ③ 返回 Access Token
    Client->>ResServer: ④ 携带令牌请求资源
    ResServer->>Client: ⑤ 返回资源数据'''
    },
    {
        "name": "password_flow",
        "code": '''sequenceDiagram
    autonumber
    participant User as 用户
    participant Client as 客户端应用
    participant AuthServer as 授权服务器
    participant ResServer as 资源服务器
    
    User->>Client: ① 提供用户名和密码
    Client->>AuthServer: ② 请求令牌<br/>POST /token<br/>username + password<br/>client_id + client_secret<br/>grant_type=password
    AuthServer->>AuthServer: ③ 验证用户凭据和客户端凭证
    AuthServer->>Client: ④ 返回 Access Token
    Client->>ResServer: ⑤ 携带令牌请求资源
    ResServer->>Client: ⑥ 返回资源数据'''
    },
    {
        "name": "mode_selection",
        "code": '''flowchart TD
    A["需要获取 OAuth 令牌"] --> B{"是否有用户参与？"}
    B -->|"否（M2M）"| C["客户端凭证模式<br/>Client Credentials"]
    B -->|"是"| D{"客户端是否有后端服务器？"}
    D -->|"是"| E["授权码模式<br/>Authorization Code<br/>（推荐 ⭐）"]
    D -->|"否（纯前端）"| F{"是否可以使用 PKCE？"}
    F -->|"是"| G["授权码模式 + PKCE<br/>（推荐 ⭐）"]
    F -->|"否"| H["隐式授权模式<br/>Implicit<br/>（⚠️ 已废弃）"]
    
    style E fill:#C8E6C9,stroke:#2E7D32
    style G fill:#C8E6C9,stroke:#2E7D32
    style C fill:#E3F2FD,stroke:#1565C0
    style H fill:#FFCDD2,stroke:#C62828'''
    },
    {
        "name": "token_lifecycle",
        "code": '''flowchart TD
    A["获取 Access Token<br/>+ Refresh Token"] --> B["使用 Access Token<br/>访问受保护资源"]
    B --> C{"Access Token<br/>是否过期？"}
    C -->|"否"| B
    C -->|"是"| D["使用 Refresh Token<br/>请求新的 Access Token"]
    D --> E{"Refresh Token<br/>是否有效？"}
    E -->|"是"| F["颁发新的 Access Token<br/>+ 新的 Refresh Token"]
    F --> B
    E -->|"否（过期或已使用）"| G["用户需要重新登录授权"]
    G --> A
    
    style A fill:#E3F2FD,stroke:#1565C0
    style B fill:#C8E6C9,stroke:#2E7D32
    style D fill:#FFF9C4,stroke:#F9A825
    style G fill:#FFCDD2,stroke:#C62828'''
    },
    {
        "name": "oauth21_security",
        "code": '''graph TB
    A["OAuth 2.1 安全增强"] --> B["✅ 强制使用 PKCE<br/>所有授权码流程都必须使用"]
    A --> C["❌ 废弃隐式授权模式<br/>不再允许 response_type=token"]
    A --> D["❌ 废弃密码模式<br/>不再允许 grant_type=password"]
    A --> E["✅ 精确匹配 redirect_uri<br/>禁止通配符，防止开放重定向攻击"]
    A --> F["✅ 禁止 URL 传递令牌<br/>必须使用 Authorization 请求头"]
    A --> G["✅ Refresh Token 一次性使用<br/>用过即失效，颁发新的"]
    
    style A fill:#E3F2FD,stroke:#1565C0
    style B fill:#C8E6C9,stroke:#2E7D32
    style C fill:#FFCDD2,stroke:#C62828
    style D fill:#FFCDD2,stroke:#C62828
    style E fill:#C8E6C9,stroke:#2E7D32
    style F fill:#C8E6C9,stroke:#2E7D32
    style G fill:#C8E6C9,stroke:#2E7D32'''
    },
    {
        "name": "pkce_flow",
        "code": '''sequenceDiagram
    autonumber
    participant Client as 客户端应用
    participant AuthServer as 授权服务器
    
    Note over Client: 生成随机字符串 code_verifier<br/>计算哈希 code_challenge = BASE64URL(SHA256(code_verifier))
    
    Client->>AuthServer: ① 授权请求<br/>携带 code_challenge
    AuthServer->>Client: ② 返回 authorization_code
    Client->>AuthServer: ③ 令牌请求<br/>携带 code_verifier
    
    Note over AuthServer: 计算 SHA256(code_verifier)<br/>与之前收到的 code_challenge 比对<br/>一致则验证通过
    
    AuthServer->>Client: ④ 返回 Access Token'''
    },
    {
        "name": "security_practices",
        "code": '''graph TB
    A["OAuth 安全最佳实践"] --> B["令牌存储"]
    A --> C["令牌传输"]
    A --> D["流程选择"]
    A --> E["令牌管理"]
    
    B --> B1["❌ 不要存在 localStorage / sessionStorage"]
    B --> B2["✅ SPA：仅存在内存中"]
    B --> B3["✅ 服务端：加密存储在服务端会话中"]
    B --> B4["✅ 使用 BFF 模式将令牌排除在浏览器之外"]
    
    C --> C1["✅ 使用 Authorization: Bearer 头部传递"]
    C --> C2["❌ 禁止通过 URL 查询参数传递"]
    C --> C3["✅ 始终使用 HTTPS / TLS"]
    
    D --> D1["✅ 所有场景使用授权码模式 + PKCE"]
    D --> D2["❌ 禁止使用隐式授权模式"]
    D --> D3["❌ 禁止使用密码模式"]
    
    E --> E1["✅ Access Token 有效期：15-30 分钟"]
    E --> E2["✅ Refresh Token 一次性使用"]
    E --> E3["✅ redirect_uri 精确匹配"]
    E --> E4["✅ 使用 state 参数防止 CSRF"]
    
    style A fill:#E3F2FD,stroke:#1565C0
    style B fill:#FFF3E0,stroke:#E65100
    style C fill:#E8F5E9,stroke:#2E7D32
    style D fill:#FCE4EC,stroke:#C62828
    style E fill:#F3E5F5,stroke:#7B1FA2'''
    },
    {
        "name": "complete_pkce_flow",
        "code": '''sequenceDiagram
    autonumber
    participant User as 用户
    participant Client as 客户端应用
    participant AuthServer as 授权服务器
    participant ResServer as 资源服务器
    
    Note over Client: 生成 code_verifier（随机字符串）<br/>计算 code_challenge = BASE64URL(SHA256(code_verifier))
    
    Client->>AuthServer: ① 授权请求<br/>client_id + response_type=code<br/>+ scope + redirect_uri + state<br/>+ code_challenge + code_challenge_method=S256
    AuthServer->>AuthServer: ② 验证客户端
    AuthServer->>User: ③ 展示登录页面
    User->>AuthServer: ④ 提交凭据
    AuthServer->>AuthServer: ⑤ 验证凭据
    AuthServer->>User: ⑥ 请求授权
    User->>AuthServer: ⑦ 同意授权
    AuthServer->>Client: ⑧ 返回 authorization_code + state<br/>重定向到 redirect_uri
    Client->>Client: 验证 state 参数
    Client->>AuthServer: ⑨ 令牌请求<br/>authorization_code + client_id<br/>+ client_secret + code_verifier
    AuthServer->>AuthServer: ⑩ 验证 client_id、client_secret<br/>验证 authorization_code<br/>验证 SHA256(code_verifier) == code_challenge
    AuthServer->>Client: ⑪ 返回 Access Token + Refresh Token
    Client->>ResServer: ⑫ 请求资源<br/>Authorization: Bearer [token]
    ResServer->>ResServer: ⑬ 验证令牌
    ResServer->>Client: ⑭ 返回资源数据'''
    }
]

def create_html_template(mermaid_code):
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Mermaid Chart</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.min.js"></script>
    <style>
        body {{ margin: 0; padding: 20px; background: white; }}
        .mermaid {{ max-width: 100%; }}
    </style>
</head>
<body>
    <div class="mermaid">{mermaid_code}</div>
    <script>
        mermaid.initialize({{
            startOnLoad: true,
            theme: 'default',
            securityLevel: 'loose'
        }});
    </script>
</body>
</html>'''

# Initialize the WebDriver
driver = webdriver.Chrome(options=chrome_options)

try:
    for chart in charts_data:
        print(f"Rendering {chart['name']}...")
        
        # Create HTML file for this chart
        html_content = create_html_template(chart['code'])
        html_path = f"/tmp/{chart['name']}.html"
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Open the HTML file in browser
        driver.get(f"file://{html_path}")
        
        # Wait for mermaid to render
        time.sleep(3)
        
        # Take screenshot
        screenshot_path = os.path.join(output_dir, f"{chart['name']}.png")
        driver.save_screenshot(screenshot_path)
        print(f"Saved {screenshot_path}")
        
        # Clean up temp file
        os.remove(html_path)
        
except Exception as e:
    print(f"Error: {e}")
finally:
    driver.quit()

print("All Mermaid charts rendered successfully!")