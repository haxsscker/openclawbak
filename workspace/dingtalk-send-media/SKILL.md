# dingtalk-send-media

**钉钉渠道专用媒体发送技能**

## 功能
- 发送本地图片文件到钉钉对话
- 发送本地文件到钉钉对话
- 自动处理文件路径和格式

## 使用方法

### 发送图片
在回复中包含以下标签：
```
[ DING:IMAGE path="/absolute/local/path/to/image.png" ]
```

### 发送文件  
在回复中包含以下标签：
```
[ DING:FILE path="/absolute/local/path/to/file.pdf" ]
```

## 约束
- 路径必须是本地绝对路径
- 不支持远程URL（http/https）
- 文件必须存在于本地文件系统
- 图片格式支持：png, jpg, jpeg, gif, webp
- 单个文件大小建议不超过10MB

## 示例
```
[ DING:IMAGE path="/root/.openclaw/media/browser/screenshot.png" ]
```