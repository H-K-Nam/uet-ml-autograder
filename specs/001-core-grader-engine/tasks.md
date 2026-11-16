# Tasks: Core Grader Engine (PoC v0.1)

**Feature**: `001-core-grader-engine`  
**Prerequisites**: [spec.md](file:///d:/uet-ml-autograder/specs/001-core-grader-engine/spec.md), [plan.md](file:///d:/uet-ml-autograder/specs/001-core-grader-engine/plan.md), [constitution.md](file:///d:/uet-ml-autograder/.specify/memory/constitution.md)  

---

## Phase 1: Environment Setup (Thiết lập môi trường)

- [x] **T001**: Khởi tạo virtual environment `.venv` tại `D:\uet-ml-autograder` bằng `uv venv` và cài đặt dependencies từ `requirements.txt`.
- [x] **T002**: Kiểm tra cú pháp toàn bộ file mã nguồn hiện có trong `src/` (`py_compile`).

---

## Phase 2: Core Execution & Local Verification (Kiểm chứng chế độ --local)

- [x] **T003**: Chạy thử nghiệm `cli.py` ở chế độ `--local` với `sample_solution_correct.py` (Kỳ vọng: Đạt 100/100, exit code 0).
- [x] **T004**: Chạy thử nghiệm `cli.py` ở chế độ `--local` với `sample_solution_wrong.py` (Kỳ vọng: Báo lỗi test case, exit code 1).
- [x] **T005**: Chạy thử nghiệm `cli.py` ở chế độ `--local` với `sample_solution_timeout.py` (Kỳ vọng: Ngắt an toàn sau timeout, exit code 1).

---

## Phase 3: Notebook Extractor Verification (Kiểm chứng bóc tách .ipynb)

- [x] **T006**: Tạo file sổ tay mẫu `sample_solution_correct.ipynb` cho Bài tập 1 chứa mã ma thuật `%matplotlib inline` và cell đánh dấu `# GRADE_CELL`.
- [x] **T007**: Chạy chấm thử nghiệm trực tiếp trên file `sample_solution_correct.ipynb` ở chế độ `--local` (Kỳ vọng: Trích xuất thành công, đạt 100/100 điểm).

---

## Phase 4: Git Audit & Evidence Reporting (Kiểm chứng lớp 3 & Báo cáo)

- [x] **T008**: Chạy `git status` và `git diff` kiểm toán toàn bộ kho mã nguồn đảm bảo sạch sẽ.
- [x] **T009**: Commit các cập nhật vào Git với thông điệp chuẩn mực.
- [x] **T010**: Xuất báo cáo bằng chứng nghiệm thu (Evidence Report) sẵn sàng báo cáo Thầy Dũng.
