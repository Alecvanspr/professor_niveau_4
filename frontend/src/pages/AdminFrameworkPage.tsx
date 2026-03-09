import { useState } from 'react'

const API_BASE = 'http://localhost:8000/api'

const starterPayload = {
  name: 'Schrijfvaardigheid',
  version: '1.0',
  description: 'Generiek schrijfkader',
  skills: [
    {
      name: 'Structuur',
      description: 'Opbouw en logische lijn',
      levels: [
        { level_index: 1, title: 'Basis', descriptor: 'tekst bevat losse punten zonder duidelijke lijn' },
        { level_index: 2, title: 'Voldoende', descriptor: 'tekst heeft inleiding kern en afsluiting' },
        { level_index: 3, title: 'Sterk', descriptor: 'tekst heeft consistente argumentatielijn met heldere overgangen' }
      ]
    }
  ]
}

export function AdminFrameworkPage() {
  const [message, setMessage] = useState('')

  async function createStarterFramework() {
    const response = await fetch(`${API_BASE}/frameworks`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(starterPayload),
    })

    const payload = await response.json()
    if (!response.ok) {
      setMessage(payload.detail ?? 'Aanmaken mislukt')
      return
    }
    setMessage(`Framework aangemaakt met id ${payload.id}`)
  }

  return (
    <div>
      <h2>Framework beheer</h2>
      <p>Maak een startkader aan om direct te kunnen testen met analyses.</p>
      <button onClick={createStarterFramework}>Maak starter framework</button>
      {message && <p>{message}</p>}
    </div>
  )
}
