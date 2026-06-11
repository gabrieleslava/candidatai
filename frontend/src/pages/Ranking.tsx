import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import type { Candidato } from '../types'
import { listarCandidatos, opcoesFiltros } from '../api'

const cargoIcon: Record<string, string> = {
  'Presidência': '🏛️', 'Governador': '🏢', 'Senador': '📜', 'Deputado Federal': '🗳️',
}

function fmtMoeda(valor: number): string {
  if (valor >= 1_000_000) return `R$ ${(valor / 1_000_000).toFixed(1)}M`
  if (valor >= 1_000) return `R$ ${(valor / 1_000).toFixed(0)}K`
  return `R$ ${valor}`
}

export default function Ranking() {
  const [candidatos, setCandidatos] = useState<Candidato[]>([])
  const [cargos, setCargos] = useState<string[]>([])
  const [estados, setEstados] = useState<string[]>([])
  const [loading, setLoading] = useState(true)

  const [cargo, setCargo] = useState('')
  const [estado, setEstado] = useState('')
  const [busca, setBusca] = useState('')
  const [temProcessos, setTemProcessos] = useState(false)
  const [temCondenacao, setTemCondenacao] = useState(false)
  const [temDoacaoInv, setTemDoacaoInv] = useState(false)
  const [baixaPresenca, setBaixaPresenca] = useState(false)

  const [selecionados, setSelecionados] = useState<number[]>([])

  const [erro, setErro] = useState('')

  const carregar = (overrides?: Record<string, string | boolean>) => {
    setLoading(true)
    setErro('')
    listarCandidatos({
      cargo: (cargo || overrides?.cargo) as string | undefined,
      estado: (estado || overrides?.estado) as string | undefined,
      busca: (busca || overrides?.busca) as string | undefined,
      tem_processos: (temProcessos || overrides?.tem_processos) as boolean | undefined,
      tem_condenacao: (temCondenacao || overrides?.tem_condenacao) as boolean | undefined,
      tem_doacao_investigada: (temDoacaoInv || overrides?.tem_doacao_investigada) as boolean | undefined,
      baixa_presenca: (baixaPresenca || overrides?.baixa_presenca) as boolean | undefined,
    }).then(setCandidatos).catch(e => setErro(e.message)).finally(() => setLoading(false))
  }

  useEffect(() => {
    opcoesFiltros().then(opts => { setCargos(opts.cargos); setEstados(opts.estados) }).catch(() => {});
    carregar()
  }, [])

  const toggleSelecionado = (id: number) => {
    setSelecionados(prev => prev.includes(id) ? prev.filter(x => x !== id) : prev.length < 4 ? [...prev, id] : prev)
  }

  const filtros = [
    { label: 'Tem processos', value: temProcessos, set: setTemProcessos, key: 'tem_processos' },
    { label: 'Condenação transitada', value: temCondenacao, set: setTemCondenacao, key: 'tem_condenacao' },
    { label: 'Doação investigada', value: temDoacaoInv, set: setTemDoacaoInv, key: 'tem_doacao_investigada' },
    { label: 'Presença < 70%', value: baixaPresenca, set: setBaixaPresenca, key: 'baixa_presenca' },
  ]

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-surface-800">Painel de Transparência</h1>
        <p className="text-surface-500 mt-1">Dados públicos de fontes oficiais — sem notas, scores ou julgamentos.</p>
      </div>

      {/* Filtros */}
      <div className="bg-white rounded-xl p-5 shadow-card border border-surface-200">
        <div className="flex flex-wrap gap-3 mb-3">
          <select value={cargo} onChange={e => { setCargo(e.target.value); carregar({ cargo: e.target.value }) }}
            className="px-4 py-2.5 rounded-lg border border-surface-200 text-sm bg-surface-50 text-surface-700 focus:ring-2 focus:ring-brand-500 focus:outline-none">
            <option value="">Todos os cargos</option>
            {cargos.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
          <select value={estado} onChange={e => { setEstado(e.target.value); carregar({ estado: e.target.value }) }}
            className="px-4 py-2.5 rounded-lg border border-surface-200 text-sm bg-surface-50 text-surface-700 focus:ring-2 focus:ring-brand-500 focus:outline-none">
            <option value="">Todos os estados</option>
            {estados.map(e => <option key={e} value={e}>{e}</option>)}
          </select>
          <input type="text" placeholder="Buscar por nome ou partido..." value={busca} onChange={e => setBusca(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && carregar()}
            className="px-4 py-2.5 rounded-lg border border-surface-200 text-sm bg-surface-50 flex-1 min-w-[200px] focus:ring-2 focus:ring-brand-500 focus:outline-none" />
        </div>
        <div className="flex flex-wrap gap-2">
          {filtros.map(f => (
            <button key={f.label} onClick={() => { f.set(!f.value); carregar({ [f.key]: !f.value }) }}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                f.value ? 'bg-brand-600 text-white' : 'bg-surface-100 text-surface-600 hover:bg-surface-200'}`}>
              {f.label}
            </button>
          ))}
        </div>
      </div>

      {/* Comparação */}
      {selecionados.length >= 2 && (
        <div className="bg-brand-50 rounded-xl p-4 border border-brand-200 flex items-center justify-between">
          <span className="text-sm font-semibold text-brand-700">{selecionados.length} candidato{selecionados.length > 1 ? 's' : ''} selecionado{selecionados.length > 1 ? 's' : ''}</span>
          <div className="flex items-center gap-3">
            <button onClick={() => setSelecionados([])} className="text-sm text-surface-500 hover:text-surface-700">Limpar</button>
            <Link to={`/comparar/${selecionados.join(',')}`} className="px-5 py-2.5 bg-brand-600 text-white rounded-lg text-sm font-semibold hover:bg-brand-700 transition-colors no-underline">
              Comparar lado a lado
            </Link>
          </div>
        </div>
      )}

      {loading && <div className="flex justify-center py-16"><div className="animate-spin rounded-full h-8 w-8 border-[3px] border-brand-200 border-t-brand-600" /></div>}

      {erro && !loading && (
        <div className="bg-red-50 border border-red-200 rounded-xl p-6 text-center">
          <p className="text-red-700 font-semibold">Erro ao carregar dados</p>
          <p className="text-red-500 text-sm mt-1">{erro}</p>
          <button onClick={() => carregar()} className="mt-3 px-4 py-2 bg-red-600 text-white rounded-lg text-sm">Tentar novamente</button>
        </div>
      )}

      {!loading && !erro && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {candidatos.map((c, idx) => (
            <div key={c.id} onClick={() => toggleSelecionado(c.id)}
              className={`bg-white rounded-xl p-5 shadow-card border cursor-pointer transition-shadow hover:shadow-elevated ${
                selecionados.includes(c.id) ? 'ring-2 ring-brand-400 border-brand-300' : 'border-surface-200'}`}>
              <div className="flex items-start gap-3 mb-3">
                <div className="w-10 h-10 rounded-xl bg-brand-100 flex items-center justify-center text-lg flex-shrink-0">{cargoIcon[c.cargo] || '👤'}</div>
                <div className="min-w-0 flex-1">
                  <div className="flex items-center gap-1.5 flex-wrap">
                    <Link to={`/candidato/${c.id}`} onClick={e => e.stopPropagation()} className="font-semibold text-surface-800 text-sm hover:text-brand-600 transition-colors">{c.nome}</Link>
                    <span className="px-2 py-0.5 rounded-md bg-surface-100 text-surface-600 text-xs font-medium">{c.partido}</span>
                  </div>
                  <p className="text-xs text-surface-400 mt-0.5">{c.cargo} — {c.estado}</p>
                </div>
              </div>

              <div className="mb-3">
                {c.intencao_voto != null ? (
                  <div className="flex items-baseline gap-1">
                    <span className="text-2xl font-bold text-brand-700 tabular-nums">{c.intencao_voto}%</span>
                    <span className="text-xs text-surface-400">intenção de voto</span>
                  </div>
                ) : <span className="text-xs text-surface-400 italic">Sem dados de intenção</span>}
                {c.pesquisa_fonte && <p className="text-[11px] text-surface-400 mt-0.5">{c.pesquisa_fonte}</p>}
              </div>

              <div className="flex flex-wrap gap-1.5">
                {c.indicadores.processos_totais > 0 && (
                  <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-red-50 text-red-600 text-xs font-medium">
                    ⚖️ {c.indicadores.processos_totais}{c.indicadores.processos_condenacao_transitada > 0 ? ` (${c.indicadores.processos_condenacao_transitada} transitada)` : ''}
                  </span>
                )}
                {c.indicadores.materias_12m > 0 && <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-blue-50 text-blue-600 text-xs font-medium">📰 {c.indicadores.materias_12m}</span>}
                {c.indicadores.doacoes_empresas_investigadas > 0 && <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-amber-50 text-amber-600 text-xs font-medium">💰 {c.indicadores.doacoes_empresas_investigadas}</span>}
                <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-emerald-50 text-emerald-600 text-xs font-medium">💼 {fmtMoeda(c.indicadores.patrimonio_declarado)}</span>
                {c.indicadores.presenca_legislativa_percent != null && (
                  <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-xs font-medium ${c.indicadores.presenca_legislativa_percent < 70 ? 'bg-red-50 text-red-600' : 'bg-emerald-50 text-emerald-600'}`}>
                    🏛️ {c.indicadores.presenca_legislativa_percent}%
                  </span>
                )}
              </div>

              <div className="mt-3 pt-3 border-t border-surface-100 flex justify-between items-center">
                <span className="text-xs text-surface-400">#{idx + 1} no ranking</span>
                <Link to={`/candidato/${c.id}`} onClick={e => e.stopPropagation()} className="text-xs font-semibold text-brand-600 hover:text-brand-700">Ver perfil completo →</Link>
              </div>
            </div>
          ))}
          {candidatos.length === 0 && <div className="col-span-full text-center py-16 text-surface-400">Nenhum candidato encontrado.</div>}
        </div>
      )}
    </div>
  )
}
