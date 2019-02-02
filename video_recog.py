import numpy as np
import tensorflow as tf
import cv2

def getInfo(index):
    if (index == 1):
        return 'person'
    elif (index == 3):
        return 'car'
    elif (index == 8):
        return 'truck'


cap = cv2.VideoCapture("data0.mp4")

# Read the graph.
with tf.gfile.FastGFile('ssd_mobilenet_v1_coco_2018_01_28/frozen_inference_graph.pb', 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    
with tf.Session() as sess:
    # Restore session
    sess.graph.as_default()
    tf.import_graph_def(graph_def, name='')

    while (cap.isOpened()):
        # Read and preprocess an image.
        ret, img = cap.read()
        if (ret == False):
            break
        rows = img.shape[0]
        cols = img.shape[1]
        inp = cv2.resize(img, (300, 300))
        inp = inp[:, :, [2, 1, 0]]  # BGR2RGB
    
        # Run the model
        out = sess.run([sess.graph.get_tensor_by_name('num_detections:0'),
                        sess.graph.get_tensor_by_name('detection_scores:0'),
                        sess.graph.get_tensor_by_name('detection_boxes:0'),
                        sess.graph.get_tensor_by_name('detection_classes:0')],
                       feed_dict={'image_tensor:0': inp.reshape(1, inp.shape[0], inp.shape[1], 3)})
    
        #THE LAST ARRAY IN OUT IS THE LABELS!
    
        # Visualize detected bounding boxes.
        num_detections = int(out[0][0])
        for i in range(num_detections):
            classId = int(out[3][0][i])
            score = float(out[1][0][i])
            bbox = [float(v) for v in out[2][0][i]]
            if score > 0.3:
                x = bbox[1] * cols
                y = bbox[0] * rows
                right = bbox[3] * cols
                bottom = bbox[2] * rows
                cv2.rectangle(img, (int(x), int(y)), (int(right), int(bottom)), (125, 255, 51), thickness=2)
        cv2.imshow('TensorFlow MobileNet-SSD', img)
            
        
        personCount = 0
        bikeCount = 0
        carCount = 0
        motorcycleCount = 0
        busCount = 0
        truckCount = 0
        trafficCount = 0
        
        objCount = int(out[0][0])
        objList = out[3][0][:objCount]
        for i in range(objCount):
            if objList[i] == 1:
                personCount = personCount + 1
            elif objList[i] == 2:
                bikeCount = bikeCount + 1
            elif objList[i] == 3:
                carCount = carCount + 1
            elif objList[i] == 4:
                motorcycleCount = motorcycleCount + 1
            elif objList[i] == 6:
                busCount = busCount + 1
            elif objList[i] == 8:
                truckCount = truckCount + 1
            trafficCount = carCount + motorcycleCount + busCount + truckCount
        
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cv2.waitKey()
cv2.destroyAllWindows() 
                
                