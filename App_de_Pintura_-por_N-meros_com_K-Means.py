import streamlit as st
import numpy as np
import cv2
from sklearn.cluster import KMeans
from matplotlib import pyplot as plt

def load_image(image_file):
    img = cv2.imdecode(np.fromstring(image_file.read(), np.uint8), 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

def process_image(img, n_clusters, font_size):
    img = np.array(img, dtype=np.float64) / 255
    w, h, d = original_shape = tuple(img.shape)
    image_array = np.reshape(img, (w * h, d))
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(image_array)
    labels = kmeans.predict(image_array)
    
    new_image = adjust_image(kmeans.cluster_centers_, labels, w, h, font_size)
    return new_image

def adjust_image(mean_color_from_model, labels, w, h, font_size):
    d = mean_color_from_model.shape[1]
    image = np.zeros((w, h, d))
    label_idx = 0
    for i in range(w):
        for j in range(h):
            image[i][j] = mean_color_from_model[labels[label_idx]]
            label_idx += 1
    return image

def main():
    st.title("App de Pintura por Números com K-Means")
    
    image_file = st.file_uploader("Carregar Imagem", type=['jpeg', 'png', 'jpg'])
    n_clusters = st.number_input("Escolha o número de clusters", min_value=2, max_value=60, value=10, step=1)
    font_size = st.number_input("Escolha o tamanho da fonte", min_value=0.1, max_value=5.0, value=1.0, step=0.1)

    if image_file is not None:
        img = load_image(image_file)
        st.image(img, caption='Imagem Carregada.', use_column_width=True)
        new_img = process_image(img, n_clusters, font_size)
        st.image(new_img, caption='Imagem Processada.', use_column_width=True)

if __name__ == "__main__":
    main()
