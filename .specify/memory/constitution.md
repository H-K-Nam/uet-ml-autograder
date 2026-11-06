# UET ML Autograder Constitution

Dự án Nghiên cứu Khoa học: **Xây dựng hệ thống chấm bài tập cho môn Học máy** (UET ML Autograder).
Đơn vị: Trường Đại học Công nghệ - ĐHQGHN (VNU-UET).
Giảng viên hướng dẫn: TS. Nguyễn Ngọc Dũng.
Thời gian thực hiện: 7 đến 8 tuần (Hình thức cá nhân).

---

## I. Core Principles (Các nguyên tắc cốt lõi bất biến)

### Principle 1: Strict Sandbox Isolation (Cô lập thực thi an toàn)
- Toàn bộ mã nguồn bài nộp của sinh viên khi chấm chính thức phải được thực thi trong môi trường Docker Container cô lập tuyệt đối.
- Bắt buộc cấu hình: `network_mode="none"` (ngắt toàn bộ kết nối mạng để chống rò rỉ đề bài và gian lận).
- Bắt buộc giới hạn tài nguyên: RAM tối đa (512MB - 1024MB), CPU quota (1 core), và Timeout độc lập từ tiến trình giám sát (10s - 30s) để ngăn chặn vòng lặp vô hạn và rò rỉ bộ nhớ.
- Cung cấp cờ dự phòng `--local` phục vụ debug cục bộ an toàn trước khi đẩy vào Docker.

### Principle 2: Deterministic ML Evaluation & Seed Injection (Tính tất định & Cố định Seed)
- Mọi bài toán Học máy có yếu tố ngẫu nhiên (khởi tạo trọng số, shuffle dữ liệu, mini-batch) phải được tiêm mã cố định seed (`random.seed(42)`, `np.random.seed(42)`, `torch.manual_seed(42)`) ngay trước khi nạp mã nguồn sinh viên.
- Bài toán phải cho ra cùng một kết quả nhất quán trên mọi lần chấm.

### Principle 3: Dual-Format Support (.py & .ipynb) (Hỗ trợ tệp Python và Jupyter Notebook)
- Hệ thống phải hỗ trợ chấm trực tiếp cả tệp mã nguồn Python (`.py`) và tệp sổ tay (`.ipynb`).
- Với Jupyter Notebook: Mô đun `notebook_extractor` phải bóc tách chính xác các cell được đánh dấu `# GRADE_CELL` hoặc thẻ `grade`, tự động lọc bỏ các mã ma thuật (`%matplotlib`, `!pip`, v.v.) trước khi thực thi.

### Principle 4: Quantitative Metric & Tolerance Assessment (Đánh giá định lượng có dung sai)
- Không so khớp chuỗi ký tự đơn thuần. Hệ thống phải đánh giá theo 2 hình thức:
  1. Kiểm thử hàm thuật toán (Unit Test) với dung sai sai số thực tế: `np.allclose(actual, expected, atol=tolerance)`.
  2. Đánh giá chất lượng mô hình trên tập kiểm thử ẩn qua các độ đo chuẩn: MSE, MAE, Accuracy, F1-score.

### Principle 5: 3-Tier Pre-Flight Verification Gate (Quy trình kiểm chứng 3 lớp)
Trước khi kết luận bất kỳ nhiệm vụ nào là "hoàn thành" và commit vào Git, bắt buộc phải vượt qua đủ 3 lớp kiểm tra:
- **Lớp 1 (Vi mô - Micro):** Cú pháp hợp lệ (`py_compile`), 100% unit tests của hệ thống autograder phải PASS.
- **Lớp 2 (Trung mô - Meso):** Chạy thử nghiệm thực tế với 3 kịch bản bài nộp mẫu (`correct` $\rightarrow$ đạt điểm tối đa, `wrong` $\rightarrow$ bị trừ điểm chính xác, `timeout` $\rightarrow$ ngắt an toàn đúng giới hạn).
- **Lớp 3 (Vĩ mô - Macro):** Rà soát `git status` và `git diff`, đảm bảo không có file rác, không rò rỉ credentials hoặc file cấu hình cá nhân.

### Principle 6: Evidence-First Reporting (Báo cáo luôn đi kèm bằng chứng)
- Mọi kết luận kỹ thuật báo cáo cho Giảng viên hướng dẫn phải đi kèm đầu ra thực tế từ Terminal (Exit code, Execution time, Memory footprint, Pass/Fail matrix).

---

## II. Technical Stack & Architectural Constraints

- **Ngôn ngữ:** Python 3.10+ (sử dụng typing, pydantic, dataclasses).
- **Môi trường Sandbox Runtime:** `python:3.11-slim` chứa các thư viện khoa học chuẩn: `numpy`, `scikit-learn`, `pandas`, `pytest`.
- **Giao diện điều khiển:** 
  - Giai đoạn 1 (Milestone 1): Giao diện dòng lệnh CLI chuẩn mực (Click/Typer) xuất kết quả dạng Structured JSON + Human-readable stdout.
  - Giai đoạn 2 (Milestone 2): Mở rộng API (FastAPI) và giao diện trực quan tinh gọn (Streamlit).

---

## III. Phân kỳ thực hiện (7-8 Tuần)

1. **Tuần 1 - 2 (Milestone 001 - Core Grader PoC v0.1):** Hoàn thiện CLI, Extractor, Docker Sandbox, và bộ nghiệm thu cho Giảng viên hướng dẫn.
2. **Tuần 3 - 4 (Milestone 002 - Advanced Evaluation & Seed Injection):** Hoàn thiện metric evaluation, tolerance matching, và bộ bài tập mẫu số 2, 3.
3. **Tuần 5 (Milestone 003 - Minimal Web Interface):** Xây dựng FastAPI backend và giao diện nộp bài Streamlit.
4. **Tuần 6 (Milestone 004 - Benchmarking & Empirical Validation):** Thu thập số liệu đo đạc tài nguyên, độ trễ và độ an toàn phục vụ bài báo.
5. **Tuần 7 - 8 (Milestone 005 - Thesis & Defense):** Biên soạn báo cáo khoa học hoàn chỉnh và chuẩn bị slide bảo vệ.

---

## IV. Governance

- Bản Hiến pháp này là quy chuẩn kỹ thuật tối cao của dự án. Mọi thay đổi về kiến trúc hoặc hạ tầng phải được cập nhật vào tài liệu này.
- Các tài liệu đặc tả `spec.md`, kế hoạch `plan.md` và nhiệm vụ `tasks.md` của từng Milestone phải luôn tuân thủ các nguyên tắc trên.

**Version**: 1.0.0 | **Ratified**: 2026-11-16 | **Status**: ACTIVE
