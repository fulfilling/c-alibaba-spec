# 通用代码规范与设计最佳实践指南（多语言综合版）

本指南汇总了软件开发中跨越具体语言（Java、Python、Go、C++、JS/TS 等）的通用编码规约、设计原则和隐患防范标准。

规约等级说明：
- 🔴 **【强制】**：必须遵守，违反可能导致线上崩溃、死锁、资源泄露、数据损坏或安全漏洞。
- 🟡 **【推荐】**：强烈建议遵守，能极大提升可读性、可维护性与协作效率。
- 偏 **【参考】**：供特定高并发、微服务或系统重构场景下斟酌使用。

---

## 1. 软件设计通用原则 (SOLID)

1. 🔴 **【强制】单一职责原则 (Single Responsibility Principle - SRP)**
   - 一个类/函数/模块有且仅有一个引起它变化的原因。禁止将数据库操作、业务逻辑、接口呈现混在同一个类/函数中。
2. 🟡 **【推荐】开闭原则 (Open-Closed Principle - OCP)**
   - 软件实体（类、模块、函数等）应对扩展开放，对修改关闭。建议通过多态和接口（或抽象类）来抽象业务，避免每次新增业务时频繁修改核心的 `if-else` 或 `switch` 分支。
3. 🟡 **【推荐】依赖倒置原则 (Dependency Inversion Principle - DIP)**
   - 高层模块不应依赖低层模块，两者都应依赖其抽象。即：面向接口/抽象编程，不面向具体实现编程。
4. 🟡 **【推荐】防空指针 / 防空对象原则**
   - 在任何调用前，进行防防御性预检。或者使用空对象模式（Null Object Pattern）或 `Optional`（Java）、`?.`（TS/JS）、单行 `if err != nil`（Go）进行保护。

---

## 2. 通用安全规约

1. 🔴 **【强制】防 SQL 注入 (SQL Injection)**
   - 绝不允许使用字符串拼接方式构建 SQL 语句。必须使用参数化查询（如 JDBC PreparedStatements, ORM 绑参，Python DB-API 参数化等）。
2. 🔴 **【强制】敏感数据脱敏**
   - 禁止在日志、错误返回或控制台输出敏感数据（如：密码、秘钥、个人身份身份证/手机号、支付信息）。在展示端必须进行打码脱敏（如 `158****9119`）。
3. 🔴 **【强制】输入校验与防 XSS / CSRF**
   - 任何由客户端或外部系统传入的参数均是“不可信”的，必须执行严格的白名单校验或格式过滤。在输出 HTML 时必须进行正确的字符转义，防范跨站脚本攻击。
4. 🔴 **【强制】秘钥硬编码**
   - 严禁将 API Key、数据库密码、各种秘钥以明文硬编码形式写入代码。必须通过环境变量（Environment Variables）或秘钥中心动态加载。

---

## 3. 语言特定核心规约分支

### 3.1 Python 核心规约

1. 🔴 **【强制】资源自动管理 (Context Manager)**
   - 凡是涉及文件读写、数据库连接、网络套接字等 I/O 资源，必须使用 `with` 语句，确保发生异常时资源仍能被安全释放。
   - *正例*：
     ```python
     with open("file.txt", "r") as f:
         data = f.read()
     ```
2. 🟡 **【推荐】符合 PEP 8 命名标准**
   - 类名使用 `UpperCamelCase`，函数、变量、属性使用 `snake_case`（蛇形命名法），常量使用全大写加下划线。
3. 🔴 **【强制】避免捕获宽泛异常**
   - 严禁直接使用不带任何类型的 `except:` 或宽泛的 `except Exception:` 来吞掉所有异常，这会导致诸如 `KeyboardInterrupt` 无法被捕获，且极难调试。
   - *正例*：`except ValueError as e:` / `except FileNotFoundError:`

---

### 3.2 Java 核心规约

1. 🔴 **【强制】线程资源池化**
   - 线程资源必须通过线程池提供，禁用 `new Thread`。且必须通过 `ThreadPoolExecutor` 显式声明拒绝策略、队列深度和最大线程，规避 `Executors` 带来的 OOM。
2. 🔴 **【强制】ThreadLocal 清理**
   - 线程池场景下的 ThreadLocal 变量必须在 `finally` 块中调用 `remove()` 回收。
3. 🔴 **【强制】集合类安全遍历**
   - 严禁在 `foreach` 或 `for` 循环内部直接进行 `list.remove()` / `list.add()` 操作。必须使用迭代器 `Iterator` 并调用其 `remove()` 方法，或通过 Java 8 提供的 `removeIf()`。

---

### 3.3 Go (Golang) 核心规约

1. 🔴 **【强制】显式错误处理**
   - 绝不能忽略任何可能返回的 `error`。对于每一个带 `error` 返回值的函数，调用后必须显式检查并妥善处理（打日志、重试或包装返回）。
   - *正例*：
     ```go
     val, err := DoSomething()
     if err != nil {
         return fmt.Errorf("failed doing something: %w", err)
     }
     ```
2. 🔴 **【强制】Goroutine 泄露防范**
   - 启动任何 goroutine 前，必须明确它是如何被终结和关闭的，确保其生命周期受 Context 或通道信标控制。
3. 🔴 **【强制】对 Close 对象的异常防护**
   - 保证通道、文件、网络连接的 `Close` 操作。如果是并发场景，注意不要多次关闭 Channel 或向已关闭的 Channel 发送数据，这会引发运行时 `panic`。

---

### 3.4 JS / TS 核心规约

1. 🔴 **【强制】异步错误不丢失 (Async Error Catching)**
   - 对于所有的 `async/await` 调用，必须使用 `try-catch` 包裹，或添加 `.catch()`，严禁产生 unhandled promise rejection（未捕获的异步异常）。
2. 🔴 **【强制】禁止使用等值强制转换比较符 `==`**
   - 比较对象和基础数据类型时，必须使用严格相等运算符 `===` 和 `!==`，避免 JavaScript 自动进行隐式类型转换带来意想不到的 bug。
3. 🟡 **【推荐】强类型安全限制 (TS)**
   - 严禁在 TypeScript 中滥用 `any` 逃避类型检查。在不确定类型时，优先使用 `unknown` 并配合类型守卫（Type Guards）或 `as` 断言。

---

### 3.5 C++ 核心规约

1. 🔴 **【强制】RAII 资源生命周期管理 (Resource Acquisition Is Initialization)**
   - 禁用原始的裸指针 `new` / `delete`。必须使用现代 C++ 智能指针（如 `std::unique_ptr` 或 `std::shared_ptr`）来自动接管内存、互斥锁、网络连接。
2. 🔴 **【强制】防范数组越界与内存溢出**
   - 禁用不安全的 C 风格字符串和内存操作函数（如 `strcpy`, `strcat`, `sprintf`）。必须使用 `std::string` 和 `snprintf`。访问容器时，如不确定索引，推荐使用 `at()` 并捕获 `std::out_of_range` 异常，而不用 `[]`。
3. 🟡 **【推荐】现代 C++ 特性偏好**
   - 优先使用 `const` 和 `constexpr` 表达只读性质。在不需要拷贝的场景下，通过引用传递（`const T&`）或移动语义（Move Semantics）来避免大对象拷贝性能损耗。
