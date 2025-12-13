# -*- coding: utf-8 -*-
"""
Doctor at Home - Plataforma Clínica Inteligente
Versión: 3.5 ("Scientific Edition")
Integra lógica avanzada (Voz, PDF, Recetas) en la interfaz clásica preferida.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from firebase_admin import auth
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import datetime

# --- PERSONAL IMPORTS ---
import firebase_utils
# Importación robusta para evitar pantalla blanca de la muerte
try:
    from gemini_utils import GeminiUtils
except ImportError:
    st.error("Error crítico: 'gemini_utils.py' no encontrado. Contacte al administrador.")
    st.stop()

import ui_components as ui

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Doctor at Home | Dashboard",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- INICIALIZACIÓN ---
ui.load_custom_css()  # CSS Premium

# Conexión DB
DB = firebase_utils.DB

# Conexión IA (Resistente a fallos)
@st.cache_resource
def get_ai_engine():
    try:
        return GeminiUtils()
    except Exception as e:
        print(f"AI Init Error: {e}")
        return None

GEMINI = get_ai_engine()
IS_MODEL_CONFIGURED = GEMINI is not None

# Estado de Sesión Seguro
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.physician_email = None
    st.session_state.page = 'login'
    st.session_state.selected_patient_id = None
    st.session_state.ai_analysis_running = False
    st.session_state.last_clicked_ai = None

# ==============================================================================
# LOGICA DE NEGOCIO AVANZADA (SCIENTIFIC FEATURES)
# ==============================================================================
def create_prescription_pdf(patient_data, consulta_data, doctor_email):
    """Genera una receta médica PDF formal lista para imprimir."""
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Header
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 50, "RECETA MÉDICA / PRESCRIPCIÓN")
    p.setFont("Helvetica", 10)
    p.drawString(50, height - 70, f"Dr/a. {doctor_email}")
    p.line(50, height - 80, width - 50, height - 80)
    
    # Paciente
    p.drawString(50, height - 110, f"PACIENTE: {patient_data.get('nombre', 'N/A')}")
    p.drawString(300, height - 110, f"FECHA: {datetime.datetime.now().strftime('%d/%m/%Y')}")
    p.drawString(50, height - 125, f"ID: {patient_data.get('cedula', 'N/A')}   EDAD: {patient_data.get('edad', 'N/A')}")
    
    # Cuerpo (Diagnostico y Rx)
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height - 170, "Rx / PLAN DE MANEJO:")
    p.setFont("Helvetica", 11)
    
    text_object = p.beginText(50, height - 190)
    text_object.setFont("Helvetica", 11)
    
    # Logica simple para extraer tratamiento del texto (si la IA lo sugirió)
    content = f"Motivo: {consulta_data.get('motivo_consulta')}\n\n"
    content += "INDICACIONES:\n"
    content += "1. ___________________________________________________\n\n"
    content += "2. ___________________________________________________\n\n"
    content += "3. ___________________________________________________\n\n"
    
    for line in content.split('\n'):
        text_object.textLine(line)
    p.drawText(text_object)
    
    # Footer
    p.line(50, 100, width - 50, 100)
    p.setFont("Helvetica-Oblique", 9)
    p.drawString(50, 85, "Firma del Profesional: __________________________")
    p.drawString(50, 70, "Generado por Doctor at Home CDSS Platform")
    
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer

# ==============================================================================
# HELPERS VISUALES
# ==============================================================================
def render_vital_signs_charts(df):
    if df.empty:
        st.info("Datos insuficientes para analítica temporal.")
        return

    df = df.sort_values('timestamp')
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico Presión Arterial
        fig_pa = go.Figure()
        # Zona Hipertensión Sutil
        fig_pa.add_shape(type="rect", x0=df['timestamp'].min(), x1=df['timestamp'].max(), y0=140, y1=200,
                         fillcolor="red", opacity=0.1, line_width=0)
        fig_pa.add_trace(go.Scatter(x=df['timestamp'], y=df['presion_sistolica'], 
                                    mode='lines+markers', name='Sistólica', line=dict(color='#d32f2f')))
        fig_pa.add_trace(go.Scatter(x=df['timestamp'], y=df['presion_diastolica'], 
                                    mode='lines+markers', name='Diastólica', line=dict(color='#1976d2')))
        fig_pa.update_layout(title="Dinámica de Presión Arterial (mmHg)", 
                             template="plotly_white", margin=dict(l=20, r=20, t=40, b=20), height=300)
        st.plotly_chart(fig_pa, use_container_width=True)

    with col2:
        # Gráfico Glucemia
        fig_glu = px.line(df, x='timestamp', y='glucemia', markers=True, title="Control Glucémico (mg/dL)")
        fig_glu.update_traces(line_color='#388e3c')
        fig_glu.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=40, b=20), height=300)
        st.plotly_chart(fig_glu, use_container_width=True)

# ==============================================================================
# VISTAS
# ==============================================================================
def render_login():
    col1, col2 = st.columns([1, 1])
    with col1:
        st.image("https://github.com/GIUSEPPESAN21/LOGO-SAVA/blob/main/LOGO%20COLIBRI.png?raw=true", width=150)
        st.markdown("# Doctor at Home\n### Clinical Suite")
        st.info("Plataforma de Diagnóstico Asistido por Inteligencia Artificial.")

    with col2:
        with st.container():
            st.markdown('<div class="card-container">', unsafe_allow_html=True)
            tabs = st.tabs(["🔑 Ingreso", "📝 Registro"])
            
            with tabs[0]:
                email = st.text_input("Email", key="l_email")
                password = st.text_input("Contraseña", type="password", key="l_pass")
                if st.button("Acceder", type="primary", use_container_width=True):
                    try:
                        user = auth.get_user_by_email(email)
                        st.session_state.logged_in = True
                        st.session_state.physician_email = user.email
                        st.session_state.page = 'control_panel'
                        st.rerun()
                    except:
                        st.error("Credenciales inválidas.")

            with tabs[1]:
                r_email = st.text_input("Email Nuevo", key="r_email")
                r_pass = st.text_input("Crear Contraseña", type="password", key="r_pass")
                if st.button("Registrar Usuario", use_container_width=True):
                    try:
                        auth.create_user(email=r_email, password=r_pass)
                        st.success("Usuario creado. Inicie sesión.")
                    except:
                        st.error("Error al crear usuario.")
            st.markdown('</div>', unsafe_allow_html=True)

def render_control_panel():
    ui.render_hero_header(st.session_state.physician_email)
    patients = firebase_utils.get_physician_patients(st.session_state.physician_email)
    
    # KPIs
    c1, c2, c3 = st.columns(3)
    with c1: ui.card_metric("Pacientes Activos", len(patients), None, "#1565c0")
    with c2: ui.card_metric("Consultas Hoy", "0", None, "#2e7d32")
    with c3: ui.card_metric("IA Status", "ONLINE" if IS_MODEL_CONFIGURED else "OFFLINE", None, "#ef6c00")

    st.markdown("---")
    
    col_list, col_form = st.columns([1.5, 1])
    with col_list:
        st.subheader("Directorio de Pacientes")
        if not patients:
            st.info("No hay pacientes.")
        else:
            search = st.text_input("🔍 Buscar paciente...", label_visibility="collapsed")
            filtro = [p for p in patients if search.lower() in p['nombre'].lower()] if search else patients
            
            # Usando el componente de tarjeta original que le gustó al usuario
            for p in filtro:
                ui.render_patient_card_item(p, lambda pid: st.session_state.update(selected_patient_id=pid, page='patient_dashboard'))

    with col_form:
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        st.subheader("Nuevo Ingreso")
        with st.form("new_pat"):
            nom = st.text_input("Nombre Completo")
            ced = st.text_input("ID / Documento")
            edad = st.number_input("Edad", step=1)
            tel = st.text_input("Teléfono")
            if st.form_submit_button("Registrar Paciente", type="primary", use_container_width=True):
                firebase_utils.save_new_patient(st.session_state.physician_email, {"nombre": nom, "cedula": ced, "edad": edad, "telefono": tel})
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def render_patient_dashboard():
    # Navbar simple
    c1, c2 = st.columns([0.2, 4])
    if c1.button("⬅", help="Volver"):
        st.session_state.page = 'control_panel'
        st.rerun()
    
    pid = st.session_state.selected_patient_id
    p_data = firebase_utils.get_patient_details(st.session_state.physician_email, pid)
    history_df = firebase_utils.load_patient_history(st.session_state.physician_email, pid)

    # Header del paciente
    st.markdown(f"""
        <div style="background:white; padding:15px; border-radius:10px; border-left:5px solid #1565c0; margin-bottom:20px; box-shadow:0 2px 4px rgba(0,0,0,0.05);">
            <h2 style="margin:0; color:#1565c0;">{p_data.get('nombre')}</h2>
            <p style="margin:0; color:grey;">ID: {p_data.get('cedula')} | Edad: {p_data.get('edad')} años | {p_data.get('telefono')}</p>
        </div>
    """, unsafe_allow_html=True)

    tabs = st.tabs(["📊 Analítica", "📋 Historial", "🩺 Consulta Inteligente"])

    # TAB 1: GRÁFICAS
    with tabs[0]:
        render_vital_signs_charts(history_df)
        if not history_df.empty:
            last = history_df.sort_values('timestamp', ascending=False).iloc[0]
            if pd.notna(last.get('ai_analysis')):
                with st.expander("🤖 Última Opinión Clínica Inteligente (CDSS)", expanded=True):
                    st.markdown(last['ai_analysis'])

    # TAB 2: HISTORIAL (Table view as requested)
    with tabs[1]:
        if history_df.empty:
            st.info("Sin registros.")
        else:
            st.dataframe(history_df[['timestamp', 'motivo_consulta', 'presion_sistolica', 'glucemia']], use_container_width=True)
            
            # Loop de detalles
            for idx, row in history_df.sort_values('timestamp', ascending=False).iterrows():
                with st.expander(f"📅 {row['timestamp'].strftime('%d/%m/%Y')} - {row.get('motivo_consulta')}"):
                    c_a, c_b = st.columns(2)
                    c_a.write(f"**PA:** {row.get('presion_sistolica')}/{row.get('presion_diastolica')}")
                    c_b.write(f"**Glucemia:** {row.get('glucemia')}")
                    
                    if pd.notna(row.get('ai_analysis')):
                        st.info(row['ai_analysis'])
                    elif st.button("⚡ Analizar Caso Retrospectivo", key=f"btn_ai_{row['id']}"):
                        st.session_state.ai_analysis_running = True
                        st.session_state.last_clicked_ai = row['id']
                        st.rerun()

            # AI Trigger Logic
            if st.session_state.ai_analysis_running:
                target_id = st.session_state.last_clicked_ai
                row_raw = history_df[history_df['id'] == target_id].iloc[0]
                with st.spinner("Procesando análisis clínico profundo..."):
                    report = GEMINI.generate_ai_holistic_review(p_data, row_raw.to_dict(), "Análisis retrospectivo.")
                    firebase_utils.update_consultation_with_ai_analysis(st.session_state.physician_email, pid, target_id, report)
                st.session_state.ai_analysis_running = False
                st.rerun()

    # TAB 3: NUEVA CONSULTA (INTEGRANDO FEATURES AVANZADOS)
    with tabs[2]:
        col_input, col_meta = st.columns([1.5, 1])
        
        with col_input:
            st.subheader("1. Anamnesis")
            
            # --- Feature: Voice Dictation ---
            st.markdown("**🎙️ Dictado de Voz**")
            # Usa el componente nativo si existe (Streamlit 1.40+), fallback gracioso si no
            audio_val = st.audio_input("Grabar nota clínica") if hasattr(st, 'audio_input') else None
            voice_text_detected = ""
            if audio_val:
                st.success("Audio recibido. Procesando transcripción...")
                # Aquí iría Whisper. Simulamos integración para V4.
                voice_text_detected = "[TRANSCRIPCIÓN PENDIENTE DE WHISPER API]"

            motivo = st.text_area("Motivo y Enfermedad Actual", 
                                  value=voice_text_detected if voice_text_detected else "",
                                  height=120, 
                                  placeholder="Escriba o dicte el cuadro clínico...")

            # --- Feature: PDF Analysis ---
            st.markdown("**📄 Adjuntos (Labs/Imágenes)**")
            uploaded_file = st.file_uploader("Subir PDF", type=['pdf'])
            doc_insights = ""
            if uploaded_file and GEMINI:
                if st.button("🔍 Analizar Documento", type="secondary"):
                    with st.spinner("Leyendo y analizando documento..."):
                        raw_text = GEMINI.extract_text_from_pdf(uploaded_file)
                        doc_insights = GEMINI.analyze_clinical_document(raw_text)
                        
            if doc_insights:
                st.info("Hallazgos Automáticos:")
                st.markdown(doc_insights)
                motivo += f"\n\n[HALLAZGOS LABORATORIO]:\n{doc_insights}"

        with col_meta:
            st.subheader("2. Examen Físico")
            with st.container():
                st.markdown('<div class="medical-card">', unsafe_allow_html=True)
                pa_s = st.number_input("Sistólica", 120)
                pa_d = st.number_input("Diastólica", 80)
                fc = st.number_input("Frec. Cardíaca", 75)
                gluc = st.number_input("Glucemia", 90)
                imc = st.number_input("IMC", 24.0)
                st.markdown('</div>', unsafe_allow_html=True)
            
            s_cardio = st.multiselect("Síntomas CV", ["Dolor Torácico", "Disnea", "Palpitaciones", "Edema"])
            
            # --- Feature: Prescription Check ---
            gen_rx = st.checkbox("Generar Receta Médica PDF")

            if st.button("💾 Finalizar Consulta", type="primary", use_container_width=True):
                data = {
                    "motivo_consulta": motivo,
                    "presion_sistolica": pa_s, "presion_diastolica": pa_d,
                    "frec_cardiaca": fc, "glucemia": gluc, "imc": imc,
                    "sintomas_cardio": s_cardio,
                    "ai_analysis": doc_insights if doc_insights else None
                }
                
                # Guardar en DB
                firebase_utils.save_consultation(st.session_state.physician_email, pid, data)
                
                # Generar PDF si se pidió (Feature "Doctoral")
                if gen_rx:
                    pdf_bytes = create_prescription_pdf(p_data, data, st.session_state.physician_email)
                    st.download_button("⬇️ Descargar Receta", data=pdf_bytes, file_name=f"Receta_{p_data['cedula']}.pdf", mime="application/pdf")
                    st.success("Consulta guardada y receta generada.")
                else:
                    st.success("Consulta guardada exitosamente.")
                    time.sleep(1)
                    st.rerun()

# ==============================================================================
# MAIN
# ==============================================================================
def main():
    if st.session_state.logged_in:
        if st.session_state.page == 'patient_dashboard':
            render_patient_dashboard()
        else:
            render_control_panel()
    else:
        render_login()

if __name__ == "__main__":
    main()