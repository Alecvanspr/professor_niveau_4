import json
from pathlib import Path

from sqlmodel import Session, select

from app.models import Framework, Skill, SkillLevel


def seed_professor_framework(session: Session) -> Framework:
    config_path = Path(__file__).resolve().parent.parent / 'config' / 'niveaukader_professor.json'
    payload = json.loads(config_path.read_text(encoding='utf-8'))

    existing = session.exec(
        select(Framework).where(
            Framework.name == payload['name'],
            Framework.version == payload['version'],
        )
    ).first()
    if existing:
        return existing

    framework = Framework(
        name=payload['name'],
        version=payload['version'],
        description=payload['description'],
    )
    session.add(framework)
    session.commit()
    session.refresh(framework)

    for skill_payload in payload['skills']:
        skill = Skill(
            framework_id=framework.id,
            name=skill_payload['name'],
            description=skill_payload['description'],
        )
        session.add(skill)
        session.commit()
        session.refresh(skill)

        for level_payload in skill_payload['levels']:
            session.add(
                SkillLevel(
                    skill_id=skill.id,
                    level_index=level_payload['level_index'],
                    title=level_payload['title'],
                    descriptor=level_payload['descriptor'],
                )
            )

    session.commit()
    return framework
