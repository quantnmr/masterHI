# masterHI

masterHI is an semi-automatic script generator for the processing of **Bruker formatted** non-uniformally sampled 3-dimensional data by the **hmsIST program**. We exploit the **nmrPipe** data format and Fourier Transform functions to aid in this process.

The basic workflow of non-uniformally sampled data reconstruction is:

* conversion from Bruker format to nmrPipe format

* a Fourier transform of the direct dimension first along with phase correction

* a reconstruction step of all the indirect 2D planes for each point in the processed direct dimension

* a final Fourier transform of the indirect 2D planes

These four steps are carried out by hmsIST by using six independent scripts that perform each task along the processing pipeline. These are typicall called:

* **convert.com** (conversion from Bruker to nmrPipe format)

* **phase.com** (Fourier transforms and phases direct dimension) and **prepare4recon**.com (prepares data for reconstruction)

* **recon.py** and **hmsist.com** (parralelizes instances of hmsist.com for reconstruction) and **prepare4ft.com** (reformats the data)

* **ft.com** (performs the final Fourier transformation of the 2 indirect dimensions)


## The Good News

The good news is masterHI generates these scripts for you at each step. It then executes the scripts. masterHI works from the command line so you provide command line options or arguments for each step. These arguments are stored between steps so they only need to be given once, unless you want to change them later during processing or reprocessing. Many of these options are gathered from the data directory so are automatically acquired for you and don't need to be provided as command line arguments. You can always override these options with command line arguments.

## Example processing

### Step 1: Conversion

We begin by converting the data from Bruker format to nmrPipe format. Bruker raw data is stored in the 'ser' file within the Bruker data directory, but in order to get frequency referencing information and certain other details, masterHI looks for acqus, acqu2s, acqu3s, puleprogram and nuslist files as well. These files must all exist in the data directory for masterHI to proceed. They should however, all be there. So to convert, move to the data directory and run:

```
> masterHI --conv
```

N.B. All command line options are given with double-dashes ('--').

This creates a file called 'fid.com' and executes it.

Alternatively you can run the script from any directory to keep the processing out of the data directory. For example its common to create a processing directory below the data directory and work in there. But you must indicate where the data directory is. For example:

```
> mkdir PROC
> cd PROC
> masterHI --conv --dir ../.
```
#### Option: Controlling number of samples requested

Sometimes you might want to use less samples than 
