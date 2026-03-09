from collections import defaultdict

from sqlmodel import Session, select

from app.models import AssessmentResult, Document, Framework, Skill, SkillAssessment, SkillLevel
from app.services.constraints import get_level_constraints


def _tokenize(text: str) -> set[str]:
    return {token.strip('.,;:!?()[]"\'').lower() for token in text.split() if token.strip()}


def _find_evidence_sentences(content: str, descriptor: str, max_hits: int = 2) -> list[str]:
    descriptor_tokens = _tokenize(descriptor)
    hits = []
    for sentence in content.split("."):
        sentence_tokens = _tokenize(sentence)
        overlap = len(descriptor_tokens.intersection(sentence_tokens))
        if overlap > 0:
            hits.append((overlap, sentence.strip()))
    hits.sort(key=lambda item: item[0], reverse=True)
    return [h[1] for h in hits[:max_hits] if h[1]]


def analyze_document(session: Session, document_id: int, framework_id: int) -> AssessmentResult:
    document = session.get(Document, document_id)
    framework = session.get(Framework, framework_id)
    if not document or not framework:
        raise ValueError("Document of framework niet gevonden.")

    assessment = AssessmentResult(document_id=document_id, framework_id=framework_id)
    session.add(assessment)
    session.commit()
    session.refresh(assessment)

    skills = session.exec(select(Skill).where(Skill.framework_id == framework_id)).all()
    levels_by_skill = defaultdict(list)
    for level in session.exec(select(SkillLevel)).all():
        levels_by_skill[level.skill_id].append(level)

    content_tokens = _tokenize(document.content)

    for skill in skills:
        levels = sorted(levels_by_skill[skill.id], key=lambda lvl: lvl.level_index)
        if not levels:
            continue

        best_level = levels[0]
        best_score = -1

        for level in levels:
            descriptor_tokens = _tokenize(level.descriptor)
            score = len(descriptor_tokens.intersection(content_tokens))
            if score > best_score:
                best_score = score
                best_level = level

        evidence_sentences = _find_evidence_sentences(document.content, best_level.descriptor)
        evidence = "\n".join(f"- {sentence}." for sentence in evidence_sentences) or "- Geen sterk direct bewijs gevonden in de tekst."

        next_level = next((lvl for lvl in levels if lvl.level_index == best_level.level_index + 1), None)
        gaps = (
            f"Om niveau {best_level.level_index + 1} te bereiken ontbreekt expliciete dekking van: {next_level.descriptor}"
            if next_level
            else "Er is geen hoger niveau gedefinieerd voor deze vaardigheid."
        )
        next_guidance = (
            f"Focus op het aantoonbaar toevoegen van elementen uit niveau {next_level.level_index}: {next_level.title}."
            if next_level
            else "Borg het huidige niveau en verbreed bewijs in nieuwe contexten."
        )

        constraints = get_level_constraints(best_level.level_index, framework.name)
        must_have = ', '.join(constraints['must_have']) or 'geen extra vereisten geconfigureerd'
        must_not_have = ', '.join(constraints['must_not_have']) or 'geen uitsluitende criteria geconfigureerd'

        actions = (
            "1) Voeg een expliciet praktijkvoorbeeld toe.\n"
            "2) Onderbouw keuzes met criteria en resultaten.\n"
            "3) Gebruik meetbare indicatoren om niveauprogressie aan te tonen.\n"
            f"4) Check levelrestricties (must-have): {must_have}."
        )

        rationale = (
            f"Niveau {best_level.level_index} ({best_level.title}) past het best bij de tekst op basis van overlap met rubric-indicatoren. "
            f"De beoordeling is vaardigheid-specifiek en gebruikt zowel descriptor-match als tekstsignalen. "
            f"Restricties voor dit niveau (must-have): {must_have}; (must-not-have): {must_not_have}."
        )

        skill_assessment = SkillAssessment(
            assessment_id=assessment.id,
            skill_id=skill.id,
            current_level=best_level.level_index,
            rationale=rationale,
            evidence=evidence,
            gaps=gaps,
            next_level_guidance=next_guidance,
            improvement_actions=actions,
        )
        session.add(skill_assessment)

    session.commit()
    session.refresh(assessment)
    return assessment
