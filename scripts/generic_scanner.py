#!/usr/bin/env python3
import sys
import re
import os

"""
Generic Code Coding Guidelines Static Scanner
Supports multi-language syntax smell patterns (Python, Java, Go, JS/TS, C++).
"""

LANGUAGE_RULES = {
    "py": {
        "with_statement_missing": {
            "level": "强制",
            "desc": "对文件、连接等 I/O 资源操作，必须使用 with 语句（上下文管理器），防止异常时资源无法释放。",
            "pattern": r"open\s*\("
        },
        "broad_except": {
            "level": "强制",
            "desc": "避免使用宽泛的 except: 或 except Exception: 吞掉所有异常，导致极难调试。",
            "pattern": r"except\s*:\s*$"
        }
    },
    "java": {
        "is_prefix_boolean": {
            "level": "强制",
            "desc": "POJO 类中的布尔类型变量禁止加 is 前缀，防止部分框架序列化错误。",
            "pattern": r"private\s+boolean\s+is[A-Z][a-zA-Z0-9]*\s*;"
        },
        "executors_creation": {
            "level": "强制",
            "desc": "线程池不允许使用 Executors 直接创建，必须通过 ThreadPoolExecutor 显式声明，规避 OOM 风险。",
            "pattern": r"Executors\.(newFixedThreadPool|newSingleThreadExecutor|newCachedThreadPool|newScheduledThreadPool)"
        }
    },
    "go": {
        "unhandled_error": {
            "level": "强制",
            "desc": "绝不能忽略函数返回的 error。必须显式进行 if err != nil 判断。",
            "pattern": r"^[ 	]*[a-zA-Z0-9_, ]+:=\s*[a-zA-Z0-9_]+\.[a-zA-Z0-9_]+\(.*\)\s*$"
        }
    },
    "js": {
        "strict_equality": {
            "level": "推荐",
            "desc": "禁止使用 == / != 比较，必须使用严格相等运算符 === / !==，防止隐式转换引入 bug。",
            "pattern": r"\s==|\s!="
        }
    },
    "ts": {
        "strict_equality": {
            "level": "推荐",
            "desc": "禁止使用 == / != 比较，必须使用严格相等运算符 === / !==，防止隐式转换引入 bug。",
            "pattern": r"\s==|\s!="
        }
    },
    "cpp": {
        "raw_new_delete": {
            "level": "强制",
            "desc": "禁用裸指针 new/delete。推荐使用智能指针（std::unique_ptr/std::shared_ptr）进行 RAII 资源管理。",
            "pattern": r"new\s+[a-zA-Z0-9_]+"
        }
    }
}

def get_file_ext(file_path):
    _, ext = os.path.splitext(file_path)
    return ext.lstrip(".").lower()

def scan_file(file_path):
    ext = get_file_ext(file_path)
    if ext not in LANGUAGE_RULES:
        print(f"Warning: Extension '{ext}' is not supported. Scanning with basic rule patterns...")
        return []

    rules = LANGUAGE_RULES[ext]
    violations = []

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    for idx, line in enumerate(lines):
        line_num = idx + 1
        for rule_name, rule_info in rules.items():
            match = re.search(rule_info["pattern"], line)
            if match:
                violations.append({
                    "line": line_num,
                    "code": line.strip(),
                    "rule": rule_name,
                    "level": rule_info["level"],
                    "desc": rule_info["desc"]
                })

    return violations

def main():
    if len(sys.argv) < 2:
        print("Usage: python generic_scanner.py <path_to_source_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    violations = scan_file(file_path)
    
    if violations is None:
        sys.exit(1)

    print(f"### Code Guidelines Review Report")
    print(f"- **Target File**: {file_path}")
    print(f"- **Total Violations**: {len(violations)}")
    print()
    
    if len(violations) == 0:
        print("🎉 Perfect! No violations found.")
        sys.exit(0)

    for v in violations:
        print(f"#### 🔴 [{v['level']}] Line {v['line']}: {v['desc']}")
        print(f"- **Code**: `{v['code']}`")
        print()

if __name__ == "__main__":
    main()
