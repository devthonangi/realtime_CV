# RealtimeCV

Realtime computer vision–based driver monitoring system using OpenCV and MediaPipe.  
The system detects eye closure, yawning, and fatigue in real time and triggers natural,
escalating alerts — including continuous critical alarms.

---

## 🚗 Features

- Realtime face detection (MediaPipe FaceMesh)
- Eye closure detection (EAR)
- Yawning detection (MAR)
- PERCLOS-based fatigue estimation
- Temporal smoothing for natural behavior
- Driver-specific calibration
- Escalating alert levels:
  - Normal
  - Warning
  - Drowsy
  - **Critical (continuous alert)**
- Cross-platform sound alerts (macOS / Windows / Linux)
- Optimized for realtime performance

---

## 🧠 How It Works

The system combines multiple proven techniques used in driver monitoring research:

- **EAR (Eye Aspect Ratio)** for eye closure
- **MAR (Mouth Aspect Ratio)** for yawning
- **PERCLOS** (percentage of eye closure over time)
- Sliding time windows for stability
- Continuous alert loop for critical fatigue

Alerts escalate gradually and only stop once the driver recovers.

---

