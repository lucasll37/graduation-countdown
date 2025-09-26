# 🎓 Graduation Countdown API

Uma API simples em Python/FastAPI que retorna quanto tempo falta para sua formatura! Totalmente dockerizada para facilitar o deploy.

## 📋 Estrutura do Projeto

```
graduation-countdown/
├── main.py              # Código principal da API
├── requirements.txt     # Dependências Python
├── Dockerfile          # Configuração do container
├── .dockerignore       # Arquivos ignorados pelo Docker
└── README.md           # Este arquivo
```

## 🚀 Como Usar com Docker

### 1. **Build da Imagem**
```bash
docker build -t graduation-api .
```

### 2. **Executar o Container**

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
  -e DATA_FORMATURA=2025-06-30 \
  -e HORA_FORMATURA=14:00 \
  --name graduation-countdown \
  graduation-api
```

### 3. **Acessar a API**
- **API Principal:** http://localhost:8000
- **Documentação:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

## 🐳 Comandos Docker Essenciais

### **Gerenciamento Básico**
```bash
# Listar containers em execução
docker ps

# Ver todos os containers (incluindo parados)
docker ps -a

# Parar container
docker stop graduation-countdown

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

# 2. Parar container anterior (se existir)
docker stop graduation-countdown 2>/dev/null || true
docker rm graduation-countdown 2>/dev/null || true

# 3. Executar novo container
docker run -d -p 8000:8000 \
  -e DATA_FORMATURA=2024-12-15 \
  -e HORA_FORMATURA=09:00 \
  --name graduation-countdown \
  --restart unless-stopped \
  graduation-api

# 4. Verificar se está funcionando
docker logs graduation-countdown
```

### **Desenvolvimento e Debug**
```bash
# Executar em modo interativo
docker run -it -p 8000:8000 graduation-api

# Abrir shell no container em execução
docker exec -it graduation-countdown /bin/bash

# Executar comandos no container
docker exec graduation-countdown curl http://localhost:8000/health
```

## ⚙️ Configuração da Data de Formatura

### **Via Variáveis de Ambiente**
```bash
docker run -d -p 8000:8000 \
  -e DATA_FORMATURA=2025-07-15 \
  -e HORA_FORMATURA=14:30 \
  --name graduation-countdown \
  graduation-api
```

### **Via API (após container estar rodando)**
```bash
# Verificar configuração atual
curl http://localhost:8000/config

# Alterar data via API
curl -X POST http://localhost:8000/config \
  -H "Content-Type: application/json" \
  -d '{"data_formatura": "2025-07-15", "hora_formatura": "14:30"}'
```

## 📊 Endpoints da API

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/` | GET | Retorna countdown completo para formatura |
| `/config` | GET | Mostra configuração atual da data |
| `/config` | POST | Altera data da formatura |
| `/health` | GET | Health check da aplicação |
| `/docs` | GET | Documentação interativa (Swagger) |
| `/redoc` | GET | Documentação alternativa |

## 🔧 Troubleshooting

### **Container não inicia**
```bash
# Ver logs de erro
docker logs graduation-countdown

# Verificar se a porta está livre
netstat -tlnp | grep :8000

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
```

### **Rebuild após mudanças no código**
```bash
# Parar container atual
docker stop graduation-countdown
docker rm graduation-countdown

# Rebuild sem cache
docker build --no-cache -t graduation-api .

# Executar novo container
docker run -d -p 8000:8000 --name graduation-countdown graduation-api
```

## 📝 Exemplo de Resposta da API

```json
{
  "dias_restantes": 180,
  "horas_restantes": 15,
  "minutos_restantes": 30,
  "segundos_restantes": 45,
  "tempo_total_segundos": 15681045,
  "data_formatura": "15/12/2024 às 09:00",
  "mensagem": "📚 Ainda há muito tempo! Faltam 180 dias para a formatura. Continue estudando!",
  "ja_formado": false
}
```

## 🎯 Scripts Úteis

### **Script de Deploy Rápido**
```bash
#!/bin/bash
# deploy.sh

echo "🚀 Deploying Graduation API..."

# Build
docker build -t graduation-api .

# Stop old container
docker stop graduation-countdown 2>/dev/null || true
docker rm graduation-countdown 2>/dev/null || true

# Run new container
docker run -d -p 8000:8000 \
  -e DATA_FORMATURA=${DATA_FORMATURA:-2024-12-15} \
  -e HORA_FORMATURA=${HORA_FORMATURA:-09:00} \
  --name graduation-countdown \
  --restart unless-stopped \
  graduation-api

echo "✅ API deployed successfully!"
echo "🌐 Access: http://localhost:8000"
echo "📚 Docs: http://localhost:8000/docs"
```

### **Script de Limpeza**
```bash
#!/bin/bash
# cleanup.sh

echo "🧹 Cleaning up..."

# Stop and remove container
docker stop graduation-countdown 2>/dev/null || true
docker rm graduation-countdown 2>/dev/null || true

# Remove image
docker rmi graduation-api 2>/dev/null || true

# Clean unused resources
docker system prune -f

echo "✅ Cleanup complete!"
```

## 🌟 Comandos em Uma Linha

```bash
# Deploy completo
docker build -t graduation-api . && docker stop graduation-countdown 2>/dev/null || true && docker rm graduation-countdown 2>/dev/null || true && docker run -d -p 8000:8000 --name graduation-countdown graduation-api

# Verificar status
docker ps | grep graduation && curl -s http://localhost:8000/health | python3 -m json.tool

# Rebuild e redeploy
docker build --no-cache -t graduation-api . && docker stop graduation-countdown && docker rm graduation-countdown && docker run -d -p 8000:8000 --name graduation-countdown graduation-api
```

## 🎓 Personalização

Para alterar a data padrão da formatura, edite as variáveis de ambiente no `Dockerfile`:
```dockerfile
ENV DATA_FORMATURA=2025-07-15
ENV HORA_FORMATURA=14:00
```

Ou passe as variáveis no comando `docker run` como mostrado nos exemplos acima.

---

**🎉 Pronto! Sua API de countdown para formatura está dockerizada e pronta para uso!**