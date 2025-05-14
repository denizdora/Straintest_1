# analyze_strain.py

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from config import DATA_FOLDER, OUTPUT_FOLDER, RESULTS_FOLDER, FILE_ORDER, ALL_SIGNAL_COLS, TOP_SURFACE_COLS, BOTTOM_SURFACE_COLS

# ---------- STEP 1: Data Load ----------
def load_and_clean_data(filename):
    filepath = os.path.join(DATA_FOLDER, filename)
    df = pd.read_csv(filepath, sep='\t')
    df = df.drop(columns=["Timestamp", "Time [s]"], errors='ignore')
    df = df[ALL_SIGNAL_COLS]
    df = df.astype(float).reset_index(drop=True)
    return df

# ---------- STEP 2: Peak Detection ----------
def detect_peaks(signal, mode='max'):
    mean_val = np.mean(signal)
    shifted = signal - mean_val
    sign_shifted = np.sign(shifted)
    crossings = [i for i in range(1, len(signal)) if sign_shifted[i - 1] <= 0 and sign_shifted[i] > 0]

    indices = []
    values = []
    for i in range(len(crossings) - 1):
        seg = signal[crossings[i]:crossings[i + 1]]
        if len(seg) == 0:
            continue
        local_idx = np.argmax(seg) if mode == 'max' else np.argmin(seg)
        global_idx = crossings[i] + local_idx
        indices.append(global_idx)
        values.append(signal[global_idx])

    baseline = signal[0]
    differences = [val - baseline if mode == 'max' else baseline - val for val in values]

    return indices, values, baseline, differences

# ---------- MAIN LOOP ----------
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

for file_name in FILE_ORDER:
    distance = os.path.splitext(file_name)[0]
    df = load_and_clean_data(file_name)

    print(f"\nProcessing: {file_name} ({distance} mm)")
    peak_differences_dict = {}

    # Peak analysis for all columns
    for col in ALL_SIGNAL_COLS:
        signal = df[col].values
        mode = 'max' if col in TOP_SURFACE_COLS else 'min'
        indices, values, baseline, differences = detect_peaks(signal, mode=mode)
        peak_differences_dict[col] = differences
        print(f"{col}: {len(differences)} peaks, mean diff = {np.mean(differences):.4f}")

    # ---------- STEP 3: Plot Δλ Differences ----------
    grouped = [TOP_SURFACE_COLS, BOTTOM_SURFACE_COLS]
    titles = [
        f"Top Surface (Tension) – {distance} mm",
        f"Bottom Surface (Compression) – {distance} mm"
    ]

    for i, group in enumerate(grouped):
        fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(8, 8), sharex=True)
        fig.suptitle(titles[i])
        for j, col in enumerate(group):
            diffs = peak_differences_dict[col]
            x = range(1, len(diffs) + 1)
            mean_diff = np.mean(diffs)
            ax = axes[j]
            ax.plot(x, diffs, marker='o', color='purple')
            ax.axhline(mean_diff, linestyle='--', color='blue', label=f"Mean = {mean_diff:.3f}")
            ax.set_title(col)
            ax.set_ylabel("Δλ [nm]")
            ax.grid(True)
            ax.legend()
        axes[-1].set_xlabel("Pulse Number")
        plt.tight_layout()
        plt.subplots_adjust(top=0.92)
        fig_name = f"{distance}_diff_plot_{'top' if i == 0 else 'bottom'}.png"
        fig_path = os.path.join(OUTPUT_FOLDER, fig_name)
        plt.savefig(fig_path)
        plt.close()
        print(f"Saved: {fig_path}")

    # ---------- STEP 4: Save Mean/Std ----------
    mean_std_list = []
    for col, diffs in peak_differences_dict.items():
        mean_val = np.mean(diffs)
        std_val = np.std(diffs)
        mean_std_list.append([col, mean_val, std_val])
    mean_std_df = pd.DataFrame(mean_std_list, columns=["Column", "MeanDiff", "StdDev"])
    mean_std_df.to_csv(os.path.join(RESULTS_FOLDER, f"{distance}_mean_std.txt"), sep='\t', index=False)
    print(f"Saved mean/std file for {distance} mm.")

    # ---------- STEP 5: Raw Signal Plot ----------
    for i, group in enumerate(grouped):
        fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(8, 8), sharex=True)
        fig.suptitle(f"{titles[i]} – Raw Signal")
        for j, col in enumerate(group):
            ax = axes[j]
            ax.plot(df[col].values, color='teal')
            ax.set_title(col)
            ax.set_ylabel("λ [nm]")
            ax.grid(True)
        axes[-1].set_xlabel("Sample Index")
        plt.tight_layout()
        plt.subplots_adjust(top=0.92)
        fig_name = f"{distance}_bragg_plot_{'top' if i == 0 else 'bottom'}.png"
        fig_path = os.path.join(OUTPUT_FOLDER, fig_name)
        plt.savefig(fig_path)
        plt.close()
        print(f"Saved raw signal plot: {fig_path}")

    # ---------- STEP 6: Derivative Plot ----------
    for i, group in enumerate(grouped):
        fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(8, 8), sharex=True)
        fig.suptitle(f"{titles[i]} – First Derivative of Signal")
        for j, col in enumerate(group):
            signal = df[col].values
            derivative = np.gradient(signal)
            ax = axes[j]
            ax.plot(derivative, color='darkorange')
            ax.set_title(f"{col} – dλ/dt")
            ax.set_ylabel("dλ [nm/sample]")
            ax.grid(True)
        axes[-1].set_xlabel("Sample Index")
        plt.tight_layout()
        plt.subplots_adjust(top=0.92)
        fig_name = f"{distance}_deriv_plot_{'top' if i == 0 else 'bottom'}.png"
        fig_path = os.path.join(OUTPUT_FOLDER, fig_name)
        plt.savefig(fig_path)
        plt.close()
        print(f"Saved derivative plot: {fig_path}")
