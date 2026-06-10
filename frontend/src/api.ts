import type { Candidato, PerfilCompleto } from './types'
import { obterCandidatosMock, obterFiltrosMock, obterPerfilMock } from './mockFallback'

// Em produção, aponte para a URL do backend (ex: https://candidatai-api.onrender.com/api)
// Em dev, o proxy do Vite redireciona /api para localhost:8000
const BASE = import.meta.env.VITE_API_URL || '/api'

async function tryFetch<T>(url: string, fallback: () => T): Promise<T> {
  try {
    const res = await fetch(url)
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    const data = await res.json()
    return data
  } catch (err) {
    console.warn(`[API] Falha ao acessar ${url}:`, err, '— usando fallback')
    try {
      const result = fallback()
      console.log(`[API] Fallback retornou:`, Array.isArray(result) ? `${result.length} itens` : typeof result)
      return result
    } catch (fallbackErr) {
      console.error(`[API] ERRO no fallback:`, fallbackErr)
      throw fallbackErr
    }
  }
}

export async function listarCandidatos(params?: {
  cargo?: string; estado?: string; busca?: string
  tem_processos?: boolean; tem_condenacao?: boolean
  tem_doacao_investigada?: boolean; baixa_presenca?: boolean
}): Promise<Candidato[]> {
  return tryFetch(
    buildUrl('/candidatos', params),
    () => obterCandidatosMock(params as Record<string, string | boolean | undefined>)
  )
}

export async function perfilCandidato(id: number): Promise<PerfilCompleto> {
  return tryFetch(
    `${BASE}/candidatos/${id}`,
    () => {
      const p = obterPerfilMock(id)
      if (!p) throw new Error('Candidato não encontrado')
      return p
    }
  )
}

export async function compararCandidatos(ids: number[]): Promise<PerfilCompleto[]> {
  return tryFetch(
    `${BASE}/candidatos/comparar?ids=${ids.join(',')}`,
    () => ids.map(id => obterPerfilMock(id)).filter(p => p !== null) as PerfilCompleto[]
  )
}

export async function opcoesFiltros(): Promise<{ cargos: string[]; estados: string[] }> {
  return tryFetch(`${BASE}/filtros`, obterFiltrosMock)
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
