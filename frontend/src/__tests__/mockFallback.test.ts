import { describe, it, expect } from 'vitest'
import { CANDIDATOS_MOCK, obterCandidatosMock, obterFiltrosMock, obterPerfilMock } from '../mockFallback'

describe('mockFallback', () => {
  describe('CANDIDATOS_MOCK', () => {
    it('tem pelo menos 10 candidatos', () => {
      expect(CANDIDATOS_MOCK.length).toBeGreaterThanOrEqual(10)
    })

    it('cada candidato tem campos obrigatórios', () => {
      for (const c of CANDIDATOS_MOCK) {
        expect(c.id).toBeGreaterThan(0)
        expect(c.nome).toBeTruthy()
        expect(typeof c.partido).toBe('string')
        expect(c.cargo).toBeTruthy()
        expect(c.estado).toBeTruthy()
        expect(c.indicadores).toBeDefined()
        expect(c.indicadores.processos_totais).toBeGreaterThanOrEqual(0)
        expect(c.indicadores.patrimonio_declarado).toBeGreaterThanOrEqual(0)
      }
    })

    it('IDs são únicos', () => {
      const ids = CANDIDATOS_MOCK.map(c => c.id)
      expect(new Set(ids).size).toBe(ids.length)
    })
  })

  describe('obterCandidatosMock', () => {
    it('retorna todos sem filtros', () => {
      const result = obterCandidatosMock({})
      expect(result.length).toBe(CANDIDATOS_MOCK.length)
    })

    it('filtra por cargo', () => {
      const result = obterCandidatosMock({ cargo: 'Presidência' })
      expect(result.length).toBeGreaterThan(0)
      for (const c of result) {
        expect(c.cargo).toBe('Presidência')
      }
    })

    it('filtra por estado', () => {
      const result = obterCandidatosMock({ estado: 'SP' })
      expect(result.length).toBeGreaterThan(0)
      for (const c of result) {
        expect(c.estado).toBe('SP')
      }
    })

    it('filtra por busca no nome', () => {
      const result = obterCandidatosMock({ busca: 'Lula' })
      expect(result.length).toBe(1)
      expect(result[0].nome).toContain('Lula')
    })

    it('filtra candidatos com processos', () => {
      const result = obterCandidatosMock({ tem_processos: 'true' })
      expect(result.length).toBeGreaterThan(0)
      for (const c of result) {
        expect(c.indicadores.processos_totais).toBeGreaterThan(0)
      }
    })

    it('retorna array vazio para cargo inexistente', () => {
      const result = obterCandidatosMock({ cargo: 'Vereador' })
      expect(result).toEqual([])
    })
  })

  describe('obterPerfilMock', () => {
    it('retorna null para ID inexistente', () => {
      const result = obterPerfilMock(9999)
      expect(result).toBeNull()
    })

    it('retorna perfil completo para ID existente', () => {
      const result = obterPerfilMock(1)
      expect(result).not.toBeNull()
      expect(result!.candidato.nome).toBeTruthy()
      expect(result!.secoes).toBeDefined()
      expect(result!.versao_schema).toBe('1.0')
    })

    it('perfil tem seções tipadas corretamente', () => {
      const result = obterPerfilMock(1)
      expect(Array.isArray(result!.secoes.processos)).toBe(true)
      expect(Array.isArray(result!.secoes.materias)).toBe(true)
      expect(Array.isArray(result!.secoes.bens_declarados)).toBe(true)
    })
  })

  describe('obterFiltrosMock', () => {
    it('retorna cargos e estados', () => {
      const result = obterFiltrosMock()
      expect(Array.isArray(result.cargos)).toBe(true)
      expect(Array.isArray(result.estados)).toBe(true)
      expect(result.cargos.length).toBeGreaterThan(0)
      expect(result.estados.length).toBeGreaterThan(0)
    })

    it('cargos estão definidos', () => {
      const result = obterFiltrosMock()
      // Sort alfabético — função usa .sort()
      const expectedCargos = ['Deputado Federal', 'Governador', 'Presidência', 'Senador']
      expect(result.cargos).toEqual(expectedCargos)
    })

    it('não tem duplicatas', () => {
      const result = obterFiltrosMock()
      expect(new Set(result.cargos).size).toBe(result.cargos.length)
      expect(new Set(result.estados).size).toBe(result.estados.length)
    })
  })
})
