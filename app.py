import streamlit as st
from calculadora import precio_total, Configuracion

# Configuración de la app
st.set_page_config(page_title="Calculadora de precios 3D", page_icon="🖨️", layout="centered")

st.title("🖨️ Next Dimension 3D")
st.write("Calculadora de precios de impresión 3D")

# --- Configuración por defecto ---
cfg = Configuracion()

st.subheader("⚙️ Configuración de costes")
cfg.precio_kw = st.number_input("💡 Precio por kWh (€)", value=cfg.precio_kw, min_value=0.0, step=0.01)
cfg.consumo_maquina = st.number_input("⚡ Consumo de la máquina (kW)", value=cfg.consumo_maquina, min_value=0.0, step=0.01)
cfg.precio_cambio_filamento = st.number_input("🎨 Precio cambio de filamento (€)", value=cfg.precio_cambio_filamento, min_value=0.0, step=0.01)
cfg.precio_mantenimiento = st.number_input("🛠️ Precio mantenimiento (€)", value=cfg.precio_mantenimiento, min_value=0.0, step=0.01)
cfg.precio_hora_diseno = st.number_input("✏️ Precio por hora de diseño (€)", value=cfg.precio_hora_diseno, min_value=0.0, step=0.01)
cfg.precio_hora_post = st.number_input("🔧 Precio por hora de postprocesado (€)", value=cfg.precio_hora_post, min_value=0.0, step=0.01)

# --- Datos del trabajo ---
st.subheader("📦 Datos del trabajo de impresión")

tipo_filamento = st.selectbox("Tipo de filamento", ["PLA", "PETG", "PLA-plus"])
tiempo_impresion = st.text_input("⏱️ Tiempo de impresión (ej: 3h12m)", "1h0m")
cantidad_filamento = st.number_input("📏 Cantidad de filamento (g)", min_value=0.0, step=0.1)
cambios_filamento = st.number_input("🔄 Cambios de filamento", min_value=0, step=1)
tiempo_diseño = st.number_input("✏️ Tiempo de diseño (h)", min_value=0.0, step=0.1)
tiempo_postprocesado = st.number_input("🔧 Tiempo de postprocesado (h)", min_value=0.0, step=0.1)
unidades = st.number_input("📦 Número de unidades", min_value=1, step=1)

# --- Botón para calcular ---
if st.button("Calcular precio"):
    coste_total, coste_unitario, coste_impresion, coste_mano_obra, beneficio, beneficio_por_hora, beneficio_por_unidad = precio_total(
        tipo_filamento,
        tiempo_impresion,
        cantidad_filamento,
        cambios_filamento,
        tiempo_diseño,
        tiempo_postprocesado,
        unidades,
        cfg
    )

    st.subheader("📊 Resultados")
    col1, col2, col3 = st.columns(4)
    with col1:
        st.metric("💰 Coste total", f"{coste_total:.2f} €")
        st.metric("🖨️ Coste de impresión", f"{coste_impresion:.2f} €")
    with col2:
        st.metric("📦 Coste unitario", f"{coste_unitario:.2f} €")
        st.metric("👷 Mano de obra", f"{coste_mano_obra:.2f} €")
    with col3:
        st.metric("📈 Beneficio", f"{beneficio:.2f} €")
        st.metric("⏳ Beneficio por hora", f"{beneficio_por_hora:.2f} €/h")
    with col4:
        st.metric("🧩 Beneficio por unidad", f"{beneficio_por_unidad:.2f} €/unidad")
