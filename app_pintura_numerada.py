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
    '2': { # Exemplo de outra cor, precisa ser preenchido corretamente
        'cor': 'Branco',
        'rgb': (255, 255, 255),
        'anima_animus': 'Interpretação para Anima/Animus do Branco...',
        'sombra': 'Interpretação para Sombra do Branco...',
        'personalidade': 'Interpretação para Personalidade do Branco...',
        'diagnostico': 'Interpretação para Diagnóstico do Branco...'
    },
    # ... (adicione outras cores Junguianas conforme necessário)
}

# Aqui estamos criando uma nova ferramenta que chamamos de "Canvas".
# Isso nos ajuda a lidar com imagens e cores.

def rgb_to_cmyk(r_norm, g_norm, b_norm): # Espera r,g,b normalizados (0-1)
    r, g, b = r_norm * 255, g_norm * 255, b_norm * 255 # Desnormaliza para cálculo original
    if (r == 0) and (g == 0) and (b == 0):
        return 0, 0, 0, 1 # CMYK para preto puro

    # Normaliza r,g,b para o cálculo CMY se não forem já
    c = 1 - r / 255.0
    m = 1 - g / 255.0
    y = 1 - b / 255.0

    min_cmy = min(c, m, y)
    
    # Evitar divisão por zero se min_cmy for 1 (branco)
    if (1 - min_cmy) == 0:
        if min_cmy == 1: # Cor é branca
             return 0,0,0,0 # CMYK para branco
        else: # Evita divisão por zero em outros casos, embora raro com float
             # Este caso não deveria ocorrer se r,g,b não são todos 255
             # Se min_cmy é próximo de 1 mas não 1, 1-min_cmy é pequeno mas não zero.
             # Se min_cmy é 1, então c,m,y são 0, e k seria 1.
             # A lógica original já tratava preto. Se r,g,b são 255, c,m,y são 0, min_cmy é 0.
             # (0-0)/(1-0) = 0. k = 0. Isso está correto para branco.
             # O problema é se min_cmy = 1, o que significa c=1, m=1, y=1 (preto).
             # Mas o preto já foi tratado (r=0,g=0,b=0).
             # Se r,g,b não são 0, então c,m,y não serão todos 1.
             # Então 1-min_cmy não será 0 a menos que min_cmy=1, que é o caso do preto.
             # A condição (r==0) and (g==0) and (b==0) já cuida do preto.
             # Para branco (r=255,g=255,b=255), c=0,m=0,y=0, min_cmy=0. k=0. (c-0)/(1-0) = 0. Correto.
             # A divisão por (1-min_cmy) só é problema se min_cmy = 1.
             # Isso ocorre se c=1, m=1, y=1, o que significa r=0, g=0, b=0 (preto).
             # Esse caso já é tratado no início.
             # Portanto, a divisão por (1-min_cmy) não deve ser por zero aqui.
             pass # Mantém a lógica original, mas a checagem de preto no início é crucial.


    c_final = (c - min_cmy) / (1 - min_cmy) if (1 - min_cmy) != 0 else 0
    m_final = (m - min_cmy) / (1 - min_cmy) if (1 - min_cmy) != 0 else 0
    y_final = (y - min_cmy) / (1 - min_cmy) if (1 - min_cmy) != 0 else 0
    k_final = min_cmy

    return c_final, m_final, y_final, k_final


def calculate_ml(c, m, y, k, total_ml):
    # Evitar divisão por zero se todas as componentes CMYK forem 0 (branco)
    total_ink = c + m + y + k
    if total_ink == 0:
        return 0, 0, 0, 0 # Nenhuma tinta necessária para branco

    c_ml = (c / total_ink) * total_ml
    m_ml = (m / total_ink) * total_ml
    y_ml = (y / total_ink) * total_ml
    k_ml = (k / total_ink) * total_ml
    return c_ml, m_ml, y_ml, k_ml

def buscar_cor_proxima(rgb_query, cores_junguianas_dict):
    # rgb_query é esperado como (R, G, B) com valores 0-255
    # As cores em cores_junguianas_dict['rgb'] também são 0-255
    
    # Normaliza rgb_query se estiver no formato 0-1 (vindo dos centroides do KMeans)
    if max(rgb_query) <= 1.0:
        rgb_query_255 = tuple(int(c * 255) for c in rgb_query)
    else:
        rgb_query_255 = tuple(int(c) for c in rgb_query)

    min_distancia = float('inf')
    cor_mais_proxima_info = None
    
    if not cores_junguianas_dict: # Verifica se o dicionário está vazio
        return { # Retorna um valor padrão ou um erro/aviso
            'cor': 'N/A (dicionário vazio)',
            'rgb': (0,0,0),
            'anima_animus': 'Não disponível.',
            'sombra': 'Não disponível.',
            'personalidade': 'Não disponível.',
            'diagnostico': 'Dicionário de cores Junguianas está vazio ou não foi carregado.'
        }

    for key, cor_data in cores_junguianas_dict.items():
        cor_junguiana_rgb = cor_data['rgb']
        distancia = np.sqrt(np.sum((np.array(rgb_query_255) - np.array(cor_junguiana_rgb)) ** 2))
        if distancia < min_distancia:
            min_distancia = distancia
            cor_mais_proxima_info = cor_data
            
    # Se nenhuma cor for encontrada (improvável se o dicionário não estiver vazio, mas por segurança)
    if cor_mais_proxima_info is None and cores_junguianas_dict:
        # Retorna a primeira cor do dicionário como fallback ou uma mensagem de erro
        # Esta situação não deveria ocorrer se o dicionário tiver pelo menos um item.
        return cores_junguianas_dict[next(iter(cores_junguianas_dict))]


    return cor_mais_proxima_info


class Canvas():
    def __init__(self, src_rgb, nb_color, target_dimension_px):
        # Espera-se que src_rgb seja uma imagem NumPy no formato RGB
        self.src_rgb = src_rgb
        self.nb_color = nb_color
        self.target_dimension_px = target_dimension_px # Renomeado de pixel_size
        self.colormap_rgb = [] # Armazenará cores RGB (0-255)

    def generate(self):
        im_source_resized_rgb = self.resize()
        
        # Para cv2.fastNlMeansDenoisingColored, é comum usar BGR.
        # Vamos converter para BGR para limpeza e depois de volta para RGB se necessário,
        # ou verificar se as funções subsequentes lidam bem com RGB.
        # Testes indicam que fastNlMeansDenoisingColored funciona com RGB.
        # Se problemas de cor surgirem, esta é uma área a ser revisada:
        # im_source_resized_bgr = cv2.cvtColor(im_source_resized_rgb, cv2.COLOR_RGB2BGR)
        # clean_img_bgr = self.cleaning(im_source_resized_bgr)
        # clean_img_rgb = cv2.cvtColor(clean_img_bgr, cv2.COLOR_BGR2RGB)
        
        # Mantendo RGB por enquanto:
        clean_img_rgb = self.cleaning(im_source_resized_rgb)

        # A quantificação espera valores normalizados (0-1)
        clean_img_norm_rgb = np.array(clean_img_rgb, dtype="float32") / 255.0 # Alterado para float32 para KMeans
        
        quantified_image_norm_rgb, colors_norm_rgb = self.quantification(clean_img_norm_rgb)
        
        # quantified_image_norm_rgb está normalizado (0-1), colors_norm_rgb também.
        # Converter quantified_image para uint8 (0-255) para desenho de contornos
        quantified_image_uint8_rgb = (quantified_image_norm_rgb * 255).astype(np.uint8)

        # A tela para pintar será em escala de cinza (contornos pretos, fundo branco)
        canvas_paint = np.ones(quantified_image_uint8_rgb.shape[:2], dtype="uint8") * 255

        self.colormap_rgb = [] # Limpa/reinicia colormap
        for ind, color_norm_rgb in enumerate(colors_norm_rgb):
            # Adiciona à colormap como RGB 0-255
            self.colormap_rgb.append([int(c * 255) for c in color_norm_rgb])
            
            # Para cv2.inRange, a cor precisa estar no mesmo range da imagem
            # color_uint8_rgb é o centroide do cluster (0-255)
            color_uint8_rgb_val = (color_norm_rgb * 255).astype(np.uint8)

            # Criar uma máscara para a cor exata na imagem quantizada (uint8)
            # np.all com axis=-1 é crucial para comparar todos os canais de cor
            mask = cv2.inRange(quantified_image_uint8_rgb, color_uint8_rgb_val, color_uint8_rgb_val)
            
            cnts, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
            # cnts = cnts[0] if len(cnts) == 2 else cnts[1] # Desnecessário com a nova assinatura de findContours

            for contour in cnts:
                if cv2.contourArea(contour) > 100: # Filtra contornos muito pequenos
                    # Desenha contornos na tela de pintura
                    cv2.drawContours(canvas_paint, [contour], -1, (0, 0, 0), 1) # Contorno preto
                    
                    # Adiciona número do índice (começando em 1)
                    # Tenta encontrar um bom lugar para o texto (ex: centróide do contorno)
                    M = cv2.moments(contour)
                    if M["m00"] != 0:
                        txt_x = int(M["m10"] / M["m00"])
                        txt_y = int(M["m01"] / M["m00"])
                        cv2.putText(canvas_paint, '{:d}'.format(ind + 1), (txt_x, txt_y),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1) # Texto preto
        
        # Retorna:
        # 1. canvas_paint: Imagem P&B numerada para pintar (uint8)
        # 2. colors_norm_rgb: Lista de cores da paleta (RGB, normalizado 0-1)
        # 3. quantified_image_uint8_rgb: Imagem segmentada com cores da paleta (RGB, uint8 0-255)
        return canvas_paint, colors_norm_rgb, quantified_image_uint8_rgb

    def resize(self):
        (height, width) = self.src_rgb.shape[:2]
        if height > width:  # modo retrato
            dim = (int(width * self.target_dimension_px / float(height)), self.target_dimension_px)
        else: # modo paisagem ou quadrado
            dim = (self.target_dimension_px, int(height * self.target_dimension_px / float(width)))
        
        # Garante que as dimensões não sejam zero
        if dim[0] == 0 or dim[1] == 0:
            # Fallback para um tamanho pequeno se o cálculo resultar em zero (ex: imagem de entrada muito pequena)
            min_dim = 100 # Define uma dimensão mínima segura
            if height > width:
                ratio = self.target_dimension_px / float(height) if height > 0 else 0
                new_width = int(width * ratio)
                dim = (max(1, new_width), self.target_dimension_px) if ratio > 0 else (min_dim, min_dim)
            else:
                ratio = self.target_dimension_px / float(width) if width > 0 else 0
                new_height = int(height * ratio)
                dim = (self.target_dimension_px, max(1, new_height)) if ratio > 0 else (min_dim, min_dim)

        return cv2.resize(self.src_rgb, dim, interpolation=cv2.INTER_AREA)

    def cleaning(self, picture_rgb):
        # picture_rgb é esperada como RGB uint8
        # cv2.fastNlMeansDenoisingColored espera BGR por padrão em algumas versões/documentações,
        # mas testes mostram que pode funcionar com RGB. Se houver problemas de cor, converter para BGR aqui.
        # temp_bgr = cv2.cvtColor(picture_rgb, cv2.COLOR_RGB2BGR)
        # denoised_bgr = cv2.fastNlMeansDenoisingColored(temp_bgr, None, 10, 10, 7, 21)
        # denoised_rgb = cv2.cvtColor(denoised_bgr, cv2.COLOR_BGR2RGB)
        
        # Usando diretamente com RGB:
        denoised_rgb = cv2.fastNlMeansDenoisingColored(picture_rgb, None, 10, 10, 7, 21)
        
        kernel = np.ones((5, 5), np.uint8)
        img_erosion_rgb = cv2.erode(denoised_rgb, kernel, iterations=1)
        img_dilation_rgb = cv2.dilate(img_erosion_rgb, kernel, iterations=1)
        return img_dilation_rgb

    def quantification(self, picture_norm_rgb):
        # picture_norm_rgb é RGB, float32, normalizado (0-1)
        width, height, depth = picture_norm_rgb.shape
        flattened_rgb = np.reshape(picture_norm_rgb, (width * height, depth))
        
        # Amostra para KMeans para eficiência
        sample_rgb = shuffle(flattened_rgb, random_state=42)[:1000] # random_state para reprodutibilidade
        
        kmeans = KMeans(n_clusters=self.nb_color, random_state=42, n_init='auto').fit(sample_rgb)
        labels = kmeans.predict(flattened_rgb)
        
        # kmeans.cluster_centers_ são as cores (RGB normalizado)
        new_img_norm_rgb = self.recreate_image(kmeans.cluster_centers_, labels, width, height)
        return new_img_norm_rgb, kmeans.cluster_centers_

    def recreate_image(self, codebook_norm_rgb, labels, width, height):
        # codebook_norm_rgb são os centroides (cores RGB normalizadas)
        # labels são os clusters para cada pixel
        # Reconstrói a imagem
        d = codebook_norm_rgb.shape[1]
        image = np.zeros((width * height, d), dtype=np.float32) # dtype float32
        for i in range(width * height):
            image[i] = codebook_norm_rgb[labels[i]]
        return np.resize(image, (width, height, d))


# --- Interface Streamlit ---
st.sidebar.title("Criação das Paletas de Cores e Tela Numerada")
st.sidebar.write("---")

st.sidebar.header("Informações do Autor")
try:
    st.sidebar.image("clube.png", use_container_width=True)
except Exception:
    st.sidebar.warning("Imagem 'clube.png' não encontrada. Coloque-a na mesma pasta do script.")
st.sidebar.write("Nome: Marcelo Claro")
st.sidebar.write("Email: marceloclaro@geomaker.org")
st.sidebar.write("WhatsApp: (88) 98158-7145")

st.sidebar.write("---")

st.sidebar.header("Configurações da Aplicação")
uploaded_file = st.sidebar.file_uploader("Escolha uma imagem", type=["jpg", "png", "jpeg"])
nb_color_slider = st.sidebar.slider('Escolha o número de cores para pintar', min_value=2, max_value=30, value=5, step=1) # Ajustado min_value e max_value
total_ml_slider = st.sidebar.slider('Escolha o total em ml da tinta por cor', min_value=10, max_value=1000, value=50, step=10)
target_dimension_slider = st.sidebar.slider(
    'Escolha a dimensão alvo da imagem processada (pixels)', 
    min_value=300, max_value=2000, value=800, step=50,
    help="A maior dimensão (largura ou altura) da imagem será ajustada para este valor, mantendo a proporção."
)


if st.sidebar.button('Gerar Paleta e Tela'):
    if uploaded_file is not None:
        try:
            pil_image = Image.open(uploaded_file)

            st.subheader("Informações da Imagem Original")
            st.image(pil_image, caption='Imagem Original Carregada', use_container_width=True)

            if 'dpi' in pil_image.info:
                dpi = pil_image.info['dpi']
                st.write(f"Resolução da imagem original: {dpi[0]:.0f}x{dpi[1]:.0f} DPI (pontos por polegada)")
                
                # Calcula a dimensão física de um pixel na imagem original
                cm_per_inch = 2.54
                if dpi[0] > 0:
                    cm_per_pixel_x = cm_per_inch / dpi[0]
                    st.write(f"Tamanho de cada pixel (largura) na original: {cm_per_pixel_x:.4f} cm")
                if dpi[1] > 0:
                    cm_per_pixel_y = cm_per_inch / dpi[1]
                    st.write(f"Tamanho de cada pixel (altura) na original: {cm_per_pixel_y:.4f} cm")
            else:
                st.write("Informação de DPI não encontrada na imagem original.")
            
            st.write(f"Dimensões originais: {pil_image.width}px x {pil_image.height}px")
            st.write("---")


            # Converter para RGB (removendo canal alfa se existir) e para array NumPy
            pil_image_rgb = pil_image.convert('RGB')
            src_np_rgb = np.array(pil_image_rgb)

            # Instanciar e gerar
            canvas_obj = Canvas(src_np_rgb, nb_color_slider, target_dimension_slider)
            # Retorna:
            # 1. result_paint_screen: Imagem P&B numerada para pintar (uint8, escala de cinza)
            # 2. colors_palette_norm_rgb: Lista de cores da paleta (RGB, normalizado 0-1)
            # 3. segmented_image_uint8_rgb: Imagem segmentada com cores da paleta (RGB, uint8 0-255)
            result_paint_screen, colors_palette_norm_rgb, segmented_image_uint8_rgb = canvas_obj.generate()
            
            st.subheader("Resultados do Processamento")
            st.image(segmented_image_uint8_rgb, caption='Imagem Segmentada (Cores Quantizadas)', use_container_width=True)
            
            # Download da imagem segmentada
            # cv2.imencode espera BGR por padrão para JPEGs.
            _, segmented_buffer = cv2.imencode('.png', cv2.cvtColor(segmented_image_uint8_rgb, cv2.COLOR_RGB2BGR))
            segmented_bytes = segmented_buffer.tobytes()
            st.download_button(
                label="Baixar Imagem Segmentada (.png)",
                data=segmented_bytes,
                file_name='imagem_segmentada.png',
                mime='image/png'
            )
            st.write("---")

            st.image(result_paint_screen, caption='Tela Numerada para Pintar', use_container_width=True)
            # Download da tela para pintar
            _, result_buffer = cv2.imencode('.png', result_paint_screen) # PNG para preservar detalhes P&B
            result_bytes_paint = result_buffer.tobytes()
            st.download_button(
                label="Baixar Tela para Pintar (.png)",
                data=result_bytes_paint,
                file_name='tela_para_pintar.png',
                mime='image/png'
            )
            st.write("---")

            if not colors_palette_norm_rgb:
                st.warning("Nenhuma paleta de cores foi gerada.")
            else:
                st.subheader("Paleta de Cores Gerada e Análise Junguiana")

                # Análise da Cor Dominante (primeira cor da paleta K-Means, pode não ser a mais prevalente em área)
                # Para uma cor dominante real, seria preciso calcular a área de cada cor.
                # Por ora, usamos a primeira cor da paleta como "representativa".
                if colors_palette_norm_rgb:
                    cor_representativa_norm_rgb = colors_palette_norm_rgb[0] # RGB 0-1
                    cor_jung_representativa = buscar_cor_proxima(cor_representativa_norm_rgb, cores_junguianas)
                    
                    if cor_jung_representativa and cor_jung_representativa['cor'] != 'N/A (dicionário vazio)':
                        st.markdown(f"**Análise Junguiana da Cor Representativa da Paleta: {cor_jung_representativa['cor']}**")
                        st.write(f"- Anima/Animus: {cor_jung_representativa['anima_animus']}")
                        st.write(f"- Sombra: {cor_jung_representativa['sombra']}")
                        st.write(f"- Personalidade: {cor_jung_representativa['personalidade']}")
                        st.write(f"- Diagnóstico: {cor_jung_representativa['diagnostico']}")
                    else:
                        st.write("Não foi possível encontrar uma análise Junguiana para a cor representativa ou o dicionário está incompleto.")
                    st.write("---")


                cols = st.columns(len(colors_palette_norm_rgb)) # Cria colunas para cada cor

                for i, color_norm_rgb_item in enumerate(colors_palette_norm_rgb):
                    color_uint8_rgb_item = [int(c * 255) for c in color_norm_rgb_item] # RGB 0-255
                    
                    with cols[i]:
                        st.markdown(f"**Cor {i+1}**")
                        # Bloco de cor para exibição
                        color_block_display = np.full((50, 50, 3), color_uint8_rgb_item, dtype=np.uint8)
                        st.image(color_block_display, caption=f"RGB: {tuple(color_uint8_rgb_item)}", width=100)

                        # Cálculo das proporções das cores CMYK
                        # rgb_to_cmyk espera r,g,b normalizados (0-1)
                        c, m, y, k = rgb_to_cmyk(color_norm_rgb_item[0], color_norm_rgb_item[1], color_norm_rgb_item[2])
                        c_ml, m_ml, y_ml, k_ml = calculate_ml(c, m, y, k, total_ml_slider)

                        st.markdown(f"**Dosagem para {total_ml_slider} ml:**")
                        st.write(f"- Ciano (C): {c_ml:.2f} ml")
                        st.write(f"- Magenta (M): {m_ml:.2f} ml")
                        st.write(f"- Amarelo (Y): {y_ml:.2f} ml")
                        st.write(f"- Preto (K): {k_ml:.2f} ml")
                        
                        # Análise Junguiana para esta cor específica
                        cor_jung_especifica = buscar_cor_proxima(color_norm_rgb_item, cores_junguianas)
                        if cor_jung_especifica and cor_jung_especifica['cor'] != 'N/A (dicionário vazio)':
                            st.markdown(f"**Análise Junguiana ({cor_jung_especifica['cor']}):**")
                            st.write(f"  - Anima/Animus: {cor_jung_especifica['anima_animus']}")
                            st.write(f"  - Sombra: {cor_jung_especifica['sombra']}")
                            # st.write(f"  - Personalidade: {cor_jung_especifica['personalidade']}") # Opcional, pode poluir
                            # st.write(f"  - Diagnóstico: {cor_jung_especifica['diagnostico']}") # Opcional
                        else:
                            st.write(f"  (Análise Junguiana não encontrada para esta cor específica)")
                        st.markdown("---")


        except Exception as e:
            st.error(f"Ocorreu um erro durante o processamento da imagem: {e}")
            st.error("Detalhes técnicos:")
            st.exception(e) # Mostra o traceback completo para debugging

    else:
        st.warning("Por favor, carregue uma imagem para gerar a paleta e a tela.")

else:
    st.info("Ajuste as configurações na barra lateral e clique em 'Gerar Paleta e Tela' após carregar uma imagem.")
