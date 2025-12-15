import numpy as np
from scipy.spatial import distance

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]
MOUTH = [61, 291, 81, 178, 13, 14]

def _pts(lm, idx, w, h):
    return np.array([(lm[i].x * w, lm[i].y * h) for i in idx], dtype=np.float32)

def ear(eye):
    return (distance.euclidean(eye[1], eye[5]) +
            distance.euclidean(eye[2], eye[4])) / (2 * distance.euclidean(eye[0], eye[3]) + 1e-6)

def mar(mouth):
    return (distance.euclidean(mouth[2], mouth[3]) +
            distance.euclidean(mouth[4], mouth[5])) / (2 * distance.euclidean(mouth[0], mouth[1]) + 1e-6)

def compute(lm, w, h):
    le = _pts(lm, LEFT_EYE, w, h)
    re = _pts(lm, RIGHT_EYE, w, h)
    mo = _pts(lm, MOUTH, w, h)
    return (ear(le) + ear(re)) / 2, mar(mo)
