# -*- coding: utf-8 -*-
"""
Módulo de Componentes de Interfaz de Usuario (UI) - v3.0
Consolidado para dar soporte a la Interfaz Unificada (V1 + Mejoras V2).
"""
import streamlit as st

# --- CONFIGURACIÓN DE ESTILOS (CSS) ---
def load_custom_css():
    """Inyecta CSS avanzado para una apariencia clínica premium."""
    st.markdown("""
        <style>
        /* --- FUENTES: Inter para UI, JetBrains Mono para datos --- */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;800&family=JetBrains+Mono:wght@400;500&display=swap');
        
        :root {
            /* Palette: Deep Medical Blue & Sterile White */
            --primary: #0F52BA;        /* Azul Zafiro */
            --primary-light: #E1EFFE;
            --success: #059669;        /* Verde Quirúrgico */
            --warning: #D97706;
            --danger: #DC2626;
            --neutral-50: #F9FAFB;
            --neutral-100: #F3F4F6;
            --neutral-200: #E5E7EB;
            --neutral-800: #1F2937;
            
            --radius: 12px;
            --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        }

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            color: var(--neutral-800);
            background-color: #F8FAFC;
        }

        /* --- TÍTULOS --- */
        h1, h2, h3 { 
            letter-spacing: -0.03em; 
            font-weight: 800;
        }
        h1 { font-size: 2.2rem; background: -webkit-linear-gradient(45deg, #0F52BA, #06B6D4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }

        /* --- TARJETAS (CARDS) --- */
        .card-container, .medical-card {
            background: white;
            border-radius: var(--radius);
            padding: 1.5rem;
            border: 1px solid var(--neutral-200);
            box-shadow: var(--shadow);
            transition: transform 0.2s, box-shadow 0.2s;
            margin-bottom: 1rem;
        }
        .card-container:hover, .medical-card:hover {
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            border-color: var(--primary);
        }

        /* --- BADGES --- */
        .badge {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 999px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
        }
        .badge-blue { background: var(--primary-light); color: var(--primary); }
        .badge-green { background: #DCFCE7; color: var(--success); }
        .badge-mid { background: #fee2e2; color: #b91c1c; }

        /* --- BOTONES LIMPIOS --- */
        div[data-testid="stButton"] > button {
            border-radius: 8px;
            font-weight: 500;
            text-transform: none;
            letter-spacing: 0.01em;
        }
        </style>
    """, unsafe_allow_html=True)

# --- COMPONENTES VISUALES UNIFICADOS ---

def render_hero_header(physician_email):
    """Encabezado estilo Hero para el Dashboard."""
    name = physician_email.split('@')[0] if physician_email else "Doctor"
    st.markdown(f"""
        <div style="background: linear-gradient(90deg, #0F52BA 0%, #06b6d4 100%); padding: 1.5rem; border-radius: 12px; color: white; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h2 style="margin:0; color:white;">Bienvenid@, De nuevo.</h2>
            <p style="margin:0; opacity:0.9;">Dr/a. {name} | Panel de Control Clínico</p>
        </div>
    """, unsafe_allow_html=True)

def card_header(title, subtitle=None, icon="🩺"):
    """Encabezado de sección limpio."""
    st.markdown(f"""
        <div style="margin-bottom: 1.5rem;">
            <h3 style="margin:0; display:flex; align-items:center; gap:10px;">
                <span style="background:var(--primary-light); padding:6px; border-radius:8px; font-size:1rem;">{icon}</span>
                {title}
            </h3>
            {f'<p style="margin:2px 0 0 44px; color:#6B7280; font-size:0.9rem;">{subtitle}</p>' if subtitle else ''}
        </div>
    """, unsafe_allow_html=True)

def card_metric(label, value, delta=None, color_hex="#0F52BA"):
    """Tarjeta de métrica (KPI) flexible."""
    delta_html = f"<div style='font-size:0.8rem; color: #059669; margin-top:5px;'>▲ {delta}</div>" if delta else ""
    st.markdown(f"""
        <div class="medical-card" style="padding: 1.2rem; border-left: 4px solid {color_hex};">
            <div style="font-size:0.8rem; text-transform:uppercase; color:#6B7280; font-weight:600;">{label}</div>
            <div style="font-size:1.8rem; font-weight:800; color:#1F2937; line-height:1.2;">{value}</div>
            {delta_html}
        </div>
    """, unsafe_allow_html=True)

def render_patient_card_item(patient, on_click):
    """Tarjeta de lista de paciente interactiva."""
    with st.container():
        # Usamos columnas de Streamlit para layout responsive
        c1, c2, c3 = st.columns([3, 2, 1.5])
        with c1:
            st.markdown(f"**{patient['nombre']}**")
            st.caption(f"ID: {patient['cedula']}")
        with c2:
            st.markdown(f"<span class='badge badge-blue'>{patient.get('edad', '?')} Años</span>", unsafe_allow_html=True)
            st.caption(patient.get('telefono', 'Sin tel.'))
        with c3:
            if st.button("Ver Historia ➜", key=f"p_btn_{patient['id']}", type="secondary", use_container_width=True):
                on_click(patient['id'])
        st.markdown("<hr style='margin: 10px 0; border:0; border-top:1px solid #E5E7EB;'>", unsafe_allow_html=True)

# Mantener compatibilidad con llamadas legacy por si acaso
render_kpi_card = card_metric
render_patient_list_item = render_patient_card_item

# ==============================================================================
# TIMELINE COMPONENT (CRITICAL - Was missing!)
# ==============================================================================
import pandas as pd

def render_consultation_timeline_item(consultation, on_ai_click):
    """
    Renderiza una consulta individual como un evento en una línea de tiempo.
    Diseño profesional tipo EHR (Electronic Health Record).
    """
    # Safe date parsing
    ts = consultation.get('timestamp')
    try:
        if ts is None or (isinstance(ts, float) and pd.isna(ts)) or str(ts) == 'NaT':
            date_str = "Fecha no registrada"
        elif hasattr(ts, 'strftime'):
            date_str = ts.strftime('%d %b %Y • %H:%M')
        else:
            date_str = str(ts)[:16]
    except:
        date_str = "Fecha desconocida"
    
    # Risk badges
    badges_html = ""
    try:
        bp_sist = int(consultation.get('presion_sistolica', 0) or 0)
        if bp_sist >= 140:
            badges_html += "<span style='background:#fee2e2; color:#b91c1c; padding:2px 8px; border-radius:999px; font-size:0.7rem; font-weight:600;'>HIPERTENSIÓN</span> "
        elif 0 < bp_sist < 90:
            badges_html += "<span style='background:#fef3c7; color:#d97706; padding:2px 8px; border-radius:999px; font-size:0.7rem; font-weight:600;'>HIPOTENSIÓN</span> "
    except: pass
    
    # Symptoms display
    symptoms_html = ""
    for k in ['sintomas_cardio', 'sintomas_resp']:
        val = consultation.get(k)
        if isinstance(val, list) and val:
            symptoms_html += f"<span style='font-size:0.8rem; color:#6B7280;'>{', '.join(val)}</span><br>"

    # Main Layout
    st.markdown(f"""
        <div style="border-left: 3px solid #E5E7EB; padding-left: 20px; margin-left: 10px; margin-bottom: 25px; position: relative;">
            <div style="position:absolute; left:-8px; top:0; width:12px; height:12px; background:#0F52BA; border-radius:50%; border:3px solid white; box-shadow:0 0 0 2px #E1EFFE;"></div>
            <div style="font-family:'JetBrains Mono', monospace; font-size:0.8rem; color:#6B7280; font-weight:600; margin-bottom:4px;">{date_str}</div>
            <div style="background:white; border:1px solid #E5E7EB; border-radius:10px; padding:16px; box-shadow:0 1px 3px rgba(0,0,0,0.05);">
                <div style="display:flex; justify-content:space-between; align-items:start; margin-bottom:12px;">
                    <div>
                        <strong style="font-size:1rem; color:#111827;">{consultation.get('motivo_consulta', 'Sin motivo')[:80]}</strong>
                        <div style="margin-top:4px;">{symptoms_html}</div>
                    </div>
                    <div>{badges_html}</div>
                </div>
                <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:12px; background:#F9FAFB; padding:12px; border-radius:8px; font-size:0.85rem; text-align:center;">
                    <div><span style="color:#9CA3AF; font-size:0.7rem;">PRESIÓN</span><br><b>{consultation.get('presion_sistolica', 'N/A')}/{consultation.get('presion_diastolica', 'N/A')}</b></div>
                    <div><span style="color:#9CA3AF; font-size:0.7rem;">FC</span><br><b>{consultation.get('frec_cardiaca', 'N/A')}</b></div>
                    <div><span style="color:#9CA3AF; font-size:0.7rem;">GLUCEMIA</span><br><b>{consultation.get('glucemia', 'N/A')}</b></div>
                    <div><span style="color:#9CA3AF; font-size:0.7rem;">IMC</span><br><b>{consultation.get('imc', 'N/A')}</b></div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # AI Analysis Section
    ai_report = consultation.get('ai_analysis')
    if ai_report and ai_report != "N/A":
        with st.expander("🤖 Análisis Clínico (IA)", expanded=False):
            st.markdown(ai_report)
    else:
        col1, _ = st.columns([1, 4])
        if col1.button("⚡ Analizar", key=f"ai_btn_{consultation.get('id', 'x')}", type="secondary"):
            on_ai_click(consultation['id'])

