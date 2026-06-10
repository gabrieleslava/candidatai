# Prompt de Engenharia — Painel de Transparência Eleitoral 2026

## 🎯 Objetivo

Projetar e implementar um **painel de transparência eleitoral** para as eleições brasileiras de 2026 que:

1. **Rankeia candidatos por intenção de voto** (pesquisas Datafolha, Quaest, Ipec)
2. **Exibe perfis informativos** com seções de evidências (processos, matérias, gastos, bens, histórico legislativo)
3. **NÃO atribui score moral**, nota ou julgamento — apenas dados brutos com fontes verificáveis
4. Permite **comparação lado a lado** entre candidatos
5. Oferece **filtros por cargo, estado e tipo de evidência**

> ⚠️ **Filosofia central:** O sistema não julga, não induz e não "ataca a índole" de candidatos. Ele expõe fatos públicos de forma organizada para que o eleitor tire suas próprias conclusões.

---

## 📊 Fontes de Dados Oficiais

| Fonte | Conteúdo | URL |
|---|---|---|
| **TSE — DivulgaCand** | Cadastro, bens declarados, situação | https://dadosabertos.tse.jus.br/ |
| **TSE — Prestação de Contas** | Doações, despesas, aprovação | https://dadosabertos.tse.jus.br/ |
| **DataJud (CNJ)** | Processos judiciais, instância, status | https://datajud.cnj.jus.br/ |
| **Câmara dos Deputados** | Votações, presença, projetos | https://dadosabertos.camara.leg.br/ |
| **Senado Federal** | Votações, proposições | https://dadosabertos.senado.leg.br/ |
| **Portal da Transparência** | Contratos, convênios | https://portaldatransparencia.gov.br/ |
| **Pesquisas de intenção de voto** | Datafolha, Quaest, Ipec, Genial/Quaest | Portais dos institutos (scraping/API) |
| **APIs de notícias** | Matérias sobre candidatos | GNews, NewsAPI, scraping |

---

## 🧭 Estrutura do Sistema

```
┌─────────────────────────────────────────────────────┐
│                   PAINEL PRINCIPAL                   │
│                                                     │
│  [Filtros: Cargo ▼  Estado ▼  Evidências □]         │
│  [Buscar por nome/partido]                          │
│                                                     │
│  ┌─────────────────────────────────────────────┐  │
│  │ Ranking por intenção de voto (descendente)   │  │
│  │                                             │  │
│  │  1º Maria Souza — 23% — Presidência        │  │
│  │  2º Carlos Lima — 18% — Presidência        │  │
│  │  3º João Silva — 12% — Dep. Federal SP      │  │
│  │  4º Ana Costa — 9% — Governador RJ         │  │
│  └─────────────────────────────────────────────┘  │
│                                                     │
│  [ ] Comparar selecionados    [ ] Exportar CSV       │
└─────────────────────────────────────────────────────┘
```

```
┌─────────────────────────────────────────────────────┐
│                   PERFIL DO CANDIDATO                   │
│                                                     │
│  Cabeçalho: nome, foto, partido, cargo, estado,     │
│  intenção de voto (% + fonte da pesquisa)            │
│                                                     │
│  ┌─────────────────────────────────────────────┐  │
│  │ 🏷️ Indicadores resumo (tags)               │  │
│  │ • 3 processos judiciais                       │  │
│  │ • 1 condenação transitada em julgado          │  │
│  │ • 5 matérias nos últimos 12 meses            │  │
│  │ • 2 doações de empresas investigadas           │  │
│  │ • Patrimônio: R$ 463.000                       │  │
│  │ • Presença legislativa: 92%                    │  │
│  └─────────────────────────────────────────────┘  │
│                                                     │
│  Abas/Seções:                                      │
│  • Processos judiciais → lista com status + fonte   │
│  • Matérias na mídia → títulos + links             │
│  • Gastos de campanha → total + maiores doadores    │
│  • Bens declarados → lista + valores               │
│  • Histórico legislativo → presença + projetos     │
│  • Contratos governamentais → lista + valores       │
│                                                     │
│  Cada item: [fonte verificável] + [data]           │
└─────────────────────────────────────────────────────┘
```

---

## 🔍 Filtros Disponíveis

### 1. Cargo
- Presidência da República (nacional)
- Governador (por estado)
- Senador (por estado)
- Deputado Federal (por estado)
- Deputado Estadual (por estado)

### 2. Estado
- Nacional (todos os estados)
- SP, RJ, MG, BA, RS, PR, SC, GO, CE, PE, DF, etc.

### 3. Evidências (mostrar apenas candidatos que possuam)
- Processos judiciais em andamento
- Condenações transitadas em julgado
- Matérias na mídia (qualquer uma)
- Doações de empresas investigadas por corrupção
- Patrimônio declarado acima de X
- Baixa presença legislativa (< 70%)
- Contratos com governo nos últimos 6 meses

---

## 📋 Regras de Exibição — NEUTRALIDADE OBRIGATÓRIA

### ❌ PROIBIDO

| Ação | Exemplo do que NÃO fazer |
|---|---|
| Atribuir score moral | "Candidato nota 12/100", "índice de confiança" |
| Linguagem acusatória | "é corrupto", "comprovadamente desviou" |
| Inferência sem fonte | Afirmar fato não documentado em fonte oficial |
| Classificar matérias | "3 matérias negativas" — não cabe ao sistema julgar tom |
| Ocultar contexto | Mostrar condenação sem indicar instância e status |

### ✅ OBRIGATÓRIO

| Ação | Exemplo do que FAZER |
|---|---|
| Linguagem descritiva | "responde a processo", "consta em matéria", "declara patrimônio de" |
| Citar fonte em cada dado | Link direto para DataJud, TSE, portal de notícias |
| Diferenciar instâncias | "1ª instância", "TRF (2ª instância)", "STJ", "transitada em julgado" |
| Exibir status processual completo | Tipo de ação + instância + status + data + link |
| Separar fato de opinião | Matérias exibidas como título + link, sem classificação de "tom" |
| Indicar data de atualização | `data_atualizacao` em cada registro |
| Normalizar nomes | `unidecode(nome).lower().strip()` para buscas e deduplicação |

---

## 🗃️ Formato de Saída — JSON (sem score moral)

```json
{
  "candidato": {
    "nome": "string",
    "numero": "int or null",
    "partido": "string",
    "cargo": "string",
    "estado": "string (UF)",
    "intencao_voto": "float or null",
    "pesquisa_fonte": "string (instituto + data)",
    "foto_url": "string or null",
    "indicadores": {
      "processos_totais": "int",
      "processos_condenacao_transitada": "int",
      "processos_em_andamento": "int",
      "materias_12m": "int",
      "doacoes_empresas_investigadas": "int",
      "patrimonio_declarado": "int (BRL, centavos)",
      "presenca_legislativa_percent": "int (0-100) or null"
    }
  },
  "secoes": {
    "processos": [
      {
        "tipo": "string (ex: Improbidade administrativa, Propaganda irregular)",
        "instancia": "string (ex: TRE-SP, TRF-3, TJ-RJ, STJ)",
        "status": "string (em_andamento | transitada_em_julgado | arquivado | absolvido)",
        "data_inicio": "AAAA-MM-DD or null",
        "data_decisao": "AAAA-MM-DD or null",
        "fonte": "string (URL)",
        "observacao": "string or null"
      }
    ],
    "materias": [
      {
        "titulo": "string",
        "veiculo": "string",
        "data": "AAAA-MM-DD",
        "url": "string (URL)",
        "fonte_api": "string"
      }
    ],
    "gastos_campanha": {
      "total_declarado": "int (BRL, centavos)",
      "maiores_doadores": [
        {
          "nome": "string",
          "valor": "int",
          "cpf_cnpj": "string or null",
          "fonte": "string (URL)"
        }
      ],
      "fonte": "string"
    },
    "bens_declarados": [
      {
        "descricao": "string",
        "valor": "int (BRL, centavos)",
        "tipo": "string (Imóvel, Veículo, Financeiro, Outro)",
        "fonte": "string (URL)"
      }
    ],
    "historico_legislativo": {
      "presenca_percent": "int or null",
      "projetos_propostos": "int",
      "votos_em_pautas_politicas": "int",
      "fonte": "string (URL)"
    },
    "contratos_governo": [
      {
        "empresa": "string",
        "contrato_numero": "string",
        "valor": "int",
        "orgao_contratante": "string",
        "data_assinatura": "AAAA-MM-DD",
        "fonte": "string (URL)"
      }
    ]
  },
  "data_atualizacao": "AAAA-MM-DD",
  "versao_schema": "1.0"
}
```

---

## ⚙️ Fluxo de Execução

```
1. INGESTÃO DE DADOS
   a) Buscar lista de pré-candidatos/candidatos registrados no TSE 2026
   b) Para cada candidato:
      - Consultar DataJud → processos
      - Consultar TSE → bens, contas
      - Consultar API de notícias → matérias
      - Consultar Câmara/Senado → histórico legislativo (se aplicável)
      - Consultar Portal da Transparência → contratos
      - Consultar agregador de pesquisas → intenção de voto
   c) Normalizar nomes (unidecode + fuzzy matching)
         │
         ▼
2. PROCESSAMENTO
   a) Construir indicadores resumo (contadores booleanos/inteiros)
   b) Montar seções de evidências com links de fonte
   c) NÃO calcular nenhum score moral
   d) Registrar data_atualizacao
         │
         ▼
3. ARMAZENAMENTO
   a) Banco de dados (PostgreSQL ou SQLite) com cache
   b) JSON exportável por candidato
         │
         ▼
4. APRESENTAÇÃO (Frontend)
   a) Tela principal: ranking por intenção de voto + filtros
   b) Perfil do candidato: seções de evidências com tooltips
      (tooltip explica o que significa "TRF-3", "transitada em julgado", etc.)
   c) Tela de comparação: lado a lado, mesma estrutura
         │
         ▼
5. ATUALIZAÇÃO
   a) Cron job semanal para refrescar DataJud e matérias
   b) Cron job mensal para pesquisas de intenção de voto
```

---

## 🛠️ Stack Técnica Recomendada

| Camada | Ferramenta |
|---|---|
| **Backend** | Python 3.10+ (FastAPI ou Flask) |
| **Coleta de dados** | `requests`, `pandas`, `unidecode`, `rapidfuzz` |
| **Banco de dados** | PostgreSQL (produção) ou SQLite (protótipo) |
| **Frontend** | React + Material UI (ou Streamlit para protótipo rápido) |
| **APIs de notícias** | GNews API, NewsAPI, ou scraping com `BeautifulSoup` |
| **Agendamento** | Celery + Redis ou cron job |
| **Deploy** | Render, Vercel, AWS EC2 |

---

## 📝 Exemplo de Prompt para o LLM Desenvolvedor

```
Você é um engenheiro de software sênior. Sua tarefa é implementar o backend de um painel de transparência eleitoral para 2026 seguindo ESTAS REGRAS:

1. NUNCA atribua score moral, nota ou julgamento a candidatos.
2. O rankeamento PRINCIPAL é por intenção de voto (pesquisa mais recente).
3. Cada candidato tem um perfil com SEÇÕES DE EVIDÊNCIAS (processos, matérias, gastos, bens, histórico legislativo, contratos).
4. Cada evidência DEVE ter link para fonte oficial verificável.
5. Use linguagem puramente descritiva ("responde a processo", "é citado em matéria").
6. Implemente os filtros: cargo, estado, evidências.
7. Use o schema JSON especificado neste prompt.
8. Foque nos candidatos das eleições de 2026 (presidência, governador, senador, deputado federal).

Entregue:
  a) Um script Python que coleta dados de pelo menos 2 fontes oficiais
  b) A função que monta o JSON no formato especificado
  c) Um endpoint REST (FastAPI) que retorna o perfil de um candidato por nome/cargo/estado
```

---

## 📌 Checklist de Validação

Antes de publicar, verificar:

- [ ] Nenhum score moral aparece em nenhuma tela
- [ ] Todo dado tem link para fonte oficial
- [ ] Instância e status processual estão explícitos em cada processo
- [ ] Matérias exibidas sem classificação de "tom"
- [ ] Rankeamento default é por intenção de voto (não por qualquer outro critério)
- [ ] Filtros funcionam por cargo, estado e evidências
- [ ] Dados atualizados com data visível
- [ ] Normalização de nomes evita duplicatas
- [ ] Tooltip em cada indicador explica o termo técnico (ex.: "O que é TRF?", "O que significa transitada em julgado?")

---

## 🧠 Notas para o LLM

1. **Se não encontrar dados de intenção de voto** para um candidato, exibir `intencao_voto: null` e rankear no final da lista.
2. **Se houver múltiplas pesquisas**, priorizar a mais recente e indicar instituto + data em `pesquisa_fonte`.
3. **Quando o DataJud retornar múltiplos processos com mesmo número**, deduplicar por `processo_id`.
4. **Para scraping de notícias**, limitar a 10 matérias mais recentes por candidato (últimos 24 meses).
5. **Todos os endpoints de API** devem ter tratamento de erro (timeout, rate limit, dados ausentes).
6. **Logs**: registrar cada falha de consulta a API com timestamp para depuração.
