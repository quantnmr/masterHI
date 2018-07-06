#!/usr/bin/env python
from __future__ import print_function
import os.path
import argparse
import pickle



parser = argparse.ArgumentParser(description='hmsIST NUS Processing Script Generator')


parser.add_argument('--conv', default=False, action='store_true')
parser.add_argument('--dir', default=False)
parser.add_argument('--nsamples', default=False)
parser.add_argument('--phasecheck', default=False, action='store_true')
parser.add_argument('--phase0', default=False)
parser.add_argument('--phase1', default=False)
parser.add_argument('--noEXT', default=True, action='store_false')
parser.add_argument('--proc', default=False)
parser.add_argument('--itr', default=False)
parser.add_argument('--xN', default=False)
parser.add_argument('--yN', default=False)
parser.add_argument('--autoN', default=False, action='store_true')
parser.add_argument('--recon', default=False, action='store_true')
parser.add_argument('--ft23', default=False, action='store_true')
parser.add_argument('--triplerez', default=False, action='store_true')



args = parser.parse_args()


class Bruker3D(object):


    def __init__(self, data):

        self.ac1     = os.path.join(data, 'acqus')
        self.ac2     = os.path.join(data, 'acqu2s')
        self.ac3     = os.path.join(data, 'acqu3s')
        self.ser     = os.path.join(data, 'ser')
        self.pp      = os.path.join(data, 'pulseprogram')
        self.nuslist = os.path.join(data, 'nuslist')
        self.dir     = data

        self.acqDict = {0: 'undefined', 1: 'qf', 2: 'qsec', 3: 'tppi', 4: 'states', 5: 'states-tppi', 6: 'echo-antiecho'}

        # check if we are a Bruker 3D data set
        if (os.path.isfile(self.ac1) and os.path.isfile(self.ac2)
            and os.path.isfile(self.ac3) and os.path.isfile(self.ser)
            and os.path.isfile(self.pp) and os.path.isfile(self.nuslist)):
            self.valid = True
        else:
            self.valid = False
            #print('Data Directory does not seem to contain Bruker Data')

        if (self.valid == True):
            # is t2 Echo/Antiecho?
            with open(self.pp) as fp:
                # set EA in t2 to false until we detect otherwise
                self.t2EA = False
                for line in fp:
                    if 'Echo/Antiecho' in line and 't2' in line:
                        self.t2EA = True

        if (self.valid == True): # lets go read the variables we need
            # first lets get grpdly, decim, dspfvs
            # then we get 'x' dimension stuff
            with open(self.ac1) as fp:
                for line in fp:
                    if 'DECIM' in line:
                        self.decim = line.split()[1]
                    if 'DSPFVS' in line:
                        self.dspfvs = line.split()[1]
                    if 'GRPDLY' in line:
                        self.grpdly = line.split()[1]
                    if '##$TD= ' in line:
                        self.xN = line.split()[1]
                    if '##$WBST= ' in line:
                        self.xT = line.split()[1]
                    if '##$SW_h= ' in line:
                        self.xSW = line.split()[1]
                    if '##$SFO1= ' in line:
                        self.xOBS = line.split()[1]
                    if '##$O1= ' in line:
                        self.xO1 = line.split()[1]
                    if '##$BF1= ' in line:
                        self.xBF1 = line.split()[1]
                    self.xMODE = 'DQD'
                    self.xLAB = 'H'

            # now we get 'y' dimension stuff
            with open(self.ac2) as fp:
                for line in fp:
                    #if '##$TD= ' in line:
                    #    self.yN = line.split()[1]
                    #if '##$WBST= ' in line:
                    #    self.yT = line.split()[1]
                    if '##$SW_h= ' in line:
                        self.ySW = line.split()[1]
                    if '##$SFO1= ' in line:
                        self.yOBS = line.split()[1]
                    if '##$O1= ' in line:
                        self.yO1 = line.split()[1]
                    if '##$BF1= ' in line:
                        self.yBF1 = line.split()[1]
                    if '##$FnMODE= ' in line:
                        self.yACQ = line.split()[1]
                    self.yN = 4
                    self.yT = 2
                    self.yMODE = 'Real'
                    self.yLAB = 'N'

            with open(self.ac3) as fp:
                for line in fp:
                    #if '##$TD= ' in line:
                    #    self.zN = line.split()[1]
                    #if '##$WBST= ' in line:
                    #    self.zT = line.split()[1]
                    if '##$SW_h= ' in line:
                        self.zSW = line.split()[1]
                    if '##$SFO1= ' in line:
                        self.zOBS = line.split()[1]
                    if '##$O1= ' in line:
                        self.zO1 = line.split()[1]
                    if '##$BF1= ' in line:
                        self.zBF1 = line.split()[1]
                    if '##$FnMODE= ' in line:
                        self.zACQ = line.split()[1]
                    self.zN = 0 #sum(1 for line in open(self.dir+'/nuslist'))
                    self.zT = 2
                    self.zMODE = 'Real'
                    self.zLAB = 'C'

            self.xCAR = float(self.xO1) / float(self.xBF1)
            self.yCAR = float(self.yO1) / float(self.yBF1)
            self.zCAR = float(self.zO1) / float(self.zBF1)





    def genDirectPhaseCheck(self, filename, phase0=0, phase1=0, ext=True):

        script = []
        script.append('#!/bin/csh')
        script.append('# hmsIST FT along direct dimension for first samples point only')
        script.append('nmrPipe -in fid/data001.fid       \\')
        script.append('| nmrPipe -fn SOL \\')
        script.append('| nmrPipe  -fn SP -off 0.5 -end 0.98 -pow 2 -c 0.5  \\')
        script.append('| nmrPipe  -fn ZF -auto                         \\')
        script.append('| nmrPipe  -fn FT -verb                             \\')
        script.append('| nmrPipe  -fn PS -p0 {} -p1 {} -di              \\'.format(phase0, phase1))
        if (ext==True):
            script.append('| nmrPipe  -fn EXT -left -sw           \\')
        script.append('>data001.dat')

        outfile = open(filename, 'w')
        for item in script:
            outfile.write("%s\n" % item)
        outfile.close()

    def genFT23(self, filename, triplerez=False, yACQ=False, zACQ=False):

        script = []
        script.append('#!/bin/csh')
        script.append('# hmsIST FT along indirect dimensions')
        script.append('xyz2pipe -in rec/data%03d.ft1 -x \\')
        script.append('| nmrPipe  -fn SP -off 0.5 -end 0.98 -pow 2 -c 0.5 \\')
        script.append('| nmrPipe  -fn ZF -auto                       \\')
        if (triplerez == True):
            script.append('| nmrPipe  -fn FT -neg -verb                            \\')
        elif (yACQ == '6'):
            script.append('| nmrPipe  -fn FT -neg -verb                            \\')
        elif (yACQ == '5'):
            script.append('| nmrPipe  -fn FT -alt -verb                            \\')
        else:
            script.append('| nmrPipe  -fn FT -verb                            \\')
        script.append('| nmrPipe  -fn PS -p0 0.0 -p1 0.0 -di              \\')
        script.append('| nmrPipe  -fn TP \\')
        script.append('| nmrPipe  -fn SP -off 0.5 -end 0.98 -pow 2 -c 0.5 \\')
        script.append('| nmrPipe  -fn ZF -auto  \\')
        if (triplerez == True):
            script.append('| nmrPipe  -fn FT -alt -verb                       \\')
        elif (zACQ == '6'):
            script.append('| nmrPipe  -fn FT -neg -verb                            \\')
        elif (zACQ == '5'):
            script.append('| nmrPipe  -fn FT -alt -verb                            \\')
        else:
            script.append('| nmrPipe  -fn FT -verb                       \\')
        script.append('| nmrPipe  -fn PS -p0 0  -p1 0.0 -di              \\')
        script.append('| nmrPipe  -fn POLY -auto -ord 1 \\')
        script.append('| nmrPipe  -fn TP \\')
        script.append('| nmrPipe  -fn POLY -auto -ord 1 \\')
        script.append('| nmrPipe  -fn ZTP \\')
        script.append('| nmrPipe  -fn POLY -auto -ord 1 \\')
        script.append('> 3Dspectrum.dat')
        script.append('proj3D.tcl -in 3Dspectrum.dat')


        outfile = open(filename, 'w')
        for item in script:
            outfile.write("%s\n" % item)
        outfile.close()




    def genPrepare(self, filename, phase0=0, phase1=0, ext=True):

        script = []
        script.append('#!/bin/csh')
        script.append('# hmsIST FT along direct dimension and prepare for reconstruction')
        script.append('xyz2pipe -in fid/data%03d.fid -x \\')
        script.append('| nmrPipe -fn SOL \\')
        script.append('| nmrPipe  -fn SP -off 0.5 -end 0.98 -pow 2 -c 0.5  \\')
        script.append('| nmrPipe  -fn ZF -auto                         \\')
        script.append('| nmrPipe  -fn FT -verb                             \\')
        script.append('| nmrPipe  -fn PS -p0 {} -p1 {} -di              \\'.format(phase0, phase1))
        if (ext==True):
            script.append('| nmrPipe  -fn EXT -left -sw           \\')

        script.append('| pipe2xyz -ov -out yzx/data%03d.dat -z')
        script.append('rm -rf yzx_ist')
        script.append('mkdir yzx_ist')

        outfile = open(filename, 'w')
        for item in script:
            outfile.write("%s\n" % item)
        outfile.close()

    def genRecon(self, filenames, proc=0, itr=0, xN=0, yN=0):
        # lets make the recon.py file first
        script = []
        script.append('#!/usr/bin/env python')
        script.append('')
        script.append('from __future__ import print_function')
        script.append('from multiprocessing import Pool')
        script.append('import curses')
        script.append('from subprocess import call')
        script.append('import sys')
        script.append('from os import listdir')
        script.append('from os.path import isfile, join')
        script.append('from os import walk')
        script.append('')
        script.append('onlyfiles = [ f for f in listdir(sys.argv[1]) if isfile(join(sys.argv[1],f)) ]')
        script.append('onlyfiles.sort()')
        script.append('num=len(onlyfiles)')
        script.append('')
        script.append('def recon(x):')
        script.append('    global num')
        script.append('    path, dirs, files = next(walk(\'./yzx_ist\'))')
        script.append('    i = len(files)')
        script.append('    hashsize = int(num/32.0)')
        script.append('    hashes = int(float(i)/float(hashsize))')
        script.append('    for n in range(32):')
        script.append('        if n < hashes:')
        script.append('            print(\'#\', end=\'\')')
        script.append('        else:')
        script.append('            print(\'-\', end=\'\')')
        script.append('    perc = 100.0*i/num')
        script.append('    print(\'%.2f\' % perc + \' %\', end=\'\\r\')')
        script.append('    sys.stdout.flush()')
        script.append('    call(["./ist.com", x])')
        script.append('')
        if proc == 0:
            script.append('pool = Pool(None)')
        else:
            script.append('pool = Pool(processes='+str(proc)+')')
        script.append('it = pool.map(recon, onlyfiles)')
        outfile = open(filenames[0], 'w')
        for item in script:
            outfile.write("%s\n" % item)
        outfile.close()
        script = []
        script.append('#!/bin/csh')
        script.append('set F = $1')
        script.append('  set in = $F:t')
        script.append('  set out = $F:t:r.phf')
        script.append('')
        #script.append('echo $out')
        if (itr == 0 and xN == 0 and yN == 0):
            script.append('hmsIST -dim 2 -incr 1 -autoN 1 -user 1 -itr 250 -verb 0 -ref 0 -vlist nuslist.used < ./yzx/${in} >! ./yzx_ist/${out}')
        elif (itr != 0 and xN == 0 and yN == 0):
            script.append('hmsIST -dim 2 -incr 1 -autoN 1 -user 1 -itr '+str(itr)+' -verb 0 -ref 0 -vlist nuslist.used < ./yzx/${in} >! ./yzx_ist/${out}')
        elif (itr == 0 and xN != 0 and yN != 0):
            script.append('hmsIST -dim 2 -incr 1 -xN '+str(xN)+' -yN '+str(yN)+' -user 1 -itr 250 -verb 0 -ref 0 -vlist nuslist.used < ./yzx/${in} >! ./yzx_ist/${out}')
        elif (itr != 0 and xN != 0 and yN != 0):
            script.append('hmsIST -dim 2 -incr 1 -xN '+str(xN)+' -yN '+str(yN)+' -user 1 -itr '+str(itr)+' -verb 0 -ref 0 -vlist nuslist.used < ./yzx/${in} >! ./yzx_ist/${out}')
        outfile = open(filenames[1], 'w')
        for item in script:
            outfile.write("%s\n" % item)
        outfile.close()
        script = []
        script.append('#!/bin/csh')
        script.append('xyz2pipe -in yzx_ist/data%03d.phf | phf2pipe -user 1 | pipe2xyz -out rec/data%03d.ft1')
        outfile = open(filenames[2], 'w')
        for item in script:
            outfile.write("%s\n" % item)
        outfile.close()



    def genConversion(self, filename, ns=None):
        if (self.valid == False):
            print('Data Directory does not seem to contain Bruker Data')
            return 1

        if (ns == None):
            self.nsamples = sum(1 for line in open(self.dir+'/nuslist'))
        else:
            self.nsamples = ns
        self.zN = self.nsamples

        script = []

        script.append('#!/bin/csh')
        script.append('# hmsIST conversion script for Bruker 3D Data')
        script.append('')
        script.append('bruk2pipe -in {} \\'.format(self.ser))
        script.append('  -bad 0.0 -ext -aswap -AMX -decim {} -dspfvs {} -grpdly {}        \\'.format(self.decim,
                                                                                                     self.dspfvs,
                                                                                                     self.grpdly))
        script.append('  -xN {0: >16}   -yN {1: >16}   -zN {2: >16} \\'.format(self.xN,
                                                                               self.yN,
                                                                               self.zN))
        script.append('  -xT {0: >16}   -yT {1: >16}   -zT {2: >16} \\'.format(self.xT,
                                                                               self.yT,
                                                                               self.zT))
        script.append('  -xMODE {0: >13}   -yMODE {1: >13}   -zMODE {2: >13} \\'.format(self.xMODE, self.yMODE, self.zMODE))
        script.append('  -xSW {0: >15}   -ySW {1: >15}   -zSW {2: >15} \\'.format(round(float(self.xSW),5),
                                                                                  round(float(self.ySW),5),
                                                                                  round(float(self.zSW),5)))
        script.append('  -xOBS {0: >14}   -yOBS {1: >14}   -zOBS {2: >14} \\'.format(round(float(self.xOBS),5),
                                                                                     round(float(self.yOBS),5),
                                                                                     round(float(self.zOBS),5)))
        script.append('  -xCAR {0: >14}   -yCAR {1: >14}   -zCAR {2: >14} \\'.format(round(float(self.xCAR),5),
                                                                                     round(float(self.yCAR),5),
                                                                                     round(float(self.zCAR),5)))
        script.append('  -xLAB {0: >14}   -yLAB {1: >14}   -zLAB {2: >14} \\'.format(self.xLAB,
                                                                                     self.yLAB,
                                                                                     self.zLAB))
        script.append('  -ndim              3   -aq2D        Complex                        \\')
        if self.t2EA == True:
            script.append('| nmrPipe -fn MAC -macro $NMRTXT/ranceY.M -noRd -noWr                \\')

        else:
            script.append('#| nmrPipe -fn MAC -macro $NMRTXT/ranceY.M -noRd -noWr               \\')

        script.append('| pipe2xyz -x -out ./fid/data%03d.fid -verb -ov -to 0')

        outfile = open(filename, 'w')
        for item in script:
            outfile.write("%s\n" % item)
        outfile.close()

class Options(object):
    def __init__(self):
        self.dir = False
        self.phase0 = 0
        self.phase1 = 0
        self.nsamples = 0
        self.noEXT = False
        self.itr = False
        self.autoN = False
        self.xN = False
        self.yN = False
        self.proc = False
        self.triplerez = False

        self.beenConverted = False
        self.beenPhased = False
        self.beenReconed = False
        self.beenFT23 = False



if (os.path.isfile('.masterHI.config')):
    file = open('.masterHI.config','rb')
    savedargs = pickle.load(file)

else:
    savedargs = Options()



if (args.conv): # requested a bruker to nmrpipe conversion

    if (args.dir):
        savedargs.dir = args.dir
    if (savedargs.dir):
        g = 1
    else:
        savedargs.dir = '.'


    data = Bruker3D(savedargs.dir)
    if args.nsamples:
        savedargs.nsamples = args.nsamples
        r = data.genConversion('fid.com', ns=savedargs.nsamples)
    else:
        r = data.genConversion('fid.com')

    if (r != 1):
        os.system('chmod 770 fid.com')
        print("Converting Bruker Data to nmrPipe Data Format (fid.com)")
        os.system('./fid.com')
        savedargs.beenConverted = True




if (args.phasecheck): # requested a phase correction in first dimension

    if (savedargs.beenConverted):
        data = Bruker3D(savedargs.dir)

        savedargs.noEXT = args.noEXT

        if (args.phase0 and args.phase1):
            savedargs.phase0 = args.phase0
            savedargs.phase1 = args.phase1
            savedargs.noEXT = args.noEXT

        elif (args.phase0):
            savedargs.phase0 = args.phase0
            savedargs.noEXT = args.noEXT

        elif (args.phase1):
            savedargs.phase1 = args.phase1
            savedargs.noEXT = args.noEXT



        data.genDirectPhaseCheck('ft1xyz.com', phase0=savedargs.phase0, phase1=savedargs.phase1, ext=savedargs.noEXT)

        os.system('chmod 770 ft1xyz.com')
        print("Transforming first Samples Point to test phases (ft1xyz.com)")
        os.system('./ft1xyz.com')
        os.system('nmrDraw -Ws 1000 700 -position 50 50 -in data001.dat')
        savedargs.beenPhased = True

    else:
        print('You need to Convert the Data from Bruker to nmrPipe format first')

if (args.recon): # requested a reconstruction - includes xyz->yzx and phf2pipe step

    if (savedargs.beenPhased):

        data = Bruker3D(savedargs.dir)
        savedargs.noEXT = args.noEXT
        if (args.nsamples):
            savedargs.nsamples = args.nsamples
        print(savedargs.nsamples)
        data.genPrepare('ft1yzx.com', phase0=savedargs.phase0, phase1=savedargs.phase1, ext=savedargs.noEXT)
        os.system('chmod 770 ft1yzx.com')
        print("Preparing Sampled Points for Full Reconstruction (ft1yzx.com)")
        os.system('./ft1yzx.com')

        if (args.proc):
            savedargs.proc = args.proc
        if (args.itr):
            savedargs.itr = args.itr
        if (args.xN and args.yN):
            savedargs.xN = args.xN
            savedargs.yN = args.yN
        if (args.autoN):
            savedargs.autoN = args.autoN
            savedargs.xN = 0
            savedargs.yN = 0

        data.genRecon(['recon.py', 'ist.com', 'phf2pipe.com'], proc=savedargs.proc, itr=savedargs.itr, xN=savedargs.xN, yN=savedargs.yN)
        os.system('chmod 770 recon.py ist.com phf2pipe.com')
        print("Performing Reconstruction (recon.py / ist.com)")

        os.system('cp '+str(data.nuslist)+' nuslist.copy')
        with open('nuslist.copy') as f:
            content = f.readlines()
        if not (savedargs.nsamples):
            os.system('cp nuslist.copy nuslist.used')
        else:
            outfile = open('nuslist.used', 'w')
            for i in range(int(savedargs.nsamples)):
                outfile.write("%s" % content[i])
            outfile.close()

        if not (os.path.isdir("yzx_ist")):
            os.system('mkdir yzx_ist')

        os.system('./recon.py yzx/')
        print("Moving from PHF to standard nmrPipe data order")
        os.system('./phf2pipe.com')
        savedargs.beenReconed = True
    else:
        print("You need to FT and phase the direct dimension first")

if (args.ft23):
    if (savedargs.beenReconed == True):
        data = Bruker3D(savedargs.dir)
        savedargs.triplerez = args.triplerez
        print(data.yACQ, data.zACQ)
        data.genFT23('ft23.com', triplerez=savedargs.triplerez, yACQ=data.yACQ, zACQ=data.zACQ)
        os.system('chmod 770 ft23.com')
        os.system('./ft23.com')



    else:
        Print("You need to do a reconstruction of the data before the final FT of the reconstructed dimensons")

file = open('.masterHI.config','wb')
pickle.dump(savedargs, file)
