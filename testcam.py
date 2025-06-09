import depthai

devices = depthai.Device.getAllConnectedDevices()
if not devices:
    print("❌ No DepthAI devices found.")
else:
    print("✅ Found devices:")
    for d in devices:
        print(d)
