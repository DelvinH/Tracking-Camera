#imports
import cv2 as cv
import detect
import comm_arduino
import globals


#variablesq
cam = 1
exposure = 27.5

min_pan = 0
max_pan = 180
target_pan = 90

min_tilt = 90
max_tilt = 170
target_tilt = 150

face_detected = False
target_locked = True
max_target_distance = 80

pan_sensitivity = 0.2
tilt_sensitivity = 0.3





port = 'COM3' #port arduino is connected to

#functions

def record():
    ret, frame = cap.read()

    # Display the resulting frame
    processed = detect.detect(frame, max_target_distance)
    
    if (not processed[4]):             #if face found and is not locked in
        face_detected, frame, distance_x, distance_y, target_locked = processed
    else:
        face_detected = False
        frame = processed[1]
        distance_x = 0
        distance_y = 0
        target_locked = False
        
    return [face_detected, frame, distance_x, distance_y, target_locked]
    
def move_cam(target_pan, target_tilt, distance_x, distance_y):
    target_pan += distance_x * -pan_sensitivity              #Larger degree = pans left
    if(target_pan > max_pan):
        target_pan = max_pan
    elif (target_pan < min_pan):
        target_pan = min_pan

    target_tilt += distance_y * -tilt_sensitivity               #Larger degree = tilts up
    if(target_tilt > max_tilt):
        target_tilt = max_tilt
    elif (target_tilt < min_tilt):
        target_tilt = min_tilt

    #print(target_tilt)
    #print(target_pan)
    return [target_pan, target_tilt]

def move_servos(arduino):
    servo_positions = "<" + str(int(target_pan)) + "," + str(int(target_tilt)) + ">"
    comm_arduino.send(arduino, servo_positions)



#script

cap = cv.VideoCapture(cam)
cap.set(cv.CAP_PROP_EXPOSURE, exposure)
arduino = comm_arduino.connect(port)
if arduino is None:
    print('--(!) Arduino failed to connect -- Break!')
    exit(0)

if not cap.isOpened:
    print('--(!)Error opening video capture')
    exit(0)

while(True):
    # Capture frame-by-frame
    face_detected, frame, distance_x, distance_y, target_locked = record()
    if frame is None:
        print('--(!) No captured frame -- Break!')
        break

    #Calculate camera movement
    target_pan, target_tilt = move_cam(target_pan, target_tilt, distance_x, distance_y)

    #Move servos
    try:
        move_servos(arduino)
    except:
        print('Arduino Disconnected -- Attempting to reconnect')
        arduino = comm_arduino.connect(port)
        

    #Terminate if q is pressed
    cv.imshow('frame', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()