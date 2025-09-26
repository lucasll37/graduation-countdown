from fastapi import FastAPI, HTTPException
from datetime import datetime, timedelta
import os
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="Contador de Formatura API",
    description="API que retorna quanto tempo falta para a formatura",
    version="1.0.0"
)

class GraduationResponse(BaseModel):
    dias_restantes: int
    horas_restantes: int
    minutos_restantes: int
    segundos_restantes: int
    tempo_total_segundos: int
    data_formatura: str
    mensagem: str
    ja_formado: bool

class ConfigFormatura(BaseModel):
    data_formatura: str  # formato: "YYYY-MM-DD"
    hora_formatura: Optional[str] = "09:00"  # formato: "HH:MM"

# Data padrão da formatura (pode ser alterada via variável de ambiente ou endpoint)
DATA_FORMATURA_DEFAULT = "2024-12-15"
HORA_FORMATURA_DEFAULT = "09:00"

def obter_data_formatura():
    """Obtém a data de formatura das variáveis de ambiente ou usa o padrão"""
    data_str = os.getenv("DATA_FORMATURA", DATA_FORMATURA_DEFAULT)
    hora_str = os.getenv("HORA_FORMATURA", HORA_FORMATURA_DEFAULT)
    
    try:
        data_formatura = datetime.strptime(f"{data_str} {hora_str}", "%Y-%m-%d %H:%M")
        return data_formatura
    except ValueError:
        # Se houver erro na conversão, usa data padrão
        return datetime.strptime(f"{DATA_FORMATURA_DEFAULT} {HORA_FORMATURA_DEFAULT}", "%Y-%m-%d %H:%M")

def calcular_tempo_restante(data_formatura: datetime) -> dict:
    """Calcula o tempo restante até a formatura"""
    agora = datetime.now()
    
    if agora >= data_formatura:
        return {
            "dias_restantes": 0,
            "horas_restantes": 0,
            "minutos_restantes": 0,
            "segundos_restantes": 0,
            "tempo_total_segundos": 0,
            "ja_formado": True,
            "mensagem": "🎓 Parabéns! Você já se formou!"
        }
    
    tempo_restante = data_formatura - agora
    
    dias = tempo_restante.days
    segundos_restantes = tempo_restante.seconds
    
    horas = segundos_restantes // 3600
    minutos = (segundos_restantes % 3600) // 60
    segundos = segundos_restantes % 60
    
    # Mensagem motivacional baseada no tempo restante
    if dias > 365:
        mensagem = f"📚 Ainda há muito tempo! Faltam {dias} dias para a formatura. Continue estudando!"
    elif dias > 30:
        mensagem = f"📖 Faltam {dias} dias! O fim está se aproximando, mantenha o foco!"
    elif dias > 7:
        mensagem = f"⏰ Última semana! Apenas {dias} dias restantes!"
    elif dias > 0:
        mensagem = f"🔥 Reta final! Faltam apenas {dias} dias!"
    else:
        mensagem = f"🚀 É hoje! Faltam apenas {horas}h {minutos}m {segundos}s!"
    
    return {
        "dias_restantes": dias,
        "horas_restantes": horas,
        "minutos_restantes": minutos,
        "segundos_restantes": segundos,
        "tempo_total_segundos": int(tempo_restante.total_seconds()),
        "ja_formado": False,
        "mensagem": mensagem
    }

@app.get("/", response_model=GraduationResponse)
async def tempo_para_formatura():
    """
    Retorna quanto tempo falta para a formatura
    """
    data_formatura = obter_data_formatura()
    resultado = calcular_tempo_restante(data_formatura)
    
    return GraduationResponse(
        **resultado,
        data_formatura=data_formatura.strftime("%d/%m/%Y às %H:%M")
    )

@app.get("/config")
async def obter_configuracao():
    """
    Retorna a configuração atual da data de formatura
    """
    data_formatura = obter_data_formatura()
    return {
        "data_formatura": data_formatura.strftime("%Y-%m-%d"),
        "hora_formatura": data_formatura.strftime("%H:%M"),
        "data_formatada": data_formatura.strftime("%d/%m/%Y às %H:%M")
    }

@app.post("/config")
async def configurar_formatura(config: ConfigFormatura):
    """
    Configura uma nova data de formatura (apenas para a sessão atual)
    """
    try:
        nova_data = datetime.strptime(f"{config.data_formatura} {config.hora_formatura}", "%Y-%m-%d %H:%M")
        
        # Em uma aplicação real, você salvaria isso em um banco de dados
        # Por simplicidade, vamos apenas retornar a confirmação
        
        return {
            "sucesso": True,
            "mensagem": "Data de formatura configurada com sucesso!",
            "nova_data": nova_data.strftime("%d/%m/%Y às %H:%M"),
            "nota": "Esta configuração é apenas para demonstração. Para persistir, configure as variáveis de ambiente."
        }
    except ValueError:
        raise HTTPException(
            status_code=400, 
            detail="Formato de data inválido. Use YYYY-MM-DD para data e HH:MM para hora."
        )

@app.get("/health")
async def health_check():
    """
    Endpoint de health check
    """
    return {"status": "OK", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)