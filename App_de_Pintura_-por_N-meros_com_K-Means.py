import numpy as np
from sklearn.cluster import KMeans
from sklearn.utils import shuffle
import cv2
import streamlit as st
from PIL import Image
import io

# Dicionário de cores Junguianas
cores_junguianas = {
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

def analyze_and_show_color(color_index, rgb_color, total_ml, segmented_image):
    # Calcular a porcentagem de pixels da cor em relação à imagem segmentada
    total_pixels = segmented_image.shape[0] * segmented_image.shape[1]
    color_pixels = np.count_nonzero(np.all(segmented_image == rgb_color, axis=-1))
    color_percentage = (color_pixels / total_pixels) * 100

    # Calcular a quantidade de tinta necessária
    c, m, y, k = rgb_to_cmyk(*rgb_color)
    c_ml, m_ml, y_ml, k_ml = calculate_ml(c, m, y, k, total_ml)

    # Exibir informações sobre a cor
    st.write(f"Cor {color_index + 1}:")
    st.write(f"Porcentagem da imagem: {color_percentage:.2f}%")
    st.write(f"Quantidade de tinta necessária:")
    st.write(f"   - Ciano: {c_ml:.2f} mL")
    st.write(f"   - Magenta: {m_ml:.2f} mL")
    st.write(f"   - Amarelo: {y_ml:.2f} mL")
    st.write(f"   - Preto: {k_ml:.2f} mL")

# Restante do código...


# Início da interface do Streamlit
st.image("clube.png")
st.title('Gerador de Paleta de Cores para Pintura por Números')

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

        # Encontrar o índice da cor dominante
        dominant_color_index = max(area_dict, key=area_dict.get)

        # Encontrar a cor junguiana mais próxima da cor dominante
        dominant_color = colors[dominant_color_index]
        closest_jungian_color = find_closest_jungian_color(dominant_color, cores_junguianas)

        # Exibir a análise da cor junguiana dominante
        st.write(f"A cor junguiana dominante é: {closest_jungian_color['cor']}")
        st.write(f"Anima/Animus: {closest_jungian_color['anima_animus']}")
        st.write(f"Sombra: {closest_jungian_color['sombra']}")
        st.write(f"Personalidade: {closest_jungian_color['personalidade']}")
        st.write(f"Diagnóstico: {closest_jungian_color['diagnostico']}")

        # Loop para analisar e mostrar todas as cores
        for i, color in enumerate(colors):
            c_ml, m_ml, y_ml, k_ml = calculate_ink_amount(color, total_ml)
            st.write(f"Cor {i + 1}:")
            st.write(f"Quantidade de tinta necessária:")
            st.write(f"   - Ciano: {c_ml:.2f} mL")
            st.write(f"   - Magenta: {m_ml:.2f} mL")
            st.write(f"   - Amarelo: {y_ml:.2f} mL")
            st.write(f"   - Preto: {k_ml:.2f} mL")

        # O código para download permanece o mesmo
        result_bytes = cv2.imencode('.jpg', result)[1].tobytes()
        st.download_button(
            label="Baixar imagem resultante",
            data=result_bytes,
            file_name='result.jpg',
            mime='image/jpeg')

        segmented_image_rgb = cv2.cvtColor(segmented_image, cv2.COLOR_BGR2RGB)
        segmented_image_bytes = cv2.imencode('.jpg', segmented_image_rgb)[1].tobytes()
        st.download_button(
            label="Baixar imagem segmentada",
            data=segmented_image_bytes,
            file_name='segmented.jpg',
            mime='image/jpeg')
