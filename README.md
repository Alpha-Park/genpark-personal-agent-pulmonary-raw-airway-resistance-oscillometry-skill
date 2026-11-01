# genpark-personal-agent-pulmonary-raw-airway-resistance-oscillometry-skill

[![GenPark AI](https://img.shields.io/badge/GenPark-AI%20Ecosystem-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark-0077b5)](https://www.linkedin.com/company/92955550)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-brightgreen.svg)](https://www.python.org/)

Forced Oscillation Technique (FOT / TremoFlo) small-airway resistance R5-R20 & reactance X5 peripheral collapse monitor.

## Overview

Part of the **GenPark Industrial Multi-Agent Skill Matrix**. Zero external pip dependencies; built purely with standard Python library modules for instant deterministic orchestration.

- **Official Web Portal**: [https://www.genpark.ai](https://www.genpark.ai)
- **Corporate LinkedIn**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)

## Tool Specification

- **Tool Name**: `assess_airway_oscillometry_resistance`
- **Category**: `personal_agent`

### Method Documentation
Analyze respiratory impedance measured by Forced Oscillation Technique (FOT / Impulse Oscillometry IOS).
Evaluates total respiratory resistance at 5 Hz (R5), central airway resistance at 20 Hz (R20), frequency dependence (R5-R20, peripheral small airway marker),
and respiratory reactance at 5 Hz (X5) for dynamic elastance and expiratory flow limitation.

## JSON-RPC 2.0 Integration

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "assess_airway_oscillometry_resistance",
    "arguments": {
    "r5_cmh2o_s_l": 3.85,
    "r20_cmh2o_s_l": 2.7,
    "x5_cmh2o_s_l": -1.82,
    "resonant_freq_fres_hz": 18.5
}
  }
}
```

## Running Self Tests

```bash
python skills.py --test
```
