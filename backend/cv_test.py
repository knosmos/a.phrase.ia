import cv2
import numpy as np

mat = cv2.imread("tmp.png")
grey = cv2.cvtColor(mat, cv2.COLOR_BGR2GRAY)

'''
# threshold
gray = cv2.cvtColor(img_cv, cv2.COLOR_RGB2GRAY)
ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

cv2.imshow("thresh", thresh)
cv2.waitKey()

# mask
mask = 255 - thresh

cv2.imshow("mask", mask)
cv2.waitKey()

#img_cv_masked = cv2.bitwise_and(img_cv, img_cv, mask=mask)
img_cv_masked = np.uint8(img_cv)
img_cv_masked[mask==0] = 255

cv2.imshow("masked", img_cv_masked)
cv2.waitKey()
'''

t1 = 80
t2 = 30
dilate_size = 5
erode_size = 6

canny = cv2.Canny(mat, 200, 100)
mask = cv2.dilate(canny, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (dilate_size, dilate_size)))
mask = cv2.erode(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (dilate_size, dilate_size)))

cv2.imshow("m", mask)
cv2.waitKey()

contours, _ = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
for cnt in contours:
    cv2.drawContours(mask, [cnt], 0, 255, -1)
mask = cv2.erode(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (erode_size, erode_size)))

img_cv_masked = np.uint8(mat)
img_cv_masked[mask==0] = 255
cv2.imshow("res", img_cv_masked)
cv2.waitKey()