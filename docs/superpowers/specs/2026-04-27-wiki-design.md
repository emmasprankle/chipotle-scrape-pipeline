# Design: Knowledge Base Wiki

## Overview

A two-layer knowledge base to support building a labor forecasting model artifact for the Manager, Workforce Management – Volume & Labor role at Chipotle. Layer 1 is the existing `knowledge/raw/` Firecrawl output. Layer 2 is a new `knowledge/wiki/` directory of synthesis pages that interpret the raw extracts and directly feed the model.

## File Layout

```
knowledge/
  raw/                        ← layer 1 (Firecrawl output, already exists)
  wiki/                       ← layer 2 (synthesis pages, new)
    chipotle-at-scale.md
    recipe-for-growth.md
    labor-demand-signals.md
    data-inventory.md
    target-metrics.md
```

## Pages

### Context Track

**`chipotle-at-scale.md`**
Scale facts that contextualize the model's scope: ~4,000+ restaurants, 130K employees, 7 countries, $11.9B FY2025 revenue (+5.4%), 21M Rewards members. Key risk factors from SEC filings: wage inflation, labor market tightness, staffing shortages. Feeds the model by establishing that even a 1% forecast improvement has material dollar impact.

**`recipe-for-growth.md`**
Chipotle's declared FY2026 strategy — four pillars: transactions, accuracy, efficiency, speed. Maps each pillar to a WFM implication (e.g., speed → throughput staffing; accuracy → right people at the right time). COO Kidd's stated priorities ("back of house modernization," "guest obsessed culture"). Notes that the FY2025 earnings release full text is a gap — currently only the headline is in raw.

### Model Track

**`labor-demand-signals.md`**
What the model needs as inputs: transaction volume (daypart, day-of-week, seasonality), promotional lifts (Rewards On Repeat, LTO launches, BOGO events), digital order mix (Rewards members as % of sales), restaurant format (Chipotlane vs. standard). Annotates which signals are available from scraped data vs. need proxying.

**`data-inventory.md`**
A structured audit: each raw file, what usable signal it contains for the model, and its quality. Ends with a prioritized scrape list of what is still needed to make the model credible.

**`target-metrics.md`**
What the model produces: labor demand forecast (by restaurant, daypart, day), SPLH targets, overstaffing/understaffing flags. Ties each output to a Recipe for Growth pillar. Defines what "good" forecast accuracy looks like in this context and why it matters to the hiring manager.

## Page Inventory

| File | Track | Primary purpose | Key raw sources | Synthesis word limit |
|---|---|---|---|---|
| `chipotle-at-scale.md` | Context | Business scope and dollar impact justification | `ir-chipotle-com-financial-releases.md`, `newsroom-chipotle-com-2025-05-06-...jason-kidd.md`, `ir-chipotle-com-sec-filings.md` | 400 |
| `recipe-for-growth.md` | Context | Strategic frame and WFM implications | `ir-chipotle-com.md`, `newsroom-chipotle-com-2025-05-06-...jason-kidd.md`, FY2025 earnings release `[NEEDS SCRAPE]` | 400 |
| `labor-demand-signals.md` | Model | Model input features and their availability | `ir-chipotle-com-news-releases.md`, `newsroom-chipotle-com-press-releases.md` | 400 |
| `data-inventory.md` | Model | Audit of scraped sources + prioritized scrape backlog | All `knowledge/raw/` files | 400 |
| `target-metrics.md` | Model | Model output design tied to business priorities | `ir-chipotle-com-financial-releases.md`, job posting | 400 |

## Demo Coupling

The wiki feeds the labor forecasting model as follows. Each page has a direct handoff role:

| Wiki page | What it gives the model |
|---|---|
| `chipotle-at-scale.md` | Business justification — scale figures to frame the model's impact narrative |
| `recipe-for-growth.md` | Output framing — model results should be presented against the four pillars (transactions, accuracy, efficiency, speed) |
| `labor-demand-signals.md` | Input feature list — the demand drivers the model must incorporate or proxy |
| `data-inventory.md` | Data decisions — which scraped sources to use as inputs, which to proxy, which require synthetic stand-ins |
| `target-metrics.md` | Output design — SPLH targets, forecast granularity (daypart × day × restaurant format), accuracy benchmarks |

The model should be buildable from `data-inventory.md` + `labor-demand-signals.md` alone. The context track pages (`chipotle-at-scale.md`, `recipe-for-growth.md`) inform the narrative framing presented to the hiring manager, not the model mechanics.

## Known Conflicts in Source Material

Conflicts identified across the raw files that must be resolved or noted before using figures in the model or narrative:

1. **Restaurant count:** Job posting "Who We Are" section lists US/Canada/UK/France/Germany only (no Middle East). Jan 2026 press release explicitly includes the Middle East and cites 3,900+ restaurants as of September 30, 2025. **Resolution:** use the Jan 2026 press release figure as current; the job posting boilerplate is stale.

2. **Revenue figure vs. available detail:** The $11.9B FY2025 revenue figure and "Recipe for Growth" strategy are visible only as a headline teaser in `ir-chipotle-com-financial-releases.md`. The full earnings release has not been scraped. **Resolution:** treat $11.9B as confirmed but flag all Recipe for Growth pillar detail as `[NEEDS SCRAPE]` until the full release is ingested.

3. **Jason Kidd title evolution:** The May 2025 announcement names Curt Garner as expanding to "President, Chief Strategy and Technology Officer" and Chris Brandt as "President, Chief Brand Officer." The Jan 2026 transitions show Brandt has since departed. Garner's expanded title remains current. **Resolution:** use the Jan 2026 press release as the authoritative leadership state.

## Page Template

Every synthesis page follows this three-section structure:

```markdown
## Synthesis
[2–4 paragraphs of interpretation]

## Sources
- [`<raw-filename>`](../raw/<raw-filename>) — one-line description of what it contributes

## Gaps
- `[NEEDS SCRAPE]` <description> — <why it matters to the model>
```

## Citation Format

Sources sections link to raw files by relative path from `knowledge/wiki/`. This keeps the layers loosely coupled — raw files can be added or updated without changing synthesis page structure.

## Gaps Convention

`[NEEDS SCRAPE]` markers in every Gaps section serve a dual purpose: they document what's missing for the model and act as a scrape backlog for the pipeline. Priority gaps identified during brainstorm:

- FY2025 full earnings release — Recipe for Growth pillar detail
- 10-K labor cost section — SPLH baseline, labor % of revenue
- Chipotle investor day / analyst transcripts — volume and transaction guidance

## Out of Scope

The following are explicitly excluded. If they appear during implementation, do not add them:

- **Interview behavioral prep** — STAR stories, "tell me about yourself" framing, general interview tips
- **Competitive landscape** — no analysis of CAVA, McDonald's, or other QSR competitors
- **Labor law and compliance detail** — FLSA, predictive scheduling laws, ADA; the model does not need legal content
- **Brand and marketing analysis** — loyalty program mechanics, menu strategy, campaign performance beyond their use as volume signals
- **Financial modeling or valuation** — no DCF, no stock analysis, no investor-oriented commentary
- **Leadership biographies beyond role context** — executive backgrounds are captured only insofar as they reveal strategic priorities relevant to WFM
- **Any content that does not have a clear handoff to the model or its narrative framing**

## Scope

Medium. Five synthesis pages. No page should exceed ~400 words in its Synthesis section. The wiki informs the model; it is not a complete interview prep guide.
