import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D

@st.cache
def load_image(image_file):
    img = cv2.imdecode(np.fromstring(image_file.read(), np.uint8), 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

def apply_canny(image, min_val, max_val):
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(image, min_val, max_val, apertureSize = 3)
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

def plot_colors(colors):
    r = [color[0] for color in colors]
    g = [color[1] for color in colors]
    b = [color[2] for color in colors]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(r, g, b, c=colors/255.0)

    ax.set_xlabel('Red')
    ax.set_ylabel('Green')
    ax.set_zlabel('Blue')

    st.pyplot(fig)

def main():
    st.title("App de Pintura por Números com K-Means")

    uploaded_file = st.file_uploader("Escolha uma imagem...", type=['png', 'jpg'])
    if uploaded_file is not None:
        img = load_image(uploaded_file)
        st.image(img, caption='Imagem Original.', use_column_width=True)

        number_of_clusters = st.slider("Número de Cores", 2, 55, 5)

        img_to_process = img.reshape((-1, 3))
        kmeans = KMeans(n_clusters=number_of_clusters)
        labels = kmeans.fit_predict(img_to_process)
        img_kmean = kmeans.cluster_centers_[kmeans.labels_]

        cluster_centers = kmeans.cluster_centers_
        cluster_labels = kmeans.labels_

        img_kmean = img_kmean.reshape(img.shape).astype('uint8')

        st.image(img_kmean, caption='Imagem processada.', use_column_width=True)

        min_val = st.slider("Valor mínimo do limiar para Canny", 0, 255, 30)
        max_val = st.slider("Valor máximo do limiar para Canny", 0, 255, 100)

        edges = apply_canny(img_kmean, min_val, max_val)
        st.image(edges, caption='Bordas da Imagem.', use_column_width=True)

        inverted_edges = invert_colors(edges)
        st.image(inverted_edges, caption='Imagem com cores invertidas.', use_column_width=True)

        h, w = img.shape[:2]
        add_cluster_numbers_to_edges(img_kmean, inverted_edges, cluster_centers, labels, w, h, 20, 20)
        st.image(img_kmean, caption='Imagem final.', use_column_width=True)

        colors = [tuple(map(lambda x: x/255, center)) for center in cluster_centers]
        plot_colors(np.array(colors))

if __name__ == "__main__":
    main()
