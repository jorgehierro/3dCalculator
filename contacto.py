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
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Jorge Fernández-Paniagua Moreno**")
        st.write("📱: 67480520")

    with col2:
        st.markdown("**Jorge Hierro Francoy**")
        st.write("📱: 606982635")

# Footer
st.markdown("---")
st.caption("© 2025 Next3Dimension. Todos los derechos reservados.")
