# Side-channel Observations on Lattice-based Operations

![SOLO Logo](SOLO_logo.png)

Welcome to the **SOLO** dataset repository, A Side-Channel Analysis Dataset for ML-KEM on ARM Cortex-M4. This project aims to provide the Post-Quantum Cryptography (PQC) Side-Channel Analysis (SCA) community with standardised, curated datasets to facilitate reproducible research and benchmarking of SCA attacks and countermeasures on ML-KEM (formerly CRYSTALS-Kyber).

---

## Dataset Description

The SOLO dataset consists of power consumption traces captured during the execution of **ML-KEM** decapsulation operations on an **ARM Cortex-M4** microcontroller. 

The data is provided in **HDF5 (.h5)** format. Each file contains a test bench of traces grouped with their respective public/secret variables and internal intermediate polynomial coefficients.

### HDF5 Structure

Every trace entry in the `.h5` file contains the following fields:

| Field Name | Type / Description |
| :--- | :--- |
| `wave` | The raw power consumption trace |
| **Public/Cryptographic Variables** | |
| `c` | Ciphertext |
| `m` | Message |
| `pk` | Public Key |
| `sk` | Secret Key |
| **Ciphertext Coefficient Vectors** | |
| `bp_b_vec0_evenCoeff0` / `bp_b_vec0_oddCoeff1` | Vector 0 intermediate coefficients (Even/Odd) |
| `bp_b_vec1_evenCoeff0` / `bp_b_vec1_oddCoeff1` | Vector 1 intermediate coefficients (Even/Odd) |
| **Secret Key Polynomial Vectors** | |
| `skpv_vec0_evenCoeff0` / `skpv_vec0_oddCoeff1` | Vector 0 secret key coefficients (Even/Odd) |
| `skpv_vec1_evenCoeff0` / `skpv_vec1_oddCoeff1` | Vector 1 secret key coefficients (Even/Odd) |
| **Base Multiplication Outputs** | |
| `r_vec0_even0` / `r_vec0_odd1` | Vector 0 multiplication outputs |
| `r_vec1_even0` / `r_vec1_odd1` | Vector 1 multiplication outputs |

---

## Download the Datasets

Due to file size limitations, the raw `.h5` files are hosted externally. 

* **[Download SOLO Dataset Dataset 1 (e.g., Fixed Key)](#)** `[Witheld until ** LAUNCH DATE **]`
* **[Download SOLO Dataset Dataset 2 (e.g., Random Key)](#)** `[Witheld until ** LAUNCH DATE **]`

---

## Getting Started & Best Practices

### Prerequisites
To read the dataset, you will need Python 3 with `h5py` and `numpy`.

pip install -r requirements.txt

## 📊 Case Study: TVLA Leakage Assessment

This repository includes a production-ready Test Vector Leakage Assessment (TVLA) engine to evaluate side-channel vulnerabilities in post-quantum cryptography implementations (specifically targeting ML-KEM / Kyber decapsulation cores).

### Directory Structure
Ensure your downloaded HDF5 trace containers are placed in the matching directories:
- `data/fixed/` -> Place fixed-key HDF5 files here.
- `data/random/` -> Place random-key HDF5 files here.

### Usage Instructions
The analysis script supports both sequential and randomised trace sampling to evaluate temporal hardware noise and statistical variance.

Run the assessment using the default configuration (Randomised Sampling, 500 traces):

python scripts/tvla_assessment.py

### ⚙️ Script Configuration & Customisation

The TVLA assessment script uses Python's `argparse` module via the `parse_arguments()` function. This enables flexible configuration. You can customise your execution environment in two ways: **directly editing the script's defaults** (ideal for Jupyter/ChipWhisperer Notebook cells) or **passing command-line overrides** (ideal for terminal runs).

Open `scripts/tvla_assessment.py` and modify the parameters inside `parse_arguments()` to customise the behavior:

