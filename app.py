# -*- coding: utf-8 -*-
"""
Doctor at Home - SaludIA
Versión: 7.0 "Polished UI"
- Login centrado perfectamente
- Logout integrado en header
- Acerca de interactivo
- Timeline corregido
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from firebase_admin import auth
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
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
st.set_page_config(page_title="SaludIA", page_icon="🩺", layout="wide", initial_sidebar_state="collapsed")
ui.load_custom_css()

# --- CONSTANTS ---
LOGO_URL = "https://github.com/GIUSEPPESAN21/LOGO-SAVA/blob/main/LOGO%20COLIBRI.png?raw=true"

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
# PDF GENERATION
# ==============================================================================
def generate_clinical_report_pdf(patient_data, consultation_data, ai_analysis, doctor_email):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=50, bottomMargin=50)
    styles = getSampleStyleSheet()
    story = []
    
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=18, textColor=colors.HexColor('#0066FF'))
    story.append(Paragraph("REPORTE CLÍNICO - SaludIA", title_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"<b>Fecha:</b> {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
    story.append(Paragraph(f"<b>Médico:</b> {doctor_email}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("<b>DATOS DEL PACIENTE</b>", styles['Heading2']))
    patient_table = Table([
        ["Nombre:", patient_data.get('nombre', 'N/A')],
        ["ID:", patient_data.get('cedula', 'N/A')],
        ["Edad:", f"{patient_data.get('edad', 'N/A')} años"],
    ], colWidths=[100, 350])
    patient_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(patient_table)
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("<b>CONSULTA</b>", styles['Heading2']))
    story.append(Paragraph(f"<b>Motivo:</b> {consultation_data.get('motivo_consulta', 'N/A')}", styles['Normal']))
    story.append(Spacer(1, 10))
    
    vitals_table = Table([
        ["PA", "FC", "Glucemia", "IMC"],
        [f"{consultation_data.get('presion_sistolica', 'N/A')}/{consultation_data.get('presion_diastolica', 'N/A')}",
         f"{consultation_data.get('frec_cardiaca', 'N/A')} lpm",
         f"{consultation_data.get('glucemia', 'N/A')} mg/dL",
         f"{consultation_data.get('imc', 'N/A')}"]
    ], colWidths=[110, 110, 110, 110])
    vitals_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E6F0FF')),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E2E8F0')),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(vitals_table)
    story.append(Spacer(1, 20))
    
    if ai_analysis:
        story.append(Paragraph("<b>ANÁLISIS IA</b>", styles['Heading2']))
        clean = ai_analysis.replace("**", "").replace("###", "").replace("##", "").replace("#", "")
        story.append(Paragraph(clean[:2000], styles['Normal']))
    
    story.append(Spacer(1, 30))
    story.append(Paragraph("<i>Generado por SaludIA</i>", styles['Normal']))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

def create_prescription_pdf(patient_data, doctor_email):
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
    text.textLines("1. _________________________________\n\n2. _________________________________\n\n3. _________________________________")
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
        st.info("📊 No hay datos históricos para graficar.")
        return
    df = df.sort_values('timestamp')
    c1, c2 = st.columns(2)
    with c1:
        fig = go.Figure()
        fig.add_shape(type="rect", x0=df['timestamp'].min(), x1=df['timestamp'].max(), y0=140, y1=200, fillcolor="red", opacity=0.1, line_width=0)
        fig.add_trace(go.Scatter(x=df['timestamp'], y=df['presion_sistolica'], name='Sistólica', line=dict(color='#F44336', width=2)))
        fig.add_trace(go.Scatter(x=df['timestamp'], y=df['presion_diastolica'], name='Diastólica', line=dict(color='#2196F3', width=2)))
        fig.update_layout(title="Presión Arterial", template="plotly_white", height=280, margin=dict(l=20,r=20,t=40,b=20), font=dict(family="Plus Jakarta Sans"))
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig2 = px.line(df, x='timestamp', y='glucemia', title="Glucemia", markers=True)
        fig2.update_traces(line_color='#4CAF50', line_width=2)
        fig2.update_layout(template="plotly_white", height=280, margin=dict(l=20,r=20,t=40,b=20), font=dict(family="Plus Jakarta Sans"))
        st.plotly_chart(fig2, use_container_width=True)

# ==============================================================================
# VIEWS
# ==============================================================================
def render_login():
    """Login CENTRADO y alineado."""
    # Centrado vertical con espaciadores
    st.markdown("<div style='height: 5vh;'></div>", unsafe_allow_html=True)
    
    # Contenedor centrado
    col_left, col_center, col_right = st.columns([1, 2, 1])
    
    with col_center:
        # Logo y título centrados
        st.markdown(f"""
            <div style="text-align: center; margin-bottom: 2rem;">
                <img src="{LOGO_URL}" width="120" style="margin-bottom: 1rem;">
                <h1 style="margin: 0;">Bienvenido a SaludIA</h1>
                <p style="color: #64748B; font-size: 1.1rem; margin-top: 0.5rem;">Tu Asistente Clínico Inteligente</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Card de login
        with st.container():
            st.markdown('<div class="card-container">', unsafe_allow_html=True)
            
            tabs = st.tabs(["🔑 Ingresar", "📝 Registro"])
            
            with tabs[0]:
                with st.form("login_form", clear_on_submit=False):
                    email = st.text_input("Email", placeholder="doctor@hospital.com")
                    password = st.text_input("Contraseña", type="password")
                    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
                    submitted = st.form_submit_button("Ingresar", type="primary", use_container_width=True)
                    
                    if submitted:
                        if email and password:
                            try:
                                user = auth.get_user_by_email(email)
                                st.session_state.logged_in = True
                                st.session_state.physician_email = user.email
                                st.session_state.page = 'control_panel'
                                st.rerun()
                            except:
                                st.error("❌ Credenciales inválidas")
                        else:
                            st.warning("⚠️ Complete todos los campos")
            
            with tabs[1]:
                with st.form("register_form", clear_on_submit=True):
                    new_email = st.text_input("Email")
                    new_pass = st.text_input("Contraseña", type="password")
                    confirm_pass = st.text_input("Confirmar Contraseña", type="password")
                    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
                    reg_submitted = st.form_submit_button("Crear Cuenta", use_container_width=True)
                    
                    if reg_submitted:
                        if new_email and new_pass:
                            if new_pass == confirm_pass:
                                try:
                                    auth.create_user(email=new_email, password=new_pass)
                                    st.success("✅ Cuenta creada exitosamente")
                                    st.balloons()
                                except Exception as e:
                                    st.error(f"Error: {e}")
                            else:
                                st.error("Las contraseñas no coinciden")
                        else:
                            st.warning("Complete todos los campos")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Footer
        st.markdown("""
            <div style="text-align: center; margin-top: 2rem; color: #94A3B8; font-size: 0.85rem;">
                <p>Desarrollado por Joseph Javier Sánchez Acuña | SAVA</p>
            </div>
        """, unsafe_allow_html=True)

def render_control_panel():
    # Header CON logout integrado
    ui.render_hero_header_with_logout(
        st.session_state.physician_email,
        on_logout=lambda: (
            st.session_state.update(logged_in=False, physician_email=None, page='login'),
            st.rerun()
        )
    )
    
    # Tabs
    tab_main, tab_about = st.tabs(["👨‍⚕️ Gestión de Pacientes", "ℹ️ Acerca de"])
    
    with tab_main:
        pats = firebase_utils.get_physician_patients(st.session_state.physician_email)
        
        col_list, col_add = st.columns([1.5, 1])
        with col_list:
            st.subheader("📋 Mis Pacientes")
            search = st.text_input("🔍", label_visibility="collapsed", placeholder="Buscar paciente...")
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
                        firebase_utils.save_new_patient(st.session_state.physician_email, {
                            "nombre": n, "cedula": c, "edad": e, "telefono": t
                        })
                        st.rerun()
                    else:
                        st.warning("Nombre e ID son obligatorios")
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab_about:
        ui.render_about_section()

def render_patient_dashboard():
    # Nav Header
    c1, c2, _ = st.columns([0.3, 5, 1])
    if c1.button("⬅", help="Volver"): 
        st.session_state.page='control_panel'
        st.rerun()
    
    pid = st.session_state.selected_patient_id
    pdata = firebase_utils.get_patient_details(st.session_state.physician_email, pid)
    history = firebase_utils.load_patient_history(st.session_state.physician_email, pid)

    # Patient Header
    st.markdown(f"""
        <div style="
            background: white;
            padding: 1.25rem 1.5rem;
            border-radius: 14px;
            border-left: 5px solid #0066FF;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 1rem;
        ">
            <div style="
                width: 50px;
                height: 50px;
                background: linear-gradient(135deg, #0066FF, #00C2FF);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 1.5rem;
                font-weight: 700;
            ">{pdata.get('nombre', 'P')[0].upper()}</div>
            <div>
                <h2 style="margin: 0; font-size: 1.4rem; color: #0F172A;">{pdata.get('nombre', 'Paciente')}</h2>
                <div style="margin-top: 4px;">
                    <span class="badge badge-blue">ID: {pdata.get('cedula', 'N/A')}</span>
                    <span class="badge badge-blue">{pdata.get('edad', '?')} Años</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📊 Analítica & Historial", "🩺 Nueva Consulta"])

    with tab1:
        st.subheader("📈 Tendencias Clínicas")
        render_vital_signs_charts(history)
        
        st.divider()
        
        st.subheader("📋 Historial de Consultas")
        
        if history.empty:
            st.info("Sin registros previos.")
        else:
            if st.session_state.ai_analysis_running:
                tid = st.session_state.last_clicked_ai
                row = history[history['id'] == tid].iloc[0]
                with st.spinner("🤖 Analizando con IA..."):
                    rep = GEMINI.generate_ai_holistic_review(pdata, row.to_dict(), "Análisis")
                    firebase_utils.update_consultation_with_ai_analysis(st.session_state.physician_email, pid, tid, rep)
                st.session_state.ai_analysis_running = False
                st.rerun()

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
            
            st.divider()
            if not history.empty:
                last = history.sort_values('timestamp', ascending=False).iloc[0].to_dict()
                if st.button("📄 Generar Reporte Completo (PDF)", type="secondary"):
                    pdf = generate_clinical_report_pdf(pdata, last, last.get('ai_analysis', ''), st.session_state.physician_email)
                    st.download_button("⬇️ Descargar", pdf, f"Reporte_{pdata.get('cedula')}.pdf", "application/pdf")

    with tab2:
        c_in, c_phy = st.columns([1.5, 1])
        with c_in:
            st.markdown("**📝 Anamnesis**")
            audio = st.audio_input("🎙️ Dictado") if hasattr(st, 'audio_input') else None
            txt_voz = "[Audio adjunto]" if audio else ""
            
            motivo = st.text_area("Motivo de Consulta", value=txt_voz, height=100, placeholder="Describa el cuadro clínico...")
            
            st.markdown("**🔍 Revisión por Sistemas**")
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                s_cardio = st.multiselect("❤️ Cardiovascular", ["Dolor Torácico", "Palpitaciones", "Disnea", "Edema"])
                s_resp = st.multiselect("🫁 Respiratorio", ["Tos", "Expectoración", "Sibilancias"])
            with col_s2:
                s_gi = st.multiselect("🍽️ Gastrointestinal", ["Dolor Abdominal", "Náuseas", "Diarrea"])
                s_neuro = st.multiselect("🧠 Neurológico", ["Cefalea", "Mareo", "Debilidad"])
            
            pdf = st.file_uploader("📄 Adjuntar Labs (PDF)", type=['pdf'])
            pdf_res = ""
            if pdf and st.button("🔍 Analizar PDF"):
                with st.spinner("Procesando..."):
                    raw = GEMINI.extract_text_from_pdf(pdf)
                    pdf_res = GEMINI.analyze_clinical_document(raw)
            if pdf_res: 
                st.success("Hallazgos:")
                st.markdown(pdf_res)

        with c_phy:
            st.markdown("**📊 Signos Vitales**")
            with st.container():
                st.markdown('<div class="card-container">', unsafe_allow_html=True)
                s = st.number_input("Sistólica (mmHg)", value=120)
                d = st.number_input("Diastólica (mmHg)", value=80)
                f = st.number_input("Frec. Cardíaca (lpm)", value=75)
                g = st.number_input("Glucemia (mg/dL)", value=90)
                
                st.markdown("**📐 Antropometría**")
                peso = st.number_input("Peso (kg)", value=70.0, step=0.5)
                altura = st.number_input("Altura (m)", value=1.70, step=0.01)
                imc_calc = round(peso / (altura ** 2), 1) if altura > 0 else 0
                st.metric("IMC", imc_calc)
                st.markdown('</div>', unsafe_allow_html=True)
            
            col_rx, col_rp = st.columns(2)
            gen_rx = col_rx.checkbox("📝 Receta")
            gen_rp = col_rp.checkbox("📄 Reporte")
            
            if st.button("💾 Guardar", type="primary", use_container_width=True):
                data = {
                    "motivo_consulta": motivo + ("\n\n" + pdf_res if pdf_res else ""),
                    "presion_sistolica": s, "presion_diastolica": d,
                    "frec_cardiaca": f, "glucemia": g, "imc": imc_calc,
                    "sintomas_cardio": s_cardio, "sintomas_resp": s_resp,
                    "sintomas_gi": s_gi, "sintomas_neuro": s_neuro,
                    "ai_analysis": pdf_res if pdf_res else None
                }
                firebase_utils.save_consultation(st.session_state.physician_email, pid, data)
                
                if gen_rx:
                    rx = create_prescription_pdf(pdata, st.session_state.physician_email)
                    st.download_button("⬇️ Receta", rx, "receta.pdf", "application/pdf")
                if gen_rp:
                    rp = generate_clinical_report_pdf(pdata, data, pdf_res, st.session_state.physician_email)
                    st.download_button("⬇️ Reporte", rp, "reporte.pdf", "application/pdf")
                
                if not gen_rx and not gen_rp:
                    st.success("✅ Guardado")
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
