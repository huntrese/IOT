import cv2
import subprocess

def start_stream(rtsp_url="rtsp://localhost:8554/stream", camera_index="http://10.44.3.130:8080/video"):
    # Open the camera
    cap = cv2.VideoCapture(camera_index)

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
        rtsp_url
    ]

    # Start ffmpeg subprocess
    process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

    print(f"🚀 Streaming camera feed to {rtsp_url}")

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

if __name__ == "__main__":
    start_stream()