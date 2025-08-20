# src/agents/movement_agent.py
import time
import math
import numpy as np
from pynput import mouse

class MovementAgent:
    def __init__(self, anomaly_queue):
        self.anomaly_queue = anomaly_queue
        self.positions = []
        self.is_learning = True
        self.learned_profile = {"mean_speed": 0, "std_dev_speed": 0}
        self.listener = mouse.Listener(on_move=self._on_move)

    def _on_move(self, x, y):
        self.positions.append({'x': x, 'y': y, 'time': time.time()})
        if len(self.positions) > 200: self.positions.pop(0)
        if not self.is_learning: self._detect_anomaly()

    def _calculate_speeds(self):
        speeds = []
        if len(self.positions) < 2: return speeds
        for i in range(1, len(self.positions)):
            p1, p2 = self.positions[i-1], self.positions[i]
            distance = math.sqrt((p2['x'] - p1['x'])**2 + (p2['y'] - p1['y'])**2)
            time_diff = p2['time'] - p1['time']
            if time_diff > 0.001: speeds.append(distance / time_diff)
        return speeds

    def _learn_profile(self):
        print("[MovementAgent] Learning normal mouse movement for 90 seconds...")
        time.sleep(90) # <-- UPDATED
        speeds = self._calculate_speeds()
        if len(speeds) > 10:
            self.learned_profile["mean_speed"] = np.mean(speeds)
            self.learned_profile["std_dev_speed"] = np.std(speeds)
        self.is_learning = False
        self.positions = []

    def _detect_anomaly(self):
        speeds = self._calculate_speeds()
        if not speeds or self.learned_profile["std_dev_speed"] == 0: return
        last_speed = speeds[-1]
        mean = self.learned_profile["mean_speed"]
        std_dev = self.learned_profile["std_dev_speed"]

        if last_speed < 0.1:
            return

        if abs(last_speed - mean) > 3 * std_dev:
            self.anomaly_queue.put(f"[ALERT] Movement Anomaly: Unusually high mouse speed detected ({last_speed:.2f}).")

    def run(self, stop_event):
        self.listener.start()
        self._learn_profile()
        print(f"[{self.__class__.__name__}] Now monitoring...")
        while not stop_event.is_set():
            time.sleep(0.5)
        self.listener.stop()
        print(f"[{self.__class__.__name__}] has stopped.")
