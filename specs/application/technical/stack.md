## Technical Stack

What PriceHorizon is built with, what it relies on in every environment, and where its code lives, the one home of each technology the technical specs use and its version: each part of the system, then what the parts rely on.

| Part | Language | Framework | Build Tool | Test Framework | Code Roots | Excluded |
|---|---|---|---|---|---|---|
| Web UI | TypeScript, on Node.js 24 LTS | React | Vite, npm, ESLint, Prettier | Vitest | `web` | `web/dist`, `web/node_modules` |
| Backend | C# 14, on .NET 10 LTS | ASP.NET Core, Aspire, Microsoft.Extensions.AI, DbUp, its SQL migrations the structured database's schema | .NET SDK, `dotnet format`, its build output under `artifacts` at the project root, outside every code root | xUnit | `backend` | |
| Acceptance tests | C# 14, on .NET 10 LTS | Reqnroll, each scenario tagged with the name of the product file holding it | .NET SDK, `dotnet format`, its build output under `artifacts` with the backend's | xUnit with Playwright for .NET, running the executable copies of the acceptance scenarios against the whole system Aspire's testing host starts | `acceptance-tests` | |
| Model serving | Python 3.13 | FastAPI | uv 0.9 or later, Ruff | pytest | `model-serving` | `model-serving/.venv` |
| Deployment | YAML | Helm 4 | Helm, an OCI container image built for each other part | Helm's lint and template checks | `deploy` | |

The backend holds the query, materialization and control plane services and the libraries they share, the model-call layer and the vault adapter among them; model serving holds the quantitative models the model registry versions; and deployment holds the chart an installation is installed and upgraded from.

| Technology | Kind | Purpose |
|---|---|---|
| PostgreSQL 17 | Database | The structured database: the harmonized quantitative foundation, reference and master data, pipeline and answer artifacts, and the audit log (`specs/application/technical/data-model.md § Core Data Model`) |
| pgvector | Database extension | The vector database, within PostgreSQL: the qualitative corpus, chunked and embedded, each business unit in its own namespace (`specs/application/technical/data-model.md § Core Data Model`) |
| Valkey | Cache | The question-intent cache |
| Temporal | Orchestration engine | Durable execution of the live path and the batch path (`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration`) |
| OpenBao | Secrets vault | Every credential the installation holds, the vault an installation uses unless it reaches one the customer already runs, through the vault adapter (`specs/application/technical/secrets-management.md § Secrets management`) |
| MLflow | Model registry | The versioned quantitative models and weighting rubrics (`specs/application/technical/model-registry.md § Model registry`) |
| vLLM | Model server | Acme AI's language models, hosted in the installation behind an OpenAI-compatible endpoint |
| OpenTelemetry Collector | Telemetry | Application traces and logs (`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Security and governance`) |
