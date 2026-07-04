# Verisaria Project Intake Baseline

Date: 2026-07-04  
Scope: read-only takeover research plus local environment/bootstrap verification.  
Primary current LLM target: MiniMax through the generic OpenAI-compatible provider. Ollama is treated as an optional legacy/local provider, not the mainline runtime.

## 1. Executive Summary

Verisaria is an LLM-driven RPG world engine implemented as a Python package. It is not a chat frontend; its differentiator is a structured world runtime where LLMs parse, propose, arbitrate, and voice responses, while durable game truth lives in typed world state, immutable events, NPC memory/belief, relationship state, agenda, world variables, and an emergent fact ledger.

The project is a functioning but transitional prototype. It has a surprisingly large deterministic test suite and substantial design/test-agent documentation, and its offline/fake runtime path works after bootstrapping with `uv`. The mainline MiniMax provider configuration is wired and instantiable. The biggest handoff risks are not basic execution; they are state/documentation drift, a very large orchestration module, unmanaged untracked research/playtest assets, optional provider tests that fail without local services, and the lack of a visible CI/quality gate.

Recommended immediate posture: freeze a reliable baseline before feature work. Concretely, document the current test matrix, make MiniMax the explicit main provider in docs, quarantine or gate optional Ollama integration tests, decide which scripts/reports/large content packs are source assets, and only then plan refactor or feature slices.

## 2. Evidence Collected

### 2.1 Files and docs inspected

Key product and design documents:

- `README.md`
- `docs/design/llm-rpg-world-engine-design.md`
- `docs/design/protocol-design.md`
- `docs/design/dynamic-world-model.md`
- `docs/design/emergent-fact-ledger.md`
- `docs/design/tui-design.md`
- `docs/design/ui-architecture-direction.md`
- `docs/design/worldclock-and-weather.md`
- `docs/design/pack-authoring-guide.md`
- `docs/design/game-modes-direction.md`
- `docs/planning/TODO.md`
- `docs/planning/TODO_TUI_CLI.md`
- `docs/planning/test-agent-handoff.md`
- `docs/planning/grand-integration-pack-task.md`

Key implementation surfaces inspected through codegraph and targeted reads:

- `src/verisaria/runtime/session.py`
- `src/verisaria/protocol/engine_session.py`
- `src/verisaria/protocol/__init__.py`
- `src/verisaria/engine/world.py`
- `src/verisaria/engine/llm.py`
- `src/verisaria/engine/campaign_loader.py`
- `src/verisaria/engine/fact_ledger.py`
- `src/verisaria/frontends/cli.py`
- `src/verisaria/frontends/tui/app.py`
- `tests/test_openai_provider.py`
- `tests/test_ollama_provider.py`

### 2.2 Commands run

Environment/bootstrap:

```bash
uv sync --extra dev --extra tui
uv run python --version
```

Runtime/test verification:

```bash
uv run python -m verisaria --help
uv run python -m verisaria validate fixtures/content_packs/valid_frontier_town.json
uv run python -m verisaria run fixtures/content_packs/valid_frontier_town.json --llm fake
uv run python -m pytest --collect-only -q
uv run python -m pytest -q
uv run python -m pytest -q --ignore=tests/test_ollama_provider.py
```

MiniMax configuration smoke, without sending a live request:

```bash
uv run python - <<'PY'
from pathlib import Path
from verisaria.runtime.session import GameSession
import os

for raw in Path('.env').read_text().splitlines():
    line = raw.strip()
    if line and not line.startswith('#') and '=' in line:
        key, value = line.split('=', 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"\''))

s = GameSession('fixtures/content_packs/minimal_valid.json', save_dir='_tmp_minimax_smoke', llm_backend='minimax')
p = s.llm_provider
print(type(p).__name__)
print(getattr(p, 'base_url', ''))
print(getattr(p, 'model', ''))
print(bool(getattr(p, 'api_key', '')))
print(getattr(p, 'extra_params', {}))
PY
```

Git/workspace facts:

```bash
GIT_MASTER=1 git status --short
GIT_MASTER=1 git diff --stat
GIT_MASTER=1 git ls-files
```

## 3. Repository Inventory

### 3.1 Current tracked source

Git currently tracks 187 files:

| Area | Tracked files |
|---|---:|
| root files | 3 |
| `content/` | 2 |
| `docs/` | 37 |
| `fixtures/` | 18 |
| `scripts/` | 2 |
| `src/` | 46 |
| `tests/` | 79 |

### 3.2 Working tree state

At intake time there were no tracked file diffs, but many untracked items. `git status --short` reported 80 status entries, including directory entries for:

- `.omo/`
- `.opencode/`
- `_wc_s3b/`
- `docs/design/ui_prototypes/generated/`
- `draft/`
- several additional `fixtures/content_packs/*.json`
- `human-test/`
- `reports/`
- 68 untracked `scripts/*` entries
- `uv.lock`

Interpretation: the repository history and the working directory are not aligned. Some untracked assets are likely important research/playtest outputs, content packs, GUI drafts, and drivers. Others may be local tool artifacts. This must be resolved before committing future work, otherwise it will be unclear what is canonical.

### 3.3 App asset scale, excluding local agent/config directories

After excluding `.git`, `.venv`, `.codegraph`, `.pytest_cache`, `.opencode`, `.omo`, `.claude`, `.vscode`, and `__pycache__`, the workspace has 737 app-adjacent files:

| Area | Files | Approx text LOC counted |
|---|---:|---:|
| `src/` | 52 | 16,896 |
| `tests/` | 79 | 17,281 |
| `scripts/` | 70 | 12,121 |
| `docs/` | 39 | 7,521 |
| `fixtures/` | 22 | 3,112 |
| `reports/` | 310 | 20,082 |
| `draft/` | 153 | 984 |
| `content/` | 2 | 224 |
| `human-test/` | 2 | 761 |

The source-to-test ratio is healthy by raw volume. The source-to-scripts/reports ratio shows the project has been driven heavily by empirical playtest/debug cycles, but those assets are not currently curated into the tracked repo.

## 4. Product Intent

### 4.1 Core product thesis

The intended product is a reusable RPG world runtime where:

- Players express complex actions in natural language.
- NPCs respond from their own limited perspective, not from global truth.
- LLMs do not directly rewrite game truth; they interpret, propose, arbitrate, and generate character voice.
- Consequences persist as structured state rather than only as prompt history.
- Content authors can create worlds through content packs rather than code changes.

The strongest conceptual distinction from AI Dungeon/SillyTavern-like systems is that the world has a structured ledger and validation layer. The LLM is closer to a GM/arbitrator inside a rules-bound world than to an unconstrained story generator.

### 4.2 Player-facing pillars

From README and design docs, the intended player experience centers on:

1. Natural language as first-class input.
2. NPC subjectivity and information asymmetry.
3. Emergent consequences rather than authored quest branches.
4. Dynamic world state that can be changed through social leverage, evidence, and authority.
5. A living world with time, weather, NPC routines, autonomous NPC interactions, and campaign pressure.
6. A structured frontend boundary so CLI, TUI, future GUI, or external clients can share the same engine.

### 4.3 Future/differentiating product direction

`docs/design/game-modes-direction.md` describes a future second-person/advisor mode. This is not current core scope. It is still strategically relevant because it reuses the same engine ideas: player gives advice, an autonomous protagonist decides whether to follow it, and consequences unfold through the world. The doc correctly recommends proving this with a small prototype before turning it into a main mode.

## 5. Architecture Baseline

### 5.1 Package layout

Current intended layout from README and source:

```text
src/verisaria/
  engine/      domain systems: world, rules, arbiter, memory, campaign, LLM, validation, etc.
  runtime/     GameSession: wires a playable session and tick loop
  protocol/    structured Command/Event/Snapshot DTOs and EngineSession facade
  frontends/   CLI REPL and Textual TUI
```

This separation is directionally good. The main issue is that the runtime layer has absorbed much of the orchestration and transitional frontend command handling.

### 5.2 Runtime spine

The central object is `GameSession` in `src/verisaria/runtime/session.py`. It wires most subsystems:

- content loading: `CampaignLoader`
- world: `WorldCore`
- intent parsing and coherence: `IntentParser`, `CoherenceChecker`
- action composition and rules: `ActionComposer`, `InteractionService`, `RulesEngine`
- arbitration: `LLMArbiter`, `StateValidator`
- memory and subjectivity: `MemoryStore`, `BeliefEngine`, `SubjectivityService`, `MemoryCompressor`
- NPC behavior: `NPCActionGenerator`, `NPCDialogueGenerator`, `NPCInteractionScheduler`
- relationship appraisal: `RelationshipAppraiser`, `RelationshipStore`
- campaign pressure: `CampaignDriverManager`
- fact ledger: `FactLedger`
- persistence: `PersistenceLayer`
- protocol emission: `protocol.Event` subclasses through `_event_sink`

This makes `GameSession` the true integration point and the highest-risk refactor target. Codegraph showed about 304 callers/references to `GameSession` across tests, scripts, CLI, protocol, and reports/scripts. Treat any change here as high blast-radius.

### 5.3 Command/tick flow

High-level flow for a player input:

```text
frontend input
  -> EngineSession.submit / GameSession.run_tick
  -> reset LLM budget
  -> handle clarification or slash command
  -> IntentParser parses natural language
  -> CoherenceChecker validates target/action feasibility
  -> ActionComposer / InteractionService creates Action
  -> special routing: world-change request, escort request, arbiter action, combat, movement, speech, physical action
  -> WorldCore commits event(s) and mutates core state
  -> ObservationDispatcher creates NPC perceptions
  -> Subjectivity/Memory/Belief/Relationship systems update
  -> NPC actions and NPC-NPC interactions run
  -> Campaign drivers and pending processes advance
  -> protocol events are emitted
  -> ResponseGenerator / frontend renders narrative
  -> tick/time/weather/pacing advance
```

Some commands still live as methods on `GameSession` (`/world`, `/agenda`, `/relationship`, `/map`, `/inject`, `/log`, etc.). The protocol design docs correctly identify this as a transitional coupling: long-term, view formatting should belong to frontends, while engine/runtime returns structured state.

### 5.4 Protocol/frontends

`EngineSession` in `src/verisaria/protocol/engine_session.py` is the protocol facade. It supports:

- `submit(command) -> TickResult`
- `submit_streaming(command, on_event) -> WorldSnapshot`
- `snapshot() -> WorldSnapshot`
- debug god-view escape hatch

This is the right architectural direction: structured Command/Event/Snapshot DTOs preserve the A5 boundary and avoid binding the engine to CLI strings.

The Textual TUI appears to be built on this protocol layer. TUI design docs say v1-v4 are largely implemented: event stream, right/left panels, world state, focus/god-view debug toggle, filtering, scrolling, dynamic world model display, time/weather display. Remaining frontend questions are less about raw capability and more about product/UX polish, view semantics, and future GUI scope.

## 6. Core Systems Status

### 6.1 Content packs and campaign loader

Content packs are JSON files under `fixtures/content_packs/`. `CampaignLoader` validates and builds `WorldState`. Tests cover schema validation, world book conflicts, declared empty locations, occupants, relationships, campaign drivers, and pack-specific fixtures.

Important content authoring rules are captured in `docs/design/pack-authoring-guide.md`. The guide is practical and tied to lint warnings, especially around world vars:

- every mutable variable needs a real satisfier (`set_by`)
- every mutable variable needs `request_keywords`
- avoid near-duplicate variables
- terminal labels should state sufficient conditions
- prerequisites must be reachable in one or two steps or represented as short processes
- NPCs who can satisfy variables must be reachable from the starting topology
- leverage facts must sit on the target NPC's own governed var
- escort/witness chains need special care

This guide is a major asset and should become part of the canonical development process.

### 6.2 World state and events

`WorldCore` owns mutable `WorldState`, an append-only event log, action/event IDs, tick advancement, movement, physical stamina changes, and snapshots. `WorldState` includes entities, locations, world vars, clock, weather, etc. Events are Pydantic models in `engine/schemas.py` and are validated to avoid subjective motive in event summaries.

The design principle is sound: events are neutral facts; observations and beliefs are subjective projections.

### 6.3 LLM provider layer

`engine/llm.py` defines:

- `FakeLLMProvider` for deterministic tests/offline development.
- `OllamaProvider` for local legacy/optional usage.
- `OpenAICompatibleProvider` for MiniMax and other chat-completions-compatible services.
- `LLMOrchestrator` for budget, priority degradation, retries, and fallback.

Current MiniMax baseline:

- `llm_backend='minimax'` builds `OpenAICompatibleProvider`.
- Base URL: `https://api.minimaxi.com/v1`.
- Model: `MiniMax-M3`.
- Extra params include `thinking: {type: disabled}`, `reasoning_split: true`, and `max_completion_tokens: 2048`.
- Tests assert MiniMax is just configuration, not a dedicated class.

Ollama baseline:

- Still present as an optional provider.
- `tests/test_ollama_provider.py` contains two real local integration tests that are not currently skipped when Ollama is absent.
- This caused the only test failures on this machine: connection refused to local Ollama.

Recommendation: mark/gate real Ollama tests consistently, like `tests/test_npc_dialogue.py` already does with `RPG_OLLAMA_TEST=1`, or split provider integration tests by environment.

### 6.4 Consequence channels

The project has three major consequence channels:

1. Channel A: relationship appraisal. NPCs evaluate player actions from their own knowledge, resulting in trust/suspicion/fear/etc. Relationship changes persist and affect later arbitration.
2. Channel B: player stance/agenda. Repeated player behavior clusters into confirmed stances, visible in agenda and usable by campaign context.
3. Channel C: world variables. Authority NPCs plus arbiter decisions can flip mutable world facts. The system supports dynamic prerequisites, pending processes, sufficiency closure, and escort/witness flows.

This is the most valuable engine layer. It turns free-form play into persistent consequences without a traditional quest-state graph.

### 6.5 Emergent fact ledger

`FactLedger` stores facts established during `partial_success` arbitration, keyed by the relevant world var. It is intentionally invisible to the player and feeds future arbiter prompts. This design addresses the problem where NPCs made concessions in dialogue but the system had no durable place to remember them.

This is a critical bridge between free-form negotiation and structured state. It should remain bounded, invisible, and validated against A5 assumptions.

### 6.6 Dynamic world model

The dynamic world model is substantially implemented according to docs and tests:

- GM/arbiter can create dynamic prerequisite vars.
- Dynamic vars are persisted.
- Near-duplicate vars are deduped or reused.
- Pending offscreen processes can mature after ticks.
- Escort is treated as a specialized willingness judgment.
- Sufficiency backstop can force terminal success when declared prerequisites are truly met.

The docs explicitly accept cyclic prerequisites as a content/emergence difficulty rather than something the engine should always solve.

### 6.7 Time, weather, living world

The world clock/weather design is implemented in slices:

- clock minutes are tied to pacing, not raw tick count
- time of day and clock are surfaced in snapshots/status
- weather changes by deterministic climate ladder
- NPC daily rhythm is opt-in at pack level
- key NPCs can be `stationed` to avoid breaking authority/escort chains
- time/weather are injected into NPC dialogue prompts and ambient narration

This subsystem is mature enough for content use, with future hooks for curfews, shift changes, weather affecting actions/visibility, and seasons.

### 6.8 CLI and TUI

CLI quality has been improved with `/map`, `/talk`, `/who`, empty-input hints, `/inject`, `/log`, `/time`, readline completion/history, status bar polish, and debug commands.

TUI has a more ambitious Textual frontend and appears to exercise the protocol layer. It is optional dependency via `.[tui]`, which is correct because the engine should stay lightweight.

The product still needs a decision on whether TUI is the near-term primary user surface or whether CLI remains the development surface while TUI/GUI mature.

## 7. Test and Verification Baseline

### 7.1 Environment

Initial system `python3` was Python 3.9.6 and lacked project dependencies. The project declares Python `>=3.12`. Using `uv` fixed the local environment:

```text
Python 3.14.6
pytest 9.1.1
verisaria 0.5.4 editable package
```

`uv sync --extra dev --extra tui` installed runtime, dev, and TUI dependencies.

### 7.2 Test results

Test collection:

```text
1069 tests collected
```

Full test suite with all files:

```text
1065 passed, 2 skipped, 2 failed
```

Failures:

- `tests/test_ollama_provider.py::TestOllamaProviderIntegration::test_ollama_responds`
- `tests/test_ollama_provider.py::TestOllamaProviderIntegration::test_ollama_intent_parsing`

Both failed because local Ollama was not running:

```text
Ollama connection error: <urlopen error [Errno 61] Connection refused>
```

Mainline/offline suite excluding the optional local Ollama provider file:

```text
1056 passed, 2 skipped
```

Runtime smoke:

```text
uv run python -m verisaria --help                     # passed
uv run python -m verisaria validate ...valid...json    # Content pack is valid.
uv run python -m verisaria run ... --llm fake          # CLI starts and exits cleanly
```

### 7.3 What this means

The deterministic/offline test baseline is healthy. Current failures do not indicate mainline product breakage if MiniMax is the actual provider. They indicate test-suite environment assumptions are stale.

However, there is no observed CI config, lockfile was previously absent/untracked, and real MiniMax E2E was not run in this intake to avoid spending API calls without a defined scenario. The next verification layer should be a controlled MiniMax driver run with transcript/log artifacts.

## 8. Documentation and State Drift

### 8.1 Version drift

- `README.md` says current status is `v0.4.0`.
- `pyproject.toml` says package version is `0.5.4`.

This should be reconciled. The docs contain valuable history, but without a current status page, readers must infer which historical claims still apply.

### 8.2 Test-count drift

`docs/planning/TODO.md` says final baseline `840 passed, 2 skipped`, but current collection is 1069 tests and current mainline excluding Ollama local integration is `1056 passed, 2 skipped`.

Again, the historical note is useful but should be moved to history or annotated as stale.

### 8.3 Provider drift

Older design docs still describe Ollama/GPT split as a core strategy. The project has moved toward MiniMax/OpenAI-compatible remote provider as the practical mainline. Documentation should explicitly state:

- MiniMax is current primary real provider.
- Fake is default deterministic dev/test provider.
- Ollama remains optional/local/legacy.
- Which integration tests require which services/env vars.

### 8.4 Asset drift

The working directory has a large amount of untracked material, especially scripts, reports, draft GUI assets, generated prototypes, human-test content, and additional content packs. Some of this likely contains important project history and playtest evidence. Until curated, it is a source of ambiguity.

## 9. Risk Register

### R1. Runtime orchestration concentration

`GameSession` is too central. It is currently the integration hub for engine, protocol, CLI command handling, LLM, state mutation, persistence, campaign, and debug surfaces. This is acceptable for a prototype but risky for continued feature growth.

Impact: high.  
Likelihood: high.  
Recommended response: do not big-bang refactor. First extract stable seams around command handling, world-change/escort routing, persistence state adapters, and protocol snapshots. Each extraction should be test-paired.

### R2. Optional provider tests fail by default

Ollama integration tests run even when no local Ollama service is available. This makes the full suite red on a valid MiniMax-focused setup.

Impact: medium.  
Likelihood: immediate.  
Recommended response: add an explicit marker/env gate for real Ollama tests, or split test profiles.

### R3. Canonical asset uncertainty

There are many untracked scripts/reports/content packs. Some are likely essential to project knowledge. Others may be disposable local artifacts.

Impact: high.  
Likelihood: high.  
Recommended response: run an asset triage. Classify each untracked top-level group into `track`, `archive`, `ignore`, or `delete after backup`. Do not start broad code changes until this is resolved.

### R4. Stale docs and historical TODOs

The docs are rich but not normalized into a current-state report. Future contributors may follow outdated assumptions about Ollama, versions, test baselines, or incomplete items that are already done.

Impact: medium-high.  
Likelihood: high.  
Recommended response: create a canonical `CURRENT_STATE.md` or update README with current status and link historical planning docs as archives.

### R5. No visible CI/quality gate

No CI/workflow or dedicated lint/typecheck configuration was observed during intake. The suite is strong, but without automation the baseline will rot.

Impact: high over time.  
Likelihood: medium-high.  
Recommended response: define `uv`-based CI: install, collect, offline tests, optional provider tests gated by env, content pack validation, possibly lint/type check later.

### R6. Real MiniMax behavior not revalidated in this intake

MiniMax config was verified without live calls. Historical reports show extensive MiniMax validation, but current code + current model + current prompts should be rechecked with one controlled scenario.

Impact: high for product confidence.  
Likelihood: unknown.  
Recommended response: run one short MiniMax smoke and one longer scripted playtest after agreeing on cost/time budget.

### R7. Content closure remains the hardest product question

Docs repeatedly show that engine mechanisms can work on clean fixtures, while rich packs fail or stall due to content topology, duplicate vars, unreachable satisfiers, or natural-language routing. The content authoring guide is a response to this, but it needs dogfooding on the current state.

Impact: high.  
Likelihood: high.  
Recommended response: treat content-pack authoring/lint/playtest as a first-class development loop, not a side artifact.

## 10. Recommended Next Workstreams

### 10.1 Baseline stabilization, immediate

Goal: make the current state reproducible for any new maintainer.

Tasks:

1. Commit or intentionally ignore `uv.lock` after deciding lockfile policy.
2. Document canonical setup: `uv sync --extra dev --extra tui`.
3. Update README provider section: Fake default, MiniMax primary real provider, Ollama optional.
4. Gate Ollama integration tests.
5. Add a test profile table:
   - offline deterministic: all tests except optional real providers
   - MiniMax smoke: one or more explicit scripts/tests
   - Ollama optional: only when local service is running
6. Triage untracked assets.

Expected result: everyone can reproduce the same green baseline before touching code.

### 10.2 Documentation consolidation, immediate

Goal: turn historical notes into maintainable state.

Tasks:

1. Add/update a current-state document.
2. Mark `TODO.md` as historical if it remains a timeline.
3. Reconcile version numbers.
4. Link key design docs from README in priority order.
5. Add a short “what to read first” path for new contributors.

Expected result: future discussions start from a single current baseline rather than scattered historical docs.

### 10.3 Real MiniMax validation, next

Goal: prove current main provider and current code still behave in a real LLM loop.

Minimum scenario:

1. One short command-path smoke on a small pack.
2. One Channel C request using a known authority/world var path.
3. One dialogue streaming check.
4. Log capture with no secrets.

Larger scenario:

- Re-run the current grand integration pack task around `emberfall_kiln_assize`, specifically the escort fix and `branding_stayed` closure path described in `docs/planning/grand-integration-pack-task.md`.

Expected result: confirm whether the historical “large pack can naturally close” question is solved or still blocked.

### 10.4 Architecture debt plan, after baseline

Goal: reduce `GameSession` blast radius without breaking behavior.

Suggested safe extraction order:

1. Move slash command rendering/handling behind a frontend command adapter.
2. Extract world-change and escort routing as a small service with direct tests.
3. Extract snapshot construction/presentation mapping from `EngineSession` only if TUI/GUI needs grow.
4. Extract persistence state assembly/restoration adapters.
5. Keep `GameSession.run_tick` as the integration spine until enough seams are proven.

Expected result: easier feature work without losing deterministic replay behavior.

### 10.5 Content/tooling loop, parallel

Goal: make “author a rich pack that closes” repeatable.

Tasks:

1. Promote `pack-authoring-guide.md` and `PackEditor.validate_pack` into a standard workflow.
2. Add validation commands for all canonical tracked content packs.
3. Decide whether untracked large content packs are canonical test assets.
4. Build a minimal report template for real playtests.
5. Keep anti-cheat checks mandatory in every real playtest.

Expected result: content failures become diagnosable and comparable instead of anecdotal.

## 11. Proposed Discussion Agenda

For the next planning meeting, decide in this order:

1. What is the near-term product target: engine demo, playable TUI prototype, content authoring platform, or closed vertical slice?
2. Which frontend is primary for the next month: CLI, TUI, or both?
3. What is the canonical real provider and test cost budget for MiniMax runs?
4. Which untracked assets should become source-of-truth?
5. Should the immediate engineering milestone be baseline/CI/docs, MiniMax playtest, runtime refactor, or content pack completion?
6. Is advisor/second-person mode still a future differentiator, or should it stay parked until core play is stable?

## 12. Suggested Definition of Done for “Project Taken Over”

The project should be considered properly taken over when all of these are true:

1. A clean clone can run `uv sync --extra dev --extra tui` and reproduce the offline green suite.
2. Optional provider tests do not fail by default when services are absent.
3. README accurately states version, provider strategy, setup, and test commands.
4. Untracked assets are classified and either tracked, archived, ignored, or removed after backup.
5. One current MiniMax smoke run has a saved log/transcript.
6. A current roadmap has explicit priorities and non-goals.
7. The first refactor/feature slice has a small, testable scope.

## 13. Current Baseline Verdict

The project is viable to continue. It is not a dead or merely speculative prototype: the offline engine works, there are over one thousand tests, the protocol/TUI direction exists, and the mainline MiniMax provider is wired. The next risk is process discipline, not raw feasibility. Without baseline cleanup, future work will be slowed by stale docs, unmanaged artifacts, and ambiguous test failures. With baseline cleanup, the project is ready for focused product and engineering planning.
