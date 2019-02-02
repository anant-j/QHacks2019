import numpy as np
from video_recog import VideoRecognize
from traffic_controller import TrafficController

video = "data0.mp4"
graph = "frozen_inference_graph.pb"
videoGrab = VideoRecognize(video, graph)

controller = TrafficController([2, 0, 2, 0])

vehicleCounts = np.zeros(4)
peopleCounts = np.zeros(4)

videoGrab.startSess()
while (True):
    (vehicleCounts[0], peopleCounts[0]) = videoGrab.analyzeFrame()
    controller.updateCount(vehicleCounts, peopleCounts)
    controller.tick()
    print(controller.getLights())
    
videoGrab.stopSess()