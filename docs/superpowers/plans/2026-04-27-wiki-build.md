# Knowledge Base Wiki Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create five synthesis wiki pages in `knowledge/wiki/` that interpret the existing raw Firecrawl extracts and feed a Chipotle labor forecasting model.

**Architecture:** Two-layer knowledge base. Layer 1 (`knowledge/raw/`) already exists as Firecrawl output. Layer 2 (`knowledge/wiki/`) is a set of five markdown synthesis pages — two context-track pages (business framing) and three model-track pages (inputs, data, outputs). Each page follows a fixed three-section template: Synthesis, Sources, Gaps.

**Tech Stack:** Markdown, bash (structural validation only)

---

## File Structure

```
knowledge/
  wiki/                         ← create this directory
    chipotle-at-scale.md        ← create (context track)
    recipe-for-growth.md        ← create (context track)
    labor-demand-signals.md     ← create (model track)
    data-inventory.md           ← create (model track)
    target-metrics.md           ← create (model track)
```

No existing files are modified. All raw files in `knowledge/raw/` remain untouched.

---

## Validation Script (used in every task)

Each task uses this bash one-liner to confirm a wiki page is structurally valid:

```bash
# Usage: validate_wiki_page <filepath>
# Checks: file exists, has all three sections, word count ≤ 400 in Synthesis
file="knowledge/wiki/<page>.md"
grep -q "^## Synthesis" "$file" && echo "✓ Synthesis" || echo "✗ Synthesis missing"
grep -q "^## Sources" "$file" && echo "✓ Sources" || echo "✗ Sources missing"
grep -q "^## Gaps" "$file" && echo "✓ Gaps" || echo "✗ Gaps missing"
awk '/^## Synthesis/{found=1; next} /^## Sources/{found=0} found{print}' "$file" | wc -w
```

Expected output for a valid page: three ✓ lines and a word count ≤ 400.

---

## Task 1: Create wiki directory

**Files:**
- Create: `knowledge/wiki/` (directory)

- [ ] **Step 1: Create the directory**

```bash
mkdir -p knowledge/wiki
```

- [ ] **Step 2: Verify it exists**

```bash
ls knowledge/
```

Expected output includes `wiki` alongside `raw`.

- [ ] **Step 3: Commit**

```bash
touch knowledge/wiki/.gitkeep
git add knowledge/wiki/.gitkeep
git commit -m "feat: create knowledge/wiki directory for synthesis layer"
```

---

## Task 2: Write chipotle-at-scale.md

**Files:**
- Create: `knowledge/wiki/chipotle-at-scale.md`

- [ ] **Step 1: Run validation to confirm it fails (file does not yet exist)**

```bash
file="knowledge/wiki/chipotle-at-scale.md"
[ -f "$file" ] && echo "exists" || echo "✗ not found — expected"
```

Expected: `✗ not found — expected`

- [ ] **Step 2: Write the file**

Create `knowledge/wiki/chipotle-at-scale.md` with this exact content:

```markdown
# Chipotle at Scale

## Synthesis

Chipotle operates at a scale where marginal improvements in labor forecasting translate directly to measurable business impact. As of December 2025, the company crossed 4,000 restaurants — a milestone marked by the opening of its Manhattan, Kansas location. As of September 30, 2025, the footprint stood at over 3,900 locations across the United States, Canada, the United Kingdom, France, Germany, and the Middle East. The workforce exceeds 130,000 employees.

Financially, Chipotle reported $11.9 billion in full-year 2025 revenue, a 5.4% increase year-over-year. At this scale, a 1% reduction in labor inefficiency — whether through reduced overstaffing or elimination of understaffing penalties — represents tens of millions of dollars in cost impact across the system. This is the core business case for a labor forecasting model.

The digital channel adds a forecastable layer on top of walk-in traffic: 21 million active Rewards members drive a significant portion of company sales, as stated in the April 2026 Rewards relaunch announcement. Digital orders cluster predictably by daypart and day-of-week, making them a higher-quality demand signal than walk-in traffic alone.

Chipotle's own forward-looking disclosures flag three workforce pressures that make accurate forecasting a strategic necessity: increasing wage inflation driven by minimum wage legislation, a competitive labor market that has caused staffing shortages, and the impact of union organizing efforts on labor cost structures. These pressures are listed as material risks in the January 2026 press release.

## Sources

- [`2026-04-15-newsroom-chipotle-com-2025-05-06-chipotle-names-jason-kidd-chief-operating-officer-president-and-chief-strategy-officer-jack-hartung-sets-retirement-date.md`](../raw/2026-04-15-newsroom-chipotle-com-2025-05-06-chipotle-names-jason-kidd-chief-operating-officer-president-and-chief-strategy-officer-jack-hartung-sets-retirement-date.md) — ~3,800 restaurants as of March 31, 2025; 130,000+ employees
- [`2026-04-15-www-prnewswire-com-news-releases-chipotle-announces-leadership-transitions-302658971.md`](../raw/2026-04-15-www-prnewswire-com-news-releases-chipotle-announces-leadership-transitions-302658971.md) — 3,900+ restaurants as of September 30, 2025; wage inflation, labor market, staffing shortages as material risks
- [`2026-04-15-ir-chipotle-com-financial-releases.md`](../raw/2026-04-15-ir-chipotle-com-financial-releases.md) — $11.9B FY2025 revenue (+5.4%); 4,000th restaurant milestone (December 2025)
- [`2026-04-15-newsroom-chipotle-com-press-releases.md`](../raw/2026-04-15-newsroom-chipotle-com-press-releases.md) — 21M active Rewards members driving significant portion of sales

## Gaps

- `[NEEDS SCRAPE]` FY2025 full earnings release — quarterly revenue breakdown, transaction comp data, labor cost as % of revenue
- `[NEEDS SCRAPE]` 10-K (filed Feb 4, 2026) labor section — SPLH baseline, total labor spend, headcount by segment
```

- [ ] **Step 3: Run validation**

```bash
file="knowledge/wiki/chipotle-at-scale.md"
grep -q "^## Synthesis" "$file" && echo "✓ Synthesis" || echo "✗ Synthesis missing"
grep -q "^## Sources" "$file" && echo "✓ Sources" || echo "✗ Sources missing"
grep -q "^## Gaps" "$file" && echo "✓ Gaps" || echo "✗ Gaps missing"
awk '/^## Synthesis/{found=1; next} /^## Sources/{found=0} found{print}' "$file" | wc -w
```

Expected: three ✓ lines and word count ≤ 400.

- [ ] **Step 4: Verify all cited raw files exist**

```bash
ls knowledge/raw/2026-04-15-newsroom-chipotle-com-2025-05-06-chipotle-names-jason-kidd-chief-operating-officer-president-and-chief-strategy-officer-jack-hartung-sets-retirement-date.md
ls knowledge/raw/2026-04-15-www-prnewswire-com-news-releases-chipotle-announces-leadership-transitions-302658971.md
ls knowledge/raw/2026-04-15-ir-chipotle-com-financial-releases.md
ls knowledge/raw/2026-04-15-newsroom-chipotle-com-press-releases.md
```

Expected: all four files found with no errors.

- [ ] **Step 5: Commit**

```bash
git add knowledge/wiki/chipotle-at-scale.md
git commit -m "feat: add chipotle-at-scale wiki page (context track)"
```

---

## Task 3: Write recipe-for-growth.md

**Files:**
- Create: `knowledge/wiki/recipe-for-growth.md`

- [ ] **Step 1: Run validation to confirm file does not yet exist**

```bash
[ -f "knowledge/wiki/recipe-for-growth.md" ] && echo "exists" || echo "✗ not found — expected"
```

Expected: `✗ not found — expected`

- [ ] **Step 2: Write the file**

Create `knowledge/wiki/recipe-for-growth.md` with this exact content:

```markdown
# Recipe for Growth

## Synthesis

Chipotle's FY2026 strategic framework, announced alongside full-year 2025 earnings on February 3, 2026, is called "Recipe for Growth." The strategy is organized around four pillars: growing transactions, driving accuracy, improving efficiency, and increasing speed. Each pillar has a direct workforce management implication.

**Transactions:** Transaction volume is the primary demand signal for labor. Growing transactions means the forecasting model must handle higher peak loads and capture incremental volume from promotions, digital channels, and new restaurant formats. Forecast accuracy at volume peaks is what serves this pillar.

**Accuracy:** In a WFM context, accuracy means having the right number of people at the right time — minimizing both overstaffing (which inflates labor cost) and understaffing (which degrades guest experience and throughput). This is the core optimization target of the forecasting model.

**Efficiency:** Efficiency maps to SPLH (sales per labor hour), the standard restaurant labor productivity metric. A model that improves SPLH by reducing wasted labor hours directly serves this pillar.

**Speed:** Speed refers to throughput — how quickly guests move through the line. Peak-hour staffing decisions determine throughput. The model must forecast at daypart-level peaks, not just daily totals, to inform throughput staffing decisions.

COO Jason Kidd, hired in May 2025 from Taco Bell, explicitly named "modernizing the back of house" and building a "guest obsessed culture" as priorities. These statements confirm that operations and labor performance are active C-suite concerns, making a labor forecasting model directly relevant to the current leadership agenda.

## Sources

- [`2026-04-15-ir-chipotle-com-financial-releases.md`](../raw/2026-04-15-ir-chipotle-com-financial-releases.md) — "Recipe for Growth" strategy headline; four pillars named
- [`2026-04-15-ir-chipotle-com.md`](../raw/2026-04-15-ir-chipotle-com.md) — IR homepage confirming Recipe for Growth as current strategic frame
- [`2026-04-15-newsroom-chipotle-com-2025-05-06-chipotle-names-jason-kidd-chief-operating-officer-president-and-chief-strategy-officer-jack-hartung-sets-retirement-date.md`](../raw/2026-04-15-newsroom-chipotle-com-2025-05-06-chipotle-names-jason-kidd-chief-operating-officer-president-and-chief-strategy-officer-jack-hartung-sets-retirement-date.md) — Kidd COO announcement; "back of house modernization" and "guest obsessed culture"

## Gaps

- `[NEEDS SCRAPE]` FY2025 full earnings release (Feb 3, 2026) — detailed pillar definitions, quantitative targets, and management commentary on each pillar
- `[NEEDS SCRAPE]` Q1 2026 earnings call transcript (April 29, 2026) — updated progress against Recipe for Growth targets and volume trends
```

- [ ] **Step 3: Run validation**

```bash
file="knowledge/wiki/recipe-for-growth.md"
grep -q "^## Synthesis" "$file" && echo "✓ Synthesis" || echo "✗ Synthesis missing"
grep -q "^## Sources" "$file" && echo "✓ Sources" || echo "✗ Sources missing"
grep -q "^## Gaps" "$file" && echo "✓ Gaps" || echo "✗ Gaps missing"
awk '/^## Synthesis/{found=1; next} /^## Sources/{found=0} found{print}' "$file" | wc -w
```

Expected: three ✓ lines and word count ≤ 400.

- [ ] **Step 4: Verify all cited raw files exist**

```bash
ls knowledge/raw/2026-04-15-ir-chipotle-com-financial-releases.md
ls knowledge/raw/2026-04-15-ir-chipotle-com.md
ls knowledge/raw/2026-04-15-newsroom-chipotle-com-2025-05-06-chipotle-names-jason-kidd-chief-operating-officer-president-and-chief-strategy-officer-jack-hartung-sets-retirement-date.md
```

Expected: all three files found with no errors.

- [ ] **Step 5: Commit**

```bash
git add knowledge/wiki/recipe-for-growth.md
git commit -m "feat: add recipe-for-growth wiki page (context track)"
```

---

## Task 4: Write labor-demand-signals.md

**Files:**
- Create: `knowledge/wiki/labor-demand-signals.md`

- [ ] **Step 1: Run validation to confirm file does not yet exist**

```bash
[ -f "knowledge/wiki/labor-demand-signals.md" ] && echo "exists" || echo "✗ not found — expected"
```

Expected: `✗ not found — expected`

- [ ] **Step 2: Write the file**

Create `knowledge/wiki/labor-demand-signals.md` with this exact content:

```markdown
# Labor Demand Signals

## Synthesis

Labor demand at Chipotle is driven by transaction volume, which is shaped by four overlapping signal types. A credible forecasting model must incorporate or proxy each of these.

**Time-based signals:** Day-of-week and daypart are the primary structural demand drivers in fast-casual restaurants. Lunch (11am–2pm) and dinner (5pm–8pm) represent peak transaction windows. The model should forecast at daypart granularity — at minimum: morning prep (8–11am), lunch peak (11am–2pm), afternoon bridge (2–5pm), dinner peak (5–8pm), and close (8pm+). Seasonal patterns operate over a longer horizon and require quarterly comp sales data for calibration.

**Promotional lift signals:** Chipotle runs structured promotional events that create predictable volume spikes. Events documented in the current raw sources: Rewards On Repeat loyalty relaunch (April 13, 2026), Burrito Vault game for National Burrito Day (March 30, 2026), Cilantro Lime Sauce LTO (March 18, 2026), and the Tatted BOGO with Swae Lee (Friday March 13, 2026). Promotion dates should be a categorical input feature — these events create measurable lifts that follow the announcement and are predictable in advance.

**Digital mix signal:** 21 million active Rewards members drive a significant portion of sales. Digital orders (app and web) cluster predictably in lunch and early dinner dayparts and are more forecastable than walk-in traffic. The Rewards member base is actively growing, making the digital share an increasingly important demand signal.

**Restaurant format:** Chipotlane locations (drive-thru digital order pickup) have a different transaction pattern and staffing model than standard dine-in. Format should be a feature in the model to avoid conflating the two demand profiles, as throughput staffing requirements differ materially.

## Sources

- [`2026-04-15-newsroom-chipotle-com-press-releases.md`](../raw/2026-04-15-newsroom-chipotle-com-press-releases.md) — promotional event calendar (Rewards On Repeat, Burrito Vault, Cilantro Lime Sauce, Tatted BOGO); 21M Rewards members driving significant portion of sales
- [`2026-04-15-ir-chipotle-com-news-releases.md`](../raw/2026-04-15-ir-chipotle-com-news-releases.md) — same promotional event list from investor relations channel

## Gaps

- `[NEEDS SCRAPE]` FY2025 earnings call transcript — management commentary on daypart mix, transaction volume by period, digital order share percentage
- `[NEEDS SCRAPE]` Chipotlane operations/investor commentary — format-specific transaction patterns and staffing model differences
- `[NEEDS SCRAPE]` Historical quarterly comp sales releases (Q1–Q4 2025) — seasonal pattern baseline for model training data
```

- [ ] **Step 3: Run validation**

```bash
file="knowledge/wiki/labor-demand-signals.md"
grep -q "^## Synthesis" "$file" && echo "✓ Synthesis" || echo "✗ Synthesis missing"
grep -q "^## Sources" "$file" && echo "✓ Sources" || echo "✗ Sources missing"
grep -q "^## Gaps" "$file" && echo "✓ Gaps" || echo "✗ Gaps missing"
awk '/^## Synthesis/{found=1; next} /^## Sources/{found=0} found{print}' "$file" | wc -w
```

Expected: three ✓ lines and word count ≤ 400.

- [ ] **Step 4: Verify all cited raw files exist**

```bash
ls knowledge/raw/2026-04-15-newsroom-chipotle-com-press-releases.md
ls knowledge/raw/2026-04-15-ir-chipotle-com-news-releases.md
```

Expected: both files found with no errors.

- [ ] **Step 5: Commit**

```bash
git add knowledge/wiki/labor-demand-signals.md
git commit -m "feat: add labor-demand-signals wiki page (model track)"
```

---

## Task 5: Write data-inventory.md

**Files:**
- Create: `knowledge/wiki/data-inventory.md`

- [ ] **Step 1: Run validation to confirm file does not yet exist**

```bash
[ -f "knowledge/wiki/data-inventory.md" ] && echo "exists" || echo "✗ not found — expected"
```

Expected: `✗ not found — expected`

- [ ] **Step 2: Write the file**

Create `knowledge/wiki/data-inventory.md` with this exact content:

```markdown
# Data Inventory

## Synthesis

The table below audits all raw files in `knowledge/raw/` for their utility to the labor forecasting model. "Model utility" rates how directly each file's content feeds model inputs, output framing, or business narrative. Files rated None contribute nothing and should not be re-scraped unless their content changes materially.

| Raw file (2026-04-15 scrape) | Model utility | What it yields for the model |
|---|---|---|
| `newsroom-chipotle-com-press-releases.md` | Medium | Promotional event calendar (volume lift signals); 21M Rewards members stat |
| `ir-chipotle-com-news-releases.md` | Low | Duplicate promotional calendar from IR channel; no new signal |
| `newsroom-...-jason-kidd.md` | High | Scale figures (3,800 restaurants, 130K employees); Kidd strategic priorities; org changes |
| `prnewswire-...-leadership-transitions.md` | Medium | 3,900+ restaurants as of Sept 2025; labor risk factors (wage inflation, staffing shortages) |
| `qsrmagazine-...-new-cmo.md` | None | Duplicate of prnewswire; no new content |
| `ir-chipotle-com-2026-01-12-...transitions.md` | None | Word-for-word duplicate of prnewswire; no new content |
| `ir-chipotle-com-financial-releases.md` | High | $11.9B FY2025 revenue (+5.4%); Recipe for Growth headline; 4,000th restaurant milestone |
| `ir-chipotle-com.md` | Low | Same financial headlines; stock price only addition |
| `ir-chipotle-com-sec-filings.md` | Medium | Confirms 10-K filed Feb 4, 2026; 8-K for earnings; links only, no document content |
| `hospitality-week-...-appointments.md` | None | Paywalled — no content accessible |

**Prioritized scrape backlog (ordered by model impact):**

1. FY2025 full earnings release — Recipe for Growth pillar detail, transaction comp data, labor cost as % of revenue
2. 10-K (filed Feb 4, 2026) — labor cost section, SPLH baseline, total labor spend, workforce risk factors with specifics
3. Q1–Q4 2025 quarterly earnings releases — comp sales data for seasonal training baseline
4. Q1 2026 earnings call transcript (available after April 29, 2026) — most recent volume trends and Recipe for Growth progress

## Sources

- All files in `knowledge/raw/` as of 2026-04-15 scrape

## Gaps

- `[NEEDS SCRAPE]` FY2025 full earnings release — highest priority; unlocks Recipe for Growth detail and transaction data
- `[NEEDS SCRAPE]` 10-K labor section — required for SPLH baseline and labor cost % benchmark
- `[NEEDS SCRAPE]` Q1–Q4 2025 earnings releases — seasonal and quarterly transaction patterns for training data
- `[NEEDS SCRAPE]` Q1 2026 earnings call transcript (available after April 29, 2026) — most current volume signal
```

- [ ] **Step 3: Run validation**

```bash
file="knowledge/wiki/data-inventory.md"
grep -q "^## Synthesis" "$file" && echo "✓ Synthesis" || echo "✗ Synthesis missing"
grep -q "^## Sources" "$file" && echo "✓ Sources" || echo "✗ Sources missing"
grep -q "^## Gaps" "$file" && echo "✓ Gaps" || echo "✗ Gaps missing"
awk '/^## Synthesis/{found=1; next} /^## Sources/{found=0} found{print}' "$file" | wc -w
```

Expected: three ✓ lines and word count ≤ 400.

- [ ] **Step 4: Verify the raw directory is accessible**

```bash
ls knowledge/raw/ | wc -l
```

Expected: `10` (ten raw files currently present).

- [ ] **Step 5: Commit**

```bash
git add knowledge/wiki/data-inventory.md
git commit -m "feat: add data-inventory wiki page (model track)"
```

---

## Task 6: Write target-metrics.md

**Files:**
- Create: `knowledge/wiki/target-metrics.md`

- [ ] **Step 1: Run validation to confirm file does not yet exist**

```bash
[ -f "knowledge/wiki/target-metrics.md" ] && echo "exists" || echo "✗ not found — expected"
```

Expected: `✗ not found — expected`

- [ ] **Step 2: Write the file**

Create `knowledge/wiki/target-metrics.md` with this exact content:

```markdown
# Target Metrics

## Synthesis

The labor forecasting model should produce three categories of output. Each is tied directly to a Recipe for Growth pillar.

**Primary forecast output — labor demand in headcount-hours:** Forecasted at daypart × day-of-week × restaurant format granularity. Dayparts: morning prep (8–11am), lunch peak (11am–2pm), afternoon bridge (2–5pm), dinner peak (5–8pm), close (8pm+). Restaurant format distinguishes Chipotlane from standard dine-in, as throughput staffing requirements differ. The forecast horizon should be at minimum two weeks — the standard scheduling window in restaurant operations.

**Efficiency metric — SPLH (sales per labor hour):** SPLH is the primary labor productivity benchmark in restaurant operations. The model's headcount recommendations should translate directly to SPLH projections: given a volume forecast and a staffing level, the implied SPLH should be visible. The model should accept a SPLH target as an input constraint. Actual baseline figures require the 10-K (currently a gap); industry benchmarks for fast-casual are approximately $50–$60 SPLH.

**Accuracy metric — MAPE (mean absolute percentage error):** A two-week forecast with MAPE below 10% is considered strong in restaurant WFM. The model should report MAPE at both the aggregate level and by daypart, since accuracy at lunch peak matters more operationally than accuracy at close. Bias (systematic over- or under-forecasting direction) should be tracked separately from MAPE.

**Recipe for Growth alignment:**
- Transactions → transaction volume input drives headcount output
- Accuracy → MAPE and bias metrics directly measure this pillar
- Efficiency → SPLH output connects forecast to labor cost impact
- Speed → daypart granularity enables throughput staffing at lunch and dinner peaks

## Sources

- [`2026-04-15-ir-chipotle-com-financial-releases.md`](../raw/2026-04-15-ir-chipotle-com-financial-releases.md) — Recipe for Growth pillars (transactions, accuracy, efficiency, speed)
- [`2026-04-15-newsroom-chipotle-com-2025-05-06-chipotle-names-jason-kidd-chief-operating-officer-president-and-chief-strategy-officer-jack-hartung-sets-retirement-date.md`](../raw/2026-04-15-newsroom-chipotle-com-2025-05-06-chipotle-names-jason-kidd-chief-operating-officer-president-and-chief-strategy-officer-jack-hartung-sets-retirement-date.md) — throughput and back-of-house modernization as Kidd priorities

## Gaps

- `[NEEDS SCRAPE]` 10-K — SPLH baseline and historical labor cost % required to replace industry estimate with Chipotle-specific target
- `[NEEDS SCRAPE]` FY2025 earnings release — any quantitative throughput or accuracy targets stated by management
```

- [ ] **Step 3: Run validation**

```bash
file="knowledge/wiki/target-metrics.md"
grep -q "^## Synthesis" "$file" && echo "✓ Synthesis" || echo "✗ Synthesis missing"
grep -q "^## Sources" "$file" && echo "✓ Sources" || echo "✗ Sources missing"
grep -q "^## Gaps" "$file" && echo "✓ Gaps" || echo "✗ Gaps missing"
awk '/^## Synthesis/{found=1; next} /^## Sources/{found=0} found{print}' "$file" | wc -w
```

Expected: three ✓ lines and word count ≤ 400.

- [ ] **Step 4: Verify all cited raw files exist**

```bash
ls knowledge/raw/2026-04-15-ir-chipotle-com-financial-releases.md
ls knowledge/raw/2026-04-15-newsroom-chipotle-com-2025-05-06-chipotle-names-jason-kidd-chief-operating-officer-president-and-chief-strategy-officer-jack-hartung-sets-retirement-date.md
```

Expected: both files found with no errors.

- [ ] **Step 5: Final check — all five wiki pages present**

```bash
ls knowledge/wiki/
```

Expected output:
```
chipotle-at-scale.md
data-inventory.md
labor-demand-signals.md
recipe-for-growth.md
target-metrics.md
```

- [ ] **Step 6: Commit**

```bash
git add knowledge/wiki/target-metrics.md
git commit -m "feat: add target-metrics wiki page (model track)"
```
