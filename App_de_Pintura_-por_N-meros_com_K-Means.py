# Importando todas as coisas necessárias para o nosso programa funcionar.
# Esses são como os blocos de construção que vamos usar para fazer o nosso programa.

import numpy as np  # Esta é uma ferramenta para lidar com listas de números.
from sklearn.cluster import KMeans  # Essa é uma ferramenta que nos ajuda a encontrar grupos de coisas.
from sklearn.utils import shuffle  # Isso nos ajuda a misturar coisas.
import cv2  # Esta é uma ferramenta para trabalhar com imagens.
import streamlit as st  # Isso é o que nos permite criar a interface do nosso programa.
from PIL import Image  # Outra ferramenta para trabalhar com imagens.
import io  # Essa é uma ferramenta que nos ajuda a lidar com arquivos e dados.
import base64  # Essa é uma ferramenta que nos ajuda a converter dados.


# Aqui estamos criando uma nova ferramenta que chamamos de "Canvas".
# Isso nos ajuda a lidar com imagens e cores.

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

def calculate_ml(c, m, y, k, total_ml):
    total_ink = c + m + y + k
    c_ml = (c / total_ink) * total_ml
    m_ml = (m / total_ink) * total_ml
    y_ml = (y / total_ink) * total_ml
    k_ml = (k / total_ink) * total_ml
    return c_ml, m_ml, y_ml, k_ml

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

# Aqui é onde começamos a construir a interface do nosso programa.
# Estamos adicionando coisas como texto e botões para as pessoas interagirem.

st.image("clube.png")  # Adiciona a imagem no topo do app
st.title('Gerador de Paleta de Cores para Pintura por Números ')
st.subheader("Sketching and concept development")
st.subheader("""
Autor: Marcelo Claro

https://orcid.org/0000-0001-8996-2887

marceloclaro@geomaker.org

Whatsapp:(88)98158-7145 (https://www.geomaker.org/)
""")
# Isso é para as pessoas fazerem o upload de uma imagem que elas querem usar.

uploaded_file = st.file_uploader("Escolha uma imagem", type=["jpg", "png"])
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
if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Corrige a ordem dos canais de cor
    st.image(image, caption='Imagem Carregada', use_column_width=True)

    nb_color = st.slider('Escolha o número de cores para pintar', min_value=1, max_value=80, value=2, step=1)

    total_ml = st.slider('Escolha o total em ml da tinta de cada cor', min_value=1, max_value=1000, value=10, step=1)
    
    pixel_size = st.slider('Escolha o tamanho do pixel da pintura', min_value=500, max_value=8000, value=4000, step=100)


    if st.button('Gerar'):
        
        # Tentativa de leitura dos metadados de resolução (DPI)
        pil_image = Image.open(io.BytesIO(file_bytes))
        if 'dpi' in pil_image.info:
            dpi = pil_image.info['dpi']
            st.write(f'Resolução da imagem: {dpi} DPI')

            # Calcula a dimensão física de um pixel
            cm_per_inch = pixel_size
            cm_per_pixel = cm_per_inch / dpi[0]  # Supõe-se que a resolução seja a mesma em ambas as direções
            st.write(f'Tamanho do pixel: {cm_per_pixel:.4f} centímetros')

        canvas = Canvas(image, nb_color, pixel_size)
        result, colors, segmented_image = canvas.generate()

        # Converter imagem segmentada para np.uint8
        segmented_image = (segmented_image * 255).astype(np.uint8)
        
        # Agora converta de BGR para RGB
        segmented_image = cv2.cvtColor(segmented_image, cv2.COLOR_BGR2RGB)

        st.image(result, caption='Imagem Resultante', use_column_width=True)
        st.image(segmented_image, caption='Imagem Segmentada', use_column_width=True)

      
        # Mostrar paleta de cores
        for i, color in enumerate(colors):
            color_block = np.ones((50, 50, 3), np.uint8) * color[::-1]  # Cores em formato BGR
            st.image(color_block, width=50)

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

            Percentual de área na imagem segmentada: {color_percentage:.2f}%
            """)


        result_bytes = cv2.imencode('.jpg', result)[1].tobytes()
        st.download_button(
            label="Baixar imagem resultante",
            data=result_bytes,
            file_name='result.jpg',
            mime='image/jpeg')

        segmented_image_bytes = cv2.imencode('.jpg', segmented_image)[1].tobytes()
        st.download_button(
            label="Baixar imagem segmentada",
            data=segmented_image_bytes,
            file_name='segmented.jpg',
            mime='image/jpeg')
