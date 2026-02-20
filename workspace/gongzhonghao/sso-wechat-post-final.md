---
title: 单点登录（SSO）完整图解
cover: /root/.openclaw/workspace/sso_cover.png
---

# 单点登录（SSO）完整图解

## 一、什么是单点登录（SSO）？

> 一种身份认证策略，允许用户使用 **一个用户名和密码** 登录多个相关但独立的服务。

### Google SSO示例

```mermaid
graph LR
    A[你通过 Gmail 登录] --> B((Gmail))
    B --> C[Google Meet]
    B --> D[YouTube]
    B --> E[Google 日历]
    B --> F[Google 文档]
    B --> G[所有 Google 产品]

    style B fill:#4285F4,stroke:#333,color:#fff
    style C fill:#fff,stroke:#333
    style D fill:#fff,stroke:#333
    style E fill:#fff,stroke:#333
    style F fill:#fff,stroke:#333
    style G fill:#fff,stroke:#333
    style A fill:#FFF9C4,stroke:#333
```

**如果没有 SSO**，你需要为每个服务使用不同的账号密码分别登录。有了 SSO，只需登录一次即可访问所有关联服务。

---

## 二、SAML — 安全断言标记语言

> **SAML**（Security Assertion Markup Language）是用于在各方之间交换**身份认证**和**授权**数据的开放标准。

### 三个核心角色

```mermaid
graph TB
    U[👤 用户 User]
    IDP[🔐 身份提供者 IDP<br>Identity Provider]
    SP[🌐 服务提供者 SP<br>Service Provider]

    U -. "需要访问资源" .-> SP
    U -. "进行身份认证" .-> IDP
    IDP -. "告诉SP该用户是否可信" .-> SP

    style U fill:#E3F2FD,stroke:#1565C0,color:#000
    style IDP fill:#FFF3E0,stroke:#E65100,color:#000
    style SP fill:#E8F5E9,stroke:#2E7D32,color:#000
```

| 角色 | 说明 |
| --- | --- |
| **用户（User）** | 需要访问某些资源的一方 |
| **身份提供者（IDP）** | 确认"用户是谁"以及"用户能做什么"的权威来源 |
| **服务提供者（SP）** | 需要被授权访问的服务 |

---

### SAML 认证流程概览

```mermaid
graph LR
    User((👤 用户)) -->|"① 用户在这里认证"| IDP[🔐 IDP<br>身份提供者]
    IDP -->|"② 生成 SAML 断言"| SAML[📄 SAML 断言<br>XML 文档]
    IDP -->|"③ 发送断言"| SP1((SP1))
    IDP -->|"③ 发送断言"| SP2((SP2))
    IDP -->|"③ 发送断言"| SP3((SP3))
    IDP -->|"③ 发送断言"| SP4((SP4))

    SP1 -->|"④ 验证通过<br>允许访问"| User
    SP2 -->|"④ 验证通过<br>允许访问"| User
    SP3 -->|"④ 验证通过<br>允许访问"| User
    SP4 -->|"④ 验证通过<br>允许访问"| User

    style IDP fill:#FFF3E0,stroke:#E65100
    style SAML fill:#FCE4EC,stroke:#C2185B
    style SP1 fill:#111,stroke:#333,color:#fff
    style SP2 fill:#111,stroke:#333,color:#fff
    style SP3 fill:#111,stroke:#333,color:#fff
    style SP4 fill:#111,stroke:#333,color:#fff
    style User fill:#E3F2FD,stroke:#1565C0
```

> **SAML 断言**是一个包含授权信息的 XML 文档，经过数字签名以确保可信性。对于任何未经认证的访问，用户都会被引导到 IDP 进行登录。

---

### SAML 元数据交换（建立信任）

```mermaid
graph TB
    IDP[🔐 IDP<br>身份提供者] <-->|"交换 XML 元数据<br>配置与证书"| SP1[🌐 SP1<br>服务提供者1]
    IDP <-->|"交换 XML 元数据<br>配置与证书"| SP2[🌐 SP2<br>服务提供者2]

    IDP --- IDP_XML[📋 IDP XML<br>配置与证书]
    SP1 --- SP1_XML[📋 IDP XML 副本<br>配置与证书]
    SP2 --- SP2_XML[📋 IDP XML 副本<br>配置与证书]

    style IDP fill:#FFF3E0,stroke:#E65100
    style SP1 fill:#E8F5E9,stroke:#2E7D32
    style SP2 fill:#E8F5E9,stroke:#2E7D32
    style IDP_XML fill:#F3E5F5,stroke:#7B1FA2
    style SP1_XML fill:#F3E5F5,stroke:#7B1FA2
    style SP2_XML fill:#F3E5F5,stroke:#7B1FA2
```

SAML 断言的格式和内容由 SP 和 IDP **预先协商确定**：

| 内容 | 说明 |
| --- | --- |
| **XML 元数据文件** | 分别放置在 IDP 和各个 SP 上 |
| **配置信息** | 例如："我需要在断言中包含用户邮箱" |
| **证书** | 用于验证断言的数字签名，确保数据可信 |

> 这些元数据也被称为 **SAML 元数据（SAML Metadata）**，这种配置交换用于建立双方之间的信任关系。

---

## 三、它是如何工作的？

启动认证流程有 **两种主要方式**：

```mermaid
graph LR
    A[认证流程] --> B[身份提供者发起<br>IDP-Initiated Flow]
    A --> C[服务提供者发起<br>SP-Initiated Flow]

    style A fill:#E3F2FD,stroke:#1565C0
    style B fill:#FFF3E0,stroke:#E65100
    style C fill:#E8F5E9,stroke:#2E7D32
```

---

### 方式一：身份提供者发起的流程（IDP 发起）

> 客户端**先请求 IDP** 来启动认证流程。

```mermaid
sequenceDiagram
    participant U as 👤 用户
    participant IDP as 🔐 IDP<br>身份提供者
    participant SP as 🌐 SP<br>服务提供者

    U->>IDP: ① 用户请求访问 IDP
    IDP->>U: ② IDP 要求用户进行认证
    U->>IDP: ③ 用户提交认证凭据（用户名/密码）
    
    Note over IDP: ④ 验证凭据<br>如果无效则拒绝

    IDP->>IDP: ⑤ 生成 SAML 断言
    IDP->>SP: ⑥ 将 SAML 断言发送给 SP
    
    Note over SP: ⑦ 验证 SAML 断言<br>是否合法有效

    SP->>U: ⑧ 会话建立，用户获得访问权限
```

**详细步骤说明：**

| 步骤 | 说明 |
| --- | --- |
| ① | 用户主动访问 IDP（身份提供者） |
| ② | IDP 返回登录页面，要求用户认证 |
| ③ | 用户输入用户名/密码等凭据 |
| ④ | IDP 验证凭据，无效则拒绝访问 |
| ⑤ | 验证通过，IDP 生成 SAML 断言（签名的 XML） |
| ⑥ | SAML 断言通过浏览器重定向发送给 SP |
| ⑦ | SP 使用预先配置的证书验证断言的签名和内容 |
| ⑧ | 验证通过，SP 为用户建立会话，授予访问权限 |

---

### 方式二：服务提供者发起的流程（SP 发起）

> 客户端**先请求 SP** 来启动认证流程。

```mermaid
sequenceDiagram
    participant U as 👤 用户
    participant SP as 🌐 SP<br>服务提供者
    participant IDP as 🔐 IDP<br>身份提供者

    U->>SP: ① 用户请求访问 SP 的资源
    
    Note over SP: 发现用户未登录

    SP->>IDP: ② 重定向用户到 IDP 进行认证
    IDP->>U: ③ IDP 要求用户进行认证
    U->>IDP: ④ 用户提交认证凭据
    
    Note over IDP: ⑤ 验证凭据<br>如果无效则拒绝

    IDP->>IDP: ⑥ 生成 SAML 断言
    IDP->>SP: ⑦ 将 SAML 断言发送给 SP
    
    Note over SP: ⑧ 验证 SAML 断言

    SP->>U: ⑨ 会话建立，用户获得访问权限
```

**与 IDP 发起流程的唯一区别：**

```plaintext
IDP 发起：用户 → IDP → SP
SP 发起： 用户 → SP → IDP → SP

SP 发起多了一步：用户先访问 SP，
SP 发现用户未登录，将用户重定向到 IDP。
其余步骤完全相同。
```

---

### 两种流程对比

```mermaid
graph TB
    subgraph IDP发起流程
        A1[👤 用户] -->|"1.先访问"| B1[🔐 IDP]
        B1 -->|"2.认证后"| C1[🌐 SP]
    end

    subgraph SP发起流程
        A2[👤 用户] -->|"1.先访问"| C2[🌐 SP]
        C2 -->|"2.重定向"| B2[🔐 IDP]
        B2 -->|"3.认证后"| C2
    end

    style B1 fill:#FFF3E0,stroke:#E65100
    style C1 fill:#E8F5E9,stroke:#2E7D32
    style A1 fill:#E3F2FD,stroke:#1565C0
    style B2 fill:#FFF3E0,stroke:#E65100
    style C2 fill:#E8F5E9,stroke:#2E7D32
    style A2 fill:#E3F2FD,stroke:#1565C0
```

---

## 四、完整流程总览

```mermaid
graph TB
    subgraph SSO["🔑 单点登录 SSO"]
        direction TB
        DESC["一次登录，访问多个服务"]
    end

    subgraph SAML["📄 SAML 安全断言标记语言"]
        direction TB
        USER["👤 用户"]
        IDP["🔐 身份提供者 IDP"]
        SP["🌐 服务提供者 SP"]
        
        USER -->|"认证"| IDP
        IDP -->|"SAML 断言"| SP
        SP -->|"授权访问"| USER
    end

    subgraph TRUST["🤝 信任建立"]
        direction TB
        META["XML 元数据 + 证书"]
        IDP2["🔐 IDP"] <-->|"交换元数据"| SP2["🌐 SP"]
    end

    subgraph FLOW["⚡ 认证流程"]
        direction LR
        IDP_FLOW["IDP 发起<br>用户→IDP→SP"]
        SP_FLOW["SP 发起<br>用户→SP→IDP→SP"]
    end

    SSO --> SAML
    SAML --> TRUST
    TRUST --> FLOW

    style SSO fill:#E3F2FD,stroke:#1565C0
    style SAML fill:#FFF3E0,stroke:#E65100
    style TRUST fill:#F3E5F5,stroke:#7B1FA2
    style FLOW fill:#E8F5E9,stroke:#2E7D32
```

---

## 五、核心概念速查表

| 术语 | 英文 | 含义 |
| --- | --- | --- |
| 单点登录 | SSO (Single Sign-On) | 一次登录，访问多个服务 |
| 安全断言标记语言 | SAML | 交换认证和授权数据的开放标准 |
| 身份提供者 | IDP (Identity Provider) | 负责认证用户身份的权威来源 |
| 服务提供者 | SP (Service Provider) | 提供用户要访问的服务 |
| SAML 断言 | SAML Assertion | 包含用户认证信息的签名 XML 文档 |
| SAML 元数据 | SAML Metadata | IDP 和 SP 之间交换的配置信息和证书 |
| IDP 发起流程 | IDP-Initiated Flow | 用户先访问 IDP，再跳转到 SP |
| SP 发起流程 | SP-Initiated Flow | 用户先访问 SP，再重定向到 IDP 认证 |

---

## 六、注意事项

```plaintext
📝 说明

SAML 是一个复杂的主题。
本文中的部分细节已被有意省略或简化，
目的是让读者更容易理解核心概念。

实际生产环境中还需要考虑：
  • SAML 2.0 协议的具体绑定方式（HTTP-POST / HTTP-Redirect）
  • 断言的加密与签名细节
  • 会话管理与单点登出（SLO）
  • 与 OAuth 2.0 / OpenID Connect 的集成
```