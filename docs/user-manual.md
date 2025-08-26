# Guardio User Manual

## Getting Started

Welcome to Guardio! This guide will help you understand and effectively use our adaptive anomaly detection system.

## Interface Overview

### Samsung One UI Dashboard
Guardio features a professional dashboard inspired by Samsung's One UI design language, providing:
- **Clean, modern interface** with intuitive controls
- **Real-time monitoring displays** for system status
- **Configurable settings** for personalized security
- **Light/Dark theme support** for comfortable viewing

## Core Features

### 1. Monitoring Controls
- **Start Monitoring**: Begin behavioral profiling and anomaly detection
- **Stop Monitoring**: Halt all detection activities
- **Reset System**: Clear learned profiles and restart learning
- **Clear Log**: Remove activity history from display

### 2. Configuration Settings
- **Sensitivity Slider** (1.0σ - 6.0σ): Adjust detection threshold
- **Alert Cooldown** (0-10 seconds): Control notification frequency
- **Theme Toggle**: Switch between light and dark modes

### 3. Live Monitoring
- **Risk Score**: Real-time security level indicator (0-15 scale)
- **Agent Status**: Individual monitoring component status
- **Typing Speed**: Live WPM calculation and categorization
- **Activity Log**: Timestamped system events and alerts

## Step-by-Step Usage

### Initial Setup
1. Launch Guardio application
2. Review default settings (3.0σ sensitivity, 3.0s cooldown)
3. Adjust theme preference if desired
4. Click "START MONITORING" to begin

### During Monitoring
1. **Normal Usage**: Continue regular computer activities
2. **Status Observation**: Monitor agent status indicators
3. **Alert Response**: Review any anomaly notifications
4. **Setting Adjustment**: Modify sensitivity/cooldown as needed

### Customization Options

#### Sensitivity Levels
- **1.0σ - 2.0σ**: High sensitivity (more alerts, catches subtle anomalies)
- **3.0σ**: Balanced (recommended default setting)
- **4.0σ - 6.0σ**: Lower sensitivity (fewer false positives)

#### Alert Cooldown
- **0s**: Immediate alerts (may cause notification spam)
- **3s**: Balanced (recommended default)
- **10s**: Minimal alerts (only persistent anomalies)

## Understanding Alerts

### Risk Levels
- **SECURE (0-3)**: Normal behavior, no concerns
- **MODERATE (4-7)**: Minor deviations detected
- **ELEVATED (8-11)**: Unusual activity patterns
- **CRITICAL (12-15)**: Significant anomalies detected

### Agent Status Indicators
- **IDLE**: System stopped, no monitoring
- **ACTIVE**: Currently monitoring and learning
- **STABLE**: Established behavioral baseline
- **LEARNING**: Adapting to pattern changes
- **NO DATA**: Insufficient activity for analysis

## Privacy and Security

### Data Protection
- **100% Local Processing**: No data leaves your device
- **No Network Communication**: Complete offline operation
- **Temporary Storage Only**: No persistent behavioral data
- **User Control**: Full control over all monitoring activities

### What We Monitor
- **Typing Patterns**: Keystroke timing and rhythm (not content)
- **Mouse Movement**: Velocity and trajectory patterns
- **App Usage**: Focus switching behavior (not app content)

### What We DON'T Monitor
- **Keystrokes Content**: No logging of actual typed text
- **Screen Content**: No screenshots or visual monitoring  
- **Network Activity**: No internet traffic analysis
- **File Access**: No monitoring of file operations

## Troubleshooting

### Common Issues
1. **No Alerts Appearing**: Increase sensitivity or ensure sufficient activity
2. **Too Many Alerts**: Decrease sensitivity or increase cooldown
3. **Agent Shows "NO DATA"**: Perform more of that activity type
4. **High CPU Usage**: Normal during initial learning phase

### Performance Optimization
- **Recommended Settings**: 3.0σ sensitivity, 3.0s cooldown
- **Learning Period**: Allow 5-10 minutes for baseline establishment
- **Regular Usage**: Consistent daily patterns improve accuracy

## Support

For technical support or questions:
- **GitHub Issues**: [https://github.com/mellowmates/Guardio/issues](https://github.com/mellowmates/Guardio/issues)
- **Documentation**: [https://github.com/mellowmates/Guardio/docs](https://github.com/mellowmates/Guardio/docs)

---

**UI Design by Sindhu B L**  
**Dev Dream Team - Samsung EnnovateX 2025**
```
