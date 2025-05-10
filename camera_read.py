import cv2

def read_stream(rtsp_url="rtsp://localhost:8554/stream"):
    video_capture = cv2.VideoCapture(rtsp_url)
    while(1):
        success, frame = video_capture.read()
        yield success, frame

if __name__ == "__main__":
    for success, frame in read_stream():
        cv2.imshow('VIDEO', frame)
        cv2.waitKey(1)