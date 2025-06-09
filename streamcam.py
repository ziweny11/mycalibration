import depthai as dai
import cv2

# Create pipeline
pipeline = dai.Pipeline()

# Create color camera node
cam = pipeline.createColorCamera()
cam.setPreviewSize(640, 480)
cam.setInterleaved(False)
cam.setBoardSocket(dai.CameraBoardSocket.RGB)

# Output stream
xout = pipeline.createXLinkOut()
xout.setStreamName("video")
cam.preview.link(xout.input)

# Start device
with dai.Device(pipeline) as device:
    print("✅ Pipeline started. Press 'q' to quit.")
    video = device.getOutputQueue(name="video", maxSize=4, blocking=False)

    while True:
        frame = video.get().getCvFrame()
        cv2.imshow("OAK Camera Preview", frame)
        if cv2.waitKey(1) == ord("q"):
            break
