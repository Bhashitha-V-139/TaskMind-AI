# ⚡ TaskMind AI

A colourful, smart task management web application built with **Flask**, **SQLite**, HTML, CSS, and JavaScript.

TaskMind AI analyzes tasks using a rule-based AI engine and automatically determines their **priority, category, estimated duration, subtasks, and optimal focus time**.

---

## ✨ Features

* 📝 Add new tasks
* 🤖 Automatic task analysis
* 🔥 Priority detection:

  * High
  * Medium
  * Low
* 🏷️ Automatic task categorization:

  * Work
  * Study
  * Personal
  * Health
  * General
* ⏱️ Automatic duration estimation
* 📋 AI-generated task breakdown
* 🧠 Recommended focus time
* ✅ Mark tasks as completed
* 🗑️ Delete tasks
* 🔍 Live task search
* 📑 Filter tasks:

  * All
  * Active
  * Completed
* 📊 Completion progress bar
* 💾 Persistent storage using SQLite
* 🎨 Responsive glassmorphism-style interface
* 🌈 Animated gradient background

---

## 🛠️ Technologies Used

| Technology | Purpose                      |
| ---------- | ---------------------------- |
| Python     | Backend programming          |
| Flask      | Web framework                |
| SQLite     | Database                     |
| HTML5      | Page structure               |
| CSS3       | Styling and animations       |
| JavaScript | Frontend interaction         |
| Fetch API  | Communication with Flask API |

---

## 📁 Project Structure

```text
TaskMind-AI/
│
├── app.py              # Main Flask application
├── tasks.db            # SQLite database (created automatically)
├── README.md           # Project documentation
└── venv/               # Python virtual environment (optional)
```

---

## 🚀 Installation

### 1. Clone or download the project

If using Git:

```bash
git clone <your-repository-url>
cd TaskMind-AI
```

Alternatively, download the project ZIP and extract it.

---

### 2. Create a virtual environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install Flask

```bash
pip install flask
```

Or:

```bash
python -m pip install flask
```

---

## ▶️ Running the Application

Run:

```bash
python app.py
```

You should see something similar to:

```text
* Running on http://127.0.0.1:5000
* Debugger is active
```

Open your browser and visit:

```text
http://127.0.0.1:5000
```

The TaskMind AI dashboard should now be available.

---

## 🗄️ Database

TaskMind AI uses **SQLite** for storing tasks.

The database is automatically created when the application starts.

The database contains the following fields:

| Field        | Description              |
| ------------ | ------------------------ |
| `id`         | Unique task ID           |
| `title`      | Task title               |
| `priority`   | High, Medium, or Low     |
| `category`   | Task category            |
| `duration`   | Estimated task duration  |
| `subtasks`   | AI-generated task steps  |
| `focus_time` | Recommended focus period |
| `completed`  | Completion status        |

You do **not** need to manually create `tasks.db`.

---

## 🤖 How the AI Engine Works

The current version uses a **rule-based AI engine** rather than an external AI API.

When you add a task, the application analyzes its title and looks for keywords.

For example:

```text
Study math exam urgent
```

The engine may determine:

```text
Priority: High
Category: Study
Duration: 60 mins
Focus Time: Morning Peak
```

It can also generate subtasks such as:

```text
Review key notes
Practice core exercises
Summarize learnings
```

### Priority Detection

Some keywords associated with high priority include:

```text
urgent
asap
deadline
fix
bug
client
critical
submit
exam
```

Medium-priority keywords include:

```text
plan
review
draft
design
update
meeting
buy
study
```

Tasks that don't match these keywords are assigned **Low** priority.

---

## 📡 API Endpoints

TaskMind AI provides a simple REST-style API.

### Get all tasks

```http
GET /api/tasks
```

Returns all stored tasks.

---

### Add a task

```http
POST /api/tasks
```

Example request:

```json
{
  "title": "Study math exam urgent"
}
```

The server automatically analyzes the task before storing it.

---

### Toggle task completion

```http
PUT /api/tasks/<task_id>/toggle
```

Example:

```text
PUT /api/tasks/1/toggle
```

---

### Delete a task

```http
DELETE /api/tasks/<task_id>
```

Example:

```text
DELETE /api/tasks/1
```

---

## 🖥️ Example Tasks

Try adding tasks such as:

```text
Fix login bug urgently
```

```text
Study mathematics for exam
```

```text
Buy groceries
```

```text
Plan weekend trip
```

```text
Write project report
```

```text
Go to gym
```

TaskMind AI will automatically analyze them and display the resulting information.

---

## 🎨 User Interface

The application uses a modern glassmorphism-inspired design featuring:

* Animated gradient background
* Glass-style cards
* Colour-coded priorities
* Colour-coded categories
* Progress visualization
* Responsive layout
* Interactive task controls

---

## 🔧 Configuration

The application currently runs in Flask's development mode:

```python
app.run(debug=True)
```

For production deployment, `debug=True` should be disabled and the application should be run using an appropriate production WSGI server.

---

## 🔮 Future Improvements

Possible improvements include:

* [ ] Connect to a real LLM/AI API
* [ ] User accounts and authentication
* [ ] Task due dates
* [ ] Recurring tasks
* [ ] Calendar integration
* [ ] Drag-and-drop task ordering
* [ ] Custom priorities
* [ ] Custom categories
* [ ] Task editing
* [ ] Dark/light theme selection
* [ ] Notifications and reminders
* [ ] Analytics dashboard
* [ ] Export tasks to CSV/JSON
* [ ] Production deployment
* [ ] Mobile-friendly enhancements

---

## 🔐 Security Notes

This project is intended primarily for learning and development.

Before deploying publicly, consider adding:

* Input validation
* CSRF protection
* Authentication
* Authorization
* Rate limiting
* Secure production configuration
* Proper error handling
* A production WSGI server

---

## 📄 License

This project is available for personal and educational use.

You can modify, improve, and extend the project according to your needs.

---

## 👨‍💻 Getting Started

The quickest way to start the project is:

```bash
python -m venv venv
```

Activate the environment:

### Windows

```bash
venv\Scripts\activate
```

### macOS/Linux

```bash
source venv/bin/activate
```

Install Flask:

```bash
pip install flask
```

Run the application:

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

---

## ⭐ Project

**TaskMind AI — Dynamic AI Productivity Task Manager**

Built with ❤️ using Python, Flask, SQLite, HTML, CSS, and JavaScript.
