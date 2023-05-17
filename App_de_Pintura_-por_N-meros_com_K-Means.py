import streamlit as st
import numpy as np
import cv2
from sklearn.cluster import KMeans
from matplotlib import pyplot as plt

def adjust_image(mean_color_from_model, labels, w, h):
    d = mean_color_from_model.shape[1]
    image = np.zeros((w, h, d))
    label_idx = 0
    for i in range(w):
        for j in range(h):
            image[i][j] = mean_color_from_model[labels[label_idx]]
            label_idx += 1
    return image

def put_text(img_plt, text, x, y, font_size):
    cv2.putText(img_plt, str(text), (x,y), cv2.FONT_HERSHEY_SIMPLEX, font_size, (0, 0, 0, 0), 2)

def check_bool(x, y, size_x, size_y, edges_image): 
    for i in range(y, y + size_y):
        for j in range(x, x+ size_x):
            try:
                if edges_image[j][i] != 255: #if not white
                    return False
            except:
                pass
    return True

st.title("Paint by numbers com KMeans")
uploaded_file = st.file_uploader("Escolha uma imagem", type=['png', 'jpg'])

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    st.image(img, caption='Imagem original.', use_column_width=True)

    w, h, d = original_shape = tuple(img.shape)
    img_array = np.reshape(img, (w * h, d))

    n_clusters = st.slider('Número de clusters', min_value=1, max_value=30, value=10)
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(img_array)
    labels = kmeans.predict(img_array)

    img_kmean = adjust_image(kmeans.cluster_centers_, labels, w, h)
    st.image(img_kmean, caption='Imagem após KMeans.', use_column_width=True)

    img_gray = cv2.imdecode(file_bytes, 0)
    edges = cv2.Canny(img_gray,100,200)
    st.image(edges, caption='Imagem de borda.', use_column_width=True)

    edges[edges == 0] = 255
    edges[edges == 255] = 0

    size_x = 17
    size_y = 17
    copy_edge = edges.copy()
    color_edge = img_kmean.copy()
    y, x, d = color_edge.shape
    mean_sort = sorted(kmeans.cluster_centers_, key=lambda x: sum(x))

    font_size = st.slider('Tamanho da fonte', min_value=0.1, max_value=2.0, value=0.4)

    for round in range(len(mean_sort)):
        for y_ in range(0, y, size_y): 
            for x_ in range(0, x, size_x): 
                if sum(color_edge[y_][x_]) == sum(mean_sort[round]): 
                    status = check_bool(x_, y_, size_x, size_y, copy_edge) 
                    if status == True: 
                        put_text(copy_edge, round+1, x_, y_, font_size)
                        break

    st.image(copy_edge, caption='Imagem final.', use_column_width=True)
