#!/usr/bin/env python3
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# Setup Chrome options for headless operation with Chromium
chrome_options = Options()
chrome_options.binary_location = "/usr/bin/chromium-browser"
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1200,800")

# Setup ChromeDriver with webdriver-manager
service = Service(ChromeDriverManager().install())

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

# Initialize the WebDriver (using older Selenium syntax for compatibility)
driver = webdriver.Chrome(service=service, options=chrome_options)

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

print("Mermaid charts rendered successfully!")