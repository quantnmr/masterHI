# Changelog

All notable changes to MHI2D and MHI3D are documented here.

## [Unreleased]

### Added

- **MHI3D workflow:** `workflow` and `W` alias run convert → phasecheck → reconstruct → ft in sequence. Optional `--convert-only`, `--phasecheck-only`, `--reconstruct-only`, `--ft-only` for partial runs.
- **MHI3D `--noDraw`:** `ft` / `FT` accept `--noDraw` to skip launching nmrDraw for 2D projections (batch/headless use).
- **Progress timing:** Long-running steps print `Started <step>` and `Finished <step> (N s)` (convert, reconstruct, prepare4recon, recon, prepare4ft, ft).

### Changed

- **MHI3D reconstruction extension:** `--yN` and `--zN` work independently. When only one is given, the other is derived from `nuslist.used` (max + 1). hmsIST always receives both `-xN` and `-yN` when not using `-autoN`.
- **MHI3D scratch disk:** When `/scratch/$(whoami)` exists, use `/scratch/$(whoami)/kg_proc/<path-after-username>` for `yzx`, `yzx_ist`, `rec`; symlinks in the processing directory. `clean` removes the scratch tree. Final outputs (`3Dspectrum.dat`, 2D projections) stay on the network disk.
- **Clean parity (MHI2D / MHI3D):** Both remove `data001.dat`, `yzx`, `yzx_ist`, `fid`, and `rec` (entire directory). MHI2D previously removed only `rec/*.ft1`.
- **MHI2D `--sthr` / `--ethr`:** Now passed to hmsIST as `-i_mult` and `-e_mult` in `proc.com` (aligned with MHI3D).

### Documentation

- **README:** Design/Architecture note; config per-directory; MHI2D vs MHI3D parity (clean, `--sthr`/`--ethr`, `--yN`/`--autoN`). Typo fix: “extyractions” → “extractions”. Clean sections clarified.
- **Docstrings:** Added for `genConversion`, `genPrepare`, `genRecon`, `genFT`, `genDirectPhaseCheck`, and related helpers.

### Internal / robustness (earlier work)

- Shared `masterhi_common.py` for config, subprocess, script I/O. Explicit encoding for Bruker/nuslist files. Pickle config versioning. Scratch path safety checks. Exit-code handling for generated scripts.
