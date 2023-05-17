import streamlit as st
import numpy as np
import cv2
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def load_image(file):
    file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_rgb = np.array(img_rgb, dtype=np.float64) / 255
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img_rgb, img_gray

def apply_kmeans(img, n_clusters):
    w, h, d = original_shape = tuple(img.shape)
    img = np.reshape(img, (w * h, d))
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(img)
    labels = kmeans.predict(img)
    return kmeans.cluster_centers_, labels, w, h

def reconstruct_image(cluster_centers, labels, w, h):
    image = np.zeros((w, h, cluster_centers.shape[1]))
    label_idx = 0
    for i in range(w):
        for j in range(h):
            image[i][j] = cluster_centers[labels[label_idx]]
            label_idx += 1
    return image

def apply_canny(img):
    edges = cv2.Canny(img,100,200)
    for i in range(edges.shape[0]):
        for j in range(edges.shape[1]):
            if (edges[i][j] == 255):
                edges[i][j] = 0
            else:
                edges[i][j] = 255
    return edges

def plot_color_image(img, color, cluster_number):
    mask = np.all(img == color, axis=-1)
    plt.imshow(mask[..., None] * img + (1 - mask[..., None]) * np.ones_like(img))
    plt.title(f'Cor do cluster {cluster_number}')
    st.pyplot(plt)

def add_text_to_image(img, x, y, text, font_size):
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, font_size, (0, 0, 0), 2)

def add_cluster_numbers_to_edges(img, edges, cluster_centers, labels, w, h, size_x, size_y):
    for cluster_number, color in enumerate(cluster_centers):
        plot_color_image(img, color, cluster_number)
        for y in range(h):
            for x in range(w):
                if np.all(img[y, x] == color):
                    if np.all(edges[max(0, y - size_y // 2):min(h, y + size_y // 2),
                                     max(0, x - size_x // 2):min(w, x + size_x // 2)] == 255):
                        add_text_to_image(img, x, y, str(cluster_number), 1)

def main():
    st.title("App de Pintura por Números com K-means")

    uploaded_file = st.file_uploader("Escolha uma imagem...", type="jpg")
    if uploaded_file is not None:
        img_rgb, img_gray = load_image(uploaded_file)
        st.image(img_rgb, caption="Imagem original", use_column_width=True)

        n_clusters = st.slider("Escolha a quantidade de clusters", min_value=1, max_value=10, step=1, value=3)

        cluster_centers, labels, w, h = apply_kmeans(img_rgb, n_clusters)
        img_kmean = reconstruct_image(cluster_centers, labels, w, h)
        st.image(img_kmean, caption="Imagem após K-means", use_column_width=True)

        edges = apply_canny(img_gray)
        st.image(edges, caption="Detecção de borda com Canny", use_column_width=True)

        add_cluster_numbers_to_edges(img_kmean, edges, cluster_centers, labels, w, h, 20, 20)
        st.image(img_kmean, caption="Imagem final com números", use_column_width=True)

if __name__ == "__main__":
    main()
