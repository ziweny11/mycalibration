import depthai as dai
import cv2
import os
import uuid

# Prepare video file
output_dir = "videos"
os.makedirs(output_dir, exist_ok=True)
filename = f"vid_{uuid.uuid4().hex[:6]}.mp4"
filepath = os.path.join(output_dir, filename)

# Create pipeline
pipeline = dai.Pipeline()
cam = pipeline.create(dai.node.ColorCamera) 
cam.setBoardSocket(dai.CameraBoardSocket.CAM_A)
cam.setResolution(dai.ColorCameraProperties.SensorResolution.THE_720_P)  # 🔽 lower res
cam.setInterleaved(False)
cam.setColorOrder(dai.ColorCameraProperties.ColorOrder.BGR)

xout = pipeline.create(dai.node.XLinkOut)
xout.setStreamName("video")
cam.video.link(xout.input)  # ⬅️ keep this link correct

# Start device
with dai.Device(pipeline) as device:
    print(f"✅ Recording started. Saving to {filepath}")
    queue = device.getOutputQueue("video", maxSize=4, blocking=False)

    frame = queue.get().getCvFrame()
    height, width = frame.shape[:2]

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(filepath, fourcc, 30.0, (width, height))

    while True:
        frame = queue.get().getCvFrame()
        writer.write(frame)
        cv2.imshow("Recording - Press 'q' to stop", frame)
        if cv2.waitKey(1) == ord('q'):
            break

    writer.release()
    cv2.destroyAllWindows()
    print(f"📁 Video saved to {filepath}")
