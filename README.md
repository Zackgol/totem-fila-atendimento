# Totem de Atendimento

API feita com FastAPI para controlar a fila de atendimento presencial de um estabelecimento.

## Como rodar

```
pip install -r requirements.txt
uvicorn main:app --reload
```

Documentação em http://127.0.0.1:8000/docs

## Rotas

| Método | Rota | O que faz |
|---|---|---|
| GET | /fila | Lista quem está esperando |
| GET | /fila/{id} | Mostra o cliente na posição informada |
| POST | /fila | Coloca um cliente na fila (`nome`, `tipo` N ou P) |
| PUT | /fila | Chama o próximo, todo mundo anda uma posição |
| DELETE | /fila/{id} | Tira o cliente da posição informada |

Clientes prioritários (P) entram na frente dos normais (N), mas depois dos outros prioritários que já estavam esperando.

Exemplo de POST:

```json
{
  "nome": "Maria",
  "tipo": "P"
}
```
