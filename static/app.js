"use strict";

// Mọi dữ liệu người dùng (title, note) chỉ được đưa vào trang bằng textContent / createElement.
const TZ = "Asia/Ho_Chi_Minh";
const VIEW_TITLES = {
  today: "Hôm nay", upcoming: "Sắp tới", overdue: "Quá hạn", done: "Đã xong", all: "Tất cả",
};
const CAT_TITLES = { work: "Công việc", study: "Học tập", personal: "Cá nhân" };
const PRIO_TITLES = { high: "Cao", medium: "Vừa", low: "Thấp" };
const EMPTY_TEXT = {
  today: "Hôm nay chưa có việc nào. Thêm một việc ở ô phía trên.",
  upcoming: "Chưa có việc nào sắp tới. Đặt hạn chót cho việc mới để chúng hiện ở đây.",
  overdue: "Không có việc nào quá hạn. Tốt lắm.",
  done: "Chưa có việc nào hoàn thành.",
  all: "Chưa có công việc nào. Thêm việc đầu tiên ở ô phía trên.",
};

const state = { view: "today", category: "", priority: "", q: "", editingId: null };

const $ = (id) => document.getElementById(id);
const list = $("list");
const errorBox = $("error");

function el(tag, props = {}, ...children) {
  const node = document.createElement(tag);
  for (const [key, value] of Object.entries(props)) {
    if (key === "class") node.className = value;
    else if (key === "text") node.textContent = value;
    else if (key.startsWith("on")) node.addEventListener(key.slice(2), value);
    else node.setAttribute(key, value);
  }
  node.append(...children);
  return node;
}

// ---------- ngày giờ (theo giờ Việt Nam, giống máy chủ) ----------
function todayStr() {
  return new Date().toLocaleDateString("en-CA", { timeZone: TZ });
}

// Có chọn giờ mà chưa chọn ngày thì lấy hôm nay (máy chủ yêu cầu giờ phải đi kèm ngày).
function todayIfTimed(start, end) {
  return start || end ? todayStr() : null;
}

function daysBetween(fromStr, toStr) {
  return Math.round((Date.parse(toStr) - Date.parse(fromStr)) / 86400000);
}

function dueText(task) {
  if (!task.due_date) return null;
  const diff = daysBetween(todayStr(), task.due_date);
  if (!task.done && diff < 0) return { text: `Quá hạn ${-diff} ngày`, overdue: true };
  if (diff === 0) return { text: "Hạn hôm nay" };
  if (diff === 1) return { text: "Hạn ngày mai" };
  const [y, m, d] = task.due_date.split("-");
  return { text: `Hạn ${d}/${m}/${y}` };
}

function timeText(task) {
  if (!task.start_time) return "";
  return task.end_time ? `${task.start_time}-${task.end_time}` : task.start_time;
}

// ---------- gọi API ----------
async function api(path, options = {}) {
  let res;
  try {
    res = await fetch(path, {
      ...options,
      headers: options.body ? { "Content-Type": "application/json" } : {},
    });
  } catch {
    throw new Error("Không kết nối được máy chủ. Hãy thử lại sau.");
  }
  if (res.status === 204) return null;
  let data = null;
  try { data = await res.json(); } catch { /* phản hồi không phải JSON */ }
  if (!res.ok) throw new Error((data && data.error) || `Lỗi ${res.status}`);
  return data;
}

function showError(message) {
  errorBox.textContent = message;
  errorBox.hidden = !message;
}

async function run(action) {
  try {
    showError("");
    await action();
  } catch (e) {
    showError(e.message);
  }
}

// ---------- vẽ giao diện ----------
function taskQuery() {
  const p = new URLSearchParams();
  if (["today", "upcoming", "overdue"].includes(state.view)) p.set("view", state.view);
  if (state.view === "done") p.set("done", "true");
  if (state.category) p.set("category", state.category);
  if (state.priority) p.set("priority", state.priority);
  if (state.q) p.set("q", state.q);
  return p.toString();
}

function renderTask(task) {
  if (task.id === state.editingId) return renderEdit(task);
  const checkbox = el("input", {
    type: "checkbox", "aria-label": `Đánh dấu xong: ${task.title}`,
    onchange: (e) => run(async () => {
      await api(`/api/tasks/${task.id}`, { method: "PATCH", body: JSON.stringify({ done: e.target.checked }) });
      await refresh();
    }),
  });
  checkbox.checked = task.done;

  const meta = el("span", { class: "meta" },
    el("span", { class: `pill ${task.priority}`, text: PRIO_TITLES[task.priority] }),
    el("span", { class: "pill cat", text: CAT_TITLES[task.category] }));
  const due = dueText(task);
  if (due) {
    const when = timeText(task);
    meta.append(el("span", {
      class: due.overdue ? "due overdue" : "due",
      text: when ? `${due.text} · ${when}` : due.text,
    }));
  }

  const main = el("button", {
    type: "button", class: "task-main", "aria-label": `Sửa: ${task.title}`,
    onclick: () => { state.editingId = task.id; renderList(lastTasks); focusEdit(); },
  }, el("span", { class: "task-title", text: task.title }));
  if (task.note) main.append(el("span", { class: "task-note", text: task.note }));
  main.append(meta);

  return el("li", { class: task.done ? "task done" : "task", "data-priority": task.priority }, checkbox, main);
}

function option(value, label, selected) {
  const o = el("option", { value, text: label });
  o.selected = selected;
  return o;
}

function field(label, control) {
  return el("label", {}, label, control);
}

function renderEdit(task) {
  const title = el("input", { type: "text", maxlength: "200", required: "" });
  title.value = task.title;
  const note = el("textarea", { maxlength: "1000" });
  note.value = task.note;
  const priority = el("select", {},
    ...Object.entries(PRIO_TITLES).map(([v, l]) => option(v, l, v === task.priority)));
  const category = el("select", {},
    ...Object.entries(CAT_TITLES).map(([v, l]) => option(v, l, v === task.category)));
  const due = el("input", { type: "date" });
  due.value = task.due_date || "";
  const start = el("input", { type: "time" });
  start.value = task.start_time || "";
  const end = el("input", { type: "time" });
  end.value = task.end_time || "";

  const cancel = () => { state.editingId = null; renderList(lastTasks); };
  const form = el("form", {
    class: "edit",
    onsubmit: (e) => {
      e.preventDefault();
      run(async () => {
        await api(`/api/tasks/${task.id}`, {
          method: "PATCH",
          body: JSON.stringify({
            title: title.value, note: note.value, priority: priority.value,
            category: category.value, due_date: due.value || todayIfTimed(start.value, end.value),
            start_time: start.value || null, end_time: end.value || null,
          }),
        });
        state.editingId = null;
        await refresh();
      });
    },
    onkeydown: (e) => { if (e.key === "Escape") cancel(); },
  },
  field("Tiêu đề", title),
  field("Ghi chú", note),
  el("div", { class: "edit-row" }, field("Ưu tiên", priority), field("Nhóm việc", category), field("Hạn chót", due)),
  el("div", { class: "edit-row" }, field("Giờ bắt đầu", start), field("Giờ kết thúc", end)),
  el("div", { class: "edit-actions" },
    el("button", { class: "btn primary", type: "submit", text: "Lưu" }),
    el("button", { class: "btn", type: "button", text: "Huỷ", onclick: cancel }),
    el("span", { class: "spacer" }),
    el("button", {
      class: "btn danger", type: "button", text: "Xoá",
      onclick: () => {
        if (!confirm(`Xoá việc "${task.title}"?`)) return;
        run(async () => {
          await api(`/api/tasks/${task.id}`, { method: "DELETE" });
          state.editingId = null;
          await refresh();
        });
      },
    })));
  return el("li", { class: "task editing", "data-priority": task.priority }, form);
}

function focusEdit() {
  const input = list.querySelector(".edit input[type=text]");
  if (input) input.focus();
}

let lastTasks = [];

function renderList(tasks) {
  lastTasks = tasks;
  if (!tasks.length) {
    list.replaceChildren(el("li", { class: "empty", text: state.q ? "Không có việc nào khớp từ khoá." : EMPTY_TEXT[state.view] }));
    return;
  }
  list.replaceChildren(...tasks.map(renderTask));
}

function renderStats(s) {
  for (const [key, value] of Object.entries(s.counts)) {
    document.querySelector(`[data-count="${key}"]`).textContent = value;
  }
  for (const [key, value] of Object.entries(s.by_category)) {
    document.querySelector(`[data-cat-count="${key}"]`).textContent = value;
  }
  const planned = s.done_today + s.today_open;
  $("stat-today").textContent = `${s.done_today}/${planned}`;
  $("bar-today").style.width = `${planned ? Math.round(100 * s.done_today / planned) : 0}%`;
  $("stat-percent").textContent = `${s.percent}%`;
  $("bar-percent").style.width = `${s.percent}%`;
}

function renderNav() {
  $("view-title").textContent = VIEW_TITLES[state.view];
  $("view-date").textContent = new Date().toLocaleDateString("vi-VN", {
    weekday: "long", day: "numeric", month: "long", year: "numeric", timeZone: TZ,
  });
  document.querySelectorAll("[data-view]").forEach((b) => {
    b.setAttribute("aria-current", String(b.dataset.view === state.view));
  });
  document.querySelectorAll("[data-category]").forEach((b) => {
    b.setAttribute("aria-current", String(b.dataset.category === state.category));
  });
}

async function refresh() {
  renderNav();
  const [tasks, stats] = await Promise.all([api(`/api/tasks?${taskQuery()}`), api("/api/stats")]);
  renderList(tasks);
  renderStats(stats);
}

// ---------- sự kiện ----------
document.querySelectorAll("[data-view]").forEach((b) => b.addEventListener("click", () => {
  state.view = b.dataset.view;
  state.editingId = null;
  run(refresh);
}));

document.querySelectorAll("[data-category]").forEach((b) => b.addEventListener("click", () => {
  state.category = state.category === b.dataset.category ? "" : b.dataset.category;
  state.editingId = null;
  run(refresh);
}));

let searchTimer;
$("search").addEventListener("input", (e) => {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(() => { state.q = e.target.value.trim(); run(refresh); }, 200);
});

$("filter-priority").addEventListener("change", (e) => {
  state.priority = e.target.value;
  run(refresh);
});

$("add-form").addEventListener("submit", (e) => {
  e.preventDefault();
  run(async () => {
    await api("/api/tasks", {
      method: "POST",
      body: JSON.stringify({
        title: $("add-title").value, priority: $("add-priority").value,
        category: $("add-category").value,
        due_date: $("add-due").value || todayIfTimed($("add-start").value, $("add-end").value),
        start_time: $("add-start").value || null, end_time: $("add-end").value || null,
      }),
    });
    $("add-title").value = "";
    $("add-due").value = "";
    $("add-start").value = "";
    $("add-end").value = "";
    await refresh();
    $("add-title").focus();
  });
});

$("import-btn").addEventListener("click", () => $("import-file").click());
$("import-file").addEventListener("change", (e) => {
  const file = e.target.files[0];
  e.target.value = "";
  if (!file) return;
  if (!confirm("Nhập sẽ thay toàn bộ dữ liệu hiện tại. Tiếp tục?")) return;
  run(async () => {
    let data;
    try { data = JSON.parse(await file.text()); } catch { throw new Error("File không phải JSON hợp lệ."); }
    await api("/api/import", { method: "POST", body: JSON.stringify(data) });
    state.editingId = null;
    await refresh();
  });
});

// Phím tắt: N thêm việc, / tìm kiếm. Không chạy khi đang gõ trong ô nhập.
document.addEventListener("keydown", (e) => {
  if (e.ctrlKey || e.metaKey || e.altKey) return;
  if (e.target.closest("input, textarea, select") || e.target.isContentEditable) return;
  if (e.key === "n" || e.key === "N") { e.preventDefault(); $("add-title").focus(); }
  else if (e.key === "/") { e.preventDefault(); $("search").focus(); }
});

run(refresh);
