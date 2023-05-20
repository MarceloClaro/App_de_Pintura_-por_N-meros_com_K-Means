# Importando todas as coisas necessárias para o nosso programa funcionar.
import numpy as np
from sklearn.cluster import KMeans
from sklearn.utils import shuffle
import cv2
import streamlit as st
from PIL import Image
import io
import base64

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
            ratio = self.tar_width / float(height)
            dim = (int(width * ratio), self.tar_width)
        else:
            ratio = self.tar_width / float(width)
            dim = (self.tar_width, int(height * ratio))
        return cv2.resize(self.src, dim, interpolation=cv2.INTER_AREA)

    def cleaning(self, image):
        # Your cleaning logic here
        return image

    def quantification(self, image):
        w, h, d = tuple(image.shape)
        image_array = np.reshape(image, (w * h, d))
        image_array_sample = shuffle(image_array, random_state=0)[:1000]
        kmeans = KMeans(n_clusters=self.nb_color, random_state=0).fit(image_array_sample)
        labels = kmeans.predict(image_array)
        colors = kmeans.cluster_centers_
        quantified_image = np.reshape(labels, (w, h))
        quantified_image = np.array(quantified_image, dtype="uint8")
        quantified_image = cv2.cvtColor(quantified_image, cv2.COLOR_GRAY2RGB)
        return quantified_image, colors

def main():
    st.title("Pintura por Números")
    uploaded_file = st.file_uploader("Escolha uma imagem", type=["jpg", "jpeg", "png"])
    nb_color = st.slider("Número de cores", min_value=2, max_value=20, value=10, step=1)
    total_ml = st.slider("Total de tinta (ml)", min_value=10, max_value=1000, value=100, step=10)
    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        src = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        canvas = Canvas(src, nb_color)
        result, colors, segmented_image = canvas.generate()

        for ind, color in enumerate(colors):
            r, g, b = [int(c * 255) for c in color]
            c, m, y, k = rgb_to_cmyk(r, g, b)
            c_ml, m_ml, y_ml, k_ml = calculate_ml(c, m, y, k, total_ml)
            
            # Calcular a área da cor na imagem segmentada
            color_area = np.count_nonzero(np.all(segmented_image == color, axis=-1))
            total_area = segmented_image.shape[0] * segmented_image.shape[1]
            color_percentage = (color_area / total_area) * 100

            st.write(f"""
            PALETAS DE COR PARA: {total_ml:.2f} ml.

            A cor pode ser alcançada pela combinação das cores primárias do modelo CMYK, utilizando a seguinte dosagem:

            Ciano (Azul) (C): {c_ml:.2f} ml
            Magenta (Vermelho) (M): {m_ml:.2f} ml
            Amarelo (Y): {y_ml:.2f} ml
            Preto (K): {k_ml:.2f} ml
            
            Porcentagem dessa cor na imagem: {color_percentage:.2f}%

            """)

        st.image(result, channels="BGR", use_column_width=True)
        st.button('Baixar Imagem')

if __name__ == "__main__":
    main()
