import numpy as np
from sklearn.cluster import KMeans
from sklearn.utils import shuffle
import cv2
import streamlit as st

# Definição das cores Junguianas
cores_junguianas = {
    '1': {
        'cor': 'Preto',
        'rgb': (0, 0, 0),
        'anima_animus': 'A cor preta representa a sombra do inconsciente, simbolizando os aspectos desconhecidos e reprimidos de uma pessoa.',
        'sombra': 'A cor preta é a própria sombra, representando os instintos primordiais e os aspectos ocultos da personalidade.',
        'personalidade': 'A cor preta pode indicar uma personalidade enigmática, poderosa e misteriosa.',
        'diagnostico': 'O uso excessivo da cor preta pode indicar uma tendência à negatividade, depressão ou repressão emocional.'
    },
    # Adicione mais cores Junguianas conforme necessário
}

# Função para calcular proporções de tinta
def calcular_proporcoes_tinta(c, m, y, k, total_ml):
    total_tinta = c + m + y + k
    c_ml = (c / total_tinta) * total_ml
    m_ml = (m / total_tinta) * total_ml
    y_ml = (y / total_tinta) * total_ml
    k_ml = (k / total_tinta) * total_ml
    return c_ml, m_ml, y_ml, k_ml

# Função para encontrar a cor Junguiana mais próxima
def encontrar_cor_proxima(rgb, cores_junguianas):
    distancias = []
    for cor_junguiana in cores_junguianas.values():
        cor_junguiana_rgb = cor_junguiana['rgb']
        distancia = np.sqrt(np.sum((np.array(rgb) - np.array(cor_junguiana_rgb)) ** 2))
        distancias.append(distancia)
    cor_proxima_index = np.argmin(distancias)
    return cores_junguianas[str(cor_proxima_index + 1)]

# Função para gerar a paleta de cores e análise da cor Junguiana
def gerar_paleta_e_analise(image, nb_color, total_ml, pixel_size):
    # Converte a imagem para o formato RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
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

    # Cria uma instância da classe Canvas com a imagem RGB
    canvas = Canvas(image_rgb, nb_color, pixel_size)
    
    # Gera a paleta de cores e imagens segmentadas
    result, colors, segmented_image = canvas.generate()
    
    # Encontra a cor Junguiana mais próxima da cor dominante na paleta
    cor_dominante = encontrar_cor_proxima(colors[0], cores_junguianas)
    
    # Retorna os resultados
    return result, colors, segmented_image, cor_dominante

# Configuração do Streamlit
st.set_page_config(
    page_title="Gerador de Paleta de Cores para Pintura por Números",
    page_icon=":art:",
    layout="wide"
)

st.image("clube.png", use_column_width=True)
st.title('Gerador de Paleta de Cores para Pintura por Números')
st.subheader("Sketching and concept development")

# Barra lateral para carregar a imagem
st.sidebar.title("Opções")
uploaded_file = st.sidebar.file_uploader("Escolha uma imagem", type=["jpg", "png"])

# Área principal do aplicativo
if uploaded_file is not None:
    st.sidebar.info("Imagem carregada com sucesso!")

    nb_color = st.sidebar.slider('Escolha o número de cores para pintar', min_value=1, max_value=80, value=2, step=1)
    total_ml = st.sidebar.slider('Escolha o total em ml da tinta de cada cor', min_value=1, max_value=1000, value=10, step=1)
    pixel_size = st.sidebar.slider('Escolha o tamanho do pixel da pintura', min_value=500, max_value=8000, value=4000, step=100)
    
    if st.sidebar.button('Gerar Paleta de Cores'):
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, 1)
        
        result, colors, segmented_image, cor_dominante = gerar_paleta_e_analise(image, nb_color, total_ml, pixel_size)
        
        # Exibir a imagem original
        st.subheader("Imagem Original")
        st.image(image, caption='Imagem Carregada', use_column_width=True)

        # Análise da Cor Dominante Junguiana
        st.subheader("Análise da Cor Dominante Junguiana")
        st.write(f"A cor dominante na paleta é {cor_dominante['cor']}.")
        st.write(f"Anima/Animus: {cor_dominante['anima_animus']}")
        st.write(f"Sombra: {cor_dominante['sombra']}")
        st.write(f"Personalidade: {cor_dominante['personalidade']}")
        st.write(f"Diagnóstico: {cor_dominante['diagnostico']}")

        # Exibir a paleta de cores
        st.subheader("Paleta de Cores")
        for i, color in enumerate(colors):
            color_block = np.ones((50, 50, 3), np.uint8) * color[::-1]  # Cores em formato BGR
            st.image(color_block, caption=f'Cor {i+1}', width=50)

        # Exibir as proporções da tinta CMYK e a cor Junguiana mais próxima para cada cor na paleta
        for i, color in enumerate(colors):
            r, g, b = color
            c, m, y, k = rgb_to_cmyk(r, g, b)
            c_ml, m_ml, y_ml, k_ml = calcular_proporcoes_tinta(c, m, y, k, total_ml)
            color_area = np.count_nonzero(np.all(segmented_image == color, axis=-1))
            total_area = segmented_image.shape[0] * segmented_image.shape[1]
            color_percentage = (color_area / total_area) * 100
            
            st.subheader(f"Detalhes da Cor {i+1}")
            st.write(f"Proporções da tinta CMYK:")
            st.write(f"Ciano (Azul) (C): {c_ml:.2f} ml")
            st.write(f"Magenta (Vermelho) (M): {m_ml:.2f} ml")
            st.write(f"Amarelo (Y): {y_ml:.2f} ml")
            st.write(f"Preto (K): {k_ml:.2f} ml")
            cor_proxima = encontrar_cor_proxima(color, cores_junguianas)
            st.write(f"Cor Junguiana Mais Próxima: {cor_proxima['cor']}")
            st.write(f"Anima/Animus: {cor_proxima['anima_animus']}")
            st.write(f"Sombra: {cor_proxima['sombra']}")
            st.write(f"Personalidade: {cor_proxima['personalidade']}")
            st.write(f"Diagnóstico: {cor_proxima['diagnostico']}")

        # Exibir botões de download para a imagem resultante e imagem segmentada
        st.subheader("Download")
        result_bytes = cv2.imencode('.jpg', result)[1].tobytes()
        st.download_button(
            label="Baixar imagem resultante",
            data=result_bytes,
            file_name='result.jpg',
            mime='image/jpeg')

