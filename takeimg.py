import depthai as dai
import cv2
import os

# Configuration
output_dir = "captures"
os.makedirs(output_dir, exist_ok=True)

# Create pipeline
pipeline = dai.Pipeline()
cam = pipeline.createColorCamera()
cam.setPreviewSize(1280, 720)
cam.setInterleaved(False)
cam.setBoardSocket(dai.CameraBoardSocket.RGB)

xout = pipeline.createXLinkOut()
xout.setStreamName("video")
cam.preview.link(xout.input)

# Start device
with dai.Device(pipeline) as device:
    print("📷 Press 'e' to capture, 'q' to quit.")
    video = device.getOutputQueue(name="video", maxSize=4, blocking=False)

    count = 0

    while True:
        frame = video.get().getCvFrame()
        cv2.imshow("OAK Camera Preview", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("e"):
            filename = os.path.join(output_dir, f"img_{count:04d}.jpg")
            cv2.imwrite(filename, frame)
            print(f"✔ Saved {filename}")
            count += 1

        elif key == ord("q"):
            print("🛑 Exiting.")
            break

    cv2.destroyAllWindows()
