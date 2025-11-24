# ============================================================
#  Hydrology Example – Unit Hydrograph Derivation in Colab
#  Author: Mirza (Example Workflow)
# ============================================================
# ============================================================
#  AUTOMATED UNIT HYDROGRAPH GENERATOR (Google Colab Version)
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from google.colab import files

plt.style.use('seaborn-v0_8-whitegrid')

# ============================================================
# 1. Create and download a CSV template for clients
# ============================================================
template = pd.DataFrame({
    "Time_hr": np.arange(0, 12, 1),
    "Rainfall_in_hr": [0, 0.5, 1.5, 1.5, 0.5, 0, 0, 0, 0, 0, 0, 0],
    "Discharge_cfs": [100, 100, 300, 700, 1000, 800, 600, 400, 300, 200, 100, 100]
})

template.to_csv("UnitHydrograph_Template.csv", index=False)
print("✅ CSV template generated: UnitHydrograph_Template.csv")
print("You can share this file with clients — they only need to fill in the same 3 columns.\n")

files.download("UnitHydrograph_Template.csv")
# ============================================================
# 2. Upload client data (rainfall & discharge)
# ============================================================
print("Please upload your rainfall–discharge CSV file:")
uploaded = files.upload()

# Read the uploaded CSV file
filename = next(iter(uploaded))
df = pd.read_csv(filename)
# ============================================================
# 3. User Inputs for constants
# ============================================================
f = float(input("Enter constant infiltration rate f (in/hr): "))
baseflow = float(input("Enter baseflow (cfs): "))
# ============================================================
# 4. Core Calculations
# ============================================================
df["Rainfall_Excess_in_hr"] = np.maximum(df["Rainfall_in_hr"] - f, 0)
df["Direct_Runoff_cfs"] = df["Discharge_cfs"] - baseflow

net_rainfall = df["Rainfall_Excess_in_hr"].sum()
df["UH_cfs"] = df["Direct_Runoff_cfs"] / net_rainfall
# ============================================================
# 5. Plotting
# ============================================================

# --- (a) Unit Hydrograph ---
plt.figure(figsize=(8,5))
plt.plot(df["Time_hr"], df["UH_cfs"], 'o-', linewidth=2, color='orange', markersize=6)
plt.title("1-inch Unit Hydrograph (Direct Runoff Only)", fontsize=13)
plt.xlabel("Time (hr)")
plt.ylabel("Direct Runoff Discharge, Q$_{DRO}$ (cfs)")
plt.text(
    6, max(df["UH_cfs"])*0.8,
    f"Net rainfall: {net_rainfall:.2f} in\nf = {f} in/hr\nBaseflow = {baseflow} cfs",
    fontsize=9, bbox=dict(facecolor='wheat', alpha=0.5)
)
plt.tight_layout()
plt.show()
# --- (b) Total Hydrograph ---
plt.figure(figsize=(8,5))
plt.plot(df["Time_hr"], df["Discharge_cfs"], 'o-', linewidth=2, color='orange', markersize=6)
plt.axhline(y=baseflow, color='gray', linestyle='--', label=f'Baseflow = {baseflow} cfs')
plt.title("Total Streamflow Hydrograph (Observed Flow)", fontsize=13)
plt.xlabel("Time (hr)")
plt.ylabel("Total Discharge, Q (cfs)")
plt.legend()
plt.tight_layout()
plt.show()


# ============================================================
# 6. Output results
# ============================================================
print(f"\n✅ Computation Complete")
print(f"Net rainfall depth = {net_rainfall:.2f} inches")
print(f"Peak of Unit Hydrograph = {df['UH_cfs'].max():.1f} cfs at t = {df.loc[df['UH_cfs'].idxmax(), 'Time_hr']} hr")

# Show final computed table
display(df)

# Optionally save and download the results
df.to_csv("Computed_UnitHydrograph.csv", index=False)
files.download("Computed_UnitHydrograph.csv")
print("✅ Results saved as Computed_UnitHydrograph.csv")
