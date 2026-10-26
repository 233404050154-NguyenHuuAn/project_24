# Số liệu thí nghiệm

Số liệu lấy bằng `gh run view --json` và `gh pr view --json`, không ước lượng. Giờ ghi theo UTC. Thời gian từng job là `completedAt - startedAt`, thời gian cả run là `updatedAt - createdAt`.

| Thí nghiệm | Trạng thái |
|---|---|
| 1. Test fail thì PR bị chặn | Đã làm phần CI và ruleset. Phần deploy làm ở GĐ 6 (job deploy đã có) |
| 2. Có và không có cache pip | Chưa làm |
| 3. Deploy thủ công và tự động | Chưa làm |
| 4. Rollback | Chưa làm |
| 5. Bảo mật | Chưa làm |
| 6. Chi phí và giới hạn | Chưa làm |

## Thí nghiệm 1: test fail thì CI đỏ và PR bị chặn

### Mục đích
Kiểm tra rằng một thay đổi làm hỏng test không vào được `main`: CI báo đỏ và ruleset `Bao ve main` khoá việc merge.

### Cách làm
1. Từ `main`, tạo nhánh `experiment/test-fail`, sửa một dòng trong `tests/test_app.py`: `test_health` kỳ vọng `version` là `"0.0.0"` trong khi `APP_VERSION` là `"1.0.0"`.
2. Push và mở PR #4 vào `main`. Quan sát CI. Khi PR còn đỏ, chạy `gh pr merge --merge` (không dùng `--admin`).
3. Dùng `git revert` để hoàn tác commit sai, push, chờ CI xanh.
4. Đóng PR bằng `gh pr close --delete-branch`, không merge.

### Kết quả

PR: https://github.com/233404050154-NguyenHuuAn/project_24/pull/4 (trạng thái cuối: CLOSED, `mergedAt` rỗng, `main` không có commit lỗi).

**Lần đẩy commit sai (CI đỏ):**

| Run | Sự kiện | Lint | Test 3.10 | Test 3.11 | Test 3.12 | Cả run | Kết luận |
|---|---|---|---|---|---|---|---|
| [40328291211](https://github.com/233404050154-NguyenHuuAn/project_24/actions/runs/40328291211) | push | thành công, 9 s | thất bại, 16 s | thất bại, 11 s | thất bại, 9 s | 30 s | failure |
| [40328301290](https://github.com/233404050154-NguyenHuuAn/project_24/actions/runs/40328301290) | pull_request | thành công, 9 s | thất bại, 11 s | thất bại, 36 s | thất bại, 13 s | 53 s | failure |

Dòng lỗi pytest (ở cả 3 phiên bản Python):

```
>       assert client.get("/health").get_json() == {"status": "ok", "version": "0.0.0"}
E       AssertionError: assert {'status': 'o...ion': '1.0.0'} == {'status': 'o...ion': '0.0.0'}
FAILED tests/test_app.py::test_health
1 failed, 74 passed
```

Trạng thái PR khi CI đỏ: `mergeStateStatus = BLOCKED`. Lệnh `gh pr merge --merge` bị từ chối:

```
X Pull request 233404050154-NguyenHuuAn/project_24#4 is not mergeable: the base branch policy prohibits the merge.
```

**Sau khi hoàn tác (CI xanh):**

| Run | Sự kiện | Lint | Test 3.10 | Test 3.11 | Test 3.12 | Cả run | Kết luận |
|---|---|---|---|---|---|---|---|
| [40329197648](https://github.com/233404050154-NguyenHuuAn/project_24/actions/runs/40329197648) | push | 12 s | 16 s | 12 s | 11 s | 34 s | success |
| [40329204846](https://github.com/233404050154-NguyenHuuAn/project_24/actions/runs/40329204846) | pull_request | 12 s | 17 s | 13 s | 13 s | 35 s | success |

Trạng thái PR sau khi xanh: `mergeStateStatus = CLEAN`, tức là hết bị chặn. PR vẫn được đóng không merge vì chỉ phục vụ thí nghiệm.

Ảnh minh chứng: `docs/minh-chung/06_ci-do.png` (run đỏ, Lint xanh, Test đỏ), `docs/minh-chung/07_pr-bi-chan.png` (PR bị chặn).

### Nhận xét
- Lint xanh còn Test đỏ vì flake8 chỉ kiểm tra style, không bắt được lỗi logic của test. Hai job kiểm hai loại lỗi khác nhau nên cần cả hai.
- Nhờ `fail-fast: false`, cả 3 phiên bản Python đều chạy xong và đều báo lỗi trong một lần, nên thấy ngay lỗi không phụ thuộc phiên bản Python.
- Ruleset chặn merge ở cả hai đường: nút Merge trên web bị khoá và lệnh `gh pr merge --merge` bị từ chối. Không dùng `--admin` và ruleset không có bypass nên không có cách vòng qua.
- Mỗi lần đẩy commit lên nhánh đang có PR sinh 2 run (một run `push`, một run `pull_request`), đúng theo cấu hình `on:` đang dùng. Kết quả hai run giống nhau, nhưng tốn gấp đôi thời gian chạy.
- Thời gian job không ổn định hoàn toàn: cùng một job Test 3.11 chạy 11 s ở run push và 36 s ở run pull_request với cùng một commit. Số liệu dùng để so sánh sau này cần lấy nhiều lần rồi tính trung bình (thí nghiệm 2).
- Về phút Actions: trang chính thức của GitHub (docs.github.com, "GitHub Actions billing", truy cập ngày 26/10/2026) ghi: "GitHub Actions usage is free for self-hosted runners and for public repositories that use standard GitHub-hosted runners." Repo `project_24` là public và chạy trên `ubuntu-latest` (runner tiêu chuẩn), nên các run này không tốn tiền. Chi phí ở đây là thời gian chờ: một lần đẩy commit đỏ mất khoảng 30 đến 53 giây mới biết kết quả. Con số này chỉ cho thấy lợi ích của việc dừng sớm, không phải khoản chi phí bằng tiền.

### Phần deploy
Chưa làm. Job deploy đã có (xem mục "Ghi nhận triển khai" bên dưới). Sẽ bổ sung ở GĐ 6: khi test đỏ thì job deploy không chạy, và web trên Render vẫn giữ bản cũ.

## Ghi nhận triển khai (GĐ 5)

Số liệu thô cho thí nghiệm 3 và phần deploy của thí nghiệm 1. Web: https://project-24-x8jl.onrender.com (Render Free, Auto-Deploy tắt, chỉ deploy qua Deploy Hook của pipeline). Cấu hình ghi ở `docs/minh-chung/08a`, `08b`. Secret `RENDER_DEPLOY_HOOK` và variable `RENDER_APP_URL` ghi ở `09a`, `09b`.

Job `deploy` chỉ chạy khi push vào `main` và sau khi lint và 3 bản test đều xanh. Nó gọi Deploy Hook, rồi smoke test: gọi `/health` tối đa 40 lần cách nhau 15 giây cho đến khi `version` khớp `APP_VERSION` trong code, sau đó kiểm tra trang `/` trả HTTP 200.

| Lần | PR | Run | Version trong code | Lint | Test 3.10 / 3.11 / 3.12 | Deploy | Cả run |
|---|---|---|---|---|---|---|---|
| 1 | [#6](https://github.com/233404050154-NguyenHuuAn/project_24/pull/6) thêm job deploy | [40334919543](https://github.com/233404050154-NguyenHuuAn/project_24/actions/runs/40334919543) | 1.0.0 (không đổi) | 15 s | 15 s / 10 s / 16 s | 7 s | 49 s |
| 2 | [#7](https://github.com/233404050154-NguyenHuuAn/project_24/pull/7) nâng lên 1.1.0 | [40336031610](https://github.com/233404050154-NguyenHuuAn/project_24/actions/runs/40336031610) | 1.1.0 | 11 s | 13 s / 13 s / 17 s | 56 s | 93 s |

Chi tiết job deploy:

| Lần | Gọi Deploy Hook | Smoke test | Số lần thử `/health` | Kết quả |
|---|---|---|---|---|
| 1 | 0 s | 1 s | 1 | Đạt ngay lần 1: `mong đợi 1.0.0, nhận được 1.0.0`, `/` trả 200 |
| 2 | 1 s | 51 s | 4 | Lần 1 đến 3 nhận `1.0.0` (bản cũ), lần 4 nhận `1.1.0`, `/` trả 200 |

Log của cả hai run chỉ hiện `RENDER_DEPLOY_HOOK: ***`, không lộ URL của hook. Lần 2: web trả `{"status":"ok","version":"1.1.0"}` và `/` trả 200 khi kiểm tra lại bằng `curl`.

Ảnh: `10_pipeline-deploy-xanh.png` (run Lint, Test, Deploy xanh), `11_web-render-v1.png` (web `v1.0.0`), `12_web-render-v2.png` (web `v1.1.0`).

### Nhận xét
- Lần 1 smoke test xanh sau 1 giây vì version trong code chưa đổi: bản `1.0.0` đang chạy cũ khớp ngay `APP_VERSION`, nên smoke test không chờ deploy mới. Kết quả xanh này chưa chứng minh Render đã build lại. Đây là hạn chế của cách kiểm tra bằng version: chỉ có giá trị khi commit đổi `APP_VERSION`. Cách chắc hơn là cho `/health` trả thêm mã commit (Render đặt biến `RENDER_GIT_COMMIT`) rồi so với commit vừa merge, chưa làm vì ngoài phạm vi cấp độ 2.
- Lần 2 cho thấy smoke test hoạt động đúng: 3 lần đầu web vẫn chạy bản cũ trong lúc Render build, lần 4 mới đạt. Khoảng 51 giây từ lúc gọi hook đến khi web chạy bản mới, cộng với 1 giây gọi hook.
- Deploy chỉ xảy ra khi có người merge PR đã xanh. Auto-Deploy của Render tắt nên mọi lần deploy đều đi qua pipeline và qua smoke test.

## Thí nghiệm 2 đến 6
Chưa làm.
