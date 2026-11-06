# Implementation Plan: Core Grader Engine (PoC v0.1)

**Feature**: `001-core-grader-engine`  
**Milestone**: Tuần 1-2  
**Spec Reference**: [spec.md](file:///d:/uet-ml-autograder/specs/001-core-grader-engine/spec.md)  
**Constitution Reference**: [constitution.md](file:///d:/uet-ml-autograder/.specify/memory/constitution.md)  

---

## 1. Technical Context

- **Language**: Python 3.10+
- **Core Dependencies**: `click`, `nbformat`, `docker`, `numpy`, `scikit-learn`
- **Sandbox Container**: Docker Engine (`python:3.11-slim`)
- **Execution Engine**:
  - Primary: `DockerSandbox` (cấm mạng, giới hạn 512MB RAM, timeout 30s)
  - Fallback / Dev: `subprocess` runner (với cờ `--local`, timeout 30s)

---

## 2. Architecture & Data Flow

```
                      [Bài nộp .py / .ipynb]
                               │
                               ▼
                   ┌────────────────────────┐
                   │   notebook_extractor   │ (Lọc cell tag, gỡ % và !)
                   └───────────┬────────────┘
                               │ Extracted Code
                               ▼
                   ┌────────────────────────┐
                   │    runner_generator    │ (Inject seed=42 + test_suite.py)
                   └───────────┬────────────┘
                               │ runner.py
            ┌──────────────────┴──────────────────┐
            │                                     │
   [Cờ --local: True]                    [Mặc định: Docker]
            │                                     │
            ▼                                     ▼
 ┌──────────────────────┐              ┌──────────────────────┐
 │ Subprocess Execution │              │    Docker Sandbox    │
 │ (Timeout = 30s)      │              │ (Net: None, RAM:512M)│
 └──────────┬───────────┘              └──────────┬───────────┘
            │                                     │
            └──────────────────┬──────────────────┘
                               │
                               ▼
                   ┌────────────────────────┐
                   │       cli.py           │ (Báo cáo điểm & Exit code)
                   └────────────────────────┘
```

---

## 3. Constitution Compliance Check

| Điều khoản Constitution | Mức độ tuân thủ trong Plan |
| :--- | :--- |
| **Principle 1 (Strict Sandbox)** | `docker_manager.py` thiết lập `network_mode="none"`, `mem_limit="512m"`, timeout 30s. |
| **Principle 2 (Deterministic ML)** | `runner_generator.py` tiêm `seed=42` cho random & numpy ngay đầu file thực thi. |
| **Principle 3 (Dual-Format)** | `notebook_extractor.py` xử lý `.ipynb`, CLI trực tiếp đọc `.py`. |
| **Principle 4 (Metric & Tolerance)** | `test_suite.py` dùng `np.isclose` và `np.allclose` với sai số $\epsilon = 10^{-4}$. |
| **Principle 5 (3-Tier Verification)**| Đầy đủ kịch bản kiểm thử: Unit tests, 3 file bài nộp mẫu, kiểm toán git diff. |
| **Principle 6 (Evidence-First)** | Kết quả in đầy đủ stdout, stderr, execution time và exit code. |

---

## 4. Component Design

1. `src/extractor/notebook_extractor.py`: Sử dụng `nbformat.read` để phân tích AST/JSON của notebook, lọc qua tags (`grade`, `# GRADE_CELL`, `# BEGIN SOLUTION`), loại bỏ `%` và `!`.
2. `src/evaluator/runner_generator.py`: Tạo header tiêm seed, nối mã nguồn sinh viên và nội dung `test_suite.py`.
3. `src/sandbox/docker_manager.py`: Gọi Docker SDK để tạo ephemeral container, mount thư mục tạm dạng `ro` (read-only), bắt ngoại lệ timeout và kiểm tra cờ `OOMKilled`.
4. `src/cli.py`: Giao diện CLI hỗ trợ `--submission`, `--assignment`, `--local`.
