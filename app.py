# -*- coding: utf-8 -*-
"""
Doctor at Home - Plataforma Clínica Inteligente v3.5
"Doctoral Standard Edition"
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from firebase_admin import auth

# --- PERSONAL IMPORTS ---
import firebase_utils
from gemini_utils import GeminiUtils
import ui_components as ui

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Doctor at Home | Clinical Suite",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

ui.load_custom_css()

# --- CONEXIONES ---
DB = firebase_utils.DB
try:
    GEMINI = GeminiUtils()
    IS_MODEL_CONFIGURED = True
except:
    GEMINI = None
    IS_MODEL_CONFIGURED = False

# --- STATE MANAGEMENT ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.physician_email = None
    st.session_state.page = 'login'
    st.session_state.selected_patient_id = None
    st.session_state.ai_executing = False
    st.session_state.ai_target_id = None

# ==============================================================================
# HELPERS GRAFICOS (Plotly)
# ==============================================================================
def render_analytics_dashboard(df):
    """Dashboard de gráficos clínicos avanzados."""
    if df.empty:
        st.warning("No hay datos clínicos suficientes para generar analítica.")
        return

    df = df.sort_values('timestamp')
    
    # 1. Gráfico Principal: Presión Arterial con Bandas de Referencia
    fig_pa = go.Figure()
    
    # Banda de hipertensión (referencia visual sutil)
    fig_pa.add_hrect(y0=140, y1=200, line_width=0, fillcolor="red", opacity=0.05, annotation_text="Hipertensión", annotation_position="top right")
    
    fig_pa.add_trace(go.Scatter(
        x=df['timestamp'], y=df['presion_sistolica'],
        mode='lines+markers', name='Sistólica (mmHg)',
        line=dict(color='#DC2626', width=3), marker=dict(size=8)
    ))
    fig_pa.add_trace(go.Scatter(
        x=df['timestamp'], y=df['presion_diastolica'],
        mode='lines+markers', name='Diastólica (mmHg)',
        line=dict(color='#2563EB', width=3), marker=dict(size=8)
    ))
    
    fig_pa.update_layout(
        title="<b>Dinámica de Presión Arterial</b>",
        yaxis_title="mmHg",
        template="plotly_white",
        hovermode="x unified",
        margin=dict(l=20, r=20, t=50, b=20),
        height=350,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    # 2. Gráfico Secundario: Glucemia + IMC (Doble Eje)
    fig_mix = go.Figure()
    fig_mix.add_trace(go.Bar(
        x=df['timestamp'], y=df['glucemia'],
        name='Glucemia (mg/dL)', marker_color='#059669', opacity=0.6
    ))
    
    fig_mix.update_layout(
        title="<b>Control Metabólico: Glucemia</b>",
        template="plotly_white",
        height=350,
        margin=dict(l=20, r=20, t=50, b=20)
    )

    c1, c2 = st.columns(2)
    c1.plotly_chart(fig_pa, use_container_width=True)
    c2.plotly_chart(fig_mix, use_container_width=True)

# ==============================================================================
# VISTAS PRINCIPALES
# ==============================================================================

def render_login():
    """Pantalla de Login minimalista y centrada."""
    col_spacer_l, col_content, col_spacer_r = st.columns([1, 1.2, 1])
    with col_content:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style="text-align:center; margin-bottom: 30px;">
                <h1 style="font-size: 3rem; margin-bottom: 10px;">SaludIA</h1>
                <p style="color: grey; font-size: 1.1rem;">Plataforma de Asistencia Clínica Avanzada</p>
            </div>
            """, unsafe_allow_html=True
        )
        
        with st.container():
            st.markdown('<div class="medical-card">', unsafe_allow_html=True)
            tabs = st.tabs(["Ingreso Médico", "Alta de Profesional"])
            
            with tabs[0]:
                email = st.text_input("Credencial (Email)", key="login_email")
                password = st.text_input("Clave de Acceso", type="password", key="login_pass")
                if st.button("Acceder al Sistema", type="primary", use_container_width=True):
                    try:
                        # Auth Logic Placeholder
                        user = auth.get_user_by_email(email)
                        st.session_state.logged_in = True
                        st.session_state.physician_email = user.email
                        st.session_state.page = 'control_panel'
                        st.rerun()
                    except:
                        st.error("Credenciales no válidas o usuario inexistente.")
            
            with tabs[1]:
                st.info("Solo para personal autorizado.")
                reg_email = st.text_input("Email Institucional", key="reg_email")
                reg_pass = st.text_input("Definir Clave", type="password", key="reg_pass")
                if st.button("Solicitar Acceso", use_container_width=True):
                    try:
                        auth.create_user(email=reg_email, password=reg_pass)
                        st.success("Usuario creado correctamente.")
                    except Exception as e:
                        st.error(f"Error: {e}")
            st.markdown('</div>', unsafe_allow_html=True)

def handle_ai_click(consultation_id):
    """Callback para manejar clic en botón de IA en el timeline."""
    st.session_state.ai_executing = True
    st.session_state.ai_target_id = consultation_id
    # No usamos rerun aqui mismo, esperamos a que el script principal lo capture o forzamos rerun global
    # La logica original de app.py ejecuta, aqui solo seteamos flag
    # Pero para limpieza, podemos ejecutar aqui si reorganizamos. Seguiremos estilo 'flag'.

def render_control_panel():
    """Panel de Control (Dashboard Principal)."""
    # Header
    cols = st.columns([4, 1])
    cols[0].markdown(f"## Bienvenid@, **Dr/a. {st.session_state.physician_email.split('@')[0]}**")
    if cols[1].button("Cerrar Sesión", type="primary"):
        st.session_state.logged_in = False
        st.rerun()
    
    st.markdown("---")
    
    # KPIs
    patients = firebase_utils.get_physician_patients(st.session_state.physician_email)
    c1, c2, c3, c4 = st.columns(4)
    with c1: ui.render_kpi_card("Pacientes Activos", len(patients), "Stable")
    with c2: ui.render_kpi_card("Consultas Mes", "12", "+2") # Fake data
    with c3: ui.render_kpi_card("Alertas Críticas", "0", None)
    with c4: ui.render_kpi_card("Eficiencia IA", "98%", "+5%")

    st.markdown("<br>", unsafe_allow_html=True)

    # Layout Principal: Lista Pacientes (Izquierda) + Accesos Rápidos (Derecha)
    row = st.columns([2, 1.2])
    
    with row[0]: # Lista de Pacientes
        ui.card_header("Directorio de Pacientes", "Seleccione un paciente para ver expediente")
        
        if not patients:
            st.info("No hay pacientes registrados. Utilice el panel derecho para agregar uno.")
        else:
            # Filtro de búsqueda
            search = st.text_input("🔍 Buscar por nombre o ID...", label_visibility="collapsed")
            filtered = [p for p in patients if search.lower() in p['nombre'].lower()] if search else patients
            
            with st.container():
                st.markdown('<div class="medical-card" style="padding:10px;">', unsafe_allow_html=True)
                for p in filtered:
                    ui.render_patient_list_item(p, lambda pid: st.session_state.update(selected_patient_id=pid, page='patient_dashboard'))
                st.markdown('</div>', unsafe_allow_html=True)

    with row[1]: # Formulario Rápido
        ui.card_header("Alta Rápida", "Registrar nuevo paciente")
        with st.container():
            st.markdown('<div class="medical-card">', unsafe_allow_html=True)
            with st.form("quick_add"):
                f_nombre = st.text_input("Nombre Completo")
                c1, c2 = st.columns(2)
                f_cedula = c1.text_input("ID / Cédula")
                f_edad = c2.number_input("Edad", min_value=0, max_value=120)
                f_tel = st.text_input("Teléfono Contacto")
                
                if st.form_submit_button("Crear Expediente", type="primary", use_container_width=True):
                    if f_nombre and f_cedula:
                        firebase_utils.save_new_patient(st.session_state.physician_email, {
                            "nombre": f_nombre, "cedula": f_cedula, "edad": f_edad, "telefono": f_tel
                        })
                        st.rerun()
                    else: st.error("Nombre e ID obligatorios")
            st.markdown('</div>', unsafe_allow_html=True)

def render_patient_detail():
    """Expediente Clínico Detallado (Timeline + Charts)."""
    p_id = st.session_state.selected_patient_id
    p_data = firebase_utils.get_patient_details(st.session_state.physician_email, p_id)
    history_df = firebase_utils.load_patient_history(st.session_state.physician_email, p_id)

    # Navbar
    c1, c2 = st.columns([0.5, 6])
    if c1.button("←", help="Volver"):
        st.session_state.page = 'control_panel'
        st.session_state.selected_patient_id = None
        st.rerun()
    c2.markdown(f"**Expediente Clínico: {p_data.get('nombre')}**")
    
    # Encabezado Paciente
    st.markdown(f"""
        <div class="medical-card" style="border-left: 6px solid #0F52BA; display:flex; justify-content:space-between; align-items:center;">
            <div>
                <h1 style="margin:0; font-size:1.8rem;">{p_data.get('nombre')}</h1>
                <p style="color:#6B7280; margin:0;">ID: {p_data.get('cedula')} • {p_data.get('edad')} años • {p_data.get('telefono')}</p>
            </div>
            <div style="text-align:right;">
                <span class="badge badge-green">Activo</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Contenido Principal
    tabs = st.tabs(["📈 Analítica & Evolución", "📋 Historia Clínica (Timeline)", "✍️ Nueva Nota Evolutiva"])

    # TAB 1: ANALYTICS
    with tabs[0]:
        render_analytics_dashboard(history_df)

    # TAB 2: TIMELINE (Sin Tablas Feas)
    with tabs[1]:
        ui.card_header("Línea de Tiempo", "Historial de consultas cronológico")
        
        # Lógica de Ejecución IA
        if st.session_state.ai_executing:
            target_id = st.session_state.ai_target_id
            row_data = history_df[history_df['id'] == target_id].iloc[0]
            with st.spinner("🤖 El Agente Clínico está analizando el caso..."):
                report = GEMINI.generate_ai_holistic_review(p_data, row_data.to_dict(), "Análisis puntual solicitado.")
                firebase_utils.update_consultation_with_ai_analysis(st.session_state.physician_email, p_id, target_id, report)
            st.session_state.ai_executing = False
            st.session_state.ai_target_id = None
            st.rerun()

        if history_df.empty:
            st.info("No hay consultas registradas para este paciente.")
        else:
            # Iterar y renderizar componente Timeline para cada fila
            for _, row in history_df.sort_values('timestamp', ascending=False).iterrows():
                # Wrapper para capturar evento del boton dentro del timeline
                # Streamlit buttons need unique keys y return bool
                ui.render_consultation_timeline_item(row.to_dict(), 
                                                   on_ai_click=lambda cid: st.session_state.update(ai_executing=True, ai_target_id=cid) or st.rerun())

    # TAB 3: INPUT FORM
    with tabs[2]:
        ui.card_header("Nueva Consulta", "Registro de signos y síntomas")
        with st.container():
            st.markdown('<div class="medical-card">', unsafe_allow_html=True)
            with st.form("new_consultation_form"):
                col_a, col_b = st.columns([2, 1])
                
                with col_a:
                    st.markdown("#### 1. Anamnesis")
                    motivo = st.text_area("Motivo de la Consulta", height=100, placeholder="Describa el cuadro actual...")
                    st.markdown("**Síntomas Cardiovasculares:**")
                    s_cardio = st.multiselect("Seleccionar...", ["Dolor Torácico", "Disnea", "Palpitaciones", "Síncope"], key="s_c")
                    st.markdown("**Síntomas Respiratorios:**")
                    s_resp = st.multiselect("Seleccionar...", ["Tos Seca", "Tos Productiva", "Disnea", "Sibilancias"], key="s_r")

                with col_b:
                    st.markdown("#### 2. Signos Vitales")
                    pa_s = st.number_input("P. Sistólica (mmHg)", value=120)
                    pa_d = st.number_input("P. Diastólica (mmHg)", value=80)
                    fc = st.number_input("Frec. Cardíaca (lpm)", value=70)
                    gluc = st.number_input("Glucemia (mg/dL)", value=90)
                    imc = st.number_input("IMC (kg/m²)", value=24.0)

                st.markdown("---")
                # Botones de Acción
                c_submit, c_files = st.columns([1, 1])
                uploaded_file = c_files.file_uploader("Adjuntar Laboratorios (Opcional)", type=['pdf', 'jpg'])
                
                if c_submit.form_submit_button("💾 Guardar Historia Clínica", type="primary", use_container_width=True):
                    # Guardado
                    data_to_save = {
                        "motivo_consulta": motivo,
                        "presion_sistolica": pa_s, "presion_diastolica": pa_d,
                        "frec_cardiaca": fc, "glucemia": gluc, "imc": imc,
                        "sintomas_cardio": s_cardio,
                        "has_attachment": True if uploaded_file else False
                    }
                    firebase_utils.save_consultation(st.session_state.physician_email, p_id, data_to_save)
                    st.success("Nota guardada correctamente.")
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# MAIN
# ==============================================================================
def main():
    if st.session_state.logged_in:
        if st.session_state.page == 'patient_dashboard':
            render_patient_detail()
        else:
            render_control_panel()
    else:
        render_login()

if __name__ == "__main__":
    main()
