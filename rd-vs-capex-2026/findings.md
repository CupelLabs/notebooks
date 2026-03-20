# R&D vs Capital Expenditure: Big Tech's Spending Inversion

## Data source
SEC EDGAR XBRL API. Annual 10-K filings for Microsoft, Alphabet, Meta, Apple. All figures in USD, from `ResearchAndDevelopmentExpense` and `PaymentsToAcquirePropertyPlantAndEquipment` XBRL taxonomy fields. Note: Amazon excluded because they do not report R&D as a separate line item (they bundle it into "Technology and content"). NVIDIA excluded because they stopped reporting capex in the standard XBRL field after 2012 (they are fabless, so capex is small relative to R&D).

## Key finding
Three of the four largest tech companies now spend more on capital expenditure (data centers, GPUs, infrastructure) than on research and development. This is a reversal of the historical pattern.

### The crossover
| Company   | 2020 CapEx/R&D | 2025 CapEx/R&D | Current crossover |
|-----------|---------------|---------------|-------------------|
| Microsoft | 0.80          | 1.99          | Since ~2021       |
| Alphabet  | 0.81          | 1.50          | Since 2024        |
| Meta      | 0.82          | 1.21          | Since 2025        |
| Apple     | 0.39          | 0.37          | Never (going opposite direction) |

### Dollar amounts (2025)
| Company   | R&D     | CapEx   | Gap      |
|-----------|---------|---------|----------|
| Microsoft | $32.5B  | $64.6B  | +$32.1B  |
| Alphabet  | $61.1B  | $91.4B  | +$30.4B  |
| Meta      | $57.4B  | $69.7B  | +$12.3B  |
| Apple     | $34.5B  | $12.7B  | -$21.8B  |

### Growth rates (2020 → 2025)
| Company   | CapEx growth | R&D growth |
|-----------|-------------|-----------|
| Microsoft | +319%       | +68%      |
| Alphabet  | +310%       | +121%     |
| Meta      | +362%       | +212%     |
| Apple     | +74%        | +84%      |

### Aggregate (Microsoft + Alphabet + Meta)
- 2020: R&D $65.3B, CapEx $52.8B (ratio 0.81)
- 2025: R&D $151.0B, CapEx $225.7B (ratio 1.49)
- Combined capex grew from $52.8B to $225.7B (+327%)
- Combined R&D grew from $65.3B to $151.0B (+131%)

### Apple as control case
Apple went the opposite direction. In 2015, their capex *exceeded* R&D (ratio 1.39). By 2025, R&D is nearly 3x capex (ratio 0.37). They ramped R&D spending from $8.1B to $34.5B while keeping capex relatively flat ($11.2B to $12.7B). Apple bet on research. Everyone else bet on infrastructure.

### Historical context
Alphabet and Meta briefly crossed the capex > R&D threshold in 2018 (ratios 1.17 and 1.35) during their first wave of data center expansion, then pulled back. The current crossover is different: it's accelerating, driven by the AI infrastructure arms race, and shows no sign of reverting.

Microsoft's capex doubled from $28.1B (2023) to $64.6B (2025) in just two years. That $36.5B increase in annual capex is larger than most companies' entire R&D budgets.

### What this means
These companies are not becoming less innovative. R&D spending is still growing. But capex is growing 2-3x faster, driven by AI data center buildout. The ratio tells you what these companies are *becoming*: infrastructure companies with research departments, not research companies with infrastructure.
