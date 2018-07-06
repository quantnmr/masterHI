# masterHI

masterHI is an semi-automatic script generator for the processing of **Bruker formatted** non-uniformally sampled 3-dimensional data by the **hmsIST program**. We exploit the **nmrPipe** data format and Fourier Transform functions to aid in this process. 

The basic workflow of non-uniformally sampled data reconstruction is:
* conversion from Bruker format to nmrPipe format
* a Fourier transform of the direct dimension first along with phase correction
* a reconstruction step of all the indirect 2D planes for each point in the processed direct dimension
* a final Fourier transform of the indirect 2D planes

These four steps are carried out by hmsIST by using 6 independent scripts that perform each task along the processing pipeline. These are typicall called:
* fid.com (conversion from Bruker to nmrPipe format)

* ft1xyz.com phases direct dimension) and ft1yzx.com (prepares data for reconstruction)

* recon.py and ist.com (parralelizes instances of ist.com for reconstruction) and phf2pipe.com (reformats the data)

* ft23.com (performs the final Fourier transformation of the 2 indirect dimensions)
