# 微信公众号发布归档规范

## 目录结构
- 所有微信公众号文章的源文件必须保存在 `/root/.openclaw/workspace/gongzhonghao/` 目录下
- 图片资源应保存在 `/root/.openclaw/workspace/gongzhonghao/images/` 子目录中
- 发布脚本和配置文件保存在 `/root/.openclaw/workspace/gongzhonghao/` 根目录

## 文件命名规范
- Markdown源文件：`{主题}-{日期}.md`（例如：sso-20260219.md）
- 图片文件：`{图表名称}.png`（例如：google-sso.png, saml-flow.png）

## 发布流程
1. 创建Markdown文件并保存到gongzhonghao目录
2. 生成所有需要的图片并保存到images子目录
3. 使用wenyan-cli或自定义脚本发布到草稿箱
4. 确保所有资源都已正确归档

## 注意事项
- 永远不要直接在工作区根目录创建公众号文章
- 所有相关资源（图片、配置等）都必须归档到gongzhonghao目录
- 发布前确保frontmatter包含正确的title和cover字段