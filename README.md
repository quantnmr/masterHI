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

1. Clone the repository:
```bash
git clone https://github.com/quantnmr/masterHI.git
cd masterHI
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Make the scripts executable and move them to an appropriate location:
```bash
chmod +x MHI2D MHI3D

# For nmrBox users:
mv MHI2D MHI3D ~/bin/

# For other installations:
mv MHI2D MHI3D /your/nmrPipe/nmrbin.<your_platform>/
```

## Quick Start

### 2D Data Processing (MHI2D)

#### Basic Workflow (Recommended)
The simplest way to process your 2D data is using the workflow command:

```bash
# Process 2D data in current directory
MHI2D workflow --dir /path/to/bruker/data
# Or using alias:
MHI2D W --dir /path/to/bruker/data

# Process with custom parameters
MHI2D workflow --dir /path/to/data --nsamples 100 --sthr 0.95 --ethr 0.95
# Or using alias:
MHI2D W --dir /path/to/data --nsamples 100 --sthr 0.95 --ethr 0.95
```

#### Step-by-Step Processing
For more control, you can run each step individually:

```bash
# Step 1: Convert Bruker data to nmrPipe format
MHI2D convert --dir /path/to/data --nsamples 100
# Or using alias:
MHI2D C --dir /path/to/data --nsamples 100

# Step 2: Reconstruct the NMR data
MHI2D reconstruct --dir /path/to/data --nsamples 100 --sthr 0.95 --ethr 0.95
# Or using alias:
MHI2D R --dir /path/to/data --nsamples 100 --sthr 0.95 --ethr 0.95
```

### 3D Data Processing (MHI3D)

#### Recommended Processing Approach
For 3D data, it's recommended to process step-by-step to ensure proper phase checking:

```bash
# Step 1: Convert Bruker data to nmrPipe format
MHI3D convert --dir /path/to/data --nsamples 100
# Or using alias:
MHI3D C --dir /path/to/data --nsamples 100

# Step 2: Check and set phase corrections
MHI3D phasecheck 
# Or using alias:
MHI3D PC 

#This step launches an nmrDraw window, which will allow you to discover the phases and extraction 
#required for your direct dimension. You will iteratively work this step putting in values determined. 
#E.g. --xP0 0.0 --xP1 0.0 --EXT_L => zero phase correction and extracting left side of spectrum.

#N.B. Solvent suppression is AUTOMATICALLY applied for 1H direct dimension experiments (on by default).
#     It is AUTOMATICALLY disabled for non-1H direct dimensions (13C, 15N, 19F).
#     Override with --noSOL to manually disable solvent suppression for any nucleus type.

MHI3D phasecheck --xP0 0.0 --xP1 0.0 --EXT_L
# Or using alias:
MHI3D PC --xP0 0.0 --xP1 0.0 --EXT_L

# Step 3: Reconstruct the NMR data
MHI3D reconstruct --sthr 0.95 --ethr 0.95
# Or using alias:
MHI3D R --sthr 0.95 --ethr 0.95

# Step 4: Perform Fourier transforms and generate projections
MHI3D ft 
# Or using alias:
MHI3D FT 
```

## Commands

### MHI2D Commands

**Command Aliases:**
- `C` - Alias for `convert`
- `R` - Alias for `reconstruct`  
- `W` - Alias for `workflow`
- `RS` / `reset` - Alias for `reset` (clear saved configuration)

#### Convert
Converts Bruker data to nmrPipe format.

```bash
MHI2D convert --dir /path/to/data --nsamples 100
MHI2D convert --dir /path/to/data --nsamples all
```

**Automatic Directory Detection:**
When no `--dir` is specified, MHI2D automatically searches for Bruker data in:
1. Current directory (`.`)
2. Parent directory (`../`)
3. Grandparent directory (`../../`)
4. Great-grandparent directory (`../../../`)

This is particularly useful when processing data from a subdirectory while the Bruker data is in a parent directory.

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
- `--xZF`: X dimension zero filling factor
- `--yZF`: Y dimension zero filling factor
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

#### Reset
Clears all saved configuration parameters and resets to defaults.

```bash
MHI2D reset
MHI2D RS  # Alias
```

### MHI3D Commands

**Command Aliases:**
- `C` - Alias for `convert`
- `PC` - Alias for `phasecheck`  
- `R` - Alias for `reconstruct`
- `FT` - Alias for `ft`
- `RS` / `reset` - Alias for `reset` (clear saved configuration)

#### Convert
Converts Bruker 3D data to nmrPipe format.

```bash
MHI3D convert --dir /path/to/data --nsamples 100
MHI3D convert --dir /path/to/data --nsamples all
```

**Automatic Directory Detection:**
When no `--dir` is specified, MHI3D automatically searches for Bruker data in:
1. Current directory (`.`)
2. Parent directory (`../`)
3. Grandparent directory (`../../`)
4. Great-grandparent directory (`../../../`)

This is particularly useful when processing data from a subdirectory while the Bruker data is in a parent directory.

**Options:**
- `--dir, -d`: Data directory path
- `--nsamples, -n`: Number of samples to convert (or 'all' for all samples)
- `--EXT_L, --EXT_R`: Extract left/right regions
- `--EXT_x1, --EXT_xn`: Extract specific ppm ranges

#### Phasecheck
Checks and sets phase corrections for all three dimensions. Automatically detects nucleus type and enables solvent suppression for 1H experiments or disables it for non-1H nuclei.

```bash
MHI3D phasecheck --xP0 0.0 --xP1 0.0
```

**Options:**
- `--xP0, --xP1`: X dimension phase corrections
- `--yP0, --yP1`: Y dimension phase corrections  
- `--zP0, --zP1`: Z dimension phase corrections
- `--xZF`: X dimension zero filling factor
- `--noSOL`: Skip solvent suppression (overrides automatic detection based on nucleus type)
- `--EXT_L, --EXT_R`: Extract left/right regions
- `--EXT_x1, --EXT_xn`: Extract specific ppm ranges

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
- `--xZF`: X dimension zero filling factor
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
- `--yZF`: Y dimension zero filling factor
- `--zZF`: Z dimension zero filling factor
- `--triplerez`: Assume processing params for standard Bruker triple resonance experiments
- `--yACQ`: Y dimension acquired
- `--zACQ`: Z dimension acquired
- `--xyz`: Output nmrPipe xyz format in addition to 3Dspectrum.dat

**Automatic Detection and Defaults:**
MHI3D automatically detects optimal processing parameters from your Bruker acquisition files:

- **Acquisition Mode Detection**: Reads `##$FnMODE=` from `acqu2s` and `acqu3s` files to determine acquisition modes
- **Smart FT Processing**: Automatically chooses appropriate Fourier transform parameters:
  - `yACQ == '6'` or `zACQ == '6'` → Uses `-neg` flag (negative acquisition mode)
  - `yACQ == '5'` or `zACQ == '5'` → Uses `-alt` flag (alternating acquisition mode)  
  - `--triplerez` flag → Uses `-alt` flag for standard Bruker triple resonance experiments where appropriate
  - Default → Standard FT processing
- **Default Phase Corrections**: If no phase corrections are specified, uses zero phase correction (`-p0 0.0 -p1 0.0`)
- **Nucleus Detection**: Automatically detects nucleus types from `##$NUC1=` in acqus files for proper labeling

**When to use `--triplerez`:**
Use this flag for standard Bruker triple resonance experiments (e.g., HNCO, HNCA, HNCACB) where the acquisition parameters are well-established and the automatic detection should use triple resonance defaults.


#### Clean
Removes processing files, keeping only projections and spectrum files.

```bash
MHI3D clean
MHI3D clean --force  # Skip confirmation prompt
```

#### Reset
Clears all saved configuration parameters and resets to defaults.

```bash
MHI3D reset
MHI3D RS  # Alias
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
- **Automatic solvent suppression control**: Automatically detects nucleus type and enables solvent suppression for 1H direct dimension experiments, while disabling it for non-1H nuclei (e.g., 13C, 15N, 19F)

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
- **Smart Bruker parameter detection**: Automatically reads acquisition modes from Bruker files and chooses optimal processing parameters
- **Intelligent FT processing**: Automatically selects appropriate Fourier transform flags based on acquisition mode (negative, alternating, or standard)
- **Automatic solvent suppression control**: Automatically detects nucleus type and enables solvent suppression for 1H direct dimension experiments, while disabling it for non-1H nuclei (e.g., 13C, 15N, 19F)

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

### Zero Filling Control
Control zero filling for each dimension independently:

```bash
# Different zero filling for each dimension
MHI2D reconstruct --dir /path/to/data --xZF 2 --yZF 4

# Only set direct dimension zero filling
MHI2D reconstruct --dir /path/to/data --xZF 2

# Only set indirect dimension zero filling  
MHI2D reconstruct --dir /path/to/data --yZF 4

# Default behavior (auto (1) zero filling for both dimensions)
MHI2D reconstruct --dir /path/to/data
```

**Zero Filling Options:**
- `--xZF`: Controls zero filling for the direct (first) dimension
- `--yZF`: Controls zero filling for the indirect (second) dimension
- **Default**: Uses `-auto` for automatic zero filling (1 zero fill) when not specified
- **Custom**: Use integer values (e.g., `--xZF 2`, `--yZF 4`) for specific zero filling factors

### MHI3D Zero Filling Control
Control zero filling for each dimension independently in 3D processing:

```bash
# Most common: Only set indirect dimension zero filling (during FT)
MHI3D ft --yZF 4                     # Y dimension only
MHI3D ft --zZF 2                     # Z dimension only
MHI3D ft --yZF 4 --zZF 2             # Both Y and Z dimensions

# Less common: Set X dimension zero filling (rarely needed)
MHI3D PC --xP0 0 --xP1 0 --xZF 2    # During phasecheck (rarely used)
MHI3D R --xZF 2                      # During reconstruct (more relevant but still uncommon)

# Default behavior (auto zero filling for all dimensions)
MHI3D PC --xP0 0 --xP1 0
MHI3D ft
```

**3D Zero Filling Options:**
- `--xZF`: Controls zero filling for the direct (first) dimension (used in `phasecheck` and `reconstruct`)
  - **Note**: Rarely needed for `phasecheck`; more relevant for `reconstruct` but typically not necessary for most applications
- `--yZF`: Controls zero filling for the first indirect (second) dimension (used in `ft`)
- `--zZF`: Controls zero filling for the second indirect (third) dimension (used in `ft`)
- **Default**: Uses `-auto` for automatic zero filling (1 zero fill) when not specified
- **Custom**: Use integer values (e.g., `--xZF 2`, `--yZF 4`, `--zZF 2`) for specific zero filling factors

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

**MHI3D Advanced Detection:**
- **Acquisition Mode Detection**: Reads `##$FnMODE=` from `acqu2s` and `acqu3s` files
- **Smart FT Parameter Selection**: Automatically chooses appropriate Fourier transform flags:
  - Negative acquisition mode (`FnMODE=6`) → `-neg` flag
  - Alternating acquisition mode (`FnMODE=5`) → `-alt` flag
  - Standard acquisition → Default FT processing
- **Triple Resonance Optimization**: `--triplerez` flag overrides detection for standard Bruker triple resonance experiments

## Requirements

- Python 3.6+
- Typer
- nmrPipe
- hmsIST
- Bruker data files

## License

This project maintains compatibility with the original masterHI workflow while providing a modern, user-friendly interface for NMR data processing.

**Copyright Notice**: This software is provided for educational and research purposes. You may use, modify, and distribute this software, but you must include proper attribution to the original author (Scott Anthony Robson) and maintain this copyright notice in all copies or substantial portions of the software. Do not copy, distribute, or use this software without proper attribution.
