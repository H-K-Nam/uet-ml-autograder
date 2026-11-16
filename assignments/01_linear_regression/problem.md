# Bài tập 1: Cài đặt Hồi quy tuyến tính (Linear Regression) từ đầu

## Yêu cầu

Sinh viên cần cài đặt hai hàm sau bằng thư viện NumPy:

1. `compute_mse(y_true, y_pred)`:
   - Tham số: `y_true` (numpy array), `y_pred` (numpy array).
   - Đầu ra: Giá trị trung bình bình phương sai số (Mean Squared Error) dạng số thực `float`.

2. `fit_linear_regression(X, y)`:
   - Tham số: `X` (ma trận đặc trưng cỡ `(N, D)`), `y` (vector nhãn cỡ `(N,)`).
   - Yêu cầu: Sử dụng công thức nghiệm giải tích dạng Normal Equation:
     $$\mathbf{w} = (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{X}^T \mathbf{y}$$
     *(Sinh viên cần tự chèn thêm cột bias bằng 1 vào đầu ma trận $\mathbf{X}$)*.
   - Đầu ra: Vector trọng số $\mathbf{w}$ cỡ `(D + 1,)` gồm cả trọng số bias.
