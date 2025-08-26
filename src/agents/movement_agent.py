import time
import math
from pynput import mouse

class MovementAgent:
    """
    Adaptive movement anomaly detector with exponential moving averages and cooldown.
    Publishes:
      - anomalies to anomaly_queue as dicts: {"source","severity","message"}
      - stats to stats_queue: {"source","mean","std","z","note"}
    """
    def __init__(self, anomaly_queue, stats_queue, sigma=3.0, cooldown=3.0):
        self.anomaly_queue = anomaly_queue
        self.stats_queue = stats_queue
        self.sigma = sigma
        self.cooldown = cooldown

        self.positions = []
        self.listener = mouse.Listener(on_move=self._on_move)

        self.mean_speed = None
        self.var_speed = None
        self.count = 0

        self.alpha = 0.01
        self.sigma = sigma
        self.cooldown = cooldown
        self._last_alert_ts = 0.0
        self._last_stat_ts = 0.0

    def _now(self):
        return time.time()

    def _on_move(self, x, y):
        t = self._now()
        self.positions.append({'x': x, 'y': y, 'time': t})
        if len(self.positions) > 200:
            self.positions.pop(0)
        self._step()

    def _speed(self):
        if len(self.positions) < 2:
            return None
        p1, p2 = self.positions[-2], self.positions[-1]
        dt = p2['time'] - p1['time']
        if dt <= 0:
            return None
        dx, dy = p2['x'] - p1['x'], p2['y'] - p1['y']
        dist = math.hypot(dx, dy)
        return dist / dt

    def _update_profile(self, value):
        if self.mean_speed is None:
            self.mean_speed = value
            self.var_speed = 0.0
            self.count = 1
        else:
            self.count += 1
            delta = value - self.mean_speed
            self.mean_speed += self.alpha * delta
            self.var_speed = (1 - self.alpha) * self.var_speed + self.alpha * (delta ** 2)

    def _std(self):
        return (self.var_speed ** 0.5) if self.var_speed is not None else 0.0

    def _publish_stats(self, z=None, note=None):
        now = self._now()
        if now - self._last_stat_ts >= 0.5:
            self._last_stat_ts = now
            mean = self.mean_speed if self.mean_speed is not None else None
            std = self._std() if self.mean_speed is not None else None
            self.stats_queue.put({
                "source": "Movement",
                "mean": mean,
                "std": std,
                "z": z,
                "note": note or ("Adapting" if self.count < 30 else "Stable")
            })

    def _step(self):
        spd = self._speed()
        if spd is None or spd < 0.1:
            self._publish_stats(z=None, note="NoSignal")
            return

        z = None
        if self.mean_speed is not None and self._std() > 1e-6 and self.count > 10:
            z = abs(spd - self.mean_speed) / max(self._std(), 1e-6)
            if z > self.sigma:
                now = self._now()
                if now - self._last_alert_ts >= self.cooldown:
                    self._last_alert_ts = now
                    sev = "High" if z > (self.sigma + 2.0) else "Medium"
                    self.anomaly_queue.put({
                        "source": "Movement",
                        "severity": sev,
                        "message": f"Speed {spd:.1f}, z={z:.2f}"
                    })

        self._update_profile(spd)
        self._publish_stats(z=z)

    def run(self, stop_event):
        self.listener.start()
        self._publish_stats(z=None, note="Adapting")
        while not stop_event.is_set():
            time.sleep(0.05)
        self.listener.stop()
