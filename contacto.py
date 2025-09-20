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
    st.write("contacto@tuempresa.com")  # <-- Cambia por tu correo real

    st.subheader("👥 Nuestro equipo")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Nombre 1**")
        st.write("Cargo / Rol")

    with col2:
        st.markdown("**Nombre 2**")
        st.write("Cargo / Rol")

# Footer
st.markdown("---")
st.caption("© 2025 Tu Empresa. Todos los derechos reservados.")
