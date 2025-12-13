# -*- coding: utf-8 -*-
"""
Doctor at Home - Plataforma Clínica Inteligente
Versión: 5.0 "Unified Experience"
- Login con st.form (un solo click)
- Tabs unificados (Analítica + Historial)
- Modelos IA actualizados
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

# --- IMPORTS ---
import firebase_utils
try:
    from gemini_utils import GeminiUtils
except ImportError:
    st.error("Error: 'gemini_utils.py' no encontrado.")
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

# Session State
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.physician_email = None
    st.session_state.page = 'login'
    st.session_state.selected_patient_id = None
    st.session_state.ai_analysis_running = False
    st.session_state.last_clicked_ai = None

# ==============================================================================
# PDF LOGIC
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
# CHARTS
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
        fig.update_layout(title="Presión Arterial", template="plotly_white", height=280, margin=dict(l=20,r=20,t=40,b=20))
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig2 = px.line(df, x='timestamp', y='glucemia', title="Glucemia", markers=True)
        fig2.update_traces(line_color='#388e3c')
        fig2.update_layout(template="plotly_white", height=280, margin=dict(l=20,r=20,t=40,b=20))
        st.plotly_chart(fig2, use_container_width=True)

# ==============================================================================
# VIEWS
# ==============================================================================
def render_login():
    """Login con st.form para evitar doble click."""
    c1, c2 = st.columns([1, 1])
    with c1:
        st.image("https://github.com/GIUSEPPESAN21/LOGO-SAVA/blob/main/LOGO%20COLIBRI.png?raw=true", width=150)
        st.markdown("# Doctor at Home")
        st.caption("Plataforma Clínica Inteligente con IA")
        st.info("Sistema de soporte al diagnóstico médico potenciado por Gemini AI.")
    
    with c2:
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        tabs = st.tabs(["🔑 Ingresar", "📝 Registro"])
        
        # TAB LOGIN - USANDO st.form PARA UN SOLO CLICK
        with tabs[0]:
            with st.form("login_form", clear_on_submit=False):
                email = st.text_input("Email", placeholder="doctor@hospital.com")
                password = st.text_input("Contraseña", type="password")
                submitted = st.form_submit_button("Ingresar", type="primary", use_container_width=True)
                
                if submitted:
                    if email and password:
                        try:
                            user = auth.get_user_by_email(email)
                            st.session_state.logged_in = True
                            st.session_state.physician_email = user.email
                            st.session_state.page = 'control_panel'
                            st.rerun()
                        except Exception as e:
                            st.error(f"Credenciales inválidas")
                    else:
                        st.warning("Complete todos los campos")
        
        # TAB REGISTRO
        with tabs[1]:
            with st.form("register_form", clear_on_submit=True):
                new_email = st.text_input("Nuevo Email")
                new_pass = st.text_input("Nueva Contraseña", type="password")
                reg_submitted = st.form_submit_button("Crear Cuenta", use_container_width=True)
                
                if reg_submitted:
                    if new_email and new_pass:
                        try:
                            auth.create_user(email=new_email, password=new_pass)
                            st.success("✅ Cuenta creada. Ahora puede ingresar.")
                        except Exception as e:
                            st.error(f"Error: {e}")
                    else:
                        st.warning("Complete todos los campos")
        
        st.markdown('</div>', unsafe_allow_html=True)

def render_control_panel():
    # Header con Logout
    c_head, c_out = st.columns([6, 1])
    with c_head:
        ui.render_hero_header(st.session_state.physician_email)
    with c_out:
        st.write("")
        if st.button("🚪 Salir", key="logout_btn", type="secondary"):
            st.session_state.logged_in = False
            st.session_state.physician_email = None
            st.session_state.page = 'login'
            st.rerun()
    
    pats = firebase_utils.get_physician_patients(st.session_state.physician_email)
    
    col_list, col_add = st.columns([1.5, 1])
    with col_list:
        st.subheader("📋 Pacientes")
        search = st.text_input("🔍 Buscar...", label_visibility="collapsed", placeholder="Buscar paciente...")
        filtered = [p for p in pats if search.lower() in p['nombre'].lower()] if search else pats
        
        if not filtered:
            st.info("No hay pacientes registrados.")
        else:
            for p in filtered:
                ui.render_patient_card_item(p, lambda pid: st.session_state.update(selected_patient_id=pid, page='patient_dashboard'))
            
    with col_add:
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        st.subheader("➕ Nuevo Paciente")
        with st.form("new_patient_form"):
            n = st.text_input("Nombre Completo")
            c = st.text_input("Documento ID")
            e = st.number_input("Edad", step=1, min_value=0, max_value=120)
            t = st.text_input("Teléfono")
            if st.form_submit_button("Guardar", type="primary", use_container_width=True):
                if n and c:
                    firebase_utils.save_new_patient(st.session_state.physician_email, {"nombre":n, "cedula":c, "edad":e, "telefono":t})
                    st.rerun()
                else:
                    st.warning("Nombre e ID son obligatorios")
        st.markdown('</div>', unsafe_allow_html=True)

def render_patient_dashboard():
    # Nav Header
    c1, c2 = st.columns([0.5, 6])
    if c1.button("⬅", help="Volver"): 
        st.session_state.page='control_panel'
        st.rerun()
    
    pid = st.session_state.selected_patient_id
    pdata = firebase_utils.get_patient_details(st.session_state.physician_email, pid)
    history = firebase_utils.load_patient_history(st.session_state.physician_email, pid)

    # Patient Header
    st.markdown(f"""
    <div style="background:white; padding:20px; border-radius:12px; border-left:6px solid #0F52BA; box-shadow:0 2px 4px rgba(0,0,0,0.05); margin-bottom:20px;">
        <h2 style="margin:0; color:#0F52BA;">{pdata.get('nombre', 'Paciente')}</h2>
        <span class="badge badge-blue">ID: {pdata.get('cedula', 'N/A')}</span>
        <span class="badge badge-blue">{pdata.get('edad', '?')} Años</span>
    </div>
    """, unsafe_allow_html=True)

    # TABS UNIFICADOS: Analítica + Historial JUNTOS, Nueva Consulta separada
    tab1, tab2 = st.tabs(["📊 Analítica & Historial", "🩺 Nueva Consulta"])

    # TAB 1: ANALÍTICA + HISTORIAL UNIFICADOS
    with tab1:
        # Gráficos primero
        st.subheader("📈 Tendencias Clínicas")
        render_vital_signs_charts(history)
        
        st.divider()
        
        # Historial Timeline
        st.subheader("📋 Historial de Consultas")
        
        if history.empty:
            st.info("Sin registros previos.")
        else:
            # AI Processing
            if st.session_state.ai_analysis_running:
                tid = st.session_state.last_clicked_ai
                row = history[history['id'] == tid].iloc[0]
                with st.spinner("🤖 Analizando con IA..."):
                    rep = GEMINI.generate_ai_holistic_review(pdata, row.to_dict(), "Análisis solicitado")
                    firebase_utils.update_consultation_with_ai_analysis(st.session_state.physician_email, pid, tid, rep)
                st.session_state.ai_analysis_running = False
                st.rerun()

            # Timeline
            idx_records = history.sort_values('timestamp', ascending=False)
            for _, row in idx_records.iterrows():
                c_data = row.to_dict()
                for k,v in c_data.items():
                    if isinstance(v, (list, tuple)):
                        continue
                    try:
                        if pd.isna(v): c_data[k] = "N/A"
                    except: pass
                
                ui.render_consultation_timeline_item(
                    c_data, 
                    on_ai_click=lambda cid: st.session_state.update(ai_analysis_running=True, last_clicked_ai=cid) or st.rerun()
                )

    # TAB 2: NUEVA CONSULTA
    with tab2:
        c_in, c_phy = st.columns([1.5, 1])
        with c_in:
            st.markdown("**1. Anamnesis**")
            audio = st.audio_input("🎙️ Dictado") if hasattr(st, 'audio_input') else None
            txt_voz = "[Audio adjunto]" if audio else ""
            
            motivo = st.text_area("Motivo de Consulta", value=txt_voz, height=100, placeholder="Describa el cuadro clínico...")
            
            pdf = st.file_uploader("📄 Adjuntar Labs (PDF)", type=['pdf'])
            pdf_res = ""
            if pdf and st.button("🔍 Analizar PDF"):
                with st.spinner("Procesando..."):
                    raw = GEMINI.extract_text_from_pdf(pdf)
                    pdf_res = GEMINI.analyze_clinical_document(raw)
            if pdf_res: 
                st.success("Hallazgos detectados:")
                st.markdown(pdf_res)

        with c_phy:
            st.markdown("**2. Signos Vitales**")
            with st.container():
                st.markdown('<div class="card-container">', unsafe_allow_html=True)
                s = st.number_input("Sistólica (mmHg)", value=120)
                d = st.number_input("Diastólica (mmHg)", value=80)
                f = st.number_input("Frec. Cardíaca (lpm)", value=75)
                g = st.number_input("Glucemia (mg/dL)", value=90)
                st.markdown('</div>', unsafe_allow_html=True)
            
            gen_pre = st.checkbox("📄 Generar Receta PDF")
            
            if st.button("💾 Guardar Consulta", type="primary", use_container_width=True):
                final_motivo = motivo + ("\n\n" + pdf_res if pdf_res else "")
                data = {
                    "motivo_consulta": final_motivo,
                    "presion_sistolica": s, "presion_diastolica": d,
                    "frec_cardiaca": f, "glucemia": g, "imc": 0,
                    "ai_analysis": pdf_res if pdf_res else None
                }
                firebase_utils.save_consultation(st.session_state.physician_email, pid, data)
                
                if gen_pre:
                    b = create_prescription_pdf(pdata, data, st.session_state.physician_email)
                    st.download_button("⬇️ Descargar Receta", b, "receta.pdf", "application/pdf")
                else:
                    st.success("✅ Consulta guardada")
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