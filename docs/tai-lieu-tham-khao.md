# Tài liệu tham khảo (Nhóm 3, Đề tài 24)

Danh mục nguồn dùng cho phần lý thuyết và phần thực hành của báo cáo. Cột "Trạng thái" cho biết nguồn đã được mở và đối chiếu nội dung hay chưa. Ngày truy cập là ngày 26/10/2026 nếu không ghi khác. Thông tin dễ thay đổi (phiên bản action, hạn mức, giới hạn gói Free) cần kiểm tra lại trước khi nộp.

## A. Tài liệu chính thức đã mở và đối chiếu

| Mã | Nguồn | Địa chỉ | Dùng cho | Trạng thái |
|---|---|---|---|---|
| [1] | GitHub Docs, "Understanding GitHub Actions" | https://docs.github.com/en/actions/get-started/understand-github-actions | Khái niệm workflow, event, job, runner. Trang định nghĩa: "A workflow is a configurable automated process that will run one or more jobs." | Đã đối chiếu |
| [2] | GitHub Docs, "Workflow syntax for GitHub Actions" | https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax | Cú pháp YAML: `name`, `on`, `permissions`, `env`, `defaults`, `concurrency`, `jobs`. Các khoá `needs`, `strategy.matrix`, `fail-fast` nằm ở phần sau của trang | Đã đối chiếu phần đầu; cần xem tiếp phần `jobs` |
| [3] | GitHub Docs, "Dependency caching reference" | https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows | Cách cache khớp và khôi phục theo khoá, `cache-mode`, giới hạn lưu trữ | Đã đối chiếu; mở lại bằng trình duyệt để ghi địa chỉ cuối cùng nếu trang chuyển hướng |
| [4] | GitHub Docs, "About rulesets" | https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets | Ruleset: "A ruleset is a named list of rules that applies to a repository"; trạng thái Active và Disabled; nhiều ruleset kết hợp với nhau | Đã đối chiếu |
| [5] | GitHub Docs, "Using secrets in GitHub Actions" | https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions | Bảo mật secret. Trích: "With the exception of `GITHUB_TOKEN`, secrets are not passed to the runner when a workflow is triggered from a forked repository." Khuyên tránh truyền secret qua đối số dòng lệnh | Đã đối chiếu |
| [6] | GitHub Docs, GitHub Actions billing | https://docs.github.com/en/billing/concepts/product-billing/github-actions | Trích: "GitHub Actions usage is free for self-hosted runners and for public repositories that use standard GitHub-hosted runners." Hạn mức mỗi tháng: Free 2.000 phút, Pro 3.000, Team 3.000, Enterprise Cloud 50.000 | Đã đối chiếu ngày 26/10/2026 |
| [7] | Render Docs, Deploy Hooks | https://render.com/docs/deploy-hooks | Deploy Hook nằm ở tab Settings; gửi GET hoặc POST để deploy; URL là bí mật, lộ thì Regenerate Hook | Đã đối chiếu; ghi lại tiêu đề trang đúng như hiển thị |
| [8] | Render Docs, gói Free | https://render.com/docs/free | Ngừng chạy sau 15 phút không có truy cập; khởi động lại khoảng một phút; 750 giờ instance miễn phí mỗi tháng cho mỗi workspace; hệ thống file bị xoá khi deploy, restart hoặc ngủ | Đã đối chiếu; ghi lại tiêu đề trang |
| [9] | Render Docs, Deploys | https://render.com/docs/deploys | Tắt Auto-Deploy ở Settings (các lựa chọn: On Commit, After CI Checks Pass, Off); Build Command, Start Command | Đã đối chiếu; ghi lại tiêu đề trang |
| [10] | Render Docs, Rollbacks | https://render.com/docs/rollbacks | Rollback ở trang Deploys; dùng lại bản build cũ nên không build lại; rollback trên dashboard tự tắt Auto-Deploy | Đã đối chiếu; ghi lại tiêu đề trang |
| [11] | Render Docs, phiên bản Python | https://render.com/docs/python-version | Thứ tự chọn phiên bản: biến `PYTHON_VERSION`, rồi file `.python-version`, rồi mặc định | Đã đối chiếu; ghi lại tiêu đề trang |

Các nguồn [16] đến [23] bổ sung ngày 27/10/2026 cho phần lý thuyết (mục D cũ). Mã đánh tiếp sau mục B để không đổi số các trích dẫn đã có; khi viết báo cáo, đánh số lại theo thứ tự xuất hiện.

| Mã | Nguồn | Địa chỉ | Dùng cho | Trạng thái |
|---|---|---|---|---|
| [16] | P. Mell và T. Grance, "The NIST Definition of Cloud Computing," NIST Special Publication 800-145, tháng 9/2011, DOI 10.6028/NIST.SP.800-145 | https://csrc.nist.gov/pubs/sp/800/145/final (bản PDF đã đọc: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-145.pdf) | Định nghĩa điện toán đám mây, 5 đặc điểm, 3 mô hình dịch vụ, 4 mô hình triển khai. Trích: "Cloud computing is a model for enabling ubiquitous, convenient, on-demand network access to a shared pool of configurable computing resources ... that can be rapidly provisioned and released with minimal management effort or service provider interaction." Năm đặc điểm: on-demand self-service, broad network access, resource pooling, rapid elasticity, measured service. PaaS: người dùng "deploy onto the cloud infrastructure consumer-created or acquired applications", không quản lý hạ tầng gồm network, server, hệ điều hành, storage, nhưng "has control over the deployed applications and possibly configuration settings for the application-hosting environment" | Đã đối chiếu 2 lần ngày 27/10/2026: trích nguyên văn từ file PDF bằng `pdftotext`; trang csrc.nist.gov tải 2 lần cho kết quả giống nhau (Published: September 2011; tác giả Peter Mell, Tim Grance; DOI khớp). Ánh đọc lại |
| [17] | AWS Whitepaper, "Practicing Continuous Integration and Continuous Delivery on AWS," mục "What is continuous integration and continuous delivery/deployment?" | https://docs.aws.amazon.com/whitepapers/latest/practicing-continuous-integration-continuous-delivery/what-is-continuous-integration-and-continuous-deliverydeployment.html | Định nghĩa CI: "a software development practice where developers regularly merge their code changes into a central repository, after which automated builds and tests are run." CD (delivery): mã "automatically built, tested, and prepared for production release." Continuous deployment: bản sửa đổi được đưa lên production "automatically without explicit approval from a developer." Có mục riêng "Continuous delivery is not continuous deployment". Trang ghi đầu bài: whitepaper "for historical reference only" (có thể lỗi thời), nên dùng cho định nghĩa khái niệm, không dùng cho cấu hình cụ thể của AWS | Đã đối chiếu 2 lần ngày 27/10/2026 trên mã HTML gốc (2 lần tải giống hệt nhau); ba câu trích khớp nguyên văn, dòng "historical reference only" có thật. Ánh đọc lại |
| [18] | AWS, "What is DevOps? - DevOps Models Explained" | https://aws.amazon.com/devops/what-is-devops/ | Định nghĩa DevOps: "DevOps is the combination of cultural philosophies, practices, and tools that increases an organization's ability to deliver applications and services at high velocity: evolving and improving products at a faster pace than organizations using traditional software development and infrastructure management processes." Cùng trang có đoạn "Continuous Integration" và "Continuous Delivery" với câu định nghĩa giống [17] | Đã đối chiếu 2 lần ngày 27/10/2026 trên mã HTML gốc (giống hệt nhau); câu định nghĩa khớp nguyên văn. Ánh đọc lại |
| [19] | GitLab Docs, "Get started with GitLab CI/CD" | https://docs.gitlab.com/ci/ | GitLab CI: pipeline cấu hình trong file YAML `.gitlab-ci.yml` ở thư mục gốc (mặc định, phân biệt hoa thường); stage quyết định thứ tự chạy, job chứa tác vụ; runner là tác nhân chạy job, GitLab.com cung cấp runner Linux, Windows, macOS và cho đăng ký runner riêng. Câu nguyên văn: "To use GitLab CI/CD, add a .gitlab-ci.yml file to the root of your project." và "Runners are the agents that run your jobs." Trang không định nghĩa riêng CI, CD (dùng [17], [18] cho phần đó) | Đã đối chiếu 2 lần ngày 27/10/2026 trên mã HTML gốc (giống hệt nhau); các ý trên khớp, gồm cả câu "Filenames are case-sensitive." và "If you use GitLab.com, runners on Linux, Windows, and macOS are already available for use." Ánh đọc lại |
| [20] | GitLab Docs, "Compute minutes" | https://docs.gitlab.com/ci/pipelines/compute_minutes/ | Hạn mức chạy CI trên GitLab.com: "Free tier namespaces receive 400 compute minutes per month." Dùng so sánh chi phí với [6] (GitHub Free 2.000 phút mỗi tháng; repo công khai dùng runner chuẩn thì miễn phí). Cùng trang: "The usage of instance runners by projects running CI/CD jobs is measured in compute minutes." Hạn mức đổi theo thời gian, ghi ngày truy cập 27/10/2026 | Đã đối chiếu 2 lần ngày 27/10/2026 trên mã HTML gốc (giống hệt nhau); hai câu trên khớp nguyên văn. Trang còn có chiết khấu riêng cho chương trình GitLab for Open Source (hệ số 0,5), không áp dụng cho nhóm. [6] cũng đã tải lại 2 lần: bảng hạn mức GitHub Free 2.000 phút, Pro 3.000, Team 3.000, Enterprise Cloud 50.000 khớp. Ánh mở lại sát ngày nộp |
| [21] | Jenkins, "Pipeline" (Jenkins User Documentation) | https://www.jenkins.io/doc/book/pipeline/ | Jenkins Pipeline là "a suite of plugins which supports implementing and integrating continuous delivery pipelines into Jenkins"; định nghĩa bằng `Jenkinsfile` đưa vào kho mã (pipeline as code); hai cú pháp Declarative (khối `pipeline`) và Scripted (khối `node`) | Đã đối chiếu 2 lần ngày 27/10/2026 trên mã HTML gốc (giống hệt nhau); khớp nguyên văn câu "Jenkins Pipeline (or simply "Pipeline" with a capital "P") is a suite of plugins which supports implementing and integrating continuous delivery pipelines into Jenkins.", câu "A Jenkinsfile can be written using two types of syntax — Declarative and Scripted." và các ví dụ `pipeline { ... }`, `node { ... }`. Ánh đọc lại |
| [22] | Jenkins, "Installing Jenkins" (Jenkins User Documentation) | https://www.jenkins.io/doc/book/installing/ | Câu nguyên văn: "Jenkins is typically run as a standalone application in its own process." và "The Jenkins WAR file bundles Winstone, a Jetty servlet container wrapper, and can be started on any operating system or platform with a version of Java supported by Jenkins." Nhận xét của nhóm (suy ra, trang không nói trực tiếp): Jenkins là phần mềm chạy trên máy do người dùng chuẩn bị, khác với GitHub Actions và GitLab.com có runner sẵn do nhà cung cấp quản lý ([19], [1]). Trang không nêu cấu hình phần cứng tối thiểu, đừng ghi con số nào từ nguồn này | Đã đối chiếu 2 lần ngày 27/10/2026 trên mã HTML gốc (giống hệt nhau); hai câu trên khớp nguyên văn. Ánh đọc lại |
| [23] | Jenkins, trang chủ | https://www.jenkins.io/ | "The leading open source automation server, Jenkins provides hundreds of plugins to support building, deploying and automating any project." và "With 2300+ community contributed plugins, Jenkins integrates with practically every tool in the continuous integration and continuous delivery toolchain." Dùng cho ý Jenkins là phần mềm mã nguồn mở và hệ plugin. Con số 2300+ là số của trang chủ tại ngày truy cập, ghi kèm ngày 27/10/2026 | Đã đối chiếu 2 lần ngày 27/10/2026 trên mã HTML gốc (giống hệt nhau); hai câu khớp nguyên văn. Trang plugins.jenkins.io tải về không có chữ nào trích được (nội dung nạp bằng JavaScript), nên không dùng làm nguồn. Ánh đọc lại |

## B. Nguồn số liệu của nhóm

| Mã | Nguồn | Dùng cho |
|---|---|---|
| [12] | `docs/thi-nghiem.md` trong repo của nhóm | Số liệu 6 thí nghiệm (thời gian job, cache, deploy, rollback, bảo mật, chi phí, cold start), kèm link từng run |
| [13] | `docs/HUONG_DAN_GITHUB_CICD.md` trong repo của nhóm | Quy trình, cấu hình, lỗi thường gặp |
| [14] | Repo https://github.com/233404050154-NguyenHuuAn/project_24 | Lịch sử commit, PR, run Actions |
| [15] | Phiên bản action: trang Releases của `actions/checkout`, `actions/setup-python`, `actions/upload-artifact` (github.com/actions/...) | Phiên bản đã dùng (tra ngày 26/10/2026): checkout v7.0.1, setup-python v7.1.0, upload-artifact v7.0.2 |

## C. Slide môn học

Thư mục `Slide tài liệu tham khảo/`: `Buổi 1-DTDM.pdf` đến `Buổi 7-DTDM.pdf` và `10_ThucHanh_ChiTiet.pdf`.

Bảng dưới do Claude lập ngày 27/10/2026, đã kiểm tra 2 lần: lần 1 đọc chữ trích từ cả file PDF, lần 2 đọc lại từng trang bằng `pdftotext -f N -l N`. Mỗi trang PDF chứa 1 đến 2 slide (bản in nhiều slide mỗi trang), nên cột "Slide" ghi số thứ tự in ở chân slide (dạng x / tổng). Chữ trích từ PDF mất dấu tiếng Việt nên không trích nguyên văn được; Ánh mở từng trang để xác nhận nội dung và chép tiêu đề đúng dấu khi dẫn vào báo cáo.

| Buổi (file) | Trang PDF | Slide | Nội dung | Dùng cho phần nào của báo cáo |
|---|---|---|---|---|
| Buổi 1 | 4 | 8 và 9 / 45 | Điện toán đám mây là gì; định nghĩa gắn với 5 đặc điểm bắt buộc theo NIST | Ch.2 mục điện toán đám mây (đối chiếu với [16]) |
| Buổi 1 | 7, 8, 9 | 3 trang liên tiếp, mỗi trang một đặc điểm | On-demand self-service, Resource pooling, Measured service | Ch.2 (đối chiếu với [16]) |
| Buổi 1 | 15 | 30 và 31 / 45 | So sánh 5 mô hình tính toán (tập trung, phân tán, Grid, Cluster, Cloud) | Ch.2 phần mở đầu về đám mây |
| Buổi 2 | 3, 4, 5 | – | Public Cloud, Hybrid Cloud, bảng so sánh 4 mô hình triển khai (Public, Private, Hybrid, Community) | Ch.2 mô hình triển khai (đối chiếu với [16]) |
| Buổi 3 | 3 | – | IaaS (ví dụ AWS EC2, EBS, VPC) | Ch.2 so sánh IaaS với PaaS |
| Buổi 4 | 3 | 5 và 6 / 17 | SaaS; BPaaS | Ch.2 mô hình dịch vụ |
| Buổi 4 | 4 | 7 / 17 | Bảng "Ai quản lý gì" theo tầng công nghệ cho On-Prem, IaaS, PaaS, SaaS | Ch.2 mục PaaS; Ch.4 phạm vi trách nhiệm |
| Buổi 4 | 5 | 10 và 11 / 17 | Luồng deploy PaaS: GitHub, Render build (`pip install`, `gunicorn app:app`), web live; lộ trình thực hành 6 bước | Ch.2 mục Render; Ch.3 kiến trúc |
| Buổi 4 | 6 | 12 và 13 / 17 | Cùng một web app trên IaaS (EC2) và PaaS (Render); lỗi hay gặp khi deploy PaaS, cold start gói Free sau 15 phút | Ch.2 so sánh IaaS và PaaS; Ch.4 cold start (đối chiếu với [8] và TN6) |
| Buổi 4 | 8 | 16 / 17 | Ghi nhớ: PaaS là nhà cung cấp lo hệ điều hành và runtime, người dùng lo code và dữ liệu | Ch.2 mục PaaS |
| Buổi 7 | 2 | 4 và 5 / 19 | Mô hình trách nhiệm chia sẻ; trách nhiệm bảo mật theo On-Prem, IaaS, PaaS, SaaS | Ch.4 bảo mật (đối chiếu với TN5) |
| 10_ThucHanh_ChiTiet | 2 | – | Bài thực hành CI/CD với GitHub Actions: pipeline Source, Build/Test, Deploy; lưu credential bằng GitHub Secrets | Ch.2 mục CI/CD; Ch.3 so sánh với bài thực hành của môn học (đích deploy là S3, của nhóm là Render) |
| 10_ThucHanh_ChiTiet | 6 | – | Giải thích dòng `on.push.branches [main]` (pipeline tự chạy khi push lên `main`) và `runs-on: ubuntu-latest` | Ch.3 giải thích khối `on` và `runs-on` trong YAML |

Buổi 5 (ảo hoá, container) và Buổi 6 (S3) không dùng trực tiếp cho đề tài này. Các slide không có nội dung về DevOps, GitLab CI hay Jenkins (đã tìm các từ khoá này trong cả 8 file; chỉ có một dòng nhắc "DevOps" ở Buổi 1 về nghề nghiệp và một dòng ở Buổi 4 về chi phí), nên ba ý đó dựa vào mục A, nguồn [17] đến [23].

## D. Ý lý thuyết và nguồn tương ứng

Claude đã tìm các nguồn dưới đây và đối chiếu câu trích hai lần ngày 27/10/2026 (tải mã HTML gốc hai lần, so sánh nội dung chữ giữa hai lần, rồi tìm từng câu trích). Ánh vẫn phải đọc lại từng trang, sửa cột "Trạng thái" ở mục A theo những gì chính Ánh đã kiểm tra, rồi mới coi là xong.

| Ý cần trích dẫn | Nguồn |
|---|---|
| Định nghĩa DevOps | [18] |
| Định nghĩa CI, CD (delivery), continuous deployment và điểm khác nhau giữa hai loại CD | [17]; [18] cho CI và CD ở mức tóm tắt |
| Điện toán đám mây, 5 đặc điểm, mô hình triển khai | [16], đối chiếu slide Buổi 1, Buổi 2 |
| PaaS và so sánh với IaaS, SaaS | [16]; slide Buổi 3, Buổi 4 |
| GitHub Actions | [1], [2] |
| GitLab CI | [19] |
| Jenkins | [21], [22], [23] (mã nguồn mở, hơn 2.300 plugin do cộng đồng đóng góp theo trang chủ) |
| Chi phí, hạn mức chạy CI | GitHub [6]; GitLab [20]; Jenkins: [23] chỉ nói là "open source automation server", không nói giá hay giấy phép, nên báo cáo viết "mã nguồn mở" và "tự chuẩn bị máy chạy" ([22]), không viết "miễn phí" |

Giới hạn còn lại (đã tìm, không có nguồn chính thức nên không viết vào báo cáo):

- Jenkins: không có nguồn về giá hay giấy phép cụ thể, không có nguồn về cấu hình phần cứng tối thiểu. Trang plugins.jenkins.io nạp nội dung bằng JavaScript nên không kiểm chứng được số plugin ở đó; chỉ dùng con số 2300+ từ trang chủ [23] kèm ngày truy cập.
- GitLab: chỉ có hạn mức 400 phút/tháng của gói Free trên GitLab.com [20]. Chưa kiểm tra giá gói trả phí và hạn mức riêng cho dự án công khai; báo cáo không nêu hai ý này.
- Bảng so sánh ba công cụ trong báo cáo chỉ so những tiêu chí có nguồn ở trên: nơi lưu cấu hình (`.github/workflows/*.yml` [2], `.gitlab-ci.yml` [19], `Jenkinsfile` [21]), nơi chạy job (runner do GitHub hoặc GitLab cung cấp [1], [19]; Jenkins chạy trên máy được chuẩn bị [22]), hạn mức miễn phí ([6], [20]), mã nguồn mở và plugin ([23]).

## E. Cách ghi trích dẫn trong báo cáo (kiểu IEEE)

Ví dụ cho nguồn [1]:

> [1] GitHub, "Understanding GitHub Actions," GitHub Docs. [Online]. Available: https://docs.github.com/en/actions/get-started/understand-github-actions. [Accessed: Oct. 26, 2026].

Trong văn bản ghi số trong ngoặc vuông, ví dụ "workflow là một quy trình tự động có thể cấu hình, chạy một hoặc nhiều job [1]".
