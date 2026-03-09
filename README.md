# AI Beoordelingsplatform (MVP codebasis)

Deze repository bevat:
- Product- en architectuurontwerp in `docs/product_en_technisch_ontwerp.md`
- FastAPI backend in `backend/`
- React + Vite frontend in `frontend/`

## Snel starten

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Open daarna `http://localhost:5173`.

## MVP-functionaliteit
- Framework aanmaken via beheerpagina.
- Document uploaden (txt/md).
- Analyse per vaardigheid met:
  - huidig niveau,
  - onderbouwing,
  - bewijs in tekst,
  - hiaten,
  - ontwikkeladvies.
- Resultaat later terugkijken via resultatenroute.
