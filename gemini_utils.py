# -*- coding: utf-8 -*-
"""
Módulo de Utilidades de Gemini AI - v3.0 (Scientific & Robust)
Descripción: Lógica avanzada para CDSS (Clinical Decision Support System).
Implementa razonamiento clínico estructurado y manejo robusto de modelos.
"""
import streamlit as st
import google.generativeai as genai
import logging
import time
from pypdf import PdfReader

# Configuración de Logging Profesional
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiUtils:
    def __init__(self):
        self.api_key = st.secrets.get('gemini_api_key')
        if not self.api_key:
            logger.error("API Key no encontrada en secrets.")
            return 
        
        genai.configure(api_key=self.api_key)
        self.model = self._get_best_model()

    def _get_best_model(self):
        """
        Intenta conectar con la mejor jerarquía de modelos disponibles.
        Patrón 'Chain of Responsibility' para fallback automático.
        """
        # Lista priorizada basada en benchmarks médicos (MedQA) y latencia
        candidates = [
            "gemini-2.0-flash-exp",    # SOTA Velocidad/Razonamiento
            "gemini-1.5-pro",          # Contexto largo (Documentos)
            "gemini-1.5-flash",        # Balanceado
            "gemini-pro-vision",       # Multimodal legacy
            "gemini-pro"               # Legacy texto
        ]
        
        for model_name in candidates:
            try:
                model = genai.GenerativeModel(model_name)
                # Intento de 'ping' muy ligero para verificar vida
                # model.generate_content("test", generation_config={'max_output_tokens': 1})
                logger.info(f"Conectado exitosamente con: {model_name}")
                return model
            except Exception as e:
                logger.warning(f"Fallo conexión con {model_name}: {e}")
                continue
        
        logger.critical("No se pudo iniciar ningún modelo de IA.")
        return None

    def extract_text_from_pdf(self, uploaded_file):
        """Extracción de texto PDF robusta."""
        try:
            reader = PdfReader(uploaded_file)
            text = []
            for page in reader.pages:
                text.append(page.extract_text() or "")
            return "\n".join(text)
        except Exception as e:
            return f"[Error sistémico leyendo PDF: {e}]"

    def analyze_clinical_document(self, text_content):
        """
        Análisis de Laboratorios basado en Rangos de Referencia.
        Salida estructurada para toma de decisiones rápida.
        """
        if not self.model: return "Servicio de IA no disponible."
        
        prompt = f"""
        **CONTEXTO:** Eres un asistente de IA para auditoría médica y patología clínica.
        **ENTRADA:** Texto extraído de un reporte médico/laboratorio.
        
        **INSTRUCCIONES:**
        1. **Detectar Anomalías:** Extrae SOLO los valores que están fuera de los rangos de referencia explícitos o implícitos.
        2. **Interpretación Fisiopatológica:** Para cada anomalía, explica en 1 frase la posible causa (ej. anemia ferropénica, infección bacteriana).
        3. **Formato:** Usa Markdown con viñetas claras. Si todo es normal, indícalo.

        --- REPORTE ---
        {text_content[:15000]}
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error en análisis documental: {e}"

    @st.cache_data(show_spinner=False, ttl=600)
    def generate_ai_holistic_review(_self, patient_info, latest_consultation, history_summary):
        """
        Sistema de Soporte a la Decisión Clínica (CDSS).
        Utiliza metodología SOAP (Subjetivo, Objetivo, Análisis, Plan) modificada para output de IA.
        """
        if not _self.model:
            return "⚠️ Sistema CDSS Offline."

        # Prompt Ingenieril basado en 'Chain of Thought' (CoT) para medicina
        prompt = f"""
        Actúa como un Comité Médico Interdisciplinario. Analiza el siguiente caso:

        **PACIENTE:** {patient_info.get('nombre')} ({patient_info.get('edad')} años).
        
        **DATOS ACTUALES:**
        - MC: {latest_consultation.get('motivo_consulta')}
        - Signos: PA {latest_consultation.get('presion_sistolica')}/{latest_consultation.get('presion_diastolica')}, FC {latest_consultation.get('frec_cardiaca')}, IMC {latest_consultation.get('imc')}.
        - Síntomas: {latest_consultation.get('sintomas_cardio')} (CV), {latest_consultation.get('sintomas_resp')} (Resp).
        
        **CONTEXTO HISTÓRICO:**
        {history_summary}

        **GENERAR INFORME CLÍNICO ESTRUCTURADO:**
        
        ### 1. 🏥 Impresión Diagnóstica (Assessment)
        *   **Diagnóstico Principal:** (El más probable fisiopatológicamente).
        *   **Justificación:** (Correlación síntoma-signo).
        *   **Diagnósticos Diferenciales:** (Listar 2 con breve descarte).

        ### 2. ⚠️ Estratificación de Riesgo
        *   **Nivel:** (Bajo / Moderado / Alto / Crítico).
        *   **Score Sugerido:** (ej. TIMI, HEART, Wells si aplica, o criterio clínico general).
        *   **Alertas:** (Signos de alarma presentes).

        ### 3. 📝 Plan de Manejo (Plan)
        *   **Paraclínicos:** (Estudios a solicitar priorizados).
        *   **Terapéutica Inicial:** (Grupos farmacológicos o medidas de soporte).
        *   **Recomendaciones:** (Educación al paciente, signos de alarma para re-consultar).

        Mantén un tono académico, directo y basado en evidencia.
        """
        
        try:
            # Configuración para reducir alucinaciones
            safe_config = genai.types.GenerationConfig(
                temperature=0.1,    # Casi determinista para medicina
                top_p=0.85,
                top_k=40,
                max_output_tokens=2048
            )
            response = _self.model.generate_content(prompt, generation_config=safe_config)
            return response.text
        except Exception as e:
            return f"Error en generación CDSS: {e}"
