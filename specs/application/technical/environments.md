## Environments

Where PriceHorizon is built, tested and run, each environment stating only what differs from the technical stack (`specs/application/technical/stack.md § Technical Stack`).

### Local

**Kind:** local

**What it is for —** a developer, or an agent writing code, builds, runs and tests the whole system on their own machine.

**Where it runs —** a developer's own machine, running Windows, macOS or Linux, every dependency in a container.

**What differs from the stack —** Ollama serves Acme AI's language models in place of vLLM; Keycloak stands in for the customer's own identity provider, over OIDC; Docker runs every dependency as a container, Aspire's host starting them; and no kind of model call reaches a frontier model provider unless the developer's own configuration names one.

**What data it holds —** synthetic data only, never a customer's.

| Tool | Version | Purpose | Windows | macOS | Linux |
|---|---|---|---|---|---|
| .NET SDK | the stack's | Builds, runs and tests the backend and the acceptance tests | `winget install Microsoft.DotNet.SDK.10` | `curl -sSL https://dot.net/v1/dotnet-install.sh \| bash -s -- --channel 10.0` | `curl -sSL https://dot.net/v1/dotnet-install.sh \| bash -s -- --channel 10.0` |
| fnm | latest | Installs and selects the stack's Node.js version | `winget install Schniz.fnm`, then `fnm install 24` | `brew install fnm`, then `fnm install 24` | `curl -fsSL https://fnm.vercel.app/install \| bash`, then `fnm install 24` |
| uv | the stack's | Installs the stack's Python version and runs model serving | `winget install astral-sh.uv` | `brew install uv` | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Docker | latest | Runs every dependency as a container | `winget install Docker.DockerDesktop` | `brew install --cask docker` | Docker Engine, as `https://docs.docker.com/engine/install` gives for the distribution |
| PowerShell | 7 | Runs Playwright's browser installer | `winget install Microsoft.PowerShell` | `brew install --cask powershell` | PowerShell 7, as `https://aka.ms/powershell` gives for the distribution |
| Helm | the stack's | Checks the deployment chart | `winget install Helm.Helm` | `brew install helm` | the Helm 4 release from `https://get.helm.sh` |

| Task | Command | Does |
|---|---|---|
| Restore | `dotnet restore backend`, `dotnet restore acceptance-tests`, `npm ci --prefix web`, `uv --directory model-serving sync` | Installs every part's dependencies |
| Build | `dotnet build backend`, `dotnet build acceptance-tests`, `npm run build --prefix web` | Builds the backend, the acceptance tests and the web UI |
| Lint | `dotnet format backend --verify-no-changes`, `dotnet format acceptance-tests --verify-no-changes`, `npm run lint --prefix web`, `uv --directory model-serving run ruff check` | Checks every part's format and lint rules |
| Test | `dotnet test backend --filter "Category!=golden-question"`, `npm test --prefix web`, `uv --directory model-serving run pytest` | Runs every part's own tests, the golden questions apart |
| Test, targeted | `dotnet test backend --filter "<filter>"`, `npm test --prefix web -- <pattern>`, `uv --directory model-serving run pytest -k "<expression>"` | Runs only the tests the argument selects: a test filter for the backend, a file pattern for the web UI, an expression for model serving |
| Golden questions | `dotnet test backend --filter "Category=golden-question"` | Runs the golden-question suite (`specs/application/technical/evaluation-and-monitoring.md § Evaluation and monitoring`) against the models the system serves |
| Golden questions, targeted | `dotnet test backend --filter "Category=golden-question&Name~<name>"` | Runs only the golden questions whose name holds the argument |
| Browsers | `pwsh artifacts/bin/PriceHorizon.AcceptanceTests/debug/playwright.ps1 install --with-deps` | Installs the browsers the acceptance tests drive, once the acceptance tests are built |
| Acceptance test | `dotnet test acceptance-tests` | Runs every acceptance scenario against the whole system, started in containers |
| Acceptance test, targeted | `dotnet test acceptance-tests --filter "Category=<tag>"` | Runs only the scenarios carrying the tag, the name of the product file holding them |
| Chart check | `helm lint deploy` | Checks the deployment chart |
| Images | `dotnet publish backend -t:PublishContainer`, `docker build web`, `docker build model-serving` | Builds each part's container image |
| Run | `dotnet run --project backend/PriceHorizon.AppHost` | Starts the whole system, with its dashboard of traces and logs |

### Continuous Integration

**Kind:** integration

**What it is for —** every change is built, linted and tested before it merges.

**Where it runs —** GitHub Actions' hosted runners: Windows, macOS and Linux.

**What differs from the stack —** GitHub Actions runs it; on its Linux runner, the only one running Linux containers, Docker runs every dependency, Keycloak stands in for the customer's identity provider, and Ollama serves a small language model on the runner's CPU, within its memory, since hosted runners have no GPU.

**What data it holds —** synthetic data only, as the local environment does.

| Task | Command | Does | Runs On |
|---|---|---|---|
| Restore, build, lint and test | the local environment's Restore, Build, Lint and Test commands | Builds, lints and tests every part | Windows, macOS, Linux |
| Acceptance test | the local environment's Browsers and Acceptance test commands | Runs every acceptance scenario against the whole system, started in containers | Linux |
| Golden questions | the local environment's Golden questions command | Runs the golden-question suite on every change, a model, prompt template or data pipeline version among them, so every assertion holds before that version ships (`specs/application/technical/evaluation-and-monitoring.md § Evaluation and monitoring`) | Linux |
| Chart check and images | the local environment's Chart check and Images commands | Checks the chart once, its result the same on every operating system, and builds the images, which are Linux containers | Linux |

### Customer Installation

**Kind:** production

**What it is for —** the customer's own people ask questions and administer PriceHorizon, in the installation `specs/application/product/platform-and-compliance-operations/deployment-topology.md § Deployment Topology` describes.

**Where it runs —** the customer's own Kubernetes cluster, inside their own environment, installed and upgraded from the deployment chart.

**What differs from the stack —** Kubernetes runs it; the customer's own identity provider signs people in; the vault the customer already runs, HashiCorp Vault or AWS Secrets Manager, holds its credentials through the vault adapter (`specs/application/technical/secrets-management.md § Secrets management`), the stack's otherwise; and the Anthropic API or the OpenAI API serves only the kinds of model call the installation's configuration names (`specs/application/technical/model-registry.md § Model registry`).

**What data it holds —** the customer's own data, which stays inside their environment, save what the client chooses to let a frontier model provider see (`specs/application/product/platform-and-compliance-operations/deployment-topology.md § Deployment Topology § Frontier Models`).
