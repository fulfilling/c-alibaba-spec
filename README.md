# 通用多语言代码规范与质量审计专家 (Generic Coding Guidelines Skill)

本文件夹是一个针对多语言（Python, Go, Java, JS/TS, C++ 等）研发场景的 **AI Agent 运行时 Skill 规范包**。它将跨语言的最佳实践、通用软件设计原则（如 SOLID 原则）以及高频质量隐患封装为结构化的配置文件和自动化脚本，使 AI 助手或开发工具可以一键加载并进行代码质量扫描。

---

## 📂 目录结构说明

```text
c-alibaba-spec/
├── README.md                   # 本说明文件
├── SKILL.md                    # 标准 Skill 描述、多语言工作流与交付契约 (Tabbit 专用)
├── references/
│   └── guidelines.md           # 跨语言设计原则及主流语言（Python, Go, Java, TS, C++）的核心规约快速字典
└── scripts/
    └── generic_scanner.py      # 多语言自适应静态代码坏味道嗅探扫描脚本 (Python)
```

---

## 🚀 核心组件介绍

### 1. 跨语言质量字典 (`references/guidelines.md`)
提炼了通用及语言特定的核心规约，并分为**【强制】**、**【推荐】**、**【参考】**三级：
- **经典设计原则**：深度集成 SOLID 原则、防空指针/防空对象等防御性编程机制。
- **通用安全防范**：防 SQL 注入（绑参限制）、数据脱敏传输、密钥防硬编码等。
- **主流语言核心分支**：
  - **Python**：使用 `with` 上下文管理 I/O、限制捕获宽泛异常（`except Exception`）。
  - **Go**：显式错误处理、防范 Goroutine 泄露与 Close channel 异常 Panic。
  - **Java**：强制线程资源池化限制、`ThreadLocal` 回收保障。
  - **JS/TS**：异步 Promise 未捕获防范、严格相等比较符（`===`）、强类型逃避检查限制。
  - **C++**：现代 RAII 资源回收、容器越界安全保障等。

### 2. 多语言扫描器 (`scripts/generic_scanner.py`)
内置于规范包的轻量级 Python 静态分析脚本。它可以自适应识别文件后缀（`.py`, `.java`, `.go`, `.js`, `.ts`, `.cpp` 等）并快速探测代码中的危险不合规项。
#### 运行方法
在沙箱或你的本地控制台运行：
```bash
python3 scripts/generic_scanner.py <待检测源代码文件路径>
```

---

## 🎯 在 AI Agent / Tabbit 中使用

1. **直接赋予系统提示词 (System Prompt)**：
   您可以直接将本文件夹下 `SKILL.md` 中定义的角色与契约配置为 Agent 的提示词，使其扮演“多语言代码质量专家”。
2. **自动化扫描**：
   在 AI 研发流中，Agent 可以先通过 `generic_scanner.py` 进行静态扫描生成预分析，再针对核心违规代码生成规范的重构正反例。
