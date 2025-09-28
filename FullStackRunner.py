import customtkinter as ctk
import subprocess
import os
import threading

# Detect base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
BACKEND_DIR = os.path.join(BASE_DIR, "backend")

# App setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Project Launcher")
app.geometry("1400x800")   # big window
app.state("zoomed")        # full screen

# Main frame divided horizontally
main_frame = ctk.CTkFrame(app)
main_frame.pack(fill="both", expand=True)

lhs = ctk.CTkFrame(main_frame, width=300)
lhs.pack(side="left", fill="y")
rhs = ctk.CTkFrame(main_frame)
rhs.pack(side="right", fill="both", expand=True)

# Terminal boxes (RHS, stacked vertically)
terminals = []
for i in range(4):
    tbox = ctk.CTkTextbox(rhs, wrap="word")
    tbox.pack(fill="both", expand=True, pady=2)
    terminals.append(tbox)

# --- Helper functions ---
def run_command(cmd, cwd, term_index):
    """Run a shell command and pipe output into terminal box."""
    def task():
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True,
            text=True
        )
        for line in iter(process.stdout.readline, ""):
            terminals[term_index].insert("end", line)
            terminals[term_index].see("end")
        process.stdout.close()
        process.wait()
    threading.Thread(target=task, daemon=True).start()

# --- Button commands ---
def npm_start():
    run_command("npm start", FRONTEND_DIR, 0)

def npm_build():
    run_command("npm run build", FRONTEND_DIR, 1)

def django_runserver():
    run_command("python manage.py runserver", BACKEND_DIR, 2)

def django_makemigrations():
    run_command("python manage.py makemigrations", BACKEND_DIR, 3)

def django_migrate():
    run_command("python manage.py migrate", BACKEND_DIR, 3)

def full_stack():
    npm_start()
    django_makemigrations()
    django_migrate()
    django_runserver()

def git_commit():
    message = commit_entry.get().strip()
    if message:
        cmd = f'git add . && git commit -m "{message}"'
        run_command(cmd, BASE_DIR, 3)

def git_sync():
    cmd = "git pull && git push"
    run_command(cmd, BASE_DIR, 3)

# --- LHS Controls ---
ctk.CTkButton(lhs, text="🚀 NPM Start", command=npm_start).pack(pady=5)
ctk.CTkButton(lhs, text="📦 NPM Build", command=npm_build).pack(pady=5)
ctk.CTkButton(lhs, text="▶ Django Runserver", command=django_runserver).pack(pady=5)
ctk.CTkButton(lhs, text="🛠 Django Makemigrations", command=django_makemigrations).pack(pady=5)
ctk.CTkButton(lhs, text="📂 Django Migrate", command=django_migrate).pack(pady=5)
ctk.CTkButton(lhs, text="⚡ Run Full Stack", command=full_stack).pack(pady=10)

ctk.CTkLabel(lhs, text="Commit Message:").pack(pady=5)
commit_entry = ctk.CTkEntry(lhs, width=250, placeholder_text="Enter commit message")
commit_entry.pack(pady=5)

ctk.CTkButton(lhs, text="💾 Git Add & Commit", command=git_commit).pack(pady=5)
ctk.CTkButton(lhs, text="🔄 Git Sync (Pull + Push)", command=git_sync).pack(pady=5)

app.mainloop()
