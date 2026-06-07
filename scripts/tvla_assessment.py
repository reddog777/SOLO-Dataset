#!/usr/bin/env python3
"""
SOLO Framework: Test Vector Leakage Assessment (TVLA) Case Study
Targets: ML-KEM (Kyber) Decapsulation Layer on ARM Cortex-M4
"""

import os
import argparse
import h5py
import numpy as np
import matplotlib.pyplot as plt
import cwtvla

def parse_arguments():
    """Parse command line arguments for flexible path management."""
    parser = argparse.ArgumentParser(
        description="Run Test Vector Leakage Assessment (TVLA) on SOLO HDF5 datasets."
    )
    parser.add_argument(
        '--fixed', 
        type=str,
        # Change this to match your file path
        default=r"C:\PATH\TO\SOLO-dataset\data\variable\ML-KEM_Decaps_FixedKey_10000.h5",
        help='Path to the fixed-key HDF5 file'
    )
    parser.add_argument(
        '--random', 
        type=str, 
        # Change this to match your file path
        default=r"C:\PATH\TO\SOLO-dataset\data\variable\ML-KEM_Decaps_VariableKey_10000.h5",
        help='Path to the random-key HDF5 file'
    )
    parser.add_argument(
        '--sample-size', 
        type=int, 
        default=500,
        help='Number of traces to extract from each file'
    )
    parser.add_argument(
        '--sampling',
        type=str,
        choices=['first', 'random'],
        #default='random',
        default='first',
        help="Sampling methodology: 'first' loads consecutive traces from index 0, 'random' samples randomly."
    )
    
    # 🌟 CHANGED THIS LINE TO FIX JUPYTER/IPYTHON CONFLICT:
    args, unknown = parser.parse_known_args()
    return args

def extract_trace_sample(file_path, sample_size, sampling_mode):
    """
    Opens an HDF5 trace container and extracts a sequential or random subset of power waveforms.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Target dataset file not found at: {file_path}")
        
    print(f"Reading waveforms from: {file_path} using [{sampling_mode}] sampling mode.")
    with h5py.File(file_path, 'r') as f:
        total_traces = f['wave'].shape[0]
        if sample_size > total_traces:
            print(f"⚠️ Requested {sample_size} sample size exceeds total traces ({total_traces}). Loading maximum size.")
            sample_size = total_traces
            
        # Switch selection method based on the chosen flag
        if sampling_mode == 'random':
            idx = np.sort(np.random.choice(total_traces, sample_size, replace=False))
            waveforms = np.array(f['wave'][idx])
        else:
            # 'first' mode: directly grab the consecutive block from index 0
            waveforms = np.array(f['wave'][:sample_size])
        
    return waveforms

def verify_and_format_shape(waveforms, name="Dataset"):
    """
    Verifies data layout orientation. If data is transposed, re-formats 
    to the standard configuration matrix: (traces, samples).
    """
    print(f"[{name}] Extracted trace shape: {waveforms.shape}")
    
    # Check if the array layout is inverted (e.g. sample length matches the row dimension)
    if waveforms.shape[0] == 600 and waveforms.shape[1] != 600:
        print(f"⚠️ [{name}] Array shape inverted! Automatically transposing matrix to (traces, samples)...")
        waveforms = waveforms.T
        
    return waveforms

def analyze_leakage(group_fixed, group_random):
    """
    Executes Welch's t-test statistical engine over the selected trace pools.
    """
    print("\nComputing Welch's T-Test across distribution boundaries...")
    t_val = cwtvla.t_test(group_fixed, group_random)
    
    # Extract 1D array if framework returns multi-dimensional dual-bound tracking matrices
    if len(t_val.shape) > 1:
        t_val = t_val[0]
        
    print(f"Final 1D T-Trace sequence generated. Length: {t_val.shape[0]} samples.")
    return t_val

def plot_tvla_results(t_val, peak_idx, peak_val, trough_idx, trough_val):
    """
    Renders the publication-ready TVLA evaluation plot with statistical annotations.
    """
    plt.figure(figsize=(12, 5))
    plt.plot(t_val, color='#1f77b4', linewidth=1.5, label='Welch T-Value')

    # Accentuate the points of interest (PoIs)
    plt.scatter(peak_idx, peak_val, color='#2ca02c', zorder=5, s=40, label=f'Global Peak ({peak_val:.2f})')
    plt.scatter(trough_idx, trough_val, color='#ff7f0e', zorder=5, s=40, label=f'Global Trough ({trough_val:.2f})')

    # Annotate critical statistical anomalies
    plt.annotate(f'Global Peak\n(Sample {peak_idx})', xy=(peak_idx, peak_val), 
                 xytext=(15, -10), textcoords='offset points', color='#2ca02c', weight='bold')
    plt.annotate(f'Global Trough\n(Sample {trough_idx})', xy=(trough_idx, trough_val), 
                 xytext=(15, 5), textcoords='offset points', color='#ff7f0e', weight='bold')

    # Plot the traditional side-channel security bounds
    plt.axhline(y=4.5, color='#d62728', linestyle='--', alpha=0.7, label=r'Security Threshold ($\pm$4.5)')
    plt.axhline(y=-4.5, color='#d62728', linestyle='--', alpha=0.7)

    plt.title('TVLA Leakage Characterization of ML-KEM Decapsulation Core')
    plt.xlabel('Sample Window Indicator (Temporal Line)')
    plt.ylabel('Welch T-Statistic Magnitude')
    plt.xlim(0, len(t_val))
    plt.grid(True, linestyle=':', alpha=0.5)
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.show()

def main():
    args = parse_arguments()
    
    try:
        # Load and sample trace populations
        fixed_raw = extract_trace_sample(args.fixed, args.sample_size, args.sampling)
        random_raw = extract_trace_sample(args.random, args.sample_size, args.sampling)
        
        # Verify array dimensional alignments
        group_fixed = verify_and_format_shape(fixed_raw, name="Fixed Key Group")
        group_random = verify_and_format_shape(random_raw, name="Random Key Group")
        
        # Process the TVLA matrix evaluation
        t_trace = analyze_leakage(group_fixed, group_random)
        
        # Calculate Peak/Trough Coordinates
        p_idx, p_val = np.argmax(t_trace), t_trace[np.argmax(t_trace)]
        t_idx, t_val = np.argmin(t_trace), t_trace[np.argmin(t_trace)]
        
        print(f"\n[Statistical Metrics]")
        print(f" -> Global Statistical Peak:   Sample {p_idx} | Value: {p_val:.4f}")
        print(f" -> Global Statistical Trough: Sample {t_idx} | Value: {t_val:.4f}")
        
        # Generate the visualization
        plot_tvla_results(t_trace, p_idx, p_val, t_idx, t_val)
        
    except FileNotFoundError as e:
        print(f"\n❌ Execution Error: {e}")
        print("Please point to your downloaded HDF5 files using the --fixed and --random flags.")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")

if __name__ == '__main__':
    main()