"""Kiểm tra dữ liệu công việc, dùng chung cho POST/PUT/PATCH/import."""
from datetime import date, time

PRIORITIES = ("high", "medium", "low")
CATEGORIES = ("work", "study", "personal")
TITLE_MAX = 200
NOTE_MAX = 1000


def parse_date(value):
    """Trả về date nếu value đúng YYYY-MM-DD, ngược lại None."""
    if not isinstance(value, str) or len(value) != 10:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def parse_time(value):
    """Trả về time nếu value đúng HH:MM, ngược lại None."""
    if not isinstance(value, str) or len(value) != 5 or value[2] != ":":
        return None
    try:
        return time.fromisoformat(value)
    except ValueError:
        return None


def validate_task(data, partial=False):
    """Trả về (fields, error). Chỉ giữ các trường hợp lệ, bỏ qua trường lạ.

    partial=True: chỉ kiểm tra trường được gửi (dùng cho sửa).
    partial=False: title bắt buộc, trường thiếu dùng mặc định (dùng cho tạo mới).
    """
    if not isinstance(data, dict):
        return None, "Dữ liệu gửi lên phải là một đối tượng JSON."
    out = {}
    if "title" in data or not partial:
        title = data.get("title")
        if not isinstance(title, str) or not title.strip():
            return None, "Tiêu đề là bắt buộc."
        if len(title.strip()) > TITLE_MAX:
            return None, f"Tiêu đề tối đa {TITLE_MAX} ký tự."
        out["title"] = title.strip()
    if "note" in data or not partial:
        note = data.get("note", "")
        if note is None:
            note = ""
        if not isinstance(note, str) or len(note) > NOTE_MAX:
            return None, f"Ghi chú phải là chuỗi tối đa {NOTE_MAX} ký tự."
        out["note"] = note
    if "priority" in data or not partial:
        priority = data.get("priority", "medium")
        if priority not in PRIORITIES:
            return None, "Mức ưu tiên phải là high, medium hoặc low."
        out["priority"] = priority
    if "category" in data or not partial:
        category = data.get("category", "work")
        if category not in CATEGORIES:
            return None, "Nhóm việc phải là work, study hoặc personal."
        out["category"] = category
    if "due_date" in data or not partial:
        due = data.get("due_date")
        if due in (None, ""):
            out["due_date"] = None
        elif parse_date(due) is None:
            return None, "Hạn chót phải có dạng YYYY-MM-DD."
        else:
            out["due_date"] = due
    for key in ("start_time", "end_time"):
        if key in data or not partial:
            value = data.get(key)
            if value in (None, ""):
                out[key] = None
            elif parse_time(value) is None:
                return None, "Giờ phải có dạng HH:MM (24 giờ)."
            else:
                out[key] = value
    if "done" in data:
        if not isinstance(data["done"], bool):
            return None, "Trạng thái done phải là true hoặc false."
        out["done"] = data["done"]
    if not partial:
        error = schedule_error(out)
        if error:
            return None, error
    return out, None


def schedule_error(task):
    """Kiểm tra quan hệ ngày - giờ trên một bản ghi đầy đủ. Trả về thông báo lỗi hoặc None."""
    start, end = task["start_time"], task["end_time"]
    if (start or end) and not task["due_date"]:
        return "Cần chọn ngày trước khi đặt giờ."
    if end and not start:
        return "Cần có giờ bắt đầu trước khi đặt giờ kết thúc."
    if start and end and end <= start:
        return "Giờ kết thúc phải sau giờ bắt đầu."
    return None
