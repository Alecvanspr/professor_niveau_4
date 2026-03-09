# AI-gedreven beoordelingsplatform voor documenten

## 1. Productconcept
Het platform helpt gebruikers om documenten te uploaden en automatisch te laten beoordelen tegen een **niveaukader** (rubric). Het doel is dubbel:
1. **Valideren waar iemand nu staat** per vaardigheid.
2. **Ontwikkelgericht verbeteren** richting het volgende niveau.

De beoordeling is transparant door de uitkomst op te splitsen in vier onderdelen per vaardigheid:
- huidig niveau;
- bewijs/signalen uit de tekst;
- hiaten t.o.v. volgend niveau;
- concrete ontwikkelacties.

Het product bestaat uit drie kernmodules:
- **Assessment Studio**: uploaden, analyseren, rapport bekijken.
- **Framework Manager**: niveaukaders en vaardigheden beheren.
- **Evidence Explorer**: per vaardigheid exact zien welke tekstpassages hebben meegewogen.

## 2. Gebruikersrollen en gebruikersflow
### Rollen
- **Kandidaat / Auteur**
  - Uploadt documenten.
  - Kiest beoordelingskader.
  - Bekijkt feedback en ontwikkeladvies.
- **Beoordelaar / Coach**
  - Controleert AI-beoordeling.
  - Geeft aanvullende context of correcties.
  - Monitort voortgang over meerdere documenten.
- **Beheerder**
  - Maakt en onderhoudt niveaukaders.
  - Beheert vaardigheden, niveaubeschrijvingen en beoordelingsrichtlijnen.

### Gebruikersflow
1. Gebruiker uploadt document en selecteert een niveaukader.
2. Systeem extraheert tekst, segmenteert inhoud en start AI-analyse per vaardigheid.
3. Voor elke vaardigheid kiest de engine het best passende niveau op basis van rubric-match.
4. Systeem genereert:
   - onderbouwing;
   - bewijsquotes;
   - hiaten;
   - volgende stap + concrete acties.
5. Resultaat wordt opgeslagen en verschijnt in dashboard.
6. Gebruiker kan later terugkijken, vergelijken en opnieuw analyseren (bijv. na revisie).

## 3. Systeemarchitectuur
Voorgestelde modulair schaalbare architectuur:

- **Frontend (React + TypeScript)**
  - Dashboard, uploadflow, resultaatviewer, beheerpagina.
  - Communiceert met backend via REST.

- **Backend API (FastAPI)**
  - Endpoints voor documenten, frameworks, analyses en resultaten.
  - Asynchrone verwerking van analyse-taken.

- **Analyse-engine**
  - Skill-by-skill beoordelingspipeline.
  - Deterministische rubric scoring + LLM uitleglaag.
  - Uniform JSON-outputcontract om willekeur te beperken.

- **Datalaag**
  - PostgreSQL (in MVP SQLite) voor metadata en resultaten.
  - Optioneel object storage voor originele bestanden.

- **Observability & Governance**
  - Audit trail (welk model, promptversie, rubricversie).
  - Reproduceerbare runs via analyse-config snapshots.

## 4. Technische stack (advies)
### Front-end
- React + TypeScript + Vite
- React Router
- TanStack Query (optioneel later)
- Eenvoudige CSS (uitbreidbaar naar Tailwind)

### Back-end
- Python 3.11+
- FastAPI + Uvicorn
- SQLModel (SQLAlchemy + Pydantic)
- Alembic voor migraties (later)

### AI-laag
- Provider-agnostische LLM-adapter (OpenAI/Azure/andere)
- Prompt templates met expliciet JSON-schema
- Rule-based pre-scoring voor robuustheid

### Data & infra
- PostgreSQL in productie
- SQLite voor lokale MVP
- Docker Compose voor lokale stack

## 5. Datastructuur
### Kernentiteiten
- **Document**: metadata, ruwe tekst, status.
- **Framework**: naam, versie, beschrijving.
- **Skill**: vaardigheid binnen framework.
- **SkillLevel**: niveaudefinitie per skill (1..N).
- **AssessmentResult**: analyse op document + framework.
- **SkillAssessment**: resultaat per skill.
- **EvidenceSnippet**: expliciete bewijsfragmenten met tekstpositie.
- **ImprovementAction**: concrete ontwikkelstappen.

### Belangrijke ontwerpkeuzes
- Versiebeheer op frameworkniveau (zodat oude analyses reproduceerbaar blijven).
- Analyse bevat modelnaam, promptversie en timestamp.
- SkillAssessment bewaart expliciet onderscheid tussen:
  - `current_level`
  - `evidence`
  - `gaps`
  - `next_level_guidance`
  - `improvement_actions`

## 6. AI-analyse stap voor stap
1. **Inname & extractie**
   - Upload document.
   - Extract plain text (MVP: TXT/MD, uitbreidbaar naar PDF/DOCX).

2. **Preprocessing**
   - Opschonen van whitespace/ruis.
   - Segmenteren in alinea’s en zinnen.

3. **Skill-specifieke slicing**
   - Voor elke skill relevante tekstsegmenten selecteren (keyword + embedding match).

4. **Rubric matching (deterministisch)**
   - Voor elk niveau score berekenen op aanwezigheid van niveau-indicatoren.
   - Hoogste score = kandidaatniveau.

5. **LLM-uitleglaag**
   - Input: skilldefinitie, niveaus, gekozen niveau, top-signalen uit tekst.
   - Output in strikt JSON-formaat:
     - inhoudelijke onderbouwing;
     - bewijsquotes;
     - hiaten voor volgend niveau;
     - concrete acties.

6. **Validatie laag**
   - Controle op verplichte velden, lengte, structuur.
   - Hallucinatiecheck: bewijsquotes moeten in documenttekst voorkomen.

7. **Opslag & presentatie**
   - Resultaat per skill opslaan.
   - UI toont transparant beoordelingspad.

## 7. MVP-omschrijving
### In scope
- Upload document als platte tekst.
- Kiezen van bestaand framework.
- Analyse per skill met:
  - huidig niveau;
  - onderbouwing;
  - bewijs;
  - hiaten;
  - acties.
- Resultaten opslaan en later terugkijken.
- Simpele beheerpagina om frameworks aan te maken/aan te passen.

### Out of scope (fase 2)
- Teambeheer en rechtenmodel.
- Geavanceerde vergelijkingsrapportages.
- Volledige human-in-the-loop reviewflow.
- Multi-tenant enterprise configuratie.

## 8. Eerste codebasis (in deze repository)
De eerste codebasis bevat:
- een FastAPI backend met endpoints voor:
  - frameworks beheren;
  - documenten uploaden;
  - analyse starten;
  - resultaten ophalen.
- een React frontend met pagina’s voor:
  - upload en analyse;
  - resultaatoverzicht;
  - frameworkbeheer.
- een modulaire analyse-service die skill-per-skill werkt en de vereiste outputstructuur afdwingt.

