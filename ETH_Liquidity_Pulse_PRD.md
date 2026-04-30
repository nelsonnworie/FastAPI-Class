# PRD: ETH Liquidity Pulse — Ethereum Stablecoin & Trader Intelligence Dashboard

**Version:** 1.0  
**Prepared for:** AI Agent Build  
**Stack:** React (JSX), HTML/CSS custom charts, no external charting libraries  
**Data Source:** Live FastAPI backend (no mock data, ever)

---

## 1. Project Overview

### 1.1 Title
**"ETH Liquidity Pulse"**  
Subtitle: *Stablecoin flows and trader behavior on Ethereum, live.*

### 1.2 Purpose
Build a single-page, data-driven React dashboard that answers high-signal business questions about Ethereum's stablecoin ecosystem and on-chain trader behavior. The data must be fetched live from the API at all times. No mock data. No placeholder values. No hardcoded numbers. Every metric displayed must be derived from the actual API response.

### 1.3 Audience
- DeFi researchers and protocol analysts
- Token issuers monitoring stablecoin market dynamics
- Institutional desks evaluating on-chain liquidity
- Independent analysts using Ethereum on-chain data

---

## 2. Data Layer

### 2.1 API Base URL
```
https://web-production-30e39.up.railway.app
```

### 2.2 Endpoints

#### `GET /data/stablecoins`
**Description:** Weekly mint, burn, and circulating supply of 9 major stablecoins on Ethereum.  
**Row count:** ~399 rows  
**Refresh cadence:** Every 3 days (check `metadata.next_refresh`)

**Response shape:**
```json
{
  "metadata": {
    "query": "stablecoins",
    "query_id": 5681885,
    "description": "Weekly Mint, Burn, and Circulating Supply of Major Stablecoins on Ethereum",
    "source": "Dune Analytics",
    "cache_backend": "in-memory",
    "row_count": 399,
    "is_cached": true,
    "is_fresh": true,
    "cache_age_hours": 0.46,
    "last_updated": "2026-04-29T17:41:21.607082",
    "next_refresh": "2026-05-02T17:41:21.607082"
  },
  "rows": [
    {
      "BUSD burns": 0,
      "BUSD mints": 0,
      "BUSD supply": 40026297.13,
      "DAI burns": -1020221117.49,
      "DAI mints": 1008042370.56,
      "DAI supply": 4415513363.27,
      "FRAX burns": 0,
      "FRAX mints": 0,
      "FRAX supply": 275927083.34,
      "LUSD burns": 0,
      "LUSD mints": 0,
      "LUSD supply": 28705635.95,
      "PYUSD burns": -10373173.92,
      "PYUSD mints": 1275864.75,
      "PYUSD supply": 2402340313.70,
      "RLUSD burns": -18750012,
      "RLUSD mints": 0,
      "RLUSD supply": 1189859897.06,
      "USDC burns": -838500387.35,
      "USDC mints": 495733429.33,
      "USDC supply": 54409735568.81,
      "USDS burns": -548800897.72,
      "USDS mints": 789841447.33,
      "USDS supply": 7954099860.16,
      "sUSD burns": -23990.40,
      "sUSD mints": 0,
      "sUSD supply": 25984890.12,
      "week": "2026-04-27 00:00:00.000 UTC"
    }
    // ... 398 more rows, descending by week
  ]
}
```

**Stablecoins covered:** `BUSD`, `DAI`, `FRAX`, `LUSD`, `PYUSD`, `RLUSD`, `USDC`, `USDS`, `sUSD`

**Data rules:**
- `burns` values are always <= 0 (negative). Display their absolute value where relevant.
- `supply` = current circulating supply for that week.
- `week` format: `"YYYY-MM-DD 00:00:00.000 UTC"` — parse to Date object.
- Rows are ordered descending (newest first). Reverse for chronological charts.
- Net flow for a coin in a week = `{coin} mints` + `{coin} burns` (burns are negative, so this is mints minus absolute burns).

---

#### `GET /data/traders`
**Description:** 2,000 sampled Ethereum wallets — their trading activity, volume, and behavioral classification over the last 365 days.  
**Row count:** 2000 rows

**Response shape:**
```json
{
  "metadata": {
    "query": "traders",
    "query_id": 5972407,
    "description": "Random traders on Ethereum (their activity, value and consistency in the last 365 days)",
    "source": "Dune Analytics",
    "cache_backend": "in-memory",
    "row_count": 2000,
    "is_cached": true,
    "is_fresh": true,
    "cache_age_hours": 0.57,
    "last_updated": "2026-04-29T17:41:26.859516",
    "next_refresh": "2026-05-02T17:41:26.859516"
  },
  "rows": [
    {
      "wallet": "0x40128ec23ab2bb7cba8cf103b14ea55b978c53d7",
      "active_weeks": 7,
      "tx_count_365d": 67,
      "total_volume": 10876.45,
      "target_variable": "🟢 Good Trader",
      "trader_activity_status": "🐦 Frequent User",
      "trader_volume_status": "🐟 Middle Value Trader",
      "trader_weekly_frequency_status": "🐦 OG"
    }
    // ... 1999 more rows
  ]
}
```

**Known categorical values (strip emoji for logic, keep for display):**

| Field | Known Values |
|---|---|
| `target_variable` | `🟢 Good Trader`, `🔴 Bad Trader` (infer others from data) |
| `trader_activity_status` | `🐦 Frequent User`, `🐤 Regular User`, others possible |
| `trader_volume_status` | `🦐 Low Value Trader`, `🐟 Middle Value Trader`, `🐳 High Value Trader` |
| `trader_weekly_frequency_status` | `🐦 OG`, others possible |

**IMPORTANT:** Do not hardcode these category values. Derive all unique values dynamically from the actual API response using `[...new Set(rows.map(r => r.field))]`.

---

### 2.3 Data Fetching Rules (NON-NEGOTIABLE)

1. **Always fetch from the live API.** No mock data, no fallback hardcoded rows, ever.
2. Both endpoints must be fetched on mount using `Promise.all` for parallel loading.
3. Show skeleton screens while fetching. Show a clear error state if fetch fails (with retry button).
4. Cache the response in component state only. Do not persist to localStorage.
5. Display `metadata.last_updated` and `metadata.next_refresh` in the dashboard header so users know data freshness.
6. Parse `week` strings to `Date` objects immediately after fetch. Sort rows chronologically (ascending) for all time series charts.

---

## 3. Business Questions the Dashboard Must Answer

These are the exact analytical questions each dashboard section must make answerable at a glance:

### Stablecoin Intelligence
1. **Market dominance:** Which stablecoin controls the most supply on Ethereum right now? How has dominance shifted over the past 52 weeks?
2. **Growth vs. contraction:** Which stablecoins are growing their supply? Which are contracting? Who is gaining ground fastest?
3. **Flow velocity:** Which stablecoin has the highest weekly mint/burn churn (gross activity), signaling deep DeFi usage?
4. **Net issuance:** Is the total stablecoin market on Ethereum expanding or contracting? What's the trend over the last 12 weeks?
5. **Shock detection:** Are there any weeks with extreme burn events (supply drops > 10% in a single week) that could signal de-pegging pressure or protocol stress?

### Trader Intelligence
6. **Quality distribution:** What share of wallets are classified as "Good Traders"? Is the sample healthy or dominated by bad actors?
7. **Volume concentration:** How concentrated is trading volume? Do a small number of high-value traders account for most volume (Pareto/whale effect)?
8. **Engagement depth:** How many weeks do traders stay active? Are most traders fly-by-night or long-term participants?
9. **Behavioral segments:** What combinations of activity and volume define each segment? Which segment has the best ROI profile?
10. **Power users:** Who are the top 10 traders by volume, and what do their behavioral tags look like?

---

## 4. Design System

Define this system in a single `designSystem.js` or CSS `:root` block. Every value in the UI must reference this system. No one-off values.

### 4.1 Color Palette

**Primary (Blue):**
```css
--color-primary-900: #0A1628;   /* darkest background */
--color-primary-800: #0D1F3C;   /* card background (dark mode) */
--color-primary-700: #102A52;   /* elevated surfaces */
--color-primary-600: #1A3D6E;   /* borders */
--color-primary-500: #2563EB;   /* brand blue, primary buttons */
--color-primary-400: #3B82F6;   /* interactive elements */
--color-primary-300: #60A5FA;   /* active states */
--color-primary-200: #93C5FD;   /* muted highlights */
--color-primary-100: #DBEAFE;   /* light mode backgrounds */
--color-primary-50:  #EFF6FF;   /* lightest surface */
```

**Semantic / Status:**
```css
--color-positive:    #10B981;   /* growth, good traders, mints */
--color-negative:    #EF4444;   /* contraction, burns, alerts */
--color-warning:     #F59E0B;   /* caution, mid-range */
--color-neutral:     #6B7280;   /* inactive, secondary text */
```

**Stablecoin Color Map (hardcoded — these are brand identities):**
```js
const STABLECOIN_COLORS = {
  USDC:  '#2775CA',   // Circle blue
  USDS:  '#7B61FF',   // Sky Protocol purple-blue
  DAI:   '#F5AC37',   // MakerDAO amber
  PYUSD: '#006FCF',   // PayPal blue
  RLUSD: '#00B2FF',   // Ripple cyan
  FRAX:  '#1A1A1A',   // Frax dark (use #94A3B8 on dark bg)
  BUSD:  '#F0B90B',   // Binance yellow
  LUSD:  '#745DDF',   // Liquity purple
  sUSD:  '#5AA0FF',   // Synthetix blue
};
```

**Trader Segment Color Map:**
```js
const TRADER_COLORS = {
  '🟢 Good Trader':    '#10B981',
  '🔴 Bad Trader':     '#EF4444',
  '🐳 High Value Trader':   '#2563EB',
  '🐟 Middle Value Trader': '#60A5FA',
  '🦐 Low Value Trader':    '#93C5FD',
  '🐦 Frequent User':  '#10B981',
  '🐤 Regular User':   '#F59E0B',
};
```

### 4.2 Typography

```css
--font-display: 'DM Mono', monospace;         /* headers, numbers, wallet addresses */
--font-body:    'IBM Plex Sans', sans-serif;  /* body text, labels */

--text-xs:   11px;
--text-sm:   13px;
--text-base: 15px;
--text-lg:   17px;
--text-xl:   20px;
--text-2xl:  24px;
--text-3xl:  30px;
--text-4xl:  36px;

--weight-regular: 400;
--weight-medium:  500;
--weight-semibold: 600;
--weight-bold:    700;

--leading-tight:  1.2;
--leading-normal: 1.5;
--leading-relaxed: 1.75;
```

Import via Google Fonts:
```html
<link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
```

### 4.3 Spacing Scale

```css
--space-1:  4px;
--space-2:  8px;
--space-3:  12px;
--space-4:  16px;
--space-5:  20px;
--space-6:  24px;
--space-8:  32px;
--space-10: 40px;
--space-12: 48px;
--space-16: 64px;
```

### 4.4 Border Radius

Three values only. Do not deviate.

```css
--radius-sm: 4px;    /* inputs, small chips */
--radius-md: 8px;    /* cards, panels */
--radius-lg: 12px;   /* modals, large containers */
```

### 4.5 Shadows

```css
--shadow-sm: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.08);
--shadow-md: 0 4px 6px rgba(0,0,0,0.1), 0 2px 4px rgba(0,0,0,0.06);
--shadow-lg: 0 10px 15px rgba(0,0,0,0.1), 0 4px 6px rgba(0,0,0,0.05);
```

Dark mode shadows use `rgba(0,0,0,0.4)` multiplier instead.

### 4.6 Animation

```css
--ease-out: cubic-bezier(0.0, 0.0, 0.2, 1);
--ease-in-out: cubic-bezier(0.4, 0.0, 0.2, 1);
--duration-fast: 120ms;
--duration-normal: 220ms;
--duration-slow: 380ms;
```

Stagger rule: when multiple cards or chart bars animate in together, add `animation-delay` increments of `40ms` per element.

### 4.7 Dark / Light Mode

Use a `data-theme="dark"` or `data-theme="light"` attribute on `<html>`. Toggle with a button in the header.

```css
/* Dark (default) */
[data-theme="dark"] {
  --bg-base:     var(--color-primary-900);
  --bg-surface:  var(--color-primary-800);
  --bg-elevated: var(--color-primary-700);
  --border:      var(--color-primary-600);
  --text-primary:   #F1F5F9;
  --text-secondary: #94A3B8;
  --text-muted:     #475569;
}

/* Light */
[data-theme="light"] {
  --bg-base:     #F8FAFC;
  --bg-surface:  #FFFFFF;
  --bg-elevated: #F1F5F9;
  --border:      #E2E8F0;
  --text-primary:   #0F172A;
  --text-secondary: #475569;
  --text-muted:     #94A3B8;
}
```

---

## 5. Component Architecture

```
src/
├── App.jsx                    # Root: fetches both endpoints, holds state
├── designSystem.js            # Exports color maps, type scale
├── components/
│   ├── layout/
│   │   ├── DashboardHeader.jsx
│   │   ├── SectionHeader.jsx
│   │   └── ThemeToggle.jsx
│   ├── primitives/
│   │   ├── KPICard.jsx
│   │   ├── SkeletonCard.jsx
│   │   ├── SkeletonChart.jsx
│   │   ├── DataBadge.jsx
│   │   └── Tooltip.jsx
│   ├── charts/
│   │   ├── MultiLineChart.jsx      # SVG, stablecoin supply over time
│   │   ├── StackedAreaChart.jsx    # SVG, market share over time
│   │   ├── DonutChart.jsx          # SVG, current supply distribution
│   │   ├── BarChart.jsx            # SVG/HTML, weekly net flow
│   │   ├── ScatterPlot.jsx         # SVG, trader volume vs active_weeks
│   │   └── HorizontalBarChart.jsx  # SVG/HTML, trader segment breakdown
│   └── sections/
│       ├── StablecoinOverview.jsx
│       ├── StablecoinFlows.jsx
│       ├── StablecoinDominance.jsx
│       ├── TraderOverview.jsx
│       ├── TraderSegments.jsx
│       └── TraderLeaderboard.jsx
├── hooks/
│   └── useEthData.js              # Fetches + processes both endpoints
└── index.css                      # CSS variables, reset, global styles
```

---

## 6. Dashboard Sections (Detailed Specs)

### 6.1 Dashboard Header
**Layout:** Full-width top bar, sticky.

**Contents:**
- Left: Dashboard title `ETH Liquidity Pulse` in `--font-display`, `--text-2xl`, `--weight-bold`
- Left sub: subtitle `Ethereum Stablecoin & Trader Intelligence`
- Right: Dark/light toggle button (icon only, no label)
- Right: Data freshness pill: `Last updated: {metadata.last_updated formatted as "Apr 29, 2026 17:41 UTC"}` + a green dot if `is_fresh: true`, amber dot if false

**No emoji in the header. No decorative sparkles. No gradient text.**

---

### 6.2 Section A: Market Snapshot (KPI Row)

**Purpose:** Answer at a glance — how big is the stablecoin market and who dominates it?

**Layout:** 5 KPI cards in a responsive row (wrap to 2 cols on mobile)

**Cards (all computed from latest row = rows[0] after sorting desc by week):**

| Card | Metric | Format |
|---|---|---|
| Total Stablecoin Supply | Sum of all `{coin} supply` in latest row | `$XX.XX B` |
| Largest Stablecoin | Coin name + supply | `USDC — $54.4B` |
| USDC Dominance | `USDC supply / total supply * 100` | `78.3%` |
| Weekly Net Issuance | Sum of all (mints + burns) in latest row | `+$X.XXB` or `-$X.XXB` with color |
| Stablecoins Tracked | Count of coins with supply > 0 in latest row | `9` |

**KPI Card anatomy:**
- Label: `--text-xs`, `--text-secondary`, `--weight-medium`, uppercase, letter-spacing 0.08em
- Value: `--text-3xl`, `--font-display`, `--weight-bold`, `--text-primary`
- Sub-label: `--text-sm`, `--text-muted` (e.g., "as of week of Apr 27")
- Trend badge: small pill showing WoW change `+2.3% ↑` in `--color-positive` or `--color-negative`
- Border-left: 3px solid matching stablecoin color or `--color-primary-500`

**Loading state:** Render `SkeletonCard` (animated pulse shimmer) while data is fetching.

---

### 6.3 Section B: Stablecoin Supply Over Time

**Business question answered:** "How has each stablecoin's supply grown or declined over the full history?"

**Chart type:** Multi-line SVG chart (fully custom, no library)

**Data:** All 399 rows, sorted ascending by `week`. Plot `{coin} supply` per week for all 9 coins.

**Specifications:**
- X-axis: weekly date labels, show every 4th week label to avoid clutter, format `MMM 'YY`
- Y-axis: supply in billions (divide by 1e9), left-aligned, 5 ticks
- Each line color-coded by `STABLECOIN_COLORS` map
- Hover: vertical hairline + floating tooltip listing all 9 coin values for that week, sorted desc
- Legend: horizontal pill legend below chart, each pill = colored dot + coin name + latest supply
- Default: show all coins. Each legend pill is a toggle to show/hide that coin's line (active/inactive state)
- Inactive line: `opacity: 0.15`, active line: `opacity: 1`, `stroke-width: 2px`
- Chart height: 320px. Responsive width.

**Tooltip anatomy:**
- Dark card with subtle border
- Week at top in `--font-display`
- Each row: `[colored dot] [COIN] [$X.XXB]`
- Sorted by supply descending

**Skeleton:** Render a gray pulse rectangle at chart height while loading.

---

### 6.4 Section C: Market Share Dominance Over Time

**Business question answered:** "How has the composition of the stablecoin market changed? Who gained or lost ground?"

**Chart type:** Stacked area SVG chart (normalized to 100%)

**Data:** Same 399-row dataset. For each week, compute each coin's share = `coin supply / sum(all coin supplies) * 100`.

**Specifications:**
- Each area color-coded by `STABLECOIN_COLORS`
- X-axis: date, same format as Section B
- Y-axis: 0% to 100%, 5 ticks at 20% intervals
- Areas stacked in order: USDC on bottom (largest), then others descending by latest supply
- Hover: tooltip shows coin name + share % at that week
- Legend: same toggle-pill pattern as Section B

---

### 6.5 Section D: Weekly Net Flow (Mints vs. Burns)

**Business question answered:** "Is money being created or destroyed on Ethereum this week? Which coins are being minted vs. burned?"

**Layout:** Two sub-panels side by side on desktop, stacked on mobile

**Left panel — Net Flow Bar Chart:**
- Bar chart (HTML/CSS-based, not SVG required here)
- Show the last 12 weeks only (slice rows[0..11], sorted desc, most recent on top or on right)
- X-axis: week dates
- Y-axis: net flow in billions ($)
- Each bar split: positive (mint-dominant) = `--color-positive`, negative (burn-dominant) = `--color-negative`
- Stacked bars: each segment = one coin's net flow for that week

**Right panel — Current Week Flow Cards:**
- For the most recent week: show a mini card per stablecoin
- Each card: coin name + color chip + mints amount (green) + burns amount (red) + net badge
- Format: `+$XM` / `-$XM` / net `+$XM`
- Sorted by absolute(net flow) descending

---

### 6.6 Section E: Trader Intelligence Overview

**Business question answered:** "What does the quality and behavior distribution of Ethereum traders look like?"

**Layout:** 4 KPI cards + 2 charts in a grid

**KPI Cards (computed from all 2000 trader rows):**

| Card | Metric |
|---|---|
| Good Trader Rate | `count(target_variable == '🟢 Good Trader') / 2000 * 100` → `XX%` |
| Median Active Weeks | Median of `active_weeks` across all rows |
| Median Tx Count | Median of `tx_count_365d` |
| Total Volume (Sample) | Sum of `total_volume` formatted as `$X.XXM` or `$X.XXK` |

**Chart 1 — Trader Quality Donut:**
- SVG donut chart
- Segments: each unique `target_variable` value (derive dynamically)
- Colors: from `TRADER_COLORS` map, with fallback to `--color-neutral`
- Center label: dominant category name + its count
- Legend below: each category with count + percentage

**Chart 2 — Volume Tier Distribution (Horizontal Bar):**
- Each unique `trader_volume_status` as a row
- Bar length = count of traders in that tier
- Color-coded by `TRADER_COLORS`
- Show count label at end of bar: `XXX traders`
- Secondary text: total volume for that tier formatted as `$X.XXM`

---

### 6.7 Section F: Trader Behavioral Matrix

**Business question answered:** "Do high-volume traders also trade more frequently? What does the active vs. passive trader landscape look like?"

**Chart type:** Scatter plot (SVG)

**Data:** All 2000 trader rows

**Axes:**
- X-axis: `active_weeks` (0 to max)
- Y-axis: `total_volume` (log scale if range is very large, otherwise linear; detect programmatically: if `max/median > 100`, use log scale)
- Point size: encode `tx_count_365d` (scale `r` from 3px to 10px using `Math.sqrt(tx_count_365d / maxTx) * 10`)
- Point color: `target_variable` value mapped via `TRADER_COLORS`

**Interactions:**
- Hover over point: tooltip showing wallet (truncated `0x1234...5678`), active_weeks, tx_count_365d, total_volume, target_variable, all three status badges
- Tooltip must be positioned to avoid viewport clipping

**Legend:**
- Color legend for `target_variable` values
- Size legend showing dot size = tx count scale (show 3 reference sizes)

**Note on performance:** 2000 SVG circles may be heavy. Render using `<canvas>` if SVG performance is degraded (detect by rendering time; switch to canvas if needed). This is a judgment call for the agent.

---

### 6.8 Section G: Trader Activity Segment Breakdown

**Business question answered:** "What combination of activity and volume defines each trader archetype? Are frequent users also high-value?"

**Layout:** Cross-tabulation heatmap (HTML table with color-coded cells)

**Build a 2D breakdown matrix:**
- Rows: each unique `trader_activity_status`
- Columns: each unique `trader_volume_status`
- Cell value: count of traders at the intersection
- Cell background: intensity map from `--color-primary-100` (low count) to `--color-primary-500` (high count), computed relative to max cell value
- Cell shows: count + percentage of total (e.g., `342 / 17.1%`)
- Row and column totals appended

---

### 6.9 Section H: Top Trader Leaderboard

**Business question answered:** "Who are the top wallets by volume, and what behavioral profile do they carry?"

**Component type:** Sortable data table

**Columns:**
| Column | Source Field | Format |
|---|---|---|
| Rank | derived | `#1`, `#2`... |
| Wallet | `wallet` | Truncated: `0x1234...5678`, clicking copies full address |
| Total Volume | `total_volume` | `$X,XXX.XX` |
| Active Weeks | `active_weeks` | `XX wks` |
| Tx Count | `tx_count_365d` | number |
| Quality | `target_variable` | Color-coded badge (strip emoji for badge label, use color) |
| Activity | `trader_activity_status` | Color-coded chip |
| Volume Tier | `trader_volume_status` | Color-coded chip |

**Default:** Top 25 rows sorted by `total_volume` desc  
**Sortable:** Click any column header to sort asc/desc. Show sort arrow indicator.  
**Pagination:** Show 25 rows at a time. Prev/Next buttons. Show `Page X of Y`.

**Row hover state:** `background: var(--bg-elevated)`, `2px` lift via `transform: translateY(-1px)`, `transition: var(--duration-fast) var(--ease-out)`

---

## 7. Loading & Error States

### 7.1 Loading (Skeleton Screens)

While both API calls are in-flight:
- KPI cards: render `SkeletonCard` — a card-shaped div with `background: linear-gradient(90deg, var(--bg-elevated) 25%, var(--border) 50%, var(--bg-elevated) 75%)` animated with `background-size: 200%` and keyframe slide
- Charts: render a gray pulse rectangle at the exact chart height
- Table: render 10 gray rows

**Animation:**
```css
@keyframes shimmer {
  0%   { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
.skeleton {
  animation: shimmer 1.5s infinite;
  border-radius: var(--radius-sm);
}
```

### 7.2 Error State

If either fetch fails, render a full-section error card:
- Icon: `⚠` (unicode, not emoji-library)
- Message: `"Failed to load {stablecoin / trader} data from API"`
- Sub-message: show the HTTP status code or error message
- Button: `Retry` — triggers re-fetch

Do not show partial data for a section that failed. Either the whole section loads or it shows the error card.

---

## 8. Interactions & UX Behaviors

### 8.1 Tooltip Behavior
- All chart tooltips appear on `mousemove` / `pointerenter`
- Tooltip must never clip outside the viewport. Check `clientX` against `window.innerWidth - tooltipWidth`. If overflow, flip to left of cursor.
- Tooltip disappears on `mouseleave`, not on click
- Transition: `opacity 120ms ease-out`

### 8.2 Chart Legend Toggles
- Every chart with multiple series has an interactive legend
- Clicking a legend item hides/shows that series: `opacity 0.15` (hidden), `opacity 1` (visible)
- Never remove hidden series from DOM — only change opacity
- Disabled legend item: strike-through label + reduced opacity

### 8.3 Table Copy-to-Clipboard
- Clicking wallet address truncation copies the full address to clipboard via `navigator.clipboard.writeText()`
- Show a transient `"Copied!"` tooltip for 1.2 seconds, then disappear

### 8.4 Theme Toggle
- Clicking the toggle switches `document.documentElement.setAttribute('data-theme', nextTheme)`
- Persist to `localStorage.setItem('eth-pulse-theme', nextTheme)` so preference survives refresh
- Read on mount: `localStorage.getItem('eth-pulse-theme') || 'dark'`
- Toggle icon: Sun for light mode, Moon for dark mode (pure CSS/SVG icon, no icon library)

### 8.5 Number Formatting Utility
Build a `formatNumber(value, decimals)` utility. Rules:
- `>= 1e9`: format as `$XX.XXB`
- `>= 1e6`: format as `$XX.XXM`
- `>= 1e3`: format as `$XX.XXK`
- `< 1e3`: format as `$XX.XX`
- Negative values: prepend `-` before `$`, not after

---

## 9. Layout & Responsiveness

### 9.1 Grid System

```css
.dashboard {
  max-width: 1440px;
  margin: 0 auto;
  padding: 0 var(--space-6);
}

.section {
  margin-bottom: var(--space-12);
}

.kpi-row {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: var(--space-4);
}

.chart-grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-6);
}

.chart-grid-3 {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: var(--space-6);
}

@media (max-width: 1024px) {
  .kpi-row { grid-template-columns: repeat(3, 1fr); }
  .chart-grid-2 { grid-template-columns: 1fr; }
  .chart-grid-3 { grid-template-columns: 1fr; }
}

@media (max-width: 640px) {
  .kpi-row { grid-template-columns: repeat(2, 1fr); }
}
```

---

## 10. Section Layout Order

Render sections in this exact order:

1. `DashboardHeader` (sticky)
2. Section A: Market Snapshot KPIs
3. Section B: Stablecoin Supply Over Time (full width)
4. Section C: Market Share Dominance (full width)
5. Section D: Weekly Net Flow (split 2-col)
6. Section E: Trader Intelligence Overview (KPIs + 2 charts)
7. Section F: Trader Behavioral Matrix / Scatter (full width)
8. Section G: Activity Segment Heatmap (full width)
9. Section H: Top Trader Leaderboard (full width)

---

## 11. Anti-Patterns to Avoid (Absolute Rules)

- **No mock data or hardcoded row data.** Ever. If the API is down, show error state.
- **No purple gradients.** The only gradients allowed are blue-range gradients defined in the design system.
- **No sparkle, star, or confetti decorations** on any heading or hero.
- **No glowing neon box-shadow** on hover. Hover = subtle lift + border color change only.
- **No generic placeholder text:** "Loading your data..." is fine. "Fetching amazing insights..." is not.
- **No oversized headings with ultra-thin body text.** Use the defined type scale.
- **No em dashes (—) in any UI copy.** Use colons or commas.
- **No fake wallet addresses** as examples in the UI. Every wallet shown must come from the API.
- **No icon libraries** (Font Awesome, Heroicons, etc.). Icons must be inline SVG or Unicode.
- **No CSS animation on every hover.** Only animate where it adds signal, not decoration.
- **No stacking of unrelated hover effects** (shadow + glow + scale + color change on the same element).
- **No border-radius values outside the 3 defined values** (`--radius-sm`, `--radius-md`, `--radius-lg`).

---

## 12. Technical Stack

| Concern | Choice |
|---|---|
| Framework | React 18 (functional components + hooks) |
| Charts | Custom SVG + HTML/CSS (no Recharts, no Chart.js, no D3) |
| Styling | CSS custom properties (no Tailwind, no styled-components) |
| State | `useState` + `useEffect` (no Redux, no Zustand) |
| Fonts | Google Fonts (DM Mono + IBM Plex Sans) |
| Build | Vite or CRA (agent's choice) |
| No external UI libraries | (no MUI, no Chakra, no shadcn) |

---

## 13. Deliverable Checklist

Before considering this complete, verify:

- [ ] Both endpoints fetched on mount, in parallel, with `Promise.all`
- [ ] Skeleton screens render while loading
- [ ] Error states render if fetch fails, with retry button
- [ ] All numerical data formatted with `formatNumber` utility
- [ ] `week` strings parsed to Date objects, sorted ascending for all time series
- [ ] Dark/light mode toggle works and persists to `localStorage`
- [ ] All chart colors reference `STABLECOIN_COLORS` or `TRADER_COLORS` maps
- [ ] All chart legends are interactive toggles
- [ ] Scatter plot tooltip shows all fields without clipping viewport
- [ ] Trader table is sortable on all columns
- [ ] Wallet address copies to clipboard on click
- [ ] Dashboard is responsive at 1440px, 1024px, and 375px breakpoints
- [ ] No hardcoded data values anywhere in the codebase
- [ ] All categorical trader values derived dynamically from API response
- [ ] `metadata.last_updated` and `metadata.next_refresh` displayed in header

---

*End of PRD. Agent: read this document in full before writing a single line of code. Build the design system first. Then data layer. Then charts. Then sections. Do not skip steps.*
