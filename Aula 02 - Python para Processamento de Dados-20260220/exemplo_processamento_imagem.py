import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import imread
from matplotlib.widgets import Slider

#Carrega imagem com matplotlib
img = imread('fern.webp')
print(type(img))
w,h,c = img.shape

#imagem grayscale
#Separando os canais de cores via slices
r, g, b = img[:,:,0], img[:,:,1], img[:,:,2]
gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
gray.astype(np.uint8)

def ajusta_mascara(valor):
    mask = gray > valor
    cp = gray.copy()
    cp[mask] = 255
    copia = img.copy()
    copia[mask] = 255
    return cp, copia


cp, copia = ajusta_mascara(100)

fig = plt.figure()

# Espaço adicional na parte de baixo da imagem
plt.subplots_adjust(bottom=0.2) 

# Configura a exibição das imagens
fig.add_subplot(2,2,1)
plt.imshow(img)
plt.title("Original")
plt.axis('off')  # Remove os eixos

fig.add_subplot(2,2,2)
plt.imshow(gray, cmap='gray')
plt.title("Grayscale")
plt.axis('off')  # Remove os eixos

fig.add_subplot(2,2,3)
im_mascara = plt.imshow(cp, cmap='gray')
plt.title("Máscara")
plt.axis('off')  # Remove os eixos

fig.add_subplot(2,2,4)
im_aplicacao = plt.imshow(copia)
plt.title("Aplicação")
plt.axis('off')  # Remove os eixos

# Define a posição e tamanho do slider [esquerda, baixo, largura, altura]
ax_slider = plt.axes([0.25, 0.05, 0.50, 0.03])

slider_limiar = Slider(
    ax=ax_slider,
    label='Limiar ',
    valmin=0.0,
    valmax=255,   # Se sua imagem for uint8 (0-255), mude para 255
    valinit=100
)

def update(val):
    # 1. Pega o valor atual do slider
    limiar = slider_limiar.val
    
    # 2. Recalcula as imagens baseadas no novo valor
    nova_mascara, novo_resultado = ajusta_mascara(limiar)
    
    # 3. Atualiza os dados dentro dos objetos de imagem existentes
    im_mascara.set_data(nova_mascara)
    im_aplicacao.set_data(novo_resultado)
    
    # 4. Redesenha a figura
    fig.canvas.draw_idle()

# Conecta a função ao evento de mudança do slider
slider_limiar.on_changed(update)

# Exibe o gráfico
plt.tight_layout()
plt.show()
