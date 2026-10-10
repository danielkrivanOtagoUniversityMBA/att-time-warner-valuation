# ==========================================
# AT&T / TIME WARNER VALUATION ANALYSIS
# Daniel Krivan
# Strategy Implementation Case
# ==========================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar

# ==========================================
# INPUTS
# ==========================================

offer_value = 108700

tax = 0.35

EBIT = 6583
DA = 669
CAPEX = 432

WC_2015 = 4511
WC_2016 = 3782

rf = 0.0231
beta = 1.90
mrp = 0.05

cost_debt = 0.035

debt_weight = 0.21
equity_weight = 0.79

terminal_growth = 0.03

annual_synergy = 1000

# ==========================================
# WACC
# ==========================================

ke = rf + beta * mrp

kd_after_tax = cost_debt * (1 - tax)

wacc = (
    equity_weight * ke
    + debt_weight * kd_after_tax
)

print("\nWACC ANALYSIS")
print("-" * 50)

print(f"Cost of Equity: {ke:.2%}")
print(f"After-Tax Cost of Debt: {kd_after_tax:.2%}")
print(f"WACC: {wacc:.2%}")

# ==========================================
# FREE CASH FLOW
# ==========================================

delta_wc = WC_2016 - WC_2015

fcf = (
    EBIT * (1 - tax)
    + DA
    - CAPEX
    - delta_wc
)

print("\nFREE CASH FLOW")
print("-" * 50)

print(f"FCF: ${fcf:,.0f}m")

# ==========================================
# DCF FUNCTION
# ==========================================

def dcf(
    fcf0,
    growth,
    wacc,
    terminal_growth=0.03
):

    years = np.arange(1, 6)

    fcfs = [
        fcf0 * (1 + growth) ** t
        for t in years
    ]

    pv_fcfs = [
        fcfs[i] /
        ((1 + wacc) ** (i + 1))
        for i in range(5)
    ]

    terminal_fcf = (
        fcfs[-1]
        * (1 + terminal_growth)
    )

    terminal_value = (
        terminal_fcf /
        (wacc - terminal_growth)
    )

    pv_terminal = (
        terminal_value /
        ((1 + wacc) ** 5)
    )

    return (
        sum(pv_fcfs)
        + pv_terminal
    )

# ==========================================
# BASE DCF
# ==========================================

ev_7 = dcf(
    fcf,
    0.07,
    wacc
)

ev_8 = dcf(
    fcf,
    0.08,
    wacc
)

print("\nDCF VALUATION")
print("-" * 50)

print(f"7% Growth EV = ${ev_7:,.0f}m")
print(f"8% Growth EV = ${ev_8:,.0f}m")

# ==========================================
# SYNERGY VALUE
# ==========================================

synergy_value = (
    annual_synergy
    * (1 - tax)
    / wacc
)

print("\nSYNERGY VALUE")
print("-" * 50)

print(
    f"Synergy PV = ${synergy_value:,.0f}m"
)

# ==========================================
# REVERSE DCF
# ==========================================

target_value = (
    offer_value
    - synergy_value
)

def objective(g):

    value = dcf(
        fcf,
        g,
        wacc,
        terminal_growth
    )

    return abs(
        value - target_value
    )

result = minimize_scalar(
    objective,
    bounds=(0.05, 0.15),
    method="bounded"
)

print("\nREVERSE DCF")
print("-" * 50)

print(
    f"Implied Growth = {result.x:.2%}"
)

# ==========================================
# WACC SENSITIVITY
# ==========================================

print("\nWACC SENSITIVITY")
print("-" * 50)

wacc_sensitivity = []

for w in [0.08, 0.09, 0.10, 0.11, 0.12\]:

    value = (
        dcf(
            fcf,
            0.09,
            w,
            0.03
        )
        + synergy_value
    )

    wacc_sensitivity.append(
        [w, value]
    )

    print(
        f"WACC {w:.0%}: ${value:,.0f}m"
    )

# ==========================================
# SYNERGY SENSITIVITY
# ==========================================

print("\nSYNERGY SENSITIVITY")
print("-" * 50)

synergy_sensitivity = []

for s in [250, 500, 750, 1000, 1250\]:

    pv = (
        s
        * (1 - tax)
        / wacc
    )

    total = (
        dcf(
            fcf,
            0.09,
            wacc,
            0.03
        )
        + pv
    )

    synergy_sensitivity.append(
        [s, total]
    )

    print(
        f"Synergy {s}m -> EV ${total:,.0f}m"
    )

# ==========================================
# MONTE CARLO
# ==========================================

print("\nRUNNING MONTE CARLO")
print("-" * 50)

simulation_count = 50000

growth_mean = 0.09
growth_std = 0.02

synergy_mean = 1000
synergy_std = 250

wacc_mean = 0.0981
wacc_std = 0.0075

values = []

for _ in range(simulation_count):

    growth = np.random.normal(
        growth_mean,
        growth_std
    )

    synergy = np.random.normal(
        synergy_mean,
        synergy_std
    )

    wacc_sim = np.random.normal(
        wacc_mean,
        wacc_std
    )

    growth = max(growth, 0)

    synergy = max(synergy, 0)

    wacc_sim = max(
        wacc_sim,
        terminal_growth + 0.01
    )

    synergy_pv = (
        synergy
        * (1 - tax)
        / wacc_sim
    )

    total_value = (
        dcf(
            fcf,
            growth,
            wacc_sim,
            terminal_growth
        )
        + synergy_pv
    )

    values.append(
        total_value
    )

values = np.array(values)

# ==========================================
# SUMMARY
# ==========================================

mean_ev = np.mean(values)
median_ev = np.median(values)
std_ev = np.std(values)

expected_gain = np.mean(
    values - offer_value
)

probability = np.mean(
    values > offer_value
)

print("\nMONTE CARLO RESULTS")
print("-" * 50)

print(f"Mean EV: ${mean_ev:,.0f}m")
print(f"Median EV: ${median_ev:,.0f}m")
print(f"Std Dev: ${std_ev:,.0f}m")
print(f"Expected Gain: ${expected_gain:,.0f}m")
print(
    f"Probability Value Creation: {probability:.1%}"
)

# ==========================================
# PERCENTILES
# ==========================================

percentiles = np.percentile(
    values,
    [1, 5, 10, 25, 50, 75, 90, 95, 99]
)

print("\nPERCENTILES")
print("-" * 50)

for p, v in zip(
    [1,5,10,25,50,75,90,95,99],
    percentiles
):
    print(
        f"{p}%: ${v:,.0f}m"
    )

# ==========================================
# DOWNSIDE RISK
# ==========================================

prob_95 = np.mean(values < 95000)
prob_100 = np.mean(values < 100000)
prob_105 = np.mean(values < 105000)

print("\nDOWNSIDE RISKS")
print("-" * 50)

print(f"EV < $95bn:  {prob_95:.1%}")
print(f"EV < $100bn: {prob_100:.1%}")
print(f"EV < $105bn: {prob_105:.1%}")

# ==========================================
# CHART
# ========================================

plt.figure(figsize=(12,6))

plt.hist(
    values / 1000,
    bins=100,
    alpha=0.7
)

plt.axvline(
    offer_value / 1000,
    color="red",
    linestyle="--",
    linewidth=3,
    label="AT&T Offer Value"
)

plt.axvline(
    mean_ev / 1000,
    color="green",
    linestyle="--",
    linewidth=3,
    label="Expected Value"
)

plt.title(
    "Monte Carlo Valuation Distribution"
)

plt.xlabel(
    "Enterprise Value ($bn)"
)

plt.ylabel(
    "Frequency"
)

plt.legend()

# SAVE CHART

plt.savefig(
    "monte_carlo_distribution.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# ==========================================
# EXPORTS
# ==========================================

summary = pd.DataFrame({

    "Metric":[
        "Mean EV",
        "Median EV",
        "Offer Value",
        "Expected Gain",
        "Probability Value Creation",
        "WACC",
        "Implied Growth"
    ],

    "Value":[
        mean_ev,
        median_ev,
        offer_value,
        expected_gain,
        probability,
        wacc,
        result.x
    ]

})

summary.to_csv(
    "summary_results.csv",
    index=False
)

percentiles_df = pd.DataFrame({

    "Percentile":[
        1,5,10,25,50,75,90,95,99
    ],

    "Enterprise_Value": percentiles

})

percentiles_df.to_csv(
    "percentiles.csv",
    index=False
)

mc_df = pd.DataFrame({
    "Enterprise_Value": values
})

mc_df.to_csv(
    "monte_carlo_results.csv",
    index=False
)

wacc_df = pd.DataFrame(
    wacc_sensitivity,
    columns=["WACC","Enterprise_Value"]
)

wacc_df.to_csv(
    "wacc_sensitivity.csv",
    index=False
)

synergy_df = pd.DataFrame(
    synergy_sensitivity,
    columns=["Synergy","Enterprise_Value"]
)

synergy_df.to_csv(
    "synergy_sensitivity.csv",
    index=False
)

with pd.ExcelWriter(
    "att_time_warner_results.xlsx"
) as writer:

    summary.to_excel(
        writer,
        sheet_name="Summary",
        index=False
    )

    percentiles_df.to_excel(
        writer,
        sheet_name="Percentiles",
        index=False
    )

    wacc_df.to_excel(
        writer,
        sheet_name="WACC",
        index=False
    )

    synergy_df.to_excel(
        writer,
        sheet_name="Synergies",
        index=False
    )

print("\nEXPORT COMPLETE")
print("-" * 50)

print("summary_results.csv")
print("percentiles.csv")
print("monte_carlo_results.csv")
print("wacc_sensitivity.csv")
print("synergy_sensitivity.csv")
print("att_time_warner_results.xlsx")
print("monte_carlo_distribution.png")

# ==========================================
# COLAB DOWNLOADS
# ==========================================

try:

    from google.colab import files

    files.download(
        "att_time_warner_results.xlsx"
    )

    files.download(
        "monte_carlo_distribution.png"
    )

except:
    pass
