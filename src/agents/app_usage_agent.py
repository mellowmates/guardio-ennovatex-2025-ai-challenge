import time
import subprocess

class AppUsageAgent:
    """
    Adaptive app-usage anomaly detector with rarity detection and rapid-switch timing profile.
    On Linux, requires xdotool + xprop; otherwise falls back gracefully and reports 'Error' status.
    """
    def __init__(self, anomaly_queue, stats_queue, sigma=3.0, cooldown=3.0):
        self.anomaly_queue = anomaly_queue
        self.stats_queue = stats_queue

        self.sigma = sigma
        self.cooldown = cooldown
        self.poll_interval = 2.0
        self.alpha = 0.01

        self.app_counts = {}
        self.history = []
        self.app_durations = {}  # Track how long each app is used
        self.usual_apps = set()  # Track commonly used apps

        self.mean_gap = None
        self.var_gap = None
        self.count = 0
        
        self.min_app_time = 5.0  # Minimum time to consider an app as "used"
        self.history_size = 100  # Increased history size for better pattern detection

        self._last_alert_ts = 0.0
        self._last_stat_ts = 0.0

        self._usable = self._check_tools()

    def _check_tools(self):
        def have(cmd):
            try:
                subprocess.check_output(["which", cmd], stderr=subprocess.DEVNULL)
                return True
            except Exception:
                return False
        return have("xdotool") and have("xprop")

    def _now(self):
        return time.time()

    def _active_app(self):
        if not self._usable:
            return None
        try:
            # Get window ID
            win_id = subprocess.check_output(["xdotool", "getactivewindow"]).decode().strip()
            
            # Get both window class and title
            cls = subprocess.check_output(["xprop", "-id", win_id, "WM_CLASS"]).decode("utf-8", "ignore").strip()
            title = subprocess.check_output(["xprop", "-id", win_id, "_NET_WM_NAME"]).decode("utf-8", "ignore").strip()
            
            # Extract the class name
            class_name = cls.split(",")[-1].strip().strip('"') if "," in cls else None
            
            # Extract the window title
            window_title = title.split("=")[-1].strip().strip('"') if "=" in title else None
            
            if class_name and window_title:
                # Combine class and a truncated version of title for better identification
                return f"{class_name}:{window_title[:50]}"
            elif class_name:
                return class_name
            
        except Exception as e:
            return None
        return None

    def _std_gap(self):
        return (self.var_gap ** 0.5) if self.var_gap is not None else 0.0

    def _update_gap_profile(self, gap):
        if self.mean_gap is None:
            self.mean_gap = gap
            self.var_gap = 0.0
            self.count = 1
        else:
            self.count += 1
            delta = gap - self.mean_gap
            self.mean_gap += self.alpha * delta
            self.var_gap = (1 - self.alpha) * self.var_gap + self.alpha * (delta ** 2)

    def _publish_stats(self, z=None, note=None):
        now = self._now()
        if now - self._last_stat_ts >= 1.0:
            self._last_stat_ts = now
            mean = self.mean_gap if self.mean_gap is not None else None
            std = self._std_gap() if self.mean_gap is not None else None
            self.stats_queue.put({
                "source": "AppUsage",
                "mean": mean,
                "std": std,
                "z": z,
                "note": note or ("Adapting" if self.count < 15 else "Stable")
            })

    def _detect(self):
        app = self._active_app()
        if not self._usable:
            self._publish_stats(note="Error")
            return
        if not app:
            self._publish_stats(note="NoSignal")
            return

        now = self._now()

        # Update app usage duration
        if self.history:
            last_app = self.history[-1][1]
            duration = now - self.history[-1][0]
            self.app_durations[last_app] = self.app_durations.get(last_app, 0) + duration
            
            # Add to usual apps if used for significant time
            if self.app_durations[last_app] > 300:  # 5 minutes total usage
                self.usual_apps.add(last_app)

        # Update app counts only if the app was used for minimum time
        if self.history and (now - self.history[-1][0]) >= self.min_app_time:
            self.app_counts[app] = self.app_counts.get(app, 0) + 1

        total = sum(self.app_counts.values())
        # Detect rare app usage, but only if it's not in usual_apps
        if (total > 30 and 
            self.app_counts.get(app, 0) <= 2 and 
            app not in self.usual_apps):
            if now - self._last_alert_ts >= self.cooldown:
                self._last_alert_ts = now
                self.anomaly_queue.put({
                    "source": "AppUsage", 
                    "severity": "High", 
                    "message": f"Rare app focused: '{app}'"
                })

        if self.history and app != self.history[-1][1]:
            gap = now - self.history[-1][0]
            z = None
            if self.mean_gap is not None and self._std_gap() > 1e-6 and self.count > 5:
                z = abs(gap - self.mean_gap) / max(self._std_gap(), 1e-6)
                if gap < (self.mean_gap - self.sigma * self._std_gap()):
                    if now - self._last_alert_ts >= self.cooldown:
                        self._last_alert_ts = now
                        self.anomaly_queue.put({"source": "AppUsage", "severity": "Medium", "message": f"Rapid switching (gap={gap:.2f}s)"})
            self._update_gap_profile(gap)
            self._publish_stats(z=z)
        else:
            self._publish_stats()
        # Update history with better management
        if not self.history or app != self.history[-1][1]:
            self.history.append((now, app))
            if len(self.history) > self.history_size:
                # Clean up old history entries
                old_time = now - (self.history_size * self.poll_interval)
                while self.history and self.history[0][0] < old_time:
                    self.history.pop(0)

    def run(self, stop_event):
        if not self._usable:
            self._publish_stats(note="Error")
        else:
            self._publish_stats(note="Adapting")

        while not stop_event.is_set():
            self._detect()
            if stop_event.wait(self.poll_interval):
                break
