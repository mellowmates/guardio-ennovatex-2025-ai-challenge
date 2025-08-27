import time
from pynput import keyboard

class TypingAgent:
    def __init__(self, anomaly_queue, stats_queue, alpha=0.01, sigma=3.0, cooldown=3.0):
        self.anomaly_queue = anomaly_queue
        self.stats_queue = stats_queue
        self.last_ts = time.time()
        self.alpha = alpha
        self.sigma = sigma
        self.cooldown = cooldown
        self.mean_delay = None
        self.var_delay = None
        self.count = 0
        self._last_alert_ts = 0.0
        self._last_stat_ts = 0.0
        self.total_chars = 0
        self.start_time = time.time()
        self.last_activity_time = time.time()
        self.wpm_samples = []
        self.typing_speed_wpm = 0
        self.window_size = 60
        self.char_timestamps = []
        self.listener = keyboard.Listener(on_press=self._on_press)

    def _calculate_wpm(self):
        now = time.time()
        
        while self.char_timestamps and (now - self.char_timestamps[0]) > self.window_size:
            self.char_timestamps.pop(0)
        
        if not self.char_timestamps or (now - self.char_timestamps[-1]) > 5:
            return 0
            
        chars_in_window = len(self.char_timestamps)
        window_duration = min(self.window_size, now - self.char_timestamps[0]) / 60
        
        if window_duration > 0:
            wpm = (chars_in_window / 5) / window_duration
            return wpm
        return 0

    def _update_wpm(self):
        current_wpm = self._calculate_wpm()
        self.wpm_samples.append(current_wpm)
        
        if len(self.wpm_samples) > 5:
            self.wpm_samples.pop(0)
        
        weights = [0.1, 0.15, 0.2, 0.25, 0.3][:len(self.wpm_samples)]
        total_weight = sum(weights)
        
        self.typing_speed_wpm = sum(w * s for w, s in zip(weights, self.wpm_samples)) / total_weight

    def _now(self):
        return time.time()

    def _std(self):
        return (self.var_delay ** 0.5) if self.var_delay is not None else 0.0

    def _update_profile(self, value):
        if self.mean_delay is None:
            self.mean_delay = value
            self.var_delay = 0.0
            self.count = 1
        else:
            self.count += 1
            delta = value - self.mean_delay
            self.mean_delay += self.alpha * delta
            self.var_delay = (1 - self.alpha) * self.var_delay + self.alpha * (delta ** 2)

    def _publish_stats(self, z=None, note=None):
        now = self._now()
        if now - self._last_stat_ts >= 0.5:
            self._last_stat_ts = now
            mean = self.mean_delay if self.mean_delay is not None else None
            std = self._std() if self.mean_delay is not None else None
            self.stats_queue.put({
                "source": "Typing",
                "mean": mean,
                "std": std,
                "z": z,
                "note": note or ("Adapting" if self.count < 30 else "Stable"),
                "wpm": self.typing_speed_wpm
            })

    def _on_press(self, key):
        now = self._now()
        delay = now - self.last_ts
        self.last_ts = now

        if hasattr(key, 'char') and key.char is not None:
            self.total_chars += 1
            self.char_timestamps.append(now)
            self._update_wpm()

        if self.typing_speed_wpm > 80:
            if now - self._last_alert_ts >= self.cooldown:
                self._last_alert_ts = now
                self.anomaly_queue.put({
                    "source": "Typing",
                    "severity": "High",
                    "message": f"Unusual Speed Detected: {self.typing_speed_wpm:.0f} WPM"
                })

        if 0.01 < delay < 2.0:
            z = None
            if self.mean_delay is not None and self._std() > 1e-6 and self.count > 10:
                z = abs(delay - self.mean_delay) / max(self._std(), 1e-6)
                if z > self.sigma:
                    if now - self._last_alert_ts >= self.cooldown:
                        self._last_alert_ts = now
                        sev = "High" if z > (self.sigma + 2.0) else "Medium"
                        self.anomaly_queue.put({
                            "source": "Typing",
                            "severity": sev,
                            "message": f"Delay {delay*1000:.0f}ms, z={z:.2f}"
                        })

            self._update_profile(delay)
            self._publish_stats(z=z)
        else:
            self._publish_stats(z=None, note="NoSignal")

    def run(self, stop_event):
        self.listener.start()
        self._publish_stats(z=None, note="Adapting")
        while not stop_event.is_set():
            time.sleep(0.05)
        self.listener.stop()