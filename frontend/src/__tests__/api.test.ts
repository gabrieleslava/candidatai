import { describe, it, expect, vi, beforeEach } from 'vitest'
import {
  listarCandidatos,
  perfilCandidato,
  compararCandidatos,
  opcoesFiltros,
} from '../api'
import type { PerfilCompleto } from '../types'

const mockCandidato = {
  id: 1,
  nome: 'Maria Souza',
  numero: 13,
  partido: 'PT',
  cargo: 'Presidência',
  estado: 'Nacional',
  foto_url: '',
  intencao_voto: 23.0,
  pesquisa_fonte: 'Datafolha',
  indicadores: {
    processos_totais: 3,
    processos_condenacao_transitada: 0,
    processos_em_andamento: 3,
    materias_12m: 12,
    doacoes_empresas_investigadas: 1,
    patrimonio_declarado: 1450000,
    presenca_legislativa_percent: null,
  },
}

const mockPerfil: PerfilCompleto = {
  candidato: {
    nome: 'Maria Souza',
    numero: 13,
    partido: 'PT',
    cargo: 'Presidência',
    estado: 'Nacional',
    intencao_voto: 23.0,
    pesquisa_fonte: 'Datafolha',
    foto_url: '',
    indicadores: mockCandidato.indicadores,
  },
  secoes: {
    processos: [],
    materias: [],
    gastos_campanha: null,
    bens_declarados: [],
    historico_legislativo: null,
    contratos_governo: [],
  },
  data_atualizacao: '2026-06-10',
  versao_schema: '1.0',
}

describe('API Client', () => {
  beforeEach(() => {
    vi.restoreAllMocks()
  })

  describe('listarCandidatos', () => {
    it('constrói URL corretamente sem parâmetros', async () => {
      globalThis.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve([mockCandidato]),
      })

      await listarCandidatos()
      expect(globalThis.fetch).toHaveBeenCalledWith('/api/candidatos')
    })

    it('constrói URL com parâmetros de filtro', async () => {
      globalThis.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve([mockCandidato]),
      })

      await listarCandidatos({ cargo: 'Presidência', estado: 'SP' })
      const url = (globalThis.fetch as ReturnType<typeof vi.fn>).mock.calls[0][0] as string
      // URLSearchParams encode accents
      expect(url).toContain('cargo=Presid%C3%AAncia')
      expect(url).toContain('estado=SP')
    })

    it('faz fallback para mock quando API falha', async () => {
      globalThis.fetch = vi.fn().mockRejectedValue(new Error('Network error'))

      const result = await listarCandidatos({ cargo: 'Presidência' })
      expect(Array.isArray(result)).toBe(true)
      expect(result.length).toBeGreaterThan(0)
      expect(result[0].nome).toBeDefined()
    })

    it('faz fallback quando resposta não é ok', async () => {
      globalThis.fetch = vi.fn().mockResolvedValue({
        ok: false,
        status: 500,
      })

      const result = await listarCandidatos()
      expect(Array.isArray(result)).toBe(true)
      expect(result.length).toBeGreaterThan(0)
    })

    it('omite parâmetros undefined ou vazios na URL', async () => {
      globalThis.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve([]),
      })

      await listarCandidatos({ cargo: '', estado: undefined, busca: '' })
      const url = (globalThis.fetch as ReturnType<typeof vi.fn>).mock.calls[0][0] as string
      expect(url).not.toContain('cargo=')
      expect(url).not.toContain('estado=')
      expect(url).not.toContain('busca=')
    })
  })

  describe('perfilCandidato', () => {
    it('busca perfil por ID', async () => {
      globalThis.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve(mockPerfil),
      })

      const result = await perfilCandidato(1)
      expect(globalThis.fetch).toHaveBeenCalledWith('/api/candidatos/1')
      expect(result.candidato.nome).toBe('Maria Souza')
    })

    it('fallback para mock quando API falha', async () => {
      globalThis.fetch = vi.fn().mockRejectedValue(new Error('fail'))

      const result = await perfilCandidato(1)
      expect(result.candidato).toBeDefined()
      expect(result.secoes).toBeDefined()
    })
  })

  describe('compararCandidatos', () => {
    it('compara múltiplos IDs', async () => {
      globalThis.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve([mockPerfil, mockPerfil]),
      })

      const result = await compararCandidatos([1, 2])
      expect(globalThis.fetch).toHaveBeenCalledWith('/api/candidatos/comparar?ids=1,2')
      expect(result.length).toBe(2)
    })

    it('fallback para mock quando API falha', async () => {
      globalThis.fetch = vi.fn().mockRejectedValue(new Error('fail'))

      const result = await compararCandidatos([1, 2])
      expect(Array.isArray(result)).toBe(true)
      expect(result.length).toBe(2)
    })
  })

  describe('opcoesFiltros', () => {
    it('retorna cargos e estados', async () => {
      globalThis.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve({ cargos: ['Presidência'], estados: ['SP'] }),
      })

      const result = await opcoesFiltros()
      expect(result.cargos).toContain('Presidência')
      expect(result.estados).toContain('SP')
    })

    it('fallback para mock quando API falha', async () => {
      globalThis.fetch = vi.fn().mockRejectedValue(new Error('fail'))

      const result = await opcoesFiltros()
      expect(Array.isArray(result.cargos)).toBe(true)
      expect(result.cargos.length).toBeGreaterThan(0)
      expect(Array.isArray(result.estados)).toBe(true)
    })
  })
})
