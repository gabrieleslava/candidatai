import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { useEffect, useState } from 'react'
import Ranking from './pages/Ranking'
import Perfil from './pages/Perfil'
import Comparacao from './pages/Comparacao'

function StatusBadge() {
  const [status, setStatus] = useState<Record<string, string>>({})

  useEffect(() => {
    fetch('/api/status')
      .then(r => r.json())
      .then(d => setStatus(d.integracoes || {}))
      .catch(() => {})
  }, [])

  const labels: Record<string, string> = {
    camara: 'Câmara', portal_transparencia: 'Transparência', tse: 'TSE', datajud: 'DataJud', gnews: 'GNews',
  }

  if (!Object.keys(status).length) return null

  return (
    <div className="max-w-6xl mx-auto px-6 pt-3 flex flex-wrap gap-2">
      {Object.entries(status).map(([key, val]) => (
        <span key={key} className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[11px] font-medium ${
          val === 'ok' ? 'bg-emerald-50 text-emerald-600' : 'bg-surface-100 text-surface-400'
        }`}>
          <span className={`w-1.5 h-1.5 rounded-full ${val === 'ok' ? 'bg-emerald-500' : 'bg-surface-300'}`} />
          {labels[key] || key}
        </span>
      ))}
    </div>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-surface-50">
        <header className="bg-gradient-to-r from-brand-600 to-brand-800 text-white sticky top-0 z-10 shadow-elevated">
          <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
            <a href="/" className="flex items-center gap-3 no-underline">
              <div className="w-10 h-10 bg-white/20 backdrop-blur rounded-xl flex items-center justify-center">
                <span className="text-white font-bold text-base">CA</span>
              </div>
              <div>
                <h1 className="text-xl font-bold text-white tracking-tight">CandidatAI</h1>
                <p className="text-xs text-brand-100 opacity-80">Painel de Transparência Eleitoral 2026</p>
              </div>
            </a>
          </div>
        </header>

        <StatusBadge />

        <main className="max-w-6xl mx-auto px-6 py-8">
          <Routes>
            <Route path="/" element={<Ranking />} />
            <Route path="/candidato/:id" element={<Perfil />} />
            <Route path="/comparar/:ids" element={<Comparacao />} />
          </Routes>
        </main>

        <footer className="border-t border-surface-200 py-6 mt-16">
          <div className="max-w-6xl mx-auto px-6 text-center text-xs text-surface-400">
            CandidatAI — Dados de fontes oficiais públicas (TSE, DataJud, Câmara, Senado, Portal da Transparência).
            O sistema não atribui scores, notas ou julgamentos.
          </div>
        </footer>
      </div>
    </BrowserRouter>
  )
}
