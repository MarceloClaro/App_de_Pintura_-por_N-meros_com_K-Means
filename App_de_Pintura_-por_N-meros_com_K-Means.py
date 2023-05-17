import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

@st.cache
def load_image(image_file):
    img = cv2.imdecode(np.fromstring(image_file.read(), np.uint8), 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

def apply_canny(image):
    if len(image.shape) == 3: # Se a imagem é colorida, converta para escala de cinza
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(image, 50, 150, apertureSize = 3)
    return edges

def invert_colors(image):
    return 255 - image

def add_text_to_image(img, x, y, text, size):
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, size, (255, 255, 255), 2, cv2.LINE_AA)

def add_cluster_numbers_to_edges(img, edges, cluster_centers, labels, w, h, size_x, size_y):
    for cluster_number, color in enumerate(cluster_centers):
        for y in range(h):
            for x in range(w):
                if np.all(img[y, x] == color):
                    if np.all(edges[y: min(h, y + size_y // 2), x: min(w, x + size_x // 2)] == 255):
                        add_text_to_image(img, x, y, str(cluster_number), 1)

def main():
    st.title("App de Pintura por Números com K-Means")

    uploaded_file = st.file_uploader("Escolha uma imagem...", type=['png', 'jpg'])
    if uploaded_file is not None:
        img = load_image(uploaded_file)
        st.image(img, caption='Imagem Original.', use_column_width=True)

        number_of_clusters = st.slider("Número de Cores", 2, 15, 5)

        img_to_process = img.reshape((-1, 3))
        kmeans = KMeans(n_clusters=number_of_clusters)
        labels = kmeans.fit_predict(img_to_process)
        img_kmean = kmeans.cluster_centers_[kmeans.labels_]

        cluster_centers = kmeans.cluster_centers_
        cluster_labels = kmeans.labels_

        img_kmean = img_kmean.reshape(img.shape).astype('uint8')

        st.image(img_kmean, caption='Imagem processada.', use_column_width=True)

        edges = apply_canny(img_kmean)
        st.image(edges, caption='Imagem com bordas.', use_column_width=True)

        inverted_edges = invert_colors(edges)
        st.image(inverted_edges, caption='Imagem com cores invertidas.', use_column_width=True)

        h, w = img.shape[:2]
        add_cluster_numbers_to_edges(img_kmean, inverted_edges, cluster_centers, cluster_labels, w, h, 20, 20)
        st.image(img_kmean, caption='Imagem final.', use_column_width=True)

if __name__ == "__main__":
    main()
