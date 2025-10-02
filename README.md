# 🎓 Graduation Countdown API

Uma API moderna em Python/FastAPI com interface visual interativa que mostra quanto tempo falta para sua formatura! Totalmente dockerizada e pronta para deploy.

## ✨ Características

- 🎨 **Interface Visual Moderna** - Homepage com countdown animado em tempo real
- 🔄 **Auto-refresh** - Atualização automática a cada 30 segundos
- 📱 **Responsivo** - Design adaptável para desktop e mobile
- 🐳 **Dockerizado** - Deploy fácil com containers
- 📊 **API REST** - Endpoints JSON para integração
- ⚙️ **Configurável** - Defina data e hora via variáveis de ambiente

## 📋 Estrutura do Projeto

```
graduation-countdown/
├── main.py              # Código principal da API FastAPI
├── requirements.txt     # Dependências Python
├── Dockerfile          # Configuração do container Docker
├── .dockerignore       # Arquivos ignorados pelo Docker
├── .gitignore          # Arquivos ignorados pelo Git
├── Makefile            # Automação de tarefas
└── README.md           # Este arquivo
```

## 🚀 Como Usar

### Opção 1: Com Docker (Recomendado)

#### 1. **Build da Imagem**
```bash
docker build -t graduation-api .
```

#### 2. **Executar o Container**

**Execução básica:**
```bash
docker run -p 8000:8000 graduation-api
```

**Execução em background:**
```bash
docker run -d -p 8000:8000 --name graduation-countdown graduation-api
```

**Com data personalizada:**
```bash
docker run -d -p 8000:8000 \
  -e DATA_FORMATURA=2025-12-19 \
  -e HORA_FORMATURA=10:00 \
  --name graduation-countdown \
  graduation-api
```

#### 3. **Acessar a Aplicação**
- **Interface Visual:** http://localhost:8000
- **API JSON:** http://localhost:8000/api
- **Health Check:** http://localhost:8000/health
- **Documentação Swagger:** http://localhost:8000/docs
- **Documentação ReDoc:** http://localhost:8000/redoc

### Opção 2: Com Makefile (Desenvolvimento Local)

#### 1. **Criar Ambiente Virtual**
```bash
make create_env
```

#### 2. **Executar em Modo Desenvolvimento**
```bash
# Com data padrão
make run

# Com data personalizada
DATA_FORMATURA=2025-12-19 HORA_FORMATURA=10:00 make run
```

A aplicação será iniciada em modo desenvolvimento com reload automático em http://localhost:8000

## 📊 Endpoints da API

| Endpoint | Método | Descrição | Retorno |
|----------|--------|-----------|---------|
| `/` | GET | Interface visual com countdown animado | HTML |
| `/api` | GET | Dados do countdown em formato JSON | JSON |
| `/health` | GET | Health check da aplicação | JSON |
| `/docs` | GET | Documentação interativa (Swagger UI) | HTML |
| `/redoc` | GET | Documentação alternativa (ReDoc) | HTML |

### Exemplo de Resposta da API (`/api`)

```json
{
  "dias_restantes": 445,
  "horas_restantes": 15,
  "minutos_restantes": 30,
  "segundos_restantes": 45,
  "tempo_total_segundos": 38473845,
  "data_formatura": "19/12/2025 às 10:00",
  "mensagem": "📖 Faltam 445 dias!!!",
  "ja_formado": false
}
```

### Exemplo de Health Check (`/health`)

```json
{
  "status": "OK",
  "timestamp": "2025-10-02T14:30:00.123456"
}
```

## 🐳 Comandos Docker Essenciais

### **Gerenciamento Básico**
```bash
# Listar containers em execução
docker ps

# Ver todos os containers (incluindo parados)
docker ps -a

# Parar container
docker stop graduation-countdown

# Iniciar container parado
docker start graduation-countdown

# Reiniciar container
docker restart graduation-countdown

# Remover container
docker rm graduation-countdown

# Ver logs do container
docker logs graduation-countdown

# Ver logs em tempo real
docker logs -f graduation-countdown
```

### **Build e Deploy Completo**
```bash
# 1. Build da imagem
docker build -t graduation-api .

# 2. Parar e remover container anterior (se existir)
docker stop graduation-countdown 2>/dev/null || true
docker rm graduation-countdown 2>/dev/null || true

# 3. Executar novo container
docker run -d -p 8000:8000 \
  -e DATA_FORMATURA=2025-12-19 \
  -e HORA_FORMATURA=10:00 \
  --name graduation-countdown \
  --restart unless-stopped \
  graduation-api

# 4. Verificar se está funcionando
docker logs graduation-countdown
curl http://localhost:8000/health
```

### **Desenvolvimento e Debug**
```bash
# Executar em modo interativo (ver logs em tempo real)
docker run -it -p 8000:8000 graduation-api

# Abrir shell no container em execução
docker exec -it graduation-countdown /bin/bash

# Executar comandos no container
docker exec graduation-countdown curl http://localhost:8000/health

# Inspecionar container
docker inspect graduation-countdown

# Ver uso de recursos
docker stats graduation-countdown
```

## ⚙️ Configuração da Data de Formatura

### **Método 1: Variáveis de Ambiente (Build/Run)**

No `Dockerfile` (padrão):
```dockerfile
ENV DATA_FORMATURA=2025-12-19
ENV HORA_FORMATURA=10:00
```

Ou no comando `docker run`:
```bash
docker run -d -p 8000:8000 \
  -e DATA_FORMATURA=2025-07-15 \
  -e HORA_FORMATURA=14:30 \
  --name graduation-countdown \
  graduation-api
```

### **Método 2: Makefile (Desenvolvimento Local)**

```bash
# Editar no Makefile ou passar via linha de comando
DATA_FORMATURA=2025-12-19 HORA_FORMATURA=10:00 make run
```

### **Formato das Datas**
- **DATA_FORMATURA**: `YYYY-MM-DD` (exemplo: `2025-12-19`)
- **HORA_FORMATURA**: `HH:MM` (exemplo: `10:00`)

## 🎨 Interface Visual

A homepage (`/`) apresenta:
- ⏰ **Countdown em tempo real** dividido em dias, horas, minutos e segundos
- 📅 **Data da formatura** formatada
- 💬 **Mensagem motivacional** que muda conforme a proximidade
- 🔄 **Auto-refresh** automático a cada 30 segundos
- 📱 **Design responsivo** para todos os dispositivos
- 🎭 **Animações suaves** e efeitos visuais modernos

## 🔧 Troubleshooting

### **Container não inicia**
```bash
# Ver logs de erro
docker logs graduation-countdown

# Verificar se a porta 8000 está livre
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Executar em modo interativo para debug
docker run -it graduation-api
```

### **API não responde**
```bash
# Verificar se container está rodando
docker ps | grep graduation

# Testar conexão
curl http://localhost:8000/health

# Ver logs em tempo real
docker logs -f graduation-countdown

# Verificar status do processo dentro do container
docker exec graduation-countdown ps aux
```

### **Erro de permissão ou porta ocupada**
```bash
# Usar outra porta
docker run -d -p 8080:8000 --name graduation-countdown graduation-api

# Parar processo que está usando a porta
lsof -ti:8000 | xargs kill  # macOS/Linux
```

### **Rebuild após mudanças no código**
```bash
# Parar e remover container atual
docker stop graduation-countdown
docker rm graduation-countdown

# Rebuild sem cache (forçar reconstrução)
docker build --no-cache -t graduation-api .

# Executar novo container
docker run -d -p 8000:8000 --name graduation-countdown graduation-api
```

### **Problemas com data/hora**
```bash
# Verificar variáveis de ambiente
docker exec graduation-countdown env | grep FORMATURA

# Testar com nova data
docker run -d -p 8000:8000 \
  -e DATA_FORMATURA=2025-12-31 \
  -e HORA_FORMATURA=23:59 \
  --name graduation-test \
  graduation-api
```

## 🎯 Scripts Úteis

### **Script de Deploy Rápido** (`deploy.sh`)
```bash
#!/bin/bash
# deploy.sh - Deploy automatizado

echo "🚀 Deploying Graduation API..."

# Build
docker build -t graduation-api .

# Stop old container
docker stop graduation-countdown 2>/dev/null || true
docker rm graduation-countdown 2>/dev/null || true

# Run new container
docker run -d -p 8000:8000 \
  -e DATA_FORMATURA=${DATA_FORMATURA:-2025-12-19} \
  -e HORA_FORMATURA=${HORA_FORMATURA:-10:00} \
  --name graduation-countdown \
  --restart unless-stopped \
  graduation-api

echo "✅ API deployed successfully!"
echo "🌐 Interface: http://localhost:8000"
echo "📊 API JSON: http://localhost:8000/api"
echo "📚 Docs: http://localhost:8000/docs"

# Verificar status
sleep 2
curl -s http://localhost:8000/health | python3 -m json.tool
```

### **Script de Limpeza** (`cleanup.sh`)
```bash
#!/bin/bash
# cleanup.sh - Limpeza completa

echo "🧹 Cleaning up Docker resources..."

# Stop and remove container
docker stop graduation-countdown 2>/dev/null || true
docker rm graduation-countdown 2>/dev/null || true

# Remove image
docker rmi graduation-api 2>/dev/null || true

# Clean unused resources
docker system prune -f

echo "✅ Cleanup complete!"
```

### **Script de Teste** (`test.sh`)
```bash
#!/bin/bash
# test.sh - Testes básicos da API

BASE_URL="http://localhost:8000"

echo "🧪 Testing Graduation API..."

# Test 1: Health check
echo "1. Health check..."
curl -s ${BASE_URL}/health | python3 -m json.tool

# Test 2: API endpoint
echo -e "\n2. API countdown..."
curl -s ${BASE_URL}/api | python3 -m json.tool

# Test 3: Homepage
echo -e "\n3. Homepage status..."
curl -s -o /dev/null -w "Status: %{http_code}\n" ${BASE_URL}/

echo -e "\n✅ All tests completed!"
```

## 🌟 Comandos em Uma Linha

```bash
# Deploy completo
docker build -t graduation-api . && docker stop graduation-countdown 2>/dev/null || true && docker rm graduation-countdown 2>/dev/null || true && docker run -d -p 8000:8000 --name graduation-countdown graduation-api

# Verificar status completo
docker ps | grep graduation && curl -s http://localhost:8000/health | python3 -m json.tool

# Rebuild e redeploy rápido
docker build --no-cache -t graduation-api . && docker stop graduation-countdown && docker rm graduation-countdown && docker run -d -p 8000:8000 --name graduation-countdown graduation-api

# Ver logs e testar
docker logs -f graduation-countdown & sleep 2 && curl http://localhost:8000/api

# Limpeza completa
docker stop graduation-countdown && docker rm graduation-countdown && docker rmi graduation-api && docker system prune -f
```

## 📦 Dependências

- **Python 3.11+**
- **FastAPI 0.104.1** - Framework web moderno
- **Uvicorn 0.24.0** - Servidor ASGI
- **Pydantic 2.5.0** - Validação de dados

## 🔐 Variáveis de Ambiente

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `DATA_FORMATURA` | `2025-12-19` | Data da formatura (YYYY-MM-DD) |
| `HORA_FORMATURA` | `10:00` | Hora da formatura (HH:MM) |

## 📝 Exemplos de Uso da API

### **cURL**
```bash
# Get countdown data
curl http://localhost:8000/api

# Health check
curl http://localhost:8000/health
```

### **Python**
```python
import requests

# Get countdown
response = requests.get('http://localhost:8000/api')
data = response.json()
print(f"Faltam {data['dias_restantes']} dias!")

# Health check
health = requests.get('http://localhost:8000/health')
print(health.json())
```

### **JavaScript**
```javascript
// Get countdown
fetch('http://localhost:8000/api')
  .then(response => response.json())
  .then(data => {
    console.log(`Faltam ${data.dias_restantes} dias!`);
  });

// Health check
fetch('http://localhost:8000/health')
  .then(response => response.json())
  .then(data => console.log(data));
```

## 🚀 Deploy em Produção

### **Docker Compose** (recomendado)
```yaml
version: '3.8'

services:
  graduation-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATA_FORMATURA=2025-12-19
      - HORA_FORMATURA=10:00
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

Executar com:
```bash
docker-compose up -d
```

### **Considerações para Produção**
- Configure um **reverse proxy** (Nginx, Traefik)
- Adicione **HTTPS** com certificado SSL
- Implemente **rate limiting**
- Configure **logs persistentes**
- Use **health checks** para monitoramento
- Considere usar **Docker Swarm** ou **Kubernetes** para alta disponibilidade

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto é de código aberto e está disponível para uso educacional.