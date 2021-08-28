import cv2
import time

# Operando com pilhas
def addElement(element, pile):  # Pile = [ 3 ,6,12 ,34 , 43 , 12] o primeiro elemento é o ultimo elemento da pilha
    i = len(pile) - 1
    if i > 12:
        i = 12
    while i > 0:
        pile[i] = pile[i - 1]
        i = i - 1
    pile[0] = element


# Aqui você pode mudar as cores que serão usadas para mostrar a detecção de objetos no promt
COLORS = [(255, 255, 0), (255, 0, 0), (0, 255, 255), (255, 0, 255)]


contador = 0
TOTAL = 0
lastTime = 0
lastPicture = 0
class_names = []
isFrame = False
blackList = []
blackCounter = 0
lastBoxes = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

# Arquivo de nomes do haarcascades vem aqui
with open("coco.names", "r") as f:
    class_names = [cname.strip() for cname in f.readlines()]


# Entrada de video, por padrão está uma câmera IP, caso queira entrar com um video:
# capture = cv2.VideoCapture("video.mp4")
capture = cv2.VideoCapture("https://192.168.0.114:8080/video")

# Leitura dos Arquivos de recohecimento de objetos
Net = cv2.dnn.readNet("yolov4-tiny.weights", "yolov4-tiny.cfg")

# Parametros da REDE ****
model = cv2.dnn_DetectionModel(Net)
model.setInputParams(size=(416, 416), scale=1 / 255)

# Quando a programa é inicializada ele ignora os caminões que já estavam inicialmente aparecendo na camera. Este for é o algoritimo para isso:
for i in range(0, 10):
    success, frame = capture.read()

    # Edita o frame para que o algoritimo não se preocupe com uma parte da imagem que não iria passar caminhões
    Edframe = frame[150:, :600].copy()
    # Detecta os Objetos
    classes, scores, boxes = model.detect(Edframe, 0.1, 0.2)  # O que é 0.1 e 0.2 ???

    # Percorre toda a detecção:
    for (classid, score, box) in zip(classes, scores, boxes):
        actualTime = time.time() # usado para calcular o fps

        # Objeto de interesse é o caminhão, ele "anota" que viu um
        if class_names[classid[0]] == "truck" and  box is not blackList:
            contador = contador + 1
            lastTime = time.time()
            isFrame = True
            blackList.append(box)
            print("Added to BlackList")


        # Mostra na tela o objeto detectado
        cor = COLORS[int(classid) % len(COLORS)]
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

        # Detecta a classe desejada
        if class_names[classid[0]] == "truck":
            if box is not blackList:
                contador = contador + 1
                lastTime = time.time()
                isFrame = True

                # Essa parte opera com a lista de recentes
                if box is lastBoxes:
                    blackCounter = blackCounter +1
                else:
                    addElement(box, lastBoxes)
                    blackCounter = 0
            else:
                print(" BlackList !")

        # Tira uma foto
        if contador == 20:
            contador = 0
            if actualTime - lastPicture > 3:
                TOTAL = TOTAL + 1
                cv2.imwrite("caminhao" + str(int(time.time())) + ".jpg", frame)
                lastPicture = time.time()
                print("saved" + "caminhao" + str(int(time.time())) + ".jpg")

        if actualTime - lastTime > 2:
            contador = 0

        # Caso a posição tenha muita recorrencia, considera-se que o caminhão esta estacionado
        if blackCounter == 2:
            blackList.append(box)
            print("Added to BlackList")
            print(blackList)

        # Mostra na tela do usuário
        cor = COLORS[int(classid) % len(COLORS)]
        label = f"{class_names[classid[0]]}: {int(score * 100)}%"
        cv2.rectangle(Edframe, box, cor, 1)
        cv2.putText(Edframe, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, cor, 2)

    # Caso não tenha nenhum caminhão o frame será diminuido
    if isFrame == False and contador > 0:
        contador = contador - 0.5
    end = time.time()

    fps_label = f"FPS: {round((1.0 / (end - start)), 2)}"
    cv2.putText(Edframe, fps_label, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 5)

    cv2.imshow("video", Edframe)

    # Pressione q para sair
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

print(TOTAL)
