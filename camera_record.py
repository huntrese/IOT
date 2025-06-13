import cv2
import subprocess
import socket

def get_local_ip():
    try:
        # Get the local machine's IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "0.0.0.0"

def start_stream(output_dir="stream", camera_index=0):
    # Open the camera
    cap = cv2.VideoCapture(camera_index)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))  # Use MJPEG codec for lower latency
    
    local_ip = get_local_ip()
    
    # Define ffmpeg command for HLS
    ffmpeg_cmd = [
        'ffmpeg',
        '-y',
        '-f', 'rawvideo',
        '-vcodec', 'rawvideo',
        '-pix_fmt', 'bgr24',
        '-s', f"{int(cap.get(3))}x{int(cap.get(4))}",
        '-r', '25',
        '-i', '-',
        '-c:v', 'libx264',
        '-preset', 'veryfast',
        '-hls_time', '2',
        '-hls_list_size', '5',
        '-hls_flags', 'delete_segments',
        '-f', 'hls',
        f'{output_dir}/stream.m3u8'  # This path must match the server's path
    ]

    # Start ffmpeg subprocess
    process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

    print(f"🚀 Streaming at http://{local_ip}:8000/stream.m3u8")  # Fixed URL path

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("⚠️ Failed to grab frame")
                break
            process.stdin.write(frame.tobytes())

    except KeyboardInterrupt:
        print("🛑 Stopping stream...")
    finally:
        cap.release()
        process.stdin.close()
        process.wait()

if __name__ == "__main__":
    start_stream()