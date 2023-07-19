import cv2

frame = cv2.imread('D:\\objectdetection\\bus.jpg')
cv2.namedWindow('name', cv2.WINDOW_FREERATIO)

cv2.imshow('name', frame)
cv2.waitKey(0)

cv2.destroyAllWindows()
