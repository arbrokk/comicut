import os
from pathlib import Path
import cv2
import argparse


def slice_image(source_image_path):
    base_path = os.path.dirname(source_image_path)
    image_name = source_image_path.stem
    image_suffix = source_image_path.suffix

    org  = cv2.imread(str(source_image_path))
    img = cv2.imread(str(source_image_path))

    # convert to RGB
    image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    ret,thresh = cv2.threshold(gray, 240,255, cv2.THRESH_BINARY_INV)

    contours,hierarchy = cv2.findContours(thresh, 1, 2)

    listCnt = [cnt for cnt in contours if cv2.boundingRect(cnt)[3]>img.shape[0]/5 and cv2.boundingRect(cnt)[3]<img.shape[0]]
    paneNumbers = len(listCnt)

    for cnt in listCnt:
        x,y,w,h = cv2.boundingRect(cnt)
        cv2.imwrite(f"{base_path}/{image_name}_p{paneNumbers}{image_suffix}", org[y:y+h, x:x+w])
        paneNumbers -= 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser("split_image")
    parser.add_argument("source_image_path", help="The source image that will be split", type=str)
    args = parser.parse_args()

    slice_image(Path(args.source_image_path), 2, 60)
