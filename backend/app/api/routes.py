from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlmodel import Session, select

from app.core.database import get_session
from app.models import AssessmentResult, Document, Framework, Skill, SkillAssessment, SkillLevel
from app.schemas import AnalyzeRequest, AssessmentRead, FrameworkCreate, FrameworkRead, Message, SkillAssessmentRead
from app.services.analyzer import analyze_document
from app.services.constraints import load_level_constraints
from app.services.framework_seed import seed_professor_framework
from app.utils.document_parser import extract_document_content

router = APIRouter()


@router.get('/health')
def health() -> dict[str, str]:
    return {'status': 'ok'}


@router.post('/frameworks', response_model=Message)
def create_framework(payload: FrameworkCreate, session: Session = Depends(get_session)):
    framework = Framework(name=payload.name, version=payload.version, description=payload.description)
    session.add(framework)
    session.commit()
    session.refresh(framework)

    for skill_payload in payload.skills:
        skill = Skill(framework_id=framework.id, name=skill_payload.name, description=skill_payload.description)
        session.add(skill)
        session.commit()
        session.refresh(skill)

        for level_payload in skill_payload.levels:
            level = SkillLevel(
                skill_id=skill.id,
                level_index=level_payload.level_index,
                title=level_payload.title,
                descriptor=level_payload.descriptor,
            )
            session.add(level)

    session.commit()
    return Message(message='Framework aangemaakt', id=framework.id)


@router.get('/frameworks', response_model=list[FrameworkRead])
def list_frameworks(session: Session = Depends(get_session)):
    frameworks = session.exec(select(Framework)).all()
    return frameworks


@router.post('/frameworks/seed/professor', response_model=Message)
def seed_framework(session: Session = Depends(get_session)):
    framework = seed_professor_framework(session)
    return Message(message='Professor niveaukader beschikbaar', id=framework.id)


@router.post('/documents', response_model=Message)
async def upload_document(file: UploadFile = File(...), session: Session = Depends(get_session)):
    payload = await file.read()
    content = extract_document_content(file.filename or 'document.txt', payload)
    document = Document(filename=file.filename, content=content)
    session.add(document)
    session.commit()
    session.refresh(document)
    return Message(message='Document geüpload', id=document.id)


@router.post('/assessments/analyze', response_model=Message)
def run_analysis(payload: AnalyzeRequest, session: Session = Depends(get_session)):
    try:
        assessment = analyze_document(session, payload.document_id, payload.framework_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return Message(message='Analyse voltooid', id=assessment.id)


@router.get('/assessments/{assessment_id}', response_model=AssessmentRead)
def get_assessment(assessment_id: int, session: Session = Depends(get_session)):
    assessment = session.get(AssessmentResult, assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail='Assessment niet gevonden')

    skill_rows = session.exec(select(SkillAssessment).where(SkillAssessment.assessment_id == assessment_id)).all()

    skills = []
    for row in skill_rows:
        skill = session.get(Skill, row.skill_id)
        skills.append(
            SkillAssessmentRead(
                skill_name=skill.name if skill else 'Onbekend',
                current_level=row.current_level,
                rationale=row.rationale,
                evidence=row.evidence,
                gaps=row.gaps,
                next_level_guidance=row.next_level_guidance,
                improvement_actions=row.improvement_actions,
            )
        )

    return AssessmentRead(
        id=assessment.id,
        document_id=assessment.document_id,
        framework_id=assessment.framework_id,
        model_name=assessment.model_name,
        skills=skills,
    )


@router.get('/constraints/levels')
def get_level_constraints() -> dict:
    return load_level_constraints()
