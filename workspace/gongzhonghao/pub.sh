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