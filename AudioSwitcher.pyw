import csv, json, os, shutil, subprocess, sys, tempfile, threading, urllib.request, zipfile
import tkinter as tk
from tkinter import ttk, messagebox

DIR = os.path.join(os.environ.get("APPDATA", "."), "AudioSwitcher")
EXE = os.path.join(DIR, "SoundVolumeView.exe")
CFG = os.path.join(DIR, "config.json")
URL = "https://www.nirsoft.net/utils/soundvolumeview-x64.zip"
NOWIN = 0x08000000
os.makedirs(DIR, exist_ok=True)

try:  # must run before the window is created so the taskbar uses our own icon
    import ctypes
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("mohammed.audioswitcher.1")
except Exception:
    pass

BG, PANEL, CHIP, ACCENT, FG = "#1e1f22", "#2b2d31", "#383a40", "#5865f2", "#f2f3f5"


def ensure_tool():
    if os.path.exists(EXE):
        return
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    bundled = os.path.join(base, "SoundVolumeView.exe")
    if os.path.exists(bundled):
        shutil.copy(bundled, EXE)
        return
    z = os.path.join(DIR, "svv.zip")
    with urllib.request.urlopen(URL, timeout=30) as r, open(z, "wb") as out:
        out.write(r.read())
    with zipfile.ZipFile(z) as f:
        f.extractall(DIR)
    os.remove(z)


def run(args):
    subprocess.run([EXE] + args, creationflags=NOWIN)


def query():
    tmp = os.path.join(tempfile.gettempdir(), "svv_out.csv")
    if os.path.exists(tmp):
        os.remove(tmp)
    run(["/scomma", tmp])
    with open(tmp, encoding="utf-8-sig", errors="replace", newline="") as f:
        rows = list(csv.DictReader(f))
    devices, apps = [], {}
    for r in rows:
        if r.get("Direction") != "Render":
            continue
        if r.get("Type") == "Device" and r.get("Device State") == "Active":
            devices.append({"label": f'{r.get("Name")} ({r.get("Device Name")})',
                            "id": r.get("Command-Line Friendly ID")})
        elif r.get("Type") == "Application" and r.get("Process Path"):
            proc = os.path.basename(r["Process Path"])
            apps[proc] = (r.get("Name") or proc).replace(".exe", "")
    return devices, apps


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Audio Switcher")
        self.geometry("460x540")
        self.resizable(False, False)          # no maximize / fullscreen
        for p in (os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico"),
                  os.path.join(DIR, "icon.ico")):
            if os.path.exists(p):
                try:
                    self.iconbitmap(default=p)
                    self.update_idletasks()
                except Exception:
                    pass
                break
        self.configure(bg=BG)
        self.devices, self.apps = query()
        self.cfg = {"headphones": "", "speaker": "", "choices": {}}
        if os.path.exists(CFG):
            try:
                self.cfg.update(json.load(open(CFG, encoding="utf-8")))
            except Exception:
                pass
        labels = [d["label"] for d in self.devices]
        self.hp = tk.StringVar(value=self.cfg["headphones"] if self.cfg["headphones"] in labels else (labels[0] if labels else ""))
        self.sp = tk.StringVar(value=self.cfg["speaker"] if self.cfg["speaker"] in labels else (labels[-1] if labels else ""))
        self.hp.trace_add("write", lambda *a: self.save())
        self.sp.trace_add("write", lambda *a: self.save())

        top = tk.Frame(self, bg=BG)
        top.pack(fill="x", padx=10, pady=(10, 4))
        for text, var in (("🎧 السماعة", self.hp), ("🔊 السبيكر", self.sp)):
            r = tk.Frame(top, bg=BG)
            r.pack(fill="x", pady=1)
            tk.Label(r, text=text, bg=BG, fg=FG, width=10, anchor="w").pack(side="left")
            ttk.Combobox(r, textvariable=var, values=labels, state="readonly").pack(side="left", fill="x", expand=True)
        tk.Button(top, text="خلّ السماعة هي الديفلت لويندوز", command=self.set_default,
                  bg=PANEL, fg=FG, relief="flat", activebackground=CHIP, activeforeground=FG).pack(fill="x", pady=(6, 0))

        cols = tk.Frame(self, bg=BG)
        cols.pack(fill="both", expand=True, padx=10, pady=6)
        self.cols = {}
        for i, (key, title) in enumerate((("headphones", "🎧 سماعة"), ("speaker", "🔊 سبيكر"))):
            f = tk.Frame(cols, bg=PANEL)
            f.grid(row=0, column=i, sticky="nsew", padx=4)
            cols.grid_columnconfigure(i, weight=1, uniform="c")
            tk.Label(f, text=title, bg=PANEL, fg=FG, font=("Segoe UI", 11, "bold")).pack(pady=6)
            self.cols[key] = f
        cols.grid_rowconfigure(0, weight=1)

        tk.Label(self, text="اسحب البرنامج بين العمودين.",
                 bg=BG, fg="#949ba4", font=("Segoe UI", 8), wraplength=430).pack(pady=(0, 8))

        self.dragging = False
        self.shown = None
        self.build()
        self.after(4000, self.refresh)

    # ---- helpers
    def dev_id(self, which):
        label = self.hp.get() if which == "headphones" else self.sp.get()
        for d in self.devices:
            if d["label"] == label:
                return d["id"]

    def save(self):
        self.cfg["headphones"], self.cfg["speaker"] = self.hp.get(), self.sp.get()
        json.dump(self.cfg, open(CFG, "w", encoding="utf-8"))

    def set_default(self):
        i = self.dev_id("headphones")
        if i:
            threading.Thread(target=run, args=(["/SetDefault", i, "all"],), daemon=True).start()
            messagebox.showinfo("تم", "السماعة صارت الديفلت.")

    def apply(self, proc, which):
        i = self.dev_id(which)
        if i:
            threading.Thread(target=run, args=(["/SetAppDefault", i, "all", proc],), daemon=True).start()
        self.cfg["choices"][proc] = which
        self.save()

    # ---- UI
    def build(self):
        for f in self.cols.values():
            for w in f.winfo_children()[1:]:
                w.destroy()
        self.shown = set(self.apps)
        for proc, name in sorted(self.apps.items(), key=lambda x: x[1].lower()):
            which = self.cfg["choices"].get(proc, "headphones")
            chip = tk.Label(self.cols[which], text="⠿  " + name, bg=CHIP, fg=FG, anchor="w",
                            padx=8, pady=6, cursor="hand2")
            chip.pack(fill="x", padx=8, pady=3)
            chip.bind("<ButtonPress-1>", lambda e, p=proc, n=name: self.start_drag(e, n))
            chip.bind("<B1-Motion>", self.drag)
            chip.bind("<ButtonRelease-1>", lambda e, p=proc: self.drop(e, p))

    def start_drag(self, e, name):
        self.dragging = True
        self.ghost = tk.Toplevel(self)
        self.ghost.overrideredirect(True)
        self.ghost.attributes("-topmost", True, "-alpha", 0.85)
        tk.Label(self.ghost, text=name, bg=ACCENT, fg="white", padx=10, pady=6).pack()
        self.drag(e)

    def drag(self, e):
        self.ghost.geometry(f"+{e.x_root + 10}+{e.y_root + 10}")

    def drop(self, e, proc):
        self.ghost.destroy()
        self.dragging = False
        for key, f in self.cols.items():
            x, y = f.winfo_rootx(), f.winfo_rooty()
            if x <= e.x_root <= x + f.winfo_width() and y <= e.y_root <= y + f.winfo_height():
                if self.cfg["choices"].get(proc, "headphones") != key:
                    self.apply(proc, key)
                break
        self.build()

    def refresh(self):
        if not self.dragging:
            try:
                _, apps = query()
                if set(apps) != self.shown:
                    self.apps = apps
                    self.build()
            except Exception:
                pass
        self.after(4000, self.refresh)


if __name__ == "__main__":
    try:
        ensure_tool()
        App().mainloop()
    except Exception as e:
        messagebox.showerror("خطأ", str(e))
