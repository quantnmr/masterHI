# MHI2D - hmsIST NUS Processing Script Generator

MHI2D is a modernized, semi-automatic script generator for processing **Bruker formatted** non-uniformly sampled **2-dimensional** data using the **hmsIST program**. It leverages the **nmrPipe** data format and Fourier Transform functions to streamline the reconstruction process.

## Overview

The basic workflow for non-uniformly sampled data reconstruction involves:

1. **Conversion** from Bruker format to nmrPipe format
2. **Processing** with nmrPipe functions of the direct dimension
3. **Reconstruction** of the indirect dimension using hmsIST
4. **Processing** with nmrPipe functions of the indirect dimension

MHI2D automates this process by generating and executing the necessary scripts, while providing a modern command-line interface with comprehensive validation and user feedback.

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Move the MHI2D file to the same execution directory as nmrPipe and make it executable:
```bash
chmod +x MHI2D
```

## Quick Start

### Basic Workflow (Recommended)
The simplest way to process your data is using the workflow command:

```bash
# Process data in current directory
MHI2D workflow --dir /path/to/bruker/data

# Process with custom parameters
MHI2D workflow --dir /path/to/data --nsamples 100 --sthr 0.95 --ethr 0.95
```

### Step-by-Step Processing
For more control, you can run each step individually:

```bash
# Step 1: Convert Bruker data to nmrPipe format
MHI2D convert --dir /path/to/data --nsamples 100

# Step 2: Reconstruct the NMR data
MHI2D reconstruct --dir /path/to/data --nsamples 100 --sthr 0.95 --ethr 0.95
```

## Commands

### Convert
Converts Bruker data to nmrPipe format.

```bash
MHI2D convert --dir /path/to/data --nsamples 100
```

**Options:**
- `--dir, -d`: Data directory path
- `--nsamples, -n`: Number of samples to convert

### Reconstruct
Reconstructs the NMR data using hmsIST.

```bash
MHI2D reconstruct --dir /path/to/data --nsamples 100 --sthr 0.95 --ethr 0.95
```

**Options:**
- `--dir, -d`: Data directory path
- `--nsamples, -n`: Number of samples for reconstruction
- `--sthr`: Start threshold [default: 0.98]
- `--ethr`: End threshold [default: 0.98]
- `--noSOL`: Skip solvent suppression
- `--xP0, --xP1`: X dimension phase corrections
- `--yP0, --yP1`: Y dimension phase corrections
- `--EXT_L, --EXT_R`: Extract left/right regions
- `--EXT_x1, --EXT_xn`: Extract specific ppm ranges
- `--yN`: Y dimension size
- `--autoN`: Auto-determine N
- `--itr`: Iteration option
- `--noDraw`: Skip automatic spectrum display

### Workflow
Runs both convert and reconstruct in sequence.

```bash
# Run both steps
MHI2D workflow --dir /path/to/data --nsamples 100

# Run only conversion
MHI2D workflow --dir /path/to/data --convert-only

# Run only reconstruction
MHI2D workflow --dir /path/to/data --reconstruct-only
```

### Clean
Removes processing files, keeping only projections and spectrum files.

```bash
MHI2D clean
MHI2D clean --force  # Skip confirmation prompt
```

## Required Files

The Bruker data directory must contain:
- `acqus` - Acquisition parameters for dimension 1
- `acqu2s` - Acquisition parameters for dimension 2
- `ser` - Raw data file
- `pulseprogram` or `pulseprogram.precomp` - Pulse sequence
- `nuslist` - Non-uniform sampling list

## Features

### Modern CLI Experience
- **Subcommands**: Organized functionality into logical commands
- **Type safety**: Better type hints and validation
- **Help system**: Built-in help for all commands and options
- **Progress indicators**: Clear feedback during processing
- **Error handling**: Comprehensive validation with helpful error messages

### Automatic Detection
- **Nucleus identification**: Automatically detects H, F, C, N based on acqus files
- **Data validation**: Checks for required Bruker files
- **Parameter extraction**: Reads acquisition parameters from Bruker files

### Configuration Management
- **Persistent settings**: Command-line options are saved between runs
- **Flexible overrides**: Change any parameter at any time
- **Directory validation**: Ensures data directory exists and contains valid Bruker data

## Common Processing Scenarios

### 15N HSQC Spectra
For 15N HSQC experiments, the 1H amide protons are typically located in the left half of the spectrum (downfield region). Use the `--EXT_L` option to extract only the relevant region:

```bash
# Process 15N HSQC with left-side extraction
MHI2D workflow --dir /path/to/15N_HSQC_data --EXT_L
```

This extracts only the left side of the spectrum, focusing on the amide region and improving processing efficiency.

### 13C HSQC/HMQC Spectra
For 13C HSQC/HMQC experiments, you might want to extract specific chemical shift ranges:

```bash
# Extract specific ppm range (e.g., 0-8 ppm for aliphatic region)
MHI2D workflow --dir /path/to/13C_HSQC_data --EXT_x1 0.0 --EXT_xn 8.0
```

### 2D Homonuclear NOESY Spectra
For 2D homonuclear NOESY experiments, you typically want the full spectrum:

```bash
# Process full NOESY spectrum (no extraction needed)
MHI2D workflow --dir /path/to/NOESY_data

# With custom phase corrections
MHI2D workflow --dir /path/to/data --xP0 0.0 --xP1 0.0 --yP0 0.0 --yP1 0.0
```

### Partial Data Processing
```bash
# Process only first 250 samples (useful for incomplete acquisitions)
MHI2D workflow --dir /path/to/data --nsamples 250
```

### Custom Processing Parameters
```bash
# Custom thresholds and no solvent suppression
MHI2D workflow --dir /path/to/data --sthr 0.95 --ethr 0.95 --noSOL
```

### Step-by-Step with Validation
```bash
# Convert first
MHI2D convert --dir /path/to/data --nsamples 100

# Then reconstruct with custom parameters
MHI2D reconstruct --dir /path/to/data --nsamples 100 --sthr 0.95 --ethr 0.95
```

## Automatic Spectrum Display

By default, MHI2D automatically opens the processed spectrum in nmrDraw after reconstruction completes. This allows you to immediately view your results without additional steps.

```bash
# Spectrum opens automatically in nmrDraw
MHI2D workflow --dir /path/to/data

# Skip automatic display (useful for batch processing)
MHI2D workflow --dir /path/to/data --noDraw
MHI2D reconstruct --dir /path/to/data --noDraw
```

**When to use `--noDraw`:**
- Batch processing multiple datasets
- Running in headless environments
- When you prefer to manually open spectra
- Automated scripts where GUI display isn't needed

## Output Files

After successful processing, you'll find:
- `test.fid` - Converted nmrPipe data
- `2Dspectrum.dat` - Final reconstructed spectrum
- `convert.com` - Conversion script
- `proc.com` - Processing script
- `nuslist.used` - NUS list used for reconstruction

## Troubleshooting

### Common Issues

**Directory not found:**
```
❌ Error: Directory '/path/to/data' does not exist!
```

**Invalid Bruker data:**
```
⚠️  Warning: Directory '/path/to/data' does not contain valid Bruker data.
   Required files: acqus, acqu2s, ser, pulseprogram (or pulseprogram.precomp), nuslist
```

**Conversion failed:**
```
❌ Conversion failed!
```

### Getting Help
```bash
# General help
MHI2D --help

# Command-specific help
MHI2D convert --help
MHI2D reconstruct --help
MHI2D workflow --help
```

## Technical Details

MHI2D generates and executes the following scripts:
- **convert.com**: Converts Bruker data to nmrPipe format using `bruk2pipe`
- **proc.com**: Processes data with nmrPipe functions and hmsIST reconstruction

The script automatically detects:
- Data dimensions and acquisition modes
- Nucleus types (H, F, C, N) from acqus files
- Required processing parameters from Bruker files

## Requirements

- Python 3.6+
- Typer
- nmrPipe
- hmsIST
- Bruker data files

## License

This project maintains compatibility with the original masterHI workflow while providing a modern, user-friendly interface for NMR data processing.

**Copyright Notice**: This software is provided for educational and research purposes. You may use, modify, and distribute this software, but you must include proper attribution to the original author (Scott Anthony Robson) and maintain this copyright notice in all copies or substantial portions of the software. Do not copy, distribute, or use this software without proper attribution.
