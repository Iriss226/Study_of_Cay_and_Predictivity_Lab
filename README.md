# CAY Lab – Study of CAY and Predictivity

## Overview

**CAY** is the consumption-wealth ratio introduced by Lettau & Ludvigson (2001).
It is a cointegrating residual from the long-run relation among consumption (`c`),
asset wealth (`a`), and labour income (`y`):

```
cay_t = c_t - β_a · a_t - β_y · y_t - const
```

CAY has been shown to be a strong predictor of excess stock-market returns.

This lab contains:

| Module | Description |
|--------|-------------|
| `cay_lab/data/` | Data loading and cleaning utilities |
| `cay_lab/analysis/` | CAY construction, decomposition, and predictive regression |
| `cay_lab/monitor/` | Rolling / expanding-window predictivity monitor |
| `tests/` | Unit tests |

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Quickstart

### 1 – Construct CAY

```python
from cay_lab.analysis.cay_builder import CayBuilder

builder = CayBuilder(df)          # df has columns: c, a, y (log-levels)
builder.fit()
print(builder.cay)                # pd.Series of cay residuals
print(builder.coef_)              # {'beta_a': ..., 'beta_y': ..., 'const': ...}
```

### 2 – Decompose CAY

```python
from cay_lab.analysis.decomposition import CayDecomposer

decomp = CayDecomposer(df, excess_returns_col='er')
decomp.fit()
print(decomp.summary())           # contribution of each component
decomp.plot_contributions()
```

### 3 – Rolling Predictivity Monitor

```python
from cay_lab.monitor.rolling_monitor import RollingPredictivityMonitor

monitor = RollingPredictivityMonitor(df, target_col='er', predictor_col='cay',
                                     window=40)
monitor.run()
print(monitor.status())           # 'ACTIVE' / 'WEAKENED' / 'LOST'
monitor.plot()
```

---

## Background

Lettau, M. and Ludvigson, S. (2001). *Consumption, Aggregate Wealth, and Expected
Stock Returns*. **Journal of Finance**, 56(3), 815–849.