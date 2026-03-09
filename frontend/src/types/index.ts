export type Framework = {
  id: number
  name: string
  version: string
  description: string
}

export type SkillAssessment = {
  skill_name: string
  current_level: number
  rationale: string
  evidence: string
  gaps: string
  next_level_guidance: string
  improvement_actions: string
}

export type Assessment = {
  id: number
  document_id: number
  framework_id: number
  model_name: string
  skills: SkillAssessment[]
}
