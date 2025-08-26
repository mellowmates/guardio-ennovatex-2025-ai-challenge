import queue
import threading
import customtkinter as ctk
from agents.movement_agent import MovementAgent
from agents.typing_agent import TypingAgent
from agents.app_usage_agent import AppUsageAgent
from dashboard import GuardioDashboard

class GuardioApp:
    def __init__(self):
        self.root = GuardioDashboard()
        
        self.anomaly_queue = queue.Queue()
        self.stats_queue = queue.Queue()
        self.risk_score = 0
        self.agent_threads = []
        self.agents = []
        self.stop_event = None

        self.sensitivity_sigma = 3.0
        self.cooldown_seconds = 3.0

        self._setup_ui_connections()
        self.root.set_state("Stopped")
        self.root.set_agent_status("Movement", "Idle")
        self.root.set_agent_status("Typing", "Idle")
        self.root.set_agent_status("AppUsage", "Idle")

    def _setup_ui_connections(self):
        try:
            if hasattr(self.root, 'start_button'):
                self.root.start_button.configure(command=self.start_monitoring)
            
            if hasattr(self.root, 'stop_button'):
                self.root.stop_button.configure(command=self.stop_monitoring)
            
            if hasattr(self.root, 'reset_button'):
                self.root.reset_button.configure(command=self.reset_monitoring)
            
            if hasattr(self.root, 'clear_button'):
                self.root.clear_button.configure(command=self._clear_log)
            
            # Connect sliders if they exist
            if hasattr(self.root, 'sensitivity_scale'):
                self.root.sensitivity_scale.configure(command=self._on_sensitivity_changed)
            
            if hasattr(self.root, 'cooldown_scale'):
                self.root.cooldown_scale.configure(command=self._on_cooldown_changed)
                
        except Exception as e:
            print(f"Warning: Error connecting UI elements: {e}")

    def _on_sensitivity_changed(self, val):
        """Update sensitivity setting"""
        try:
            self.sensitivity_sigma = float(val)
            self.root.add_log_message(f"[System] Sensitivity updated to {self.sensitivity_sigma:.1f}σ")
            # Update running agents if they exist
            for agent in self.agents:
                if hasattr(agent, 'sigma'):
                    agent.sigma = self.sensitivity_sigma
        except Exception as e:
            print(f"Error updating sensitivity: {e}")

    def _on_cooldown_changed(self, val):
        """Update cooldown setting"""
        try:
            self.cooldown_seconds = float(val)
            self.root.add_log_message(f"[System] Cooldown updated to {self.cooldown_seconds:.1f}s")
            # Update running agents if they exist
            for agent in self.agents:
                if hasattr(agent, 'cooldown'):
                    agent.cooldown = self.cooldown_seconds
        except Exception as e:
            print(f"Error updating cooldown: {e}")

    def start_monitoring(self):
        """Start all monitoring agents"""
        try:
            # Update UI state safely
            if hasattr(self.root, 'start_button'):
                self.root.start_button.configure(state="disabled")
            if hasattr(self.root, 'stop_button'):
                self.root.stop_button.configure(state="normal")
            if hasattr(self.root, 'reset_button'):
                self.root.reset_button.configure(state="disabled")
            
            self.root.set_state("Monitoring")
            self.root.add_log_message("[System] Starting adaptive monitoring agents...")
            
            # Create stop event and agents
            self.stop_event = threading.Event()
            self.agents = [
                MovementAgent(self.anomaly_queue, self.stats_queue, 
                             sigma=self.sensitivity_sigma, cooldown=self.cooldown_seconds),
                TypingAgent(self.anomaly_queue, self.stats_queue, 
                           sigma=self.sensitivity_sigma, cooldown=self.cooldown_seconds),
                AppUsageAgent(self.anomaly_queue, self.stats_queue, 
                             sigma=self.sensitivity_sigma, cooldown=self.cooldown_seconds)
            ]

            # Start agent threads
            for agent in self.agents:
                thread = threading.Thread(target=agent.run, args=(self.stop_event,), daemon=True)
                thread.start()
                self.agent_threads.append(thread)

            # Update agent status
            self.root.set_agent_status("Movement", "Running")
            self.root.set_agent_status("Typing", "Running") 
            self.root.set_agent_status("AppUsage", "Running")

            # Start processing queues
            self.process_queues()

            # Enable reset after startup
            if hasattr(self.root, 'reset_button'):
                self.root.after(2000, lambda: self.root.reset_button.configure(state="normal")
                               if self.stop_event and not self.stop_event.is_set() else None)
                               
        except Exception as e:
            print(f"Error starting monitoring: {e}")
            self.root.add_log_message(f"[ERROR] Failed to start monitoring: {e}")

    def stop_monitoring(self):
        """Stop all monitoring agents"""
        try:
            if self.stop_event:
                self.root.add_log_message("[System] Stopping all agents...")
                self.stop_event.set()
                
                # Wait for threads to complete
                for thread in self.agent_threads:
                    thread.join(timeout=1.5)
                
                # Clean up
                self.agent_threads = []
                self.agents = []
                self.stop_event = None

                # Update UI state
                self.root.set_state("Stopped")
                self.root.set_agent_status("Movement", "Idle")
                self.root.set_agent_status("Typing", "Idle")
                self.root.set_agent_status("AppUsage", "Idle")

                if hasattr(self.root, 'start_button'):
                    self.root.start_button.configure(state="normal")
                if hasattr(self.root, 'stop_button'):
                    self.root.stop_button.configure(state="disabled")
                if hasattr(self.root, 'reset_button'):
                    self.root.reset_button.configure(state="disabled")
                
                # Reset typing speed display
                if hasattr(self.root, 'update_typing_speed'):
                    self.root.update_typing_speed(0)
                
                self.root.add_log_message("[System] All agents stopped.")
        except Exception as e:
            print(f"Error stopping monitoring: {e}")

    def reset_monitoring(self):
        """Reset system - stop, clear data, restart"""
        try:
            if hasattr(self.root, 'reset_button'):
                self.root.reset_button.configure(state="disabled")
            self.stop_monitoring()
            
            # Reset risk score and clear log
            self.risk_score = 0
            self.root.update_risk_score(self.risk_score)
            self._clear_log()
            
            # Restart monitoring
            self.root.add_log_message("[System] Resetting system...")
            self.root.after(500, self.start_monitoring)
        except Exception as e:
            print(f"Error resetting: {e}")

    def _clear_log(self):
        """Clear the log area"""
        try:
            self.root._clear_log()
        except Exception as e:
            print(f"Error clearing log: {e}")

    def process_queues(self):
        """Process anomaly and stats queues from agents"""
        try:
            # Process anomaly events
            while True:
                try:
                    event = self.anomaly_queue.get_nowait()
                    source = event.get("source", "Unknown")
                    severity = event.get("severity", "Low")
                    message = event.get("message", "")

                    # Update risk score based on severity
                    if severity == "High":
                        self.risk_score += 3
                    elif severity == "Medium":
                        self.risk_score += 2
                    else:
                        self.risk_score += 1

                    # Update UI
                    self.root.update_risk_score(self.risk_score)
                    self.root.add_log_message(f"[ALERT] {source} Anomaly ({severity}): {message}")

                    # Check for critical risk level
                    if self.risk_score > 15:
                        self.root.add_log_message("!!! CRITICAL RISK LEVEL - POTENTIAL SECURITY BREACH !!!")
                        self.risk_score = 0
                        self.root.update_risk_score(self.risk_score)

                except queue.Empty:
                    break
                    
            # Process agent statistics
            while True:
                try:
                    stats = self.stats_queue.get_nowait()
                    source = stats.get("source", "")
                    if source:
                        self.root.update_agent_stats(source, stats)
                        
                        # Update typing speed if available (FIXED TYPO)
                        if source == "Typing" and "wpm" in stats:
                            if hasattr(self.root, 'update_typing_speed'):
                                self.root.update_typing_speed(stats["wpm"])
                                
                except queue.Empty:
                    break

        except Exception as e:
            print(f"Error processing queues: {e}")

        # Continue polling if monitoring is active
        if not self.stop_event or not self.stop_event.is_set():
            self.root.after(100, self.process_queues)

    def run(self):
        """Run the application"""
        self.root.mainloop()

if __name__ == "__main__":
    # Create and run the application
    app = GuardioApp()
    app.run()
