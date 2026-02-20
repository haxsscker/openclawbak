# Mermaid CLI 图表生成技能

## 工作流程
1. 所有通过mermaid-cli生成的图表图片都必须存放在 `/root/.openclaw/workspace/mermaid-cli/` 目录下
2. 每个图表对应一个.mmd文件和一个.png文件，文件名保持一致
3. 在处理Markdown文档时，将Mermaid代码块替换为本地图片链接，指向mermaid-cli目录下的对应PNG文件

## 文件结构
```
mermaid-cli/
├── SKILL.md                 # 本技能说明文件
├── diagram1.mmd            # Mermaid源代码文件
├── diagram1.png            # 生成的PNG图片
├── diagram2.mmd            # Mermaid源代码文件  
├── diagram2.png            # 生成的PNG图片
└── ...
```

## 使用规范
- 生成图片时使用命令：`mmdc -i input.mmd -o output.png --puppeteerConfigFile /root/.openclaw/workspace/puppeteer-config.json`
- 确保puppeteer配置文件存在以避免沙箱问题
- 所有公众号相关的Mermaid图表都应遵循此归档规范