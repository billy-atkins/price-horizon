## Technical Stack

This section sets what PriceHorizon is built with, what it relies on in every environment, and where its code lives. It is the one home of each technology the technical specs use, and of that technology's version. It gives each part of the system, then what the parts rely on.

**Reference Key:** Part \
**Required:** Language, Framework, Build Tool, Test Framework, Code Roots

| Part | Language | Framework | Build Tool | Test Framework | Code Roots | Excluded |
|---|---|---|---|---|---|---|
| Web UI | TypeScript 7.0.2 on Node.js 26.13.1 | React 19.3.1 | Vite 8.4.0, npm 12.2.3, ESLint 10.15.0, Prettier 3.10.1 | Vitest 5.1.2 | `web` | `web/dist`, `web/node_modules` |
| Backend | C# at the selected SDK’s compiler default for `net11.0` | ASP.NET Core 11.0.0, Aspire.Hosting.AppHost 17.0.0, Microsoft.Extensions.AI 11.0.1, dbup-postgresql 7.0.1 for the SQL migrations that define the structured database schema | .NET SDK 11.0.100 with its bundled `dotnet format`, build output under `artifacts` at the project root | xunit.v3 4.0.3 with xunit.runner.visualstudio 4.0.1 and Microsoft.NET.Test.Sdk 18.12.0 for the VSTest filters | `backend` | |
| Acceptance tests | Same compiler and target as the backend | Reqnroll.xUnit.v3 3.3.4 with the product-file scenario tag | The backend SDK, formatter and artifacts root | The backend xUnit/VSTest stack with Microsoft.Playwright 1.65.1 and its matching browsers, with Aspire.Hosting.Testing from the AppHost release to start the whole system | `acceptance-tests` | |
| Model serving | CPython 3.15.2 | FastAPI 0.165.0 | uv 0.13.10, Ruff 0.17.6 | pytest 9.2.0 | `model-serving` | `model-serving/.venv` |
| Deployment | YAML 1.2.2, using Helm-compatible values | Helm 4.3.2 | Helm and OCI Image Specification 1.1.1 images for the application parts | Helm lint and template rendering | `deploy` | |

The backend holds the query, materialization and control plane services and the libraries they share, the model-call layer and the vault adapter among them. Model serving holds the quantitative models the model registry versions. Deployment holds the chart an installation is installed and upgraded from.

**Reference Key:** Technology \
**Required:** Kind, Purpose

| Technology | Kind | Purpose |
|---|---|---|
| PostgreSQL 19.0 | Database | The structured database: the harmonized quantitative foundation, reference and master data, pipeline and answer artifacts, and the audit log ([`specs/application/technical/data-model.md § Core Data Model`](/specs/application/technical/data-model.md#core-data-model)) |
| pgvector 0.8.7 | Database extension | The vector database, within PostgreSQL: the qualitative corpus, chunked and embedded, each business unit in its own namespace ([`specs/application/technical/data-model.md § Core Data Model`](/specs/application/technical/data-model.md#core-data-model)) |
| Valkey 9.2.1 | Cache | The question-intent cache |
| Temporal 1.32.2 | Orchestration engine | Durable execution of the live path and the batch path ([`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration`](/specs/application/technical/engineering-and-production-considerations.md#orchestration)) |
| OpenBao 2.7.3 | Secrets vault | Every credential the installation holds, the vault an installation uses unless it reaches one the customer already runs, through the vault adapter ([`specs/application/technical/secrets-management.md § Secrets management`](/specs/application/technical/secrets-management.md#secrets-management)) |
| MLflow 3.18.0 | Model registry | The versioned quantitative models and weighting rubrics ([`specs/application/technical/model-registry.md § Model registry`](/specs/application/technical/model-registry.md#model-registry)) |
| vLLM 0.34.0 | Model server | Acme AI's language models, hosted in the installation behind an OpenAI-compatible endpoint. The upstream release container supplies its own compatible interpreter. The quantitative FastAPI service uses the separate CPython pin in the parts table |
| OpenTelemetry Collector 0.166.0 | Telemetry | Application traces and logs ([`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Security and governance`](/specs/application/technical/engineering-and-production-considerations.md#security-and-governance)) |

### Web transport

In local development, CI and customer installations, PriceHorizon serves its web UI and APIs over HTTPS and uses HTTPS for outbound web requests, including calls between services and calls made by dependencies. Each client verifies the server’s certificate chain and hostname. It rejects a plaintext URL, a redirect to plaintext HTTP, or a failed certificate check before sending application data on that connection. Local and CI clients trust certificates issued for their own environment.

### Release selection

Compare stable releases for each part, shared service, environment tool and bundled component. A compatible release supports PriceHorizon’s required APIs, dependencies, hosts and deployment configuration. Compare eligible releases using supplier advisories and package registry affected ranges for that configuration. Count remaining exposure after applicable fixes or mitigations. Among releases with equal evidenced exposure, use release order.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Conditions:** Stable?, Receives security fixes?, Compatible?, Safer eligible release exists?, Newer equally secure eligible release exists?

| Stable? | Receives security fixes? | Compatible? | Safer eligible release exists? | Newer equally secure eligible release exists? | Selection |
|---|---|---|---|---|---|
| false | - | - | - | - | Ineligible |
| true | false | - | - | - | Ineligible |
| true | true | false | - | - | Ineligible |
| true | true | true | true | - | Prefer safer release |
| true | true | true | false | true | Prefer newer release |
| true | true | true | false | false | Select candidate |

Record the release, date, application constraint, advisory evidence and any compatibility or security reason to select an older version. Mark incomplete coverage as provisional even when a release is selected. Reassess on a relevant advisory or the end of security support. For customer-managed services and hosted runners, distinguish the interface or baseline PriceHorizon selects from the versions the operator controls.

The evidence records checks made on 26 November 2026. Registry results apply to the named direct package versions. Commit results come from the [OSV advisory index](https://osv.dev/). Each shipped container, including MLflow and vLLM, still requires an assessment of its image digest, base, interpreter and resolved packages. For language and image formats the revision identifies the interface, and the implementing tool or image supplies the security evidence.

**Table Name:** Stack Release Evidence \
**Reference Key:** Component \
**Required:** Release Evidence, Advisory Assessment

| Component | Release Evidence | Advisory Assessment |
|---|---|---|
| npm packages | [eslint](https://registry.npmjs.org/eslint/10.15.0), [npm](https://registry.npmjs.org/npm/12.2.3), [prettier](https://registry.npmjs.org/prettier/3.10.1), [react](https://registry.npmjs.org/react/19.3.1), [typescript](https://registry.npmjs.org/typescript/7.0.2), [vite](https://registry.npmjs.org/vite/8.4.0), [vitest](https://registry.npmjs.org/vitest/5.1.2) | No direct-version match in [npm audit](https://docs.npmjs.com/cli/v11/commands/npm-audit/#bulk-advisory-endpoint). Resolved dependencies remain provisional until the lockfile is checked. |
| NuGet packages | [aspire.hosting.apphost](https://www.nuget.org/packages/aspire.hosting.apphost/17.0.0), [aspire.hosting.testing](https://www.nuget.org/packages/aspire.hosting.testing/17.0.0), [dbup-postgresql](https://www.nuget.org/packages/dbup-postgresql/7.0.1), [microsoft.extensions.ai](https://www.nuget.org/packages/microsoft.extensions.ai/11.0.1), [microsoft.net.test.sdk](https://www.nuget.org/packages/microsoft.net.test.sdk/18.12.0), [microsoft.playwright](https://www.nuget.org/packages/microsoft.playwright/1.65.1), [reqnroll.xunit.v3](https://www.nuget.org/packages/reqnroll.xunit.v3/3.3.4), [xunit.runner.visualstudio](https://www.nuget.org/packages/xunit.runner.visualstudio/4.0.1), [xunit.v3](https://www.nuget.org/packages/xunit.v3/4.0.3) | No direct-version match in [NuGet vulnerability index](https://api.nuget.org/v3/vulnerabilities/index.json). Resolved dependencies remain provisional until the lockfile is checked. |
| PyPI packages | [fastapi](https://pypi.org/pypi/fastapi/0.165.0/json), [mlflow](https://pypi.org/pypi/mlflow/3.18.0/json), [pytest](https://pypi.org/pypi/pytest/9.2.0/json), [ruff](https://pypi.org/pypi/ruff/0.17.6/json), [uv](https://pypi.org/pypi/uv/0.13.10/json), [vllm](https://pypi.org/pypi/vllm/0.34.0/json) | No direct-version match in the vulnerabilities field of each linked PyPI release. Resolved dependencies remain provisional until the lockfile is checked. |
| .NET SDK, ASP.NET Core, C# compiler and dotnet format | [Microsoft release manifest](https://builds.dotnet.microsoft.com/dotnet/release-metadata/11.0/releases.json) | The stable SDK and runtime contain fixes for [GHSA-q7j6-px74-p2vw](https://github.com/advisories/GHSA-q7j6-px74-p2vw) and [GHSA-cpw3-h88j-9f6x](https://github.com/advisories/GHSA-cpw3-h88j-9f6x). The compiler and formatter follow SDK servicing. Package queries covered Windows and Linux x64. Other runtime identifiers are provisional. |
| Node.js | [Node release catalog](https://nodejs.org/dist/index.json) | The supplier marks the pin as a [security release](https://nodejs.org/en/blog/vulnerability/november-2026-security-releases). Its bundled npm installs the npm release selected for the Web UI. |
| CPython | [CPython release tag](https://github.com/python/cpython/tree/5e58eaad7c58df58dfa8ea549c87996e01dd1077) | Conditional on keeping a separate cookie jar for each origin that uses cookies. |
| Playwright browsers | [Microsoft.Playwright package](https://www.nuget.org/packages/Microsoft.Playwright/1.65.1) | Browser revisions follow the package manifest. Provisional for the browser binaries pending revision-specific supplier advisory checks. |
| PostgreSQL | [REL_19_0](https://github.com/postgres/postgres/tree/5c839a2a08b9b87a349be97371fac6c5a2873b10) | No OSV match for this commit. The [supplier advisory list](https://www.postgresql.org/support/security/) identifies earlier affected major lines. |
| pgvector | [v0.8.7](https://github.com/pgvector/pgvector/tree/f37c13f68b57d2c3472b2214fbcff699d6d34876) | No OSV match for this commit. The [release documents host compatibility](https://github.com/pgvector/pgvector/tree/v0.8.7). Extension-specific supplier advisory coverage is provisional. |
| Valkey | [9.2.1](https://github.com/valkey-io/valkey/tree/d1a551720f5feb1a2ff5b9a7b5e22520ae77eeef) | No OSV match for this commit. The pin follows the fixed build in [GHSA-3885-pq5f-788j](https://github.com/advisories/GHSA-3885-pq5f-788j). |
| Temporal | [v1.32.2](https://github.com/temporalio/temporal/tree/6d085822273f4336796e6959c73ab1d14a23eb77) | No OSV match for this commit. Separate supplier affected-range coverage is provisional. |
| OpenBao | [v2.7.3](https://github.com/openbao/openbao/tree/0439ef5812538733afb277b4445a54706edc1db7) | No OSV match for this commit. The pin follows the fixed build in [GHSA-5pmx-2p74-x478](https://github.com/advisories/GHSA-5pmx-2p74-x478). |
| OTel Collector | [v0.166.0](https://github.com/open-telemetry/opentelemetry-collector/tree/4b5ae43f8998fedf783b52917ff0ffb7cad1ed48) | No OSV match for this commit. The exporter helper fix is identified in [GHSA-cx3c-rmcx-ff35](https://github.com/advisories/GHSA-cx3c-rmcx-ff35). |
| Helm | [v4.3.2](https://github.com/helm/helm/tree/8346aaa55e7161f7c547212d0a87f01367976727) | No OSV match for this commit. The pin follows the corrected 4.x release in [GHSA-vmx8-mqv2-9gmg](https://github.com/advisories/GHSA-vmx8-mqv2-9gmg). |
| YAML and OCI image format | [YAML revision](https://yaml.org/spec/1.2.2/), [OCI release](https://github.com/opencontainers/image-spec/releases/tag/v1.1.1) | These are format revisions. Helm supplies the parser. Security coverage of each built image is provisional until its digest and packages are known. |

CPython 3.15.2 and the older supported stable lines fall within the supplier’s affected range for CVE-2026-124249 in `http.cookiejar`, Python’s cookie-handling module. For this release, each quantitative-service client that stores cookies, including clients supplied by dependencies, uses a separate cookie jar per origin (scheme, host and port), including when following redirects. HTTPS protects the connection. Separate jars prevent one origin’s response from deleting another origin’s cookies. A client requiring cross-origin cookie state needs a verified patched build before adoption. Reassess when a fixed stable release is available. [Python Software Foundation advisory](https://github.com/CVEProject/cvelistV5/blob/main/cves/2026/124xxx/CVE-2026-124249.json)
