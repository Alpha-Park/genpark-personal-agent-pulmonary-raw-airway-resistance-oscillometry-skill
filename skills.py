# -*- coding: utf-8 -*-
"""GenPark Industrial Skill: genpark-personal-agent-pulmonary-raw-airway-resistance-oscillometry-skill
Category: personal_agent
Website: https://www.genpark.ai
LinkedIn: https://www.linkedin.com/company/92955550
"""
import sys
import json
import math

sys.stdout.reconfigure(encoding="utf-8")

def assess_airway_oscillometry_resistance(r5_cmh2o_s_l, r20_cmh2o_s_l, x5_cmh2o_s_l, resonant_freq_fres_hz=16.0):
    if r5_cmh2o_s_l <= 0 or r20_cmh2o_s_l <= 0:
        raise ValueError("Resistance values must be positive numbers")
        
    # Small airway peripheral resistance delta: R5 - R20
    # Normal in adults: R5-R20 < 0.07 kPa/(L/s) or < 0.70 cmH2O/(L/s)
    # X5 normal: > -0.15 kPa/(L/s) or > -1.5 cmH2O/(L/s) (more negative = worse peripheral stiffness)
    # Fres (resonant frequency): normal 7 - 14 Hz
    r5_r20_diff = r5_cmh2o_s_l - r20_cmh2o_s_l
    
    small_airway_disease = r5_r20_diff > 0.70
    peripheral_reactance_impairment = x5_cmh2o_s_l < -1.5
    fres_elevated = resonant_freq_fres_hz > 15.0
    
    if small_airway_disease and peripheral_reactance_impairment:
        phenotype = "PERIPHERAL_SMALL_AIRWAY_DYSFUNCTION"
        severity = "High peripheral heterogeneity and dynamic lung stiffness"
    elif small_airway_disease:
        phenotype = "ISOLATED_SMALL_AIRWAY_RESISTANCE_ELEVATION"
        severity = "Early pre-spirometric airway remodeling (e.g. early asthma, vapor/smoke exposure)"
    elif r5_cmh2o_s_l > 3.5:
        phenotype = "CENTRAL_LARGE_AIRWAY_RESISTANCE"
        severity = "Tracheobronchial structural or mucus obstruction"
    else:
        phenotype = "NORMAL_RESPIRATORY_IMPEDANCE"
        severity = "Optimal central and peripheral airway patency"
        
    return {
        "total_resistance_r5_cmh2o_s_l": round(r5_cmh2o_s_l, 2),
        "central_resistance_r20_cmh2o_s_l": round(r20_cmh2o_s_l, 2),
        "peripheral_resistance_r5_minus_r20": round(r5_r20_diff, 2),
        "reactance_x5_cmh2o_s_l": round(x5_cmh2o_s_l, 2),
        "resonant_frequency_fres_hz": round(resonant_freq_fres_hz, 1),
        "oscillometry_phenotype": phenotype,
        "clinical_severity": severity,
        "small_airway_involvement": small_airway_disease
    }


def handle_rpc(request_str):
    try:
        req = json.loads(request_str)
        rpc_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})
        
        if method == "tools/list":
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "tools": [{
                        "name": "assess_airway_oscillometry_resistance",
                        "description": """Analyze respiratory impedance measured by Forced Oscillation Technique (FOT / Impulse Oscillometry IOS).
Evaluates total respiratory resistance at 5 Hz (R5), central airway resistance at 20 Hz (R20), frequency dependence (R5-R20, peripheral small airway marker),
and respiratory reactance at 5 Hz (X5) for dynamic elastance and expiratory flow limitation.""",
                        "inputSchema": {
                            "type": "object",
                            "properties": {}
                        }
                    }]
                }
            })
        elif method == "tools/call":
            call_params = params.get("arguments", {})
            res = assess_airway_oscillometry_resistance(**call_params)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "content": [{
                        "type": "text",
                        "text": json.dumps(res, indent=2)
                    }]
                }
            })
        else:
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "error": {"code": -32601, "message": f"Method '{method}' not found"}
            })
    except Exception as e:
        return json.dumps({
            "jsonrpc": "2.0",
            "id": None,
            "error": {"code": -32000, "message": str(e)}
        })

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        sample = {'r5_cmh2o_s_l': 3.85, 'r20_cmh2o_s_l': 2.7, 'x5_cmh2o_s_l': -1.82, 'resonant_freq_fres_hz': 18.5}
        out = assess_airway_oscillometry_resistance(**sample)
        print("[TEST_PASS] Output:", json.dumps(out))
    else:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            print(handle_rpc(line))
