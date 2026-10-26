# Số liệu thí nghiệm

Số liệu lấy bằng `gh run view --json` và `gh pr view --json`, không ước lượng. Giờ ghi theo UTC. Thời gian từng job là `completedAt - startedAt`, thời gian cả run là `updatedAt - createdAt`.

| Thí nghiệm | Trạng thái |
|---|---|
| 1. Test fail thì PR bị chặn | Đã làm (CI, ruleset, deploy) |
| 2. Có và không có cache pip | Đã làm |
| 3. Deploy thủ công và tự động | Đã làm |
| 4. Rollback | Đã làm, kèm so sánh với Rollback của Render và cải tiến sau thí nghiệm |
| 5. Bảo mật | Đã làm |
| 6. Chi phí và giới hạn | Đã làm |

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

### Phần deploy: test đỏ thì web giữ bản cũ

**Cách làm.** Tạo nhánh `experiment/test-fail-deploy` từ `main`: làm sai `test_health` và đổi `APP_VERSION` thành `9.9.9` (để nếu deploy lỡ chạy thì thấy ngay trên web). Chỉ push nhánh, không mở PR, rồi xoá nhánh sau khi lấy số liệu.

**Kết quả.** Run [40339403295](https://github.com/233404050154-NguyenHuuAn/project_24/actions/runs/40339403295) (sự kiện push):

| Job | Kết quả | Thời gian |
|---|---|---|
| Lint (flake8) | thành công | 14 s |
| Test (Python 3.10) | thất bại | 13 s |
| Test (Python 3.11) | thất bại | 15 s |
| Test (Python 3.12) | thất bại | 18 s |
| Deploy (Render) | bị bỏ qua (`skipped`) | không chạy |

Gọi `/health` của web trước và sau khi push đều trả `{"status":"ok","version":"1.1.0"}`, không phải `9.9.9`.

**Nhận xét.**
- Khi test đỏ, job deploy không chạy và web giữ nguyên bản cũ.
- Ruleset đã không cho commit đỏ vào `main`, nên trường hợp "bản đỏ nằm trên `main`" không xảy ra trong điều kiện thật. Vì vậy thí nghiệm này chỉ kiểm được job deploy trên một nhánh khác `main`. Nó không tách riêng được tác dụng của `needs: test` khỏi điều kiện `if: ... refs/heads/main`, vì cả hai cùng khiến job bị bỏ qua.

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

## Thí nghiệm 2: có và không có cache pip

### Mục đích
Đo xem `cache: pip` của `actions/setup-python` rút ngắn bao nhiêu thời gian chạy pipeline.

### Cách làm
- Chạy workflow bằng `gh workflow run ci-cd.yml --ref main` (sự kiện `workflow_dispatch`, job deploy tự bỏ qua nên không đụng tới Render). Mỗi lần chờ run xong rồi mới chạy lần sau.
- **Không cache:** 5 lần, mỗi lần chạy `gh cache delete --all` ngay trước khi gửi lệnh. **Có cache:** 5 lần liên tiếp ngay sau đó, không xoá cache. Dùng 5 lần thay vì 3 vì thí nghiệm 1 cho thấy cùng một job dao động từ 11 đến 36 giây.
- Thời gian lấy từ `gh run view --json jobs` (tổng job và từng bước). Hit hay miss xác nhận bằng log của `setup-python`.
- Run không cache: 40348982963, 40349099593, 40349246000, 40349379333, 40349498934. Run có cache: 40349661657, 40349778813, 40349877028, 40349990037, 40350108766.

### Kết quả
Xác nhận từ log: ở lượt không cache, Lint, Test 3.10 và Test 3.11 đều ghi `pip cache is not found` rồi lưu cache (miss thật). Test 3.12 là **hit** ngay cả ở lượt "không cache", vì nó chỉ bắt đầu sau khi Lint (cùng Python 3.12, cùng khoá cache) đã lưu cache. Ở lượt có cache, cả 4 job đều `Cache restored successfully` (khoảng 4 đến 5 MB).

Thời gian trung bình ± độ lệch chuẩn của 5 lần (giây):

| Job | Không cache | Có cache | Chênh |
|---|---|---|---|
| Lint (flake8) | 11,0 ± 1,6 | 10,6 ± 1,5 | giảm 0,4 |
| Test (Python 3.10) | 18,4 ± 5,0 | 14,4 ± 2,7 | giảm 4,0 |
| Test (Python 3.11) | 15,2 ± 2,2 | 13,0 ± 2,9 | giảm 2,2 |
| Test (Python 3.12), hit ở cả hai lượt | 15,4 ± 2,3 | 13,4 ± 2,1 | giảm 2,0 |
| Cả run (từ lúc tạo đến lúc xong) | 37,8 ± 3,9 | 33,2 ± 3,3 | giảm 4,6 (khoảng 12%) |

Theo từng bước (trung bình, giây, ba job miss: Lint, 3.10, 3.11):

| Bước | Không cache | Có cache |
|---|---|---|
| `pip install` | 3,6 / 6,0 / 4,8 | 3,6 / 3,8 / 3,4 |
| Lưu cache (Post `setup-python`) | 1,0 / 0,8 / 1,2 | 0,0 / 0,2 / 0,0 |

Tổng thời gian từng lần (giây). Không cache, Test 3.10: 14, 22, 21, 12, 23. Có cache, Test 3.10: 19, 14, 14, 13, 12. Cả run, không cache: 36, 42, 39, 32, 40. Cả run, có cache: 38, 30, 32, 31, 35.

### Nhận xét
- Cache giúp rút ngắn nhưng ít: khoảng 2 đến 4 giây mỗi job và khoảng 4,6 giây cả run. Lý do là gói rất nhỏ (Flask, gunicorn, pytest, flake8 và phụ thuộc, khoảng 4 đến 5 MB), pip cài chỉ mất vài giây.
- Mức chênh nhỏ hơn hoặc tương đương độ dao động giữa các lần chạy (độ lệch chuẩn 1,5 đến 5 giây). Hai nhóm còn chồng lấn nhau, ví dụ Test 3.10 không cache có lần chỉ 12 giây còn có cache có lần 19 giây. Với 5 mẫu mỗi nhóm, kết luận chỉ mang tính xu hướng, không đủ để khẳng định chắc.
- Test 3.12 đã là hit ở cả hai lượt nhưng vẫn lệch 2,0 giây (15,4 so với 13,4). Con số này cho thấy mức nhiễu của runner khoảng 2 giây, nên chênh lệch 2 giây của các job khác cũng nằm trong vùng nhiễu.
- Lưu cache khi miss tốn thêm khoảng 1 giây ở bước Post. Khi dependency lớn (ví dụ gói khoa học dữ liệu) hiệu quả của cache sẽ rõ hơn, nhưng đề tài này không có điều kiện đó.

## Thí nghiệm 3: deploy thủ công và tự động

### Mục đích
So sánh deploy thủ công qua dashboard Render với deploy tự động qua pipeline về số bước, thời gian và khả năng sai sót.

### Cách làm
- **Thủ công** (An thực hiện lúc 22:05 giờ Việt Nam ngày 26/10/2026): mở dashboard Render, chọn service, Manual Deploy, Deploy latest commit, chờ Live, mở web kiểm tra. Thời gian lấy từ log Render mà An gửi, kèm mốc khách quan: việc đánh dấu trong bộ nhớ của app biến mất khi bản mới chạy.
- **Tự động:** các lần deploy của pipeline, lấy từ log smoke test (thăm dò mỗi 15 giây nên sai số tối đa 15 giây).
- Thời gian chạy `flake8` và `pytest` trên máy đo bằng `Measure-Command`, vì đó là hai việc người deploy thủ công phải tự nhớ làm.

### Kết quả

Deploy thủ công, commit `3be0dc6`, giờ UTC:

| Mốc | Giờ | Cách tính |
|---|---|---|
| An bấm Manual Deploy | 15:05:40 | An báo (22:05:40 giờ VN) |
| Render bắt đầu clone | 15:05:48.8 | log, trễ 9 giây sau khi bấm |
| Build xong | 15:06:05.2 | log, 16,4 giây sau khi clone |
| Dịch vụ live | 15:06:28.6 | log, 48,6 giây sau khi bấm |

Số bước người làm: 6. `flake8` mất 0,99 giây, `pytest` kèm coverage mất 1,68 giây.

Deploy tự động:

| Lần | Từ lúc gọi Deploy Hook đến khi `/health` trả bản mới | Nguồn |
|---|---|---|
| GĐ 5, PR #7 | 52 giây (1 giây gọi hook, 51 giây smoke test, 4 lần thử) | run 40336031610 |
| TN4 lần 2, PR #12 (bản lỗi) | tối đa 111 giây (gọi hook khoảng 15:15:43, lần thử 8 lúc 15:17:34.5 mới thấy bản mới, bản mới lên trong khoảng 15 giây trước đó) | run 40347471000 |
| TN4 lần 2, PR #13 (revert) | 65 giây (gọi hook khoảng 15:19:40, lần thử 5 lúc 15:20:45.6) | run 40348131269 |

| | Thủ công | Tự động |
|---|---|---|
| Số bước người làm sau khi code đã nằm trên `main` | 6 | 0 (merge PR là đủ) |
| Thời gian phần Render build và deploy | 39,8 giây (từ clone đến live, 1 mẫu) | 52, 65 và 111 giây (3 mẫu, đã gồm sai số thăm dò tối đa 15 giây của smoke test) |
| Chạy test trước khi deploy | tuỳ người, không bắt buộc | bắt buộc: lint và 3 bản test phải xanh (`needs: test`) |
| Kiểm tra sau khi deploy | tuỳ người mở web xem | tự động: `/health` đúng phiên bản, `/` trả 200, file tĩnh trả 200 |
| Dấu vết | chỉ có trong lịch sử deploy của Render | PR, run, log và thời gian trong GitHub |
| Ai có quyền deploy | ai có quyền vào Render | ai merge được PR và có quyền ghi vào repo |

### Nhận xét
- Phần máy chủ Render làm (clone, build, khởi động) là cùng một việc ở hai cách. Số đo thủ công chỉ có 1 mẫu (39,8 giây) còn số đo tự động có 3 mẫu từ 52 đến 111 giây và có sai số thăm dò đến 15 giây, nên không đủ cơ sở để nói Render chạy nhanh hơn hay chậm hơn ở cách nào. Pipeline còn thêm thời gian cho CI (khoảng 30 giây cho lint và test). Nếu chỉ đếm thời gian thì deploy thủ công có vẻ nhanh hơn, đổi lại pipeline không cần người thao tác trên dashboard.
- Chỗ dễ sai sót của cách thủ công: quên chạy test (không có gì ngăn người deploy), bấm nhầm commit hoặc nhầm service, không mở lại web để kiểm tra. Những lỗi này không thể hiện được trong một lần thử có người cẩn thận, nên bảng trên mô tả khả năng sai sót chứ không đo tần suất sai sót.
- Điểm này ngược với trực giác: deploy tự động không hề nhanh hơn. Giá trị của nó là kiểm soát (bắt buộc qua test, kiểm tra sau deploy, có dấu vết), không phải tốc độ.

## Thí nghiệm 4: rollback

### Mục đích
Đo thời gian khôi phục khi một lỗi lọt qua CI và đã lên web, bằng `git revert` và bằng nút Rollback của Render, rồi so sánh hai cách.

### Cách làm
- **Gây lỗi lọt qua CI:** sửa `templates/index.html` thành `<script src=".../static/app.jss">` (gõ sai tên file). `pytest` vẫn xanh vì chỉ kiểm tra tiêu đề và version, `/health` và `/` vẫn trả 200 nên smoke test lúc đó cũng xanh, nhưng giao diện không tải được JavaScript. Chọn lỗi này thay cho "`/health` trả sai version" vì lỗi đó làm smoke test đỏ nên không lọt được.
- **Xác nhận web hỏng:** `curl /` lấy URL trong `<script>` và `<link>` rồi kiểm tra từng URL. Bản lỗi trả `/static/app.jss` 404.
- Sau đó khôi phục bằng `git revert -m 1` (PR #10), rồi bằng Rollback trên Render (An làm hai lượt: về bản lỗi rồi về bản tốt, trong lúc bộ theo dõi nền kiểm tra web mỗi 4 giây).

### Kết quả

**Khôi phục bằng `git revert`** (giờ UTC, 26/10/2026):

| Mốc | Giờ | Ghi chú |
|---|---|---|
| Merge bản lỗi, PR #9 | 14:27:37 | CI xanh, commit `d1de8eb` |
| Job Deploy kết thúc, xanh | 14:29:17 | run 40339846870, chỉ 6 giây vì version không đổi nên smoke test đạt ngay trên bản cũ |
| Phát hiện web hỏng | 14:30:12 | `/static/app.jss` trả 404. Đây là mốc phát hiện đầu tiên, thời điểm bản lỗi thực sự lên web không biết chính xác |
| Mở PR revert, #10 | 14:30:42 | commit `827ca39` |
| Merge revert | 14:31:29 | merge `3be0dc6`, CI xanh, run 40340383314 |
| Web khoẻ lại | 14:33:01 | file tĩnh trả 200 |

Thời gian khôi phục: **2 phút 19 giây** từ lúc mở PR revert, **1 phút 32 giây** từ lúc merge revert. Web hỏng ít nhất 2 phút 49 giây (từ mốc phát hiện đến lúc khoẻ lại).

**Khôi phục bằng Rollback của Render** (An làm trên dashboard, giờ Việt Nam đổi sang UTC; mốc chuyển trạng thái từ bộ theo dõi nền):

| Lượt | Đích | Bấm | Live (An báo) | Bộ theo dõi thấy đổi trạng thái |
|---|---|---|---|---|
| 1 | bản lỗi `d1de8eb` | 14:50:05 | 14:50:30 | 14:50:28, hỏng sau 23 giây |
| 2 | bản tốt `3be0dc6` | 14:52:20 | 14:52:45 | 14:52:44, khoẻ sau 24 giây |

Theo trang chính thức của Render (truy cập 26/10/2026), Rollback dùng lại bản build cũ nên không build lại, và khi làm trên dashboard thì tự tắt Auto-Deploy (service này vốn đã tắt).

**So sánh `git revert` và Rollback:**

| | `git revert` (PR #10) | Rollback của Render |
|---|---|---|
| Thời gian khôi phục | 2 phút 19 giây từ lúc mở PR, 1 phút 32 giây từ lúc merge | khoảng 25 giây mỗi lượt (An báo 25 giây, bộ theo dõi 23 và 24 giây) |
| Build lại | có | không, dùng lại bản build cũ |
| Qua CI | có | không |
| Dấu vết trong repo | có: PR, commit revert | không có gì |
| Code trên `main` so với web | luôn khớp | có thể lệch |

Trong lượt Rollback, từ 14:50:28 đến 14:52:44 (khoảng 2 phút 16 giây) web chạy bản lỗi `d1de8eb` trong khi `main` đã là bản tốt `3be0dc6`: web và `main` lệch nhau. Sau lượt 2, web chạy `3be0dc6` đúng bằng HEAD của `main` nên khớp lại.

### Nhận xét
- Cả CI lẫn smoke test của thời điểm đó đều xanh dù web hỏng. Bộ kiểm tra thiếu một lớp: không có kiểm tra nào cho file tĩnh. Đây là hạn chế thật của pipeline, không phải của cách làm thí nghiệm.
- Rollback nhanh hơn `git revert` khoảng 4 đến 6 lần vì bỏ qua CI và build. Nhưng nó không để lại dấu vết trong repo và có thể làm web lệch khỏi `main`, nên chỉ nên dùng để cắt lỗi tạm thời, sau đó vẫn phải sửa `main` bằng revert hoặc commit sửa.
- `git revert` chậm hơn nhưng giữ được hai điều: mọi thay đổi đều đi qua CI, và web luôn trùng nội dung với `main`. Với đồ án này, nên dùng Rollback để dừng sự cố nhanh rồi dùng revert để chốt.

### Cải tiến sau thí nghiệm 4: kiểm tra file tĩnh trong smoke test
Sau khi smoke test không bắt được lỗi, thêm bước: sau khi `/health` đạt và `/` trả 200, lấy HTML của `/`, lọc mọi URL cùng máy chủ trong `<script src>` và `<link href>` rồi kiểm tra từng URL trả 200 (PR #11). Link ngoài như Google Fonts cố ý bỏ qua để smoke test không phụ thuộc dịch vụ ngoài. Không tìm thấy URL nào cũng tính là lỗi.

Chạy lại lỗi `app.jss`, lần này kèm đổi `APP_VERSION` thành `1.1.1` (PR #12). Phải đổi version, nếu không smoke test đạt ngay trên bản cũ còn đang chạy rồi mới kiểm tra file tĩnh, lỗi vẫn lọt như lần 1.

| Mốc | Giờ UTC | Ghi chú |
|---|---|---|
| Merge bản lỗi, PR #12 | 15:15:04 | CI xanh, commit `e456030` |
| Smoke test, lần thử 1 đến 7 | 15:15:46 đến 15:17:19 | web vẫn trả `1.1.0` (bản cũ) |
| Lần thử 8 | 15:17:34.5 | web trả `1.1.1`, `/` trả 200, `style.css` 200, `/static/app.jss` **404** |
| Job Deploy báo đỏ | 15:17:35.7 | run 40347471000, `File tĩnh /static/app.jss phải trả 200` |
| Mở PR revert, #13 | 15:18:18 | commit `67bd7ca` |
| Merge revert | 15:19:04 | merge `26015cf`, CI xanh, run 40348131269 |
| Smoke test, lần thử 5 | 15:20:45.6 | web trả `1.1.0`, `app.js` và `style.css` đều 200, Deploy xanh |

- Pipeline báo đỏ tự động sau merge 2 phút 31,7 giây, không cần ai kiểm tra bằng tay (lần 1: xanh và phát hiện thủ công).
- Khôi phục bằng revert: **2 phút 27,6 giây** từ lúc mở PR revert, **1 phút 41,6 giây** từ lúc merge. Web hỏng khoảng 3 phút 11 giây đến 3 phút 26 giây.
- **Giới hạn phải ghi rõ:** smoke test chạy sau khi gọi Deploy Hook nên bản lỗi vẫn lên web. Cải tiến này giúp **phát hiện** nhanh và tự động, chưa **chặn** được bản lỗi. Muốn chặn từ trước khi merge cần thêm một test `pytest` kiểm tra file tĩnh (CI đỏ thì ruleset khoá PR); test này đã được thêm, xem mục tiếp theo. Nếu version không đổi, smoke test cũng không phân biệt được bản cũ và bản mới, muốn phân biệt cần cho `/health` trả thêm mã commit.

### Bổ sung: test pytest chặn lỗi file tĩnh trước khi merge
Để chặn thay vì chỉ phát hiện, thêm `test_index_static_files_exist` vào `tests/test_app.py`: lấy HTML của `/`, lọc mọi URL cùng máy chủ trong `<script src>` và `<link href>`, yêu cầu có `/static/app.js` và `/static/style.css`, rồi gọi từng URL bằng test client và kiểm tra trả 200. Test chạy trong job Test của CI nên nằm trong các check bắt buộc của ruleset.

Kiểm chứng cục bộ: với code đúng, 76 test đạt và coverage vẫn 100%. Khi cố ý đổi `app.js` thành `app.jss` trong `templates/index.html`, chỉ test mới này thất bại (`1 failed, 75 passed`), các test cũ vẫn xanh như trước. Vì CI đỏ khoá nút Merge nhờ ruleset (đã kiểm ở thí nghiệm 1), bản lỗi kiểu này giờ bị chặn trước khi vào `main`. Chuỗi CI đỏ rồi PR bị chặn không chạy lại cho lỗi này, chỉ kiểm cục bộ bước test thất bại.

Smoke test sau deploy vẫn giữ lại làm lớp kiểm tra thứ hai, vì nó kiểm tra bản đang chạy trên Render chứ không phải bản trong CI.

## Thí nghiệm 5: bảo mật

### Mục đích
Kiểm tra các biện pháp bảo vệ secret và quyền hạn trong pipeline, và ghi nhận rủi ro còn lại.

### Cách làm
Chủ yếu đọc, không tạo thêm run in secret và không tự đặt hay đọc giá trị secret. Số liệu lấy từ log run có sẵn, từ `gh api` (chỉ đọc), và từ tài liệu chính thức của GitHub (truy cập ngày 26/10/2026).

### Kết quả
1. **Secret bị che trong log.** Log run [40334919543](https://github.com/233404050154-NguyenHuuAn/project_24/actions/runs/40334919543), job Deploy, bước gọi Deploy Hook: `RENDER_DEPLOY_HOOK: ***`. URL của hook không xuất hiện ở bất kỳ dòng nào. Secret chỉ được dùng ở một chỗ duy nhất, là biến môi trường của bước đó.
2. **Quyền tối thiểu.** Workflow khai báo `permissions: contents: read`. Log "Set up job" của mọi job ghi `GITHUB_TOKEN Permissions: Contents: read, Metadata: read`. Cấu hình của repo qua `gh api`: quyền mặc định của token là `read`, `can_approve_pull_request_reviews` là `false`.
3. **PR từ fork không đọc được secret.** Tài liệu GitHub (docs.github.com, "Using secrets in GitHub Actions") ghi: "With the exception of `GITHUB_TOKEN`, secrets are not passed to the runner when a workflow is triggered from a forked repository." Trang Secrets của repo (ảnh `09a`) cũng ghi câu tương tự. Workflow chỉ dùng `pull_request`, không dùng `pull_request_target` hay `workflow_run` (kiểm tra bằng tìm trong file). Chính sách duyệt workflow từ người đóng góp lần đầu của repo là `first_time_contributors`.
4. **Môi trường `production`:** không có bước duyệt thủ công (0 protection rule) và không giới hạn nhánh.

### Nhận xét
- Các biện pháp chính đều có và kiểm chứng được: secret bị che trong log, token chỉ đọc, fork không nhận secret.
- Tài liệu GitHub nói che secret không áp dụng cho giá trị bị biến đổi và khuyên tránh truyền secret qua đối số dòng lệnh. Bước deploy truyền URL hook cho `curl` qua đối số dòng lệnh (lấy từ biến môi trường). Log không lộ, nhưng đối số này có thể thấy được với tiến trình khác trên runner trong lúc chạy. Cách an toàn hơn là cho `curl` đọc từ stdin. Với runner dùng một lần và chỉ chứa code của repo thì rủi ro thấp.
- **Rủi ro còn lại (chưa xử lý):**
  - Action ghim theo tag chính (`@v7`) chứ không theo mã SHA. Cài đặt `sha_pinning_required` của repo đang là `false`. Nếu tag bị đổi trỏ, pipeline sẽ chạy mã khác.
  - Deploy Hook là secret cấp repo nên người có quyền push (Ánh, Hồng) có thể viết workflow dùng nó. Cách giảm: chuyển thành secret của environment `production` kèm giới hạn nhánh `main`.
  - Môi trường `production` chưa có bước duyệt trước khi deploy.

## Thí nghiệm 6: chi phí và giới hạn

### Mục đích
Ước lượng mức dùng phút Actions so với hạn mức, và đo thời gian khởi động lại (cold start) của Render Free.

### Cách làm
- **Phút Actions:** API billing của GitHub cần quyền `user` mà token hiện tại không có, và nhóm không mở rộng quyền chỉ để đo. Vì vậy tính từ chính các run của repo: cộng thời gian từng job (bỏ qua job bị bỏ qua), làm tròn lên từng phút theo cách GitHub tính. Đây là cách tính của nhóm, không phải số liệu lấy từ hóa đơn. Ảnh trang Usage ở `13_actions-usage.png`.
- **Cold start:** script chạy nền: chờ 18 phút không truy cập (Render ngủ sau 15 phút theo trang chính thức), rồi `curl --max-time 120` vào `/health` lần đầu và 3 lần liên tiếp sau đó, ghi `time_starttransfer` và `time_total`. Lặp 2 chu kỳ. Trong lúc đo, không ai mở web, không có deploy nào.

### Kết quả

**Phút Actions (đến hết ngày 26/10/2026, toàn bộ trong một ngày):**

| Sự kiện | Số run | Số job (không tính job bỏ qua) | Phút, làm tròn lên từng job |
|---|---|---|---|
| push | 23 | 100 | 102 |
| pull_request | 12 | 48 | 48 |
| workflow_dispatch | 10 | 40 | 40 |
| **Tổng** | **45** | **188** | **190** |

Tổng thời gian chạy thực: 2733 giây (khoảng 45,6 phút). Làm tròn lên từng job làm số phút tăng gấp bốn lần vì mỗi job chỉ chạy 10 đến 20 giây.

Hạn mức theo trang chính thức của GitHub (docs.github.com, "GitHub Actions billing", truy cập ngày 26/10/2026): "GitHub Actions usage is free for self-hosted runners and for public repositories that use standard GitHub-hosted runners." Hạn mức mỗi tháng cho tài khoản: GitHub Free 2.000 phút, Pro 3.000, Team 3.000, Enterprise Cloud 50.000.

**Trang Usage của GitHub** (ảnh `13_actions-usage.png`, chụp ngày 26/10/2026, tháng 10/2026): ngày 26/10 hiển thị Gross $1,04, **Billed $0,00**, Discount $1,15. Phần tiền được giảm toàn bộ nên số tiền phải trả là 0, khớp với việc repo công khai dùng runner tiêu chuẩn. Nếu toàn bộ Gross là phút Actions Linux (đơn giá $0,006 mỗi phút theo trang chính thức) thì tương ứng khoảng 173 phút, cùng cỡ với 190 phút nhóm tự tính. Điều này chỉ là suy luận: ảnh chưa mở phần chi tiết theo loại sản phẩm, và Discount lớn hơn Gross một chút nên nhóm không khẳng định số phút chính xác từ trang này.

**Cold start Render Free** (`GET /health`, giờ UTC, 26/10/2026; mỗi chu kỳ chờ 18 phút 23 giây không truy cập trước lần đo đầu):

| Chu kỳ | Yêu cầu | Giờ | Mã HTTP | Thời gian phản hồi đầu tiên (`time_starttransfer`) | Tổng (`time_total`) |
|---|---|---|---|---|---|
| 1 | lần đầu (cold) | 15:42:15 | 200 | 22,55 s | 22,55 s |
| 1 | lần 2 | 15:42:17 | 200 | 0,21 s | 0,21 s |
| 1 | lần 3 | 15:42:20 | 200 | 0,31 s | 0,31 s |
| 1 | lần 4 | 15:42:22 | 200 | 0,32 s | 0,32 s |
| 2 | lần đầu (cold) | 16:00:45 | 200 | 22,65 s | 22,65 s |
| 2 | lần 2 | 16:00:47 | 200 | 0,31 s | 0,31 s |
| 2 | lần 3 | 16:00:49 | 200 | 0,29 s | 0,29 s |
| 2 | lần 4 | 16:00:52 | 200 | 0,18 s | 0,18 s |

Trung bình: lần đầu sau khi ngủ **22,6 giây** (hai mẫu), các lần sau **0,27 giây** (sáu mẫu), chậm hơn khoảng 83 lần. Hai mẫu cold nằm sát nhau (22,55 và 22,65 giây), nhưng chỉ có hai mẫu nên đây là số đo thăm dò, không phải thống kê.

**Giới hạn của Render Free** (trang chính thức render.com/docs/free, truy cập ngày 26/10/2026): web ngủ sau 15 phút không có truy cập; khởi động lại mất khoảng một phút; mỗi workspace có 750 giờ instance miễn phí mỗi tháng; hệ thống file bị xoá mỗi lần deploy, restart hay ngủ.

### Nhận xét
- Repo công khai và dùng runner tiêu chuẩn nên các run này miễn phí. Chi phí ở đây là thời gian chờ chứ không phải tiền: một lần chạy CI đầy đủ mất khoảng 33 đến 38 giây, deploy thêm khoảng 1 đến 2 phút.
- Nếu repo là riêng tư, 190 phút trong một ngày (đã làm tròn) bằng khoảng 9,5% hạn mức 2.000 phút của gói Free. Phần lớn do thí nghiệm lặp lại trong một ngày, mức dùng bình thường thấp hơn nhiều.
- Lần mở đầu tiên sau 15 phút không có ai truy cập mất khoảng 22,6 giây, ngắn hơn mức "khoảng một phút" mà trang Render nêu. Trong thời gian đó người dùng chỉ thấy trang chờ hoặc không nhận được phản hồi. Khi demo, nên mở web trước giờ thuyết trình để tránh chờ ở cold start.
- Hạn chế của Render Free liên hệ trực tiếp với app: dữ liệu lưu trong bộ nhớ nên mất khi deploy, restart hoặc ngủ. Đây là lý do app có nút Xuất/Nhập JSON để sao lưu.

## Hạn chế và đề xuất cải tiến (chưa làm)
- Cho `/health` trả thêm mã commit (Render đặt biến `RENDER_GIT_COMMIT`) để smoke test phân biệt được bản cũ và bản mới khi version không đổi.
- Ghim `ubuntu-24.04` thay cho `ubuntu-latest` (GitHub thông báo `ubuntu-latest` đang chuyển sang Ubuntu 26) và ghim action theo mã SHA.
- Chuyển Deploy Hook thành secret của environment `production`, giới hạn nhánh `main`.
- Cho `curl` đọc URL của hook từ stdin thay vì đối số dòng lệnh.
