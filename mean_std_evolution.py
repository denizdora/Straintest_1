import os
import pandas as pd
import matplotlib.pyplot as plt

results_dir = "results"
mean_std_files = [f for f in os.listdir(results_dir) if f.endswith("_mean_std.txt")]
mean_std_files.sort()

df_all = pd.DataFrame()
for file in mean_std_files:
    distance = int(file.split("_")[0])
    df = pd.read_csv(os.path.join(results_dir, file), sep="\t")
    df["Distance"] = distance
    df_all = pd.concat([df_all, df], ignore_index=True)

df_pivot_mean = df_all.pivot(index="Distance", columns="Column", values="MeanDiff")
df_pivot_std = df_all.pivot(index="Distance", columns="Column", values="StdDev")

# Plotting
for col in df_pivot_mean.columns:
    plt.figure(figsize=(6, 4))
    plt.plot(df_pivot_mean.index, df_pivot_mean[col], marker='o', label='Mean')
    plt.fill_between(df_pivot_std.index,
                     df_pivot_mean[col] - df_pivot_std[col],
                     df_pivot_mean[col] + df_pivot_std[col],
                     color='gray', alpha=0.3, label='±1 Std Dev')
    plt.title(f"Mean and StdDev of {col} vs Distance")
    plt.xlabel("Distance [mm]")
    plt.ylabel("Δλ [nm]")
    plt.gca().invert_xaxis()  # reverse direction
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{col.replace('[','').replace(']','').replace(' ','_')}_evolution.png")
    plt.close()
