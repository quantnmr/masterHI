# masterHI

masterHI is an semi-automatic script generator for the processing of **Bruker formatted** non-uniformally sampled 3-dimensional data by the **hmsIST program**. We exploit the **nmrPipe** data format and Fourier Transform functions to aid in this process. 

The basic workflow of non-uniformally sampled data reconstruction is:
* conversion from Bruker format to nmrPipe format
* a Fourier transform of the direct dimension first, along with phase correction
* a reconstruction step of all the indirect 2D planes for each point in the processed direct dimension
* a final Fourier transform of the indirect 2D planes
