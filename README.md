# Nhóm 3 – Đề tài 24: CI/CD với GitHub Actions

Ứng dụng quản lý công việc hằng ngày (To-do) viết bằng Flask, dùng làm đối tượng để xây dựng quy trình CI/CD bằng GitHub Actions và triển khai lên Render.

- CI: ![CI](https://github.com/233404050154-NguyenHuuAn/project_24/actions/workflows/ci-cd.yml/badge.svg)
- Ứng dụng: https://project-24-x8jl.onrender.com (Render Free, ngủ sau 15 phút không có truy cập, lần mở đầu có thể chờ khoảng một phút)

## Chạy trên máy (Windows PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
flask --app app run --debug
```

Mở http://127.0.0.1:5000. Gunicorn không chạy trên Windows nên local dùng `flask run`.

Kiểm tra chất lượng:

```powershell
flake8
pytest --cov=app --cov=validators --cov-report=term-missing
```

## API

| Route | Mô tả |
|---|---|
| `GET /` | Giao diện chính |
| `GET /health` | `{"status": "ok", "version": ...}` |
| `GET /api/tasks` | Danh sách. Lọc: `done`, `category`, `priority`, `view` (`today`, `upcoming`, `overdue`), `q`. Giá trị sai trả 400 |
| `POST /api/tasks` | Tạo mới, trả 201 |
| `GET /api/tasks/<id>` | Xem một việc, 404 nếu không có |
| `PUT` / `PATCH /api/tasks/<id>` | Sửa các trường được gửi |
| `DELETE /api/tasks/<id>` | Xoá, trả 204 |
| `GET /api/stats` | Thống kê và số đếm cho thanh bên |
| `GET /api/export` | Tải toàn bộ dữ liệu dạng JSON |
| `POST /api/import` | Nhập lại file đã xuất, thay toàn bộ dữ liệu (tối đa 1 MB) |

Mỗi việc có thể có khung giờ `start_time` và `end_time` (dạng `HH:MM`, tuỳ chọn). Giờ phải đi kèm ngày hạn, giờ kết thúc phải có giờ bắt đầu và phải sau giờ bắt đầu. Việc quá hạn vẫn tính theo ngày.

Lỗi 400, 404, 405, 413 đều trả JSON dạng `{"error": "..."}`. Việc "Hôm nay" gồm việc có hạn hôm nay và việc quá hạn chưa xong. "Hôm nay" tính theo giờ Việt Nam.

## Hạn chế

- Dữ liệu lưu trong bộ nhớ, mất khi máy chủ khởi động lại, deploy lại hoặc ngủ (Render Free). Dùng nút Xuất/Nhập JSON để sao lưu.
- Chỉ đúng khi chạy gunicorn với 1 worker.
- Không có đăng nhập, mọi người truy cập cùng thấy chung một danh sách.

## Cấu trúc

```
app.py · validators.py      # backend
templates/ · static/        # giao diện (HTML, CSS, JS thuần)
tests/test_app.py           # pytest
docs/                       # minh chứng, số liệu thí nghiệm, hướng dẫn
```
