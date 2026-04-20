import pandas as pd
import numpy as np
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
OUTPUTS_DIR = BASE_DIR / 'outputs'
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

# ==========================================
# 1. CONFIGURACIÓN Y RUTAS
# ==========================================
print("Iniciando Pipeline de Análisis Multietiqueta...")

ruta_humano = OUTPUTS_DIR / 'validacion_real.csv'
ruta_gemma  = OUTPUTS_DIR / 'eval_gemma4_26b_validacion_108.csv'
ruta_qwen   = OUTPUTS_DIR / 'eval_qwen2.5_14b_validacion_108.csv'
ruta_llama  = OUTPUTS_DIR / 'eval_llama3_1_8b_validacion_108.csv'

# ==========================================
# 2. CARGA SEGURA Y LIMPIEZA DE DATOS
# ==========================================
def cargar_y_limpiar(ruta):
    try:
        # utf-8-sig elimina automáticamente el caracter invisible \ufeff (BOM)
        df = pd.read_csv(ruta, sep=None, engine='python', encoding='utf-8-sig')
    except UnicodeDecodeError:
        df = pd.read_csv(ruta, sep=None, engine='python', encoding='latin1')
    except FileNotFoundError:
        print(f"\n❌ ERROR: Archivo no encontrado:\n{ruta}")
        exit()
    
    # Limpiamos nombres de columnas y el doc_id
    df.columns = df.columns.str.strip().str.lower()
    if 'doc_id' in df.columns:
        df['doc_id'] = df['doc_id'].astype(str).str.strip()
    else:
        print(f"\n❌ ERROR FATAL: No encuentro 'doc_id' en {ruta}. Columnas: {df.columns.tolist()}")
        exit()
    return df

df_human = cargar_y_limpiar(ruta_humano)
df_gemma = cargar_y_limpiar(ruta_gemma)
df_qwen  = cargar_y_limpiar(ruta_qwen)
df_llama = cargar_y_limpiar(ruta_llama)

# ==========================================
# 3. PROCESAMIENTO MULTIETIQUETA (HUMANO)
# ==========================================
# Identificamos las columnas de PB del 1 al 6 (ignorando pb_drive)
cols_pb = ['1stpb', '2ndpb', '3rdpb', '4thpb', '5thpb', '6thpb']
columnas_existentes = [col for col in cols_pb if col in df_human.columns]

def extraer_conjunto_pbs_humano(row):
    pbs = set()
    for col in columnas_existentes:
        val = str(row[col]).strip()
        if val.lower() not in ['nan', 'none', '']:
            # Quitar el ".0" si Pandas lo leyó como decimal
            if val.endswith('.0'): val = val[:-2]
            if val.isdigit():
                pbs.add(f"PB{val}")
            elif val.upper().startswith('PB'):
                pbs.add(val.upper())
    
    return pbs if len(pbs) > 0 else {'None'}

df_human['Human_PBs_Set'] = df_human.apply(extraer_conjunto_pbs_humano, axis=1)
df_human = df_human[['doc_id', 'Human_PBs_Set']]

# ==========================================
# 4. PROCESAMIENTO MULTIETIQUETA (LLMs)
# ==========================================
def extraer_conjunto_pbs_llm(val):
    val = str(val).strip()
    if val.lower() in ['nan', 'none', '']:
        return {'None'}
    
    # Extraemos todos los PBs que haya devuelto el LLM separados por comas
    pbs = set()
    for part in val.split(','):
        p = part.strip().upper()
        if p.startswith('PB'): pbs.add(p)
        
    return pbs if len(pbs) > 0 else {'None'}

df_gemma['Gemma_PBs_Set'] = df_gemma['llm_predicted_pbs'].apply(extraer_conjunto_pbs_llm)
df_qwen['Qwen_PBs_Set']   = df_qwen['llm_predicted_pbs'].apply(extraer_conjunto_pbs_llm)
df_llama['Llama_PBs_Set'] = df_llama['llm_predicted_pbs'].apply(extraer_conjunto_pbs_llm)

# Unimos todo
df_master = df_human.merge(df_gemma[['doc_id', 'Gemma_PBs_Set', 'inference_time_sec']], on='doc_id', how='inner')
df_master = df_master.merge(df_qwen[['doc_id', 'Qwen_PBs_Set', 'inference_time_sec']], on='doc_id', how='inner', suffixes=('_gemma', '_qwen'))
df_master = df_master.merge(df_llama[['doc_id', 'Llama_PBs_Set', 'inference_time_sec']], on='doc_id', how='inner')
df_master.rename(columns={'inference_time_sec_gemma': 'Gemma_Time', 'inference_time_sec_qwen': 'Qwen_Time', 'inference_time_sec': 'Llama_Time'}, inplace=True)

total_docs = len(df_master)
if total_docs == 0:
    print("❌ ERROR: La tabla unida está vacía. Revisa los IDs.")
    exit()

# ==========================================
# 5. MOTOR DE CÁLCULO DE MÉTRICAS AVANZADAS
# ==========================================
def calcular_metricas_modelo(col_modelo):
    acuerdos = 0
    positivity_bias = 0
    rigurosidad = 0
    total_nones = 0
    
    for _, row in df_master.iterrows():
        humano_set = row['Human_PBs_Set']
        modelo_set = row[col_modelo]
        
        # 1. ACUERDO FLEXIBLE (Hay intersección)
        if humano_set == {'None'} and modelo_set == {'None'}:
            acuerdos += 1
        elif humano_set != {'None'} and modelo_set != {'None'} and len(humano_set.intersection(modelo_set)) > 0:
            acuerdos += 1
            
        # 2. POSITIVITY BIAS (Humano dice None, IA fuerza un PB)
        if humano_set == {'None'} and modelo_set != {'None'}:
            positivity_bias += 1
            
        # 3. RIGUROSIDAD/FILTRO (Humano pone PB, IA dice None porque es irrelevante)
        if humano_set != {'None'} and modelo_set == {'None'}:
            rigurosidad += 1
            
        # 4. Total de rechazos de la IA
        if modelo_set == {'None'}:
            total_nones += 1
            
    return {
        "Acuerdo_Flexible": (acuerdos / total_docs) * 100,
        "Positivity_Bias": (positivity_bias / total_docs) * 100,
        "Rigurosidad": (rigurosidad / total_docs) * 100,
        "Tasa_Rechazo": (total_nones / total_docs) * 100
    }

m_gemma = calcular_metricas_modelo('Gemma_PBs_Set')
m_qwen  = calcular_metricas_modelo('Qwen_PBs_Set')
m_llama = calcular_metricas_modelo('Llama_PBs_Set')

# ==========================================
# 6. IMPRESIÓN DEL INFORME FINAL
# ==========================================
print("\n" + "█"*60)
print(" 🔬 REPORTE DE MÉTRICAS AVANZADAS (PROYECTO UPV-EARTH)")
print("█"*60)
print(f"Total de documentos evaluados: {total_docs}\n")

print("▶ 1. TASA DE ACUERDO FLEXIBLE (El LLM acertó al menos un PB humano):")
print(f"   - Llama 3.1 (8B)  : {m_llama['Acuerdo_Flexible']:.2f}%")
print(f"   - Qwen 2.5 (14B)  : {m_qwen['Acuerdo_Flexible']:.2f}%")
print(f"   - Gemma 4 (26B)   : {m_gemma['Acuerdo_Flexible']:.2f}%")
print("   (NOTA: Un acuerdo muy alto puede ser bueno, pero cuidado si el humano se equivocó).\n")

print("▶ 2. TASA DE RIGUROSIDAD / CORRECCIÓN DE SESGO (Humano asigna PB, pero el LLM dice 'None'):")
print(f"   - Llama 3.1 (8B)  : {m_llama['Rigurosidad']:.2f}% (Poca rigurosidad = se cree todo)")
print(f"   - Qwen 2.5 (14B)  : {m_qwen['Rigurosidad']:.2f}% (Filtra la basura metodológica)")
print(f"   - Gemma 4 (26B)   : {m_gemma['Rigurosidad']:.2f}% (El más estricto con las reglas)\n")

print("▶ 3. TASA DE 'POSITIVITY BIAS' (Humano dice None, pero el LLM fuerza un PB inventado):")
print(f"   - Llama 3.1 (8B)  : {m_llama['Positivity_Bias']:.2f}% (Peligro de Alucinación Verde)")
print(f"   - Qwen 2.5 (14B)  : {m_qwen['Positivity_Bias']:.2f}%")
print(f"   - Gemma 4 (26B)   : {m_gemma['Positivity_Bias']:.2f}%\n")

print("▶ 4. RENDIMIENTO COMPUTACIONAL (Tiempos de Inferencia por Abstract):")
print(f"   - Llama 3.1 (8B)  : Media {df_master['Llama_Time'].mean():.2f}s | Max {df_master['Llama_Time'].max():.2f}s")
print(f"   - Qwen 2.5 (14B)  : Media {df_master['Qwen_Time'].mean():.2f}s | Max {df_master['Qwen_Time'].max():.2f}s")
print(f"   - Gemma 4 (26B)   : Media {df_master['Gemma_Time'].mean():.2f}s | Max {df_master['Gemma_Time'].max():.2f}s\n")

print("█"*60)

# Exportar tabla amigable
def set_to_string(s): return ", ".join(list(s))
df_master['Human_PBs_Set'] = df_master['Human_PBs_Set'].apply(set_to_string)
df_master['Gemma_PBs_Set'] = df_master['Gemma_PBs_Set'].apply(set_to_string)
df_master['Qwen_PBs_Set']  = df_master['Qwen_PBs_Set'].apply(set_to_string)
df_master['Llama_PBs_Set'] = df_master['Llama_PBs_Set'].apply(set_to_string)

ruta_salida = OUTPUTS_DIR / 'Matriz_Multietiqueta_Final.csv'
df_master.to_csv(ruta_salida, index=False, encoding='utf-8-sig')
print(f"✅ Matriz detallada guardada en: {ruta_salida}")