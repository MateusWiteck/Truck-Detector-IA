import cv2
import numpy as np
import time


def addElement(element, pile):  # Pile = [ 3 ,6,12 ,34 , 43 , 12] o primeiro elemento é o ultimo elemento da pilha
    i = len(pile) - 1
    if i > 12:
        i = 12
    while i > 0:
        pile[i] = pile[i - 1]
        i = i - 1
    pile[0] = element


# Cores para as classes:
COLORS = [(255, 255, 0), (255, 0, 0), (0, 255, 255), (255, 0, 255)]
contador = 0
TOTAL = 0
lastTime = 0
lastPicture = 0

class_names = []
with open("coco.names", "r") as f:
    class_names = [cname.strip() for cname in f.readlines()]

# img = cv2.imread("/home/mateusw/Área de Trabalho/OpenCV/img.jpg")
# Entrada
# capture = cv2.VideoCapture("video.mp4")
capture = cv2.VideoCapture("https://192.168.0.114:8080/video")

Net = cv2.dnn.readNet("yolov4-tiny.weights", "yolov4-tiny.cfg")

# Parametros da REDE ****
model = cv2.dnn_DetectionModel(Net)
model.setInputParams(size=(416, 416), scale=1 / 255)

isFrame = False
blackList = []
lastBoxes = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
for i in range(0, 10):
    success, frame = capture.read()
    Edframe = frame[150:, :600].copy()
    classes, scores, boxes = model.detect(Edframe, 0.1, 0.2)  # O que é 0.1 e 0.2 ???

    for (classid, score, box) in zip(classes, scores, boxes):
        actualTime = time.time()
        if class_names[classid[0]] == "truck" and  box is not blackList:
            contador = contador + 1
            lastTime = time.time()
            isFrame = True
            blackList.append(box)

        if contador == 20:
            contador = 0
            if actualTime - lastPicture > 3:
                TOTAL = TOTAL + 1
                cv2.imwrite("caminhao" + str(int(time.time())) + ".jpg", frame)
                lastPicture = time.time()
                print("saved" + "caminhao" + str(int(time.time())) + ".jpg")

        if actualTime - lastTime > 2:
            contador = 0

        #

        cor = COLORS[int(classid) % len(COLORS)]

        # texto
        label = f"{class_names[classid[0]]}: {int(score * 100)}%"
        cv2.rectangle(Edframe, box, cor, 1)

        cv2.putText(Edframe, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, cor, 2)

while True:
    success, frame = capture.read()

    # marca o inicio da deteccao
    start = time.time()

    # edita para reduzir o consumo:
    Edframe = frame[150:, :600].copy()

    # Deteccao:
    classes, scores, boxes = model.detect(Edframe, 0.1, 0.2)  # O que é 0.1 e 0.2 ???

    # imprimir caixas
    for (classid, score, box) in zip(classes, scores, boxes):
        actualTime = time.time()
        if class_names[classid[0]] == "truck":
            if box is not blackList:
                print(blackList)
                contador = contador + 1
                lastTime = time.time()
                isFrame = True
                if box is not lastBoxes:
                    blackList.append(box)
                else:
                    addElement(box, lastBoxes)
            else:
                print(" BlackList !")
        if contador == 20:
            contador = 0
            if actualTime - lastPicture > 3:
                TOTAL = TOTAL + 1
                cv2.imwrite("caminhao" + str(int(time.time())) + ".jpg", frame)
                lastPicture = time.time()
                print("saved" + "caminhao" + str(int(time.time())) + ".jpg")

        if actualTime - lastTime > 2:
            contador = 0

        #

        cor = COLORS[int(classid) % len(COLORS)]

        # texto
        label = f"{class_names[classid[0]]}: {int(score * 100)}%"
        cv2.rectangle(Edframe, box, cor, 1)

        cv2.putText(Edframe, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, cor, 2)

    if isFrame == False and contador > 0:
        contador = contador - 0.5
    end = time.time()

    fps_label = f"FPS: {round((1.0 / (end - start)), 2)}"

    cv2.putText(Edframe, fps_label, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 5)

    cv2.imshow("video", Edframe)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    if cv2.waitKey(1) & 0xFF == ord("s"):
        contador = 0
        TOTAL = TOTAL + 1
        cv2.imwrite("caminhao" + str(int(time.time())) + ".jpg", frame)
        print("saved")
print(TOTAL)
"""
celular = cv2.VideoCapture("https://192.168.0.114:8080/video")

while True:
    success, frame = celular.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow("video", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
"""
