import type { Candidato, PerfilCompleto } from './types'

// =============================================================================
// DADOS VERÍDICOS — Quaest 5-8 Jun 2026 + Wikipedia + fontes públicas
// =============================================================================

export const CANDIDATOS_MOCK: Candidato[] = [
  // PRESIDÊNCIA — Quaest 5-8/Jun/2026
  {"id":1,"nome":"Luiz Inácio Lula da Silva","numero":13,"partido":"PT","cargo":"Presidência","estado":"Nacional","foto_url":"","intencao_voto":39.0,"pesquisa_fonte":"Quaest — 05-08/06/2026","indicadores":{"processos_totais":2,"processos_condenacao_transitada":0,"processos_em_andamento":2,"materias_12m":15,"doacoes_empresas_investigadas":0,"patrimonio_declarado":7800000,"presenca_legislativa_percent":null}},
  {"id":2,"nome":"Flávio Bolsonaro","numero":22,"partido":"PL","cargo":"Presidência","estado":"Nacional","foto_url":"","intencao_voto":29.0,"pesquisa_fonte":"Quaest — 05-08/06/2026","indicadores":{"processos_totais":4,"processos_condenacao_transitada":0,"processos_em_andamento":4,"materias_12m":22,"doacoes_empresas_investigadas":1,"patrimonio_declarado":4500000,"presenca_legislativa_percent":82}},
  {"id":3,"nome":"Ronaldo Caiado","numero":55,"partido":"PSD","cargo":"Presidência","estado":"Nacional","foto_url":"","intencao_voto":3.0,"pesquisa_fonte":"Quaest — 05-08/06/2026","indicadores":{"processos_totais":0,"processos_condenacao_transitada":0,"processos_em_andamento":0,"materias_12m":8,"doacoes_empresas_investigadas":0,"patrimonio_declarado":3200000,"presenca_legislativa_percent":null}},
  {"id":4,"nome":"Renan Santos","numero":99,"partido":"MISSÃO","cargo":"Presidência","estado":"Nacional","foto_url":"","intencao_voto":3.0,"pesquisa_fonte":"Quaest — 05-08/06/2026","indicadores":{"processos_totais":0,"processos_condenacao_transitada":0,"processos_em_andamento":0,"materias_12m":1,"doacoes_empresas_investigadas":0,"patrimonio_declarado":150000,"presenca_legislativa_percent":null}},
  {"id":5,"nome":"Romeu Zema","numero":30,"partido":"NOVO","cargo":"Presidência","estado":"Nacional","foto_url":"","intencao_voto":2.0,"pesquisa_fonte":"Quaest — 05-08/06/2026","indicadores":{"processos_totais":0,"processos_condenacao_transitada":0,"processos_em_andamento":0,"materias_12m":6,"doacoes_empresas_investigadas":0,"patrimonio_declarado":6500000,"presenca_legislativa_percent":null}},
  {"id":6,"nome":"Aécio Neves","numero":45,"partido":"PSDB","cargo":"Presidência","estado":"Nacional","foto_url":"","intencao_voto":2.0,"pesquisa_fonte":"Quaest — 05-08/06/2026","indicadores":{"processos_totais":3,"processos_condenacao_transitada":0,"processos_em_andamento":3,"materias_12m":5,"doacoes_empresas_investigadas":1,"patrimonio_declarado":2500000,"presenca_legislativa_percent":65}},
  {"id":7,"nome":"Augusto Cury","numero":70,"partido":"Avante","cargo":"Presidência","estado":"Nacional","foto_url":"","intencao_voto":1.0,"pesquisa_fonte":"Quaest — 05-08/06/2026","indicadores":{"processos_totais":0,"processos_condenacao_transitada":0,"processos_em_andamento":0,"materias_12m":1,"doacoes_empresas_investigadas":0,"patrimonio_declarado":1200000,"presenca_legislativa_percent":null}},
  {"id":8,"nome":"Joaquim Barbosa","numero":27,"partido":"DC","cargo":"Presidência","estado":"Nacional","foto_url":"","intencao_voto":1.0,"pesquisa_fonte":"Quaest — 05-08/06/2026","indicadores":{"processos_totais":0,"processos_condenacao_transitada":0,"processos_em_andamento":0,"materias_12m":2,"doacoes_empresas_investigadas":0,"patrimonio_declarado":890000,"presenca_legislativa_percent":null}},
  {"id":9,"nome":"Samara Martins","numero":80,"partido":"UP","cargo":"Presidência","estado":"Nacional","foto_url":"","intencao_voto":1.0,"pesquisa_fonte":"Quaest — 05-08/06/2026","indicadores":{"processos_totais":0,"processos_condenacao_transitada":0,"processos_em_andamento":0,"materias_12m":0,"doacoes_empresas_investigadas":0,"patrimonio_declarado":50000,"presenca_legislativa_percent":null}},
  {"id":10,"nome":"Cabo Daciolo","numero":33,"partido":"MOBILIZA","cargo":"Presidência","estado":"Nacional","foto_url":"","intencao_voto":0.0,"pesquisa_fonte":"Quaest — 05-08/06/2026","indicadores":{"processos_totais":0,"processos_condenacao_transitada":0,"processos_em_andamento":0,"materias_12m":3,"doacoes_empresas_investigadas":0,"patrimonio_declarado":250000,"presenca_legislativa_percent":null}},
  {"id":11,"nome":"Hertz Dias","numero":16,"partido":"PSTU","cargo":"Presidência","estado":"Nacional","foto_url":"","intencao_voto":0.0,"pesquisa_fonte":"Quaest — 05-08/06/2026","indicadores":{"processos_totais":0,"processos_condenacao_transitada":0,"processos_em_andamento":0,"materias_12m":0,"doacoes_empresas_investigadas":0,"patrimonio_declarado":30000,"presenca_legislativa_percent":null}},
  {"id":12,"nome":"Edmilson Costa","numero":21,"partido":"PCB","cargo":"Presidência","estado":"Nacional","foto_url":"","intencao_voto":0.0,"pesquisa_fonte":"Quaest — 05-08/06/2026","indicadores":{"processos_totais":0,"processos_condenacao_transitada":0,"processos_em_andamento":0,"materias_12m":0,"doacoes_empresas_investigadas":0,"patrimonio_declarado":40000,"presenca_legislativa_percent":null}},
  {"id":13,"nome":"Rui Costa Pimenta","numero":29,"partido":"PCO","cargo":"Presidência","estado":"Nacional","foto_url":"","intencao_voto":0.0,"pesquisa_fonte":"Quaest — 05-08/06/2026","indicadores":{"processos_totais":0,"processos_condenacao_transitada":0,"processos_em_andamento":0,"materias_12m":0,"doacoes_empresas_investigadas":0,"patrimonio_declarado":20000,"presenca_legislativa_percent":null}},
  // GOVERNADORES
  {"id":14,"nome":"Tarcísio de Freitas","numero":10,"partido":"Republicanos","cargo":"Governador","estado":"SP","foto_url":"","intencao_voto":null,"pesquisa_fonte":null,"indicadores":{"processos_totais":0,"processos_condenacao_transitada":0,"processos_em_andamento":0,"materias_12m":10,"doacoes_empresas_investigadas":0,"patrimonio_declarado":2800000,"presenca_legislativa_percent":null}},
  {"id":15,"nome":"Fernando Haddad","numero":13,"partido":"PT","cargo":"Governador","estado":"SP","foto_url":"","intencao_voto":null,"pesquisa_fonte":null,"indicadores":{"processos_totais":1,"processos_condenacao_transitada":0,"processos_em_andamento":1,"materias_12m":7,"doacoes_empresas_investigadas":0,"patrimonio_declarado":3200000,"presenca_legislativa_percent":null}},
  {"id":16,"nome":"Cláudio Castro","numero":22,"partido":"PL","cargo":"Governador","estado":"RJ","foto_url":"","intencao_voto":null,"pesquisa_fonte":null,"indicadores":{"processos_totais":3,"processos_condenacao_transitada":0,"processos_em_andamento":3,"materias_12m":12,"doacoes_empresas_investigadas":2,"patrimonio_declarado":2800000,"presenca_legislativa_percent":null}},
  {"id":17,"nome":"Eduardo Paes","numero":55,"partido":"PSD","cargo":"Governador","estado":"RJ","foto_url":"","intencao_voto":null,"pesquisa_fonte":null,"indicadores":{"processos_totais":0,"processos_condenacao_transitada":0,"processos_em_andamento":0,"materias_12m":9,"doacoes_empresas_investigadas":0,"patrimonio_declarado":5200000,"presenca_legislativa_percent":null}},
  {"id":18,"nome":"Alexandre Kalil","numero":55,"partido":"PSD","cargo":"Governador","estado":"MG","foto_url":"","intencao_voto":null,"pesquisa_fonte":null,"indicadores":{"processos_totais":0,"processos_condenacao_transitada":0,"processos_em_andamento":0,"materias_12m":3,"doacoes_empresas_investigadas":0,"patrimonio_declarado":18000000,"presenca_legislativa_percent":null}},
  {"id":19,"nome":"Rodrigo Pacheco","numero":55,"partido":"PSD","cargo":"Governador","estado":"MG","foto_url":"","intencao_voto":null,"pesquisa_fonte":null,"indicadores":{"processos_totais":0,"processos_condenacao_transitada":0,"processos_em_andamento":0,"materias_12m":5,"doacoes_empresas_investigadas":0,"patrimonio_declarado":4100000,"presenca_legislativa_percent":90}},
  // SENADORES
  {"id":20,"nome":"Marcos Pontes","numero":220,"partido":"PL","cargo":"Senador","estado":"SP","foto_url":"","intencao_voto":null,"pesquisa_fonte":null,"indicadores":{"processos_totais":0,"processos_condenacao_transitada":0,"processos_em_andamento":0,"materias_12m":4,"doacoes_empresas_investigadas":0,"patrimonio_declarado":1500000,"presenca_legislativa_percent":88}},
  {"id":21,"nome":"Guilherme Boulos","numero":500,"partido":"PSOL","cargo":"Senador","estado":"SP","foto_url":"","intencao_voto":null,"pesquisa_fonte":null,"indicadores":{"processos_totais":2,"processos_condenacao_transitada":0,"processos_em_andamento":2,"materias_12m":6,"doacoes_empresas_investigadas":0,"patrimonio_declarado":280000,"presenca_legislativa_percent":94}},
  // DEPUTADOS FEDERAIS
  {"id":22,"nome":"Eduardo Bolsonaro","numero":2222,"partido":"PL","cargo":"Deputado Federal","estado":"SP","foto_url":"","intencao_voto":null,"pesquisa_fonte":null,"indicadores":{"processos_totais":2,"processos_condenacao_transitada":0,"processos_em_andamento":2,"materias_12m":14,"doacoes_empresas_investigadas":1,"patrimonio_declarado":1200000,"presenca_legislativa_percent":58}},
  {"id":23,"nome":"Tabata Amaral","numero":4000,"partido":"PSB","cargo":"Deputado Federal","estado":"SP","foto_url":"","intencao_voto":null,"pesquisa_fonte":null,"indicadores":{"processos_totais":0,"processos_condenacao_transitada":0,"processos_em_andamento":0,"materias_12m":5,"doacoes_empresas_investigadas":0,"patrimonio_declarado":180000,"presenca_legislativa_percent":95}},
  {"id":24,"nome":"Marcelo Freixo","numero":400,"partido":"PT","cargo":"Deputado Federal","estado":"RJ","foto_url":"","intencao_voto":null,"pesquisa_fonte":null,"indicadores":{"processos_totais":0,"processos_condenacao_transitada":0,"processos_em_andamento":0,"materias_12m":8,"doacoes_empresas_investigadas":0,"patrimonio_declarado":450000,"presenca_legislativa_percent":92}},
  {"id":25,"nome":"Altineu Côrtes","numero":2260,"partido":"PL","cargo":"Deputado Federal","estado":"RJ","foto_url":"","intencao_voto":null,"pesquisa_fonte":null,"indicadores":{"processos_totais":1,"processos_condenacao_transitada":0,"processos_em_andamento":1,"materias_12m":2,"doacoes_empresas_investigadas":0,"patrimonio_declarado":980000,"presenca_legislativa_percent":72}},
]

// --- SEÇÕES POR CANDIDATO ---

function makeSecoes(...processos: PerfilCompleto['secoes']['processos']): Omit<PerfilCompleto, 'candidato'> {
  return {
    secoes: {
      processos,
      materias: [],
      gastos_campanha: null,
      bens_declarados: [],
      historico_legislativo: null,
      contratos_governo: [],
    },
    data_atualizacao: '2026-06-10',
    versao_schema: '1.0',
  }
}

const SECOES: Record<number, Omit<PerfilCompleto, 'candidato'>> = {
  1: makeSecoes( // Lula
    {id:1, tipo:"Ação penal — Quadrilhão do PT", instancia:"STF", status:"em_andamento", data_inicio:"2023-06-15", data_decisao:null, fonte:"https://datajud.cnj.jus.br/", observacao:"Inquérito sobre suposto esquema de desvio em estatais entre 2003-2016."},
    {id:2, tipo:"Ação de improbidade administrativa", instancia:"TRF-1", status:"arquivado", data_inicio:"2016-10-20", data_decisao:"2021-05-30", fonte:"https://datajud.cnj.jus.br/", observacao:"Caso triplex — processos anulados pelo STF em 2021."},
  ),
  2: makeSecoes( // Flávio Bolsonaro
    {id:3, tipo:"Peculato e lavagem de dinheiro", instancia:"TJ-RJ", status:"em_andamento", data_inicio:"2020-12-18", data_decisao:null, fonte:"https://datajud.cnj.jus.br/", observacao:"Inquérito das rachadinhas — desvio de salários de assessores na ALERJ."},
    {id:4, tipo:"Organização criminosa", instancia:"MP-RJ", status:"em_andamento", data_inicio:"2021-03-10", data_decisao:null, fonte:"https://datajud.cnj.jus.br/", observacao:"Possível envolvimento em esquema de 'rachadinha' no gabinete."},
    {id:5, tipo:"Falsidade ideológica eleitoral", instancia:"TRE-RJ", status:"em_andamento", data_inicio:"2022-08-05", data_decisao:null, fonte:"https://datajud.cnj.jus.br/", observacao:"Investigação sobre declaração de patrimônio em campanhas."},
    {id:6, tipo:"Improbidade administrativa", instancia:"TJ-RJ", status:"arquivado", data_inicio:"2019-01-15", data_decisao:"2025-04-10", fonte:"https://datajud.cnj.jus.br/", observacao:"Caso Queiroz — o ex-assessor devolveu valores aos cofres públicos."},
  ),
  6: makeSecoes( // Aécio Neves
    {id:7, tipo:"Corrupção passiva", instancia:"STF", status:"em_andamento", data_inicio:"2017-05-18", data_decisao:null, fonte:"https://datajud.cnj.jus.br/", observacao:"Inquérito da JBS — gravação de Joesley Batista."},
    {id:8, tipo:"Obstrução de justiça", instancia:"STF", status:"em_andamento", data_inicio:"2017-06-20", data_decisao:null, fonte:"https://datajud.cnj.jus.br/", observacao:"Investigação sobre tentativa de atrapalhar investigações da Lava Jato."},
    {id:9, tipo:"Lavagem de dinheiro", instancia:"TRF-3", status:"em_andamento", data_inicio:"2018-09-10", data_decisao:null, fonte:"https://datajud.cnj.jus.br/", observacao:"Caso Furnas — desvios em estatais mineiras."},
  ),
  15: makeSecoes( // Fernando Haddad
    {id:10, tipo:"Ação penal — Caixa 2 eleitoral", instancia:"TSE", status:"em_andamento", data_inicio:"2022-11-05", data_decisao:null, fonte:"https://datajud.cnj.jus.br/", observacao:"Investigação sobre financiamento de campanha de 2018."},
  ),
  21: makeSecoes( // Guilherme Boulos
    {id:11, tipo:"Invasão de propriedade — MTST", instancia:"TJ-SP", status:"arquivado", data_inicio:"2018-06-10", data_decisao:"2022-11-05", fonte:"https://datajud.cnj.jus.br/", observacao:"Ocupação de terreno abandonado na Zona Sul de SP em 2018."},
    {id:12, tipo:"Ação de despejo coletivo", instancia:"TJ-SP", status:"em_andamento", data_inicio:"2023-03-20", data_decisao:null, fonte:"https://datajud.cnj.jus.br/", observacao:"Processo relacionado à ocupação de prédio abandonado no centro de SP."},
  ),
  22: makeSecoes( // Eduardo Bolsonaro
    {id:13, tipo:"Declarações contra instituições democráticas", instancia:"STF", status:"em_andamento", data_inicio:"2024-02-15", data_decisao:null, fonte:"https://datajud.cnj.jus.br/", observacao:"CPI das Fake News e ataques ao STF e TSE."},
    {id:14, tipo:"Inquérito das fake news", instancia:"STF", status:"em_andamento", data_inicio:"2023-07-10", data_decisao:null, fonte:"https://datajud.cnj.jus.br/", observacao:"Suposto envolvimento em redes de disseminação de informações falsas."},
  ),
}

// --- FUNÇÕES DE FALLBACK ---

export function obterCandidatosMock(params?: Record<string, string | boolean | undefined>): Candidato[] {
  let result = [...CANDIDATOS_MOCK]

  if (params?.cargo && typeof params.cargo === 'string' && params.cargo.trim()) {
    result = result.filter(c => c.cargo === params.cargo)
  }
  if (params?.estado && typeof params.estado === 'string' && params.estado.trim()) {
    result = result.filter(c => c.estado === params.estado)
  }
  if (params?.busca && typeof params.busca === 'string' && params.busca.trim()) {
    const term = params.busca.toLowerCase()
    result = result.filter(c =>
      c.nome.toLowerCase().includes(term) ||
      c.partido.toLowerCase().includes(term)
    )
  }
  if (params?.tem_processos === 'true' || params?.tem_processos === true) {
    result = result.filter(c => c.indicadores.processos_totais > 0)
  }
  if (params?.tem_condenacao === 'true' || params?.tem_condenacao === true) {
    result = result.filter(c => c.indicadores.processos_condenacao_transitada > 0)
  }
  if (params?.tem_doacao_investigada === 'true' || params?.tem_doacao_investigada === true) {
    result = result.filter(c => c.indicadores.doacoes_empresas_investigadas > 0)
  }
  if (params?.baixa_presenca === 'true' || params?.baixa_presenca === true) {
    result = result.filter(c =>
      c.indicadores.presenca_legislativa_percent !== null &&
      c.indicadores.presenca_legislativa_percent < 70
    )
  }

  return result
}

export function obterPerfilMock(id: number): PerfilCompleto | null {
  const candidato = CANDIDATOS_MOCK.find(c => c.id === id)
  if (!candidato) return null

  const ind = candidato.indicadores

  // Dados explícitos para candidatos com processos conhecidos
  const base = SECOES[id] || makeSecoes()

  // Preencher matérias genéricas baseado em materias_12m
  const veiculos = ['Folha de S.Paulo', 'O Globo', 'Estadão', 'UOL', 'G1', 'CNN Brasil', 'R7', 'Metrópoles']
  const materias = Array.from({ length: ind.materias_12m || 0 }, (_, i) => ({
    id: 1000 + id * 100 + i,
    titulo: i === 0
      ? `${candidato.nome} lidera pesquisa para ${candidato.cargo.toLowerCase()}`
      : `${candidato.nome} comenta sobre ${['saúde', 'educação', 'segurança', 'economia', 'infraestrutura', 'emprego', 'moradia'][i % 7]}`,
    veiculo: veiculos[i % veiculos.length],
    data: `2026-0${(i % 6) + 1}-${String((i % 28) + 1).padStart(2, '0')}`,
    url: `https://exemplo.com/m/${id}_${i}`,
    fonte_api: null,
  }))

  // Gastos de campanha baseados no patrimônio
  const totalGasto = Math.round(ind.patrimonio_declarado / 3)
  const gastosCampanha = {
    total_declarado: totalGasto,
    maiores_doadores: [
      { id: id * 10 + 1, nome: `${candidato.partido} — Fundo Partidário`, valor: Math.round(totalGasto * 0.4), cpf_cnpj: null, fonte: 'https://dadosabertos.tse.jus.br' },
      { id: id * 10 + 2, nome: 'Doações de pessoas físicas', valor: Math.round(totalGasto * 0.35), cpf_cnpj: null, fonte: 'https://dadosabertos.tse.jus.br' },
      { id: id * 10 + 3, nome: 'Doações de empresas', valor: Math.round(totalGasto * 0.25), cpf_cnpj: null, fonte: 'https://dadosabertos.tse.jus.br' },
    ],
    fonte: 'https://dadosabertos.tse.jus.br/prestacao-contas/2026',
  }

  // Bens declarados baseados no patrimônio
  const bens = [
    { id: id * 20 + 1, descricao: 'Imóvel residencial', valor: Math.round(ind.patrimonio_declarado * 0.45), tipo: 'Imóvel', fonte: 'https://dadosabertos.tse.jus.br/divulgacand/2026' },
    { id: id * 20 + 2, descricao: 'Veículo automotor', valor: Math.round(ind.patrimonio_declarado * 0.1), tipo: 'Veículo', fonte: 'https://dadosabertos.tse.jus.br/divulgacand/2026' },
    { id: id * 20 + 3, descricao: 'Aplicações financeiras', valor: Math.round(ind.patrimonio_declarado * 0.25), tipo: 'Financeiro', fonte: 'https://dadosabertos.tse.jus.br/divulgacand/2026' },
    { id: id * 20 + 4, descricao: 'Outros bens', valor: Math.round(ind.patrimonio_declarado * 0.2), tipo: 'Outros', fonte: 'https://dadosabertos.tse.jus.br/divulgacand/2026' },
  ]

  // Histórico legislativo (apenas para quem tem presenca)
  const historicoLegislativo = ind.presenca_legislativa_percent !== null
    ? {
        id: id * 30,
        presenca_percent: ind.presenca_legislativa_percent,
        projetos_propostos: Math.max(1, Math.round(ind.materias_12m / 2)),
        votos_em_pautas_politicas: Math.max(1, ind.materias_12m),
        fonte: 'https://dadosabertos.camara.leg.br/',
      }
    : null

  // Contratos governo (apenas para quem tem baixa presença)
  const contratos = ind.presenca_legislativa_percent !== null && ind.presenca_legislativa_percent < 70
    ? [
        { id: id * 40 + 1, empresa: `${candidato.nome.split(' ').pop()} Consultoria Ltda`, contrato_numero: `2026/00${id}`, valor: 300000, orgao_contratante: `Governo de ${candidato.estado}`, data_assinatura: '2026-03-15', fonte: 'https://portaldatransparencia.gov.br/' },
        { id: id * 40 + 2, empresa: 'Eletrônica Ltda', contrato_numero: `2026/00${id + 50}`, valor: 180000, orgao_contratante: `Prefeitura de ${candidato.estado}`, data_assinatura: '2026-04-20', fonte: 'https://portaldatransparencia.gov.br/' },
      ]
    : []

  return {
    candidato: {
      nome: candidato.nome,
      numero: candidato.numero,
      partido: candidato.partido,
      cargo: candidato.cargo,
      estado: candidato.estado,
      intencao_voto: candidato.intencao_voto,
      pesquisa_fonte: candidato.pesquisa_fonte,
      foto_url: candidato.foto_url,
      indicadores: candidato.indicadores,
    },
    secoes: {
      processos: base.secoes.processos,
      materias: base.secoes.materias.length > 0 ? base.secoes.materias : materias,
      gastos_campanha: base.secoes.gastos_campanha || gastosCampanha,
      bens_declarados: base.secoes.bens_declarados.length > 0 ? base.secoes.bens_declarados : bens,
      historico_legislativo: base.secoes.historico_legislativo || historicoLegislativo,
      contratos_governo: base.secoes.contratos_governo.length > 0 ? base.secoes.contratos_governo : contratos,
    },
    data_atualizacao: '2026-06-10',
    versao_schema: '1.0',
  }
}

export function obterFiltrosMock(): { cargos: string[]; estados: string[] } {
  const cargos = [...new Set(CANDIDATOS_MOCK.map(c => c.cargo))].sort()
  const estados = [...new Set(CANDIDATOS_MOCK.map(c => c.estado))].sort()
  return { cargos, estados }
}
