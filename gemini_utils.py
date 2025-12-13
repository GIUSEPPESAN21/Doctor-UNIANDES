# -*- coding: utf-8 -*-
"""
Módulo de Utilidades de Gemini AI - v3.1 (Stable Fallback)
Descripción: Lógica avanzada con manejo robusto de límites de cuota (Error 429).
Prioriza modelos estables y eficientes.
"""
import streamlit as st
import google.generativeai as genai
import logging
import time
import random
from pypdf import PdfReader
from google.api_core import exceptions

# Configuración de Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiUtils:
    def __init__(self):
        self.api_key = st.secrets.get('gemini_api_key')
        if not self.api_key:
            logger.error("API Key no encontrada.")
            return 
        
        genai.configure(api_key=self.api_key)
        # Definimos modelos en orden de prioridad/estabilidad
        self.models_priority = [
            "gemini-1.5-flash",        # Rápido y estable (Tier gratuito generoso)
            "gemini-1.5-pro",          # Mejor razonamiento
            "gemini-2.0-flash-exp",    # Experimental (Suele dar 429)
            "gemini-pro"               # Legacy
        ]
        self.current_model_name = self.models_priority[0]
        self.model = self._init_model(self.current_model_name)

    def _init_model(self, model_name):
        try:
            return genai.GenerativeModel(model_name)
        except Exception as e:
            logger.error(f"Error init model {model_name}: {e}")
            return None

    def _generate_with_retry(self, prompt, config=None):
        """
        Intenta generar contenido manejando errores de cuota (429).
        Si falla el modelo actual, intenta con el siguiente de la lista.
        """
        if not self.model: return "Error: IA no inicializada."

        # Lista de intentos: modelo actual primero, luego los demás
        attempt_order = [self.current_model_name] + [m for m in self.models_priority if m != self.current_model_name]
        
        for model_name in attempt_order:
            try:
                # Instanciar el modelo si cambiamos
                active_model = genai.GenerativeModel(model_name)
                
                response = active_model.generate_content(
                    prompt, 
                    generation_config=config
                )
                return response.text
                
            except exceptions.ResourceExhausted:
                logger.warning(f"Cuota excedida (429) en {model_name}. Intentando siguiente...")
                time.sleep(1) # Breve pausa antes de reintentar
                continue
            except Exception as e:
                logger.error(f"Error en generación con {model_name}: {e}")
                continue
        
        return "⚠️ Servicio de IA saturado momentáneamente. Por favor intente en 1 minuto."

    def extract_text_from_pdf(self, uploaded_file):
        try:
            reader = PdfReader(uploaded_file)
            text = []
            for page in reader.pages:
                text.append(page.extract_text() or "")
            return "\n".join(text)
        except Exception as e:
            return f"[Error sistémico leyendo PDF: {e}]"

    def analyze_clinical_document(self, text_content):
        prompt = f"""
        **ROL:** Auditor Médico IA.
        **TAREA:** Analizar reporte y listar HALLAZGOS ANORMALES.
        
        **TEXTO:**
        {text_content[:10000]}
        
        **FORMATO SALIDA:**
        - ⚠️ [Hallazgo 1]: [Interpretación breve]
        - ⚠️ [Hallazgo 2]: [Interpretación breve]
        (Si todo normal: "✅ Sin hallazgos patológicos evidentes")
        """
        return self._generate_with_retry(prompt)

    @st.cache_data(show_spinner=False, ttl=600)
    def generate_ai_holistic_review(_self, patient_info, latest_consultation, history_summary):
        """
        CDSS: Soporte a la decisión clínica.
        """
        prompt = f"""
        **CASO CLÍNICO:**
        Paciente: {patient_info.get('nombre', 'N/A')} ({patient_info.get('edad', '?')} años).
        Consulta: {latest_consultation.get('motivo_consulta', 'Sin datos')}
        Signos: PA {latest_consultation.get('presion_sistolica')}/{latest_consultation.get('presion_diastolica')}, Glu {latest_consultation.get('glucemia')}.
        
        **HISTORIAL:**
        {history_summary}

        **ANÁLISIS ESTRUCTURADO (Responde médico a médico):**
        1. **Diagnóstico Mas Probable:** Justificación breve.
        2. **Alerta de Riesgo:** (Bajo/Medio/Alto) basado en signos vitales.
        3. **Plan Sugerido:** 3 acciones concretas (Lab, Meds, Hábitos).
        """
        
        config = genai.types.GenerationConfig(
            temperature=0.3, # Balanceado
            max_output_tokens=1024
        )
        return _self._generate_with_retry(prompt, config)
