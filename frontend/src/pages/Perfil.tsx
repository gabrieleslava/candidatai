import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import type { PerfilCompleto } from '../types'
import { perfilCandidato } from '../api'

const statusLabels: Record<string, string> = {
  em_andamento: 'Em andamento', transitada_em_julgado: 'Trânsito em julgado', arquivado: 'Arquivado', absolvido: 'Absolvido',
}

const instanciaInfo: Record<string, string> = {
  'TJ-SP': 'Tribunal de Justiça — 2ª instância estadual', 'TJ-RJ': 'Tribunal de Justiça — 2ª instância estadual',
  'TJ-MG': 'Tribunal de Justiça — 2ª instância estadual', 'TJ-DF': 'Tribunal de Justiça — 2ª instância estadual',
  'TRF-2': 'Tribunal Regional Federal — 2ª instância', 'TRF-3': 'Tribunal Regional Federal — 2ª instância',
  'TRF-4': 'Tribunal Regional Federal — 2ª instância',
  'STJ': 'Superior Tribunal de Justiça — 3ª instância', 'STF': 'Supremo Tribunal Federal — instância máxima',
  'TSE': 'Tribunal Superior Eleitoral', 'TRE-SP': 'Tribunal Regional Eleitoral de SP', 'TRE-RJ': 'Tribunal Regional Eleitoral do RJ',
}

function fmtMoeda(v: number): string { if (v >= 1_000_000) return `R$ ${(v / 1_000_000).toFixed(1)}M`; if (v >= 1_000) return `R$ ${(v / 1_000).toFixed(0)}K`; return `R$ ${v}` }

export default function Perfil() {
  const { id } = useParams<{ id: string }>()
  const [perfil, setPerfil] = useState<PerfilCompleto | null>(null)
  const [aba, setAba] = useState('processos')
  const [loading, setLoading] = useState(true)

  useEffect(() => { if (!id) return; setLoading(true); perfilCandidato(parseInt(id)).then(setPerfil).finally(() => setLoading(false)) }, [id])

  if (loading) return <div className="flex justify-center py-16"><div className="animate-spin rounded-full h-8 w-8 border-[3px] border-brand-200 border-t-brand-600" /></div>
  if (!perfil) return <div className="text-center py-16 text-surface-500">Candidato não encontrado.</div>

  const { candidato: c, secoes } = perfil

  const abas = [
    { key: 'processos', label: '⚖️ Processos', count: secoes.processos.length },
    { key: 'materias', label: '📰 Matérias', count: secoes.materias.length },
    { key: 'gastos', label: '💰 Gastos', count: secoes.gastos_campanha ? 1 : 0 },
    { key: 'bens', label: '🏠 Bens', count: secoes.bens_declarados.length },
    { key: 'legislativo', label: '🏛️ Legislativo', count: secoes.historico_legislativo ? 1 : 0 },
    { key: 'contratos', label: '📋 Contratos', count: secoes.contratos_governo.length },
  ]

  return (
    <div className="space-y-6">
      <Link to="/" className="text-sm font-medium text-brand-600 hover:text-brand-700 inline-flex items-center gap-1">← Voltar ao ranking</Link>

      {/* Cabeçalho */}
      <div className="bg-white rounded-xl p-6 shadow-card border border-surface-200">
        <div className="flex items-start gap-5">
          <div className="w-16 h-16 rounded-2xl bg-brand-600 flex items-center justify-center text-2xl font-bold text-white flex-shrink-0 shadow-elevated">{c.nome.charAt(0)}</div>
          <div className="flex-1 min-w-0">
            <h1 className="text-2xl font-bold text-surface-800">{c.nome}</h1>
            <div className="flex items-center gap-2 mt-1.5 flex-wrap">
              <span className="px-2.5 py-1 rounded-md bg-brand-50 text-brand-700 text-sm font-semibold">{c.partido}</span>
              <span className="text-sm text-surface-500">{c.cargo} — {c.estado}</span>
              {c.numero && <span className="text-sm text-surface-400">Nº {c.numero}</span>}
            </div>
            {c.intencao_voto != null && (
              <div className="mt-3 flex items-baseline gap-2">
                <span className="text-3xl font-bold text-brand-700 tabular-nums">{c.intencao_voto}%</span>
                <span className="text-sm text-surface-400">{c.pesquisa_fonte}</span>
              </div>
            )}
          </div>
        </div>

        <div className="flex flex-wrap gap-2 mt-4 pt-4 border-t border-surface-100">
          <span className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-md text-xs font-medium ${c.indicadores.processos_totais > 0 ? 'bg-red-50 text-red-600' : 'bg-emerald-50 text-emerald-600'}`}>⚖️ {c.indicadores.processos_totais} processos</span>
          <span className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-md text-xs font-medium ${c.indicadores.processos_condenacao_transitada > 0 ? 'bg-red-50 text-red-600' : 'bg-emerald-50 text-emerald-600'}`}>⚠️ {c.indicadores.processos_condenacao_transitada} condenação transitada</span>
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-md bg-blue-50 text-blue-600 text-xs font-medium">📰 {c.indicadores.materias_12m} matérias (12m)</span>
          <span className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-md text-xs font-medium ${c.indicadores.doacoes_empresas_investigadas > 0 ? 'bg-amber-50 text-amber-600' : 'bg-emerald-50 text-emerald-600'}`}>💰 {c.indicadores.doacoes_empresas_investigadas} doações investigadas</span>
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-md bg-emerald-50 text-emerald-600 text-xs font-medium">💼 {fmtMoeda(c.indicadores.patrimonio_declarado)}</span>
          {c.indicadores.presenca_legislativa_percent != null && (
            <span className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-md text-xs font-medium ${c.indicadores.presenca_legislativa_percent < 70 ? 'bg-red-50 text-red-600' : 'bg-emerald-50 text-emerald-600'}`}>🏛️ Presença: {c.indicadores.presenca_legislativa_percent}%</span>
          )}
        </div>
      </div>

      {/* Abas */}
      <div className="bg-white rounded-xl shadow-card border border-surface-200 overflow-hidden">
        <div className="flex overflow-x-auto border-b border-surface-100">
          {abas.map(a => (
            <button key={a.key} onClick={() => setAba(a.key)}
              className={`px-5 py-3.5 text-sm font-semibold whitespace-nowrap transition-colors ${aba === a.key ? 'border-b-[2.5px] border-brand-600 text-brand-700 bg-brand-50/50' : 'text-surface-500 hover:text-surface-700 hover:bg-surface-50'}`}>
              {a.label}
              {a.count > 0 && <span className="ml-2 px-1.5 py-0.5 rounded-full bg-surface-200 text-xs font-bold text-surface-600">{a.count}</span>}
            </button>
          ))}
        </div>

        <div className="p-6">
          {aba === 'processos' && (
            <div>
              <p className="text-xs text-surface-400 mb-4">Fonte: DataJud (CNJ). Passe o mouse sobre a instância para ver o significado.</p>
              {secoes.processos.length === 0 ? <div className="text-center py-8 text-surface-400"><p className="text-sm">Nenhum processo judicial encontrado.</p></div> : (
                <div className="space-y-3">
                  {secoes.processos.map((p, i) => (
                    <div key={i} className="p-4 bg-surface-50 rounded-xl border border-surface-100">
                      <div className="flex items-start justify-between gap-3">
                        <div className="flex-1">
                          <p className="font-semibold text-surface-800 text-sm">{p.tipo}</p>
                          <div className="flex items-center gap-2 mt-1.5 flex-wrap">
                            <span className="text-xs bg-white px-2 py-0.5 rounded-md border border-surface-200 cursor-help" title={instanciaInfo[p.instancia] || p.instancia}>{p.instancia}</span>
                            <span className={`inline-flex items-center px-2 py-0.5 rounded-md text-[11px] font-medium ${p.status === 'transitada_em_julgado' ? 'bg-red-50 text-red-600' : p.status === 'em_andamento' ? 'bg-amber-50 text-amber-600' : 'bg-emerald-50 text-emerald-600'}`}>{statusLabels[p.status] || p.status}</span>
                          </div>
                          {p.observacao && <p className="text-xs text-surface-500 mt-2 leading-relaxed">{p.observacao}</p>}
                          <div className="flex gap-3 mt-2 text-[11px] text-surface-400">{p.data_inicio && <span>Início: {p.data_inicio}</span>}{p.data_decisao && <span>Decisão: {p.data_decisao}</span>}</div>
                        </div>
                      </div>
                      <a href={p.fonte} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1 mt-3 text-xs font-medium text-brand-600 hover:text-brand-700">Ver no DataJud ↗</a>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {aba === 'materias' && (
            <div>
              <p className="text-xs text-surface-400 mb-4">O sistema não classifica o tom das matérias — apenas lista os fatos.</p>
              {secoes.materias.length === 0 ? <div className="text-center py-8 text-surface-400"><p className="text-sm">Nenhuma matéria encontrada.</p></div> : (
                <div className="divide-y divide-surface-100">
                  {secoes.materias.map((m, i) => (
                    <div key={i} className="py-3 flex items-start justify-between gap-3">
                      <div>
                        <a href={m.url} target="_blank" rel="noopener noreferrer" className="text-sm text-surface-800 hover:text-brand-600 font-medium leading-snug">{m.titulo}</a>
                        <p className="text-xs text-surface-400 mt-0.5">{m.veiculo} • {m.data}</p>
                      </div>
                      <a href={m.url} target="_blank" rel="noopener noreferrer" className="text-xs text-brand-600 font-medium whitespace-nowrap hover:underline">Ler →</a>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {aba === 'gastos' && (
            <div>
              <p className="text-xs text-surface-400 mb-4">Fonte: TSE — Prestação de Contas 2026.</p>
              {secoes.gastos_campanha ? (
                <div>
                  <div className="bg-surface-50 rounded-xl p-5 mb-4"><p className="text-3xl font-bold text-surface-800 tabular-nums">{fmtMoeda(secoes.gastos_campanha.total_declarado)}</p><p className="text-sm text-surface-500 mt-1">Total declarado em campanha</p></div>
                  {secoes.gastos_campanha.maiores_doadores.length > 0 && (
                    <div>
                      <h4 className="font-semibold text-sm text-surface-700 mb-2">Maiores doadores</h4>
                      <div className="space-y-2">
                        {secoes.gastos_campanha.maiores_doadores.map((d, i) => (
                          <div key={i} className="flex justify-between items-center p-3 bg-surface-50 rounded-xl border border-surface-100">
                            <div><p className="text-sm font-medium text-surface-800">{d.nome}</p>{d.cpf_cnpj && <p className="text-[11px] text-surface-400">CPF/CNPJ: {d.cpf_cnpj}</p>}</div>
                            <span className="text-sm font-bold text-surface-700 tabular-nums">{fmtMoeda(d.valor)}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                  <a href={secoes.gastos_campanha.fonte} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1 mt-4 text-xs font-medium text-brand-600 hover:underline">Ver fonte no TSE ↗</a>
                </div>
              ) : <div className="text-center py-8 text-surface-400"><p className="text-sm">Sem dados disponíveis.</p></div>}
            </div>
          )}

          {aba === 'bens' && (
            <div>
              <p className="text-xs text-surface-400 mb-4">Fonte: TSE — DivulgaCand 2026.</p>
              {secoes.bens_declarados.length === 0 ? <div className="text-center py-8 text-surface-400"><p className="text-sm">Nenhum bem declarado.</p></div> : (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {secoes.bens_declarados.map((b, i) => (
                    <div key={i} className="p-4 bg-surface-50 rounded-xl border border-surface-100 flex justify-between items-start">
                      <div><p className="text-sm font-medium text-surface-800">{b.descricao}</p><span className="inline-flex items-center mt-1 px-2 py-0.5 rounded-md bg-surface-200 text-surface-600 text-[11px] font-medium">{b.tipo}</span></div>
                      <span className="text-sm font-bold text-surface-700 tabular-nums">{fmtMoeda(b.valor)}</span>
                    </div>
                  ))}
                </div>
              )}
              {secoes.bens_declarados.length > 0 && <a href={secoes.bens_declarados[0].fonte} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1 mt-4 text-xs font-medium text-brand-600 hover:underline">Ver fonte no TSE ↗</a>}
            </div>
          )}

          {aba === 'legislativo' && (
            <div>
              <p className="text-xs text-surface-400 mb-4">Fonte: Câmara dos Deputados / Senado Federal.</p>
              {secoes.historico_legislativo ? (
                <div className="grid grid-cols-3 gap-4">
                  <div className="bg-surface-50 rounded-xl p-5 text-center border border-surface-100"><p className="text-3xl font-bold text-surface-800 tabular-nums">{secoes.historico_legislativo.presenca_percent}%</p><p className="text-xs text-surface-500 mt-1 font-medium">Presença</p></div>
                  <div className="bg-surface-50 rounded-xl p-5 text-center border border-surface-100"><p className="text-3xl font-bold text-surface-800 tabular-nums">{secoes.historico_legislativo.projetos_propostos}</p><p className="text-xs text-surface-500 mt-1 font-medium">Projetos</p></div>
                  <div className="bg-surface-50 rounded-xl p-5 text-center border border-surface-100"><p className="text-3xl font-bold text-surface-800 tabular-nums">{secoes.historico_legislativo.votos_em_pautas_politicas}</p><p className="text-xs text-surface-500 mt-1 font-medium">Votações</p></div>
                </div>
              ) : <div className="text-center py-8 text-surface-400"><p className="text-sm">Candidato sem cargo parlamentar registrado.</p></div>}
            </div>
          )}

          {aba === 'contratos' && (
            <div>
              <p className="text-xs text-surface-400 mb-4">Fonte: Portal da Transparência.</p>
              {secoes.contratos_governo.length === 0 ? <div className="text-center py-8 text-surface-400"><p className="text-sm">Nenhum contrato governamental encontrado.</p></div> : (
                <div className="space-y-3">
                  {secoes.contratos_governo.map((ct, i) => (
                    <div key={i} className="p-4 bg-surface-50 rounded-xl border border-surface-100">
                      <p className="font-semibold text-surface-800 text-sm">{ct.empresa}</p>
                      <div className="grid grid-cols-2 gap-2 mt-2 text-xs text-surface-600"><p>Contrato: {ct.contrato_numero}</p><p>Valor: {fmtMoeda(ct.valor)}</p><p>Órgão: {ct.orgao_contratante}</p><p>Data: {ct.data_assinatura}</p></div>
                      <a href={ct.fonte} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1 mt-2 text-xs font-medium text-brand-600 hover:underline">Ver no Portal ↗</a>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      <p className="text-center text-xs text-surface-400">Dados atualizados em {perfil.data_atualizacao} • Schema v{perfil.versao_schema}</p>
    </div>
  )
}
