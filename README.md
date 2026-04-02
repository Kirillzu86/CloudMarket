# CloudMarket

Storefront monorepo:
- `frontend`: React + Vite
- `backend`: FastAPI + SQLAlchemy

## Local Run

Backend:

```powershell
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Frontend:

```powershell
cd frontend
npm install
$env:VITE_API_BASE_URL="http://localhost:8000"
npm run dev
```

## Production Notes

- Backend seeds demo products automatically on first startup.
- Default SQLite path is `backend/data/shop.db`.
- You can override storage with `DATABASE_URL` or `CLOUDMARKET_DATA_DIR`.
- Frontend defaults to same-origin API calls, so in production it works well behind a reverse proxy.

## Coolify Deployment

Create two services from this repository.

Backend service:
- Build context: `/backend`
- Dockerfile: `Dockerfile`
- Port: `8000`
- Persistent storage: mount a volume to `/app/data`
- Required env:
  `CLOUDMARKET_JWT_SECRET=replace-with-a-long-random-secret`
  `CLOUDMARKET_ALLOWED_ORIGINS=https://your-frontend-domain`

Frontend service:
- Build context: `/frontend`
- Dockerfile: `Dockerfile`
- Port: `80`

If both services are in the same Coolify network, the frontend container already proxies `/api/*` to `http://backend:8000`.

## API Endpoints

- `GET /api/products`
- `GET /api/products/{slug}`
- `GET /api/health`
- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/auth/me`
