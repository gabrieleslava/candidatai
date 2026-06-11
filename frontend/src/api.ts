import type { Candidato, PerfilCompleto } from './types'

const BASE = import.meta.env.VITE_API_URL || '/api'

export async function listarCandidatos(params?: {
  cargo?: string; estado?: string; busca?: string
  tem_processos?: boolean; tem_condenacao?: boolean
  tem_doacao_investigada?: boolean; baixa_presenca?: boolean
}): Promise<Candidato[]> {
  const url = buildUrl('/candidatos', params)
  const res = await fetch(url)
  if (!res.ok) throw new Error(`HTTP ${res.status}`)
  return res.json()
}

export async function perfilCandidato(id: number): Promise<PerfilCompleto> {
  const res = await fetch(`${BASE}/candidatos/${id}`)
  if (!res.ok) throw new Error(`HTTP ${res.status}`)
  return res.json()
}

export async function compararCandidatos(ids: number[]): Promise<PerfilCompleto[]> {
  const res = await fetch(`${BASE}/candidatos/comparar?ids=${ids.join(',')}`)
  if (!res.ok) throw new Error(`HTTP ${res.status}`)
  return res.json()
}

export async function opcoesFiltros(): Promise<{ cargos: string[]; estados: string[] }> {
  const res = await fetch(`${BASE}/filtros`)
  if (!res.ok) throw new Error(`HTTP ${res.status}`)
  return res.json()
}

function buildUrl(path: string, params?: Record<string, unknown>): string {
  const sp = new URLSearchParams()
  if (params) {
    for (const [k, v] of Object.entries(params)) {
      if (v !== undefined && v !== '') sp.set(k, String(v))
    }
  }
  const qs = sp.toString()
  return `${BASE}${path}${qs ? `?${qs}` : ''}`
}
