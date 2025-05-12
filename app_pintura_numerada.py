# Importando todas as coisas necessárias para o nosso programa funcionar.
# Esses são como os blocos de construção que vamos usar para fazer o nosso programa.

import numpy as np  # Esta é uma ferramenta para lidar com listas de números.
from sklearn.cluster import KMeans  # Essa é uma ferramenta que nos ajuda a encontrar grupos de coisas.
from sklearn.utils import shuffle  # Isso nos ajuda a misturar coisas.
import cv2  # Esta é uma ferramenta para trabalhar com imagens.
import streamlit as st  # Isso é o que nos permite criar a interface do nosso programa.
from PIL import Image  # Outra ferramenta para trabalhar com imagens.
import io  # Essa é uma ferramenta que nos ajuda a lidar com arquivos e dados.
# import base64 # Não está sendo usado diretamente, pode ser removido se não for usado por dependências indiretas.

# TODO: Expandir este dicionário com mais cores e suas respectivas análises Junguianas.
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
        'cor': 'Branco',
        'rgb': (255, 255, 255),
        'anima_animus': 'Pureza, totalidade, o Self não diferenciado, potencialidade.',
        'sombra': 'Frieza, vazio, negação da vida instintiva, perfeccionismo estéril.',
        'personalidade': 'Pode indicar busca por clareza, simplicidade, ou um ideal de perfeição.',
        'diagnostico': 'Uso excessivo pode sugerir distanciamento emocional, dificuldade em lidar com a "sujeira" da vida.'
    },
    '3': {
        'cor': 'Vermelho',
        'rgb': (255, 0, 0),
        'anima_animus': 'Paixão, energia vital, libido, o princípio masculino ativo.',
        'sombra': 'Raiva, agressividade descontrolada, perigo, impulsividade destrutiva.',
        'personalidade': 'Personalidade extrovertida, assertiva, energética, competitiva.',
        'diagnostico': 'Excesso pode indicar stress, inflamação, ou uma necessidade de extravasar emoções intensas.'
    },
    # ... (adicione outras cores Junguianas conforme necessário)
}

def rgb_to_cmyk(r_norm, g_norm, b_norm): # Espera r,g,b normalizados (0-1)
    if (r_norm == 0) and (g_norm == 0) and (b_norm == 0): # Preto
        return 0, 0, 0, 1

    c = 1 - r_norm
    m = 1 - g_norm
    y = 1 - b_norm

    min_cmy = min(c, m, y)

    if (1 - min_cmy) == 0: # Caso de branco (r_norm=1, g_norm=1, b_norm=1)
        return 0, 0, 0, 0 # k = min_cmy = 0

    c_final = (c - min_cmy) / (1 - min_cmy)
    m_final = (m - min_cmy) / (1 - min_cmy)
    y_final = (y - min_cmy) / (1 - min_cmy)
    k_final = min_cmy

    return c_final, m_final, y_final, k_final


def calculate_ml(c, m, y, k, total_ml):
    total_ink = c + m + y + k
    if total_ink == 0: # Nenhuma tinta necessária para branco ou cor sem componentes CMYK
        return 0, 0, 0, 0

    c_ml = (c / total_ink) * total_ml
    m_ml = (m / total_ink) * total_ml
    y_ml = (y / total_ink) * total_ml
    k_ml = (k / total_ink) * total_ml
    return c_ml, m_ml, y_ml, k_ml

def buscar_cor_proxima(rgb_query, cores_junguianas_dict):
    if max(rgb_query) <= 1.0: # Normaliza se estiver no formato 0-1
        rgb_query_255 = tuple(int(c * 255) for c in rgb_query)
    else:
        rgb_query_255 = tuple(int(c) for c in rgb_query)

    min_distancia = float('inf')
    cor_mais_proxima_info = None
    
    if not cores_junguianas_dict:
        return {
            'cor': 'N/A', 'rgb': (0,0,0), 'anima_animus': 'Dicionário vazio.',
            'sombra': 'Dicionário vazio.', 'personalidade': 'Dicionário vazio.',
            'diagnostico': 'Dicionário de cores Junguianas está vazio.'
        }

    for key, cor_data in cores_junguianas_dict.items():
        cor_junguiana_rgb = cor_data['rgb']
        distancia = np.sqrt(np.sum((np.array(rgb_query_255) - np.array(cor_junguiana_rgb)) ** 2))
        if distancia < min_distancia:
            min_distancia = distancia
            cor_mais_proxima_info = cor_data
            
    if cor_mais_proxima_info is None and cores_junguianas_dict: # Fallback improvável
        return cores_junguianas_dict[next(iter(cores_junguianas_dict))]

    return cor_mais_proxima_info


class Canvas():
    def __init__(self, src_rgb, nb_color, target_dimension_px):
        self.src_rgb = src_rgb # Espera-se NumPy array RGB
        self.nb_color = nb_color
        self.target_dimension_px = target_dimension_px
        self.colormap_rgb_0_255 = []

    def generate(self):
        im_source_resized_rgb = self.resize()
        clean_img_rgb = self.cleaning(im_source_resized_rgb) # RGB uint8
        
        clean_img_norm_rgb = np.array(clean_img_rgb, dtype=np.float32) / 255.0 # RGB float32 (0-1)
        
        quantified_image_norm_rgb, colors_palette_norm_rgb = self.quantification(clean_img_norm_rgb) # Ambos RGB float32 (0-1)
        
        quantified_image_uint8_rgb = (quantified_image_norm_rgb * 255).astype(np.uint8) # RGB uint8 (0-255)

        canvas_paint = np.ones(quantified_image_uint8_rgb.shape[:2], dtype="uint8") * 255 # P&B

        self.colormap_rgb_0_255 = []
        if colors_palette_norm_rgb.shape[0] > 0: # Se houver cores na paleta
            for ind, color_norm_rgb in enumerate(colors_palette_norm_rgb):
                self.colormap_rgb_0_255.append([int(c * 255) for c in color_norm_rgb]) # Armazena como RGB 0-255
                
                color_uint8_rgb_val = (color_norm_rgb * 255).astype(np.uint8)

                mask = cv2.inRange(quantified_image_uint8_rgb, color_uint8_rgb_val, color_uint8_rgb_val)
                
                contours, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

                for contour in contours:
                    if cv2.contourArea(contour) > 100: 
                        cv2.drawContours(canvas_paint, [contour], -1, (0, 0, 0), 1)
                        M = cv2.moments(contour)
                        if M["m00"] != 0:
                            txt_x = int(M["m10"] / M["m00"])
                            txt_y = int(M["m01"] / M["m00"])
                            cv2.putText(canvas_paint, '{:d}'.format(ind + 1), (txt_x, txt_y),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
        
        return canvas_paint, colors_palette_norm_rgb, quantified_image_uint8_rgb

    def resize(self):
        (height, width) = self.src_rgb.shape[:2]
        if width == 0 or height == 0: # Lida com imagem vazia
            return np.zeros((100,100,3), dtype=self.src_rgb.dtype) # Retorna uma imagem preta pequena

        if height > width:
            dim = (int(width * self.target_dimension_px / float(height)), self.target_dimension_px)
        else:
            dim = (self.target_dimension_px, int(height * self.target_dimension_px / float(width)))
        
        if dim[0] <= 0 or dim[1] <= 0: # Fallback se dimensão calculada for inválida
            dim = (max(1, dim[0]), max(1, dim[1])) # Garante pelo menos 1x1
            if dim[0] == 0 or dim[1] == 0: # Se ainda for zero, usa um fallback maior
                 dim = (100,100)


        return cv2.resize(self.src_rgb, dim, interpolation=cv2.INTER_AREA)

    def cleaning(self, picture_rgb_uint8):
        denoised_rgb = cv2.fastNlMeansDenoisingColored(picture_rgb_uint8, None, 10, 10, 7, 21)
        kernel = np.ones((5, 5), np.uint8)
        img_erosion_rgb = cv2.erode(denoised_rgb, kernel, iterations=1)
        img_dilation_rgb = cv2.dilate(img_erosion_rgb, kernel, iterations=1)
        return img_dilation_rgb

    def quantification(self, picture_norm_rgb_float32):
        width, height, depth = picture_norm_rgb_float32.shape
        if width * height == 0: # Imagem vazia
            return picture_norm_rgb_float32, np.array([])

        flattened_rgb = np.reshape(picture_norm_rgb_float32, (width * height, depth))
        
        sample_size = min(1000, flattened_rgb.shape[0]) # Garante que a amostra não seja maior que a população
        if sample_size == 0: # Se não houver pixels para amostrar
            return picture_norm_rgb_float32, np.array([])

        sample_rgb = shuffle(flattened_rgb, random_state=42, n_samples=sample_size)
        
        actual_nb_color = min(self.nb_color, sample_rgb.shape[0]) # n_clusters não pode ser > n_samples
        if actual_nb_color < 1: # Se não houver clusters para formar
             return picture_norm_rgb_float32, np.array([])

        kmeans = KMeans(n_clusters=actual_nb_color, random_state=42, n_init='auto').fit(sample_rgb)
        labels = kmeans.predict(flattened_rgb)
        
        new_img_norm_rgb = self.recreate_image(kmeans.cluster_centers_, labels, width, height) # RGB float32 (0-1)
        return new_img_norm_rgb, kmeans.cluster_centers_ # kmeans.cluster_centers_ é RGB float32 (0-1)

    def recreate_image(self, codebook_norm_rgb, labels, width, height):
        d = codebook_norm_rgb.shape[1]
        image = np.zeros((width * height, d), dtype=np.float32)
        for i in range(width * height):
            image[i] = codebook_norm_rgb[labels[i]]
        return np.resize(image, (width, height, d))


# --- Interface Streamlit ---
st.set_page_config(layout="wide") # Usa layout mais largo

st.sidebar.title("Criação das Paletas de Cores e Tela Numerada")
st.sidebar.write("---")

st.sidebar.header("Informações do Autor")
try:
    st.sidebar.image("clube.png", use_container_width=True)
except Exception:
    st.sidebar.warning("Imagem 'clube.png' não encontrada.")
st.sidebar.write("Nome: Marcelo Claro")
st.sidebar.write("Email: marceloclaro@geomaker.org")
st.sidebar.write("WhatsApp: (88) 98158-7145")

st.sidebar.write("---")

st.sidebar.header("Configurações da Aplicação")
uploaded_file = st.sidebar.file_uploader("Escolha uma imagem", type=["jpg", "png", "jpeg"])
nb_color_slider = st.sidebar.slider('Número de cores na paleta', min_value=2, max_value=30, value=5, step=1)
total_ml_slider = st.sidebar.slider('Total em ml da tinta (por cor)', min_value=10, max_value=1000, value=50, step=10)
target_dimension_slider = st.sidebar.slider(
    'Dimensão alvo da imagem (pixels)', 
    min_value=300, max_value=2000, value=800, step=50,
    help="A maior dimensão (largura ou altura) da imagem será ajustada para este valor, mantendo a proporção."
)

if st.sidebar.button('🎨 Gerar Paleta e Tela'):
    if uploaded_file is not None:
        try:
            pil_image = Image.open(uploaded_file)

            col1_orig, col2_proc = st.columns(2)

            with col1_orig:
                st.subheader("🖼️ Imagem Original")
                st.image(pil_image, caption=f'Original: {uploaded_file.name}', use_container_width=True)

                if 'dpi' in pil_image.info:
                    dpi = pil_image.info['dpi']
                    st.write(f"Resolução: {dpi[0]:.0f}x{dpi[1]:.0f} DPI")
                    cm_per_inch = 2.54
                    if dpi[0] > 0: st.write(f"Tam. pixel X: {cm_per_inch / dpi[0]:.4f} cm")
                    if dpi[1] > 0: st.write(f"Tam. pixel Y: {cm_per_inch / dpi[1]:.4f} cm")
                else:
                    st.write("Info DPI não encontrada.")
                st.write(f"Dimensões: {pil_image.width}px x {pil_image.height}px")
            
            with st.spinner('Processando imagem... Por favor, aguarde.'):
                pil_image_rgb = pil_image.convert('RGB')
                src_np_rgb = np.array(pil_image_rgb) # RGB uint8

                canvas_obj = Canvas(src_np_rgb, nb_color_slider, target_dimension_slider)
                # Retornos:
                # result_paint_screen: P&B uint8 (tela para pintar)
                # colors_palette_norm_rgb: Paleta de cores, RGB float32 (0-1)
                # segmented_image_uint8_rgb: Imagem segmentada, RGB uint8 (0-255)
                result_paint_screen, colors_palette_norm_rgb, segmented_image_uint8_rgb = canvas_obj.generate()
            
            with col2_proc:
                st.subheader("🎨 Imagem Segmentada")
                st.image(segmented_image_uint8_rgb, caption='Cores Quantizadas', use_container_width=True)
                
                # Download da imagem segmentada (RGB para BGR para cv2.imencode com PNG)
                _, segmented_buffer = cv2.imencode('.png', cv2.cvtColor(segmented_image_uint8_rgb, cv2.COLOR_RGB2BGR))
                st.download_button(
                    label="📥 Baixar Segmentada (.png)", data=segmented_buffer.tobytes(),
                    file_name=f'segmentada_{uploaded_file.name}.png', mime='image/png'
                )
                st.write("---")
                st.subheader("🖌️ Tela para Pintar")
                st.image(result_paint_screen, caption='Numerada para Pintar', use_container_width=True)
                # Download da tela para pintar (já é P&B, imencode lida bem)
                _, result_buffer = cv2.imencode('.png', result_paint_screen)
                st.download_button(
                    label="📥 Baixar Tela para Pintar (.png)", data=result_buffer.tobytes(),
                    file_name=f'tela_pintar_{uploaded_file.name}.png', mime='image/png'
                )
            
            st.write("---")
            st.subheader("🌈 Paleta de Cores Gerada e Análise")

            # Verifica se colors_palette_norm_rgb (um array NumPy) tem alguma linha (cor)
            if colors_palette_norm_rgb.shape[0] == 0:
                st.warning("Nenhuma paleta de cores foi gerada. Tente com outra imagem ou configurações.")
            else:
                # Análise da Cor Representativa (primeira cor da paleta K-Means)
                cor_representativa_norm_rgb = colors_palette_norm_rgb[0] # RGB 0-1
                cor_jung_representativa = buscar_cor_proxima(cor_representativa_norm_rgb, cores_junguianas)
                
                if cor_jung_representativa and cor_jung_representativa['cor'] != 'N/A':
                    expander_title = f"Análise Junguiana da Cor Representativa: {cor_jung_representativa['cor']}"
                    with st.expander(expander_title):
                        st.write(f"**Anima/Animus:** {cor_jung_representativa['anima_animus']}")
                        st.write(f"**Sombra:** {cor_jung_representativa['sombra']}")
                        st.write(f"**Personalidade:** {cor_jung_representativa['personalidade']}")
                        st.write(f"**Diagnóstico:** {cor_jung_representativa['diagnostico']}")
                else:
                    st.write("Análise Junguiana para a cor representativa não disponível.")
                st.write("---")

                num_colors_in_palette = colors_palette_norm_rgb.shape[0]
                cols = st.columns(num_colors_in_palette) 

                for i, color_norm_rgb_item in enumerate(colors_palette_norm_rgb):
                    color_uint8_rgb_item = [int(c * 255) for c in color_norm_rgb_item] # RGB 0-255
                    
                    with cols[i]:
                        st.markdown(f"**Cor {i+1}**")
                        color_block_display = np.full((70, 70, 3), color_uint8_rgb_item, dtype=np.uint8)
                        st.image(color_block_display, caption=f"RGB: {tuple(color_uint8_rgb_item)}", width=70)

                        c, m, y, k = rgb_to_cmyk(color_norm_rgb_item[0], color_norm_rgb_item[1], color_norm_rgb_item[2])
                        c_ml, m_ml, y_ml, k_ml = calculate_ml(c, m, y, k, total_ml_slider)

                        st.markdown(f"**CMYK ({total_ml_slider}ml):**")
                        st.caption(f"C: {c_ml:.1f}ml, M: {m_ml:.1f}ml\nY: {y_ml:.1f}ml, K: {k_ml:.1f}ml")
                        
                        cor_jung_especifica = buscar_cor_proxima(color_norm_rgb_item, cores_junguianas)
                        if cor_jung_especifica and cor_jung_especifica['cor'] != 'N/A':
                            with st.expander(f"Jung: {cor_jung_especifica['cor']}", expanded=False):
                                st.write(f"**Anima/Animus:** {cor_jung_especifica['anima_animus']}")
                                st.write(f"**Sombra:** {cor_jung_especifica['sombra']}")
                        st.markdown("---")

        except Exception as e:
            st.error(f"Ocorreu um erro durante o processamento da imagem: {e}")
            st.error("Detalhes técnicos:")
            st.exception(e) 

    else:
        st.warning("Por favor, carregue uma imagem para gerar a paleta e a tela.")

else:
    st.info("👈 Ajuste as configurações na barra lateral, carregue uma imagem e clique em 'Gerar Paleta e Tela'.")
