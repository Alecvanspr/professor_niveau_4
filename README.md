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
- Document uploaden (txt/md/pdf of zip met txt/md/pdf-bestanden).
- Analyse per vaardigheid met:
  - huidig niveau,
  - onderbouwing,
  - bewijs in tekst,
  - hiaten,
  - ontwikkeladvies.
- Resultaat later terugkijken via resultatenroute.


## Ondersteunde documentformaten
- Direct upload: `.txt`, `.md`, `.pdf`, `.zip`
- Voor `.zip`: alleen `.txt`, `.md` en `.pdf` bestanden worden ingelezen
- Niveau-restricties configureer je in `backend/app/config/level_constraints.json`
- Restricties zijn opvraagbaar via `GET /api/constraints/levels`
