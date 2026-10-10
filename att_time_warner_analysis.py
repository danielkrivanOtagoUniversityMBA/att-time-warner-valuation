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

kd_after_tax = cost_debt * (1-tax)

wacc = (
    equity_weight * ke
    +
    debt_weight * kd_after_tax
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
    EBIT * (1-tax)
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

    years = np.arange(1,6)

    fcfs = [
        fcf0*(1+growth)**t
      ***or t in years
    ]

    pv_fcfs***[
        fcfs[i] /
        ((1+wacc)**(i+1))
        for i in rang*(5)
    ]

    terminal_fcf = (
  *     fcfs[-1]
        *
        (1*terminal_growth)
    )

    termin*l_value = (
        terminal_fcf /*        (wacc-terminal_growth)
   *)

    pv_terminal = (
        ter*inal_value /
        ((1+wacc)**5)***  )

    return (
        sum(pv***fs)
        +
        pv_termina***   )

# ========================***===============
# BASE DCF
# ===***================================***=

ev_7 = dcf(
    fcf,
    0.07***   wacc
)

ev_8 = dcf(
    fcf,
*** 0.08,
    wacc
)

print("\nDCF ***UATION")
print("-" * 50)

print(***% Growth EV: ${ev_7:,.0f}m")
pri***f"8% Growth EV: ${ev_8:,.0f}m")
***================================***=======
# SYNERGY VALUE
# ======***================================***synergy_value = (
    annual_syn***y
    *
    (1-tax)
    /
    wa***)

print("\nSYNERGY VALUE")
prin***-" * 50)

print(
    f"Synergy P***${synergy_value:,.0f}m"
)

# ===***================================***=
# REVERSE DCF
# ==============***=========================

targe***alue = (
    offer_value -
    s***rgy_value
)

def objective(g):

*** value = dcf(
        fcf,
     ***g,
        wacc,
        termina***rowth
    )

    return abs(
   ***  value -
        target_value
 ***)

result = minimize_scalar(
   ***jective,
    bounds=(0.05,0.15),***  method="bounded"
)

print("\nR***RSE DCF")
print("-" * 50)

print***   f"Implied Growth: {result.x:.***"
)

# =========================***==============
# WACC SENSITIVIT*** ===============================***========

print("\nWACC SENSITIV***")
print("-" * 50)

for w in [0.08,0.09,0.10,0.11,0.12\]:

    valu*** (
        dcf(
            fcf,***          0.09,
            w,
 ***        0.03
        )
        +***      synergy_value
    )

    p***t(
        f"WACC {w:.0%}: "
   ***  f"${value:,.0f}m"
    )

# ===***================================***=
# SYNERGY SENSITIVITY
# ======***================================***print("\nSYNERGY SENSITIVITY")
p***t("-" * 50)

for s in [250,500,750,1000,1250\]:

    pv = (
       ***        *
        (1-tax)
      ***
        wacc
    )

    total =***        dcf(
            fcf,
  ***       0.09,
            wacc,
 ***        0.03
        )
        +***      pv
    )

    print(
     ***f"Synergy {s}m -> "
        f"EV***total:,.0f}m"
    )

# =========***==============================
#***NTE CARLO
# ====================***===================

print("\nRU***NG MONTE CARLO...")
print("-" * ***

simulation_count = 50000

grow***mean = 0.09
growth_std = 0.02

s***rgy_mean = 1000
synergy_std = 25***wacc_mean = 0.0981
wacc_std = 0.***5

values = []

for _ in range(s***lation_count):

    growth = np.***dom.normal(
        growth_mean,***      growth_std
    )

    syne*** = np.random.normal(
        syn***y_mean,
        synergy_std
    ***    wacc_sim = np.random.normal(***      wacc_mean,
        wacc_st***   )

    growth = max(
        ***wth,
        0
    )

    synerg*** max(
        synergy,
        0***  )

    wacc_sim = max(
       ***cc_sim,
        terminal_growth ***.01
    )

    synergy_pv = (
  ***   synergy
        *
        (1-***)
        /
        wacc_sim
   ***
    total_value = (
        dcf***           fcf,
            grow***           wacc_sim,
            terminal_growth
        )
        +
        synergy_pv
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
    f"Probability Value Creation: "
    f"{probability:.1%}"
)

# ==========================================
# PERCENTILES
# ==========================================

print("\nPERCENTILES")
print("-" * 50)

percentiles = np.percentile(
    values,
    [1,5,10,25,50,75,90,95,99]
)

for p,v in zip(
    [1,5,10,25,50,75,90,95,99],
    percentiles
):
    print(
        f"{p}%: ${v:,.0f}m"
    )

# ==========================================
# DOWNSIDE
# ==========================================

prob_95 = np.mean(
    values < 95000
)

prob_100 = np.mean(
    values < 100000
)

prob_105 = np.mean(
    values < 105000
)

print("\nDOWNSIDE RISKS")
print("-" * 50)

print(
    f"EV < 95bn:  {prob_95:.1%}"
)

print(
    f"EV < 100bn: {prob_100:.1%}"
)

print(
    f"EV < 105bn: {prob_105:.1%}"
)

# ==========================================
# CHART
# ==========================================

plt.figure(
    figsize=(12,6)
)

plt.hist(
    values/1000,
    bins=100,
    alpha=0.7
)

plt.axvline(
    offer_value/1000,
    color='red',
    linestyle='--',
    linewidth=3,
    label='AT&T Offer Value'
)

plt.axvline(
    mean_ev/1000,
    color='green',
    linestyle='--',
    linewidth=3,
    label='Expected Value'
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

plt.show()
