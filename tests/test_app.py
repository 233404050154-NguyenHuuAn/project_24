from datetime import datetime

import pytest

import app as app_module
from validators import parse_date

FIXED_NOW = datetime(2026, 10, 26, 10, 0, tzinfo=app_module.VN_TZ)


@pytest.fixture
def client(monkeypatch):
    app_module.reset_store()
    monkeypatch.setattr(app_module, "now", lambda: FIXED_NOW)
    return app_module.app.test_client()


def add(client, title="Việc", **extra):
    res = client.post("/api/tasks", json={"title": title, **extra})
    assert res.status_code == 201
    return res.get_json()


# ---------- trang chính, health ----------

def test_health(client):
    assert client.get("/health").get_json() == {"status": "ok", "version": app_module.APP_VERSION}


def test_index_shows_version_and_title(client):
    html = client.get("/").get_data(as_text=True)
    assert f"v{app_module.APP_VERSION}" in html
    assert "Nhóm 3 – Đề tài 24" in html


def test_script_title_stored_verbatim_and_page_escapes(client):
    payload = "<script>alert(1)</script>"
    task = add(client, payload)
    assert client.get(f"/api/tasks/{task['id']}").get_json()["title"] == payload
    assert "<script>alert" not in client.get("/").get_data(as_text=True)


# ---------- tạo, đọc, sửa, xoá ----------

def test_create_defaults(client):
    task = add(client, "  Nộp bài  ")
    assert task == {"id": 1, "title": "Nộp bài", "note": "", "priority": "medium",
                    "category": "work", "due_date": None, "start_time": None,
                    "end_time": None, "done": False,
                    "created_at": "2026-10-26T10:00:00+07:00", "completed_at": None}


def test_create_full_fields_and_ids_increase(client):
    add(client, "a")
    task = add(client, "b", note="n", priority="high", category="study", due_date="2026-11-01")
    assert task["id"] == 2
    assert (task["priority"], task["category"], task["due_date"]) == ("high", "study", "2026-11-01")


@pytest.mark.parametrize("body", [
    {}, {"title": ""}, {"title": "   "}, {"title": 5}, {"title": "x" * 201},
    {"title": "a", "note": "x" * 1001}, {"title": "a", "note": 3},
    {"title": "a", "priority": "urgent"}, {"title": "a", "category": "game"},
    {"title": "a", "due_date": "26/10/2026"}, {"title": "a", "due_date": "2026-13-45"},
    {"title": "a", "due_date": 20261026}, {"title": "a", "done": "yes"},
    [], "chuỗi",
])
def test_create_invalid(client, body):
    res = client.post("/api/tasks", json=body)
    assert res.status_code == 400
    assert res.get_json()["error"]


def test_create_not_json(client):
    res = client.post("/api/tasks", data="không phải json", content_type="text/plain")
    assert res.status_code == 400


def test_create_accepts_null_note_and_empty_due(client):
    task = add(client, "a", note=None, due_date="")
    assert task["note"] == "" and task["due_date"] is None


def test_title_max_length_ok(client):
    assert add(client, "x" * 200)["title"] == "x" * 200


def test_get_task_and_404(client):
    task = add(client)
    assert client.get(f"/api/tasks/{task['id']}").get_json() == task
    res = client.get("/api/tasks/99")
    assert res.status_code == 404 and res.get_json()["error"]


def test_update_partial_and_put(client):
    task = add(client, "a", priority="low")
    res = client.patch(f"/api/tasks/{task['id']}", json={"title": "b"})
    assert res.get_json()["title"] == "b" and res.get_json()["priority"] == "low"
    res = client.put(f"/api/tasks/{task['id']}", json={"priority": "high", "due_date": None})
    assert res.get_json()["priority"] == "high"


def test_update_invalid_and_404(client):
    task = add(client)
    assert client.patch(f"/api/tasks/{task['id']}", json={"title": ""}).status_code == 400
    assert client.patch("/api/tasks/99", json={"title": "x"}).status_code == 404


def test_completed_at_set_and_cleared(client):
    task = add(client)
    url = f"/api/tasks/{task['id']}"
    done = client.patch(url, json={"done": True}).get_json()
    assert done["completed_at"] == "2026-10-26T10:00:00+07:00"
    again = client.patch(url, json={"done": True}).get_json()
    assert again["completed_at"] == done["completed_at"]
    assert client.patch(url, json={"done": False}).get_json()["completed_at"] is None


def test_delete(client):
    task = add(client)
    assert client.delete(f"/api/tasks/{task['id']}").status_code == 204
    assert client.get(f"/api/tasks/{task['id']}").status_code == 404
    assert client.delete(f"/api/tasks/{task['id']}").status_code == 404


def test_method_not_allowed_returns_json(client):
    res = client.post("/health")
    assert res.status_code == 405 and res.get_json()["error"]


# ---------- khung giờ ----------

def test_create_with_time_range_and_start_only(client):
    full = add(client, "a", due_date="2026-10-26", start_time="08:00", end_time="09:30")
    assert (full["start_time"], full["end_time"]) == ("08:00", "09:30")
    start_only = add(client, "b", due_date="2026-10-26", start_time="14:00", end_time="")
    assert (start_only["start_time"], start_only["end_time"]) == ("14:00", None)


@pytest.mark.parametrize("extra", [
    {"start_time": "8:00"}, {"start_time": "25:00"}, {"start_time": 800},
    {"start_time": "0800T"}, {"start_time": "T0800"}, {"end_time": "12:60"},
])
def test_create_invalid_time_format(client, extra):
    res = client.post("/api/tasks", json={"title": "a", "due_date": "2026-10-26", **extra})
    assert res.status_code == 400


@pytest.mark.parametrize("extra", [
    {"start_time": "08:00"},
    {"due_date": "2026-10-26", "end_time": "09:00"},
    {"due_date": "2026-10-26", "start_time": "09:00", "end_time": "09:00"},
    {"due_date": "2026-10-26", "start_time": "10:00", "end_time": "09:00"},
])
def test_create_invalid_schedule(client, extra):
    res = client.post("/api/tasks", json={"title": "a", **extra})
    assert res.status_code == 400 and res.get_json()["error"]


def test_patch_time_rules(client):
    task = add(client, "a", due_date="2026-10-26", start_time="08:00", end_time="09:00")
    url = f"/api/tasks/{task['id']}"
    res = client.patch(url, json={"due_date": None})
    assert res.status_code == 400
    assert client.get(url).get_json() == task
    assert client.patch(url, json={"start_time": "10:00"}).status_code == 400
    assert client.patch(url, json={"start_time": None}).status_code == 400
    res = client.patch(url, json={"start_time": None, "end_time": None, "due_date": None})
    assert res.status_code == 200 and res.get_json()["start_time"] is None


def test_patch_adds_time_to_task_with_date(client):
    task = add(client, "a", due_date="2026-10-26")
    res = client.patch(f"/api/tasks/{task['id']}", json={"start_time": "07:30"})
    assert res.status_code == 200 and res.get_json()["start_time"] == "07:30"


def test_sort_by_start_time_within_same_day(client):
    no_time = add(client, "không giờ", due_date="2026-11-01")
    late = add(client, "chiều", due_date="2026-11-01", start_time="15:00")
    early = add(client, "sáng", due_date="2026-11-01", start_time="08:00")
    next_day = add(client, "hôm sau", due_date="2026-11-02", start_time="06:00")
    assert ids(client) == [early["id"], late["id"], no_time["id"], next_day["id"]]


# ---------- lọc, sắp xếp ----------

def ids(client, query=""):
    return [t["id"] for t in client.get(f"/api/tasks{query}").get_json()]


def test_filter_done_category_priority(client):
    a = add(client, "a", category="study", priority="high")
    b = add(client, "b", category="personal", priority="low")
    client.patch(f"/api/tasks/{b['id']}", json={"done": True})
    assert ids(client, "?done=true") == [b["id"]]
    assert ids(client, "?done=false") == [a["id"]]
    assert ids(client, "?category=study") == [a["id"]]
    assert ids(client, "?priority=low") == [b["id"]]
    assert ids(client, "?category=study&priority=low") == []


def test_filter_search_case_insensitive_in_title_and_note(client):
    a = add(client, "Học Python")
    b = add(client, "khác", note="ôn PYTHON")
    add(client, "không liên quan")
    assert ids(client, "?q=python") == [a["id"], b["id"]]
    assert ids(client, "?q=%20") == [1, 2, 3]  # q chỉ có khoảng trắng thì bỏ qua


def test_views(client):
    over = add(client, "quá hạn", due_date="2026-10-20")
    now_ = add(client, "hôm nay", due_date="2026-10-26")
    soon = add(client, "sắp tới", due_date="2026-10-30")
    add(client, "không hạn")
    done_over = add(client, "xong từ lâu", due_date="2026-10-01")
    client.patch(f"/api/tasks/{done_over['id']}", json={"done": True})
    assert ids(client, "?view=today") == [over["id"], now_["id"]]
    assert ids(client, "?view=upcoming") == [soon["id"]]
    assert ids(client, "?view=overdue") == [over["id"]]


def test_today_view_includes_done_task_due_today(client):
    t = add(client, "xong hôm nay", due_date="2026-10-26")
    client.patch(f"/api/tasks/{t['id']}", json={"done": True})
    assert ids(client, "?view=today") == [t["id"]]


def test_default_sort_order(client):
    no_due = add(client, "không hạn", priority="high")
    later_low = add(client, "sau, thấp", due_date="2026-11-05", priority="low")
    later_high = add(client, "sau, cao", due_date="2026-11-05", priority="high")
    soon = add(client, "gần", due_date="2026-10-28")
    overdue = add(client, "quá hạn", due_date="2026-10-01")
    finished = add(client, "xong", due_date="2026-10-02")
    client.patch(f"/api/tasks/{finished['id']}", json={"done": True})
    assert ids(client) == [overdue["id"], soon["id"], later_high["id"], later_low["id"],
                           no_due["id"], finished["id"]]


@pytest.mark.parametrize("query", [
    "?done=maybe", "?category=x", "?priority=x", "?view=x",
])
def test_filter_invalid(client, query):
    assert client.get(f"/api/tasks{query}").status_code == 400


# ---------- thống kê ----------

def test_stats_empty(client):
    data = client.get("/api/stats").get_json()
    assert data["total"] == 0 and data["percent"] == 0
    assert data["counts"]["all"] == 0
    assert data["by_category"] == {"work": 0, "study": 0, "personal": 0}


def test_stats_values(client):
    add(client, "quá hạn", due_date="2026-10-20", category="study")
    add(client, "hôm nay", due_date="2026-10-26")
    add(client, "sắp tới", due_date="2026-11-01", category="personal")
    finished = add(client, "xong", due_date="2026-10-26")
    client.patch(f"/api/tasks/{finished['id']}", json={"done": True})
    data = client.get("/api/stats").get_json()
    assert (data["total"], data["done"], data["remaining"]) == (4, 1, 3)
    assert (data["overdue"], data["done_today"], data["today_open"]) == (1, 1, 2)
    assert data["percent"] == 25
    assert data["by_category"] == {"work": 1, "study": 1, "personal": 1}
    assert data["counts"] == {"today": 3, "upcoming": 1, "overdue": 1, "done": 1, "all": 4}


def test_stats_done_before_today_not_counted(client):
    t = add(client)
    client.patch(f"/api/tasks/{t['id']}", json={"done": True})
    app_module.tasks[t["id"]]["completed_at"] = "2026-10-25T09:00:00+07:00"
    assert client.get("/api/stats").get_json()["done_today"] == 0


# ---------- xuất, nhập ----------

def test_export_headers_and_content(client):
    add(client, "a")
    res = client.get("/api/export")
    assert "todo-export.json" in res.headers["Content-Disposition"]
    data = res.get_json()
    assert data["version"] == app_module.APP_VERSION
    assert [t["title"] for t in data["tasks"]] == ["a"]


def test_export_import_roundtrip(client):
    add(client, "a", priority="high", due_date="2026-10-30")
    b = add(client, "b", category="personal")
    client.patch(f"/api/tasks/{b['id']}", json={"done": True})
    exported = client.get("/api/export").get_json()
    app_module.reset_store()
    res = client.post("/api/import", json=exported)
    assert res.status_code == 200 and res.get_json() == {"imported": 2}
    assert client.get("/api/export").get_json()["tasks"] == exported["tasks"]
    assert add(client, "mới")["id"] == 3


def test_import_replaces_everything_and_fills_missing_timestamps(client):
    add(client, "cũ")
    res = client.post("/api/import", json={"tasks": [
        {"id": 7, "title": "mới", "done": True},
        {"id": 9, "title": "chưa xong", "created_at": 5, "completed_at": "bị bỏ qua"},
    ]})
    assert res.status_code == 200
    tasks = client.get("/api/export").get_json()["tasks"]
    assert [t["id"] for t in tasks] == [7, 9]
    assert tasks[0]["created_at"] == tasks[0]["completed_at"] == "2026-10-26T10:00:00+07:00"
    assert tasks[1]["completed_at"] is None
    assert add(client, "tiếp")["id"] == 10


def test_import_keeps_time_range(client):
    add(client, "a", due_date="2026-10-30", start_time="08:00", end_time="09:30")
    exported = client.get("/api/export").get_json()
    app_module.reset_store()
    assert client.post("/api/import", json=exported).status_code == 200
    task = client.get("/api/tasks/1").get_json()
    assert (task["start_time"], task["end_time"]) == ("08:00", "09:30")


def test_import_invalid_time_changes_nothing(client):
    keep = add(client, "giữ lại")
    bad = {"tasks": [{"id": 1, "title": "a", "start_time": "08:00"}]}  # có giờ mà không có ngày
    assert client.post("/api/import", json=bad).status_code == 400
    assert ids(client) == [keep["id"]]


def test_import_empty_list_resets_counter(client):
    add(client)
    assert client.post("/api/import", json={"tasks": []}).status_code == 200
    assert add(client)["id"] == 1


@pytest.mark.parametrize("body", [
    [], {}, {"tasks": "x"},
    {"tasks": ["x"]},
    {"tasks": [{"title": "a"}]},
    {"tasks": [{"id": 0, "title": "a"}]},
    {"tasks": [{"id": True, "title": "a"}]},
    {"tasks": [{"id": "1", "title": "a"}]},
    {"tasks": [{"id": 1, "title": ""}]},
    {"tasks": [{"id": 1, "title": "a"}, {"id": 1, "title": "b"}]},
    {"tasks": [{"id": 1, "title": "a"}, {"id": 2, "title": "b", "priority": "x"}]},
])
def test_import_invalid_changes_nothing(client, body):
    keep = add(client, "giữ lại")
    res = client.post("/api/import", json=body)
    assert res.status_code == 400 and res.get_json()["error"]
    assert ids(client) == [keep["id"]]


def test_import_too_large_returns_413_json(client):
    big = "x" * (1024 * 1024 + 1)
    res = client.post("/api/import", data=big, content_type="application/json")
    assert res.status_code == 413
    assert res.get_json()["error"]


# ---------- validators ----------

def test_parse_date():
    assert parse_date("2026-10-26").day == 26
    assert parse_date("2026-1-5") is None
    assert parse_date("abc") is None
    assert parse_date(None) is None


def test_today_uses_vietnam_timezone(monkeypatch):
    monkeypatch.undo()
    assert app_module.now().tzinfo is app_module.VN_TZ
    assert app_module.today() == app_module.now().date().isoformat()
