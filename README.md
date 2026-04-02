# CloudMarket

Local storefront project with:
- `frontend`: React + Vite
- `backend`: FastAPI + SQLAlchemy + SQLite

## Run Backend

```powershell
cd backend
.\venv\Scripts\activate
uvicorn main:app --reload --port 8000
```

Backend automatically:
- creates SQLite tables
- seeds demo products on first run
- exposes `GET /api/products`
- exposes `GET /api/products/{slug}`
- exposes `GET /api/health`
- stores SQLite data in your system temp folder under `cloudmarket/shop.db`

## Run Frontend

```powershell
cd frontend
npm install
npm run dev
```

Frontend default API base URL:
- `http://localhost:8000`

Optional override:

```powershell
$env:VITE_API_BASE_URL="http://localhost:8000"
npm run dev
```

## Production Build

```powershell
cd frontend
npm run build
```
