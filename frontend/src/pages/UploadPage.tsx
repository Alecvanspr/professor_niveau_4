import { useEffect, useState } from 'react'

import { analyzeDocument, getFrameworks, uploadDocument } from '../services/api'
import type { Framework } from '../types'

export function UploadPage() {
  const [file, setFile] = useState<File | null>(null)
  const [frameworks, setFrameworks] = useState<Framework[]>([])
  const [frameworkId, setFrameworkId] = useState<number | null>(null)
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')

  useEffect(() => {
    getFrameworks().then((items) => {
      setFrameworks(items)
      if (items.length > 0) {
        setFrameworkId(items[0].id)
      }
    })
  }, [])

  async function handleAnalyze() {
    if (!file || !frameworkId) {
      setMessage('Selecteer een document en framework.')
      return
    }

    setLoading(true)
    setMessage('Document wordt geanalyseerd...')

    try {
      const documentId = await uploadDocument(file)
      const assessmentId = await analyzeDocument(documentId, frameworkId)
      setMessage(`Analyse afgerond. Open resultaat via /results/${assessmentId}`)
    } catch (error) {
      setMessage(error instanceof Error ? error.message : 'Onbekende fout')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <h2>Upload en Analyse</h2>
      <div className="card">
        <input type="file" accept=".txt,.md,.pdf,.zip" onChange={(event) => setFile(event.target.files?.[0] ?? null)} />
        <select value={frameworkId ?? ''} onChange={(event) => setFrameworkId(Number(event.target.value))}>
          {frameworks.map((framework) => (
            <option key={framework.id} value={framework.id}>
              {framework.name} v{framework.version}
            </option>
          ))}
        </select>
        <button onClick={handleAnalyze} disabled={loading}>
          {loading ? 'Bezig...' : 'Start beoordeling'}
        </button>
      </div>
      {message && <p>{message}</p>}
    </div>
  )
}
