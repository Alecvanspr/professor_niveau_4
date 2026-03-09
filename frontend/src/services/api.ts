import type { Assessment, Framework } from '../types'

const API_BASE = 'http://localhost:8000/api'

export async function getFrameworks(): Promise<Framework[]> {
  const response = await fetch(`${API_BASE}/frameworks`)
  if (!response.ok) {
    throw new Error('Kon frameworks niet ophalen')
  }
  return response.json()
}

export async function uploadDocument(file: File): Promise<number> {
  const formData = new FormData()
  formData.append('file', file)

  const response = await fetch(`${API_BASE}/documents`, {
    method: 'POST',
    body: formData,
  })

  const payload = await response.json()
  if (!response.ok) {
    throw new Error(payload.detail ?? 'Upload mislukt')
  }
  return payload.id
}

export async function analyzeDocument(documentId: number, frameworkId: number): Promise<number> {
  const response = await fetch(`${API_BASE}/assessments/analyze`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ document_id: documentId, framework_id: frameworkId }),
  })

  const payload = await response.json()
  if (!response.ok) {
    throw new Error(payload.detail ?? 'Analyse mislukt')
  }
  return payload.id
}

export async function getAssessment(assessmentId: number): Promise<Assessment> {
  const response = await fetch(`${API_BASE}/assessments/${assessmentId}`)
  if (!response.ok) {
    throw new Error('Kon assessment niet ophalen')
  }
  return response.json()
}
