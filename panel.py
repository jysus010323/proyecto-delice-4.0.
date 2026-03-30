import streamlit as st
import pandas as pd
import numpy as np
import time

# 1. Configuración de la página
st.set_page_config(page_title="Dashboard Industria 4.0 - Délice", layout="wide")

st.title("🏭 Panel de Control 4.0: Gemelo Digital del Horno")
st.markdown("Monitor en tiempo real de la transferencia de calor y humedad en la línea continua.")

# 2. Generación de datos simulados (Simulando el Filtro de Kalman / Sensor Virtual)
# Zonas térmicas: Zona 1 (160°C), Zona 2 (185°C), Zona 3 (170°C)
tiempo = pd.date_range(start="2026-03-29 07:00:00", periods=20, freq="1min")
datos_horno = pd.DataFrame({
    'Tiempo': tiempo,
    'Zona 1 - Expansión (°C)': np.random.normal(160, 2, 20),
    'Zona 2 - Cocción (°C)': np.random.normal(185, 1.5, 20),
    'Zona 3 - Secado (°C)': np.random.normal(170, 2, 20),
    'Humedad Núcleo (%)': np.random.normal(15, 0.5, 20) # Target: 14% - 16%
}).set_index('Tiempo')

# 3. Métricas Principales (KPIs Operativos y Energéticos)
st.subheader("Estado Actual del Proceso (Control Predictivo MPC)")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Producción Actual", "5,000 un/h", "Óptimo")
col2.metric("Humedad del Bizcocho", "14.8 %", "-0.2% vs Setpoint", delta_color="normal")
col3.metric("Tiempo de Residencia", "11.5 min", "Estable")
col4.metric("Ahorro Energético (ROI)", "15.2 %", "+0.2% proyectado")

st.divider()

# 4. Gráficos de Monitoreo Termodinámico
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    st.markdown("### Perfil Térmico del Horno (Zonas 1-3)")
    st.write("Datos del Gemelo Digital evaluando el flujo de calor total ($q$).")
    st.line_chart(datos_horno[['Zona 1 - Expansión (°C)', 'Zona 2 - Cocción (°C)', 'Zona 3 - Secado (°C)']])

with col_graf2:
    st.markdown("### Sensor Virtual: Humedad del Núcleo")
    st.write("Estimación de estados para garantizar gelatinización a 95°C.")
    # Resaltamos visualmente si se sale del rango 14-16%
    st.area_chart(datos_horno['Humedad Núcleo (%)'], color="#ffaa00")

# 5. Interfaz de Decisión (Simulación del Lazo de Control)
st.subheader("Alertas del Edge Computing")
humedad_actual = datos_horno['Humedad Núcleo (%)'].iloc[-1]

if humedad_actual < 14.0:
    st.error(f"⚠️ Alerta MPC: Humedad proyectada baja ({humedad_actual:.2f}%). Aumentando velocidad de banda en 0.5 m/min.")
elif humedad_actual > 16.0:
    st.warning(f"⚠️ Alerta MPC: Humedad proyectada alta ({humedad_actual:.2f}%). Aumentando extracción de aire.")
else:
    st.success("✅ Estabilidad termodinámica alcanzada. Interacción físico-química con la crema garantizada.")
    
# Mostrar tabla de datos puros para el operador
with st.expander("Ver telemetría detallada (Datos Crudos)"):
    st.dataframe(datos_horno.style.highlight_max(axis=0))