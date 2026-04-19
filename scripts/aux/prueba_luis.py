import pandas as pd
import requests
import json
import time

# ==========================================
# 1. CARGA DE DATOS Y CONSTRUCCIÓN DE REGLAS
# ==========================================
print("Cargando datasets...")
# Rutas a tus archivos (asegúrate de que estén en la misma carpeta o ajusta la ruta)
ruta_corpus = 'data/corpus/master_corpus_mixto_1000_clean_enriched.csv'
ruta_pbs = '/home/sortmon/UPV_EARTH_PROYECTOIII/corpus_PB/data/pb_reference.csv'

try:
    df_corpus = pd.read_csv(ruta_corpus)
    df_pbs = pd.read_csv(ruta_pbs)
except FileNotFoundError as e:
    print(f"Error fatal: No se encontró el archivo. {e}")
    exit()

# Inyectamos tu inteligencia institucional (CSV de reglas) en el prompt
pb_rules = ""
for index, row in df_pbs.iterrows():
    pb_rules += f"- PB Code: {row['pb_code']} ({row['pb_name']})\n"
    pb_rules += f"  * Core Definition: {row['short_definition']}\n"
    pb_rules += f"  * UPV Context: Look for terms like: {row['applied_keywords_upv']}\n"
    pb_rules += f"  * ACTIVATION LOGIC: {row['activation_logic']}\n"
    pb_rules += f"  * EXCLUSION RULE (CRITICAL): {row['exclusion_notes']}\n\n"

# ==========================================
# 2. CONFIGURACIÓN DEL LLM LOCAL (OLLAMA)
# ==========================================
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma4:26b"

def classify_abstract_advanced(abstract_text):
    prompt = f"""You are an expert scientific evaluator auditing research abstracts from the Universitat Politècnica de València (UPV) for their impact on Planetary Boundaries (PBs).

Your task is to analyze the abstract and strictly apply the activation and exclusion rules provided below. 
Do NOT assign a PB just because the text sounds "green" or "sustainable" (Misled by Positivity bias). You need explicit evidence.

### PLANETARY BOUNDARIES RULES:
{pb_rules}

### ABSTRACT TO EVALUATE:
"{abstract_text}"

### INSTRUCTIONS:
Step 1: Think step-by-step. Analyze if the abstract contains explicit metrics, outcomes, or core keywords related to any PB.
Step 2: Check the "EXCLUSION RULE" for that PB. Does the abstract violate the exclusion rule? If yes, discard the PB.
Step 3: Output the final decision in JSON format EXACTLY as follows:

{{
    "reasoning_process": "Your step-by-step analysis applying the activation and exclusion rules. Mention why a PB was included or discarded.",
    "assigned_pbs": [
        {{
            "pb_code": "PB1",
            "reason": "Direct quote from the text that proves the activation logic."
        }}
    ]
}}
If no PB is relevant, return {{"reasoning_process": "Explain why none apply...", "assigned_pbs": []}}.

### EXAMPLE OF EXPECTED OUTPUT:
{{
    "reasoning_process": "Step 1: The abstract discusses meteorological phenomena (SSW) and stratospheric clouds, not anthropogenic emissions. Step 2: It violates the exclusion rule for PB1 and PB3. No other PBs apply.",
    "assigned_pbs": []
}}
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.1, 
            "top_p": 0.9
        }
    }

    start_time = time.time()
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        result_json = response.json()
        
        llm_response_text = result_json.get("response", "{}")
        eval_time = time.time() - start_time
        return llm_response_text, eval_time
    except Exception as e:
        return json.dumps({"error": str(e)}), time.time() - start_time

# ==========================================
# EXTRAE EL JSON AUNQUE EL MODELO HABLE DE MÁS
# ==========================================
def parse_llm_output(raw_text):
    try:
        # Buscamos la primera llave '{' y la última llave '}'
        start_idx = raw_text.find('{')
        end_idx = raw_text.rfind('}')
        
        if start_idx != -1 and end_idx != -1:
            # Recortamos estrictamente el bloque JSON
            json_str = raw_text[start_idx:end_idx+1]
            data = json.loads(json_str)
        else:
            raise ValueError("No se encontró estructura JSON en la respuesta.")
        
        reasoning = data.get("reasoning_process", "")
        assigned_pbs = data.get("assigned_pbs", [])
        
        if not assigned_pbs or len(assigned_pbs) == 0:
            pb_codes_str = "None"
        else:
            pb_codes_str = ", ".join([item.get("pb_code", "") for item in assigned_pbs])
            
        return reasoning, pb_codes_str
    except Exception as e:
        return f"Error procesando JSON: {e}", "Error_Formato"

# ==========================================
# 3. BUCLE DE EVALUACIÓN
# ==========================================
sample_size = 5  # Abstracts a procesar
df_sample = df_corpus.head(sample_size).copy()

resultados_raw = []
resultados_reasoning = []
resultados_codes = []
tiempos_inferencia = []

print(f"\nIniciando evaluación avanzada con el modelo: {MODEL_NAME}")
print("-" * 50)

for index, row in df_sample.iterrows():
    print(f"Procesando Abstract {index + 1}/{sample_size} (Doc ID: {row['doc_id']})...", end=" ", flush=True)
    
    llm_out, t_elapsed = classify_abstract_advanced(row['clean_abstract'])
    
    reasoning, codes = parse_llm_output(llm_out)
    
    resultados_raw.append(llm_out)
    resultados_reasoning.append(reasoning)
    resultados_codes.append(codes)
    tiempos_inferencia.append(t_elapsed)
    
    print(f"[{t_elapsed:.2f}s] -> PBs Detectados: {codes}")

# ==========================================
# 4. GUARDAR RESULTADOS PARA ANÁLISIS
# ==========================================
df_sample['llm_raw_output'] = resultados_raw
df_sample['llm_reasoning'] = resultados_reasoning
df_sample['llm_predicted_pbs'] = resultados_codes 
df_sample['inference_time_sec'] = tiempos_inferencia

# Reordenamos columnas para la vista en Excel
cols_to_front = ['doc_id', 'llm_predicted_pbs', 'llm_reasoning', 'clean_abstract']
remaining_cols = [c for c in df_sample.columns if c not in cols_to_front]
df_sample = df_sample[cols_to_front + remaining_cols]

output_filename = f'eval_{MODEL_NAME.replace(":", "_")}_advanced.csv'
df_sample.to_csv(output_filename, index=False)

print("\n" + "=" * 50)
print(f"✅ Completado. Tiempo medio por abstract: {sum(tiempos_inferencia)/len(tiempos_inferencia):.2f} segundos.")
print(f"📄 Resultados guardados listos para revisar en: {output_filename}")