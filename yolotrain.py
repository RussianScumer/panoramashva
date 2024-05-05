from ultralytics import YOLO

# Load a model
model = YOLO('last.pt')  # build a new model from scratch

model('7.jpg')
