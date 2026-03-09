import { Link, Route, Routes } from 'react-router-dom'

import { AdminFrameworkPage } from './pages/AdminFrameworkPage'
import { ResultPage } from './pages/ResultPage'
import { UploadPage } from './pages/UploadPage'

export function App() {
  return (
    <div className="container">
      <h1>AI Beoordelingsplatform</h1>
      <nav>
        <Link to="/">Upload</Link>
        <Link to="/admin/frameworks">Framework beheer</Link>
      </nav>
      <Routes>
        <Route path="/" element={<UploadPage />} />
        <Route path="/admin/frameworks" element={<AdminFrameworkPage />} />
        <Route path="/results/:id" element={<ResultPage />} />
      </Routes>
    </div>
  )
}
