import mediapipe as mp

class FaceMeshDetector:
    def __init__(self):
        self.mesh = mp.solutions.face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def process(self, rgb_frame):
        return self.mesh.process(rgb_frame)
