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

## Scope

Medium. Five synthesis pages. No page should exceed ~400 words in its Synthesis section. The wiki informs the model; it is not a complete interview prep guide.
