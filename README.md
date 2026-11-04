# UET ML Autograder (`uet-ml-autograder`)

Hệ thống chấm bài tự động cho môn Học máy tại Trường Đại học Công nghệ (VNU-UET).

Dự án tập trung giải quyết các bài toán đặc thù trong đánh giá mã nguồn Học máy:
* Cô lập an toàn quá trình thực thi bằng Docker (ngắt mạng, giới hạn RAM và thời gian chạy).
* Trích xuất và kiểm thử mã nguồn từ sổ tay Jupyter Notebook (`.ipynb`) và tệp Python (`.py`).
* Kiểm soát tính bất định của thuật toán bằng cơ chế cố định seed ngẫu nhiên tự động.
* Đánh giá kết quả theo cả hai hình thức: kiểm thử hàm (Unit Test) và so khớp độ đo mô hình (Accuracy, F1, MSE kèm dung sai $\epsilon$).

---

## Cấu trúc thư mục

```
uet-ml-autograder/
├── assignments/              # Đề bài mẫu và bộ test case
│   └── 01_linear_regression/ # Bài tập mẫu 1: Hồi quy tuyến tính
├── docker/                   # Cấu hình môi trường thực thi trong Sandbox
│   └── Dockerfile.grader     # Runtime image chứa Python và thư viện ML
├── src/                      # Mã nguồn hệ thống chấm
│   ├── extractor/            # Bóc tách code từ .ipynb và .py
│   ├── sandbox/              # Quản lý Docker container, limits và timeout
│   ├── evaluator/            # Logic chấm điểm, so khớp metric, seed injection
│   └── cli.py                # Giao diện dòng lệnh thực thi bài chấm
├── tests/                    # Unit tests cho hệ thống autograder
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Yêu cầu môi trường

* Hệ điều hành: Windows 10/11, Linux, hoặc macOS
* Python: Phiên bản 3.10 trở lên
* Docker: Docker Desktop (Windows/macOS) hoặc Docker Engine (Linux)

---

## Cài đặt và sử dụng

### 1. Cài đặt thư viện
```bash
pip install -r requirements.txt
```

### 2. Xây dựng Docker Image cho Sandbox
```bash
docker build -t uet-ml-sandbox:latest -f docker/Dockerfile.grader .
```

### 3. Chạy chấm một bài nộp qua CLI
```bash
python -m src.cli --submission path/to/student_work.ipynb --assignment assignments/01_linear_regression
```

---

## Lộ trình phát triển (7-8 tuần)

* **Giai đoạn 1 (Tuần 1-2):** Xây dựng Core Grader v0.1 (CLI + Docker Sandbox + bóc tách notebook cơ bản).
* **Giai đoạn 2 (Tuần 3-4):** Hoàn thiện mô đun đánh giá metric, dung sai sai số và seed injection.
* **Giai đoạn 3 (Tuần 5):** Bổ sung giao diện web tinh gọn (FastAPI + Streamlit).
* **Giai đoạn 4 (Tuần 6):** Chạy thực nghiệm đo đạc hiệu năng với 03 bài tập mẫu.
* **Giai đoạn 5 (Tuần 7-8):** Hoàn thành báo cáo khoa học và slide bảo vệ.
