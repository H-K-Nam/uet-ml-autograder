# Feature Specification: Core Grader Engine (PoC v0.1)

**Feature**: `001-core-grader-engine`  
**Milestone**: Tuần 1-2 (Báo cáo tiến độ Giảng viên hướng dẫn)  
**Created**: 2026-11-16  
**Status**: Approved  

---

## 1. User Scenarios & Testing (Kịch bản kiểm thử)

### User Story 1 - Giảng viên chấm tự động bài nộp Python thuần (.py) (Priority: P1)
Giảng viên chạy câu lệnh CLI để chấm bài nộp dạng script `.py` của sinh viên cho Bài tập 1 (Hồi quy tuyến tính: Normal Equation & MSE).

- **Why this priority**: Là chức năng tối thiểu chứng minh hệ thống có thể ghép nối mã nguồn sinh viên với bộ test suite và tính toán điểm số chính xác.
- **Acceptance Scenarios**:
  1. **Given** bài nộp đúng [sample_solution_correct.py](file:///d:/uet-ml-autograder/assignments/01_linear_regression/sample_solution_correct.py), **When** chạy chấm, **Then** hệ thống in kết quả `100/100` và exit code 0.
  2. **Given** bài nộp sai [sample_solution_wrong.py](file:///d:/uet-ml-autograder/assignments/01_linear_regression/sample_solution_wrong.py), **When** chạy chấm, **Then** hệ thống in thông tin lỗi chi tiết của test case thất bại và trừ điểm tương ứng.
  3. **Given** bài nộp có vòng lặp vô hạn [sample_solution_timeout.py](file:///d:/uet-ml-autograder/assignments/01_linear_regression/sample_solution_timeout.py), **When** chạy chấm, **Then** hệ thống tự động hủy tiến trình sau 30 giây (TLE) và thông báo an toàn.

---

### User Story 2 - Giảng viên chấm tự động bài nộp Jupyter Notebook (.ipynb) (Priority: P2)
Sinh viên nộp bài làm dưới dạng sổ tay Jupyter Notebook. Hệ thống tự động bóc tách các cell lập trình, loại bỏ mã phụ trợ và chấm điểm bình thường.

- **Why this priority**: 90% bài tập môn Học máy trên lớp được giao dưới dạng file `.ipynb`.
- **Acceptance Scenarios**:
  1. **Given** file `.ipynb` chứa code và biểu đồ matplotlib, **When** bóc tách code, **Then** các dòng `%matplotlib inline` và `!pip` được loại bỏ an toàn.
  2. **Given** file `.ipynb` có các cell được gán nhãn `# GRADE_CELL`, **When** chạy chấm, **Then** hệ thống trích xuất đúng các hàm cần chấm và trả về bảng điểm đầy đủ.

---

### User Story 3 - Chế độ thực thi cô lập Docker Sandbox & Dự phòng Local (Priority: P3)
Hệ thống cho phép chạy bằng Docker Sandbox cách ly hoàn toàn (cấm mạng, giới hạn RAM) hoặc chạy dự phòng cục bộ bằng subprocess thông qua cờ `--local`.

- **Why this priority**: Cho phép chạy kiểm thử logic ngay cả khi môi trường máy trạm chưa bật Docker Desktop, đồng thời đảm bảo an toàn tuyệt đối khi chấm chính thức.
- **Acceptance Scenarios**:
  1. **Given** môi trường có Docker, **When** chạy mặc định, **Then** container khởi chạy với `network_mode="none"` và `mem_limit="512m"`.
  2. **Given** cờ `--local`, **When** chạy chấm, **Then** hệ thống chạy an toàn qua Python subprocess và trả về kết quả tương đương.

---

## 2. Requirements (Yêu cầu chức năng & phi chức năng)

### Functional Requirements
- **FR-001**: Hệ thống CLI chấp nhận 2 tham số bắt buộc: `--submission` (đường dẫn file `.py` hoặc `.ipynb`) và `--assignment` (thư mục chứa đề bài và tests).
- **FR-002**: Tự động chèn seed ngẫu nhiên (`seed=42`) vào đầu kịch bản thực thi để đảm bảo tính tất định.
- **FR-003**: Hỗ trợ bóc tách code từ `.ipynb` thông qua `nbformat`.
- **FR-004**: Hỗ trợ cờ `--local` để chạy trong môi trường subprocess thay thế cho Docker.
- **FR-005**: Xuất báo cáo điểm rõ ràng gồm: Tên test case, điểm đạt được, log lỗi (nếu có), và tổng điểm cuối cùng.

### Non-Functional Requirements
- **NFR-001**: Thời gian bóc tách và tạo kịch bản runner < 1 giây.
- **NFR-002**: Cơ chế timeout cưỡng chế ngắt tiến trình sau tối đa 30 giây.
- **NFR-003**: Cấu trúc mã nguồn module hóa rõ ràng theo chuẩn Clean Architecture (`extractor`, `sandbox`, `evaluator`, `cli`).
