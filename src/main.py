import cv2
from src.config import Config
from src.vision.face_mesh import FaceMeshDetector
from src.vision.metrics import compute
from src.state.smoothing import Smoother
from src.state.fatigue_logic import FatigueLogic
from src.state.calibration import Calibrator
from src.alerts.alert_controller import AlertController
from src.alerts.sound import play
from src.alerts.overlay import draw

cap = cv2.VideoCapture(Config.CAMERA_INDEX)
mesh = FaceMeshDetector()

ear_s = Smoother()
mar_s = Smoother()

logic = FatigueLogic(window_seconds=20.0)
cal = Calibrator(seconds=3.0)

alerts = AlertController()

while cap.isOpened():
    ok, frame = cap.read()
    if not ok:
        break

    h, w = frame.shape[:2]
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    res = mesh.process(rgb)

    if res.multi_face_landmarks:
        lm = res.multi_face_landmarks[0].landmark
        ear, mar = compute(lm, w, h)

        ear = ear_s.update(ear)
        mar = mar_s.update(mar)

        # 1) Calibration phase (first 3 seconds with a face)
        if not cal.done:
            cal.update(ear)
            cv2.putText(frame, "Calibrating... keep neutral & look forward",
                        (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
            if cal.done:
                logic.set_calibration(cal.baseline)
        else:
            # 2) Fatigue inference (PERCLOS + yawn episodes)
            out = logic.update(ear=ear, mar=mar, mar_threshold=Config.MAR_THRESHOLD)
            level = out["level"]

            # 3) Alert throttling + sound
            fired = alerts.update(score=level * 3.0)  # map levels into controller scoring
            draw(frame, score=out["perclos"]*10.0, level=level)  # show perclos*10 as "score"

            # Debug overlay (helps tuning)
            cv2.putText(frame, f"PERCLOS:{out['perclos']:.2f} Yawns:{out['yawns']} EARthr:{out['ear_thr']:.2f}",
                        (20, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)

            if fired is not None and level >= 2:
                play(level)

    else:
        cv2.putText(frame, "NO FACE", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,255), 2)

    cv2.imshow(Config.WINDOW_NAME, frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
