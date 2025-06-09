import cv2
import numpy as np
import glob
import os

# ====== USER SETTINGS ======
image_folder = "captures"  # Folder with calibration images
checkerboard_size = (9, 6)  # (width, height) inner corners
square_size = 0.025  # in meters
save_file = "camera_calib.npz"  # Output .npz file
# ============================

# Prepare known 3D points in checkerboard coordinate system
objp = np.zeros((checkerboard_size[0] * checkerboard_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0 : checkerboard_size[0], 0 : checkerboard_size[1]].T.reshape(
    -1, 2
)
objp *= square_size

objpoints = []  # 3D points in real world
imgpoints = []  # 2D points in image

images = glob.glob(os.path.join(image_folder, "*.jpg")) + glob.glob(
    os.path.join(image_folder, "*.png")
)

print(f"Found {len(images)} images")

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect corners
    ret, corners = cv2.findChessboardCorners(gray, checkerboard_size, None)

    if ret:
        objpoints.append(objp)
        refined_corners = cv2.cornerSubPix(
            gray,
            corners,
            (11, 11),
            (-1, -1),
            criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001),
        )
        imgpoints.append(refined_corners)
        print(f"✔️ Corners found in {os.path.basename(fname)}")
    else:
        print(f"❌ Skipping {os.path.basename(fname)} (no corners found)")

# Run calibration
ret, K, dist, rvecs, tvecs = cv2.calibrateCamera(
    objpoints, imgpoints, gray.shape[::-1], None, None
)

print("\n=== Calibration Results ===")
print("RMS reprojection error:", ret)
print("Camera Matrix (K):\n", K)
print("Distortion Coefficients:\n", dist.ravel())

# Save to file
np.savez(save_file, K=K, dist=dist, rvecs=rvecs, tvecs=tvecs)
print(f"\n📁 Calibration saved to {save_file}")
