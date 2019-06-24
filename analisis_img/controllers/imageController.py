import cv2
import matplotlib
from matplotlib import colors
from matplotlib import pyplot as plt
import numpy as np

from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import argparse
import imutils

savePath = "arduino/static/"

def save_file(image, fname):
    cv2.imwrite(savePath+fname, image)

def color_filter(fname):

	objColor = {"colorRatio": 0, "brightnessRatio": 0}

	def show(image):
		plt.figure(figsize=(15, 15))
		plt.imshow(image, interpolation='nearest')

	def show_hsv(hsv):
		rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
		show(rgb)

	def show_mask(mask):
		plt.figure(figsize=(10, 10))
		plt.imshow(mask, cmap='gray')

	def overlay_mask(mask, image):
		rgb_mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
		img = cv2.addWeighted(rgb_mask, 0.5, image, 0.5, 0)
		return img

	def find_biggest_contour(image):
		image = image.copy()
		contours, hierarchy = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
		contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
		biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]
		mask = np.zeros(image.shape, np.uint8)
		cv2.drawContours(mask, [biggest_contour], -1, 255, -1)
		return biggest_contour, mask

	def circle_countour(image, countour):
		image_with_ellipse = image.copy()
		ellipse = cv2.fitEllipse(countour)
		cv2.ellipse(image_with_ellipse, ellipse, (0,255,0), 2)
		return image_with_ellipse


	image = cv2.imread(fname)

	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	max_dimension = max(image.shape)
	scale = 700/max_dimension
	image = cv2.resize(image, None, fx=scale,fy=scale)

	image_blur = cv2.GaussianBlur(image, (7, 7), 0)
	image_blur_hsv = cv2.cvtColor(image_blur, cv2.COLOR_RGB2HSV)

	# filter by color
	min_red = np.array([0, 100, 80])
	max_red = np.array([10, 256, 256])
	mask1 = cv2.inRange(image_blur_hsv, min_red, max_red)
	print("color red mask", mask1)

	res = cv2.bitwise_and(image_blur_hsv, image_blur_hsv, mask=mask1)
	ratio = cv2.countNonZero(mask1)/(image_blur_hsv.size/3)
	objColor["colorRatio"] = ratio
	print('pixel percentage:', np.round(ratio*100, 2))

	# filter by brightness
	min_red = np.array([170, 100, 80])
	max_red = np.array([180, 256, 256])
	mask2 = cv2.inRange(image_blur_hsv, min_red, max_red)
	print("color red bright", mask2)

	mask = mask1 + mask2

	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
	mask_closed = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
	mask_clean = cv2.morphologyEx(mask_closed, cv2.MORPH_OPEN, kernel)

	# Extract biggest bounding box
	big_contour, red_mask = find_biggest_contour(mask_clean)
	print('big', big_contour, 'red', red_mask)
	# Apply mask
	overlay = overlay_mask(red_mask, image)
	# Draw bounding box
	circled = circle_countour(overlay, big_contour)
	# # show(circled)
	save_file(circled, "color.jpg")

	# plt.show()
	return objColor
#color_filter

def size_filter(fname):

	_width = 2 #cm
	lstObjs = list()

	def midpoint(ptA, ptB):
		return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

	# construct the argument parse and parse the arguments
	# ap = argparse.ArgumentParser()
	# ap.add_argument("-i", "--image", required=True,
	# 	help="path to the input image")
	# ap.add_argument("-w", "--width", type=float, required=True,
	# 	help="width of the left-most object in the image (in inches)")
	# args = vars(ap.parse_args())

	# load the image, convert it to grayscale, and blur it slightly
	#image = cv2.imread(args["image"])
	image = cv2.imread(fname)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (7, 7), 0)

	# perform edge detection, then perform a dilation + erosion to
	# close gaps in between object edges
	edged = cv2.Canny(gray, 50, 100)
	edged = cv2.dilate(edged, None, iterations=1)
	edged = cv2.erode(edged, None, iterations=1)

	# find contours in the edge map
	cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)

	# sort the contours from left-to-right and initialize the
	# 'pixels per metric' calibration variable
	(cnts, _) = contours.sort_contours(cnts)
	pixelsPerMetric = None

	orig = image.copy()
	# loop over the contours individually
	for c in cnts:
		# if the contour is not sufficiently large, ignore it
		if cv2.contourArea(c) < 100:
			continue

		# compute the rotated bounding box of the contour
		# orig = image.copy()
		box = cv2.minAreaRect(c)
		box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
		box = np.array(box, dtype="int")

		# order the points in the contour such that they appear
		# in top-left, top-right, bottom-right, and bottom-left
		# order, then draw the outline of the rotated bounding
		# box
		box = perspective.order_points(box)
		cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)

		# loop over the original points and draw them
		for (x, y) in box:
			cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)

		# unpack the ordered bounding box, then compute the midpoint
		# between the top-left and top-right coordinates, followed by
		# the midpoint between bottom-left and bottom-right coordinates
		(tl, tr, br, bl) = box
		(tltrX, tltrY) = midpoint(tl, tr)
		(blbrX, blbrY) = midpoint(bl, br)

		# compute the midpoint between the top-left and top-right points,
		# followed by the midpoint between the top-righ and bottom-right
		(tlblX, tlblY) = midpoint(tl, bl)
		(trbrX, trbrY) = midpoint(tr, br)

		# draw the midpoints on the image
		cv2.circle(orig, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
		cv2.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
		cv2.circle(orig, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
		cv2.circle(orig, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)

		# draw lines between the midpoints
		cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
			(255, 0, 255), 2)
		cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
			(255, 0, 255), 2)

		# compute the Euclidean distance between the midpoints
		dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
		dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

		# if the pixels per metric has not been initialized, then
		# compute it as the ratio of pixels to supplied metric
		# (in this case, inches)
		if pixelsPerMetric is None:
			pixelsPerMetric = dB / _width

		# compute the size of the object
		dimA = dA / pixelsPerMetric
		dimB = dB / pixelsPerMetric

		objSize = {"dimA": dimA, "dimB": dimB}
		print( "objSize", objSize)
		lstObjs.append(objSize)
		# draw the object sizes on the image
		cv2.putText(orig, "{:.1f}cm".format(dimA),
			(int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,
			0.65, (255, 255, 255), 2)
		cv2.putText(orig, "{:.1f}cm".format(dimB),
			(int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,
			0.65, (255, 255, 255), 2)

		# show the output image
		# cv2.imshow("Image", orig)
		# cv2.waitKey(0)

	save_file(orig, "lenght.jpg")
	return lstObjs
#size_filter