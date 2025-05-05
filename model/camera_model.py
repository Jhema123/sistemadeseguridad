import cv2

class CameraModel:
    def get_available_cameras(self, max_test=10):
        indexes = []
        for i in range(max_test):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    indexes.append(i)
                cap.release()
        return indexes

    def open_camera(self, index):
        return cv2.VideoCapture(index)