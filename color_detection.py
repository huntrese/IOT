import numpy as np
import cv2
import json
import time
from camera_read import *


def color_detection_stream():
    for success, imageFrame in read_stream():
        if not success:
            break
        
        # Convert the imageFrame in BGR to HSV color space
        hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
        
        # Set range for red color and define mask
        red_lower = np.array([136, 87, 111], np.uint8)
        red_upper = np.array([180, 255, 255], np.uint8)
        red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)
        
        # Set range for green color and define mask
        green_lower = np.array([25, 52, 72], np.uint8)
        green_upper = np.array([102, 255, 255], np.uint8)
        green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)
        
        # Set range for blue color and define mask
        blue_lower = np.array([94, 80, 2], np.uint8)
        blue_upper = np.array([120, 255, 255], np.uint8)
        blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)
        
        # Morphological Transform, Dilation for each color
        kernel = np.ones((5, 5), "uint8")
        red_mask = cv2.dilate(red_mask, kernel)
        green_mask = cv2.dilate(green_mask, kernel)
        blue_mask = cv2.dilate(blue_mask, kernel)
        
        detection_results = {
            "red": [],
            "green": [],
            "blue": [],
        }
        
        # Red color detection
        contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 300:
                x, y, w, h = cv2.boundingRect(contour)
                detection_results["red"].append({
                    "x": int(x),
                    "y": int(y),
                    "width": int(w),
                    "height": int(h),
                    "area": int(area)
                })
        
        # Green color detection
        contours, _ = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 300:
                x, y, w, h = cv2.boundingRect(contour)
                detection_results["green"].append({
                    "x": int(x),
                    "y": int(y),
                    "width": int(w),
                    "height": int(h),
                    "area": int(area)
                })
        
        # Blue color detection
        contours, _ = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 300:
                x, y, w, h = cv2.boundingRect(contour)
                detection_results["blue"].append({
                    "x": int(x),
                    "y": int(y),
                    "width": int(w),
                    "height": int(h),
                    "area": int(area)
                })
        
        # Convert detection results to JSON and yield as SSE
        json_data = json.dumps(detection_results)
        yield f'data: {json_data}\n\n'
        
        # Small delay to control frame rate
        time.sleep(0.05)
        
        
def color_detection_once():
    for success, imageFrame in read_stream():
        if not success:
            break
        
        detection_results = {
            "red": [],
            "green": [],
            "blue": [],
        }
        # Convert the imageFrame in BGR to HSV color space
        hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
        
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
                    detection_results[color_name].append({
                        "x": int(x),
                        "y": int(y),
                        "width": int(w),
                        "height": int(h),
                        "area": int(area)
                    })
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color_bgr, 2)
                    cv2.putText(frame, color_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color_bgr, 2)

        # Detect colors
        detect_color(red_mask, imageFrame, "red", (0, 0, 255))
        detect_color(green_mask, imageFrame, "green", (0, 255, 0))
        detect_color(blue_mask, imageFrame, "blue", (255, 0, 0))
        
        # Convert detection results to JSON and yield as SSE
        json_data = json.dumps(detection_results)
        return json_data