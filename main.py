from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
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
    if dias > 30:
        mensagem = f"📖 Faltam {dias} dias! O fim se aproxima!"
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

@app.get("/", response_class=HTMLResponse)
async def homepage():
    """
    Página principal com interface visual do countdown
    """
    data_formatura = obter_data_formatura()
    resultado = calcular_tempo_restante(data_formatura)
    
    # Emojis baseados no status
    emoji_principal = "🎓" if resultado["ja_formado"] else "⏰"
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Formatura T-25 🎓</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
            }}
            
            .container {{
                text-align: center;
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 3rem;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                max-width: 600px;
                width: 90%;
            }}
            
            .emoji {{
                font-size: 4rem;
                margin-bottom: 1rem;
                animation: bounce 2s infinite;
            }}
            
            @keyframes bounce {{
                0%, 20%, 50%, 80%, 100% {{ transform: translateY(0); }}
                40% {{ transform: translateY(-10px); }}
                60% {{ transform: translateY(-5px); }}
            }}
            
            h1 {{
                font-size: 2.5rem;
                margin-bottom: 1rem;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            }}
            
            .countdown {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
                gap: 1rem;
                margin: 2rem 0;
            }}
            
            .time-unit {{
                background: rgba(255, 255, 255, 0.2);
                border-radius: 15px;
                padding: 1.5rem 1rem;
                border: 1px solid rgba(255, 255, 255, 0.3);
            }}
            
            .time-number {{
                font-size: 2.5rem;
                font-weight: bold;
                display: block;
                text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
            }}
            
            .time-label {{
                font-size: 0.9rem;
                opacity: 0.9;
                margin-top: 0.5rem;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
            
            .message {{
                font-size: 1.2rem;
                margin: 2rem 0;
                padding: 1rem;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                border-left: 4px solid #ffd700;
            }}
            
            .graduation-date {{
                font-size: 1.1rem;
                opacity: 0.8;
                margin-bottom: 2rem;
            }}
            
            .api-links {{
                margin-top: 2rem;
                display: flex;
                gap: 1rem;
                justify-content: center;
                flex-wrap: wrap;
            }}
            
            .api-link {{
                background: rgba(255, 255, 255, 0.2);
                color: white;
                text-decoration: none;
                padding: 0.7rem 1.5rem;
                border-radius: 25px;
                border: 1px solid rgba(255, 255, 255, 0.3);
                transition: all 0.3s ease;
                font-size: 0.9rem;
            }}
            
            .api-link:hover {{
                background: rgba(255, 255, 255, 0.3);
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            }}
            
            .api-links {{
                margin-top: 2rem;
                display: flex;
                gap: 1rem;
                justify-content: center;
                flex-wrap: wrap;
            }}
            
            .api-link {{
                background: rgba(255, 255, 255, 0.2);
                color: white;
                text-decoration: none;
                padding: 0.7rem 1.5rem;
                border-radius: 25px;
                border: 1px solid rgba(255, 255, 255, 0.3);
                transition: all 0.3s ease;
                font-size: 0.9rem;
            }}
            
            .api-link:hover {{
                background: rgba(255, 255, 255, 0.3);
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            }}
            
            .refresh-btn {{
                background: #ffd700;
                color: #333;
                border: none;
                padding: 1rem 2rem;
                border-radius: 25px;
                font-size: 1rem;
                font-weight: bold;
                cursor: pointer;
                margin-top: 1rem;
                transition: all 0.3s ease;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
            
            .refresh-btn:hover {{
                background: #ffed4e;
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            }}
            
            @media (max-width: 768px) {{
                .container {{
                    padding: 2rem 1rem;
                }}
                
                h1 {{
                    font-size: 2rem;
                }}
                
                .countdown {{
                    grid-template-columns: repeat(2, 1fr);
                }}
                
                .time-number {{
                    font-size: 2rem;
                }}
                
                .api-links {{
                    flex-direction: column;
                    align-items: center;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="emoji">{emoji_principal}</div>
            <h1>Countdown para Formatura T-25</h1>
            
            <div class="graduation-date">
                📅 {data_formatura.strftime("%d/%m/%Y às %H:%M")}
            </div>
            
            <div class="countdown">
                <div class="time-unit">
                    <span class="time-number">{resultado['dias_restantes']}</span>
                    <div class="time-label">Dias</div>
                </div>
                <div class="time-unit">
                    <span class="time-number">{resultado['horas_restantes']}</span>
                    <div class="time-label">Horas</div>
                </div>
                <div class="time-unit">
                    <span class="time-number">{resultado['minutos_restantes']}</span>
                    <div class="time-label">Minutos</div>
                </div>
                <div class="time-unit">
                    <span class="time-number">{resultado['segundos_restantes']}</span>
                    <div class="time-label">Segundos</div>
                </div>
            </div>
            
            <div class="message">
                {resultado['mensagem']}
            </div>
            
            <button class="refresh-btn" onclick="window.location.reload()">
                🔄 Atualizar
            </button>
            

        </div>
        
        <script>
            // Auto-refresh a cada 30 segundos
            setTimeout(() => {{
                window.location.reload();
            }}, 30000);
        </script>
    </body>
    </html>
    """
    
    return html_content

@app.get("/api", response_model=GraduationResponse)
async def api_tempo_para_formatura():
    """
    Retorna dados JSON do tempo para formatura (antiga rota principal)
    """
    data_formatura = obter_data_formatura()
    resultado = calcular_tempo_restante(data_formatura)
    
    return GraduationResponse(
        **resultado,
        data_formatura=data_formatura.strftime("%d/%m/%Y às %H:%M")
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