# -*- coding: utf-8 -*-
"""
Módulo de Componentes de Interfaz de Usuario (UI) - v2.0
Diseño "Medical Grade" - Limpio, Consistente y sin Tablas Genéricas.
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
        .medical-card {
            background: white;
            border-radius: var(--radius);
            padding: 1.5rem;
            border: 1px solid var(--neutral-200);
            box-shadow: var(--shadow);
            transition: transform 0.2s, box-shadow 0.2s;
            margin-bottom: 1rem;
        }
        .medical-card:hover {
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            border-color: var(--primary);
        }

        /* --- TIMELINE DE CONSULTAS (Reemplaza Tablas) --- */
        .timeline-item {
            border-left: 3px solid var(--neutral-200);
            padding-left: 20px;
            margin-left: 10px;
            padding-bottom: 30px;
            position: relative;
        }
        .timeline-item::before {
            content: '';
            width: 14px;
            height: 14px;
            background: var(--primary);
            border: 3px solid white;
            border-radius: 50%;
            position: absolute;
            left: -8.5px;
            top: 0;
            box-shadow: 0 0 0 2px var(--primary-light);
        }
        .timeline-date {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            color: #6B7280;
            margin-bottom: 4px;
            font-weight: 600;
        }
        .timeline-content {
            background: white;
            border: 1px solid var(--neutral-200);
            border-radius: 8px;
            padding: 1rem;
            margin-top: 5px;
        }

        /* --- BADGES/ETIQUETAS --- */
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
        .badge-red { background: #FEE2E2; color: var(--danger); }

        /* --- METRIC VALUE --- */
        .big-number {
            font-size: 2rem;
            font-weight: 800;
            color: var(--primary);
            line-height: 1;
        }
        .metric-label {
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #6B7280;
            font-weight: 600;
        }

        /* --- BOTONES LIMPIOS --- */
        div[data-testid="stButton"] > button {
            border-radius: 8px;
            font-weight: 500;
            text-transform: none;
            letter-spacing: 0.01em;
        }
        </style>
    """, unsafe_allow_html=True)

# --- COMPONENTES VISUALES ---

def card_header(title, subtitle=None, icon="🩺"):
    """Encabezado de sección limpio."""
    st.markdown(f"""
        <div style="margin-bottom: 1.5rem;">
            <h2 style="margin:0; display:flex; align-items:center; gap:10px; font-size:1.5rem;">
                <span style="background:var(--primary-light); padding:8px; border-radius:8px; font-size:1.2rem;">{icon}</span>
                {title}
            </h2>
            {f'<p style="margin:5px 0 0 54px; color:#6B7280;">{subtitle}</p>' if subtitle else ''}
        </div>
    """, unsafe_allow_html=True)

def render_kpi_card(label, value, trend=None, color_class="blue"):
    """Tarjeta de métrica pequeña (KPI)."""
    trend_html = f"<span style='font-size:0.8rem; color:green'>▲ {trend}</span>" if trend else ""
    st.markdown(f"""
        <div class="medical-card" style="padding: 1rem; text-align: center;">
            <div class="metric-label">{label}</div>
            <div class="big-number">{value}</div>
            {trend_html}
        </div>
    """, unsafe_allow_html=True)

def render_patient_list_item(patient, on_click):
    """Tarjeta de paciente en lista (Reemplaza tabla)."""
    with st.container():
        cols = st.columns([0.1, 3, 2, 2])
        # Icono visual basado en género o random (placeholder)
        cols[0].markdown("👤") 
        
        with cols[1]:
            st.markdown(f"**{patient['nombre']}**")
            st.caption(f"ID: {patient['cedula']}")
        
        with cols[2]:
            st.markdown(f"<span class='badge badge-blue'>{patient.get('edad', '?')} Años</span>", unsafe_allow_html=True)
            
        with cols[3]:
            if st.button("Abrir Expediente →", key=f"btn_{patient['id']}", type="secondary", use_container_width=True):
                on_click(patient['id'])
        st.markdown("<hr style='margin: 0.5rem 0; opacity: 0.1;'>", unsafe_allow_html=True)

def render_consultation_timeline_item(consultation, on_ai_click):
    """
    Renderiza una consulta individual como un evento en una línea de tiempo.
    Mucho mejor que una fila de tabla.
    """
    date_str = consultation['timestamp'].strftime('%d %B %Y • %H:%M')
    
    # Determinamos badges de riesgo (simulado logicamente)
    badges_html = ""
    bp_sist = consultation.get('presion_sistolica', 0)
    if bp_sist > 140:
        badges_html += "<span class='badge badge-red'>Hipertensión</span> "
    elif bp_sist < 90:
        badges_html += "<span class='badge badge-warning'>Hipotensión</span> "
    
    # Layout HTML/Markdown
    st.markdown(f"""
        <div class="timeline-item">
            <div class="timeline-date">{date_str}</div>
            <div class="timeline-content">
                <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                    <strong>{consultation.get('motivo_consulta', 'Sin motivo registrado')}</strong>
                    <div>{badges_html}</div>
                </div>
                <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:10px; background:#F9FAFB; padding:10px; border-radius:6px; font-size:0.9rem;">
                    <div><span style="color:#6B7280">PA:</span> <b>{consultation.get('presion_sistolica')}/{consultation.get('presion_diastolica')}</b></div>
                    <div><span style="color:#6B7280">FC:</span> <b>{consultation.get('frec_cardiaca')}</b> lpm</div>
                    <div><span style="color:#6B7280">Glu:</span> <b>{consultation.get('glucemia')}</b> mg</div>
                    <div><span style="color:#6B7280">IMC:</span> <b>{consultation.get('imc')}</b></div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Análisis IA (sección expandible dentro del timeline)
    if 'ai_analysis' in consultation and consultation['ai_analysis']:
         with st.expander("🤖 Ver Análisis de IA", expanded=False):
             st.info(consultation['ai_analysis'])
    else:
        # Botón discreto para generar
        col1, _ = st.columns([1, 4])
        if col1.button("⚡ Analizar con IA", key=f"ai_btn_{consultation['id']}", type="primary"):
            on_ai_click(consultation['id'])
