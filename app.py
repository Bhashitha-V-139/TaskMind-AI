from flask import Flask, render_template_string, request, jsonify
import sqlite3

app = Flask(__name__)

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            priority TEXT,
            category TEXT,
            duration TEXT,
            subtasks TEXT,
            focus_time TEXT,
            completed INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# --- Rule-Based AI Engine ---
def analyze_task_with_ai(title):
    text = title.lower()
    
    # 1. Determine Priority
    high_keywords = ['urgent', 'asap', 'deadline', 'fix', 'bug', 'client', 'critical', 'submit', 'exam']
    medium_keywords = ['plan', 'review', 'draft', 'design', 'update', 'meeting', 'buy', 'study']
    
    if any(k in text for k in high_keywords):
        priority = "High"
    elif any(k in text for k in medium_keywords):
        priority = "Medium"
    else:
        priority = "Low"

    # 2. Determine Category
    if any(k in text for k in ['code', 'bug', 'app', 'design', 'fix', 'build', 'client', 'email']):
        category = "Work"
    elif any(k in text for k in ['study', 'exam', 'read', 'class', 'homework', 'notes']):
        category = "Study"
    elif any(k in text for k in ['buy', 'pay', 'clean', 'groceries', 'shop']):
        category = "Personal"
    elif any(k in text for k in ['run', 'gym', 'workout', 'meditate', 'doctor', 'health']):
        category = "Health"
    else:
        category = "General"

    # 3. Estimate Duration
    if any(k in text for k in ['quick', 'email', 'call', 'buy', 'pay', 'clean']):
        duration = "15 mins"
    elif any(k in text for k in ['review', 'draft', 'meeting', 'workout', 'read']):
        duration = "30 mins"
    else:
        duration = "60 mins"

    # 4. AI Sub-steps Breakdown
    subtasks = []
    if 'code' in text or 'build' in text or 'app' in text or 'fix' in text:
        subtasks = ["Outline architecture", "Write core logic", "Test & debug"]
    elif 'write' in text or 'essay' in text or 'report' in text or 'draft' in text:
        subtasks = ["Research topic", "Create bullet outline", "Draft & refine"]
    elif 'plan' in text or 'event' in text or 'trip' in text:
        subtasks = ["List requirements", "Check schedule & budget", "Confirm details"]
    elif 'study' in text or 'read' in text or 'exam' in text:
        subtasks = ["Review key notes", "Practice core exercises", "Summarize learnings"]
    else:
        subtasks = ["Initiate task setup", "Execute core action", "Perform final review"]

    # 5. Optimal Focus Time
    if priority == "High":
        focus_time = "Morning Peak"
    elif priority == "Medium":
        focus_time = "Early Afternoon"
    else:
        focus_time = "Late Afternoon"

    return {
        "priority": priority,
        "category": category,
        "duration": duration,
        "subtasks": " | ".join(subtasks),
        "focus_time": focus_time
    }

# --- API Routes ---
@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, priority, category, duration, subtasks, focus_time, completed FROM tasks ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    
    tasks = []
    for r in rows:
        tasks.append({
            "id": r[0],
            "title": r[1],
            "priority": r[2],
            "category": r[3] if len(r) > 3 and r[3] else "General",
            "duration": r[4],
            "subtasks": r[5].split(" | ") if r[5] else [],
            "focus_time": r[6],
            "completed": bool(r[7])
        })
    return jsonify(tasks)

@app.route("/api/tasks", methods=["POST"])
def add_task():
    data = request.json
    title = data.get("title", "").strip()
    if not title:
        return jsonify({"error": "Title required"}), 400

    ai_data = analyze_task_with_ai(title)

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (title, priority, category, duration, subtasks, focus_time, completed)
        VALUES (?, ?, ?, ?, ?, ?, 0)
    ''', (title, ai_data["priority"], ai_data["category"], ai_data["duration"], ai_data["subtasks"], ai_data["focus_time"]))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()

    return jsonify({"id": task_id, "title": title, **ai_data, "completed": False})

@app.route("/api/tasks/<int:task_id>/toggle", methods=["PUT"])
def toggle_task(task_id):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET completed = CASE WHEN completed = 1 THEN 0 ELSE 1 END WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

# --- HTML & CSS Template ---
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>TaskMind AI - Colourful Smart Task Manager</title>
</head>
<body style="margin: 0; padding: 20px; min-height: 100vh; box-sizing: border-box; display: flex; justify-content: center; align-items: center; background: linear-gradient(-45deg, #0f172a, #3b0764, #0284c7, #4c1d95); background-size: 400% 400%; animation: gradientBG 15s ease infinite; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; -webkit-font-smoothing: antialiased; color: #f8fafc;">

  <style>
    @keyframes gradientBG {
      0% { background-position: 0% 50%; }
      50% { background-position: 100% 50%; }
      100% { background-position: 0% 50%; }
    }
  </style>

  <div style="background: rgba(15, 23, 42, 0.65); backdrop-filter: blur(24px); -webkit-backdrop-filter: blur(24px); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 28px; padding: 32px; width: 100%; max-width: 540px; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7); box-sizing: border-box;">
    
    <!-- Header -->
    <div style="text-align: center; margin-bottom: 24px;">
      <div style="display: inline-block; padding: 6px 14px; background: rgba(236, 72, 153, 0.2); border: 1px solid rgba(236, 72, 153, 0.4); border-radius: 20px; color: #f472b6; font-size: 12px; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 10px;">⚡ Dynamic AI Productivity</div>
      <h2 style="margin: 0; font-size: 28px; font-weight: 800; background: linear-gradient(135deg, #38bdf8, #f472b6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">TaskMind AI</h2>
    </div>

    <!-- Progress Tracker Bar -->
    <div style="margin-bottom: 20px; background: rgba(255, 255, 255, 0.05); padding: 12px 16px; border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.08);">
      <div style="display: flex; justify-content: space-between; font-size: 12px; font-weight: 600; color: #cbd5e1; margin-bottom: 6px;">
        <span>Completion Rate</span>
        <span id="progressText">0%</span>
      </div>
      <div style="height: 8px; width: 100%; background: rgba(255, 255, 255, 0.1); border-radius: 4px; overflow: hidden;">
        <div id="progressBar" style="height: 100%; width: 0%; background: linear-gradient(90deg, #38bdf8, #34d399); transition: width 0.4s ease;"></div>
      </div>
    </div>

    <!-- Add Task Input Form -->
    <div style="display: flex; gap: 10px; margin-bottom: 18px;">
      <input type="text" id="taskInput" placeholder="Enter task (e.g., 'Study math exam urgent')" style="flex: 1; padding: 14px 18px; border-radius: 14px; border: 1px solid rgba(255, 255, 255, 0.15); background: rgba(15, 23, 42, 0.7); color: #f8fafc; font-size: 15px; outline: none; transition: border-color 0.2s;" onkeydown="if(event.key==='Enter') addTask()">
      <button onclick="addTask()" style="padding: 14px 22px; border: none; border-radius: 14px; background: linear-gradient(135deg, #ec4899 0%, #8b5cf6 100%); color: #ffffff; font-size: 15px; font-weight: 700; cursor: pointer; white-space: nowrap; transition: opacity 0.2s ease;" onmouseover="this.style.opacity='0.9'" onmouseout="this.style.opacity='1'">+ Add</button>
    </div>

    <!-- Filter Tabs & Search Row -->
    <div style="display: flex; justify-content: space-between; align-items: center; gap: 10px; margin-bottom: 18px;">
      <!-- Filter Tabs -->
      <div style="display: flex; gap: 6px; background: rgba(15, 23, 42, 0.5); padding: 4px; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.05);">
        <button onclick="setFilter('all')" id="filterAll" style="padding: 6px 12px; border: none; border-radius: 8px; background: #3b82f6; color: #fff; font-size: 12px; font-weight: 600; cursor: pointer;">All</button>
        <button onclick="setFilter('active')" id="filterActive" style="padding: 6px 12px; border: none; border-radius: 8px; background: transparent; color: #94a3b8; font-size: 12px; font-weight: 600; cursor: pointer;">Active</button>
        <button onclick="setFilter('completed')" id="filterCompleted" style="padding: 6px 12px; border: none; border-radius: 8px; background: transparent; color: #94a3b8; font-size: 12px; font-weight: 600; cursor: pointer;">Completed</button>
      </div>

      <!-- Live Search Box -->
      <input type="text" id="searchInput" oninput="fetchTasks()" placeholder="🔍 Search..." style="width: 110px; padding: 7px 12px; border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.1); background: rgba(15, 23, 42, 0.5); color: #f8fafc; font-size: 12px; outline: none;">
    </div>

    <!-- Tasks List Container -->
    <div id="taskList" style="display: flex; flex-direction: column; gap: 12px; max-height: 380px; overflow-y: auto; padding-right: 4px;">
      <!-- Dynamic Tasks Render Here -->
    </div>

  </div>

  <script>
    let allTasks = [];
    let currentFilter = 'all';

    async function fetchTasks() {
      const res = await fetch('/api/tasks');
      allTasks = await res.json();
      renderTasks();
    }

    async function addTask() {
      const input = document.getElementById('taskInput');
      const title = input.value.trim();
      if (!title) return;

      input.value = '';
      await fetch('/api/tasks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title })
      });
      fetchTasks();
    }

    async function toggleTask(id) {
      await fetch(`/api/tasks/${id}/toggle`, { method: 'PUT' });
      fetchTasks();
    }

    async function deleteTask(id) {
      await fetch(`/api/tasks/${id}`, { method: 'DELETE' });
      fetchTasks();
    }

    function setFilter(filter) {
      currentFilter = filter;
      ['all', 'active', 'completed'].forEach(f => {
        const btn = document.getElementById('filter' + f.charAt(0).toUpperCase() + f.slice(1));
        if (f === filter) {
          btn.style.background = '#3b82f6';
          btn.style.color = '#fff';
        } else {
          btn.style.background = 'transparent';
          btn.style.color = '#94a3b8';
        }
      });
      renderTasks();
    }

    function renderTasks() {
      const container = document.getElementById('taskList');
      const searchQuery = document.getElementById('searchInput').value.toLowerCase();
      container.innerHTML = '';

      // Update Completion Progress Bar
      const total = allTasks.length;
      const completedCount = allTasks.filter(t => t.completed).length;
      const percent = total === 0 ? 0 : Math.round((completedCount / total) * 100);
      document.getElementById('progressBar').style.width = percent + '%';
      document.getElementById('progressText').textContent = `${completedCount}/${total} (${percent}%)`;

      // Filter tasks
      let filtered = allTasks.filter(t => {
        const matchesFilter = currentFilter === 'all' || 
          (currentFilter === 'active' && !t.completed) || 
          (currentFilter === 'completed' && t.completed);
        const matchesSearch = t.title.toLowerCase().includes(searchQuery);
        return matchesFilter && matchesSearch;
      });

      if (filtered.length === 0) {
        container.innerHTML = '<div style="text-align: center; color: #94a3b8; font-size: 14px; padding: 24px;">No matching tasks found.</div>';
        return;
      }

      filtered.forEach(task => {
        const priorityColors = { High: '#f43f5e', Medium: '#fbbf24', Low: '#34d399' };
        const categoryColors = { Work: '#38bdf8', Study: '#c084fc', Personal: '#f472b6', Health: '#4ade80', General: '#cbd5e1' };

        const card = document.createElement('div');
        card.style.cssText = `background: rgba(15, 23, 42, 0.65); padding: 16px; border-radius: 18px; border: 1px solid rgba(255, 255, 255, 0.08); display: flex; flex-direction: column; gap: 10px; opacity: ${task.completed ? '0.55' : '1'}; transition: all 0.2s ease;`;

        const subtasksHtml = task.subtasks.map(s => `<li style="margin-bottom: 2px;">${s}</li>`).join('');

        card.innerHTML = `
          <div style="display: flex; align-items: center; justify-content: space-between; gap: 12px;">
            <div style="display: flex; align-items: center; gap: 12px; flex: 1;">
              <input type="checkbox" ${task.completed ? 'checked' : ''} onclick="toggleTask(${task.id})" style="width: 18px; height: 18px; accent-color: #ec4899; cursor: pointer;">
              <span style="font-size: 16px; font-weight: 600; color: #f8fafc; text-decoration: ${task.completed ? 'line-through' : 'none'};">${task.title}</span>
            </div>
            <button onclick="deleteTask(${task.id})" style="background: transparent; border: none; color: #64748b; font-size: 16px; cursor: pointer; transition: color 0.15s;" onmouseover="this.style.color='#f43f5e'" onmouseout="this.style.color='#64748b'">✕</button>
          </div>

          <!-- Badges Bar -->
          <div style="display: flex; flex-wrap: wrap; gap: 6px; font-size: 11px; font-weight: 600;">
            <span style="background: rgba(255,255,255,0.05); color: ${categoryColors[task.category] || '#cbd5e1'}; padding: 3px 8px; border-radius: 6px; border: 1px solid ${categoryColors[task.category] || '#cbd5e1'}40;">🏷️ ${task.category}</span>
            <span style="background: rgba(255,255,255,0.05); color: ${priorityColors[task.priority]}; padding: 3px 8px; border-radius: 6px; border: 1px solid ${priorityColors[task.priority]}40;">● ${task.priority}</span>
            <span style="background: rgba(255,255,255,0.05); color: #38bdf8; padding: 3px 8px; border-radius: 6px; border: 1px solid rgba(56, 189, 248, 0.2);">⏱️ ${task.duration}</span>
            <span style="background: rgba(255,255,255,0.05); color: #c084fc; padding: 3px 8px; border-radius: 6px; border: 1px solid rgba(192, 132, 252, 0.2);">🤖 ${task.focus_time}</span>
          </div>

          <!-- AI Action Plan Breakdown -->
          ${task.subtasks.length > 0 ? `
            <div style="background: rgba(9, 13, 22, 0.5); padding: 10px 12px; border-radius: 10px; font-size: 12px; color: #cbd5e1; border-left: 3px solid #ec4899;">
              <div style="font-weight: 700; color: #f472b6; margin-bottom: 4px; font-size: 11px; text-transform: uppercase;">AI Breakdown Plan:</div>
              <ul style="margin: 0; padding-left: 16px;">${subtasksHtml}</ul>
            </div>
          ` : ''}
        `;
        container.appendChild(card);
      });
    }

    fetchTasks();
  </script>
</body>
</html>"""

if __name__ == "__main__":
    app.run()