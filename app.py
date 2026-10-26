"""Ứng dụng quản lý công việc hằng ngày (Nhóm 3 - Đề tài 24).

Dữ liệu lưu trong bộ nhớ: mất khi server khởi động lại, chỉ đúng với gunicorn 1 worker.
Dùng nút Xuất/Nhập JSON để sao lưu.
"""
from datetime import datetime
from zoneinfo import ZoneInfo

from flask import Flask, abort, jsonify, render_template, request
from werkzeug.exceptions import HTTPException

from validators import CATEGORIES, PRIORITIES, schedule_error, validate_task

APP_VERSION = "1.1.1"
VN_TZ = ZoneInfo("Asia/Ho_Chi_Minh")
VIEWS = ("today", "upcoming", "overdue")

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024  # 1 MB, quá thì trả 413

tasks = {}
counter = {"next_id": 1}


def now():
    """Giờ Việt Nam hiện tại. Tách riêng để test giả lập."""
    return datetime.now(VN_TZ)


def today():
    return now().date().isoformat()


def reset_store():
    tasks.clear()
    counter["next_id"] = 1


@app.errorhandler(HTTPException)
def handle_http_error(e):
    return jsonify(error=e.description), e.code


def get_body():
    return request.get_json(silent=True)


def valid_or_400(data, partial=False):
    fields, error = validate_task(data, partial)
    if error:
        abort(400, error)
    return fields


def get_task_or_404(task_id):
    task = tasks.get(task_id)
    if task is None:
        abort(404, "Không tìm thấy công việc.")
    return task


def is_overdue(task):
    return not task["done"] and task["due_date"] is not None and task["due_date"] < today()


def sort_key(task):
    due = task["due_date"]
    start = task["start_time"]
    return (task["done"], not is_overdue(task), due is None, due or "", start is None,
            start or "", PRIORITIES.index(task["priority"]), task["id"])


def in_view(task, view):
    due = task["due_date"]
    if view == "today":
        return due is not None and (due == today() or is_overdue(task))
    if view == "upcoming":
        return due is not None and due > today()
    return is_overdue(task)


def parse_filters():
    """Đọc và kiểm tra query string, giá trị sai thì trả 400."""
    args = request.args
    done = args.get("done")
    if done not in (None, "true", "false"):
        abort(400, "Tham số done phải là true hoặc false.")
    category = args.get("category")
    if category is not None and category not in CATEGORIES:
        abort(400, "Tham số category không hợp lệ.")
    priority = args.get("priority")
    if priority is not None and priority not in PRIORITIES:
        abort(400, "Tham số priority không hợp lệ.")
    view = args.get("view")
    if view is not None and view not in VIEWS:
        abort(400, "Tham số view phải là today, upcoming hoặc overdue.")
    return done, category, priority, view, args.get("q", "").strip().lower()


@app.get("/")
def index():
    return render_template("index.html", version=APP_VERSION)


@app.get("/health")
def health():
    return jsonify(status="ok", version=APP_VERSION)


@app.get("/api/tasks")
def list_tasks():
    done, category, priority, view, q = parse_filters()
    result = list(tasks.values())
    if done is not None:
        result = [t for t in result if t["done"] == (done == "true")]
    if category:
        result = [t for t in result if t["category"] == category]
    if priority:
        result = [t for t in result if t["priority"] == priority]
    if view:
        result = [t for t in result if in_view(t, view)]
    if q:
        result = [t for t in result if q in t["title"].lower() or q in t["note"].lower()]
    return jsonify(sorted(result, key=sort_key))


@app.post("/api/tasks")
def create_task():
    fields = valid_or_400(get_body())
    task = {"id": counter["next_id"], "done": False, "completed_at": None,
            "created_at": now().isoformat(timespec="seconds"), **fields}
    counter["next_id"] += 1
    tasks[task["id"]] = task
    return jsonify(task), 201


@app.get("/api/tasks/<int:task_id>")
def get_task(task_id):
    return jsonify(get_task_or_404(task_id))


@app.route("/api/tasks/<int:task_id>", methods=["PUT", "PATCH"])
def update_task(task_id):
    task = get_task_or_404(task_id)
    fields = valid_or_400(get_body(), partial=True)
    error = schedule_error({**task, **fields})
    if error:
        abort(400, error)
    if "done" in fields and fields["done"] != task["done"]:
        task["completed_at"] = now().isoformat(timespec="seconds") if fields["done"] else None
    task.update(fields)
    return jsonify(task)


@app.delete("/api/tasks/<int:task_id>")
def delete_task(task_id):
    get_task_or_404(task_id)
    del tasks[task_id]
    return "", 204


@app.get("/api/stats")
def stats():
    all_tasks = list(tasks.values())
    done = [t for t in all_tasks if t["done"]]
    done_today = [t for t in done if t["completed_at"][:10] == today()]
    open_tasks = [t for t in all_tasks if not t["done"]]
    return jsonify(
        total=len(all_tasks),
        done=len(done),
        remaining=len(open_tasks),
        overdue=sum(is_overdue(t) for t in all_tasks),
        done_today=len(done_today),
        today_open=sum(in_view(t, "today") for t in open_tasks),
        percent=round(100 * len(done) / len(all_tasks)) if all_tasks else 0,
        by_category={c: sum(t["category"] == c for t in open_tasks) for c in CATEGORIES},
        counts={
            "today": sum(in_view(t, "today") for t in all_tasks),
            "upcoming": sum(in_view(t, "upcoming") for t in open_tasks),
            "overdue": sum(is_overdue(t) for t in all_tasks),
            "done": len(done),
            "all": len(all_tasks),
        },
    )


@app.get("/api/export")
def export_data():
    response = jsonify(version=APP_VERSION, exported_at=now().isoformat(timespec="seconds"),
                       tasks=sorted(tasks.values(), key=lambda t: t["id"]))
    response.headers["Content-Disposition"] = "attachment; filename=todo-export.json"
    return response


@app.post("/api/import")
def import_data():
    body = get_body()
    records = body.get("tasks") if isinstance(body, dict) else None
    if not isinstance(records, list):
        abort(400, "File nhập phải có danh sách tasks.")
    imported = {}
    for i, record in enumerate(records, start=1):
        fields = validate_task(record)[0]
        task_id = record.get("id") if isinstance(record, dict) else None
        if (fields is None or isinstance(task_id, bool) or not isinstance(task_id, int)
                or task_id < 1 or task_id in imported):
            abort(400, f"Bản ghi số {i} không hợp lệ, chưa nhập gì.")
        done = fields.get("done", False)
        stamp = now().isoformat(timespec="seconds")
        created = record.get("created_at")
        completed = record.get("completed_at")
        imported[task_id] = {
            "id": task_id, "done": done, **fields,
            "created_at": created if isinstance(created, str) else stamp,
            "completed_at": (completed if isinstance(completed, str) else stamp) if done else None,
        }
    tasks.clear()
    tasks.update(imported)
    counter["next_id"] = max(imported, default=0) + 1
    return jsonify(imported=len(imported))
