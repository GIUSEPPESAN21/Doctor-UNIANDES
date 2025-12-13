# -*- coding: utf-8 -*-
"""
Doctor at Home - Plataforma Clínica Inteligente
Versión: 4.1 "Professional Suite"
UI Reparada + IA Robusta
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
import time

# --- PERSONAL IMPORTS ---
import firebase_utils
try:
    from gemini_utils import GeminiUtils
except ImportError:
    st.error("Error crítico: 'gemini_utils.py' no encontrado.")
    st.stop()

import ui_components as ui

# --- CONFIG ---
st.set_page_config(page_title="Doctor at Home", page_icon="🩺", layout="wide", initial_sidebar_state="collapsed")
ui.load_custom_css()

# --- INIT ---
DB = firebase_utils.DB
@st.cache_resource
def get_ai():
    return GeminiUtils()
GEMINI = get_ai()

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.physician_email = None
    st.session_state.page = 'login'
    st.session_state.selected_patient_id = None
    st.session_state.ai_analysis_running = False
    st.session_state.last_clicked_ai = None

# ==============================================================================
# LOGICA PDF
# ==============================================================================
def create_prescription_pdf(patient_data, consulta_data, doctor_email):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 50, "RECETA MÉDICA")
    p.setFont("Helvetica", 10)
    p.drawString(50, height - 70, f"Dr/a. {doctor_email}")
    p.line(50, height - 80, width - 50, height - 80)
    p.drawString(50, height - 110, f"PACIENTE: {patient_data.get('nombre', 'N/A')}")
    p.drawString(50, height - 125, f"ID: {patient_data.get('cedula', 'N/A')} | FECHA: {datetime.datetime.now().strftime('%d/%m/%Y')}")
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height - 160, "Rx:")
    p.setFont("Helvetica", 11)
    text = p.beginText(50, height - 180)
    lines = consulta_data.get('motivo_consulta', '').split('\n')[:5]
    text.textLines("\n".join(lines))
    p.drawText(text)
    p.line(50, 100, width - 50, 100)
    p.drawString(50, 80, "Firma: __________________________")
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer

# ==============================================================================
# HELPERS GRAFICOS
# ==============================================================================
def render_vital_signs_charts(df):
    if df.empty:
        st.info("No hay datos históricos para graficar.")
        return
    df = df.sort_values('timestamp')
    c1, c2 = st.columns(2)
    with c1:
        fig = go.Figure()
        fig.add_shape(type="rect", x0=df['timestamp'].min(), x1=df['timestamp'].max(), y0=140, y1=200, fillcolor="red", opacity=0.1, line_width=0)
        fig.add_trace(go.Scatter(x=df['timestamp'], y=df['presion_sistolica'], name='Sistólica', line=dict(color='#d32f2f')))
        fig.add_trace(go.Scatter(x=df['timestamp'], y=df['presion_diastolica'], name='Diastólica', line=dict(color='#1976d2')))
        fig.update_layout(title="Presión Arterial", template="plotly_white", height=300, margin=dict(l=20,r=20,t=40,b=20))
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig2 = px.line(df, x='timestamp', y='glucemia', title="Glucemia", markers=True)
        fig2.update_traces(line_color='#388e3c')
        fig2.update_layout(template="plotly_white", height=300, margin=dict(l=20,r=20,t=40,b=20))
        st.plotly_chart(fig2, use_container_width=True)

# ==============================================================================
# VISTAS
# ==============================================================================
def render_login():
    c1, c2 = st.columns([1, 1])
    with c1:
        st.image("https://github.com/GIUSEPPESAN21/LOGO-SAVA/blob/main/LOGO%20COLIBRI.png?raw=true", width=150)
        st.markdown("# Doctor at Home")
        st.caption("Plataforma Clínica Inteligente")
    with c2:
        with st.container():
            st.markdown('<div class="card-container">', unsafe_allow_html=True)
            tabs = st.tabs(["Ingresar", "Registro"])
            with tabs[0]:
                email = st.text_input("Email", key="le")
                pw = st.text_input("Password", type="password", key="lp")
                if st.button("Entrar", type="primary", use_container_width=True):
                    try:
                        u = auth.get_user_by_email(email)
                        st.session_state.logged_in = True
                        st.session_state.physician_email = u.email
                        st.session_state.page = 'control_panel'
                        st.rerun()
                    except: st.error("Error de credenciales")
            with tabs[1]:
                ne = st.text_input("Nuevo Email", key="ne")
                np = st.text_input("Nueva Password", type="password", key="np")
                if st.button("Registrar", use_container_width=True):
                    auth.create_user(email=ne, password=np); st.success("Creado")
            st.markdown('</div>', unsafe_allow_html=True)

def render_control_panel():
    ui.render_hero_header(st.session_state.physician_email)
    pats = firebase_utils.get_physician_patients(st.session_state.physician_email)
    
    col_list, col_add = st.columns([1.5, 1])
    with col_list:
        st.subheader("Pacientes")
        search = st.text_input("Buscar...", label_visibility="collapsed")
        filtered = [p for p in pats if search.lower() in p['nombre'].lower()] if search else pats
        for p in filtered:
            ui.render_patient_card_item(p, lambda pid: st.session_state.update(selected_patient_id=pid, page='patient_dashboard'))
            
    with col_add:
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        st.subheader("Nuevo Ingreso")
        with st.form("np"):
            n = st.text_input("Nombre"); c = st.text_input("ID"); e = st.number_input("Edad", step=1); t = st.text_input("Tel")
            if st.form_submit_button("Guardar", type="primary"):
                firebase_utils.save_new_patient(st.session_state.physician_email, {"nombre":n, "cedula":c, "edad":e, "telefono":t})
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def render_patient_dashboard():
    # Header Nav
    c1, c2 = st.columns([0.5, 6])
    if c1.button("⬅", help="Atrás"): st.session_state.page='control_panel'; st.rerun()
    
    pid = st.session_state.selected_patient_id
    pdata = firebase_utils.get_patient_details(st.session_state.physician_email, pid)
    history = firebase_utils.load_patient_history(st.session_state.physician_email, pid)

    # Patient Header
    st.markdown(f"""
    <div style="background:white; padding:20px; border-radius:12px; border-left:6px solid #0F52BA; box-shadow:0 2px 4px rgba(0,0,0,0.05); margin-bottom:20px;">
        <h2 style="margin:0; color:#0F52BA;">{pdata.get('nombre')}</h2>
        <span class="badge badge-blue">ID: {pdata.get('cedula')}</span>
        <span class="badge badge-blue">{pdata.get('edad')} Años</span>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📊 Analítica", "📋 Historial (Timeline)", "🩺 Nueva Consulta"])

    with tab1:
        render_vital_signs_charts(history)

    # --- HISTORIAL: TIMELINE VIEW REPARADA ---
    with tab2:
        if history.empty:
            st.info("Sin registros.")
        else:
            # Ordenar por fecha descendente
            idx_records = history.sort_values('timestamp', ascending=False)
            
            # Flags de IA
            if st.session_state.ai_analysis_running:
                tid = st.session_state.last_clicked_ai
                row = history[history['id'] == tid].iloc[0]
                with st.spinner("🤖 Consultando Segunda Opinión..."):
                    rep = GEMINI.generate_ai_holistic_review(pdata, row.to_dict(), "Análisis solicitado")
                    firebase_utils.update_consultation_with_ai_analysis(st.session_state.physician_email, pid, tid, rep)
                st.session_state.ai_analysis_running = False
                st.rerun()

            # Render Loop usando componente visual Timeline
            for _, row in idx_records.iterrows():
                # Preparar datos limpios para el componente
                c_data = row.to_dict()
                # Asegurar tipos nativos para evitar errores de serializacion visual
                for k,v in c_data.items():
                    if pd.isna(v): c_data[k] = "N/A"
                
                ui.render_consultation_timeline_item(
                    c_data, 
                    on_ai_click=lambda cid: st.session_state.update(ai_analysis_running=True, last_clicked_ai=cid) or st.rerun()
                )

    with tab3:
        c_in, c_phy = st.columns([1.5, 1])
        with c_in:
            st.markdown("**1. Subjetivo (Anamnesis)**")
            # Voz
            audio = st.audio_input("🎙️") if hasattr(st, 'audio_input') else None
            txt_voz = ""
            if audio: st.success("Audio Ok"); txt_voz = "[Audio adjunto]"
            
            motivo = st.text_area("Motivo de Consulta", value=txt_voz, height=100)
            
            # PDF
            pdf = st.file_uploader("Adjuntar Labs (PDF)", type=['pdf'])
            pdf_res = ""
            if pdf and st.button("Analizar PDF"):
                with st.spinner("Leyendo..."):
                    raw = GEMINI.extract_text_from_pdf(pdf)
                    pdf_res = GEMINI.analyze_clinical_document(raw)
            if pdf_res: st.info(pdf_res)

        with c_phy:
            st.markdown("**2. Objetivo (Vitales)**")
            with st.container():
                st.markdown('<div class="card-container">', unsafe_allow_html=True)
                s = st.number_input("Sistólica", 120)
                d = st.number_input("Diastólica", 80)
                f = st.number_input("FC", 75)
                g = st.number_input("Glu", 90)
                st.markdown('</div>', unsafe_allow_html=True)
            
            gen_pre = st.checkbox("Generar PDF Receta")
            
            if st.button("Guardar Consulta", type="primary", use_container_width=True):
                data = {
                    "motivo_consulta": motivo + ("\n\n" + pdf_res if pdf_res else ""),
                    "presion_sistolica": s, "presion_diastolica": d,
                    "frec_cardiaca": f, "glucemia": g, "imc": 0,
                    "ai_analysis": pdf_res
                }
                firebase_utils.save_consultation(st.session_state.physician_email, pid, data)
                if gen_pre:
                    b = create_prescription_pdf(pdata, data, st.session_state.physician_email)
                    st.download_button("Descargar Receta", b, "rx.pdf", "application/pdf")
                else:
                    st.success("Guardado.")
                    time.sleep(1)
                    st.rerun()

def main():
    if st.session_state.logged_in:
        if st.session_state.page == 'patient_dashboard': render_patient_dashboard()
        else: render_control_panel()
    else: render_login()

if __name__ == "__main__":
    main()