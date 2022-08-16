from eaftbt.ExamDraft import compare_paths
from pathlib import Path
import cv2 as cv
import numpy as np
from deskew import determine_skew
from skimage.transform import rotate

def get_contours(img):
    contours, _ = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    return contours

def area_filter(contour, img_shape, expected_area_ratio, tolerance_ratio):
    img_area = img_shape[0]*img_shape[1]
    expected_area = img_area*expected_area_ratio
    tolerance = img_area*tolerance_ratio
    return abs(cv.contourArea(contour) - expected_area) <= tolerance

def draw_image(img):
    k = float(800)/float(img.shape[0])
    dim = (int(float(img.shape[0]) * k), int(float(img.shape[1]) * k))
    resized = cv.resize(img, dim, interpolation=cv.INTER_AREA)
    cv.imshow('image', resized)
    cv.waitKey(0)

def cut_out_rect_pieces(img_gray, contours, returns_extended_img=True):
    final_image = cv.cvtColor(no_background, cv.COLOR_GRAY2BGR)

    boxes = []
    for c in contours:
        (x, y, w, h) = cv.boundingRect(c)
        boxes.append([x, y, x + w, y + h])
    boxes = np.asarray(boxes)
    pieces = []
    for left, top, right, bottom in boxes:
        cv.rectangle(final_image, (left, top), (right, bottom), (255, 0, 0), 2)
        pieces.append(img_gray[top:bottom, left:right])
    if not returns_extended_img:
        return pieces
    return (pieces, final_image)

if __name__ == "__main__":
    path = f'{Path(__file__).parent / "data" / "sample-data" / "sample_exam_thick_photo.png"}'
    image = cv.imread(path)
    angle = determine_skew(image)
    rotated = cv.warpAffine(image, cv.getRotationMatrix2D(center=(image.shape[1]/2, image.shape[0]/2), angle=angle,scale=1), dsize=(image.shape[1], image.shape[0]))
    gray = cv.cvtColor(rotated, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray, (5, 5), 0)
    no_background = cv.adaptiveThreshold(blurred, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 13, 8)
    edged = cv.Canny(no_background, 30, 100)

    cnts, _ = cv.findContours(edged.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    filtered_cnts = [con for con in cnts if area_filter(con, edged.shape, 0.125, 0.05)]

    pieces, fin_img = cut_out_rect_pieces(no_background, filtered_cnts, returns_extended_img=True)
    draw_image(fin_img)

    # cv.imshow('', pieces[0])
    # cv.waitKey(0)