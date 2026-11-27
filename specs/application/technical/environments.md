## Environments

These are the environments where PriceHorizon is built, tested and run. Each environment states only what differs from the technical stack ([`specs/application/technical/stack.md § Technical Stack`](/specs/application/technical/stack.md#technical-stack)).

### Local

**Kind:** local

**What it is for.** A developer, or an agent writing code, builds, runs and tests the whole system on their own machine.

**Where it runs.** A developer's own machine, running Windows, macOS or Linux, with every dependency in a container.

**What differs from the stack.** Ollama 0.40.18 serves Acme AI's language models in place of vLLM. Keycloak 26.8.2 stands in for the customer's own identity provider, over OIDC. Docker runs every dependency as a container, and Aspire's host starts them. No kind of model call reaches a frontier model provider unless the developer's own configuration names one.

**What data it holds.** Synthetic data only, never a customer's.

**Reference Key:** Tool \
**Required:** Version, Purpose, Windows, macOS, Linux

| Tool | Version | Purpose | Windows | macOS | Linux |
|---|---|---|---|---|---|
| .NET SDK | the stack’s | Build and test .NET parts | Run Microsoft’s `dotnet-install.ps1 -Version <sdk>` | Run Microsoft’s `dotnet-install.sh --version <sdk>` | Run Microsoft’s `dotnet-install.sh --version <sdk>` |
| fnm | 1.39.0 | Select Node.js | Extract fnm-windows.zip from the [tagged release](https://github.com/Schniz/fnm/releases/tag/v1.39.0) and add fnm to PATH | Extract fnm-macos.zip from the tagged release and add fnm to PATH | Extract the tagged fnm-linux or fnm-arm64 archive for the host and add fnm to PATH |
| uv | the stack’s | Select Python and project packages | Run `uv-installer.ps1` from the [pinned uv release](https://github.com/astral-sh/uv/releases/tag/0.13.10) | Run that release’s `uv-installer.sh` | Run that release’s `uv-installer.sh` |
| Docker Desktop | 4.100.1 | Run Linux containers on developer hosts | Use the verified Windows installer retained for this release | Use the verified DMG retained for this release and Mac CPU | Use the Engine row |
| Docker Engine | 29.10.1 | Run Linux containers natively | Use the Desktop row | Use the Desktop row | Select the exact Engine and CLI package builds for this release and distribution from Docker’s package repository |
| PowerShell | 7.7.0 | Run the Playwright installer | Install the tagged MSI for the host CPU | Install the tagged macOS pkg for the host CPU | Install the distribution package or Linux release archive for the host CPU |
| Helm | the stack’s | Verify the chart | Extract the Windows archive for the [pinned Helm release](https://github.com/helm/helm/releases/tag/v4.3.2) | Extract the Darwin archive for the named release | Extract the Linux archive for the named release |

Choose the asset for the host OS and CPU from the named release. Substitute the exact versions from the tool or stack table for command placeholders. Verify the reported versions before running project tasks. On Windows and macOS, verify the Docker Desktop build as well as the bundled server version against the Engine advisory.

Before selecting a Docker Desktop build for developer use, obtain each supported Windows installer and macOS DMG from the [Docker Desktop release notes](https://docs.docker.com/desktop/release-notes/). Verify each against Docker’s published SHA-256 checksum and retain the installer and checksum by release, OS and CPU in the project’s internal artifact store for the life of the pin. A fresh host retrieves the matching artifact and verifies its digest before installation. Reassess the selection if a verified artifact is unavailable.

Activate fnm for the shell, run `fnm install <node>` and `fnm use <node>`, then install the selected npm with `npm install --global npm@<npm>`. Verify `node --version` and `npm --version`. Run `uv python install <python>` and select that interpreter in the model-serving project. The web test script invokes Vitest. The .NET projects select the pinned SDK and VSTest runner. The pinned Playwright package’s installer selects its matching browser revisions.

**Table Name:** Local Tasks \
**Reference Key:** Task \
**Required:** Command, Does

| Task | Command | Does |
|---|---|---|
| Restore | `dotnet restore backend`, `dotnet restore acceptance-tests`, `npm ci --prefix web`, `uv --directory model-serving sync --locked` | Installs every part's dependencies |
| Build | `dotnet build backend`, `dotnet build acceptance-tests`, `npm run build --prefix web` | Builds the backend, the acceptance tests and the web UI |
| Lint | `dotnet format backend --verify-no-changes`, `dotnet format acceptance-tests --verify-no-changes`, `npm run lint --prefix web`, `uv --directory model-serving run ruff check` | Checks every part's format and lint rules |
| Test | `dotnet test backend --filter "Category!=golden-question"`, `npm test --prefix web -- --run`, `uv --directory model-serving run pytest` | Runs every part's own tests, the golden questions apart |
| Test, targeted | `dotnet test backend --filter "(Category!=golden-question)&(<filter>)"`, `npm test --prefix web -- --run <pattern>`, `uv --directory model-serving run pytest -k "<expression>"` | Selects ordinary backend tests with a VSTest expression, Vitest tests in run mode with a file pattern, and Python tests with a pytest expression |
| Golden questions | `dotnet test backend --filter "Category=golden-question"` | Runs the golden-question suite ([`specs/application/technical/evaluation-and-monitoring.md § Evaluation and monitoring`](/specs/application/technical/evaluation-and-monitoring.md#evaluation-and-monitoring)) against the models the system serves |
| Golden questions, targeted | `dotnet test backend --filter "(Category=golden-question)&(FullyQualifiedName~<name>)"` | Runs golden tests whose fully qualified name contains the argument |
| Browsers | `pwsh artifacts/bin/PriceHorizon.AcceptanceTests/debug/playwright.ps1 install --with-deps` | Installs the browsers the acceptance tests drive, once the acceptance tests are built |
| Acceptance test | `dotnet test acceptance-tests` | Runs every acceptance scenario against the whole system, started in containers |
| Acceptance test, targeted | `dotnet test acceptance-tests --filter "Category=<tag>"` | Runs only the scenarios carrying the tag, the name of the product file holding them |
| Chart check | `helm lint deploy`, `helm template pricehorizon deploy` | Lints the chart and renders the installation manifests |
| Images | `dotnet publish backend -t:PublishContainer`, `docker build web`, `docker build model-serving` | Builds each part's container image |
| Run | `dotnet run --project backend/PriceHorizon.AppHost` | Starts the whole system, with its dashboard of traces and logs |

#### Environment release evidence

The supplier checks for environment-specific components are dated 26 November 2026. Local and CI use the same substitute images. The release-selection rule in [`specs/application/technical/stack.md § Technical Stack § Release selection`](/specs/application/technical/stack.md#release-selection) applies to environment tools and images.

**Table Name:** Environment Release Evidence \
**Reference Key:** Component \
**Required:** Release Evidence, Advisory Assessment

| Component | Release Evidence | Advisory Assessment |
|---|---|---|
| fnm | [v1.39.0](https://github.com/Schniz/fnm/tree/d2555b46362ad8888213b76822631561371ce199) | No OSV match for this commit. Separate supplier advisory coverage is provisional. |
| PowerShell | [v7.7.0](https://github.com/PowerShell/PowerShell/tree/5c95ed61735c05eb99543aabf196529b5f267602) | No OSV match for this commit. The published [supplier advisories](https://github.com/PowerShell/PowerShell/security/advisories) also cover earlier releases. |
| Docker Desktop | [Desktop release and installers](https://docs.docker.com/desktop/release-notes/#41001) | Provisional on Windows and macOS. The [Desktop announcements](https://docs.docker.com/security/security-announcements/) and this release entry do not establish the shipped Engine fix. Confirm the bundled server version or a vendor backport for [GHSA-vfmq-r373-x89f](https://github.com/advisories/GHSA-vfmq-r373-x89f) before accepting this build. |
| Docker Engine | [docker-v29.10.1](https://github.com/moby/moby/tree/54cd494d0b39abfc7a958fcc876f706271f8b909) | No OSV match for this commit. The native Linux server pin contains the fix for [GHSA-vfmq-r373-x89f](https://github.com/advisories/GHSA-vfmq-r373-x89f). |
| Ollama | [v0.40.18](https://github.com/ollama/ollama/tree/924cc286cc592f49c481fa84e15fa60dbc75989e) | No OSV match for this commit. The local and CI container base is provisional pending an image digest. |
| Keycloak | [26.8.2](https://github.com/keycloak/keycloak/tree/e514445f9dcdabc5bdcf67cab56c1e49655de067) | No OSV match for this commit. The server pin is outside the affected ranges of [GHSA-6qm4-x97f-55fh](https://github.com/advisories/GHSA-6qm4-x97f-55fh). The local and CI image base is provisional pending a digest. |
| Kubernetes | [v1.37.3](https://github.com/kubernetes/kubernetes/tree/f81a9c5f95912fd97b7c8aa4966301aeae84a253) | No OSV match for this commit. This is the chart compatibility target. The customer owns the deployed control plane and node patch levels. Supplier coverage for the deployed cluster is provisional until its versions are known. |

### Continuous Integration

**Kind:** integration

**What it is for.** Every change is built, linted and tested before it merges.

**Where it runs.** GitHub Actions' hosted runners: Windows, macOS and Linux.

**What differs from the stack.** GitHub maintains the runner operating systems. Each job selects and verifies the same project tool versions as Local. The Linux jobs that run containers select and verify the native Docker Engine version in the Local tool table. They use Local’s Keycloak and Ollama release images with a small CPU-served language model that fits the runner’s memory.

**What data it holds.** Synthetic data only, as the local environment does.

**Table Name:** CI Tasks \
**Reference Key:** Task \
**Required:** Command, Does, Runs On

| Task | Command | Does | Runs On |
|---|---|---|---|
| Restore, build, lint and test | [`§ Environments § Local [Local Tasks.Task: Restore]`](#local), [`§ Environments § Local [Local Tasks.Task: Build]`](#local), [`§ Environments § Local [Local Tasks.Task: Lint]`](#local), [`§ Environments § Local [Local Tasks.Task: Test]`](#local) | Restore the selected dependencies and run the backend, web and Python unit suites | Windows, macOS, Linux |
| Targeted unit tests | [`§ Environments § Local [Local Tasks.Task: Test, targeted]`](#local) | Supply a known ordinary test filter, a matching web test-file pattern and a matching pytest expression. Confirm each invocation executed at least one selected test | Windows, macOS, Linux |
| Golden questions | [`§ Environments § Local [Local Tasks.Task: Golden questions]`](#local), [`§ Environments § Local [Local Tasks.Task: Golden questions, targeted]`](#local) | Run the full model-backed suite, then select a known golden test by its name | Linux |
| Acceptance tests | [`§ Environments § Local [Local Tasks.Task: Browsers]`](#local), [`§ Environments § Local [Local Tasks.Task: Acceptance test]`](#local), [`§ Environments § Local [Local Tasks.Task: Acceptance test, targeted]`](#local) | Install the matching browsers after Build. Run all scenarios, then select a known product-file tag | Linux |
| Chart and images | [`§ Environments § Local [Local Tasks.Task: Chart check]`](#local), [`§ Environments § Local [Local Tasks.Task: Images]`](#local) | Lint and render the deployment chart and build the Linux container images | Linux |

The Linux acceptance suite checks the web transport rules in [`specs/application/technical/stack.md § Technical Stack § Web transport`](/specs/application/technical/stack.md#web-transport). A request to a trusted HTTPS endpoint succeeds. A plaintext endpoint, a downgrade redirect and a server with an untrusted or mismatched certificate each receive no application data. The model-serving unit suite checks that two HTTPS origins retain separate cookie state across redirects.

#### Targeted run evidence

CI records the exact selector, one executed test and one excluded control from the same suite for each targeted invocation on each assigned runner. For the web run, record the Vitest file pattern and a test in that file, with a test in another file as the control. For Python, record the pytest -k expression and the selected and deselected node IDs. Resolve those identities from tests present in that checkout. For example, a backend filter matching both an ordinary test and a golden question runs only the ordinary test on the unit runners. Selecting the golden test by name on Linux runs it against the model.

Evaluate each targeted invocation on each assigned runner. The matching test and the unrelated control must belong to the same full suite. The control qualifies as excluded when it is absent from the executed selection. An invocation with an error fails the job.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Conditions:** Matching test executed?, Unrelated control excluded?

| Matching test executed? | Unrelated control excluded? | Targeted evidence passes? |
|---|---|---|
| false | - | false |
| true | false | false |
| true | true | true |

### Customer Installation

**Kind:** production

**What it is for.** The customer's own people ask questions and administer PriceHorizon, in the installation [`specs/application/product/platform-and-compliance-operations/deployment-topology.md § Deployment Topology`](/specs/application/product/platform-and-compliance-operations/deployment-topology.md#deployment-topology) describes.

**Where it runs.** The customer's own Kubernetes cluster, inside their environment. The deployment chart targets Kubernetes 1.37.3 for compatibility. The customer manages the deployed control plane and node patch levels.

**What differs from the stack.** The customer's own identity provider supplies federated identities. Where the customer already runs HashiCorp Vault or AWS Secrets Manager, that vault holds PriceHorizon's credentials through the vault adapter ([`specs/application/technical/secrets-management.md § Secrets management`](/specs/application/technical/secrets-management.md#secrets-management)). Otherwise the stack's vault holds them. The customer selects any external identity or vault server release compatible with the installation’s interfaces. For permitted external model calls, the client’s infrastructure team selects the Anthropic API or OpenAI API and dated model version for each call kind ([`specs/application/technical/model-registry.md § Model registry`](/specs/application/technical/model-registry.md#model-registry)).

**What data it holds.** The customer's own data. It stays inside the customer's environment, except what the client chooses to let a frontier model provider see ([`specs/application/product/platform-and-compliance-operations/deployment-topology.md § Deployment Topology § Frontier Models`](/specs/application/product/platform-and-compliance-operations/deployment-topology.md#frontier-models)).
