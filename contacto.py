import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Contacto",
    page_icon="📬",
    layout="centered"
)

# Título principal
st.title("📬 Contacto")

st.write("Bienvenido a nuestra página de contacto. Aquí encontrarás nuestra información corporativa:")

# Tarjetas de contacto
with st.container():
    st.subheader("📧 Correo corporativo")
    st.write("next3ddimension@gmail.com")  # <-- Cambia por tu correo real

    st.subheader("👥 Nuestro equipo")
    st.write("**Jorge Fernández-Paniagua Moreno** – 📱: 67480520")
    st.write("**Jorge Hierro Francoy** – 📱: 606982635")

# Footer
st.markdown("---")
st.caption("© 2025 Next3Dimension. Todos los derechos reservados.")
