import cv2 as cv
import math
import globals

margin = 70



font_pos = (10, 470) #bottom left corner
font = cv.FONT_HERSHEY_PLAIN
font_scale = 1
font_gap = 15

x_pixels_to_deg = 12
y_pixels_to_deg = 12

#cascade paths
frontalface_haarcascade = 'C:/Users/delvi/source/repos/TrackingCam/TrackingCam/haarcascade_frontalface_default.xml'
profileface_haarcascade = 'C:/Users/delvi/source/repos/TrackingCam/TrackingCam/haarcascade_profileface.xml'
eye_haarcascade = 'C:/Users/delvi/source/repos/TrackingCam/TrackingCam/haarcascade_eye.xml'
upperbody_haarcascade = 'C:/Users/delvi/source/repos/TrackingCam/TrackingCam/haarcascade_upperbody.xml'

#load cascades
target1_cascade = cv.CascadeClassifier()
target2_cascade = cv.CascadeClassifier()

if not target1_cascade.load(frontalface_haarcascade):
    print('--(!)Error loading face cascade')
    exit(0)
if not target2_cascade.load(profileface_haarcascade):
    print('--(!)Error loading eyes cascade')
    exit(0)

def detect(frame, max_target_distance):
    cv.rectangle(frame, (0, 480), (160, 410), (255, 255, 255), -1)    #text background
    
    #frame count
    globals.frame = globals.frame + 1
    cv.putText(frame, 'Frame:' + str(globals.frame), (font_pos[0], font_pos[1] - 3 * font_gap), font, font_scale, (0, 0, 0), 1)

    #reset target if lost
    if globals.frames_not_tracking > globals.frames_not_tracking_max:
        globals.first_tracking = False
    
    #process frame
    try:
        frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        frame_gray = cv.equalizeHist(frame_gray)
    except:
        return [False, frame, 0, 0, False]
    
    
    #-- Detect targets
    targets = target1_cascade.detectMultiScale(frame_gray)     #look for targets
    globals.target2 = False
    #if no target1 found, try finding target2
    if len(targets) < 1:
        targets = target2_cascade.detectMultiScale(frame_gray)
        globals.target2 = True


    height, width, channels = frame.shape
    cv.circle(frame, (int(width/2), int(height/2)), int(max_target_distance) , (255, 255, 255), 2)    #draw lock-on circle
    

    if len(targets) >= 1: #if target(s) detected
        if globals.target2 is False:
            cv.putText(frame, 'Front view', (font_pos[0], font_pos[1] - 2 * font_gap), font, font_scale, (0, 0, 0), 1)  
        else:
            cv.putText(frame, 'Side view', (font_pos[0], font_pos[1] - 2 * font_gap), font, font_scale, (0, 0, 0), 1) 


        targets = list(targets)[0] #if several targets found use the first one
        x = targets[0]
        y = targets[1]
        w = targets[2]
        h = targets[3]

        


        center_target_x = int(x + w / 2)
        center_target_y = int(y + h / 2)
        
        if globals.first_tracking is False:
            globals.last_x = center_target_x
            globals.last_y = center_target_y
            globals.first_tracking = True

        distance_from_center_x = (center_target_x - width/2) / x_pixels_to_deg 
        distance_from_center_y = (center_target_y - height/2) / y_pixels_to_deg

        target_distance = math.sqrt((distance_from_center_x * x_pixels_to_deg)**2 + (distance_from_center_y * y_pixels_to_deg)**2) # calculate distance between image center and target center

        if target_distance < max_target_distance :#set added geometry colour
            locked = True
            lock_color = (0, 255, 0)

        else:
            locked = False
            lock_color = (0, 0, 255)
            
        cv.putText(frame, 'LockedOn: ' + str(locked), (font_pos[0], font_pos[1] - 0 * font_gap), font, font_scale, lock_color, 1)    


        cv.rectangle(frame,(center_target_x - 10, center_target_y), (center_target_x + 10, center_target_y),    #draw first line of the cross
                      lock_color, 2)
        cv.rectangle(frame,(center_target_x, center_target_y - 10), (center_target_x, center_target_y + 10),    #draw second line of the cross
                      lock_color,2)
        
        #if the last target position is too far from current one (i.e. incorrect reading), ignore reading
        if (abs(globals.last_x - center_target_x) > margin or abs(globals.last_y - center_target_y) > margin) :
            globals.frames_not_tracking = globals.frames_not_tracking + 1   #lost track of target
            track_color = (255, 0, 0)
            cv.circle(frame, (int(globals.last_x), int(globals.last_y)), int(10) , track_color, 2)    #not tracking
            cv.putText(frame, 'Tracking: False', (font_pos[0], font_pos[1] - 1 * font_gap), font, font_scale, track_color, 1)
            return [False, frame, 0, 0, locked]
        track_color = (0, 255, 0)
        cv.circle(frame, (int(globals.last_x), int(globals.last_y)), int(10) , track_color, 2)    #draw last location
        cv.putText(frame, 'Tracking: True', (font_pos[0], font_pos[1] - 1 * font_gap), font, font_scale, track_color, 1)
        
        
        #update globals
        globals.last_x = center_target_x
        globals.last_y = center_target_y
        globals.frames_not_tracking = 0
        
        #cv.imshow('Capture - Target detection', frame)
        return [True, frame, distance_from_center_x, distance_from_center_y, locked]

    else:
        globals.frames_not_tracking = globals.frames_not_tracking + 1   #lost track of target
        cv.putText(frame, 'No face detected', (font_pos[0], font_pos[1] - 2 * font_gap), font, font_scale, (0, 0, 0), 1)
        cv.putText(frame, 'Tracking: False', (font_pos[0], font_pos[1] - 1 * font_gap), font, font_scale, (255, 0, 0), 1)
        cv.putText(frame, 'LockedOn: False', (font_pos[0], font_pos[1] - 0 * font_gap), font, font_scale, (0, 0, 255), 1)
        return [False, frame, 0, 0, False]
    






