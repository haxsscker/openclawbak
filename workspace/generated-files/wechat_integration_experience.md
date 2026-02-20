# WeChat 公众号对接集成经验记录

## 项目背景

为实现自动化内容发布流程，将 OpenClaw 与微信公众号进行集成，支持一键将 Markdown 格式的文章发布到微信公众号草稿箱。

## 技术栈

- **核心工具**: [wenyan-cli](https://github.com/caol64/wenyan-cli)
- **封装方式**: OpenClaw Skill 封装
- **认证方式**: 微信公众号 AppID + AppSecret
- **部署环境**: Linux 服务器 (OpenClaw 工作区)

## 配置信息

### API 凭证
```bash
export WECHAT_APP_ID=wx97e912e779e8e36f
export WECHAT_APP_SECRET=d8bb15b6ea2ddbc37354460dfbe666b5
```

> **重要安全提示**: 确保服务器 IP 已添加到微信公众号后台的 IP 白名单中

## 实现方案

### 1. 自定义发布脚本 (`pub.sh`)

创建了专用的发布脚本，解决了以下关键问题：

- **环境隔离**: 独立的环境变量设置，避免与其他进程冲突
- **超时保护**: 60秒超时机制，防止长时间阻塞
- **文件验证**: 自动验证输入文件是否存在
- **默认回退**: 支持无参数调用，默认使用预设文件

```bash
#!/bin/bash
# ============================================
# OpenClaw 专用发布脚本（支持动态 Markdown 文件）
# 用法: ./pub.sh [Markdown文件路径]
# ============================================

# 1. 加载完整环境
export HOME=/root
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
source /root/.bashrc 2>/dev/null
export WECHAT_APP_ID=wx97e912e779e8e36f 
export WECHAT_APP_SECRET=d8bb15b6ea2ddbc37354460dfbe666b5

# 2. 设置默认文件路径
DEFAULT_MD_FILE="/root/.openclaw/workspace/gongzhonghao/safety_letter.md"

# 3. 获取输入参数或使用默认值
md_file="${1:-$DEFAULT_MD_FILE}"

# 4. 验证文件存在性
if [[ ! -f "$md_file" ]]; then
    echo "错误: 文件不存在 - $md_file" >&2
    exit 1
fi

# 5. 执行发布（超时60秒 + 关闭 stdin）
timeout 60 wenyan publish \
  -f "$md_file" \
  -t lapis \
  < /dev/null \
  2>&1

exit $?
```

### 2. Markdown 格式规范

通过实际测试发现，**wenyan-cli 对 Frontmatter 有严格要求**：

#### 必需字段（实测验证）
```markdown
---
title: 文章标题（必填！）
cover: 封面图片URL或路径（必填！）
---
```

> **关键发现**: 虽然官方文档提到"正文有图片可省略 cover"，但实际测试中 **title 和 cover 都是必需字段**，缺少任一都会报错 "未能找到文章封面"。

#### 支持的封面图格式
- **相对路径**: `./assets/cover.jpg` (推荐，便于分享)
- **绝对路径**: `/root/.openclaw/workspace/cover.jpg`
- **网络图片**: `https://example.com/cover.jpg`

### 3. 功能特性

- ✅ **自动图片上传**: 所有本地和网络图片自动上传到微信图床
- ✅ **代码高亮**: 支持多种主题和代码高亮方案
- ✅ **主题定制**: 内置 lapis、phycat 等主题，支持自定义 CSS
- ✅ **一键发布**: 直接推送到公众号草稿箱，无需手动复制粘贴

## 使用流程

1. **准备内容**: 按规范编写 Markdown 文件
2. **执行发布**: 运行 `./pub.sh /path/to/article.md`
3. **审核发布**: 在微信公众号后台审核并正式发布

## 故障排查

### 常见问题及解决方案

| 问题 | 错误信息 | 解决方案 |
|------|----------|----------|
| IP 未授权 | `ip not in whitelist` | 在公众号后台添加服务器 IP 到白名单 |
| 工具未安装 | `wenyan: command not found` | `npm install -g @wenyan-md/cli` |
| 凭证缺失 | `WECHAT_APP_ID is required` | 设置正确的环境变量 |
| 格式错误 | `未能找到文章封面` | 确保 Frontmatter 包含 title 和 cover |

## 实际应用案例

成功发布了《策马奔腾启新程 ——2025 学年第一学期一年级寒假实践活动倡议》等教育类文章，验证了整个流程的可靠性。

## 经验总结

1. **环境隔离很重要**: 自定义脚本确保了稳定的运行环境
2. **格式验证必须严格**: Frontmatter 的完整性直接影响发布成功率
3. **超时机制必要**: 防止网络问题导致的长时间阻塞
4. **IP 白名单配置**: 这是很多用户容易忽略的关键步骤

## 后续优化方向

- [ ] 添加更详细的日志记录
- [ ] 支持批量发布功能
- [ ] 集成发布状态通知
- [ ] 增加内容预览功能

---
*记录时间: 2026年2月19日*
*记录人: OpenClaw Assistant*