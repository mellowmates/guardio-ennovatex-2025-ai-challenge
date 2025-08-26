# API Reference

## GuardioDashboard Class

Main dashboard interface for the Guardio application.

### Methods

#### `set_state(state: str)`
Updates the system monitoring status display.

**Parameters:**
- `state` (str): System state - "Stopped", "Monitoring", or "Learning"

**Example:**
```python
dashboard.set_state("Monitoring")
```

#### `set_agent_status(agent_name: str, status: str)`
Updates individual agent status indicators.

**Parameters:**
- `agent_name` (str): Agent identifier - "Movement", "Typing", or "AppUsage"  
- `status` (str): Status - "Idle", "Running", "Stable", "Adapting", "NoSignal", "Error"

**Example:**
```python
dashboard.set_agent_status("Typing", "Stable")
```

#### `update_agent_stats(agent_name: str, stats: dict)`
Updates agent statistical information display.

**Parameters:**
- `agent_name` (str): Agent identifier
- `stats` (dict): Statistics dictionary with keys: "mean", "std", "z", "note"

**Example:**
```python
stats = {"mean": 0.150, "std": 0.025, "z": 2.1, "note": "Stable"}
dashboard.update_agent_stats("Typing", stats)
```

#### `update_risk_score(score: int)`
Updates the security risk score display and progress indicator.

**Parameters:**
- `score` (int): Risk score value (0-15)

**Example:**
```

dashboard.update_risk_score(5)

```

#### `update_typing_speed(wpm: float)`
Updates the live typing speed display.

**Parameters:**
- `wpm` (float): Words per minute value

**Example:**
```

dashboard.update_typing_speed(45.2)

```

#### `add_log_message(message: str)`
Adds a timestamped message to the activity log.

**Parameters:**
- `message` (str): Log message content

**Example:**
```

dashboard.add_log_message("[ALERT] Movement Anomaly (High): Erratic mouse pattern")

```

#### `toggle_theme()`
Switches between light and dark theme modes.

**Example:**
```

dashboard.toggle_theme()

```

## Agent Classes

### MovementAgent

Monitors and analyzes mouse movement patterns.

#### `__init__(anomaly_queue, stats_queue, sigma=3.0, cooldown=3.0)`
Initialize movement monitoring agent.

**Parameters:**
- `anomaly_queue` (Queue): Queue for anomaly notifications
- `stats_queue` (Queue): Queue for statistics updates
- `sigma` (float): Detection sensitivity threshold
- `cooldown` (float): Alert cooldown period in seconds

### TypingAgent

Analyzes keystroke dynamics and typing patterns.

#### `__init__(anomaly_queue, stats_queue, sigma=3.0, cooldown=3.0)`
Initialize typing pattern monitoring agent.

**Parameters:**
- Same as MovementAgent

#### Properties
- `typing_speed_wmp` (float): Current typing speed in words per minute

### AppUsageAgent

Monitors application focus and switching behavior.

#### `__init__(anomaly_queue, stats_queue, sigma=3.0, cooldown=3.0)`
Initialize application usage monitoring agent.

**Parameters:**
- Same as MovementAgent

## GuardioApp Class

Main application controller managing agents and UI coordination.

### Methods

#### `start_monitoring()`
Initiates all monitoring agents and begins behavioral profiling.

#### `stop_monitoring()`
Halts all monitoring activities and cleans up resources.

#### `reset_monitoring()`
Stops monitoring, clears learned profiles, and restarts the system.

#### `process_queues()`
Processes anomaly and statistics queues from active agents.

## Data Structures

### Anomaly Event
```

{
"source": str,      \# Agent name
"severity": str,    \# "Low", "Medium", "High"
"message": str      \# Descriptive message
}

```

### Statistics Update
```

{
"source": str,      \# Agent name
"mean": float,      \# Current mean value
"std": float,       \# Standard deviation
"z": float,         \# Z-score of latest observation
"note": str,        \# Current agent status
"wpm": float        \# Typing speed (TypingAgent only)
}

```

## Configuration Constants

```


# Sensitivity Levels

VERY_SENSITIVE = 1.0    \# Detects minor deviations
BALANCED = 3.0          \# Recommended default
RELAXED = 6.0           \# Only major anomalies

# Cooldown Periods (seconds)

IMMEDIATE = 0.0         \# No cooldown
BALANCED = 3.0          \# Recommended default
MINIMAL_ALERTS = 10.0   \# Maximum spacing

```

---

**Backend Integration by Vittal G B**  
**API Documentation by Dev Dream Team**
```
