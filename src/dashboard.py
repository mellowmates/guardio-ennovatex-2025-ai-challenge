# src/dashboard.py
import tkinter as tk
from tkinter import ttk, scrolledtext

# High-contrast palette for readability
PALETTE = {
    "bg": "#0f1115",        # window background
    "panel": "#171a21",     # panel/card background
    "text": "#f2f5f7",      # primary text
    "muted": "#b7bec7",     # secondary text
    "primary": "#4ca8ff",   # accent
    "success": "#2bd47c",   # success/ok
    "warning": "#f7b731",   # learning/attention
    "danger": "#ff4d4f",    # high risk
    "accent": "#8a7dff",
    "border": "#262b33",
    "input_bg": "#1e232b",
}


class GuardioDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Guardio — Anomaly Detection Dashboard")
        self.geometry("820x560")
        self.minsize(760, 520)
        self.configure(bg=PALETTE["bg"])

        self._build_styles()
        self._build_layout()

        # Defaults for filters
        self.chk_move.state(["!alternate", "selected"])
        self.chk_type.state(["!alternate", "selected"])
        self.chk_app.state(["!alternate", "selected"])

    def _build_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        # Frames / Panels
        style.configure("TFrame", background=PALETTE["bg"])
        style.configure("Panel.TFrame", background=PALETTE["panel"], borderwidth=1, relief="solid")

        # Labels
        base_font = ("Segoe UI", 11)
        style.configure("TLabel", background=PALETTE["bg"], foreground=PALETTE["text"], font=base_font)
        style.configure("Muted.TLabel", background=PALETTE["bg"], foreground=PALETTE["muted"], font=base_font)
        style.configure("Title.TLabel", background=PALETTE["bg"], foreground=PALETTE["text"], font=("Segoe UI", 18, "bold"))
        style.configure("SubTitle.TLabel", background=PALETTE["bg"], foreground=PALETTE["muted"], font=("Segoe UI", 12, "bold"))
        style.configure("Badge.TLabel", background=PALETTE["warning"], foreground="#0b0f12", font=("Segoe UI", 10, "bold"), padding=(8, 3))

        # Buttons
        style.configure(
            "TButton",
            background=PALETTE["panel"],
            foreground=PALETTE["text"],
            font=("Segoe UI", 10),
            padding=(12, 6),
            borderwidth=0,
        )
        style.map(
            "TButton",
            background=[("active", PALETTE["accent"]), ("disabled", PALETTE["panel"])],
            foreground=[("active", "#ffffff"), ("disabled", PALETTE["muted"])],
        )

        # Checkboxes
        style.configure("TCheckbutton", background=PALETTE["bg"], foreground=PALETTE["text"], font=("Segoe UI", 10))
        style.map("TCheckbutton", foreground=[("disabled", PALETTE["muted"])])

        # Progress bar
        style.configure(
            "Horizontal.TProgressbar",
            troughcolor=PALETTE["panel"],
            bordercolor=PALETTE["border"],
            background=PALETTE["primary"],
            lightcolor=PALETTE["primary"],
            darkcolor=PALETTE["primary"],
        )

        # Score label
        style.configure("Score.TLabel", background=PALETTE["bg"], foreground=PALETTE["success"], font=("Segoe UI", 30, "bold"))

    def _build_layout(self):
        # Top status bar
        status_bar = ttk.Frame(self, style="Panel.TFrame")
        status_bar.pack(fill=tk.X, padx=14, pady=(14, 10))
        status_bar.configure(borderwidth=1)
        status_bar["padding"] = (12, 8)

        self.state_badge = ttk.Label(status_bar, text="Stopped", style="Badge.TLabel")
        self._set_badge(self.state_badge, "Stopped")
        self.state_badge.pack(side=tk.LEFT)

        self.learning_timer = ttk.Label(status_bar, text="Learn: --s", style="Muted.TLabel")
        self.learning_timer.pack(side=tk.LEFT, padx=12)

        # Title + controls row
        header = ttk.Frame(self)
        header.pack(fill=tk.X, padx=14, pady=(0, 12))

        ttk.Label(header, text="Guardio Live Monitoring", style="Title.TLabel").pack(side=tk.LEFT)

        controls = ttk.Frame(header)
        controls.pack(side=tk.RIGHT)
        self.start_button = ttk.Button(controls, text="Start Monitoring")
        self.start_button.pack(side=tk.LEFT, padx=6)
        self.reset_button = ttk.Button(controls, text="Reset Learning", state=tk.DISABLED)
        self.reset_button.pack(side=tk.LEFT, padx=6)
        self.clear_button = ttk.Button(controls, text="Clear Log")
        self.clear_button.pack(side=tk.LEFT, padx=6)

        # Content area (left metrics, right logs)
        content = ttk.Frame(self)
        content.pack(fill=tk.BOTH, expand=True, padx=14, pady=(0, 14))

        # Left column
        left = ttk.Frame(content)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        metrics = ttk.Frame(left, style="Panel.TFrame")
        metrics.pack(fill=tk.X, pady=(0, 10))
        metrics["padding"] = (12, 12)

        ttk.Label(metrics, text="Current Risk Score", style="SubTitle.TLabel").pack(anchor="w")
        self.risk_score_label = ttk.Label(metrics, text="0", style="Score.TLabel")
        self.risk_score_label.pack(anchor="w", pady=(4, 10))

        self.risk_bar = ttk.Progressbar(metrics, orient="horizontal", length=280, mode="determinate", maximum=10)
        self.risk_bar.pack(fill=tk.X)

        # Filters
        filters = ttk.Frame(left, style="Panel.TFrame")
        filters.pack(fill=tk.X)
        filters["padding"] = (12, 12)

        ttk.Label(filters, text="Filter alerts", style="SubTitle.TLabel").pack(anchor="w", pady=(0, 6))
        self.chk_move = ttk.Checkbutton(filters, text="Movement")
        self.chk_type = ttk.Checkbutton(filters, text="Typing")
        self.chk_app = ttk.Checkbutton(filters, text="App Usage")
        self.chk_move.pack(anchor="w")
        self.chk_type.pack(anchor="w")
        self.chk_app.pack(anchor="w")

        # Right column (logs)
        right = ttk.Frame(content)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        log_panel = ttk.Frame(right, style="Panel.TFrame")
        log_panel.pack(fill=tk.BOTH, expand=True)
        log_panel["padding"] = (12, 12)

        ttk.Label(log_panel, text="Anomaly Alerts", style="SubTitle.TLabel").pack(anchor="w", pady=(0, 6))

        self.log_area = scrolledtext.ScrolledText(
            log_panel,
            height=18,
            wrap=tk.WORD,
            font=("Consolas", 10),
            background=PALETTE["input_bg"],
            foreground=PALETTE["text"],
            insertbackground=PALETTE["text"],
            borderwidth=1,
            relief="solid",
        )
        self.log_area.pack(fill=tk.BOTH, expand=True)
        self.log_area.configure(state="disabled")

        # Wire clear
        self.clear_button.config(command=self._clear_log)

    # Helpers
    def _set_badge(self, widget, state: str):
        color = {
            "Stopped": PALETTE["muted"],
            "Learning": PALETTE["warning"],
            "Monitoring": PALETTE["success"],
        }.get(state, PALETTE["muted"])
        widget.configure(text=state, background=color, foreground="#0b0f12", borderwidth=0)

    # Public API used from main.py
    def set_state(self, state: str):
        self._set_badge(self.state_badge, state)

    def set_learning_seconds(self, seconds_remaining: int):
        self.learning_timer.configure(text=f"Learn: {max(0, seconds_remaining):>2}s")

    def update_risk_score(self, score: int):
        # Numeric label
        self.risk_score_label.config(text=str(score))
        # Bar and color (clamp bar to 0..10)
        self.risk_bar["value"] = min(max(score, 0), 10)
        if score > 10:
            fg = PALETTE["danger"]
        elif score > 5:
            fg = PALETTE["warning"]
        else:
            fg = PALETTE["success"]
        self.risk_score_label.config(foreground=fg)

    def add_log_message(self, message: str):
        # Basic in-UI filter by message prefix
        if message.startswith("[ALERT] Movement") and not self._chk(self.chk_move):
            return
        if message.startswith("[ALERT] Typing") and not self._chk(self.chk_type):
            return
        if message.startswith("[ALERT] AppUsage") and not self._chk(self.chk_app):
            return

        self.log_area.configure(state="normal")
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.configure(state="disabled")

    def _chk(self, chk: ttk.Checkbutton) -> bool:
        # Infer selected state from ttk state flags
        return "selected" in chk.state()

    def _clear_log(self):
        self.log_area.configure(state="normal")
        self.log_area.delete(1.0, tk.END)
        self.log_area.configure(state="disabled")
