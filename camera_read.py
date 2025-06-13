import numpy as np
import cv2


stream_url="rtsp://10.44.3.223:8554/stream"
# Kernel for morphological operations
kernel = np.ones((5, 5), np.uint8)

# Minimum contour area to reduce noise
MIN_AREA = 2000
def read_stream(rtsp_url=stream_url):
    video_capture = cv2.VideoCapture(rtsp_url)
    while(1):
        success, frame = video_capture.read()
        yield success, frame
if __name__ == "__main__":
    # Open webcam stream
    webcam = cv2.VideoCapture(stream_url)



    while True:
        success, imageFrame = webcam.read()
        if not success:
            break

        # Apply Gaussian Blur
        blurred = cv2.GaussianBlur(imageFrame, (11, 11), 0)

        # Convert BGR to HSV
        hsvFrame = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        # Red (dual range)
        red_lower = np.array([136, 87, 111], np.uint8)
        red_upper = np.array([180, 255, 255], np.uint8)

        # Green
        green_lower = np.array([40, 100, 100])
        green_upper = np.array([85, 255, 255])

        # Blue
        blue_lower = np.array([100, 150, 50])
        blue_upper = np.array([130, 255, 255])


        # Masks + Morphological opening
        red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)
        red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)
        red_mask = cv2.dilate(red_mask, kernel)

        green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)
        green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_OPEN, kernel)
        green_mask = cv2.dilate(green_mask, kernel)

        blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)
        blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_OPEN, kernel)
        blue_mask = cv2.dilate(blue_mask, kernel)

        # Color detection function
        def detect_color(mask, frame, color_name, color_bgr):
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > MIN_AREA:
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color_bgr, 2)
                    cv2.putText(frame, color_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color_bgr, 2)

        # Detect colors
        detect_color(red_mask, imageFrame, "Red", (0, 0, 255))
        detect_color(green_mask, imageFrame, "Green", (0, 255, 0))
        detect_color(blue_mask, imageFrame, "Blue", (255, 0, 0))

        # Show frame
        cv2.imshow("Color Detection", imageFrame)

        # Exit on 'q'
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    # Cleanup
    webcam.release()
    cv2.destroyAllWindows()
