import cv2 as cv

img = cv.imread('C:/Users/delvi/Pictures/Screenshots/Screenshot(3)')

frontalface_haarcascade = 'C:/Users/delvi/source/repos/TrackingCam/TrackingCam/haarcascade_frontalface_default.xml'
profileface_haarcascade = 'C:/Users/delvi/source/repos/TrackingCam/TrackingCam/haarcascade_profileface.xml'
eye_haarcascade = 'C:/Users/delvi/source/repos/TrackingCam/TrackingCam/haarcascade_eye.xml'
upperbody_haarcascade = 'C:/Users/delvi/source/repos/TrackingCam/TrackingCam/haarcascade_upperbody.xml'

target1_cascade = cv.CascadeClassifier()
target2_cascade = cv.CascadeClassifier()

if not target1_cascade.load(frontalface_haarcascade):
    print('--(!)Error loading face cascade')
    exit(0)
if not target2_cascade.load(profileface_haarcascade):
    print('--(!)Error loading eyes cascade')
    exit(0)

targets = target1_cascade.detectMultiScale(img)
targets = target2_cascade.detectMultiScale(img)