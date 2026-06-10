import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import type { PerfilCompleto } from '../types'
import { compararCandidatos } from '../api'

function fmtMoeda(v: number): string { if (v >= 1_000_000) return `R$ ${(v / 1_000_000).toFixed(1)}M`; if (v >= 1_000) return `R$ ${(v / 1_000).toFixed(0)}K`; return `R$ ${v}` }

const statusLabels: Record<string, string> = { em_andamento: 'Em andamento', transitada_em_julgado: 'Trânsito em julgado', arquivado: 'Arquivado', absolvido: 'Absolvido' }

export default function Comparacao() {
  const { ids } = useParams<{ ids: string }>()
  const [perfis, setPerfis] = useState<PerfilCompleto[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => { if (!ids) return; setLoading(true); compararCandidatos(ids.split(',').map(Number)).then(setPerfis).finally(() => setLoading(false)) }, [ids])

  if (loading) return <div className="flex justify-center py-16"><div className="animate-spin rounded-full h-8 w-8 border-[3px] border-brand-200 border-t-brand-600" /></div>
  if (perfis.length < 2) return <div className="text-center py-16 text-surface-500">Selecione pelo menos 2 candidatos para comparar.</div>

  const rows = [
    { label: 'Intenção de voto', render: (p: PerfilCompleto) => p.candidato.intencao_voto != null ? <span className="text-xl font-bold text-brand-700 tabular-nums">{p.candidato.intencao_voto}%</span> : <span className="text-surface-400">—</span> },
    { label: 'Processos judiciais', render: (p: PerfilCompleto) => (<div><span className="font-bold text-surface-800">{p.candidato.indicadores.processos_totais}</span>{p.candidato.indicadores.processos_condenacao_transitada > 0 && <span className="text-red-600 text-xs ml-1">({p.candidato.indicadores.processos_condenacao_transitada} transitada)</span>}{p.secoes.processos.slice(0, 2).map((proc, i) => <p key={i} className="text-[11px] text-surface-500 mt-0.5">• {proc.tipo} — {statusLabels[proc.status] || proc.status}</p>)}</div>) },
    { label: 'Matérias (12m)', render: (p: PerfilCompleto) => <span className="font-bold text-surface-800">{p.candidato.indicadores.materias_12m}</span> },
    { label: 'Doações investigadas', render: (p: PerfilCompleto) => <span className={`font-bold ${p.candidato.indicadores.doacoes_empresas_investigadas > 0 ? 'text-amber-600' : 'text-surface-800'}`}>{p.candidato.indicadores.doacoes_empresas_investigadas}</span> },
    { label: 'Patrimônio declarado', render: (p: PerfilCompleto) => <span className="font-bold text-surface-800 tabular-nums">{fmtMoeda(p.candidato.indicadores.patrimonio_declarado)}</span> },
    { label: 'Presença legislativa', render: (p: PerfilCompleto) => p.candidato.indicadores.presenca_legislativa_percent != null ? <span className={`font-bold tabular-nums ${p.candidato.indicadores.presenca_legislativa_percent < 70 ? 'text-red-600' : 'text-emerald-600'}`}>{p.candidato.indicadores.presenca_legislativa_percent}%</span> : <span className="text-surface-400">—</span> },
    { label: 'Gastos de campanha', render: (p: PerfilCompleto) => p.secoes.gastos_campanha ? <span className="font-bold text-surface-800 tabular-nums">{fmtMoeda(p.secoes.gastos_campanha.total_declarado)}</span> : <span className="text-surface-400">—</span> },
    { label: 'Bens declarados', render: (p: PerfilCompleto) => p.secoes.bens_declarados.length > 0 ? <span className="font-bold text-surface-800">{p.secoes.bens_declarados.length} itens</span> : <span className="text-surface-400">—</span> },
  ]

  return (
    <div className="space-y-6">
      <Link to="/" className="text-sm font-medium text-brand-600 hover:text-brand-700 inline-flex items-center gap-1">← Voltar ao ranking</Link>
      <div>
        <h1 className="text-2xl font-bold text-surface-800">Comparação lado a lado</h1>
        <p className="text-surface-500 text-sm mt-1">Dados públicos de {perfis.length} candidatos — sem scores ou julgamentos.</p>
      </div>

      <div className="bg-white rounded-xl shadow-card border border-surface-200 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-surface-100">
                <th className="text-left p-5 font-semibold text-surface-500 text-xs uppercase tracking-wider w-48">Indicador</th>
                {perfis.map(p => (
                  <th key={p.candidato.nome} className="p-5 text-left min-w-[200px]">
                    <Link to={`/candidato/${perfis.indexOf(p) + 1}`} className="text-surface-800 font-semibold hover:text-brand-600">{p.candidato.nome}</Link>
                    <p className="text-xs text-surface-400 font-normal mt-0.5">{p.candidato.partido} — {p.candidato.cargo}</p>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rows.map((row, idx) => (
                <tr key={idx} className="border-b border-surface-50 hover:bg-surface-50/50 transition-colors">
                  <td className="p-5 text-surface-500 font-medium text-xs uppercase tracking-wide">{row.label}</td>
                  {perfis.map(p => <td key={p.candidato.nome} className="p-5 align-top">{row.render(p)}</td>)}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <p className="text-center text-xs text-surface-400">Dados de fontes oficiais (TSE, DataJud, Câmara, Senado, Portal da Transparência). Sem scores ou julgamentos.</p>
    </div>
  )
}
