import cv2
from bs4 import BeautifulSoup
from pytesseract import pytesseract as pt

def get_coordinates(element_arr):
    """
    Get the coordinates of the bounding box

    Args:
        element_arr(list): List of bs4.element.Tag objects

    Returns:
        coordinates(list): 2D array containing coordinates in the form [x0, y0, x1, y1]
    """
    title_atrs = [element["title"].split(";") for element in element_arr]
    coordinates = [atr_value[0].split(" ")[1:] for atr_value in title_atrs]
    coordinates = [[int(x) for x in coordinate_arr] for coordinate_arr in coordinates]
    return coordinates

filename = 'test.png'

pt.run_tesseract(filename, 'output', lang="yid", extension="box", config="hocr")

hocr = open("output.hocr", "r", encoding="utf-8").read()

#extract coordinate information from hocr
soup = BeautifulSoup(hocr, "html.parser")
words = soup.find_all('span',class_='ocrx_word')
word_coordinates = get_coordinates(words)
lines = soup.find_all('span',class_='ocr_line')
line_coordinates = get_coordinates(lines)
paragraphs = soup.find_all('p',class_='ocr_par')
paragraph_coordinates = get_coordinates(paragraphs)


# Draw the bounding box
img = cv2.imread(filename)
boxes = pt.image_to_boxes(img)
h, w, _ = img.shape

for c in word_coordinates:
    img = cv2.rectangle(img,(int(c[0]),int(c[1])),(int(c[2]),int(c[3])),(255,0,0),2) #blue

for c in line_coordinates:
    img = cv2.rectangle(img,(int(c[0]),int(c[1])),(int(c[2]),int(c[3])),(0,0,255),2) #red

for c in paragraph_coordinates:
    img = cv2.rectangle(img,(int(c[0]),int(c[1])),(int(c[2]),int(c[3])),(255,255,0),2) #cyan

for b in boxes.splitlines():
    b = b.split(' ')
    img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2) #green

cv2.imshow('output',img)


