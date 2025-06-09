import depthai as dai
import cv2
import os

# Output video config
output_dir = "videos"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "output.mp4")
fps = 30
frame_size = (1280, 720)

# Create pipeline
pipeline = dai.Pipeline()
cam = pipeline.createColorCamera()
cam.setPreviewSize(*frame_size)
cam.setInterleaved(False)
cam.setBoardSocket(dai.CameraBoardSocket.RGB)

xout = pipeline.createXLinkOut()
xout.setStreamName("video")
cam.preview.link(xout.input)

# Start device and recording
with dai.Device(pipeline) as device:
    print("⏺️ Recording started. Press 'q' to stop.")

    video_queue = device.getOutputQueue(name="video", maxSize=4, blocking=False)

    # Define MP4 writer
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(output_path, fourcc, fps, frame_size)

    while True:
        frame = video_queue.get().getCvFrame()
        writer.write(frame)  # Write to file
        cv2.imshow("Recording...", frame)  # Show live

        if cv2.waitKey(1) & 0xFF == ord("q"):
            print("🛑 Recording stopped.")
            break

    writer.release()
    cv2.destroyAllWindows()
    print(f"💾 Saved video to: {output_path}")
