# Biên bản họp nhóm – Đề tài 24: CI/CD với GitHub Actions

---

# Buổi 1: Phân chia công việc

## Thông tin buổi họp
- Thời gian: 11/10/2026, 20:00 – 20:30
- Hình thức: online qua Zalo
- Có mặt: Ngô Ngọc Ánh, Nguyễn Hữu An, Nguyễn Thị Thanh Hồng; vắng: không
- Chủ trì: Nguyễn Hữu An · Thư ký: Nguyễn Thị Thanh Hồng

## Chương trình (30 phút)
1. (10 phút) An giới thiệu đề tài 24 (CI/CD với GitHub Actions cho ứng dụng web) và hướng thực hiện.
2. (10 phút) Phân chia công việc cho từng thành viên.
3. (10 phút) Thống nhất phương thức thực hiện và cách lưu minh chứng đóng góp.

## 1. Tình hình hiện tại
- Nhóm đã nhận đề tài 24, chưa bắt đầu phần kỹ thuật.
- An đề xuất làm một ứng dụng web Flask nhỏ (To-do), quản lý mã nguồn trên GitHub, dùng GitHub Actions làm pipeline CI/CD và triển khai lên Render.com.

## 2. Phương thức thực hiện
- **Phần kỹ thuật:** An tạo repository `project_24` trên GitHub, xây dựng ứng dụng và pipeline (có dùng Claude Code hỗ trợ viết mã), chạy thí nghiệm, ghi số liệu và quay video demo.
- **Phần lý thuyết và báo cáo:** Ánh và Hồng tìm tài liệu, viết các chương được giao; được thêm làm collaborator để đóng góp file lên repo qua Pull Request.
- **Trao đổi:** qua nhóm Zalo. Báo cáo soạn trên file Word do An lưu trên máy; Ánh và Hồng gửi phần nội dung của mình qua Zalo để An ghép vào file chung.

## 3. Quyết định
- Báo cáo gồm 5 chương: (1) Tổng quan đề tài; (2) Cơ sở lý thuyết; (3) Phân tích, thiết kế và triển khai; (4) Thực nghiệm và đánh giá kết quả; (5) Kết luận và hướng phát triển.
- Phân công như bảng dưới.

## 4. Phân công

| Người | Việc | Hạn | Minh chứng |
|---|---|---|---|
| Ngô Ngọc Ánh | Tìm tài liệu lý thuyết; viết Chương 1 và Chương 2; lập danh mục tài liệu tham khảo | 25/10/2026 | Bản thảo Chương 1–2 gửi qua Zalo, PR trên GitHub |
| Nguyễn Hữu An | Làm phần kỹ thuật (repo, ứng dụng, pipeline, deploy); chạy thí nghiệm; viết Chương 3 và Chương 4; chuẩn bị slide thuyết trình | 25/10/2026 | Lịch sử commit, Pull Request, video demo |
| Nguyễn Thị Thanh Hồng | Viết Chương 5, lời mở đầu và tóm tắt; viết biên bản họp; lập phiếu phân công; chuẩn bị slide thuyết trình | 25/10/2026 | Biên bản họp, phiếu phân công, PR trên GitHub |

## 5. Vấn đề còn mở
- Ánh và Hồng chưa quen thao tác trên GitHub; An sẽ hướng dẫn ở buổi họp sau.
- Ngày họp buổi 2: khi phần kỹ thuật hoàn thành (dự kiến cuối tháng 10).

Thư ký ghi: Nguyễn Thị Thanh Hồng

---

# Buổi 2: Tổng kết phần kỹ thuật và chốt dàn ý báo cáo

## Thông tin buổi họp
- Thời gian: 26/10/2026, 20:00 – 21:00
- Hình thức: online qua Zalo
- Có mặt: Ngô Ngọc Ánh, Nguyễn Hữu An, Nguyễn Thị Thanh Hồng; vắng: không
- Chủ trì: Nguyễn Hữu An · Thư ký: Nguyễn Thị Thanh Hồng

## Chương trình (60 phút)
1. (20 phút) An trình bày những gì đã làm, chia sẻ màn hình: app trên Render, repo, ruleset, một vòng PR → CI → deploy, video demo, bảng thí nghiệm.
2. (10 phút) Ánh và Hồng đặt câu hỏi về pipeline.
3. (10 phút) Thống nhất các điểm cần đưa vào báo cáo: kết quả nổi bật, hạn chế.
4. (10 phút) Chốt dàn ý báo cáo.
5. (10 phút) Ánh và Hồng commit file của mình lên repo qua web GitHub, An hướng dẫn.

## 1. Tình hình đã làm (An báo cáo; nguồn: nhật ký repo)
- Repo `project_24` công khai, 17 Pull Request (16 đã merge, 1 đóng không merge). Ánh và Hồng đã là collaborator.
- App To-do Flask chạy tại https://project-24-x8jl.onrender.com, phiên bản 1.1.0.
- Pipeline: lint → test (3 phiên bản Python) → deploy qua Deploy Hook → smoke test (`/health` đúng phiên bản, trang `/` và file tĩnh trả về 200).
- Ruleset `Bao ve main`: bắt buộc PR và 4 check xanh mới được merge, chặn force push và xoá nhánh.
- Đã làm 6 thí nghiệm, số liệu trong `docs/thi-nghiem.md`; có video demo 2 phút 28 giây; tài liệu hướng dẫn GitHub CI/CD đã hoàn thành (PR #16).

## 2. Câu hỏi và trả lời trong buổi họp

| Người hỏi | Câu hỏi | Trả lời (An) |
|---|---|---|
| Ánh | CI và CD khác nhau thế nào? | CI tự động kiểm tra mã (lint, test) mỗi khi có push hoặc PR; CD tự động triển khai lên Render khi mã đã vào nhánh `main`. |
| Ánh | Vì sao job deploy có `needs: test`? | Để deploy chỉ chạy khi test thành công, tránh đưa mã lỗi lên môi trường chạy thật. |
| Ánh | Secret được giấu ra sao? | Deploy Hook lưu trong GitHub Secrets, được mã hoá, không nằm trong mã nguồn; trong log chỉ hiện `***`. |
| Hồng | Vì sao pipeline xanh mà web vẫn hỏng ở thí nghiệm 4? | Test chỉ kiểm tra mã Python, không kiểm tra trang web thực tế sau khi deploy; vì vậy nhóm bổ sung bước smoke test gọi thẳng vào web. |
| Hồng | Rollback của Render khác `git revert` thế nào? | Rollback của Render đưa server về bản deploy cũ ngay lập tức nhưng mã lỗi vẫn còn trên `main`; `git revert` tạo commit đảo ngược, đi qua PR và CI nên lịch sử rõ ràng và sửa tận gốc. |
| Hồng | Vì sao test chạy trên 3 phiên bản Python? | Để đảm bảo ứng dụng tương thích với nhiều phiên bản và phát hiện sớm lỗi do khác biệt phiên bản. |

## 3. Quyết định
- **Kết quả nổi bật đưa vào báo cáo:** pipeline tự động hoàn toàn từ PR đến deploy; ruleset bảo vệ nhánh `main`; smoke test sau deploy; 6 thí nghiệm có số liệu; video demo.
- **Hạn chế đưa vào báo cáo:** gói miễn phí của Render tự "ngủ" khi không có truy cập nên lần mở đầu tiên chậm; chưa có môi trường staging riêng; test chưa bao phủ giao diện; ứng dụng còn quy mô nhỏ.
- **Dàn ý:** giữ nguyên 5 chương như buổi 1.
- **Phân công:** giữ nguyên như buổi 1.
- Hoàn thiện bản nháp các chương trước buổi họp 3 (20:00, 27/10/2026).

## 4. Phân công

| Người | Việc | Hạn | Minh chứng |
|---|---|---|---|
| Ngô Ngọc Ánh | Tìm phần lý thuyết, viết Chương 1 và Chương 2; commit `docs/tai-lieu-tham-khao.md` | 27/10/2026 | PR #18, bản thảo Chương 1–2 gửi qua Zalo |
| Nguyễn Hữu An | Hoàn thiện phần kỹ thuật, viết Chương 3 và Chương 4; chuẩn bị slide thuyết trình | 27/10/2026 | Lịch sử commit, 17 PR, video demo |
| Nguyễn Thị Thanh Hồng | Viết Chương 5, lời mở đầu và tóm tắt; commit `docs/bien-ban-hop.md`; lập phiếu phân công; chuẩn bị slide thuyết trình | 27/10/2026 | PR trên GitHub, phiếu phân công |

## 5. Vấn đề còn mở
- Ánh hoàn tất PR #18 vào sáng 27/10; An review và merge sau khi kiểm tra.
- Cần chốt nội dung slide và các câu hỏi phản biện ở buổi 3.

Thư ký ghi: Nguyễn Thị Thanh Hồng

---

# Buổi 3: Chốt slide, báo cáo và chuẩn bị phản biện

## Thông tin buổi họp
- Thời gian: 27/10/2026, 20:00 – 20:30
- Hình thức: online qua Zalo
- Có mặt: Ngô Ngọc Ánh, Nguyễn Hữu An, Nguyễn Thị Thanh Hồng; vắng: không
- Chủ trì: Nguyễn Hữu An · Thư ký: Nguyễn Thị Thanh Hồng

## Chương trình (30 phút)
1. (10 phút) Chốt nội dung slide thuyết trình.
2. (10 phút) Rà soát và chốt báo cáo.
3. (10 phút) Soạn các câu hỏi giảng viên có thể hỏi để phản biện.

## 1. Tình hình
- Các chương đã có bản nháp và được An ghép vào file Word chung; Hồng đã rà soát tính nhất quán của báo cáo.
- Slide đã có bản nháp do An và Hồng chuẩn bị.

## 2. Câu hỏi phản biện dự kiến

| Câu hỏi | Người trả lời |
|---|---|
| CI/CD là gì, mang lại lợi ích gì so với deploy thủ công? | Ánh |
| Vì sao chọn GitHub Actions mà không chọn Jenkins hay GitLab CI? | Ánh |
| Nếu một thành viên đẩy mã lỗi thẳng lên `main` thì sao? | An |
| Secret được bảo vệ thế nào, có bị lộ trong log không? | An |
| Khi deploy lỗi, nhóm khôi phục hệ thống ra sao? | An |
| Hạn chế của hệ thống và hướng phát triển tiếp theo? | Hồng |

## 3. Quyết định
- **Slide:** chốt theo 5 phần của báo cáo, có chèn video demo. Phân công thuyết trình: Ánh trình bày tổng quan và lý thuyết; An trình bày thiết kế, triển khai, thực nghiệm và demo; Hồng trình bày kết luận và hướng phát triển.
- **Báo cáo:** chốt bản cuối. An xuất file PDF từ Word; Hồng hoàn thiện phiếu phân công.
- Mỗi thành viên tự chuẩn bị câu trả lời cho các câu hỏi phản biện được giao.

## 4. Phân công

| Người | Việc | Hạn | Minh chứng |
|---|---|---|---|
| Ngô Ngọc Ánh | Chuẩn bị phần thuyết trình Chương 1–2; trả lời câu hỏi phản biện được giao | Trước buổi bảo vệ | Slide, phiếu phân công |
| Nguyễn Hữu An | Chuẩn bị phần thuyết trình Chương 3–4 và demo; xuất báo cáo PDF; trả lời câu hỏi phản biện được giao | Trước buổi bảo vệ | Slide, video demo, file báo cáo |
| Nguyễn Thị Thanh Hồng | Rà soát bản cuối của báo cáo; hoàn thiện phiếu phân công; chuẩn bị phần thuyết trình Chương 5 | Trước buổi bảo vệ | Phiếu phân công, slide |

## 5. Vấn đề còn mở
- Không có.

Thư ký ghi: Nguyễn Thị Thanh Hồng
