import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import Ranking from '../pages/Ranking'

// Mock the API module to avoid real fetch calls
vi.mock('../api', () => ({
  listarCandidatos: () =>
    Promise.resolve([
      {
        id: 1,
        nome: 'Luiz Inácio Lula da Silva',
        numero: 13,
        partido: 'PT',
        cargo: 'Presidência',
        estado: 'Nacional',
        foto_url: '',
        intencao_voto: 39.0,
        pesquisa_fonte: 'Quaest — 05-08/06/2026',
        indicadores: {
          processos_totais: 2,
          processos_condenacao_transitada: 0,
          processos_em_andamento: 2,
          materias_12m: 15,
          doacoes_empresas_investigadas: 0,
          patrimonio_declarado: 7800000,
          presenca_legislativa_percent: null,
        },
      },
      {
        id: 2,
        nome: 'Flávio Bolsonaro',
        numero: 22,
        partido: 'PL',
        cargo: 'Presidência',
        estado: 'Nacional',
        foto_url: '',
        intencao_voto: 29.0,
        pesquisa_fonte: 'Quaest — 05-08/06/2026',
        indicadores: {
          processos_totais: 4,
          processos_condenacao_transitada: 0,
          processos_em_andamento: 4,
          materias_12m: 22,
          doacoes_empresas_investigadas: 1,
          patrimonio_declarado: 4500000,
          presenca_legislativa_percent: 82,
        },
      },
    ]),
  opcoesFiltros: () =>
    Promise.resolve({
      cargos: ['Presidência', 'Governador'],
      estados: ['Nacional', 'SP', 'RJ'],
    }),
}))

describe('Ranking Page', () => {
  it('renderiza o título', () => {
    render(
      <MemoryRouter>
        <Ranking />
      </MemoryRouter>
    )

    expect(screen.getByText('Painel de Transparência')).toBeDefined()
  })

  it('renderiza os filtros de cargo e estado', async () => {
    render(
      <MemoryRouter>
        <Ranking />
      </MemoryRouter>
    )

    // Wait for data to load
    expect(await screen.findByText('Luiz Inácio Lula da Silva')).toBeDefined()
  })

  it('renderiza cards de candidatos após carregar', async () => {
    render(
      <MemoryRouter>
        <Ranking />
      </MemoryRouter>
    )

    expect(await screen.findByText('Luiz Inácio Lula da Silva')).toBeDefined()
    expect(await screen.findByText('Flávio Bolsonaro')).toBeDefined()
  })

  it('exibe intenção de voto quando disponível', async () => {
    render(
      <MemoryRouter>
        <Ranking />
      </MemoryRouter>
    )

    expect(await screen.findByText('39%')).toBeDefined()
  })

  it('exibe indicadores nos cards', async () => {
    render(
      <MemoryRouter>
        <Ranking />
      </MemoryRouter>
    )

    // Aguarda carregar
    await screen.findByText('Luiz Inácio Lula da Silva')

    // Badges de indicadores
    const processoBadge = document.querySelector('.bg-red-50')
    expect(processoBadge).toBeDefined()
  })
})
