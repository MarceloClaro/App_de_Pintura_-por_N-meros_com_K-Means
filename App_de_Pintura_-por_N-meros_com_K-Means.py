import streamlit as st
import numpy as np
import cv2
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def load_image(file):
    file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = np.array(img, dtype=np.float64) / 255
    return img

def apply_kmeans(img, n_clusters):
    w, h, d = original_shape = tuple(img.shape)
    img = np.reshape(img, (w * h, d))
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(img)
    labels = kmeans.predict(img)
    return kmeans.cluster_centers_, labels, w, h

def reconstruct_image(mean_colors, labels, w, h):
    image = np.zeros((w, h, mean_colors.shape[1]))
    label_idx = 0
    for i in range(w):
        for j in range(h):
            image[i][j] = mean_colors[labels[label_idx]]
            label_idx += 1
    return image

def apply_canny(img):
    img = cv2.imread("img.png", 0)
    edges = cv2.Canny(img,100,200)
    for i in range(edges.shape[0]):
        for j in range(edges.shape[1]):
            if (edges[i][j] == 0):
                edges[i][j] = 255
            elif (edges[i][j] == 255):
                edges[i][j] = 0
    return edges

def add_numbers(img, edges, cluster_centers, labels, font_size):
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if edges[i][j] == 255:
                cv2.putText(img, str(labels[i]), (j, i), cv2.FONT_HERSHEY_SIMPLEX, font_size, (0, 0, 0), 2)
    return img

def main():
    st.title("App de Pintura por Números com K-means")

    uploaded_file = st.file_uploader("Escolha uma imagem...", type="jpg")
    if uploaded_file is not None:
        img = load_image(uploaded_file)
        st.image(img, caption="Imagem original", use_column_width=True)

        n_clusters = st.slider("Escolha a quantidade de clusters", min_value=1, max_value=20, value=10)
        font_size = st.slider("Escolha o tamanho da fonte", min_value=1, max_value=5, value=2)

        cluster_centers, labels, w, h = apply_kmeans(img, n_clusters)
        img_kmean = reconstruct_image(cluster_centers, labels, w, h)

        st.image(img_kmean, caption="Imagem após K-means", use_column_width=True)

        edges = apply_canny(img)

        st.image(edges, caption="Detecção de borda com Canny", use_column_width=True)

        img_numbered = add_numbers(img_kmean.copy(), edges, cluster_centers, labels, font_size)

        st.image(img_numbered, caption="Imagem final com números", use_column_width=True)

if __name__ == "__main__":
    main()
