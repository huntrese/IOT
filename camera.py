import cv2
import subprocess

# Camera index (0 = default camera)
CAMERA_INDEX = 0

# Your RTSP server URL (must exist!)
RTSP_URL = "rtsp://localhost:8554/mystream"

# Open the camera
cap = cv2.VideoCapture(CAMERA_INDEX)

# Define ffmpeg command to push to RTSP
ffmpeg_cmd = [
    'ffmpeg',
    '-y',
    '-f', 'rawvideo',
    '-vcodec', 'rawvideo',
    '-pix_fmt', 'bgr24',
    '-s', f"{int(cap.get(3))}x{int(cap.get(4))}",  # width x height
    '-r', '25',  # frames per second
    '-i', '-',  # Input from stdin
    '-c:v', 'libx264',
    '-preset', 'veryfast',
    '-f', 'rtsp',
    '-rtsp_transport', 'tcp',  # Use TCP transport for more stable connections
    RTSP_URL
]

# Start ffmpeg subprocess
process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

print(f"🚀 Streaming camera feed to {RTSP_URL}")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ Failed to grab frame")
            break

        # Write frame to ffmpeg stdin
        process.stdin.write(frame.tobytes())

except KeyboardInterrupt:
    print("🛑 Stopping stream...")

finally:
    cap.release()
    process.stdin.close()
    process.wait()
