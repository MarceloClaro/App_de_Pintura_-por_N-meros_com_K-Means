import numpy as np
from sklearn.cluster import KMeans
from sklearn.utils import shuffle
import cv2
import streamlit as st
from PIL import Image
import io

# Dicionário de cores Junguianas
cores_junguianas =  {
    '1': {
        'cor': 'Preto',
        'rgb': (0, 0, 0),
        'anima_animus': 'A cor preta representa a sombra do inconsciente, simbolizando os aspectos desconhecidos e reprimidos de uma pessoa.',
        'sombra': 'A cor preta é a própria sombra, representando os instintos primordiais e os aspectos ocultos da personalidade.',
        'personalidade': 'A cor preta pode indicar uma personalidade enigmática, poderosa e misteriosa.',
        'diagnostico': 'O uso excessivo da cor preta pode indicar uma tendência à negatividade, depressão ou repressão emocional.'
    },
    '2': {
        'cor': 'Preto carvão',
        'rgb': (10, 10, 10),
        'anima_animus': 'O preto carvão simboliza a sombra feminina do inconsciente, representando os aspectos desconhecidos e reprimidos da feminilidade.',
        'sombra': 'O preto carvão é a própria sombra feminina, representando os instintos primordiais e os aspectos ocultos da feminilidade.',
        'personalidade': 'A cor preto carvão pode indicar uma personalidade poderosa, misteriosa e enigmática com uma forte presença feminina.',
        'diagnostico': 'O uso excessivo da cor preto carvão pode indicar uma tendência à negatividade, depressão ou repressão emocional na expressão feminina.'
    },
    '3': {
        'cor': 'Cinza escuro',
        'rgb': (17, 17, 17),
        'anima_animus': 'O cinza escuro representa a parte sombria e desconhecida do inconsciente, relacionada aos aspectos reprimidos e negligenciados da personalidade.',
        'sombra': 'O cinza escuro simboliza a sombra interior, representando a reserva de energia não utilizada e os aspectos ocultos da personalidade.',
        'personalidade': 'A cor cinza escuro pode indicar uma personalidade reservada, misteriosa e com profundidade interior.',
        'diagnostico': 'O uso excessivo da cor cinza escuro pode indicar uma tendência a se esconder, reprimir emoções ou evitar o autoconhecimento.'
    },
    '4': {
        'cor': 'Cinza ardósia',
        'rgb': (47, 79, 79),
        'anima_animus': 'O cinza ardósia representa a sombra feminina do inconsciente, relacionada aos aspectos reprimidos e negligenciados da feminilidade.',
        'sombra': 'O cinza ardósia é a própria sombra feminina, representando a reserva de energia não utilizada e os aspectos ocultos da feminilidade.',
        'personalidade': 'A cor cinza ardósia pode indicar uma personalidade reservada, misteriosa e com uma forte presença feminina.',
        'diagnostico': 'O uso excessivo da cor cinza ardósia pode indicar uma tendência a se esconder, reprimir emoções ou evitar o autoconhecimento na expressão feminina.'
    },
    
}


# Funções auxiliares

def rgb_to_cmyk(r, g, b):
    if (r == 0) and (g == 0) and (b == 0):
        return 0, 0, 0, 1
    c = 1 - r / 255
    m = 1 - g / 255
    y = 1 - b / 255

    min_cmy = min(c, m, y)
    c = (c - min_cmy) / (1 - min_cmy)
    m = (m - min_cmy) / (1 - min_cmy)
    y = (y - min_cmy) / (1 - min_cmy)
    k = min_cmy

    return c, m, y, k

# As outras funções auxiliares como 'calculate_ml' e 'buscar_cor_proxima' também seriam mantidas aqui.


def calculate_ml(c, m, y, k, total_ml):
    total_ink = c + m + y + k
    c_ml = (c / total_ink) * total_ml
    m_ml = (m / total_ink) * total_ml
    y_ml = (y / total_ink) * total_ml
    k_ml = (k / total_ink) * total_ml
    return c_ml, m_ml, y_ml, k_ml

def buscar_cor_proxima(rgb, cores_junguianas):
    distancias = []
    for cor_junguiana in cores_junguianas.values():
        cor_junguiana_rgb = cor_junguiana['rgb']
        distancia = np.sqrt(np.sum((np.array(rgb) - np.array(cor_junguiana_rgb)) ** 2))
        distancias.append(distancia)
    cor_proxima_index = np.argmin(distancias)
    return cores_junguianas[str(cor_proxima_index + 1)]

# Classe Canvas para manipulação de imagem
class Canvas():
    def __init__(self, src, nb_color, pixel_size=4000):
        self.src = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
        self.nb_color = nb_color
        self.tar_width = pixel_size
        self.colormap = []

    def generate(self):
        im_source = self.resize()
        clean_img = self.cleaning(im_source)
        width, height, depth = clean_img.shape
        clean_img = np.array(clean_img, dtype="uint8") / 255
        quantified_image, colors = self.quantification(clean_img)
        canvas = np.ones(quantified_image.shape[:2], dtype="uint8") * 255

        for ind, color in enumerate(colors):
            self.colormap.append([int(c * 255) for c in color])
            mask = cv2.inRange(quantified_image, color, color)
            cnts = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
            cnts = cnts[0] if len(cnts) == 2 else cnts[1]

            for contour in cnts:
                _, _, width_ctr, height_ctr = cv2.boundingRect(contour)
                if width_ctr > 10 and height_ctr > 10 and cv2.contourArea(contour, True) < -100:
                    cv2.drawContours(canvas, [contour], -1, (0, 0, 0), 1)
                    txt_x, txt_y = contour[0][0]
                    cv2.putText(canvas, '{:d}'.format(ind + 1), (txt_x, txt_y + 15),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

        return canvas, colors, quantified_image

    def resize(self):
        (height, width) = self.src.shape[:2]
        if height > width:
            dim = (int(width * self.tar_width / float(height)), self.tar_width)
        else:
            dim = (self.tar_width, int(height * self.tar_width / float(width)))
        return cv2.resize(self.src, dim, interpolation=cv2.INTER_AREA)

    def cleaning(self, picture):
        clean_pic = cv2.fastNlMeansDenoisingColored(picture, None, 10, 10, 7, 21)
        kernel = np.ones((5, 5), np.uint8)
        img_erosion = cv2.erode(clean_pic, kernel, iterations=1)
        img_dilation = cv2.dilate(img_erosion, kernel, iterations=1)
        return img_dilation

    def quantification(self, picture):
        width, height, depth = picture.shape
        flattened = np.reshape(picture, (width * height, depth))
        sample = shuffle(flattened)[:1000]
        kmeans = KMeans(n_clusters=self.nb_color).fit(sample)
        labels = kmeans.predict(flattened)
        new_img = self.recreate_image(kmeans.cluster_centers_, labels, width, height)
        return new_img, kmeans.cluster_centers_

    def recreate_image(self, codebook, labels, width, height):
        vfunc = lambda x: codebook[labels[x]]
        out = vfunc(np.arange(width * height))
        return np.resize(out, (width, height, codebook.shape[1]))


# Início da interface do Streamlit
st.image("clube.png")
st.title('Gerador de Paleta de Cores para Pintura por Números')
# ... (outros elementos de UI aqui)

uploaded_file = st.file_uploader("Escolha uma imagem", type=["jpg", "png"])

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    st.image(image, caption='Imagem Carregada', use_column_width=True)

    nb_color = st.slider('Escolha o número de cores para pintar', min_value=1, max_value=80, value=2, step=1)
    total_ml = st.slider('Escolha o total em ml da tinta de cada cor', min_value=1, max_value=1000, value=10, step=1)

    if st.button('Gerar'):
        canvas = Canvas(image, nb_color)
        result, colors, segmented_image = canvas.generate()

        segmented_image = (segmented_image * 255).astype(np.uint8)
        segmented_image = cv2.cvtColor(segmented_image, cv2.COLOR_BGR2RGB)

        st.image(result, caption='Imagem Resultante', use_column_width=True)
        st.image(segmented_image, caption='Imagem Segmentada', use_column_width=True)

        # Dicionário para armazenar a área de cada cor
        area_dict = {}

        for i, color in enumerate(colors):
            color_block = np.ones((50, 50, 3), np.uint8) * color[::-1]
            st.image(color_block, caption=f'Cor {i+1}', width=50)

            color_area = np.count_nonzero(np.all(segmented_image == color, axis=-1))
            area_dict[i] = color_area

            # (Você pode manter aqui as outras análises e downloads)

        # Encontrar o índice da cor dominante
        dominant_color_index = max(area_dict, key=area_dict.get)

        # Encontrar a cor junguiana mais próxima da cor dominante
        dominant_color = colors[dominant_color_index]
        closest_jungian_color = buscar_cor_proxima(dominant_color, cores_junguianas)

        # Exibir a análise da cor junguiana dominante
        st.write(f"A cor junguiana dominante é: {closest_jungian_color['cor']}")
        st.write(f"Anima/Animus: {closest_jungian_color['anima_animus']}")
        st.write(f"Sombra: {closest_jungian_color['sombra']}")
        st.write(f"Personalidade: {closest_jungian_color['personalidade']}")
        st.write(f"Diagnóstico: {closest_jungian_color['diagnostico']}")

---

def analyze_and_show_color(i, color, total_ml, segmented_image):
    color_block = np.ones((50, 50, 3), np.uint8) * color[::-1]  # Cores em formato BGR
    st.image(color_block, caption=f'Cor {i+1}', width=50)
    
    # Cálculo das proporções das cores CMYK
    r, g, b = color
    c, m, y, k = rgb_to_cmyk(r, g, b)
    c_ml, m_ml, y_ml, k_ml = calculate_ml(c, m, y, k, total_ml)
    
    # Calcular a área da cor na imagem segmentada
    color_area = np.count_nonzero(np.all(segmented_image == color, axis=-1))
    total_area = segmented_image.shape[0] * segmented_image.shape[1]
    color_percentage = (color_area / total_area) * 100
    
    st.subheader("Sketching and concept development da paleta de cor")
    st.write(f"""
    PALETAS DE COR PARA: {total_ml:.2f} ml.
    
    A cor pode ser alcançada pela combinação das cores primárias do modelo CMYK, utilizando a seguinte dosagem:

    Ciano (Azul) (C): {c_ml:.2f} ml
    Magenta (Vermelho) (M): {m_ml:.2f} ml
    Amarelo (Y): {y_ml:.2f} ml
    Preto (K): {k_ml:.2f} ml
    """)
    
    cor_proxima = buscar_cor_proxima(color, cores_junguianas)
    st.write(f"Cor Junguiana Mais Próxima: {cor_proxima['cor']}")
    st.write(f"Anima/Animus: {cor_proxima['anima_animus']}")
    st.write(f"Sombra: {cor_proxima['sombra']}")
    st.write(f"Personalidade: {cor_proxima['personalidade']}")
    st.write(f"Diagnóstico: {cor_proxima['diagnostico']}")
    
# No loop:
for i, color in enumerate(colors):
    analyze_and_show_color(i, color, total_ml, segmented_image)

# O código para download permanece o mesmo
result_bytes = cv2.imencode('.jpg', result)[1].tobytes()
# ...
