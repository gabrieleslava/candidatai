export interface Indicadores {
  processos_totais: number
  processos_condenacao_transitada: number
  processos_em_andamento: number
  materias_12m: number
  doacoes_empresas_investigadas: number
  patrimonio_declarado: number
  presenca_legislativa_percent: number | null
}

export interface Candidato {
  id: number
  nome: string
  numero: number | null
  partido: string
  cargo: string
  estado: string
  foto_url: string | null
  intencao_voto: number | null
  pesquisa_fonte: string | null
  indicadores: Indicadores
}

export interface Processo {
  id: number
  tipo: string
  instancia: string
  status: string
  data_inicio: string | null
  data_decisao: string | null
  fonte: string
  observacao: string | null
}

export interface Materia {
  id: number
  titulo: string
  veiculo: string
  data: string
  url: string
  fonte_api: string | null
}

export interface GastosCampanha {
  total_declarado: number
  maiores_doadores: Doador[]
  fonte: string
}

export interface Doador {
  id: number
  nome: string
  valor: number
  cpf_cnpj: string | null
  fonte: string
}

export interface Bem {
  id: number
  descricao: string
  valor: number
  tipo: string
  fonte: string
}

export interface HistoricoLegislativo {
  id: number
  presenca_percent: number | null
  projetos_propostos: number
  votos_em_pautas_politicas: number
  fonte: string
}

export interface Contrato {
  id: number
  empresa: string
  contrato_numero: string
  valor: number
  orgao_contratante: string
  data_assinatura: string
  fonte: string
}

export interface PerfilCompleto {
  candidato: {
    nome: string
    numero: number | null
    partido: string
    cargo: string
    estado: string
    intencao_voto: number | null
    pesquisa_fonte: string | null
    foto_url: string | null
    indicadores: Indicadores
  }
  secoes: {
    processos: Processo[]
    materias: Materia[]
    gastos_campanha: GastosCampanha | null
    bens_declarados: Bem[]
    historico_legislativo: HistoricoLegislativo | null
    contratos_governo: Contrato[]
  }
  data_atualizacao: string
  versao_schema: string
}
