# Truck-Detector-IA
Utiliza visão computacional para detectar e registra a passagem de um caminhão por uma via em que o tráfego do mesmo é proibido.

## Introdução:

Esse script foi usado para monitorar o tráfego de caminhões em uma via onde o tráfego dos mesmos é expressamente proibido. A intenção nunca foi punir os condutores, mas sim coletar dados de modo que eles fossem usados para sensibilizar o poder público a tomar medidas com relação ao problema enfrentado pela comunidade. As Fotos que foram retiradas não serão publicisadas aqui, mas falarei sobre os resultados obtidos.
Que fique claro também que se trata de um projeto amador e esta publicação serve para registrar os conhecimentos adiquiridos na elaboração do algoritimo.

### Conhecimento Inicial
Sobre as tecnologias utilizadas:
Python: conhecimento razoavel da linguagem foi o suficiente
OpenCV: conhecimento nulo. Tanto com realção à manipulção de imagens quanto ao uso de haarcascades.

### Bibliotecas Utilizadas
Utilizou-se OpenCV2 e a biblioteca time do python. O haarcascades utilizado foi o yolo v4 tiny por ele ser o suficiente para o projeto e não exigir tantos recursos, ele está disponibilizado aqui:
https://github.com/Tianxiaomo/pytorch-YOLOv4

## Utilização
Para a captura de imagens usei um celular antigo e o configurei para transmitir  o que a câmera capturava, por wifi, para meu computador.
O computador utilizado é composto por um i5-8300H e uma GTX1050 mobile, foi o suficiente para executar o algoritimo por volta de 25 e 30 FPS mesmo rodando outros programas (leves) simultaneamente.

# Resultados:
Em 16 horas ligado o algoritimo coletou 220 (verdadeiros positivos) fotos de caminhões, das quais cerca de 20-30 eram repitidas, e cerca de 50 falsos positivos(vans, alguns onibus e caminhoetes grandes)

Para seu uso pouco exigente o algoritimo se saiu bem, mas possui ainda muitos defeitos que serão enumerados a seguir:
Quanto ao meu código:

1- O algoritimo repete fotos dos mesmos caminhões. Por ter utilizado apenas uma restrição de tempo, caminhöes que demoravam a cruzar toda a extensão da câmera eram fotografados duas ou até três vezes.

2- por conta do algoritimo continuar reconhecendo veiculos estacionados tive de trabalhar para que o algoritimo parasse de tirar fotos dos mesmos, a solução implementada reduz drasticamente o número de fotos porém não resolve o problema por completo.

Quanto ao haarcascades utilizado:

1- O haarcascades utilizado não diferencia caminhões de vans e caminhonetes grandes, principalmente escuras.

2- Há angulos que qualquer veiculo é um caminhão

3- Caminhões com cor poxima a cor de terra são ignorados
