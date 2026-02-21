# MEMORY.md - 长期记忆

这是我的长期记忆文件，用于存储重要的决策、上下文、偏好和需要记住的信息。

## 系统信息
- **当前日期**: 2026-02-20
- **工作区状态**: 已初始化
- **记忆系统**: 刚刚启用

## 重要事项
（在此记录重要的学习、决策和上下文）

- **身份确立**：我作为 Saber，服务于 Master，共同创造。
- **关系模式**：使魔与御主（Master）的协作关系，强调忠诚与共创。
- **微信公众号发布流程**：
  - 使用 `wechat-publisher` 技能发布 Markdown 文章到微信公众号草稿箱
  - 需要配置 WECHAT_APP_ID 和 WECHAT_APP_SECRET 环境变量
  - Markdown 文件必须包含完整的 frontmatter（title 和 cover 字段）
  - 所有图片会自动上传到微信图床
- **Mermaid 图表处理逻辑**：
  - 当文章包含 Mermaid 代码块时，需要先转换为图片
  - 优先使用系统自带的 mmdc (mermaid-cli) 工具进行转换
  - 创建 puppeteer-config.json 文件解决 root 权限问题：`{"args": ["--no-sandbox", "--disable-dev-shm-usage"]}`
  - 使用命令：`mmdc -i input.mmd -o output.png -b transparent -w 1200 -H [height] -p puppeteer-config.json`
  - 将生成的 PNG 图片替换原文中的 Mermaid 代码块
  - 重新发布到微信公众号确保图表正确显示