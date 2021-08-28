# Truck-Detector-IA
Utiliza visão computacional para detectar e registra a passagem de um caminhão por uma via em que o tráfego do mesmo é proibido.

## Introdução:

Esse script foi usado para monitorar o tráfego de caminhões em uma via onde o tráfego dos mesmos é expressamente proibido. A intenção nunca foi punir os condutores, mas sim coletar dados de modo que eles fossem usados para sensibilizar o poder público a tomar medidas com relação ao problema enfrentado pela comunidade. As Fotos que foram retiradas não serão publicadas aqui, mas falarei sobre os resultados obtidos.
Que fique claro também que se trata de um projeto amador e esta publicação serve para registrar os conhecimentos adquiridos na elaboração do algoritmo.

### Conhecimento Inicial
Sobre as tecnologias utilizadas:
Python: conhecimento razoável da linguagem foi o suficiente
OpenCV: conhecimento nulo. Tanto com relação à manipulação de imagens quanto ao uso de haarcascades.

### Bibliotecas Utilizadas
Utilizou-se OpenCV2 e a biblioteca time do python. O haarcascades utilizado foi o yolo v4 tiny por ele ser o suficiente para o projeto e não exigir tantos recursos, ele está disponibilizado aqui:
https://github.com/Tianxiaomo/pytorch-YOLOv4

## Utilização
Para a captura de imagens usei um celular antigo e o configurei para transmitir o que a câmera capturava, por wifi, para meu computador.
O computador utilizado é composto por um i5-8300H e uma GTX1050 mobile, foi o suficiente para executar o algoritmo por volta de 25 e 30 FPS mesmo rodando outros programas (leves) simultaneamente.

# Resultados:
Em 16 horas ligado o algoritmo coletou 220 (verdadeiros positivos) fotos de caminhões, das quais cerca de 20-30 eram repetidas, e cerca de 50 falsos positivos(vans, alguns onibus e caminhoetes grandes)

Para seu uso pouco exigente o algoritmo se saiu bem, mas possui ainda muitos defeitos que serão enumerados a seguir:
Quanto ao meu código:

1- O algorítimo repete fotos dos mesmos caminhões. Por utilizar apenas uma restrição de tempo, caminhões que demoravam a cruzar toda a extensão da câmera eram fotografados duas ou até três vezes.

2- por conta do algorítimo continuar reconhecendo veículos estacionados tive de trabalhar para que o programa parasse de fotografar os mesmos, a solução implementada reduz drasticamente o número de fotos, porém não resolve o problema por completo.

Quanto ao haarcascades utilizado:

1- O haarcascades utilizado não diferencia caminhões de vans e caminhonetes grandes, principalmente escuras.

2- Há ângulos que qualquer veiculo é um caminhão

3- Caminhões com cor próxima à cor de terra são ignorados
