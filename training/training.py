from ultralytics import YOLO
model = YOLO ('yolov7-seg-1.pt')
model.predict(source=0, show=TRUE)
