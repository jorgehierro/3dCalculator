import streamlit as st
from calculadora import precio_total, Configuracion
from utils import leer_gcode, leer_parametros

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

#tipo_filamento = st.selectbox("Tipo de filamento", ["PLA", "PETG", "PLA-plus"])
num_tandas = st.number_input("🔄 Número de tandas de impresión", min_value=1, step=1, value=1)

# Guardar datos de cada tanda
tandas = []
for i in range(num_tandas):
    st.markdown(f"### 🖨️ Tanda {i+1}")

    modo = st.radio(
        f"📥 ¿Cómo introducir los datos de la tanda {i+1}?",
        ["Subir archivo .gcode", "Introducir manualmente"],
        key=f"modo{i}"
    )

    tiempo_impresion, gramos, tipo_filamento = None, None, None

    if modo == "Subir archivo .gcode":
        uploaded_file = st.file_uploader(
            "📂 Arrastra o sube el archivo .gcode",
            type=["gcode"],
            key=f"gcode{i}"
        )
        if uploaded_file:
            contenido = leer_gcode(uploaded_file)
            tiempo_impresion, tipo_filamento, gramos = leer_parametros(contenido)

            # --- Preview de parámetros detectados ---
            with st.expander(f"👀 Preview parámetros detectados en Tanda {i+1}", expanded=True):
                st.write(f"⏱️ **Tiempo de impresión:** {tiempo_impresion}")
                st.write(f"📏 **Filamento usado:** {gramos} g")
                st.write(f"🎨 **Tipo de filamento:** {tipo_filamento}")

    else:  # Manual
        tiempo_impresion = st.text_input(
            f"⏱️ Tiempo de impresión (ej: 3h12m) - Tanda {i+1}",
            "1h0m",
            key=f"t{i}"
        )
        gramos = st.number_input(
            f"📏 Cantidad de filamento (g) - Tanda {i+1}",
            min_value=0.0,
            step=0.1,
            key=f"f{i}"
        )
        tipo_filamento = st.selectbox(
            f"🎨 Tipo de filamento - Tanda {i+1}",
            ["PLA", "PETG", "ABS", "PLA-plus"],
            key=f"fil{i}"
        )

    # Campos comunes
    cambios_filamento = st.number_input(f"🔄 Cambios de filamento - Tanda {i+1}", min_value=0, step=1, key=f"c{i}")
    tiempo_diseño = st.number_input(f"✏️ Tiempo de diseño (h) - Tanda {i+1}", min_value=0.0, step=0.1, key=f"d{i}")
    tiempo_postprocesado = st.number_input(f"🔧 Tiempo de postprocesado (h) - Tanda {i+1}", min_value=0.0, step=0.1, key=f"p{i}")
    unidades = st.number_input(f"📦 Número de unidades - Tanda {i+1}", min_value=1, step=1, key=f"u{i}")

    # Guardar tanda (aunque no tenga cálculos aún)
    tandas.append({
        "tiempo_impresion": tiempo_impresion,
        "tipo_filamento": tipo_filamento,
        "cantidad_filamento": gramos,
        "cambios_filamento": cambios_filamento,
        "tiempo_diseño": tiempo_diseño,
        "tiempo_postprocesado": tiempo_postprocesado,
        "unidades": unidades
    })

# --- Botón para calcular ---
if st.button("Calcular precio"):
    total_coste = total_unitario = total_impresion = 0
    total_mano_obra = total_beneficio = 0
    total_unidades = 0
    total_beneficio_hora = []
    total_beneficio_unidad = []

    st.subheader("📊 Resultados por tanda")

    for i, t in enumerate(tandas):
        # Solo calcular si hay datos completos
        if not t["tiempo_impresion"] or not t["tipo_filamento"] or t["cantidad_filamento"] is None:
            st.warning(f"⚠️ La tanda {i+1} no tiene datos suficientes para calcular.")
            continue

        coste_total, coste_unitario, coste_impresion, coste_mano_obra, beneficio, beneficio_por_hora, beneficio_por_unidad = precio_total(
            t["tipo_filamento"],
            t["tiempo_impresion"],
            t["cantidad_filamento"],
            t["cambios_filamento"],
            t["tiempo_diseño"],
            t["tiempo_postprocesado"],
            t["unidades"],
            cfg
        )

        # Mostrar métricas por tanda
        st.markdown(f"#### 📊 Resultados Tanda {i+1}")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("💰 Coste total", f"{coste_total:.2f} €")
            st.metric("🖨️ Coste de impresión", f"{coste_impresion:.2f} €")
        with col2:
            st.metric("📦 Coste unitario", f"{coste_unitario:.2f} €")
            st.metric("👷 Mano de obra", f"{coste_mano_obra:.2f} €")
        st.write("---")

        # Acumular totales
        total_coste += coste_total
        total_impresion += coste_impresion
        total_mano_obra += coste_mano_obra
        total_beneficio += beneficio
        total_unidades += t["unidades"]
        total_beneficio_hora.append(beneficio_por_hora)
        total_beneficio_unidad.append(beneficio_por_unidad)

    # --- Resultados globales ---
    if total_unidades > 0:
        st.subheader("📊 Resultados totales")
        col3, col4 = st.columns(2)
        with col3:
            st.metric("💰 Coste total", f"{total_coste:.2f} €")
            st.metric("🖨️ Coste de impresión", f"{total_impresion:.2f} €")
        with col4:
            st.metric("📦 Unidades totales", f"{total_unidades}")
            st.metric("👷 Mano de obra total", f"{total_mano_obra:.2f} €")

        st.subheader("📊 Beneficios globales")
        col5, col6 = st.columns(2)
        with col5:
            st.metric("📈 Beneficio total", f"{total_beneficio:.2f} €")
            st.metric("⏳ Beneficio medio por hora", f"{sum(total_beneficio_hora)/len(total_beneficio_hora):.2f} €/h")
        with col6:
            st.metric("🧩 Beneficio medio por unidad", f"{sum(total_beneficio_unidad)/len(total_beneficio_unidad):.2f} €/unidad")
            st.metric(" 📈 Beneficio porcentual", f"{(total_beneficio/total_coste*100) if total_coste else 0:.2f} %")
