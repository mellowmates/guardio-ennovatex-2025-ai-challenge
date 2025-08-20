# src/agents/app_usage_agent.py
import time
import numpy as np
import subprocess
import platform

class AppUsageAgent:
    def __init__(self, anomaly_queue, poll_interval=1.0):
        self.anomaly_queue = anomaly_queue
        self.poll_interval = poll_interval
        self.is_learning = True
        self.history = []
        self.profile = {"top_apps": set(), "avg_switch_gap": 0, "std_switch_gap": 0}

    def _get_active_app_linux(self):
        try:
            win_id = subprocess.check_output(["xdotool", "getactivewindow"]).decode().strip()
            cls = subprocess.check_output(["xprop", "-id", win_id, "WM_CLASS"]).decode().strip()
            if "," in cls: return cls.split(",")[-1].strip().strip('"')
        except (subprocess.CalledProcessError, FileNotFoundError):
            return "unknown"
        return "unknown"

    def _learn_profile(self, learn_seconds=90): # <-- UPDATED
        print("[AppUsageAgent] Learning typical app usage for 90 seconds...")
        start_time, last_app, switch_gaps = time.time(), None, []
        while time.time() - start_time < learn_seconds:
            app = self._get_active_app_linux()
            if app and app != "unknown" and app != last_app:
                current_time = time.time()
                if last_app: switch_gaps.append(current_time - self.history[-1][0])
                self.history.append((current_time, app))
                last_app = app
            time.sleep(self.poll_interval)
        app_names = [name for _, name in self.history]
        if app_names: self.profile["top_apps"] = {name for name in app_names if app_names.count(name) > 1}
        if len(switch_gaps) > 1:
            self.profile["avg_switch_gap"] = np.mean(switch_gaps)
            self.profile["std_switch_gap"] = np.std(switch_gaps)
        self.is_learning = False
        self.history = []

    def _detect_anomaly(self):
        app = self._get_active_app_linux()
        if not app or app == "unknown": return
        if self.profile["top_apps"] and app not in self.profile["top_apps"]:
            self.anomaly_queue.put(f"[ALERT] AppUsage Anomaly: Unusual app in focus: '{app}'.")
        current_time = time.time()
        if self.history and app != self.history[-1][1] and self.profile["std_switch_gap"] > 0:
            gap = current_time - self.history[-1]
            if gap < (self.profile["avg_switch_gap"] - 3 * self.profile["std_switch_gap"]):
                self.anomaly_queue.put(f"[ALERT] AppUsage Anomaly: Rapid app switching detected.")
        if not self.history or app != self.history[-1][1]: self.history.append((current_time, app))
        if len(self.history) > 10: self.history.pop(0)

    def run(self, stop_event):
        self._learn_profile()
        print(f"[{self.__class__.__name__}] Now monitoring...")
        while not stop_event.is_set():
            self._detect_anomaly()
            if stop_event.wait(self.poll_interval):
                break
        print(f"[{self.__class__.__name__}] has stopped.")
