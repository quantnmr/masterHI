# MHI2D & MHI3D - hmsIST NUS Processing Script Generators

MHI2D and MHI3D are modernized, semi-automatic script generators for processing **Bruker formatted** non-uniformly sampled **2-dimensional and 3-dimensional** data using the **hmsIST program**. They leverage the **nmrPipe** data format and Fourier Transform functions to streamline the reconstruction process.

- **MHI2D**: For 2D NMR data processing with nmrDraw preview for phase correction.
- **MHI3D**: For 3D NMR data processing with automatic 2D projection generation .

## Overview

The basic workflow for non-uniformly sampled data reconstruction involves:

### 2D Data (MHI2D)
1. **Conversion** from Bruker format to nmrPipe format
2. **Reconstruction** of the indirect dimension using hmsIST while **FT Processing and Phasing** the direct and indirect dimensions
3. **Review** with nmrDraw so phases, processing modes, extyractions can be adjusted


### 3D Data (MHI3D)
1. **Conversion** from Bruker format to nmrPipe format
2. **Phase checking** and correction for the direct dimension (manual step - critical for quality)
3. **Reconstruction** of the indirect dimensions using hmsIST
4. **Fourier transforms** for indirect dimensions with automatic phase detection or manual setting
5. **Automatic generation** of 2D projections and 3D spectrum 
6. **Automatic display** of all projections in nmrDraw for phase checking

Both MHI2D and MHI3D automate these processes by generating and executing the necessary scripts, while providing a modern command-line interface.

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Move the MHI2D and MHI3D files to the same execution directory as nmrPipe and make them executable:
```bash
chmod +x MHI2D MHI3D
```

## Quick Start

### 2D Data Processing (MHI2D)

#### Basic Workflow (Recommended)
The simplest way to process your 2D data is using the workflow command:

```bash
# Process 2D data in current directory
MHI2D workflow --dir /path/to/bruker/data

# Process with custom parameters
MHI2D workflow --dir /path/to/data --nsamples 100 --sthr 0.95 --ethr 0.95
```

#### Step-by-Step Processing
For more control, you can run each step individually:

```bash
# Step 1: Convert Bruker data to nmrPipe format
MHI2D convert --dir /path/to/data --nsamples 100

# Step 2: Reconstruct the NMR data
MHI2D reconstruct --dir /path/to/data --nsamples 100 --sthr 0.95 --ethr 0.95
```

### 3D Data Processing (MHI3D)

#### Recommended Processing Approach
For 3D data, it's recommended to process step-by-step to ensure proper phase checking:

```bash
# Step 1: Convert Bruker data to nmrPipe format
MHI3D convert --dir /path/to/bruker/data --nsamples 100

# Step 2: Check and set phase corrections (CRITICAL STEP)
MHI3D phasecheck --xP0 0.0 --xP1 0.0

# Step 3: Reconstruct the 3D NMR data
MHI3D reconstruct --nsamples 100 --sthr 0.95 --ethr 0.95

# Step 4: Perform Fourier transforms and generate projections
MHI3D ft --yP0 0.0 --yP1 0.0 --zP0 0.0 --zP1 0.0
```

#### Step-by-Step Processing
For more control, you can run each step individually:

```bash
# Step 1: Convert Bruker data to nmrPipe format
MHI3D convert --dir /path/to/data --nsamples 100
# Or using alias:
MHI3D C --dir /path/to/data --nsamples 100

# Step 2: Check and set phase corrections
MHI3D phasecheck --xP0 0.0 --xP1 0.0
# Or using alias:
MHI3D PC --xP0 0.0 --xP1 0.0

# Step 3: Reconstruct the NMR data
MHI3D reconstruct --nsamples 100 --sthr 0.95 --ethr 0.95
# Or using alias:
MHI3D R --nsamples 100 --sthr 0.95 --ethr 0.95

# Step 4: Perform Fourier transforms and generate projections
MHI3D ft --yP0 0.0 --yP1 0.0 --zP0 0.0 --zP1 0.0
# Or using alias:
MHI3D FT --yP0 0.0 --yP1 0.0 --zP0 0.0 --zP1 0.0
```

## Commands

### MHI2D Commands

#### Convert
Converts Bruker data to nmrPipe format.

```bash
MHI2D convert --dir /path/to/data --nsamples 100
MHI2D convert --dir /path/to/data --nsamples all
```

**Options:**
- `--dir, -d`: Data directory path
- `--nsamples, -n`: Number of samples to convert (or 'all' for all samples)

#### Reconstruct
Reconstructs the NMR data using hmsIST.

```bash
MHI2D reconstruct --dir /path/to/data --nsamples 100 --sthr 0.95 --ethr 0.95
MHI2D reconstruct --dir /path/to/data --nsamples all --sthr 0.95 --ethr 0.95
```

**Options:**
- `--dir, -d`: Data directory path
- `--nsamples, -n`: Number of samples for reconstruction (or 'all' for all samples)
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

#### Workflow
Runs both convert and reconstruct in sequence.

```bash
# Run both steps
MHI2D workflow --dir /path/to/data --nsamples 100

# Run only conversion
MHI2D workflow --dir /path/to/data --convert-only

# Run only reconstruction
MHI2D workflow --dir /path/to/data --reconstruct-only
```

#### Clean
Removes processing files, keeping only projections and spectrum files.

```bash
MHI2D clean
MHI2D clean --force  # Skip confirmation prompt
```

### MHI3D Commands

**Command Aliases:**
- `C` - Alias for `convert`
- `PC` - Alias for `phasecheck`  
- `R` - Alias for `reconstruct`
- `FT` - Alias for `ft`

#### Convert
Converts Bruker 3D data to nmrPipe format.

```bash
MHI3D convert --dir /path/to/data --nsamples 100
MHI3D convert --dir /path/to/data --nsamples all
```

**Options:**
- `--dir, -d`: Data directory path
- `--nsamples, -n`: Number of samples to convert (or 'all' for all samples)
- `--noSOL`: Skip solvent suppression
- `--EXT_L, --EXT_R`: Extract left/right regions
- `--EXT_x1, --EXT_xn`: Extract specific ppm ranges

#### Phasecheck
Checks and sets phase corrections for all three dimensions.

```bash
MHI3D phasecheck --xP0 0.0 --xP1 0.0
```

**Options:**
- `--xP0, --xP1`: X dimension phase corrections
- `--yP0, --yP1`: Y dimension phase corrections  
- `--zP0, --zP1`: Z dimension phase corrections

#### Reconstruct
Reconstructs the 3D NMR data using hmsIST.

```bash
MHI3D reconstruct --nsamples 100 --sthr 0.95 --ethr 0.95
MHI3D reconstruct --nsamples all --sthr 0.95 --ethr 0.95
```

**Options:**
- `--nsamples, -n`: Number of samples for reconstruction (or 'all' for all samples)
- `--sthr`: Start threshold [default: 0.98]
- `--ethr`: End threshold [default: 0.98]
- `--yN`: Y dimension size
- `--zN`: Z dimension size
- `--autoN`: Auto-determine N
- `--itr`: Iteration option

#### FT (Fourier Transform)
Performs Fourier transforms and generates 2D projections.

```bash
MHI3D ft --yP0 0.0 --yP1 0.0 --zP0 0.0 --zP1 0.0
```

**Options:**
- `--yP0, --yP1`: Y dimension phase corrections
- `--zP0, --zP1`: Z dimension phase corrections
- `--triplerez`: Assume processing params for standard Bruker triple resonance experiments
- `--yACQ`: Y dimension acquired
- `--zACQ`: Z dimension acquired
- `--xyz`: Output nmrPipe xyz format in addition to 3Dspectrum.dat


#### Clean
Removes processing files, keeping only projections and spectrum files.

```bash
MHI3D clean
MHI3D clean --force  # Skip confirmation prompt
```

## Required Files

### 2D Data (MHI2D)
The Bruker data directory must contain:
- `acqus` - Acquisition parameters for dimension 1
- `acqu2s` - Acquisition parameters for dimension 2
- `ser` - Raw data file
- `pulseprogram` or `pulseprogram.precomp` - Pulse sequence
- `nuslist` - Non-uniform sampling list

### 3D Data (MHI3D)
The Bruker data directory must contain:
- `acqus` - Acquisition parameters for dimension 1
- `acqu2s` - Acquisition parameters for dimension 2
- `acqu3s` - Acquisition parameters for dimension 3
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

### MHI3D-Specific Features
- **Automatic 2D projection generation**: Creates all possible 2D projections from 3D data
- **Intelligent projection naming**: Automatically names projections based on nucleus types (e.g., `1H.13C.dat`, `13C.15N.dat`)
- **Automatic nmrDraw launching**: Opens all projections in nmrDraw with proper window positioning
- **3D spectrum generation**: Creates `3Dspectrum.dat` for full 3D analysis
- **Multi-dimensional phase correction**: Handles phase corrections for all three dimensions
- **Nucleus detection**: Automatically detects H, C, N, F nuclei across all dimensions

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

# Process all available samples from nuslist
MHI2D convert --dir /path/to/data --nsamples all
MHI2D reconstruct --dir /path/to/data --nsamples all
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

### MHI2D Output Files
After successful 2D processing, you'll find:
- `test.fid` - Converted nmrPipe data
- `2Dspectrum.dat` - Final reconstructed 2D spectrum
- `convert.com` - Conversion script
- `proc.com` - Processing script
- `nuslist.used` - NUS list used for reconstruction

### MHI3D Output Files
After successful 3D processing, you'll find:
- `test.fid` - Converted nmrPipe data
- `3Dspectrum.dat` - Final reconstructed 3D spectrum
- `1H.13C.dat` - 2D projection (1H vs 13C)
- `1H.15N.dat` - 2D projection (1H vs 15N)
- `13C.15N.dat` - 2D projection (13C vs 15N)
- `convert.com` - Conversion script
- `phase.com` - Phase correction script
- `prepare4recon.com` - Pre-reconstruction script
- `recon.com` - Reconstruction script
- `ft.com` - Fourier transform script
- `nuslist.used` - NUS list used for reconstruction

**Note**: The exact names of 2D projection files depend on the nucleus types detected in your 3D experiment. MHI3D automatically generates all possible 2D projections and names them appropriately.

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
# MHI2D help
MHI2D --help
MHI2D convert --help
MHI2D reconstruct --help
MHI2D workflow --help

# MHI3D help
MHI3D --help
MHI3D convert --help
MHI3D phasecheck --help
MHI3D reconstruct --help
MHI3D ft --help
```

## Technical Details

### MHI2D Scripts
MHI2D generates and executes the following scripts:
- **convert.com**: Converts Bruker data to nmrPipe format using `bruk2pipe`
- **proc.com**: Processes data with nmrPipe functions and hmsIST reconstruction

### MHI3D Scripts
MHI3D generates and executes the following scripts:
- **convert.com**: Converts Bruker data to nmrPipe format using `bruk2pipe`
- **phase.com**: Phase correction script for the direct dimension
- **prepare4recon.com**: Pre-reconstruction processing script - transforms, extracts and phases all acquired FIDs
- **recon.com**: hmsIST reconstruction script that feeds CPUs with data to reconstruct. It launches:
    - **hmist.com**: The wrapper around the hmsIST function
- **ft.com**: Fourier transform script for all indirect dimensions

### Automatic Detection
Both scripts automatically detect:
- Data dimensions and acquisition modes
- Nucleus types (H, F, C, N) from acqus files
- Required processing parameters from Bruker files
- 3D projection naming based on nucleus combinations (MHI3D only)

## Requirements

- Python 3.6+
- Typer
- nmrPipe
- hmsIST
- Bruker data files

## License

This project maintains compatibility with the original masterHI workflow while providing a modern, user-friendly interface for NMR data processing.

**Copyright Notice**: This software is provided for educational and research purposes. You may use, modify, and distribute this software, but you must include proper attribution to the original author (Scott Anthony Robson) and maintain this copyright notice in all copies or substantial portions of the software. Do not copy, distribute, or use this software without proper attribution.
