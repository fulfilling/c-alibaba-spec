# 开发规范与代码质量审计 Skill 工具包 (Developer Guidelines Skills Pack)

本工具包包含两套标准的 AI Agent 运行时 Skill，旨在将大厂编码规约与通用高质量软件工程实践无缝整合到 AI 研发工作流中。你可以直接将本工具包导入到支持 Tabbit Agent 或类似 AI 框架的运行时中直接调用。

---

## 📂 工具包目录结构

```text
c-alibaba-spec/
├── README.md                           # 本说明文件
├── alibaba-java-guidelines-skill.yaml  # 阿里 Java 规约 Skill 配置 (YAML 格式)
├── alibaba-java-guidelines-skill.json  # 阿里 Java 规约 Skill 配置 (JSON 格式)
├── generic-coding-guidelines-skill.yaml# 通用多语言规约 Skill 配置 (YAML 格式)
├── generic-coding-guidelines-skill.json# 通用多语言规约 Skill 配置 (JSON 格式)
│
├── alibaba-java-guidelines/            # 阿里巴巴 Java 开发手册专家 Skill 源码包
│   ├── SKILL.md                        # 核心 Skill 定义、工作流与契约
│   ├── references/
│   │   └── guidelines.md               # 完整的 Java 规约、MySQL 规约快速字典
│   └── scripts/
│       └── review_code.py              # 轻量级 Java 规约静态扫描 Python 脚本
│
└── generic-coding-guidelines/          # 通用多语言代码规范与质量审计专家 Skill 源码包
    ├── SKILL.md                        # 核心 Skill 定义、通用工作流与契约
    ├── references/
    │   └── guidelines.md               # 跨语言通用设计原则 (SOLID) 及主流语言细则字典
    └── scripts/
        └── generic_scanner.py          # 多语言自适应静态代码坏味道扫描脚本
```

---

## 🛠️ 包含的两个核心 Skill

### 1. 阿里巴巴 Java 开发手册专家 (`alibaba_java_guidelines`)
- **定位**：深度集成《阿里巴巴 Java 开发手册》（华山/泰山/嵩山版综合）。
- **用途**：Java 源代码 Code Review、安全审计、高并发下线程安全与 ThreadLocal 检查、MySQL 数据库建表 DDL 审查、索引和 SQL 高性能审计、工程应用分层及依赖规范。
- **内置工具**：`scripts/review_code.py`，支持一键在沙箱中对指定 Java 源码文件进行【强制】、【推荐】和【参考】规约等级的静态预检。

### 2. 通用代码规范与质量审计专家 (`generic_coding_guidelines`)
- **定位**：面向多语言混合研发场景的跨语言代码质量专家。
- **用途**：支持 Java、Python、Go、TypeScript/JavaScript、C++ 等多门主流语言的合规审查、内存泄露排查、资源回收安全审计、并发模型（Goroutine、多线程、智能指针）健康检查、安全漏洞（SQL注入、秘钥硬编码、数据脱敏）审计。
- **设计规范**：内置经典的 SOLID 原则、防御性编程和 Clean Code 最佳实践。
- **内置工具**：`scripts/generic_scanner.py`，能自适应识别文件类型并对多语言源码进行快速静态代码坏味道嗅探。

---

## 🚀 如何在 Agent 中直接调用？

### 方法 A：作为 System Prompt 直接导入
1. 将 `alibaba-java-guidelines-skill.yaml` 或 `generic-coding-guidelines-skill.yaml` 中的 `system_prompt` 段落直接复制到你的 Agent/LLM 的系统提示词中。
2. 将 `functions` 下定义的 API 结构（如 `review_code`、`explain_rule`）配置为你 Agent 的可调用函数（Tools/Actions）。

### 方法 B：在 Tabbit 运行沙箱中动态加载
如果你在 Tabbit Agent 内部使用：
1. 你的 Agent 可直接执行 `load_skill` 载入对应的 Skill 文件夹。
2. 载入后，Agent 可以读取并解析对应目录下的 `SKILL.md`，并在代码审查过程中通过 `e2b_bash` 调用内置的静态扫描脚本做底层快速过滤：
   - 扫描 Java 文件：`python3 scripts/review_code.py <path_to_java_file>`
   - 扫描多语言文件：`python3 scripts/generic_scanner.py <path_to_source_file>`

---

## 🔴 审计输出规范契约

任何被本工具包激活的 Agent 在完成审计时，必须交付如下结构的 Markdown 审计报告：

1. **审计概览**：包含审计的文件目标、目标语言、发现的🔴【强制】级别（高危）、🟡【推荐】级别（中危）、⚪【参考】级别（低危）缺陷数量汇总。
2. **危害分析与原理解析**：对每一处缺陷说明具体危害（如会导致 OOM、并发死锁、SQL注入、序列化失效等），拒绝盲目限制个性。
3. **对比正反例**：针对发现的问题，提供原不规范的反例代码与重构后绝对符合规约的正例代码。
4. **完整重构代码**：在报告最后提供一份完全重构、可直接无缝替换使用的合规代码文件。
