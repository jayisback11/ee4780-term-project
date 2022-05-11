import cv2 as cv
import time
import math

Conf_threshold = 0.4
NMS_threshold = 0.4
COLORS = [(0, 255, 0), (0, 0, 255), (255, 0, 0),
          (255, 255, 0), (255, 0, 255), (0, 255, 255)]

class_name = ["trashcan"]

net = cv.dnn.readNet('trashcan.weights', 'trashcan.cfg')
net.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA_FP16)

model = cv.dnn_DetectionModel(net)
model.setInputParams(size=(416, 416), scale=1/255, swapRB=True)

#FOR WEBCAM
#cap = cv.VideoCapture(0)
#cap.set(3, 1280)
#cap.set(4, 720)

#FOR CSI CAMERA
cap = cv.VideoCapture('nvarguscamerasrc ! video/x-raw(memory:NVMM), width=1640, height=1232, format=(string)NV12, framerate=(fraction)20/1 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink' , cv.CAP_GSTREAMER)

#FOR FPS. THIS IS NOT IMPORTANT FOR AUTONOMOUS DELIVERY. ONLY USE THIS IF YOU WANT TO SEE THE FPS OF THE DEVICE (JETSON NANO 4GB).
starting_time = time.time()
frame_counter = 0

while True:
    f = open("commands.txt", "r")

    if "ready" in f.read():
        ready = True
    else:
        ready = False

    f.close()

    ret, frame = cap.read()
    frame_counter += 1
    if ret == False:
        break
    classes, scores, boxes = model.detect(frame, Conf_threshold, NMS_threshold)
    for (classid, score, box) in zip(classes, scores, boxes):
        color = COLORS[int(classid) % len(COLORS)]
        label = "%s : %f" % (class_name, score)

        #calculate the center of detected object
        x = math.floor(abs((box[0]+box[0]+box[2])/2))
        y = math.floor(abs((box[1]+box[1]+box[3])/2))

        cv.rectangle(frame, box, color, 1)
        cv.circle(frame, (x, y), 3, color, -1)
        cv.putText(frame, label, (box[0], box[1]-10),
                   cv.FONT_HERSHEY_COMPLEX, 0.3, color, 1)

        #GREEN SQUARE AT THE CENTER OF THE VIDEO FEEDBACK
        #This will write the command to commands.txt and tell move.py where to move
        if ready:
            f = open("commands.txt", "w")

            if x < 743:
                time.sleep(1)
                f.write("LEFTcommand")
                print("ROLLING LEFT")
            elif x > 939:
                time.sleep(1)
                f.write("RIGHTcommand")
                print("ROLLING RIGHT")
            elif y < 239:
                time.sleep(1)
                f.write("FORWARDcommand")
                print("PITCHING FORWARD")
            elif y > 393:
                time.sleep(1)
                f.write("BACKWARDcommand")
                print("PITCHING BACKWARD")
            else:
                time.sleep(1)
                f.write("LANDcommand")
                print("DESCENDING")
                
            f.close()
        else:
            print("NOT YET READY: WAITING FOR DRONE...") # if not ready, then wait for the drone to finish the current command
        
    cv.rectangle(frame, (743, 239), (939, 393), (0, 255, 0), 1) # draw the green square at the center
    endingTime = time.time() - starting_time
    fps = frame_counter/endingTime
    # print(fps) #print the fps
    cv.putText(frame, f'FPS: {fps}', (20, 50),
               cv.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2) # create a text
    cv.imshow('frame', frame) # print the fps on the video feedback
    key = cv.waitKey(1)
    if key == ord('q'):
        break
cap.release()
cv.destroyAllWindows()
