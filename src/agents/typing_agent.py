# agents/typing_agent.py
import time
import numpy as np
from pynput import keyboard

class TypingAgent:
    def __init__(self, anomaly_queue):
        self.anomaly_queue = anomaly_queue
        self.key_press_times = []
        self.last_press_time = time.time()
        self.is_learning = True
        self.learned_profile = {"mean_delay": 0, "std_dev_delay": 0}
        self.listener = keyboard.Listener(on_press=self._on_press)

    def _on_press(self, key):
        current_time = time.time()
        delay = current_time - self.last_press_time
        self.last_press_time = current_time
        if 0.01 < delay < 2.0:
            self.key_press_times.append(delay)
        if len(self.key_press_times) > 500:
            self.key_press_times.pop(0)
        if not self.is_learning:
            self._detect_anomaly(delay)

    def _learn_profile(self):
        print("[TypingAgent] Learning normal typing rhythm for 30 seconds...")
        time.sleep(30)
        if len(self.key_press_times) > 10:
            self.learned_profile["mean_delay"] = np.mean(self.key_press_times)
            self.learned_profile["std_dev_delay"] = np.std(self.key_press_times)
            print(f"[TypingAgent] Learning complete. Mean delay: {self.learned_profile['mean_delay']*1000:.2f} ms")
        else:
            print("[TypingAgent] Not enough typing to create a profile. Please type naturally.")
        self.is_learning = False
        self.key_press_times = []

    def _detect_anomaly(self, current_delay):
        if not self.learned_profile["std_dev_delay"] or not (0.01 < current_delay < 2.0):
            return
        mean = self.learned_profile["mean_delay"]
        std_dev = self.learned_profile["std_dev_delay"]
        if abs(current_delay - mean) > 3 * std_dev:
            report = f"[ALERT] Typing Anomaly: Unusual typing rhythm detected ({current_delay*1000:.2f} ms)."
            self.anomaly_queue.put(report)

    def run(self):
        self.listener.start()
        self._learn_profile()
        print("[TypingAgent] Now monitoring for anomalies...")

