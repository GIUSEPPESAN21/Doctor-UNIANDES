# -*- coding: utf-8 -*-
"""
Doctor at Home - Plataforma Clínica Inteligente v4.0
"Profesional, Robusta y Potenciada por IA"
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from firebase_admin import auth
import datetime

# --- PERSONAL IMPORTS ---
import firebase_utils
# Aseguramos importaciones robustas
try:
    from gemini_utils import GeminiUtils
except ImportError:
    st.error("Error crítico: No se encontró 'gemini_utils.py'. Verifique la instalación.")
    st.stop()

import ui_components as ui

# --- CONFIGURACIÓN DE PÁGINA (V1 Style Layout) ---
st.set_page_config(
    page_title="SaludIA | Doctor at Home",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded" 
)

# --- CSS LOAD ---
ui.load_custom_css()

# --- INITIALIZE SESSION STATE (CRITICAL FIX) ---
if 'init_done' not in st.session_state:
    st.session_state.init_done = True
    st.session_state.logged_in = False
    st.session_state.physician_email = None
    st.session_state.page = 'login'
    st.session_state.selected_patient_id = None
    # Flags de procesos
    st.session_state.ai_executing = False
    st.session_state.ai_target_id = None

# --- CONEXIONES ---
DB = firebase_utils.DB
try:
    GEMINI = GeminiUtils()
    IS_MODEL_CONFIGURED = True
except Exception as e:
    GEMINI = None
    IS_MODEL_CONFIGURED = False
    # No mostramos error intrusivo, solo degradamos funcionalidad

# ==============================================================================
# LOGICA DE NEGOCIO Y VISUALIZACION
# ==============================================================================

def render_sidebar():
    """Barra lateral de navegación (Estilo V1 mejorado)."""
    with st.sidebar:
        st.markdown(f"### 👨‍⚕️ {st.session_state.physician_email.split('@')[0] if st.session_state.physician_email else 'Médico'}")
        st.markdown("---")
        
        if st.button("🏠 Inicio / Panel", use_container_width=True):
            st.session_state.page = 'control_panel'
            st.session_state.selected_patient_id = None
            st.rerun()
            
        st.markdown("---")
        if st.button("🚪 Cerrar Sesión", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.physician_email = None
            st.rerun()
            
        st.markdown("---")
        st.info("💡 **Tip:** Use el dictado por voz para agilizar la anamnesis.")

def render_login():
    """Login Estilo V1 pero limpio."""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br><h1 style='text-align: center; color: #0F52BA;'>Doctor at Home</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: gray;'>Plataforma Inteligente de Nueva Generación</p>", unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div class="medical-card">', unsafe_allow_html=True)
            email = st.text_input("✉️ Email Médico", key="login_email")
            password = st.text_input("🔑 Contraseña", type="password", key="login_pass")
            
            if st.button("Iniciar Sesión", type="primary", use_container_width=True):
                try:
                    user = auth.get_user_by_email(email)
                    st.session_state.logged_in = True
                    st.session_state.physician_email = user.email
                    st.session_state.page = 'control_panel'
                    st.rerun()
                except Exception:
                    st.error("Credenciales incorrectas o usuario no encontrado.")
            st.markdown('</div>', unsafe_allow_html=True)

def render_control_panel():
    """Dashboard Principal."""
    st.title("Panel de Control")
    patients = firebase_utils.get_physician_patients(st.session_state.physician_email)
    
    # KPIs Rápidos
    c1, c2, c3 = st.columns(3)
    c1.metric("Pacientes Totales", len(patients))
    c2.metric("Consultas Hoy", "0") # Placeholder logic
    c3.metric("Alertas Pendientes", "0")

    st.markdown("---")

    col_izq, col_der = st.columns([2, 1])
    
    with col_izq:
        st.subheader("📂 Pacientes Registrados")
        if not patients:
            st.info("No hay pacientes. Registre el primero a la derecha.")
        else:
            # Lista limpia con estilo "UI Components" pero simple
            for p in patients:
                ui.render_patient_list_item(p, lambda pid: st.session_state.update(selected_patient_id=pid, page='patient_dashboard'))

    with col_der:
        st.subheader("➕ Nuevo Paciente")
        with st.container():
            st.markdown('<div class="medical-card">', unsafe_allow_html=True)
            with st.form("add_p"):
                nom = st.text_input("Nombre")
                ced = st.text_input("ID / Cédula")
                edad = st.number_input("Edad", step=1)
                tel = st.text_input("Teléfono")
                if st.form_submit_button("Registrar", type="primary", use_container_width=True):
                    firebase_utils.save_new_patient(st.session_state.physician_email, {"nombre": nom, "cedula": ced, "edad": edad, "telefono": tel})
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

def render_patient_dashboard():
    """Detalle del Paciente Completo."""
    pid = st.session_state.selected_patient_id
    p_data = firebase_utils.get_patient_details(st.session_state.physician_email, pid)
    history_df = firebase_utils.load_patient_history(st.session_state.physician_email, pid)
    
    st.markdown(f"## Expediente: <span style='color:#0F52BA'>{p_data.get('nombre')}</span>", unsafe_allow_html=True)
    st.caption(f"ID: {p_data.get('cedula')} | Edad: {p_data.get('edad')}")

    tab1, tab2, tab3 = st.tabs(["📝 Historia Clínica", "📊 Gráficas Vitales", "🎙️ Nueva Consulta (AI)"])
    
    # --- TAB 1: HISTORIA (Timeline) ---
    with tab1:
        if st.session_state.ai_executing:
            # Procesar IA pendiente
            t_id = st.session_state.ai_target_id
            row_c = history_df[history_df['id'] == t_id].iloc[0]
            with st.spinner("🧠 SaludIA analizando caso clínico..."):
                report = GEMINI.generate_ai_holistic_review(p_data, row_c.to_dict(), "Análisis solicitado.")
                firebase_utils.update_consultation_with_ai_analysis(st.session_state.physician_email, pid, t_id, report)
            st.session_state.ai_executing = False
            st.session_state.ai_target_id = None
            st.rerun()

        if history_df.empty:
            st.info("Sin registros previos.")
        else:
            for _, row in history_df.sort_values('timestamp', ascending=False).iterrows():
                ui.render_consultation_timeline_item(
                    row.to_dict(), 
                    on_ai_click=lambda cid: st.session_state.update(ai_executing=True, ai_target_id=cid) or st.rerun()
                )

    # --- TAB 2: GRÁFICAS ---
    with tab2:
        if not history_df.empty:
            # Gráfico Potente de Presión Arterial
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=history_df['timestamp'], y=history_df['presion_sistolica'], name='Sistólica', line=dict(color='red', width=2)))
            fig.add_trace(go.Scatter(x=history_df['timestamp'], y=history_df['presion_diastolica'], name='Diastólica', line=dict(color='blue', width=2)))
            fig.update_layout(title="Monitoreo de Hipertensión", xaxis_title="Fecha", yaxis_title="mmHg", template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Se requieren datos para graficar.")

    # --- TAB 3: NUEVA CONSULTA (CON features solicitados) ---
    with tab3:
        # Layout columnas
        c_left, c_right = st.columns([1.5, 1])
        
        with c_left:
            st.subheader("1. Anamnesis Multimodal")
            
            # Feature 1: Dictado (Simulado con UI clara)
            st.markdown("**🎙️ Dictado por voz**")
            audio_text = st.empty()
            # Nota: st.audio_input es nuevo en 1.40+. Si tiene 1.52, funciona.
            try:
                # Intentamos usar el nuevo widget nativo si existe
                audio_val = st.audio_input("Grabar nota de voz")
                if audio_val:
                    st.success("Audio capturado. (Transcripción simulada: 'Paciente refiere dolor precordial...')")
                    # En producción real aquí iría Whisper API
            except:
                 st.info("Use el micrófono de su dispositivo.")

            motivo = st.text_area("Motivo de Consulta (Texto)", height=150, help="Escriba o pegue la transcripción aquí.")

            # Feature 2: Análisis de Documentos
            st.markdown("**📄 Adjuntar Laboratorios (PDF/Imagen)**")
            doc_file = st.file_uploader("Subir resultados", type=['pdf', 'png', 'jpg'])
            doc_analysis = ""
            if doc_file and GEMINI:
                if st.button("🔍 Analizar Documento con IA"):
                    with st.spinner("Leyendo documento..."):
                        if doc_file.type == "application/pdf":
                            txt = GEMINI.extract_text_from_pdf(doc_file)
                            doc_analysis = GEMINI.analyze_clinical_document(txt)
                            st.info("Hallazgos del documento importados.")
                        else:
                            st.warning("Por ahora solo PDF soportado para OCR completo.")
            
            if doc_analysis:
                with st.expander("Resultados del Análisis de Documento", expanded=True):
                    st.markdown(doc_analysis)
                    # Opcional: concatenar al motivo
                    motivo += f"\n\n[HALLAZGOS LABORATORIO AI]:\n{doc_analysis}"

        with c_right:
            st.subheader("2. Signos Vitales")
            with st.container(): # UI Card Style implicitly
                st.markdown('<div class="medical-card">', unsafe_allow_html=True)
                pa_s = st.number_input("Sistólica", 120)
                pa_d = st.number_input("Diastólica", 80)
                fc = st.number_input("Frecuencia Cardíaca", 75)
                gluc = st.number_input("Glucemia", 90)
                imc = st.number_input("IMC", 24.0)
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.subheader("3. Síntomas")
            s_cardio = st.multiselect("Cardiovascular", ["Dolor Torácico", "Palpitaciones", "Edema", "Disnea"])
            
            # Feature 3: Receta (Placeholder lógico)
            st.checkbox("Generar Receta Médica al guardar")

            if st.button("💾 Guardar Consulta", type="primary", use_container_width=True):
                data = {
                    "motivo_consulta": motivo,
                    "presion_sistolica": pa_s, "presion_diastolica": pa_d,
                    "frec_cardiaca": fc, "glucemia": gluc, "imc": imc,
                    "sintomas_cardio": s_cardio,
                    "ai_analysis": doc_analysis if doc_analysis else None # Guardar el análisis del doc si existe
                }
                firebase_utils.save_consultation(st.session_state.physician_email, pid, data)
                st.success("Datos guardados.")
                st.rerun()

# ==============================================================================
# MAIN
# ==============================================================================
def main():
    if st.session_state.logged_in:
        render_sidebar()
        if st.session_state.page == 'patient_dashboard':
            render_patient_dashboard()
        else:
            render_control_panel()
    else:
        render_login()

if __name__ == "__main__":
    main()
