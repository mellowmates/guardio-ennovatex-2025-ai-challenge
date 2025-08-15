# main.py
import queue
import threading
import time
from agents.movement_agent import MovementAgent
from agents.typing_agent import TypingAgent
from agents.app_usage_agent import AppUsageAgent

if __name__ == "__main__":
    print("Starting Guardio...")

    anomaly_queue = queue.Queue()
    risk_score = 0

    movement_agent = MovementAgent(anomaly_queue=anomaly_queue)
    typing_agent = TypingAgent(anomaly_queue=anomaly_queue)
    app_usage_agent = AppUsageAgent(anomaly_queue=anomaly_queue)

    movement_thread = threading.Thread(target=movement_agent.run, daemon=True)
    typing_thread = threading.Thread(target=typing_agent.run, daemon=True)
    app_thread = threading.Thread(target=app_usage_agent.run, daemon=True)
    
    movement_thread.start()
    typing_thread.start()
    app_thread.start()

    print("\nGuardio is running. All agents active.")
    print("Please use your computer normally for 30 seconds for baseline learning.")

    while True:
        try:
            anomaly_report = anomaly_queue.get() 
            print(anomaly_report)
            
            if "Movement" in anomaly_report:
                risk_score += 1
            elif "Typing" in anomaly_report:
                risk_score += 2
            elif "AppUsage" in anomaly_report:
                risk_score += 3
            
            print(f"--> Current Risk Score: {risk_score}")

            if risk_score > 10:
                print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print("!!! HIGH RISK SCORE DETECTED - POTENTIAL FRAUD !!!")
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
                risk_score = 0

        except KeyboardInterrupt:
            print("\nStopping Guardio. All threads will now exit.")
            break
        except Exception as e:
            print(f"An unexpected error occurred in the main loop: {e}")
            break
