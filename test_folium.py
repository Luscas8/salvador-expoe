import folium

# Criar um mapa
m = folium.Map(location=[-12.9714, -38.5014], zoom_start=13)

# Adicionar um marcador
folium.Marker(
    [-12.9714, -38.5014],
    popup='Salvador',
    tooltip='Salvador'
).add_to(m)

# Salvar o mapa
m.save('teste_mapa.html') 