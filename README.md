# MY FRIEND BOT

## Descrição

Chatbot interativo

## Índice

- [Instalação](#instalação)
- [Uso](#uso)

## Instalação
1 - Clone o projeto para sua máquina.

```bash
git clone https://github.com/roxreis/chatbot-ia.git
```
2 - Renomeie o arquivo _.env-exemplo_ para _.env_ na raiz do projeto.

3 - Gere uma chave de api gratuita no site: https://console.groq.com/keys

4 - Adicione a seguinte variáveil de ambiente ao _.env_:

GROQ_API_KEY=sua_chave_api

4 - Por último faça o build do projeto.

```bash
cd chatbot-ia
docker compose up --build
```

## Uso
Acesso ao sistema:
http://localhost:8501/

Acesso ao Database Qdrant client:
http://localhost:6333/dashboard


