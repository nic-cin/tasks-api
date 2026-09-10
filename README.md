# tasks-api

```
rest api de tarefas
fastapi · sqlmodel · sqlite · pytest
```

---

## rodando

```
git clone https://github.com/nic-cin/tasks-api
cd tasks-api
python -m venv venv
venv\Scripts\activate        # linux/mac: source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

docs interativa: http://127.0.0.1:8000/docs

---

## endpoints

| método | rota | descrição |
|---|---|---|
| POST | `/tasks/` | cria tarefa |
| GET | `/tasks/` | lista tarefas (`?done=true` / `?done=false` filtra) |
| GET | `/tasks/{id}` | busca por id |
| PATCH | `/tasks/{id}` | atualiza campos enviados |
| DELETE | `/tasks/{id}` | apaga |

---

## exemplo

```
curl -X POST http://127.0.0.1:8000/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title": "estudar fastapi", "description": "etapa 3"}'
```

```
{"id":1,"title":"estudar fastapi","description":"etapa 3","done":false,"created_at":"2026-09-10T15:54:11"}
```

---

## estrutura

```
tasks-api/
├── app/
│   ├── main.py          # app, lifespan, include_router
│   ├── database.py      # engine sqlite, sessão por requisição
│   ├── models.py        # Task (tabela)
│   ├── schemas.py       # TaskCreate / TaskUpdate / TaskRead
│   └── routers/
│       └── tasks.py     # CRUD + filtro
├── tests/
│   └── test_tasks.py    # pytest com sqlite em memória
└── requirements.txt
```

---

## testes

```
pytest -v
```

9 testes: crud completo, validação de entrada (422), 404, filtro por status.

---

## conceitos

```
rest            verbos http, códigos de status, query params
validação       pydantic/sqlmodel nos schemas de entrada
orm             classe python → tabela sql
injeção de dep. Depends(get_session), sessão por requisição
testes          TestClient + dependency_overrides + banco em memória
```

---

## próximos passos

```
- migrar para mysql / supabase
- deploy (render / railway)
- autenticação
```

---

*primeiro projeto backend. feito enquanto aprendo.*