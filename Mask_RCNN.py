import cv2
import numpy as np

# Settings
conf_thresh = 0.5

# Loading Mask RCNN
net = cv2.dnn.readNetFromTensorflow("dnn/frozen_inference_graph.pb",
                                    "dnn/mask_rcnn_inception_v2_coco_2018_01_28.pbtxt")

# Generate random colors
colors = np.random.randint(0,255,(80,3))


# Load image
img = cv2.imread("images/road_2.jpg")
height, width, _ = img.shape

# Create black image
black_image = np.zeros((height, width, 3), np.uint8)


# Detect objects
blob = cv2.dnn.blobFromImage(img, swapRB=True)
net.setInput(blob)
boxes, masks = net.forward(["detection_out_final", "detection_masks"])
detection_count = boxes.shape[2]

for i in range(detection_count):
    box = boxes[0, 0, i]
    class_id = box[1]
    score = box[2]
    if score < conf_thresh:
        continue

    # Get box coordinates
    x1 = int(box[3] * width)
    y1 = int(box[4] * height)
    x2 = int(box[5] * width)
    y2 = int(box[6] * height)

    roi = black_image[y1:y2,x1:x2]
    roi_height, roi_width, _ = roi.shape

    # Get the mask
    mask = masks[i, int(class_id)]
    mask = cv2.resize(mask, dsize=(roi_width, roi_height))
    _, mask = cv2.threshold(mask,thresh=0.5, maxval=255, type=cv2.THRESH_BINARY)


    cv2.rectangle(img, pt1=(x1,y1), pt2=(x2,y2), color=(255,0,0), thickness=2)

    # Get mask coordinates
    contours, _ = cv2.findContours(np.array(mask, np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    color = colors[int(class_id)]
    for cnt in contours:
        cv2.fillPoly(roi, [cnt], (int(color[0]), int(color[1]), int(color[2])))

#seg_img = cv2.bitwise_and(img, black_image)
seg_img = cv2.addWeighted(img,1.0,black_image,0.4,0)

cv2.imshow("Image", img)
cv2.imshow("black image", black_image)
cv2.imshow("segmentation", seg_img)

cv2.waitKey(0)