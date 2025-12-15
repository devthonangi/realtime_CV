import cv2

def draw(frame, score, level):
    labels = ["NORMAL", "WARNING", "DROWSY", "CRITICAL"]
    colors = [(0,255,0), (0,165,255), (0,140,255), (0,0,255)]

    cv2.putText(
        frame,
        f"{labels[level]} | Fatigue: {score:.1f}/10",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        colors[level],
        2
    )
