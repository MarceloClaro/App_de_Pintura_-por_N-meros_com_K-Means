# Importando todas as bibliotecas necessárias para o nosso programa funcionar.

import numpy as np  # Esta é uma biblioteca para lidar com matrizes numéricas.
from sklearn.cluster import KMeans  # Esta é uma biblioteca que nos ajuda a encontrar grupos de itens.
from sklearn.utils import shuffle  # Isso nos ajuda a embaralhar itens.
import cv2  # Esta é uma biblioteca para trabalhar com imagens.
import streamlit as st  # Isso é o que nos permite criar a interface do nosso programa.
from PIL import Image  # Outra biblioteca para trabalhar com imagens.
import io  # Esta é uma biblioteca que nos ajuda a lidar com arquivos e dados.
import base64  # Esta é uma biblioteca que nos ajuda a converter dados em diferentes formatos.

# Dicionário de cores junguianas com informações associadas
cores_junguianas = {
    '1': {
        'cor': 'Preto',
        'rgb': (0, 0, 0),
        'anima_animus': 'A cor preta representa a sombra do inconsciente, simbolizando os aspectos desconhecidos e reprimidos de uma pessoa.',
        'sombra': 'A cor preta é a própria sombra, representando os instintos primordiais e os aspectos ocultos da personalidade.',
        'personalidade': 'A cor preta pode indicar uma personalidade enigmática, poderosa e misteriosa.',
        'diagnóstico': 'O uso excessivo da cor preta pode indicar uma tendência à negatividade, depressão ou repressão emocional.'
    },
    '2': {
        'cor': 'Preto carvão',
        'rgb': (10, 10, 10),
        'anima_animus': 'O preto carvão simboliza a sombra feminina do inconsciente, representando os aspectos desconhecidos e reprimidos da feminilidade.',
        'sombra': 'O preto carvão é a própria sombra feminina, representando os instintos primordiais e os aspectos ocultos da feminilidade.',
        'personalidade': 'A cor preto carvão pode indicar uma personalidade poderosa, misteriosa e enigmática com uma forte presença feminina.',
        'diagnóstico': 'O uso excessivo da cor preto carvão pode indicar uma tendência à negatividade, depressão ou repressão emocional na expressão feminina.'
    },
    '3': {
        'cor': 'Cinza escuro',
        'rgb': (17, 17, 17),
        'anima_animus': 'O cinza escuro representa a parte sombria e desconhecida do inconsciente, relacionada aos aspectos reprimidos e negligenciados da personalidade.',
        'sombra': 'O cinza escuro simboliza a sombra interior, representando a reserva de energia não utilizada e os aspectos ocultos da personalidade.',
        'personalidade': 'A cor cinza escuro pode indicar uma personalidade reservada, misteriosa e com profundidade interior.',
        'diagnóstico': 'O uso excessivo da cor cinza escuro pode indicar uma tendência a se esconder, reprimir emoções ou evitar o autoconhecimento.'
    },
    '4': {
        'cor': 'Cinza ardósia',
        'rgb': (47, 79, 79),
        'anima_animus': 'O cinza ardósia representa a sombra feminina do inconsciente, relacionada aos aspectos reprimidos e negligenciados da feminilidade.',
        'sombra': 'O cinza ardósia é a própria sombra feminina, representando a reserva de energia não utilizada e os aspectos ocultos da feminilidade.',
        'personalidade': 'A cor cinza ardósia pode indicar uma personalidade reservada, misteriosa e com uma forte presença feminina.',
        'diagnóstico': 'O uso excessivo da cor cinza ardósia pode indicar uma tendência a se esconder, reprimir emoções ou evitar o autoconhecimento na expressão feminina.'
    },
}

# Classe Canvas para lidar com imagens e cores
class Canvas():
    def __init__(self, src, nb_color, pixel_size=4000):
        self.src = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)  # Corrige a ordem dos canais de cor
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
        if height > width:  # modo retrato
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

# Função para converter RGB em CMYK
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

# Função para calcular a quantidade de tinta em ML para cada cor CMYK
def calculate_ml(c, m, y, k, total_ml):
    total_ink = c + m + y + k
    c_ml = (c / total_ink) * total_ml
    m_ml = (m / total_ink) * total_ml
    y_ml = (y / total_ink) * total_ml
    k_ml = (k / total_ink) * total_ml
    return c_ml, m_ml, y_ml, k_ml

# Função para buscar a cor junguiana mais próxima com base em um RGB
def buscar_cor_proxima(rgb, cores_junguianas):
    distancias = []
    for cor_junguiana in cores_junguianas.values():
        cor_junguiana_rgb = cor_junguiana['rgb']
        distancia = np.sqrt(np.sum((np.array(rgb) - np.array(cor_junguiana_rgb)) ** 2))
        distancias.append(distancia)
    cor_proxima_index = np.argmin(distancias)
    return cores_junguianas[str(cor_proxima_index + 1)]

# Interface do Streamlit
st.image("clube.png")  # Adiciona a imagem no topo do app
st.title('Gerador de Paleta de Cores para Pintura por Números')
st.subheader("Sketching and concept development")
st.subheader("""
Autor: Marcelo Claro

https://orcid.org/0000-0001-8996-2887

marceloclaro@geomaker.org

Whatsapp:(88)98158-7145 (https://www.geomaker.org/)
""")
st.write("""
Apresento a vocês um aplicativo chamado "Gerador de Paleta de Cores para Pintura por Números". Esse aplicativo foi desenvolvido pelo artista plástico Marcelo Claro Laranjeira, conhecido pelo pseudônimo Marcelo Claro. Marcelo é professor de geografia na cidade de Crateús, Ceará, e também é um artista plástico autodidata.
Este aplicativo é uma ferramenta útil para artistas plásticos, pois oferece recursos para gerar paletas de cores, criar pinturas por números, desenvolver esboços e conceitos, e explorar diferentes combinações de cores.
Como funciona? Primeiro, você pode fazer o upload de uma imagem de referência, que pode ser uma foto, ilustração ou qualquer imagem que você deseje usar como base. Em seguida, o aplicativo utiliza o algoritmo K-means para quantificar as cores presentes na imagem. Você pode controlar o número de cores desejado através de um controle deslizante, permitindo extrair a quantidade adequada de cores para sua pintura.
Uma vez gerada a paleta de cores, o aplicativo exibe a imagem resultante, onde cada região da imagem original é substituída pela cor correspondente da paleta. Isso permite que você visualize como sua pintura ficaria usando essas cores específicas. Além disso, o aplicativo também exibe a imagem segmentada, onde cada região da imagem original é preenchida com uma cor sólida correspondente à cor dominante da região. Isso ajuda na identificação de áreas de destaque e contrastes na imagem, facilitando o processo de esboço e desenvolvimento de conceitos.
Uma característica interessante do aplicativo é a possibilidade de definir o total em mililitros de tinta antes de gerar a paleta de cores. Isso permite que você obtenha doses precisas de cada cor primária para alcançar tons exatos em suas paletas.
No processo criativo de Marcelo Claro, ele utiliza o aplicativo como uma ferramenta complementar para sua análise da paisagem humana. Ele reúne imagens, fotos e referências como inspiração e, em seguida, faz esboços e desenvolve conceitos usando a técnica de "Sketching and concept development". Ele explora diferentes ideias, experimenta composições e cores, e utiliza as paletas de cores geradas pelo aplicativo para criar suas pinturas finais.
O trabalho de Marcelo Claro tem como conceito central "Retratando a paisagem humana: a intersecção entre a arte e a geografia". Ele busca retratar a beleza nas coisas simples e cotidianas, explorando como a paisagem humana afeta nossa vida e como nós a modificamos. Sua abordagem geográfica e estética se complementam, permitindo uma análise mais profunda da paisagem e sua relação com nossa existência.
Em resumo, o aplicativo "Gerador de Paleta de Cores para Pintura por Números" é uma ferramenta valiosa para artistas plásticos, oferecendo recursos para criar paletas de cores, desenvolver conceitos e explorar diferentes combinações de cores. Ele auxilia no processo criativo, permitindo visualizar e experimentar as cores antes mesmo de começar a pintar. É uma ferramenta inovadora que combina arte, tecnologia e geografia, permitindo uma análise mais profunda da paisagem humana e sua relação com nossa existência.
""")
uploaded_file = st.file_uploader("Escolha uma imagem", type=["jpg", "png"])
st.write("""
Para começar, faça o upload de uma imagem que você deseja usar como base para a paleta de cores. Você pode usar uma foto, ilustração ou qualquer imagem de sua escolha.
""")
if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Corrige a ordem dos canais de cor
    st.image(image, caption='Imagem Carregada', use_column_width=True)

    nb_color = st.slider('Escolha o número de cores para a paleta', min_value=1, max_value=80, value=2, step=1)
    total_ml = st.slider('Escolha o total em ml da tinta de cada cor', min_value=1, max_value=1000, value=10, step=1)
    pixel_size = st.slider('Escolha o tamanho do pixel da pintura', min_value=500, max_value=8000, value=4000, step=100)

    if st.button('Gerar Paleta de Cores'):
        # Tentativa de leitura dos metadados de resolução (DPI)
        pil_image = Image.open(io.BytesIO(file_bytes))
        if 'dpi' in pil_image.info:
            dpi = pil_image.info['dpi']
            st.write(f'Resolução da imagem: {dpi} DPI')

            # Calcula a dimensão física de um pixel
            cm_per_inch = pixel_size
            cm_per_pixel = cm_per_inch / dpi[0]  # Supõe-se que a resolução seja a mesma em ambas as direções
            st.write(f'Tamanho de cada pixel: {cm_per_pixel:.4f} centímetros')

        canvas = Canvas(image, nb_color, pixel_size)
        result, colors, segmented_image = canvas.generate()

        # Converter imagem segmentada para np.uint8
        segmented_image = (segmented_image * 255).astype(np.uint8)

        # Exibir a imagem segmentada
        st.image(result, caption=f'Paleta de Cores ({nb_color} cores)', use_column_width=True)

        # Converter cores da paleta para CMYK
        cmyk_colors = [rgb_to_cmyk(int(color[0]), int(color[1]), int(color[2])) for color in colors]

        # Calcular a quantidade de tinta em ML para cada cor CMYK
        tinta_ml = [calculate_ml(c, m, y, k, total_ml) for (c, m, y, k) in cmyk_colors]

        # Mostrar a quantidade de tinta em ML para cada cor
        st.write('Quantidade de tinta em ML para cada cor:')
        for i, color_ml in enumerate(tinta_ml):
            st.write(f'Cor {i + 1}:')
            st.write(f'Ciano: {color_ml[0]:.2f} mL')
            st.write(f'Magenta: {color_ml[1]:.2f} mL')
            st.write(f'Amarelo: {color_ml[2]:.2f} mL')
            st.write(f'Preto: {color_ml[3]:.2f} mL')

        # Encontre a cor junguiana mais próxima para cada cor dominante
        cores_junguianas_proximas = [buscar_cor_proxima(color, cores_junguianas) for color in colors]

        # Exibir análise junguiana
        st.write('Análise Junguiana das Cores Dominantes:')
        for i, cor_junguiana in enumerate(cores_junguianas_proximas):
            st.write(f'Cor Dominante {i + 1}: {cor_junguiana["cor"]}')
            st.write(f'Descrição Junguiana:')
            st.write(f'Anima/Animus: {cor_junguiana["anima_animus"]}')
            st.write(f'Sombra: {cor_junguiana["sombra"]}')
            st.write(f'Personalidade: {cor_junguiana["personalidade"]}')
            st.write(f'Diagnóstico: {cor_junguiana["diagnóstico"]}')
            st.write('---')

st.write("""
Espero que você aproveite o uso deste aplicativo para aprimorar seu processo criativo e explorar diferentes paletas de cores para suas obras de arte. Se tiver alguma dúvida ou feedback, sinta-se à vontade para entrar em contato com o autor, Marcelo Claro, usando os dados de contato fornecidos acima.
""")
