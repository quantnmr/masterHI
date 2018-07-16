# masterHI

masterHI is an semi-automatic script generator for the processing of **Bruker formatted** non-uniformally sampled **3-dimensional** data by the **hmsIST program**. We exploit the **nmrPipe** data format and Fourier Transform functions to aid in this process.

The basic workflow of non-uniformally sampled data reconstruction is:

* conversion from Bruker format to nmrPipe format

* a Fourier transform of the direct dimension first along with phase correction

* a reconstruction step of all the indirect 2D planes for each point in the processed direct dimension

* a final Fourier transform of the indirect 2D planes

These four steps are carried out by hmsIST by using seven independent scripts that perform each task along the processing pipeline - masterHI will create these scripts for you. They are called (and do):

* **convert.com** (conversion from Bruker to nmrPipe format)

* **phase.com** (Fourier transforms and phases direct dimension) and **prepare4recon**.com (prepares data for reconstruction)

* **recon.py** and **hmsist.com** (parallelizes instances of hmsist.com for reconstruction) and **prepare4ft.com** (reformats the data)

* **ft.com** (performs the final Fourier transformation of the 2 indirect dimensions)


## The Good News

The good news is masterHI generates and executes these scripts. You interact with masterHI on the command line by using command line arguments. These arguments are stored between steps so they only need to be given once unless you want to change them later during processing or reprocessing. Many of these options are gathered from the data directory so are automatically acquired for you and don't need to be provided as command line arguments. You can always override these options with command line arguments.

## Example processing (lets get started quickly version)

### Two-Step processing

The simplest way to do a reconstruction breaks down into two commands. The first command does steps 1 and 2 above, and the second command does steps 3 and 4.

**First Command:**

```
> masterHI --conv --phasecheck
```

This will launch nmrDraw and show you the FIDs of the first sampled point. Use nmrDraw to find the correct phase.

**Second Command:**

```
> masterHI --phasecheck --phase0 xx.xx --phase1 xx.xx --recon --ft
```

Where xx.xx are the correct phases. Keep in mind, you can drop the `--phase1` or even the `--phase0` if either one is actually zero.

And that is it. the '--recon' and '--ft' flags will automatically take care of the rest - but it may not do everything you want.

### Step by Step Processing

#### Step 1: Conversion

Convert the data from Bruker to nmrPipe format with:

```
> masterHI --conv
```

This will fail if the following files are not in the data directory:

* nuslist
* ser
* acqus
* acqu2s
* acqu3s
* pulseprogram


#### Step 2: Fourier Transform of direct dimension and phase check

The first dimension is directly acquired and can be processed with a regular FT - but we must correct for the phase. To do so, execute:

```
> masterHI --phasecheck
```

This takes the first 4 FIDs (the first sampled point), does an FT on them and loads the result into nmrDraw. In nmrDraw you can usually find one or two FIDs out of these four with good signal and correct the phase as you would normally do so in nmrDraw. Not the phase correction. Lets say it is 39.2 for phase 0 (p0) and no phase correction for phase 1 (p1). We check we have the phases correct by executing:

```
> masterHI --phasecheck --phase0 39.2 --phase1 0
```

Note: you can simply not add the `--phase1` argument to make things briefer.

This will redo the transformation and load the result in nmrDraw for you to view again. Make any other fine adjustments if you think they are needed and repeat the above command. Keep in mind that if you found you needed, say, another 5 degrees correction, you should use `--phase0 44.2`, not `--phase0 5.0`. Always check that you are happy with the phase before moving on. You can simply run:

```
> masterHI --phasecheck
```

as a final check.

#### Step 3: Reconstruction

Reconstruction can take many command line variables but mostly what you will want is default or can be detected from the data directory. The simplest thing to do, which will work in probably about 95% of cases is:

```
> masterHI --recon
```

Briefly, this will FT and phase correct all the data transpose it to the indirect dimensions are ready for reconstruction. It will then start the reconstruction. It will automatically detect how many cpus/threads it can use and will use 100% of the resources it can. To limit the number of concurrent processes, use the `--proc` argument:

```
> masterHI --recon --proc 2
```
This will only use two concurrent processes.

You should see an output that looks something like this:

```
Preparing Sampled Points for Full Reconstruction (prepare4recon.com)
FT       412 of 412    H     
Performing Reconstruction (recon.py / hmsist.com)
[####----------------------------] 15.33% done
```

Finally, it will reorder the data for the final step. It will output something like this during that step:

```
Moving from PHF to standard nmrPipe data order
```

#### Step 4: Final Fourier Transform of Indirect Dimensions

To complete the processing, a final FT of the indirect dimensions is needed. We do that with the following command:

```
> masterHI --ft
```

This generates a generic nmrPipe script that does window functions and zero filling with standard parameters. The necessary Fourier Transforms with various flags set like '-alt' or '-neg' are autodetected, but you should not rely on these. It will probably work in most cases, but you should check the 2D projections that are automatically created for you by the above command. They are written out as something like this:

```
Reading Projection: H/C
Reading Projection: H/N
Reading Projection: C/N
Writing Projection: H.C.dat
Writing Projection: H.N.dat
Writing Projection: C.N.dat
```

So you would for example load the 'H.N.dat' file into nmrDraw and check that it looks correctly orientated. Same for 'H.C.dat'. Details of problems to look for and how to fix them are given below.

The final reconstrcuted spectrum is written out as **3Dspectrum.dat**. This file can be directly viewed in nmrDraw as well.



## Detailed Example

Below is a detailed example where many of the command line options are used and explained along the way. Sorry, its wordy - but necessary to describe all the options.

### Step 1: Conversion

We begin by converting the data from Bruker format to nmrPipe format. Bruker raw data is stored in the 'ser' file within the Bruker data directory, but in order to get frequency referencing information and certain other details, masterHI looks for acqus, acqu2s, acqu3s, puleprogram and nuslist files as well. These files must all exist in the data directory for masterHI to proceed. They should however, all be there. So to convert, move to the data directory and run:

```
> masterHI --conv
```

N.B. All command line options are given with double-dashes ('--').

This creates a file called 'fid.com' and executes it.

#### Option: Doing a reconstruction in a different directory than the data directory

Alternatively you can run the script from any directory to keep the processing out of the data directory. For example its common to create a processing directory below the data directory and work in there. But you must indicate where the data directory is. For example:

```
> mkdir PROC
> cd PROC
> masterHI --conv --dir ..
```
#### Option: Controlling number of samples used in reconstruction

Sometimes you might want to use less samples than originally requested at the start of data acquisition. There are two main reasons why you would want to do this: 1) The experiment was terminated early for some reason so not all points where acquired or 2) Acquisition is not finished yet but you want to see how its all going so far. TO be able to get a decent reconstruction under these circumstances it is best to have acquired your samples randomly. You should always do this anyway.

Anyway, to limit the number of samples used, use the --nsamples argument when converting the data. For example, you originally wanted to collect 500 samples but the cryoprobe warmed up after collecting 250. Ugh - I know. But now you have a serial file with only 250 sampled points in it. No sweat, just run:

```
> masterHI --conv --nsamples 250
```

This will only convert the first 250 sampled points and will also limit the 'nuslist' file used later on during reconstruction.

Now, lets say you are running a 4 day experiment with 4000 samples to be collected but want to make sure you are not wasting spectrometer time. So, after say 12 hours you have collected only 500 samples. No problem. Again, just run:

```
> masterHI --conv --nsamples 500
```

and complete the reconstruction as usual.

### Step 2: Phase correction in first dimension.
