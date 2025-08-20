# src/main.py
import queue
import threading
import tkinter as tk
from agents import MovementAgent, TypingAgent, AppUsageAgent
from dashboard import GuardioDashboard

class GuardioApp:
    def __init__(self, root: GuardioDashboard):
        self.root = root
        self.anomaly_queue = queue.Queue()
        self.risk_score = 0
        self.agent_threads = []
        self.stop_event = None

        self.root.start_button.config(command=self.start_monitoring)
        self.root.reset_button.config(command=self.reset_monitoring)
        self.root.clear_button.config(command=self.root._clear_log)

    def start_monitoring(self):
        self.root.start_button.config(state=tk.DISABLED)
        self.root.reset_button.config(state=tk.DISABLED)
        self.root.set_state("Monitoring")  # No learning phase - immediate monitoring
        self.root.add_log_message("[System] Starting adaptive monitoring agents...")

        self.stop_event = threading.Event()
        agents = [MovementAgent(self.anomaly_queue), TypingAgent(self.anomaly_queue), AppUsageAgent(self.anomaly_queue)]
        
        for agent in agents:
            thread = threading.Thread(target=agent.run, args=(self.stop_event,), daemon=True)
            thread.start()
            self.agent_threads.append(thread)

        self.process_queue()
        self.root.after(2000, lambda: self.root.reset_button.config(state=tk.NORMAL) if self.stop_event and not self.stop_event.is_set() else None)

    def stop_monitoring(self):
        if self.stop_event:
            self.root.add_log_message("[System] Stopping all agents...")
            self.stop_event.set()
            for thread in self.agent_threads:
                thread.join(timeout=1.0)
            self.agent_threads = []
            self.stop_event = None
            self.root.set_state("Stopped")
            self.root.start_button.config(state=tk.NORMAL)
            self.root.reset_button.config(state=tk.DISABLED)

    def reset_monitoring(self):
        self.root.reset_button.config(state=tk.DISABLED)
        self.stop_monitoring()
        self.risk_score = 0
        self.root.update_risk_score(self.risk_score)
        self.root._clear_log()
        self.start_monitoring()

    def process_queue(self):
        try:
            while True:
                message = self.anomaly_queue.get_nowait()
                # Enhanced scoring based on severity
                if "High" in message:
                    self.risk_score += 3
                elif "Medium" in message:
                    self.risk_score += 2
                else:
                    self.risk_score += 1
                    
                self.root.update_risk_score(self.risk_score)
                self.root.add_log_message(message)
                
                if self.risk_score > 15:
                    self.root.add_log_message("!!! CRITICAL RISK LEVEL - POTENTIAL SECURITY BREACH !!!")
                    self.risk_score = 0
        except queue.Empty:
            pass
        if not self.stop_event or not self.stop_event.is_set():
            self.root.after(100, self.process_queue)

if __name__ == "__main__":
    dashboard = GuardioDashboard()
    app = GuardioApp(dashboard)
    dashboard.mainloop()
