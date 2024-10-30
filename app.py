import streamlit as st
import requests
import os
import pandas as pd
import matplotlib.pyplot as plt
import pickle

# Configuration de Streamlit
st.set_page_config(page_title='Moteur de Recherche d\'Images', layout='wide')

def main():
    st.title("Moteur de Recherche d'Images")

    # Formulaire de téléversement
    st.sidebar.header("Téléversez une Image")
    uploaded_file = st.sidebar.file_uploader("Choisissez une image...", type=["jpg", "jpeg", "png"])

    # Sélecteurs pour le descripteur et la distance
    descriptor_choice = st.sidebar.selectbox("Choisissez le descripteur", ["GLCM", "BitDesc"])
    distance_choice = st.sidebar.selectbox("Choisissez la distance", ["Manhattan", "Canberra", "Euclidean", "Chebyshev"])

    if uploaded_file:
        # Sauvegarder l'image téléversée
        image_path = os.path.join('static/uploads', uploaded_file.name)
        with open(image_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        
        st.image(image_path, caption='Image Téléversée', width=300)  # Modifier la taille de l'image téléversée
        
        # Effectuer la recherche
        if st.sidebar.button('Rechercher des Images Similaires'):
            data = {'descriptor': descriptor_choice, 'distance': distance_choice}
            files = {'file': open(image_path, 'rb')}
            response = requests.post("http://127.0.0.1:5001/api/search", data=data, files=files)
            
            if response.status_code == 200:
                results = response.json()
                
                # Afficher les images similaires
                st.header("Top 10 Images Similaires")
                if 'similar_images' in results:
                    images = results['similar_images']
                    
                    # Organiser les images en colonnes
                    cols = st.columns(5)  # Nombre de colonnes, ajustez selon vos besoins
                    for index, result in enumerate(images):
                        col = cols[index % 5]
                        col.image(result['image_path'], caption=f"Distance: {result['distance']}", width=150)  # Modifier la taille des images similaires
                
if __name__ == "__main__":
    main()
