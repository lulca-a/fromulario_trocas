# fromulario_trocas
formulario de trocas de escala

## Instalação e ambiente Python

1. Crie e ative o ambiente virtual:
   - `python -m venv .venv`
   - `.\.venv\Scripts\activate`

2. Instale as dependências:
   - `pip install -r requirements.txt`

3. Crie o arquivo `.env` a partir do `.env.example` e preencha:
   - `EMAIL_FROM`
   - `EMAIL_PASSWORD`
   - `SMTP_HOST` (padrão: `smtp.gmail.com`)
   - `SMTP_PORT` (padrão: `587`)
   - `EMAIL_ADMIN`

4. Execute o backend:
   - `python backend/backend.py`

## Estrutura de pastas
- `backend/` - lógica e endpoints do servidor
- `frontend/` - arquivos HTML e JavaScript do cliente

## Notas
- O projeto agora usa `python-dotenv` para carregar variáveis de ambiente.
- O arquivo `.gitignore` já ignora `.venv` e `.env`.
