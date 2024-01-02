from BasicParams import *
from Cvt2Gray import convertToGray
import cv2
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio


# Get the video. Count the number of the frames.
vid = cv2.VideoCapture(INPUT_FILE)
total_frame = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))


# Use 1 frame to get the points we want to track. Select the points manually.
_, old_frame = vid.read()


def mouseCallback(event, x, y, flags, userdata):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"({x}, {y})")
        INITIAL_POINTS.append([x, y])
        cv2.circle(old_frame, (x, y), 5, (0, 0, 255), -1)
        cv2.imshow(NAME_OF_INITIAL_FRAME, old_frame)


cv2.namedWindow(NAME_OF_INITIAL_FRAME, 0)
cv2.resizeWindow(NAME_OF_INITIAL_FRAME, 1920, 1080)
cv2.imshow(NAME_OF_INITIAL_FRAME, old_frame)
cv2.setMouseCallback(NAME_OF_INITIAL_FRAME, mouseCallback)
cv2.waitKey(0)
print(f"We choose {len(INITIAL_POINTS)} points to track.")

# Then we will start tracking these points
Displacement = np.zeros([total_frame - 2, len(INITIAL_POINTS)])
_, old_frame = vid.read()
frame = old_frame
features = np.float32(INITIAL_POINTS)
count = 2  # Count how many frames have been read.
x_label = np.array(range(Displacement.shape[0])) / FPS
while old_frame is not None:
    _, frame = vid.read()
    if frame is None:
        break
    count += 1

    nextPts, status, err = cv2.calcOpticalFlowPyrLK(old_frame, frame, features, None)
    # status = status[:, 0]
    # nextPts = nextPts[status == 1]
    # features = features[status == 1]
    Displacement[count - 3, :] = (nextPts - INITIAL_POINTS)[:, 1]

    label = 100 * count / total_frame
    if label % 20 == 0:
        print(f"Now finished {label}%...")
    if label >= 95:
        print("Done!")
        break  # Discard the last 5% frames

Displacement[:, 0] *= 250 / 40
Displacement[:, 1] *= 250 / 32
Displacement[:, 2] *= 250 / 31
Displacement[:, 3] *= 250 / 31  # These parameters are measured manually.

for i in range(1, len(INITIAL_POINTS) + 1):
    plt.subplot(2, 2, i)
    plt.title(f"Level_{i}")
    plt.xlabel("Time/s")
    plt.ylabel("Displacement/mm")
    plt.plot(x_label, Displacement[:, i - 1])
plt.show()

plt.plot(x_label, Displacement[:, 0])
plt.show()
sio.savemat("Result.mat", {"Displacement": Displacement})

vid.release()
