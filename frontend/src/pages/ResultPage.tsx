import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'

import { getAssessment } from '../services/api'
import type { Assessment } from '../types'

export function ResultPage() {
  const { id } = useParams()
  const [assessment, setAssessment] = useState<Assessment | null>(null)
  const [error, setError] = useState('')

  useEffect(() => {
    if (!id) {
      return
    }

    getAssessment(Number(id))
      .then(setAssessment)
      .catch((reason: Error) => setError(reason.message))
  }, [id])

  if (error) {
    return <p>{error}</p>
  }

  if (!assessment) {
    return <p>Resultaat wordt geladen...</p>
  }

  return (
    <div>
      <h2>Analyse #{assessment.id}</h2>
      {assessment.skills.map((skill) => (
        <article key={skill.skill_name} className="card">
          <h3>{skill.skill_name}</h3>
          <p>
            <strong>Huidig niveau:</strong> {skill.current_level}
          </p>
          <p>
            <strong>Onderbouwing:</strong> {skill.rationale}
          </p>
          <p>
            <strong>Bewijs:</strong>
            <br />
            <pre>{skill.evidence}</pre>
          </p>
          <p>
            <strong>Hiaten:</strong> {skill.gaps}
          </p>
          <p>
            <strong>Volgend niveau:</strong> {skill.next_level_guidance}
          </p>
          <p>
            <strong>Verbeterstappen:</strong>
            <br />
            <pre>{skill.improvement_actions}</pre>
          </p>
        </article>
      ))}
    </div>
  )
}
