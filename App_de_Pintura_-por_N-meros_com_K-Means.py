import streamlit as st
import numpy as np
import cv2
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


def load_image(file):
    img = cv2.cvtColor(np.array(file), cv2.COLOR_BGR2RGB)
    img = np.array(img, dtype=np.float64) / 255
    return img


def apply_kmeans(img, n_clusters):
    w, h, d = img.shape
    img_reshaped = np.reshape(img, (w * h, d))
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(img_reshaped)
    labels = kmeans.predict(img_reshaped)
    return kmeans.cluster_centers_, labels, w, h


def reconstruct_image(cluster_centers, labels, w, h):
    d = cluster_centers.shape[1]
    image = np.zeros((w, h, d))
    label_idx = 0
    for i in range(w):
        for j in range(h):
            image[i][j] = cluster_centers[labels[label_idx]]
            label_idx += 1
    return image


def apply_canny(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img_gray = (img_gray * 255).astype(np.uint8)
    edges = cv2.Canny(img_gray, 100, 200)
    edges = np.where(edges == 255, 0, 255)
    return edges


def add_numbers(img, edges, cluster_centers, labels, font_size):
    mean_sort = sorted(cluster_centers, key=lambda x: sum(x))
    w, h, d = img.shape
    size_x, size_y = font_size * 2, font_size * 2

    for round in range(len(mean_sort)):
        for y_ in range(0, w, size_y):
            for x_ in range(0, h, size_x):
                if sum(img[y_][x_]) == sum(mean_sort[round]):
                    if np.all(edges[y_:y_ + size_y, x_:x_ + size_x] == 255):
                        cv2.putText(
                            img,
                            str(round + 1),
                            (x_, y_ + size_y // 2),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            font_size / 20,
                            (0, 0, 0, 0),
                            1,
                        )
                        break
    return img


def main():
    st.title("Paint by Numbers with K-means")

    uploaded_file = st.file_uploader("Escolha uma imagem:", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        img = load_image(uploaded_file)

        st.image(img, caption="Imagem original", use_column_width=True)

        n_clusters = st.slider("Quantidade de clusters:", min_value=2, max_value=50, value=10, step=1)
        font_size = st.slider("Tamanho da fonte dos números:", min_value=5, max_value=40, value=17, step=1)

        cluster_centers, labels, w, h = apply_kmeans(img, n_clusters)
        img_kmean = reconstruct_image(cluster_centers, labels, w, h)

        st.image(img_kmean, caption="Imagem após K-means", use_column_width=True)

        edges = apply_canny(img)

        st.image(edges, caption="Detecção de borda com Canny", use_column_width=True)

        img_numbered = add_numbers(img_kmean.copy(), edges, cluster_centers, labels, font_size)

        st.image(img_numbered, caption="Imagem final com números", use_column_width=True)


if __name__ == "__main__":
    main()
