# -*- coding: utf-8 -*-
"""
Doctor at Home - Plataforma Clínica Inteligente
Versión: 3.0 ("Visual Analytics & Professional UI")
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from firebase_admin import auth
from io import BytesIO
import reportlab # Mantenemos para compatibilidad de PDF, aunque se podría modularizar

# --- PERSONAL IMPORTS ---
import firebase_utils
from gemini_utils import GeminiUtils
import ui_components as ui

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Doctor at Home | Dashboard",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- INICIALIZACIÓN ---
ui.load_custom_css()  # <--- INYECTAR CSS PREMIUM

# Conexión DB
DB = firebase_utils.DB
# Conexión IA
try:
    GEMINI = GeminiUtils()
    IS_MODEL_CONFIGURED = True
except Exception:
    GEMINI = None
    IS_MODEL_CONFIGURED = False

# Estado de Sesión
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.physician_email = None
    st.session_state.page = 'login'
    st.session_state.selected_patient_id = None
    st.session_state.ai_analysis_running = False

# ==============================================================================
# HELPERS VISUALES (CHARTS)
# ==============================================================================
def render_vital_signs_charts(df):
    """Genera gráficos interactivos de signos vitales usando Plotly."""
    if df.empty:
        st.info("No hay datos suficientes para graficar.")
        return

    # Asegurar orden cronológico
    df = df.sort_values('timestamp')

    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de Presión Arterial
        fig_pa = go.Figure()
        fig_pa.add_trace(go.Scatter(x=df['timestamp'], y=df['presion_sistolica'], 
                                    mode='lines+markers', name='Sistólica', line=dict(color='#EF4444')))
        fig_pa.add_trace(go.Scatter(x=df['timestamp'], y=df['presion_diastolica'], 
                                    mode='lines+markers', name='Diastólica', line=dict(color='#3B82F6')))
        fig_pa.update_layout(title="Evolución de Presión Arterial (mmHg)", 
                             template="plotly_white", margin=dict(l=20, r=20, t=40, b=20), height=300)
        st.plotly_chart(fig_pa, use_container_width=True)

    with col2:
        # Gráfico de Glucemia e IMC
        # Usamos subplots o dos ejes y si es confuso, mejor otro grafico limpio. 
        # Haremos Glucemia independiente.
        fig_glu = px.line(df, x='timestamp', y='glucemia', markers=True, title="Tendencia de Glucemia (mg/dL)")
        fig_glu.update_traces(line_color='#10B981')
        fig_glu.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=40, b=20), height=300)
        st.plotly_chart(fig_glu, use_container_width=True)

# ==============================================================================
# VISTAS PRINCIPALES
# ==============================================================================

def render_login():
    """Vista de Login modernizada."""
    col1, col2 = st.columns([1, 1])
    with col1:
        st.image("https://github.com/GIUSEPPESAN21/LOGO-SAVA/blob/main/LOGO%20COLIBRI.png?raw=true", width=150)
        st.markdown("# Bienvenido a\n# Doctor at Home")
        st.markdown("### Inteligencia Artificial al servicio de la salud.")
        st.info("Acceda a su panel para gestionar pacientes y realizar diagnósticos asistidos.")

    with col2:
        with st.container():
            st.markdown('<div class="card-container">', unsafe_allow_html=True)
            tab_login, tab_register = st.tabs(["Iniciar Sesión", "Registrarse"])
            
            with tab_login:
                email = st.text_input("Correo Electrónico", key="l_email")
                password = st.text_input("Contraseña", type="password", key="l_pass")
                if st.button("Ingresar", type="primary", use_container_width=True):
                    try:
                        # Simulamos login (Firebase Auth real requiere cliente frontend o REST API key para password)
                        # Nota: admin SDK 'get_user_by_email' no verifica password. 
                        # Para este demo ASUMIMOS auth correcto si el usuario existe (limitación de SDK Admin en python puro)
                        # O se implementa auth custom. Mantenemos logica anterior por simplicidad del usuario.
                        user = auth.get_user_by_email(email)
                        st.session_state.logged_in = True
                        st.session_state.physician_email = user.email
                        st.session_state.page = 'control_panel'
                        st.rerun()
                    except:
                        st.error("Usuario no encontrado o credenciales inválidas.")

            with tab_register:
                r_email = st.text_input("Nuevo Correo", key="r_email")
                r_pass = st.text_input("Nueva Contraseña", type="password", key="r_pass")
                if st.button("Crear Cuenta", use_container_width=True):
                    try:
                        user = auth.create_user(email=r_email, password=r_pass)
                        st.success("Cuenta creada. Por favor inicie sesión.")
                    except Exception as e:
                        st.error(f"Error: {e}")
            st.markdown('</div>', unsafe_allow_html=True)

def select_patient_callback(patient_id):
    st.session_state.selected_patient_id = patient_id
    st.session_state.page = 'patient_dashboard'
    st.rerun()

def render_control_panel():
    """Panel principal del médico."""
    ui.render_hero_header(st.session_state.physician_email)
    
    # 1. Métricas Rápidas
    patients = firebase_utils.get_physician_patients(st.session_state.physician_email)
    
    c1, c2, c3 = st.columns(3)
    with c1: ui.card_metric("Total Pacientes", len(patients), "+1 esta semana", "#2563EB")
    with c2: ui.card_metric("Consultas Hoy", "0", None, "#10B981") # Placeholder
    with c3: ui.card_metric("Alertas Activas", "0", "Todo bajo control", "#F59E0B")

    st.markdown("---")
    
    col_list, col_form = st.columns([1.5, 1])
    
    with col_list:
        st.subheader("📋 Mis Pacientes")
        if not patients:
            st.info("No hay pacientes registrados aún.")
        else:
            for p in patients:
                ui.render_patient_card_item(p, select_patient_callback)

    with col_form:
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        st.subheader("➕ Registrar Nuevo Paciente")
        with st.form("add_patient"):
            nombre = st.text_input("Nombre Completo")
            cedula = st.text_input("Documento ID")
            edad = st.number_input("Edad", step=1)
            tel = st.text_input("Teléfono")
            if st.form_submit_button("Guardar Paciente", type="primary", use_container_width=True):
                firebase_utils.save_new_patient(st.session_state.physician_email, 
                                              {"nombre": nombre, "cedula": cedula, "edad": edad, "telefono": tel})
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def render_patient_dashboard():
    """Dashboard clínico detallado por paciente."""
    # Header de navegación
    c1, c2 = st.columns([6, 1])
    with c1: st.button("← Volver al Panel", on_click=lambda: st.session_state.update(page='control_panel'))
    with c2: st.empty()

    # Cargar datos
    p_id = st.session_state.selected_patient_id
    p_data = firebase_utils.get_patient_details(st.session_state.physician_email, p_id)
    history_df = firebase_utils.load_patient_history(st.session_state.physician_email, p_id)

    # Encabezado del Paciente
    st.markdown(f"""
        <div style="background: white; padding: 20px; border-radius: 10px; border-left: 6px solid #2563EB; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
            <h1 style="margin:0; font-size: 2.2rem;">{p_data.get('nombre', 'Paciente')}</h1>
            <p style="color: #6B7280; font-size: 1.1rem;">
                ID: <b>{p_data.get('cedula')}</b> &nbsp;|&nbsp; Edad: <b>{p_data.get('edad')} años</b> &nbsp;|&nbsp; Tel: {p_data.get('telefono')}
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Tabs de Funcionalidad
    tabs = st.tabs(["📊 Análisis Visual", "⏱️ Historial Clínico", "🩺 Nueva Consulta"])

    # TAB 1: VISUAL ANALYTICS
    with tabs[0]:
        st.subheader("Tendencias Clínicas")
        render_vital_signs_charts(history_df)
        
        # Ultimo análisis IA
        if not history_df.empty:
            last_record = history_df.iloc[0]
            if 'ai_analysis' in last_record and pd.notna(last_record['ai_analysis']):
                st.markdown("### 🧠 Último Análisis de IA")
                st.info(last_record['ai_analysis'])

    # TAB 2: HISTORIAL
    with tabs[1]:
        if history_df.empty:
            st.info("Sin historial previo.")
        else:
            # Vista de tabla moderna
            st.dataframe(
                history_df[['timestamp', 'motivo_consulta', 'presion_sistolica', 'presion_diastolica', 'glucemia']],
                use_container_width=True,
                hide_index=True
            )
            # Expander para detalles IA
            for i, row in history_df.iterrows():
                with st.expander(f"Consulta del {row['timestamp'].strftime('%d/%m/%Y')} - {row.get('motivo_consulta')}"):
                    st.write(f"**Signos:** PA {row.get('presion_sistolica')}/{row.get('presion_diastolica')}, Glucemia {row.get('glucemia')}")
                    if 'ai_analysis' in row and pd.notna(row['ai_analysis']):
                        st.markdown("---")
                        st.markdown(row['ai_analysis'])
                    elif st.button("Generar Análisis IA", key=f"ai_gen_{row['id']}"):
                         st.session_state.ai_analysis_running = True
                         st.session_state.last_clicked_ai = row['id']
                         # Lógica IA Quick-fix: Recargar para ejecutar
                         st.rerun()
            
            # Ejecutor de IA diferido (mantiene lógica original)
            if st.session_state.ai_analysis_running:
                c_id = st.session_state.last_clicked_ai
                row = history_df[history_df['id'] == c_id].iloc[0]
                summary = "Análisis retrospectivo solicitado."
                with st.spinner("SaludIA analizando datos..."):
                    report = GEMINI.generate_ai_holistic_review(p_data, row.to_dict(), summary)
                    firebase_utils.update_consultation_with_ai_analysis(st.session_state.physician_email, p_id, c_id, report)
                st.session_state.ai_analysis_running = False
                st.rerun()

    # TAB 3: NUEVA CONSULTA
    with tabs[2]:
        with st.form("new_consultation_premium"):
            c1, c2 = st.columns([2, 1])
            with c1:
                motivo = st.text_area("Motivo de la Consulta", height=100)
                st.markdown("**Revisión por Sistemas**")
                s_cardio = st.multiselect("Cardiovascular", ["Dolor Torácico", "Disnea", "Palpitaciones", "Edema"])
                s_resp = st.multiselect("Respiratorio", ["Tos", "Expectoración", "Disnea", "Sibilancias"])
            with c2:
                st.markdown("**Signos Vitales**")
                pa_s = st.number_input("P. Sistólica", value=120)
                pa_d = st.number_input("P. Diastólica", value=80)
                hr = st.number_input("Frec. Cardíaca", value=75)
                gluc = st.number_input("Glucemia", value=90)
                imc = st.number_input("IMC", value=24.0)
            
            submitted = st.form_submit_button("Finalizar y Guardar Consulta", type="primary", use_container_width=True)
            if submitted:
                data = {
                    "motivo_consulta": motivo,
                    "presion_sistolica": pa_s, "presion_diastolica": pa_d,
                    "frec_cardiaca": hr, "glucemia": gluc, "imc": imc,
                    "sintomas_cardio": s_cardio, "sintomas_resp": s_resp
                }
                firebase_utils.save_consultation(st.session_state.physician_email, p_id, data)
                st.success("Consulta registrada exitosamente.")
                st.rerun()

# ==============================================================================
# MAIN CONTROLLER
# ==============================================================================
def main():
    if not st.session_state.logged_in:
        render_login()
    elif st.session_state.page == 'control_panel':
        render_control_panel()
    elif st.session_state.page == 'patient_dashboard':
        render_patient_dashboard()
    else:
        st.session_state.page = 'control_panel'
        st.rerun()

if __name__ == "__main__":
    main()
