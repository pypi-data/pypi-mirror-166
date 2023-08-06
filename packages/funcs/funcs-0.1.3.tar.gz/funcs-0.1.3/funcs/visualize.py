import numpy as np
import cv2


def draw_bboxes(image: np.array, boxes: np.array, labels: np.array = None, prelabel_text: str = ''):
    """
    Draws rectangles on the image.

    Args:
        image (np.array): image to draw rectangles on
        boxes (np.array): boxes to draw, each row should be in the format of (x1, y1, x2, y2, ... any other info)
        labels (np.array): label to type in the top left corner of each box
        prelabel_text (str): string to prepend to box label when visualizing

    Returns:
        image (np.array): image with rectangles drawn on it
    """
    img = image.copy()
    boxes = boxes.astype('int32')

    for i in range(boxes.shape[0]):
        box = boxes[i, :4]
        cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
        if labels is not None:
            cv2.putText(img, prelabel_text + str(labels[i]), (box[0], box[1]),
                        cv2.FONT_HERSHEY_SIMPLEX, .7, (255, 0, 0), 2)

    return img
