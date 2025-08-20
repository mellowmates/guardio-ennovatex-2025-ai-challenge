import time
import math
import numpy as np
from pynput import mouse

class MovementAgent:
    def __init__(self, anomaly_queue, alpha=0.01):
        self.anomaly_queue = anomaly_queue
        self.positions = []
        self.listener = mouse.Listener(on_move=self._on_move)
        self.mean_speed = None
        self.var_speed = None
        self.count = 0
        self.alpha = alpha  # Learning rate for adaptation

    def update_profile(self, speed):
        """Continuously updates the behavioral profile using exponential moving averages"""
        if self.mean_speed is None:
            self.mean_speed = speed
            self.var_speed = 0
            self.count = 1
        else:
            self.count += 1
            delta = speed - self.mean_speed
            self.mean_speed += self.alpha * delta
            self.var_speed = (1 - self.alpha) * self.var_speed + self.alpha * (delta ** 2)

    def std_speed(self):
        """Returns current standard deviation of speeds"""
        if self.var_speed is None:
            return 0
        return self.var_speed ** 0.5

    def _on_move(self, x, y):
        """Handles mouse movement events"""
        t = time.time()
        self.positions.append({'x': x, 'y': y, 'time': t})
        if len(self.positions) > 200:
            self.positions.pop(0)
        self.detect_anomaly()

    def compute_speed(self):
        """Calculates current mouse movement speed"""
        if len(self.positions) < 2:
            return None
        p1, p2 = self.positions[-2], self.positions[-1]
        dist = math.sqrt((p2['x'] - p1['x'])**2 + (p2['y'] - p1['y'])**2)
        dt = p2['time'] - p1['time']
        if dt <= 0:
            return None
        return dist / dt

    def detect_anomaly(self):
        """Detects movement anomalies and continuously updates profile"""
        speed = self.compute_speed()
        if speed is None or speed < 0.1:
            return
        
        # Detect anomaly only if we have enough data
        if self.mean_speed is not None and self.std_speed() > 0 and self.count > 10:
            if abs(speed - self.mean_speed) > 3 * self.std_speed():
                severity = "High" if abs(speed - self.mean_speed) > 5 * self.std_speed() else "Medium"
                self.anomaly_queue.put(f"[ALERT] Movement Anomaly ({severity}): Speed {speed:.1f} vs normal {self.mean_speed:.1f}")
        
        # Always update profile for continuous learning
        self.update_profile(speed)

    def run(self, stop_event):
        self.listener.start()
        print("[MovementAgent] Starting adaptive monitoring...")
        stop_event.wait()
        self.listener.stop()
        print("[MovementAgent] Stopped.")
