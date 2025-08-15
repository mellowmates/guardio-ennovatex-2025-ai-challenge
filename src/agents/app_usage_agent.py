# agents/app_usage_agent.py
import time
import psutil
import numpy as np
import subprocess
import platform

class AppUsageAgent:
    def __init__(self, anomaly_queue, poll_interval=1.0):
        self.anomaly_queue = anomaly_queue
        self.poll_interval = poll_interval
        self.is_learning = True
        self.history = []
        self.profile = {
            "top_apps": set(),
            "avg_switch_gap": 0,
            "std_switch_gap": 0
        }

    def _get_active_app_linux(self):
        try:
            win_id = subprocess.check_output(["xdotool", "getactivewindow"]).decode().strip()
            cls = subprocess.check_output(["xprop", "-id", win_id, "WM_CLASS"]).decode().strip()
            if "," in cls:
                app_name = cls.split(",")[-1].strip().strip('"')
                return app_name
        except (subprocess.CalledProcessError, FileNotFoundError):
            return "unknown"
        return "unknown"

    def _learn_profile(self, learn_seconds=30):
        print("[AppUsageAgent] Learning typical app usage for 30 seconds...")
        start_time = time.time()
        last_app = None
        switch_gaps = []

        while time.time() - start_time < learn_seconds:
            app = self._get_active_app_linux()
            if app and app != "unknown":
                if app != last_app:
                    current_time = time.time()
                    if last_app is not None:
                        switch_gaps.append(current_time - self.history[-1][0])
                    self.history.append((current_time, app))
                    last_app = app
            time.sleep(self.poll_interval)

        if self.history:
            app_names = [name for _, name in self.history]
            self.profile["top_apps"] = {name for name in app_names if app_names.count(name) > 1}
        
        if len(switch_gaps) > 1:
            self.profile["avg_switch_gap"] = np.mean(switch_gaps)
            self.profile["std_switch_gap"] = np.std(switch_gaps)
        
        print(f"[AppUsageAgent] Learning complete. Common apps: {self.profile['top_apps']}")
        self.is_learning = False
        self.history = []

    def _detect_anomaly(self):
        app = self._get_active_app_linux()
        if not app or app == "unknown":
            return
        current_time = time.time()

        if self.profile["top_apps"] and app not in self.profile["top_apps"]:
            report = f"[ALERT] AppUsage Anomaly: Unusual app in focus: '{app}'."
            self.anomaly_queue.put(report)

        if self.history and app != self.history[-1][1]:
            gap = current_time - self.history[-1][0]
            if self.profile["std_switch_gap"] > 0:
                if gap < (self.profile["avg_switch_gap"] - 3 * self.profile["std_switch_gap"]):
                    report = f"[ALERT] AppUsage Anomaly: Rapid app switching detected ({gap:.2f}s)."
                    self.anomaly_queue.put(report)
        
        if not self.history or app != self.history[-1][1]:
            self.history.append((current_time, app))
        if len(self.history) > 10:
            self.history.pop(0)

    def run(self):
        self._learn_profile()
        print("[AppUsageAgent] Now monitoring for anomalies...")
        while True:
            try:
                self._detect_anomaly()
                time.sleep(self.poll_interval)
            except KeyboardInterrupt:
                break
