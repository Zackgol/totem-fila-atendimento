from datetime import datetime
from typing import Literal
from zoneinfo import ZoneInfo

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Totem de Atendimento")

clientes = []


class NovoCliente(BaseModel):
    model_config = {"str_strip_whitespace": True}

    nome: str = Field(min_length=1, max_length=20)
    tipo: Literal["N", "P"]


def na_fila():
    aguardando = [c for c in clientes if not c["atendido"]]
    return sorted(aguardando, key=lambda c: c["posicao"])


def mostrar(c):
    return {
        "posicao": c["posicao"],
        "nome": c["nome"],
        "tipo": c["tipo"],
        "data_chegada": c["data_chegada"],
    }


def buscar(posicao):
    for c in na_fila():
        if c["posicao"] == posicao:
            return c
    raise HTTPException(status_code=404, detail=f"Nenhum cliente na posicao {posicao}")


@app.get("/fila")
def listar():
    return [mostrar(c) for c in na_fila()]


@app.get("/fila/{id}")
def ver(id: int):
    return mostrar(buscar(id))


@app.post("/fila", status_code=201)
def entrar(dados: NovoCliente):
    fila = na_fila()

    if dados.tipo == "P":
        pos = len([c for c in fila if c["tipo"] == "P"]) + 1
        for c in fila:
            if c["posicao"] >= pos:
                c["posicao"] += 1
    else:
        pos = len(fila) + 1

    novo = {
        "posicao": pos,
        "nome": dados.nome,
        "tipo": dados.tipo,
        "data_chegada": datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%d/%m/%Y %H:%M:%S"),
        "atendido": False,
    }
    clientes.append(novo)
    return mostrar(novo)


@app.put("/fila")
def chamar_proximo():
    fila = na_fila()
    if not fila:
        return {"mensagem": "A fila esta vazia"}

    chamado = None
    for c in fila:
        c["posicao"] -= 1
        if c["posicao"] == 0:
            c["atendido"] = True
            chamado = c["nome"]

    return {"mensagem": f"{chamado} foi chamado para atendimento", "fila": listar()}


@app.delete("/fila/{id}")
def remover(id: int):
    cliente = buscar(id)
    clientes.remove(cliente)

    for c in na_fila():
        if c["posicao"] > id:
            c["posicao"] -= 1

    return {"mensagem": f"{cliente['nome']} saiu da fila", "fila": listar()}
