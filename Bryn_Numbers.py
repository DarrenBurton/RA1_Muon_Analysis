#!/usr/bin/env python
from ROOT import *
import ROOT as r
import logging,itertools
import os,fnmatch,sys
import glob, errno
from time import strftime
from optparse import OptionParser
import array
import math as m

def Data_Scaler(htbin,hist):
	  
          return float(hist)
          #Scale_Amount = {"275":float(1/0.9153),"325":float(1/0.9562),"375":float(1/0.9688),"475":float(1/0.9789),"575":1,"675":1,"775":1,"875":1}
          #if htbin in Scale_Amount and Scale_Amount[htbin] != 1:
          #    print "Scaling data due to Trigger efficiency of %s percent " % ((1/Scale_Amount[htbin]) * 100)
          #    return float(Scale_Amount[htbin])*float(hist)
          #else: return float(1.0)


class Number_Extractor(object):

  def __init__(self,passed_dictionary):

    print "\n\nGetting Numbers\n\n"
    sampleDict1 = {	"DiMuSelectionDY_0"  : {"HT":"275", "Yield": 4.776e+01 ,"SampleType":"Zmumu","Category":"DiMuon"},
	"DiMuSelectionDY_1"  : {"HT":"325", "Yield": 3.285e+01 ,"SampleType":"Zmumu","Category":"DiMuon"},
	"DiMuSelectionDY_2"  : {"HT":"375", "Yield": 2.337e+01 ,"SampleType":"Zmumu","Category":"DiMuon"},
	"DiMuSelectionDY_3"  : {"HT":"475", "Yield": 5.088e+00 ,"SampleType":"Zmumu","Category":"DiMuon"},
	"DiMuSelectionDY_4"  : {"HT":"575", "Yield": 8.923e-01 ,"SampleType":"Zmumu","Category":"DiMuon"},
	"DiMuSelectionDY_5"  : {"HT":"675", "Yield": 1.555e+00 ,"SampleType":"Zmumu","Category":"DiMuon"},
	"DiMuSelectionDY_6"  : {"HT":"775", "Yield": 0.000e+00 ,"SampleType":"Zmumu","Category":"DiMuon"},
	"DiMuSelectionDY_7"  : {"HT":"875", "Yield": 1.496e-01 ,"SampleType":"Zmumu","Category":"DiMuon"},
	"DiMuTTbar_0"  : {"HT":"275", "Yield": 4.003e-01 ,"SampleType":"TTbar","Category":"DiMuon"},
	"DiMuTTbar_1"  : {"HT":"325", "Yield": 0.000e+00 ,"SampleType":"TTbar","Category":"DiMuon"},
	"DiMuTTbar_2"  : {"HT":"375", "Yield": 1.408e-02 ,"SampleType":"TTbar","Category":"DiMuon"},
	"DiMuTTbar_3"  : {"HT":"475", "Yield": 2.433e-01 ,"SampleType":"TTbar","Category":"DiMuon"},
	"DiMuTTbar_4"  : {"HT":"575", "Yield": 0.000e+00 ,"SampleType":"TTbar","Category":"DiMuon"},
	"DiMuTTbar_5"  : {"HT":"675", "Yield": 0.000e+00 ,"SampleType":"TTbar","Category":"DiMuon"},
	"DiMuTTbar_6"  : {"HT":"775", "Yield": 0.000e+00 ,"SampleType":"TTbar","Category":"DiMuon"},
	"DiMuTTbar_7"  : {"HT":"875", "Yield": 0.000e+00 ,"SampleType":"TTbar","Category":"DiMuon"},
	"HadSelectionDY_0"  : {"HT":"275", "Yield": 4.027e+00 ,"SampleType":"Zmumu","Category":"Had"},
	"HadSelectionDY_1"  : {"HT":"325", "Yield": 4.950e-01 ,"SampleType":"Zmumu","Category":"Had"},
	"HadSelectionDY_2"  : {"HT":"375", "Yield": 1.238e+00 ,"SampleType":"Zmumu","Category":"Had"},
	"HadSelectionDY_3"  : {"HT":"475", "Yield": 0.000e+00 ,"SampleType":"Zmumu","Category":"Had"},
	"HadSelectionDY_4"  : {"HT":"575", "Yield": 0.000e+00 ,"SampleType":"Zmumu","Category":"Had"},
	"HadSelectionDY_5"  : {"HT":"675", "Yield": 0.000e+00 ,"SampleType":"Zmumu","Category":"Had"},
	"HadSelectionDY_6"  : {"HT":"775", "Yield": 0.000e+00 ,"SampleType":"Zmumu","Category":"Had"},
	"HadSelectionDY_7"  : {"HT":"875", "Yield": 0.000e+00 ,"SampleType":"Zmumu","Category":"Had"},
	"HadTTbar_0"  : {"HT":"275", "Yield": 2.327e+01 ,"SampleType":"TTbar","Category":"Had"},
	"HadTTbar_1"  : {"HT":"325", "Yield": 9.342e+00 ,"SampleType":"TTbar","Category":"Had"},
	"HadTTbar_2"  : {"HT":"375", "Yield": 7.215e+00 ,"SampleType":"TTbar","Category":"Had"},
	"HadTTbar_3"  : {"HT":"475", "Yield": 1.086e+00 ,"SampleType":"TTbar","Category":"Had"},
	"HadTTbar_4"  : {"HT":"575", "Yield": 7.495e-02 ,"SampleType":"TTbar","Category":"Had"},
	"HadTTbar_5"  : {"HT":"675", "Yield": 0.000e+00 ,"SampleType":"TTbar","Category":"Had"},
	"HadTTbar_6"  : {"HT":"775", "Yield": 0.000e+00 ,"SampleType":"TTbar","Category":"Had"},
	"HadTTbar_7"  : {"HT":"875", "Yield": 0.000e+00 ,"SampleType":"TTbar","Category":"Had"},
	"HadWJets250_0"  : {"HT":"275", "Yield": 0.000e+00 ,"SampleType":"WJets250","Category":"Had"},
	"HadWJets250_1"  : {"HT":"325", "Yield": 0.000e+00 ,"SampleType":"WJets250","Category":"Had"},
	"HadWJets250_2"  : {"HT":"375", "Yield": 2.081e-01 ,"SampleType":"WJets250","Category":"Had"},
	"HadWJets250_3"  : {"HT":"475", "Yield": 8.635e-02 ,"SampleType":"WJets250","Category":"Had"},
	"HadWJets250_4"  : {"HT":"575", "Yield": 2.375e-02 ,"SampleType":"WJets250","Category":"Had"},
	"HadWJets250_5"  : {"HT":"675", "Yield": 1.324e-03 ,"SampleType":"WJets250","Category":"Had"},
	"HadWJets250_6"  : {"HT":"775", "Yield": 0.000e+00 ,"SampleType":"WJets250","Category":"Had"},
	"HadWJets250_7"  : {"HT":"875", "Yield": 0.000e+00 ,"SampleType":"WJets250","Category":"Had"},
	"HadWJets300_0"  : {"HT":"275", "Yield": 0.000e+00 ,"SampleType":"WJets300","Category":"Had"},
	"HadWJets300_1"  : {"HT":"325", "Yield": 0.000e+00 ,"SampleType":"WJets300","Category":"Had"},
	"HadWJets300_2"  : {"HT":"375", "Yield": 1.197e+02 ,"SampleType":"WJets300","Category":"Had"},
	"HadWJets300_3"  : {"HT":"475", "Yield": 3.027e+01 ,"SampleType":"WJets300","Category":"Had"},
	"HadWJets300_4"  : {"HT":"575", "Yield": 8.102e+00 ,"SampleType":"WJets300","Category":"Had"},
	"HadWJets300_5"  : {"HT":"675", "Yield": 2.294e+00 ,"SampleType":"WJets300","Category":"Had"},
	"HadWJets300_6"  : {"HT":"775", "Yield": 9.859e-01 ,"SampleType":"WJets300","Category":"Had"},
	"HadWJets300_7"  : {"HT":"875", "Yield": 2.627e-01 ,"SampleType":"WJets300","Category":"Had"},
	"HadWJetsInc_0"  : {"HT":"275", "Yield": 4.321e+02 ,"SampleType":"WJetsInc","Category":"Had"},
	"HadWJetsInc_1"  : {"HT":"325", "Yield": 1.286e+02 ,"SampleType":"WJetsInc","Category":"Had"},
	"HadWJetsInc_2"  : {"HT":"375", "Yield": 0.000e+00 ,"SampleType":"WJetsInc","Category":"Had"},
	"HadWJetsInc_3"  : {"HT":"475", "Yield": 0.000e+00 ,"SampleType":"WJetsInc","Category":"Had"},
	"HadWJetsInc_4"  : {"HT":"575", "Yield": 0.000e+00 ,"SampleType":"WJetsInc","Category":"Had"},
	"HadWJetsInc_5"  : {"HT":"675", "Yield": 0.000e+00 ,"SampleType":"WJetsInc","Category":"Had"},
	"HadWJetsInc_6"  : {"HT":"775", "Yield": 0.000e+00 ,"SampleType":"WJetsInc","Category":"Had"},
	"HadWJetsInc_7"  : {"HT":"875", "Yield": 0.000e+00 ,"SampleType":"WJetsInc","Category":"Had"},
	"HadZinv100_0"  : {"HT":"275", "Yield": 4.760e-01 ,"SampleType":"Zinv100","Category":"Had"},
	"HadZinv100_1"  : {"HT":"325", "Yield": 0.000e+00 ,"SampleType":"Zinv100","Category":"Had"},
	"HadZinv100_2"  : {"HT":"375", "Yield": 0.000e+00 ,"SampleType":"Zinv100","Category":"Had"},
	"HadZinv100_3"  : {"HT":"475", "Yield": 0.000e+00 ,"SampleType":"Zinv100","Category":"Had"},
	"HadZinv100_4"  : {"HT":"575", "Yield": 0.000e+00 ,"SampleType":"Zinv100","Category":"Had"},
	"HadZinv100_5"  : {"HT":"675", "Yield": 0.000e+00 ,"SampleType":"Zinv100","Category":"Had"},
	"HadZinv100_6"  : {"HT":"775", "Yield": 0.000e+00 ,"SampleType":"Zinv100","Category":"Had"},
	"HadZinv100_7"  : {"HT":"875", "Yield": 0.000e+00 ,"SampleType":"Zinv100","Category":"Had"},
	"HadZinv200_0"  : {"HT":"275", "Yield": 6.237e+02 ,"SampleType":"Zinv200","Category":"Had"},
	"HadZinv200_1"  : {"HT":"325", "Yield": 2.946e+02 ,"SampleType":"Zinv200","Category":"Had"},
	"HadZinv200_2"  : {"HT":"375", "Yield": 2.256e+02 ,"SampleType":"Zinv200","Category":"Had"},
	"HadZinv200_3"  : {"HT":"475", "Yield": 5.570e+01 ,"SampleType":"Zinv200","Category":"Had"},
	"HadZinv200_4"  : {"HT":"575", "Yield": 2.066e+01 ,"SampleType":"Zinv200","Category":"Had"},
	"HadZinv200_5"  : {"HT":"675", "Yield": 6.866e+00 ,"SampleType":"Zinv200","Category":"Had"},
	"HadZinv200_6"  : {"HT":"775", "Yield": 2.560e+00 ,"SampleType":"Zinv200","Category":"Had"},
	"HadZinv200_7"  : {"HT":"875", "Yield": 1.749e+00 ,"SampleType":"Zinv200","Category":"Had"},
	"HadZinv50_0"  : {"HT":"275", "Yield": 0.000e+00 ,"SampleType":"Zinv50","Category":"Had"},
	"HadZinv50_1"  : {"HT":"325", "Yield": 0.000e+00 ,"SampleType":"Zinv50","Category":"Had"},
	"HadZinv50_2"  : {"HT":"375", "Yield": 0.000e+00 ,"SampleType":"Zinv50","Category":"Had"},
	"HadZinv50_3"  : {"HT":"475", "Yield": 0.000e+00 ,"SampleType":"Zinv50","Category":"Had"},
	"HadZinv50_4"  : {"HT":"575", "Yield": 0.000e+00 ,"SampleType":"Zinv50","Category":"Had"},
	"HadZinv50_5"  : {"HT":"675", "Yield": 0.000e+00 ,"SampleType":"Zinv50","Category":"Had"},
	"HadZinv50_6"  : {"HT":"775", "Yield": 0.000e+00 ,"SampleType":"Zinv50","Category":"Had"},
	"HadZinv50_7"  : {"HT":"875", "Yield": 0.000e+00 ,"SampleType":"Zinv50","Category":"Had"},
	"SingleMuSelectionDY_0"  : {"HT":"275", "Yield": 5.905e+00 ,"SampleType":"Zmumu","Category":"Muon"},
	"SingleMuSelectionDY_1"  : {"HT":"325", "Yield": 1.853e+00 ,"SampleType":"Zmumu","Category":"Muon"},
	"SingleMuSelectionDY_2"  : {"HT":"375", "Yield": 2.516e+00 ,"SampleType":"Zmumu","Category":"Muon"},
	"SingleMuSelectionDY_3"  : {"HT":"475", "Yield": 0.000e+00 ,"SampleType":"Zmumu","Category":"Muon"},
	"SingleMuSelectionDY_4"  : {"HT":"575", "Yield": 0.000e+00 ,"SampleType":"Zmumu","Category":"Muon"},
	"SingleMuSelectionDY_5"  : {"HT":"675", "Yield": 0.000e+00 ,"SampleType":"Zmumu","Category":"Muon"},
	"SingleMuSelectionDY_6"  : {"HT":"775", "Yield": 0.000e+00 ,"SampleType":"Zmumu","Category":"Muon"},
	"SingleMuSelectionDY_7"  : {"HT":"875", "Yield": 0.000e+00 ,"SampleType":"Zmumu","Category":"Muon"},
	"SingleMuTTbar_0"  : {"HT":"275", "Yield": 3.308e+01 ,"SampleType":"TTbar","Category":"Muon"},
	"SingleMuTTbar_1"  : {"HT":"325", "Yield": 1.318e+01 ,"SampleType":"TTbar","Category":"Muon"},
	"SingleMuTTbar_2"  : {"HT":"375", "Yield": 8.242e+00 ,"SampleType":"TTbar","Category":"Muon"},
	"SingleMuTTbar_3"  : {"HT":"475", "Yield": 2.018e+00 ,"SampleType":"TTbar","Category":"Muon"},
	"SingleMuTTbar_4"  : {"HT":"575", "Yield": 4.086e-01 ,"SampleType":"TTbar","Category":"Muon"},
	"SingleMuTTbar_5"  : {"HT":"675", "Yield": 0.000e+00 ,"SampleType":"TTbar","Category":"Muon"},
	"SingleMuTTbar_6"  : {"HT":"775", "Yield": 0.000e+00 ,"SampleType":"TTbar","Category":"Muon"},
	"SingleMuTTbar_7"  : {"HT":"875", "Yield": 0.000e+00 ,"SampleType":"TTbar","Category":"Muon"},
	"SingleMuWJets250_0"  : {"HT":"275", "Yield": 0.000e+00 ,"SampleType":"WJets250","Category":"Muon"},
	"SingleMuWJets250_1"  : {"HT":"325", "Yield": 0.000e+00 ,"SampleType":"WJets250","Category":"Muon"},
	"SingleMuWJets250_2"  : {"HT":"375", "Yield": 3.365e-01 ,"SampleType":"WJets250","Category":"Muon"},
	"SingleMuWJets250_3"  : {"HT":"475", "Yield": 0.000e+00 ,"SampleType":"WJets250","Category":"Muon"},
	"SingleMuWJets250_4"  : {"HT":"575", "Yield": 0.000e+00 ,"SampleType":"WJets250","Category":"Muon"},
	"SingleMuWJets250_5"  : {"HT":"675", "Yield": 0.000e+00 ,"SampleType":"WJets250","Category":"Muon"},
	"SingleMuWJets250_6"  : {"HT":"775", "Yield": 0.000e+00 ,"SampleType":"WJets250","Category":"Muon"},
	"SingleMuWJets250_7"  : {"HT":"875", "Yield": 0.000e+00 ,"SampleType":"WJets250","Category":"Muon"},
	"SingleMuWJets300_0"  : {"HT":"275", "Yield": 0.000e+00 ,"SampleType":"WJets300","Category":"Muon"},
	"SingleMuWJets300_1"  : {"HT":"325", "Yield": 0.000e+00 ,"SampleType":"WJets300","Category":"Muon"},
	"SingleMuWJets300_2"  : {"HT":"375", "Yield": 1.491e+02 ,"SampleType":"WJets300","Category":"Muon"},
	"SingleMuWJets300_3"  : {"HT":"475", "Yield": 3.741e+01 ,"SampleType":"WJets300","Category":"Muon"},
	"SingleMuWJets300_4"  : {"HT":"575", "Yield": 1.317e+01 ,"SampleType":"WJets300","Category":"Muon"},
	"SingleMuWJets300_5"  : {"HT":"675", "Yield": 5.004e+00 ,"SampleType":"WJets300","Category":"Muon"},
	"SingleMuWJets300_6"  : {"HT":"775", "Yield": 1.254e+00 ,"SampleType":"WJets300","Category":"Muon"},
	"SingleMuWJets300_7"  : {"HT":"875", "Yield": 1.004e+00 ,"SampleType":"WJets300","Category":"Muon"},
	"SingleMuWJetsInc_0"  : {"HT":"275", "Yield": 3.748e+02 ,"SampleType":"WJetsInc","Category":"Muon"},
	"SingleMuWJetsInc_1"  : {"HT":"325", "Yield": 2.176e+02 ,"SampleType":"WJetsInc","Category":"Muon"},
	"SingleMuWJetsInc_2"  : {"HT":"375", "Yield": 0.000e+00 ,"SampleType":"WJetsInc","Category":"Muon"},
	"SingleMuWJetsInc_3"  : {"HT":"475", "Yield": 0.000e+00 ,"SampleType":"WJetsInc","Category":"Muon"},
	"SingleMuWJetsInc_4"  : {"HT":"575", "Yield": 0.000e+00 ,"SampleType":"WJetsInc","Category":"Muon"},
	"SingleMuWJetsInc_5"  : {"HT":"675", "Yield": 0.000e+00 ,"SampleType":"WJetsInc","Category":"Muon"},
	"SingleMuWJetsInc_6"  : {"HT":"775", "Yield": 0.000e+00 ,"SampleType":"WJetsInc","Category":"Muon"},
	"SingleMuWJetsInc_7"  : {"HT":"875", "Yield": 0.000e+00 ,"SampleType":"WJetsInc","Category":"Muon"},
	"SingleMuZinv100_0"  : {"HT":"275", "Yield": 0.000e+00 ,"SampleType":"Zinv100","Category":"Muon"},
	"SingleMuZinv100_1"  : {"HT":"325", "Yield": 0.000e+00 ,"SampleType":"Zinv100","Category":"Muon"},
	"SingleMuZinv100_2"  : {"HT":"375", "Yield": 0.000e+00 ,"SampleType":"Zinv100","Category":"Muon"},
	"SingleMuZinv100_3"  : {"HT":"475", "Yield": 0.000e+00 ,"SampleType":"Zinv100","Category":"Muon"},
	"SingleMuZinv100_4"  : {"HT":"575", "Yield": 0.000e+00 ,"SampleType":"Zinv100","Category":"Muon"},
	"SingleMuZinv100_5"  : {"HT":"675", "Yield": 0.000e+00 ,"SampleType":"Zinv100","Category":"Muon"},
	"SingleMuZinv100_6"  : {"HT":"775", "Yield": 0.000e+00 ,"SampleType":"Zinv100","Category":"Muon"},
	"SingleMuZinv100_7"  : {"HT":"875", "Yield": 0.000e+00 ,"SampleType":"Zinv100","Category":"Muon"},
	"SingleMuZinv200_0"  : {"HT":"275", "Yield": 0.000e+00 ,"SampleType":"Zinv200","Category":"Muon"},
	"SingleMuZinv200_1"  : {"HT":"325", "Yield": 0.000e+00 ,"SampleType":"Zinv200","Category":"Muon"},
	"SingleMuZinv200_2"  : {"HT":"375", "Yield": 0.000e+00 ,"SampleType":"Zinv200","Category":"Muon"},
	"SingleMuZinv200_3"  : {"HT":"475", "Yield": 0.000e+00 ,"SampleType":"Zinv200","Category":"Muon"},
	"SingleMuZinv200_4"  : {"HT":"575", "Yield": 0.000e+00 ,"SampleType":"Zinv200","Category":"Muon"},
	"SingleMuZinv200_5"  : {"HT":"675", "Yield": 0.000e+00 ,"SampleType":"Zinv200","Category":"Muon"},
	"SingleMuZinv200_6"  : {"HT":"775", "Yield": 0.000e+00 ,"SampleType":"Zinv200","Category":"Muon"},
	"SingleMuZinv200_7"  : {"HT":"875", "Yield": 0.000e+00 ,"SampleType":"Zinv200","Category":"Muon"},
	"SingleMuZinv50_0"  : {"HT":"275", "Yield": 0.000e+00 ,"SampleType":"Zinv50","Category":"Muon"},
	"SingleMuZinv50_1"  : {"HT":"325", "Yield": 0.000e+00 ,"SampleType":"Zinv50","Category":"Muon"},
	"SingleMuZinv50_2"  : {"HT":"375", "Yield": 0.000e+00 ,"SampleType":"Zinv50","Category":"Muon"},
	"SingleMuZinv50_3"  : {"HT":"475", "Yield": 0.000e+00 ,"SampleType":"Zinv50","Category":"Muon"},
	"SingleMuZinv50_4"  : {"HT":"575", "Yield": 0.000e+00 ,"SampleType":"Zinv50","Category":"Muon"},
	"SingleMuZinv50_5"  : {"HT":"675", "Yield": 0.000e+00 ,"SampleType":"Zinv50","Category":"Muon"},
	"SingleMuZinv50_6"  : {"HT":"775", "Yield": 0.000e+00 ,"SampleType":"Zinv50","Category":"Muon"},
	"SingleMuZinv50_7"  : {"HT":"875", "Yield": 0.000e+00 ,"SampleType":"Zinv50","Category":"Muon"},
	"nDiMu_0"  : {"HT":"275", "Yield": 4.900e+01 ,"SampleType":"Data","Category":"DiMuon"},
	"nDiMu_1"  : {"HT":"325", "Yield": 3.100e+01 ,"SampleType":"Data","Category":"DiMuon"},
	"nDiMu_2"  : {"HT":"375", "Yield": 1.800e+01 ,"SampleType":"Data","Category":"DiMuon"},
	"nDiMu_3"  : {"HT":"475", "Yield": 5.000e+00 ,"SampleType":"Data","Category":"DiMuon"},
	"nDiMu_4"  : {"HT":"575", "Yield": 1.000e+00 ,"SampleType":"Data","Category":"DiMuon"},
	"nDiMu_5"  : {"HT":"675", "Yield": 1.000e+00 ,"SampleType":"Data","Category":"DiMuon"},
	"nDiMu_6"  : {"HT":"775", "Yield": 0.000e+00 ,"SampleType":"Data","Category":"DiMuon"},
	"nDiMu_7"  : {"HT":"875", "Yield": 0.000e+00 ,"SampleType":"Data","Category":"DiMuon"},
	"nHad_0"  : {"HT":"275", "Yield": 1.000e+03 ,"SampleType":"Data","Category":"Had"},
	"nHad_1"  : {"HT":"325", "Yield": 4.200e+02 ,"SampleType":"Data","Category":"Had"},
	"nHad_2"  : {"HT":"375", "Yield": 2.960e+02 ,"SampleType":"Data","Category":"Had"},
	"nHad_3"  : {"HT":"475", "Yield": 6.700e+01 ,"SampleType":"Data","Category":"Had"},
	"nHad_4"  : {"HT":"575", "Yield": 2.700e+01 ,"SampleType":"Data","Category":"Had"},
	"nHad_5"  : {"HT":"675", "Yield": 8.000e+00 ,"SampleType":"Data","Category":"Had"},
	"nHad_6"  : {"HT":"775", "Yield": 3.000e+00 ,"SampleType":"Data","Category":"Had"},
	"nHad_7"  : {"HT":"875", "Yield": 0.000e+00 ,"SampleType":"Data","Category":"Had"},
	"nSingleMu_0"  : {"HT":"275", "Yield": 4.360e+02 ,"SampleType":"Data","Category":"Muon"},
	"nSingleMu_1"  : {"HT":"325", "Yield": 1.920e+02 ,"SampleType":"Data","Category":"Muon"},
	"nSingleMu_2"  : {"HT":"375", "Yield": 1.640e+02 ,"SampleType":"Data","Category":"Muon"},
	"nSingleMu_3"  : {"HT":"475", "Yield": 3.700e+01 ,"SampleType":"Data","Category":"Muon"},
	"nSingleMu_4"  : {"HT":"575", "Yield": 6.000e+00 ,"SampleType":"Data","Category":"Muon"},
	"nSingleMu_5"  : {"HT":"675", "Yield": 1.000e+00 ,"SampleType":"Data","Category":"Muon"},
	"nSingleMu_6"  : {"HT":"775", "Yield": 0.000e+00 ,"SampleType":"Data","Category":"Muon"},
	"nSingleMu_7"  : {"HT":"875", "Yield": 0.000e+00 ,"SampleType":"Data","Category":"Muon"},
	"photon_0"  : {"HT":"275", "Yield": 0 ,"SampleType":"Data","Category":"Photon"},
	"photon_1"  : {"HT":"325", "Yield": 0 ,"SampleType":"Data","Category":"Photon"},
	"photon_2"  : {"HT":"375", "Yield": 4.27e+02 ,"SampleType":"Data","Category":"Photon"},
	"photon_3"  : {"HT":"475", "Yield": 1.27e+02 ,"SampleType":"Data","Category":"Photon"},
	"photon_4"  : {"HT":"575", "Yield": 3.400e+01 ,"SampleType":"Data","Category":"Photon"},
	"photon_5"  : {"HT":"675", "Yield": 1.000e+01 ,"SampleType":"Data","Category":"Photon"},
	"photon_6"  : {"HT":"775", "Yield": 2.000e+00 ,"SampleType":"Data","Category":"Photon"},
	"photon_7"  : {"HT":"875", "Yield": 1.000e+00 ,"SampleType":"Data","Category":"Photon"},
	"photonmc_0"  : {"HT":"275", "Yield": 0 ,"SampleType":"Photon","Category":"Photon","Error":0},
	"photonmc_1"  : {"HT":"325", "Yield": 0 ,"SampleType":"Photon","Category":"Photon","Error":0},
	"photonmc_2"  : {"HT":"375", "Yield": 6.00e+02 ,"SampleType":"Photon","Category":"Photon","Error":2.00e+01},
	"photonmc_3"  : {"HT":"475", "Yield": 1.50e+02 ,"SampleType":"Photon","Category":"Photon","Error":1.00e+01},
	"photonmc_4"  : {"HT":"575", "Yield": 5.70e+01 ,"SampleType":"Photon","Category":"Photon","Error":7.00e+00},
	"photonmc_5"  : {"HT":"675", "Yield": 1.600e+01 ,"SampleType":"Photon","Category":"Photon","Error":4.00e+00},
	"photonmc_6"  : {"HT":"775", "Yield": 4.000e+00 ,"SampleType":"Photon","Category":"Photon","Error":2.00e+00},
	"photonmc_7"  : {"HT":"875", "Yield": 3.000e+00 ,"SampleType":"Photon","Category":"Photon","Error":1.00e+00},
}

    sampleDictnjet = {	"DiMuSelectionDY_0"  : {"HT":"275", "Yield": 1.133e+02 ,"SampleType":"Zmumu","Category":"DiMuon"},
	"DiMuSelectionDY_1"  : {"HT":"325", "Yield": 7.556e+01 ,"SampleType":"Zmumu","Category":"DiMuon"},
	"DiMuSelectionDY_2"  : {"HT":"375", "Yield": 4.479e+01 ,"SampleType":"Zmumu","Category":"DiMuon"},
	"DiMuSelectionDY_3"  : {"HT":"475", "Yield": 1.612e+01 ,"SampleType":"Zmumu","Category":"DiMuon"},
	"DiMuSelectionDY_4"  : {"HT":"575", "Yield": 9.043e+00 ,"SampleType":"Zmumu","Category":"DiMuon"},
	"DiMuSelectionDY_5"  : {"HT":"675", "Yield": 3.020e+00 ,"SampleType":"Zmumu","Category":"DiMuon"},
	"DiMuSelectionDY_6"  : {"HT":"775", "Yield": 0.000e+00 ,"SampleType":"Zmumu","Category":"DiMuon"},
	"DiMuSelectionDY_7"  : {"HT":"875", "Yield": 1.208e+00 ,"SampleType":"Zmumu","Category":"DiMuon"},
	"DiMuTTbar_0"  : {"HT":"275", "Yield": 5.318e+00 ,"SampleType":"TTbar","Category":"DiMuon"},
	"DiMuTTbar_1"  : {"HT":"325", "Yield": 3.854e-01 ,"SampleType":"TTbar","Category":"DiMuon"},
	"DiMuTTbar_2"  : {"HT":"375", "Yield": 1.019e+00 ,"SampleType":"TTbar","Category":"DiMuon"},
	"DiMuTTbar_3"  : {"HT":"475", "Yield": 1.423e+00 ,"SampleType":"TTbar","Category":"DiMuon"},
	"DiMuTTbar_4"  : {"HT":"575", "Yield": 1.897e-01 ,"SampleType":"TTbar","Category":"DiMuon"},
	"DiMuTTbar_5"  : {"HT":"675", "Yield": 0.000e+00 ,"SampleType":"TTbar","Category":"DiMuon"},
	"DiMuTTbar_6"  : {"HT":"775", "Yield": 1.389e-01 ,"SampleType":"TTbar","Category":"DiMuon"},
	"DiMuTTbar_7"  : {"HT":"875", "Yield": 7.088e-01 ,"SampleType":"TTbar","Category":"DiMuon"},
	"DiMuWJets250_0"  : {"HT":"275", "Yield": 0.000e+00 ,"SampleType":"WJets250","Category":"DiMuon"},
	"DiMuWJets250_1"  : {"HT":"325", "Yield": 0.000e+00 ,"SampleType":"WJets250","Category":"DiMuon"},
	"DiMuWJets250_2"  : {"HT":"375", "Yield": 0.000e+00 ,"SampleType":"WJets250","Category":"DiMuon"},
	"DiMuWJets250_3"  : {"HT":"475", "Yield": 0.000e+00 ,"SampleType":"WJets250","Category":"DiMuon"},
	"DiMuWJets250_4"  : {"HT":"575", "Yield": 0.000e+00 ,"SampleType":"WJets250","Category":"DiMuon"},
	"DiMuWJets250_5"  : {"HT":"675", "Yield": 0.000e+00 ,"SampleType":"WJets250","Category":"DiMuon"},
	"DiMuWJets250_6"  : {"HT":"775", "Yield": 0.000e+00 ,"SampleType":"WJets250","Category":"DiMuon"},
	"DiMuWJets250_7"  : {"HT":"875", "Yield": 0.000e+00 ,"SampleType":"WJets250","Category":"DiMuon"},
	"DiMuWJets300_0"  : {"HT":"275", "Yield": 0.000e+00 ,"SampleType":"WJets300","Category":"DiMuon"},
	"DiMuWJets300_1"  : {"HT":"325", "Yield": 0.000e+00 ,"SampleType":"WJets300","Category":"DiMuon"},
	"DiMuWJets300_2"  : {"HT":"375", "Yield": 0.000e+00 ,"SampleType":"WJets300","Category":"DiMuon"},
	"DiMuWJets300_3"  : {"HT":"475", "Yield": 0.000e+00 ,"SampleType":"WJets300","Category":"DiMuon"},
	"DiMuWJets300_4"  : {"HT":"575", "Yield": 0.000e+00 ,"SampleType":"WJets300","Category":"DiMuon"},
	"DiMuWJets300_5"  : {"HT":"675", "Yield": 0.000e+00 ,"SampleType":"WJets300","Category":"DiMuon"},
	"DiMuWJets300_6"  : {"HT":"775", "Yield": 0.000e+00 ,"SampleType":"WJets300","Category":"DiMuon"},
	"DiMuWJets300_7"  : {"HT":"875", "Yield": 0.000e+00 ,"SampleType":"WJets300","Category":"DiMuon"},
	"DiMuWJetsInc_0"  : {"HT":"275", "Yield": 0.000e+00 ,"SampleType":"WJetsInc","Category":"DiMuon"},
	"DiMuWJetsInc_1"  : {"HT":"325", "Yield": 0.000e+00 ,"SampleType":"WJetsInc","Category":"DiMuon"},
	"DiMuWJetsInc_2"  : {"HT":"375", "Yield": 0.000e+00 ,"SampleType":"WJetsInc","Category":"DiMuon"},
	"DiMuWJetsInc_3"  : {"HT":"475", "Yield": 0.000e+00 ,"SampleType":"WJetsInc","Category":"DiMuon"},
	"DiMuWJetsInc_4"  : {"HT":"575", "Yield": 0.000e+00 ,"SampleType":"WJetsInc","Category":"DiMuon"},
	"DiMuWJetsInc_5"  : {"HT":"675", "Yield": 0.000e+00 ,"SampleType":"WJetsInc","Category":"DiMuon"},
	"DiMuWJetsInc_6"  : {"HT":"775", "Yield": 0.000e+00 ,"SampleType":"WJetsInc","Category":"DiMuon"},
	"DiMuWJetsInc_7"  : {"HT":"875", "Yield": 0.000e+00 ,"SampleType":"WJetsInc","Category":"DiMuon"},
	"DiMuZinv100_0"  : {"HT":"275", "Yield": 0.000e+00 ,"SampleType":"Zinv100","Category":"DiMuon"},
	"DiMuZinv100_1"  : {"HT":"325", "Yield": 0.000e+00 ,"SampleType":"Zinv100","Category":"DiMuon"},
	"DiMuZinv100_2"  : {"HT":"375", "Yield": 0.000e+00 ,"SampleType":"Zinv100","Category":"DiMuon"},
	"DiMuZinv100_3"  : {"HT":"475", "Yield": 0.000e+00 ,"SampleType":"Zinv100","Category":"DiMuon"},
	"DiMuZinv100_4"  : {"HT":"575", "Yield": 0.000e+00 ,"SampleType":"Zinv100","Category":"DiMuon"},
	"DiMuZinv100_5"  : {"HT":"675", "Yield": 0.000e+00 ,"SampleType":"Zinv100","Category":"DiMuon"},
	"DiMuZinv100_6"  : {"HT":"775", "Yield": 0.000e+00 ,"SampleType":"Zinv100","Category":"DiMuon"},
	"DiMuZinv100_7"  : {"HT":"875", "Yield": 0.000e+00 ,"SampleType":"Zinv100","Category":"DiMuon"},
	"DiMuZinv200_0"  : {"HT":"275", "Yield": 0.000e+00 ,"SampleType":"Zinv200","Category":"DiMuon"},
	"DiMuZinv200_1"  : {"HT":"325", "Yield": 0.000e+00 ,"SampleType":"Zinv200","Category":"DiMuon"},
	"DiMuZinv200_2"  : {"HT":"375", "Yield": 0.000e+00 ,"SampleType":"Zinv200","Category":"DiMuon"},
	"DiMuZinv200_3"  : {"HT":"475", "Yield": 0.000e+00 ,"SampleType":"Zinv200","Category":"DiMuon"},
	"DiMuZinv200_4"  : {"HT":"575", "Yield": 0.000e+00 ,"SampleType":"Zinv200","Category":"DiMuon"},
	"DiMuZinv200_5"  : {"HT":"675", "Yield": 0.000e+00 ,"SampleType":"Zinv200","Category":"DiMuon"},
	"DiMuZinv200_6"  : {"HT":"775", "Yield": 0.000e+00 ,"SampleType":"Zinv200","Category":"DiMuon"},
	"DiMuZinv200_7"  : {"HT":"875", "Yield": 0.000e+00 ,"SampleType":"Zinv200","Category":"DiMuon"},
	"DiMuZinv50_0"  : {"HT":"275", "Yield": 0.000e+00 ,"SampleType":"Zinv50","Category":"DiMuon"},
	"DiMuZinv50_1"  : {"HT":"325", "Yield": 0.000e+00 ,"SampleType":"Zinv50","Category":"DiMuon"},
	"DiMuZinv50_2"  : {"HT":"375", "Yield": 0.000e+00 ,"SampleType":"Zinv50","Category":"DiMuon"},
	"DiMuZinv50_3"  : {"HT":"475", "Yield": 0.000e+00 ,"SampleType":"Zinv50","Category":"DiMuon"},
	"DiMuZinv50_4"  : {"HT":"575", "Yield": 0.000e+00 ,"SampleType":"Zinv50","Category":"DiMuon"},
	"DiMuZinv50_5"  : {"HT":"675", "Yield": 0.000e+00 ,"SampleType":"Zinv50","Category":"DiMuon"},
	"DiMuZinv50_6"  : {"HT":"775", "Yield": 0.000e+00 ,"SampleType":"Zinv50","Category":"DiMuon"},
	"DiMuZinv50_7"  : {"HT":"875", "Yield": 0.000e+00 ,"SampleType":"Zinv50","Category":"DiMuon"},
	"HadSelectionDY_0"  : {"HT":"275", "Yield": 1.127e+01 ,"SampleType":"Zmumu","Category":"Had"},
	"HadSelectionDY_1"  : {"HT":"325", "Yield": 3.565e+00 ,"SampleType":"Zmumu","Category":"Had"},
	"HadSelectionDY_2"  : {"HT":"375", "Yield": 4.883e+00 ,"SampleType":"Zmumu","Category":"Had"},
	"HadSelectionDY_3"  : {"HT":"475", "Yield": 1.151e+00 ,"SampleType":"Zmumu","Category":"Had"},
	"HadSelectionDY_4"  : {"HT":"575", "Yield": 4.669e-01 ,"SampleType":"Zmumu","Category":"Had"},
	"HadSelectionDY_5"  : {"HT":"675", "Yield": 0.000e+00 ,"SampleType":"Zmumu","Category":"Had"},
	"HadSelectionDY_6"  : {"HT":"775", "Yield": 0.000e+00 ,"SampleType":"Zmumu","Category":"Had"},
	"HadSelectionDY_7"  : {"HT":"875", "Yield": 0.000e+00 ,"SampleType":"Zmumu","Category":"Had"},
	"HadTTbar_0"  : {"HT":"275", "Yield": 4.888e+02 ,"SampleType":"TTbar","Category":"Had"},
	"HadTTbar_1"  : {"HT":"325", "Yield": 2.152e+02 ,"SampleType":"TTbar","Category":"Had"},
	"HadTTbar_2"  : {"HT":"375", "Yield": 1.740e+02 ,"SampleType":"TTbar","Category":"Had"},
	"HadTTbar_3"  : {"HT":"475", "Yield": 6.933e+01 ,"SampleType":"TTbar","Category":"Had"},
	"HadTTbar_4"  : {"HT":"575", "Yield": 2.097e+01 ,"SampleType":"TTbar","Category":"Had"},
	"HadTTbar_5"  : {"HT":"675", "Yield": 1.450e+01 ,"SampleType":"TTbar","Category":"Had"},
	"HadTTbar_6"  : {"HT":"775", "Yield": 1.680e+00 ,"SampleType":"TTbar","Category":"Had"},
	"HadTTbar_7"  : {"HT":"875", "Yield": 1.161e+00 ,"SampleType":"TTbar","Category":"Had"},
	"HadWJets250_0"  : {"HT":"275", "Yield": 0.000e+00 ,"SampleType":"WJets250","Category":"Had"},
	"HadWJets250_1"  : {"HT":"325", "Yield": 0.000e+00 ,"SampleType":"WJets250","Category":"Had"},
	"HadWJets250_2"  : {"HT":"375", "Yield": 9.681e+00 ,"SampleType":"WJets250","Category":"Had"},
	"HadWJets250_3"  : {"HT":"475", "Yield": 5.110e-01 ,"SampleType":"WJets250","Category":"Had"},
	"HadWJets250_4"  : {"HT":"575", "Yield": 2.375e-02 ,"SampleType":"WJets250","Category":"Had"},
	"HadWJets250_5"  : {"HT":"675", "Yield": 1.324e-03 ,"SampleType":"WJets250","Category":"Had"},
	"HadWJets250_6"  : {"HT":"775", "Yield": 0.000e+00 ,"SampleType":"WJets250","Category":"Had"},
	"HadWJets250_7"  : {"HT":"875", "Yield": 0.000e+00 ,"SampleType":"WJets250","Category":"Had"},
	"HadWJets300_0"  : {"HT":"275", "Yield": 0.000e+00 ,"SampleType":"WJets300","Category":"Had"},
	"HadWJets300_1"  : {"HT":"325", "Yield": 0.000e+00 ,"SampleType":"WJets300","Category":"Had"},
	"HadWJets300_2"  : {"HT":"375", "Yield": 3.566e+02 ,"SampleType":"WJets300","Category":"Had"},
	"HadWJets300_3"  : {"HT":"475", "Yield": 1.276e+02 ,"SampleType":"WJets300","Category":"Had"},
	"HadWJets300_4"  : {"HT":"575", "Yield": 4.627e+01 ,"SampleType":"WJets300","Category":"Had"},
	"HadWJets300_5"  : {"HT":"675", "Yield": 1.558e+01 ,"SampleType":"WJets300","Category":"Had"},
	"HadWJets300_6"  : {"HT":"775", "Yield": 6.587e+00 ,"SampleType":"WJets300","Category":"Had"},
	"HadWJets300_7"  : {"HT":"875", "Yield": 4.475e+00 ,"SampleType":"WJets300","Category":"Had"},
	"HadWJetsInc_0"  : {"HT":"275", "Yield": 1.435e+03 ,"SampleType":"WJetsInc","Category":"Had"},
	"HadWJetsInc_1"  : {"HT":"325", "Yield": 6.105e+02 ,"SampleType":"WJetsInc","Category":"Had"},
	"HadWJetsInc_2"  : {"HT":"375", "Yield": 0.000e+00 ,"SampleType":"WJetsInc","Category":"Had"},
	"HadWJetsInc_3"  : {"HT":"475", "Yield": 0.000e+00 ,"SampleType":"WJetsInc","Category":"Had"},
	"HadWJetsInc_4"  : {"HT":"575", "Yield": 0.000e+00 ,"SampleType":"WJetsInc","Category":"Had"},
	"HadWJetsInc_5"  : {"HT":"675", "Yield": 0.000e+00 ,"SampleType":"WJetsInc","Category":"Had"},
	"HadWJetsInc_6"  : {"HT":"775", "Yield": 0.000e+00 ,"SampleType":"WJetsInc","Category":"Had"},
	"HadWJetsInc_7"  : {"HT":"875", "Yield": 0.000e+00 ,"SampleType":"WJetsInc","Category":"Had"},
	"HadZinv100_0"  : {"HT":"275", "Yield": 2.147e+01 ,"SampleType":"Zinv100","Category":"Had"},
	"HadZinv100_1"  : {"HT":"325", "Yield": 1.836e+00 ,"SampleType":"Zinv100","Category":"Had"},
	"HadZinv100_2"  : {"HT":"375", "Yield": 5.054e-01 ,"SampleType":"Zinv100","Category":"Had"},
	"HadZinv100_3"  : {"HT":"475", "Yield": 0.000e+00 ,"SampleType":"Zinv100","Category":"Had"},
	"HadZinv100_4"  : {"HT":"575", "Yield": 0.000e+00 ,"SampleType":"Zinv100","Category":"Had"},
	"HadZinv100_5"  : {"HT":"675", "Yield": 0.000e+00 ,"SampleType":"Zinv100","Category":"Had"},
	"HadZinv100_6"  : {"HT":"775", "Yield": 0.000e+00 ,"SampleType":"Zinv100","Category":"Had"},
	"HadZinv100_7"  : {"HT":"875", "Yield": 0.000e+00 ,"SampleType":"Zinv100","Category":"Had"},
	"HadZinv200_0"  : {"HT":"275", "Yield": 1.558e+03 ,"SampleType":"Zinv200","Category":"Had"},
	"HadZinv200_1"  : {"HT":"325", "Yield": 6.966e+02 ,"SampleType":"Zinv200","Category":"Had"},
	"HadZinv200_2"  : {"HT":"375", "Yield": 5.243e+02 ,"SampleType":"Zinv200","Category":"Had"},
	"HadZinv200_3"  : {"HT":"475", "Yield": 1.877e+02 ,"SampleType":"Zinv200","Category":"Had"},
	"HadZinv200_4"  : {"HT":"575", "Yield": 7.167e+01 ,"SampleType":"Zinv200","Category":"Had"},
	"HadZinv200_5"  : {"HT":"675", "Yield": 2.426e+01 ,"SampleType":"Zinv200","Category":"Had"},
	"HadZinv200_6"  : {"HT":"775", "Yield": 1.012e+01 ,"SampleType":"Zinv200","Category":"Had"},
	"HadZinv200_7"  : {"HT":"875", "Yield": 6.959e+00 ,"SampleType":"Zinv200","Category":"Had"},
	"HadZinv50_0"  : {"HT":"275", "Yield": 0.000e+00 ,"SampleType":"Zinv50","Category":"Had"},
	"HadZinv50_1"  : {"HT":"325", "Yield": 0.000e+00 ,"SampleType":"Zinv50","Category":"Had"},
	"HadZinv50_2"  : {"HT":"375", "Yield": 0.000e+00 ,"SampleType":"Zinv50","Category":"Had"},
	"HadZinv50_3"  : {"HT":"475", "Yield": 0.000e+00 ,"SampleType":"Zinv50","Category":"Had"},
	"HadZinv50_4"  : {"HT":"575", "Yield": 0.000e+00 ,"SampleType":"Zinv50","Category":"Had"},
	"HadZinv50_5"  : {"HT":"675", "Yield": 0.000e+00 ,"SampleType":"Zinv50","Category":"Had"},
	"HadZinv50_6"  : {"HT":"775", "Yield": 0.000e+00 ,"SampleType":"Zinv50","Category":"Had"},
	"HadZinv50_7"  : {"HT":"875", "Yield": 0.000e+00 ,"SampleType":"Zinv50","Category":"Had"},
	"SingleMuSelectionDY_0"  : {"HT":"275", "Yield": 1.417e+01 ,"SampleType":"Zmumu","Category":"Muon"},
	"SingleMuSelectionDY_1"  : {"HT":"325", "Yield": 7.617e+00 ,"SampleType":"Zmumu","Category":"Muon"},
	"SingleMuSelectionDY_2"  : {"HT":"375", "Yield": 4.238e+00 ,"SampleType":"Zmumu","Category":"Muon"},
	"SingleMuSelectionDY_3"  : {"HT":"475", "Yield": 3.053e-01 ,"SampleType":"Zmumu","Category":"Muon"},
	"SingleMuSelectionDY_4"  : {"HT":"575", "Yield": 1.971e+00 ,"SampleType":"Zmumu","Category":"Muon"},
	"SingleMuSelectionDY_5"  : {"HT":"675", "Yield": 3.787e-01 ,"SampleType":"Zmumu","Category":"Muon"},
	"SingleMuSelectionDY_6"  : {"HT":"775", "Yield": 0.000e+00 ,"SampleType":"Zmumu","Category":"Muon"},
	"SingleMuSelectionDY_7"  : {"HT":"875", "Yield": 0.000e+00 ,"SampleType":"Zmumu","Category":"Muon"},
	"SingleMuTTbar_0"  : {"HT":"275", "Yield": 4.646e+02 ,"SampleType":"TTbar","Category":"Muon"},
	"SingleMuTTbar_1"  : {"HT":"325", "Yield": 2.183e+02 ,"SampleType":"TTbar","Category":"Muon"},
	"SingleMuTTbar_2"  : {"HT":"375", "Yield": 1.533e+02 ,"SampleType":"TTbar","Category":"Muon"},
	"SingleMuTTbar_3"  : {"HT":"475", "Yield": 5.526e+01 ,"SampleType":"TTbar","Category":"Muon"},
	"SingleMuTTbar_4"  : {"HT":"575", "Yield": 2.250e+01 ,"SampleType":"TTbar","Category":"Muon"},
	"SingleMuTTbar_5"  : {"HT":"675", "Yield": 5.970e+00 ,"SampleType":"TTbar","Category":"Muon"},
	"SingleMuTTbar_6"  : {"HT":"775", "Yield": 1.030e+00 ,"SampleType":"TTbar","Category":"Muon"},
	"SingleMuTTbar_7"  : {"HT":"875", "Yield": 9.533e-01 ,"SampleType":"TTbar","Category":"Muon"},
	"SingleMuWJets250_0"  : {"HT":"275", "Yield": 0.000e+00 ,"SampleType":"WJets250","Category":"Muon"},
	"SingleMuWJets250_1"  : {"HT":"325", "Yield": 0.000e+00 ,"SampleType":"WJets250","Category":"Muon"},
	"SingleMuWJets250_2"  : {"HT":"375", "Yield": 1.963e+00 ,"SampleType":"WJets250","Category":"Muon"},
	"SingleMuWJets250_3"  : {"HT":"475", "Yield": 0.000e+00 ,"SampleType":"WJets250","Category":"Muon"},
	"SingleMuWJets250_4"  : {"HT":"575", "Yield": 0.000e+00 ,"SampleType":"WJets250","Category":"Muon"},
	"SingleMuWJets250_5"  : {"HT":"675", "Yield": 0.000e+00 ,"SampleType":"WJets250","Category":"Muon"},
	"SingleMuWJets250_6"  : {"HT":"775", "Yield": 0.000e+00 ,"SampleType":"WJets250","Category":"Muon"},
	"SingleMuWJets250_7"  : {"HT":"875", "Yield": 0.000e+00 ,"SampleType":"WJets250","Category":"Muon"},
	"SingleMuWJets300_0"  : {"HT":"275", "Yield": 0.000e+00 ,"SampleType":"WJets300","Category":"Muon"},
	"SingleMuWJets300_1"  : {"HT":"325", "Yield": 0.000e+00 ,"SampleType":"WJets300","Category":"Muon"},
	"SingleMuWJets300_2"  : {"HT":"375", "Yield": 3.416e+02 ,"SampleType":"WJets300","Category":"Muon"},
	"SingleMuWJets300_3"  : {"HT":"475", "Yield": 1.182e+02 ,"SampleType":"WJets300","Category":"Muon"},
	"SingleMuWJets300_4"  : {"HT":"575", "Yield": 4.333e+01 ,"SampleType":"WJets300","Category":"Muon"},
	"SingleMuWJets300_5"  : {"HT":"675", "Yield": 1.534e+01 ,"SampleType":"WJets300","Category":"Muon"},
	"SingleMuWJets300_6"  : {"HT":"775", "Yield": 6.280e+00 ,"SampleType":"WJets300","Category":"Muon"},
	"SingleMuWJets300_7"  : {"HT":"875", "Yield": 4.042e+00 ,"SampleType":"WJets300","Category":"Muon"},
	"SingleMuWJetsInc_0"  : {"HT":"275", "Yield": 9.936e+02 ,"SampleType":"WJetsInc","Category":"Muon"},
	"SingleMuWJetsInc_1"  : {"HT":"325", "Yield": 5.029e+02 ,"SampleType":"WJetsInc","Category":"Muon"},
	"SingleMuWJetsInc_2"  : {"HT":"375", "Yield": 0.000e+00 ,"SampleType":"WJetsInc","Category":"Muon"},
	"SingleMuWJetsInc_3"  : {"HT":"475", "Yield": 0.000e+00 ,"SampleType":"WJetsInc","Category":"Muon"},
	"SingleMuWJetsInc_4"  : {"HT":"575", "Yield": 0.000e+00 ,"SampleType":"WJetsInc","Category":"Muon"},
	"SingleMuWJetsInc_5"  : {"HT":"675", "Yield": 0.000e+00 ,"SampleType":"WJetsInc","Category":"Muon"},
	"SingleMuWJetsInc_6"  : {"HT":"775", "Yield": 0.000e+00 ,"SampleType":"WJetsInc","Category":"Muon"},
	"SingleMuWJetsInc_7"  : {"HT":"875", "Yield": 0.000e+00 ,"SampleType":"WJetsInc","Category":"Muon"},
	"SingleMuZinv100_0"  : {"HT":"275", "Yield": 0.000e+00 ,"SampleType":"Zinv100","Category":"Muon"},
	"SingleMuZinv100_1"  : {"HT":"325", "Yield": 0.000e+00 ,"SampleType":"Zinv100","Category":"Muon"},
	"SingleMuZinv100_2"  : {"HT":"375", "Yield": 0.000e+00 ,"SampleType":"Zinv100","Category":"Muon"},
	"SingleMuZinv100_3"  : {"HT":"475", "Yield": 0.000e+00 ,"SampleType":"Zinv100","Category":"Muon"},
	"SingleMuZinv100_4"  : {"HT":"575", "Yield": 0.000e+00 ,"SampleType":"Zinv100","Category":"Muon"},
	"SingleMuZinv100_5"  : {"HT":"675", "Yield": 0.000e+00 ,"SampleType":"Zinv100","Category":"Muon"},
	"SingleMuZinv100_6"  : {"HT":"775", "Yield": 0.000e+00 ,"SampleType":"Zinv100","Category":"Muon"},
	"SingleMuZinv100_7"  : {"HT":"875", "Yield": 0.000e+00 ,"SampleType":"Zinv100","Category":"Muon"},
	"SingleMuZinv200_0"  : {"HT":"275", "Yield": 0.000e+00 ,"SampleType":"Zinv200","Category":"Muon"},
	"SingleMuZinv200_1"  : {"HT":"325", "Yield": 0.000e+00 ,"SampleType":"Zinv200","Category":"Muon"},
	"SingleMuZinv200_2"  : {"HT":"375", "Yield": 0.000e+00 ,"SampleType":"Zinv200","Category":"Muon"},
	"SingleMuZinv200_3"  : {"HT":"475", "Yield": 0.000e+00 ,"SampleType":"Zinv200","Category":"Muon"},
	"SingleMuZinv200_4"  : {"HT":"575", "Yield": 0.000e+00 ,"SampleType":"Zinv200","Category":"Muon"},
	"SingleMuZinv200_5"  : {"HT":"675", "Yield": 0.000e+00 ,"SampleType":"Zinv200","Category":"Muon"},
	"SingleMuZinv200_6"  : {"HT":"775", "Yield": 0.000e+00 ,"SampleType":"Zinv200","Category":"Muon"},
	"SingleMuZinv200_7"  : {"HT":"875", "Yield": 0.000e+00 ,"SampleType":"Zinv200","Category":"Muon"},
	"SingleMuZinv50_0"  : {"HT":"275", "Yield": 0.000e+00 ,"SampleType":"Zinv50","Category":"Muon"},
	"SingleMuZinv50_1"  : {"HT":"325", "Yield": 0.000e+00 ,"SampleType":"Zinv50","Category":"Muon"},
	"SingleMuZinv50_2"  : {"HT":"375", "Yield": 0.000e+00 ,"SampleType":"Zinv50","Category":"Muon"},
	"SingleMuZinv50_3"  : {"HT":"475", "Yield": 0.000e+00 ,"SampleType":"Zinv50","Category":"Muon"},
	"SingleMuZinv50_4"  : {"HT":"575", "Yield": 0.000e+00 ,"SampleType":"Zinv50","Category":"Muon"},
	"SingleMuZinv50_5"  : {"HT":"675", "Yield": 0.000e+00 ,"SampleType":"Zinv50","Category":"Muon"},
	"SingleMuZinv50_6"  : {"HT":"775", "Yield": 0.000e+00 ,"SampleType":"Zinv50","Category":"Muon"},
	"SingleMuZinv50_7"  : {"HT":"875", "Yield": 0.000e+00 ,"SampleType":"Zinv50","Category":"Muon"},
	"nDiMu_0"  : {"HT":"275", "Yield": 1.140e+02 ,"SampleType":"Data","Category":"DiMuon"},
	"nDiMu_1"  : {"HT":"325", "Yield": 6.500e+01 ,"SampleType":"Data","Category":"DiMuon"},
	"nDiMu_2"  : {"HT":"375", "Yield": 4.200e+01 ,"SampleType":"Data","Category":"DiMuon"},
	"nDiMu_3"  : {"HT":"475", "Yield": 1.500e+01 ,"SampleType":"Data","Category":"DiMuon"},
	"nDiMu_4"  : {"HT":"575", "Yield": 7.000e+00 ,"SampleType":"Data","Category":"DiMuon"},
	"nDiMu_5"  : {"HT":"675", "Yield": 1.000e+00 ,"SampleType":"Data","Category":"DiMuon"},
	"nDiMu_6"  : {"HT":"775", "Yield": 0.000e+00 ,"SampleType":"Data","Category":"DiMuon"},
	"nDiMu_7"  : {"HT":"875", "Yield": 2.000e+00 ,"SampleType":"Data","Category":"DiMuon"},
	"nHad_0"  : {"HT":"275", "Yield": 3.700e+03 ,"SampleType":"Data","Category":"Had"},
	"nHad_1"  : {"HT":"325", "Yield": 1.536e+03 ,"SampleType":"Data","Category":"Had"},
	"nHad_2"  : {"HT":"375", "Yield": 1.043e+03 ,"SampleType":"Data","Category":"Had"},
	"nHad_3"  : {"HT":"475", "Yield": 3.460e+02 ,"SampleType":"Data","Category":"Had"},
	"nHad_4"  : {"HT":"575", "Yield": 1.220e+02 ,"SampleType":"Data","Category":"Had"},
	"nHad_5"  : {"HT":"675", "Yield": 4.400e+01 ,"SampleType":"Data","Category":"Had"},
	"nHad_6"  : {"HT":"775", "Yield": 1.400e+01 ,"SampleType":"Data","Category":"Had"},
	"nHad_7"  : {"HT":"875", "Yield": 6.000e+00 ,"SampleType":"Data","Category":"Had"},
	"nSingleMu_0"  : {"HT":"275", "Yield": 1.421e+03 ,"SampleType":"Data","Category":"Muon"},
	"nSingleMu_1"  : {"HT":"325", "Yield": 6.440e+02 ,"SampleType":"Data","Category":"Muon"},
	"nSingleMu_2"  : {"HT":"375", "Yield": 5.170e+02 ,"SampleType":"Data","Category":"Muon"},
	"nSingleMu_3"  : {"HT":"475", "Yield": 1.690e+02 ,"SampleType":"Data","Category":"Muon"},
	"nSingleMu_4"  : {"HT":"575", "Yield": 5.200e+01 ,"SampleType":"Data","Category":"Muon"},
	"nSingleMu_5"  : {"HT":"675", "Yield": 1.800e+01 ,"SampleType":"Data","Category":"Muon"},
	"nSingleMu_6"  : {"HT":"775", "Yield": 8.000e+00 ,"SampleType":"Data","Category":"Muon"},
	"nSingleMu_7"  : {"HT":"875", "Yield": 1.000e+00 ,"SampleType":"Data","Category":"Muon"},
	"photon_0"  : {"HT":"275", "Yield": 0 ,"SampleType":"Data","Category":"Photon"},
	"photon_1"  : {"HT":"325", "Yield": 0 ,"SampleType":"Data","Category":"Photon"},
	"photon_2"  : {"HT":"375", "Yield": 1.046e+03 ,"SampleType":"Data","Category":"Photon"},
	"photon_3"  : {"HT":"475", "Yield": 3.75e+02 ,"SampleType":"Data","Category":"Photon"},
	"photon_4"  : {"HT":"575", "Yield": 1.300e+02 ,"SampleType":"Data","Category":"Photon"},
	"photon_5"  : {"HT":"675", "Yield": 5.900e+01 ,"SampleType":"Data","Category":"Photon"},
	"photon_6"  : {"HT":"775", "Yield": 1.800e+01 ,"SampleType":"Data","Category":"Photon"},
	"photon_7"  : {"HT":"875", "Yield": 1.400e+01 ,"SampleType":"Data","Category":"Photon"},
	"photonmc_0"  : {"HT":"275", "Yield": 0 ,"SampleType":"Photon","Category":"Photon","Error":0},
	"photonmc_1"  : {"HT":"325", "Yield": 0 ,"SampleType":"Photon","Category":"Photon","Error":0},
	"photonmc_2"  : {"HT":"375", "Yield": 1.290e+03 ,"SampleType":"Photon","Category":"Photon","Error":4.00e+01},
	"photonmc_3"  : {"HT":"475", "Yield": 4.40e+02 ,"SampleType":"Photon","Category":"Photon","Error":2.00e+01},
	"photonmc_4"  : {"HT":"575", "Yield": 1.780e+02 ,"SampleType":"Photon","Category":"Photon","Error":1.00e+01},
	"photonmc_5"  : {"HT":"675", "Yield": 5.800e+01 ,"SampleType":"Photon","Category":"Photon","Error":8.00e+00},
	"photonmc_6"  : {"HT":"775", "Yield": 2.000e+01 ,"SampleType":"Photon","Category":"Photon","Error":5.00e+00},
	"photonmc_7"  : {"HT":"875", "Yield": 1.400e+01 ,"SampleType":"Photon","Category":"Photon","Error":3.00e+00}}


 
    i = 1
    self.table = open('Table_%s.tex'%i,'w')
    self.Prediction_Maker(sampleDictnjet)
    #self.Preiction_Maker(passed_dictionary)
    self.table.close()
    i += 1

  def Prediction_Maker(self,dict):
      
      inhad_zinv = False
      inhad_wjet = False
      indimuon = False
      inmuon = False
      inphoton = False

      #Bin_Info["Yield_Error"] = (m.sqrt(Grab_Integral.Integral()*float(Bin_Info["MC_Weight"]))*10.0*float(a.options.Lumo) if self.SampleInfo[input]["SampleType"] != "Data" else sqrt(float(Bin_Info["Yield"])))

      MC_Weights = {"TTbar":0.00425452,"WJetsInc":0.0666131,"WJets250":0.000450549,"WJets300":0.00102329,"Zinv50":0.00485311,"Zinv100":0.00410382,"Zinv200":0.0013739,"Zmumu":0.00849073,"Photon":1.,"Data":1.}

      self.bins = ('275','325','375','475','575','675','775','875')
      entries = ('Data','Yield','SM_Stat_Error','Muon_Trans','DiMuon_Trans','TotError')

      self.Had_Yield_Per_Bin = dict.fromkeys(self.bins)
      self.Had_Muon_Yield_Per_Bin = dict.fromkeys(self.bins)
      self.Had_Zmumu_Yield_Per_Bin = dict.fromkeys(self.bins)
      self.Muon_Yield_Per_Bin = dict.fromkeys(self.bins)
      self.DiMuon_Yield_Per_Bin = dict.fromkeys(self.bins)
      self.Photon_Yield_Per_Bin = dict.fromkeys(self.bins)

      dictionaries = [self.Had_Yield_Per_Bin,self.Had_Muon_Yield_Per_Bin,self.Had_Zmumu_Yield_Per_Bin,self.DiMuon_Yield_Per_Bin,self.Muon_Yield_Per_Bin,self.Photon_Yield_Per_Bin]
      for dicto in dictionaries:
        for key in self.bins:
          dicto[key] = dict.fromkeys(entries,0)
          dicto[key]['TotError'] = []

      for entry in dict:
        Error = 0
        if dict[entry]["Category"] is not "Photon" or  dict[entry]["SampleType"] is "Data": Error = m.sqrt(dict[entry]["Yield"]*float(MC_Weights[dict[entry]["SampleType"]])*46.5)
        else: Error = dict[entry]["Error"]

        if dict[entry]["SampleType"] == "Data":
          if dict[entry]["Category"] == "Had": 
            self.Had_Yield_Per_Bin[dict[entry]["HT"]]["Data"] = Data_Scaler(dict[entry]["HT"],dict[entry]["Yield"])
            self.Had_Muon_Yield_Per_Bin[dict[entry]["HT"]]["Data"] = Data_Scaler(dict[entry]["HT"],dict[entry]["Yield"])
            self.Had_Zmumu_Yield_Per_Bin[dict[entry]["HT"]]["Data"] = Data_Scaler(dict[entry]["HT"],dict[entry]["Yield"])
          if dict[entry]["Category"] == "Muon": self.Muon_Yield_Per_Bin[dict[entry]["HT"]]["Data"] = Data_Scaler(dict[entry]["HT"],dict[entry]["Yield"])
          if dict[entry]["Category"] == "DiMuon": self.DiMuon_Yield_Per_Bin[dict[entry]["HT"]]["Data"] = Data_Scaler(dict[entry]["HT"],dict[entry]["Yield"])
          if dict[entry]["Category"] == "Photon": self.Photon_Yield_Per_Bin[dict[entry]["HT"]]["Data"] = Data_Scaler(dict[entry]["HT"],dict[entry]["Yield"])

        elif dict[entry]["Category"] == "Had" :
            if dict[entry]["SampleType"] == "Zinv50" or dict[entry]["SampleType"] == "Zinv100" or dict[entry]["SampleType"] == "Zinv200": 
              inhad_zinv = True
              self.Had_Zmumu_Yield_Per_Bin[dict[entry]["HT"]]["Yield"] +=  dict[entry]["Yield"]
              self.Had_Zmumu_Yield_Per_Bin[dict[entry]["HT"]]["TotError"].append(Error)
            else:  
              inhad_wjet = True
              self.Had_Muon_Yield_Per_Bin[dict[entry]["HT"]]["Yield"] +=  dict[entry]["Yield"]
              self.Had_Muon_Yield_Per_Bin[dict[entry]["HT"]]["TotError"].append(Error)
            
            self.Had_Yield_Per_Bin[dict[entry]["HT"]]["Yield"] +=  dict[entry]["Yield"]
            self.Had_Yield_Per_Bin[dict[entry]["HT"]]["TotError"].append(Error)

        elif dict[entry]["Category"] == "Muon":
            inmuon = True
            self.Muon_Yield_Per_Bin[dict[entry]["HT"]]["Yield"] +=  dict[entry]["Yield"]
            self.Muon_Yield_Per_Bin[dict[entry]["HT"]]["TotError"].append(Error)
        elif dict[entry]["Category"] == "DiMuon":
            indimuon = True
            self.DiMuon_Yield_Per_Bin[dict[entry]["HT"]]["Yield"] +=  dict[entry]["Yield"]
            self.DiMuon_Yield_Per_Bin[dict[entry]["HT"]]["TotError"].append(Error)
        elif dict[entry]["Category"] == "Photon":
            inphoton = True
            self.Photon_Yield_Per_Bin[dict[entry]["HT"]]["Yield"] +=  dict[entry]["Yield"]
            self.Photon_Yield_Per_Bin[dict[entry]["HT"]]["TotError"].append(Error)
      
      for bin in self.Muon_Yield_Per_Bin: 
        for dict in dictionaries: 
          try:  dict[bin]["SM_Stat_Error"] = sqrt(reduce(lambda x,y : x+y,map(lambda x: x*x, dict[bin]["TotError"])))
          except TypeError: pass
       
      if inhad_wjet and indimuon and inmuon and inhad_zinv:
        category = "Combined_SM"
        self.Table_Prep(self.Muon_Yield_Per_Bin,self.Had_Muon_Yield_Per_Bin, comb = self.DiMuon_Yield_Per_Bin, comb_test=self.Had_Zmumu_Yield_Per_Bin)
        self.Produce_Tables(self.Dict_For_Table,category = category, dict2 = self.Combination_Pred_Table)

      if inhad_wjet and inphoton and inmuon and inhad_zinv:
        category = "Combined_SM_Photon"
        self.Table_Prep(self.Muon_Yield_Per_Bin,self.Had_Muon_Yield_Per_Bin, comb = self.Photon_Yield_Per_Bin, comb_test=self.Had_Zmumu_Yield_Per_Bin)
        self.Produce_Tables(self.Dict_For_Table,category = category, dict2 = self.Combination_Pred_Table)

      if inmuon and inhad_zinv and inhad_wjet:
        category = "Total_SM"
        self.Table_Prep(self.Muon_Yield_Per_Bin,self.Had_Yield_Per_Bin)
        self.Produce_Tables(self.Dict_For_Table,category = category)
        self.Ratio_Plots(self.Dict_For_Table, category = category)

      if inhad_wjet and inmuon:
        category = "Muon"
        self.Table_Prep(self.Muon_Yield_Per_Bin,self.Had_Muon_Yield_Per_Bin)
        self.Produce_Tables(self.Dict_For_Table,category = category)
        self.Ratio_Plots(self.Dict_For_Table, category = category)

      if inphoton and inhad_zinv:
        category = "Photon_Zinv"
        self.Table_Prep(self.Photon_Yield_Per_Bin,self.Had_Zmumu_Yield_Per_Bin)
        self.Produce_Tables(self.Dict_For_Table,category = category)
        self.Ratio_Plots(self.Dict_For_Table, category = category)

      if inhad_zinv and indimuon:
        category = "Di_Muon_Zinv"
        self.Table_Prep(self.DiMuon_Yield_Per_Bin,self.Had_Zmumu_Yield_Per_Bin)
        self.Produce_Tables(self.Dict_For_Table,category = category)
        self.Ratio_Plots(self.Dict_For_Table, category = category)

      if inmuon and indimuon:
        category = "Di_Muon"
        self.Table_Prep(self.Muon_Yield_Per_Bin,self.DiMuon_Yield_Per_Bin)
        self.Produce_Tables(self.Dict_For_Table,category = category)
        self.Ratio_Plots(self.Dict_For_Table, category = category)


      if inphoton and indimuon:
        category = "Photon_DiMuon"
        self.Table_Prep(self.Photon_Yield_Per_Bin,self.DiMuon_Yield_Per_Bin)
        self.Produce_Tables(self.Dict_For_Table,category = category)
        self.Ratio_Plots(self.Dict_For_Table, category = category)

      if inphoton and inmuon:
        category = "Photon_Muon"
        self.Table_Prep(self.Photon_Yield_Per_Bin,self.Muon_Yield_Per_Bin)
        self.Produce_Tables(self.Dict_For_Table,category = category)
        self.Ratio_Plots(self.Dict_For_Table, category = category)

  
  def Ratio_Plots(self,dict,category =""):
      c1 = TCanvas() 
      ratio_plot = TH1F("ratio_plot","",8,0,8)
      ratio_plot.GetXaxis().SetTitle("H_{T} (GeV)")
      ratio_plot.GetYaxis().SetTitle("Translation Factor")
      ratio_plot.GetYaxis().SetTitleSize(0.055)
      ratio_plot.GetYaxis().SetTitleOffset(.85)
      ratio_plot.GetXaxis().SetTitleSize(0.05)
      ratio_plot.GetYaxis().SetTitleSize(0.06)
      ratio_plot.SetTitle("%s Sample" %category)
      data_plot = ratio_plot.Clone()
      pred_plot = ratio_plot.Clone()
      RatioTitleEntries = ["275","325","375","475","575","675","775","875"]
      for num,bin in enumerate(sorted(dict.iterkeys())):
        ratio_plot.SetBinContent(num+1,dict[bin]["Trans"])
        ratio_plot.SetBinError(num+1,dict[bin]["Trans_Error"])
        ratio_plot.GetXaxis().SetBinLabel(num+1,RatioTitleEntries[num])
      ratio_plot.SetStats(0)
      ratio_plot.Draw("P")
      c1.SaveAs("%s_Prediction_Traslation_Factor.png" %category)

      data_plot.GetYaxis().SetTitle("Events")
      for num,bin in enumerate(sorted(dict.iterkeys())):
        data_plot.SetBinContent(num+1,dict[bin]["Data"])
        data_plot.SetBinError(num+1,m.sqrt(dict[bin]["Data"]))
        data_plot.GetXaxis().SetBinLabel(num+1,RatioTitleEntries[num])
        pred_plot.SetBinContent(num+1,dict[bin]["Prediction"])
        pred_plot.SetBinError(num+1,dict[bin]["Pred_Error"])
      pred_plot.SetLineColor(4)
      pred_plot.SetMarkerColor(4)
      data_plot.Draw("P")
      pred_plot.Draw("Psame")
      c1.SaveAs("%s_Prediction_Numbers.png" %category)

  def Table_Prep(self,control,test,comb="",comb_test=""):

      self.Dict_For_Table = dict.fromkeys(self.bins)
      self.Combination_Pred_Table = dict.fromkeys(self.bins)
      entries = ('Data_Pred','Prediction','Pred_Error','Data','Trans','Trans_Error')
      dictionaries = [self.Dict_For_Table,self.Combination_Pred_Table]

      for dicto in dictionaries:
        for key in self.bins: dicto[key] = dict.fromkeys(entries,0)

      for bin in control: 
          try:
            self.Dict_For_Table[bin]['Trans'] = test[bin]["Yield"]/control[bin]["Yield"]
          except ZeroDivisionError: pass
          try: control_error =  control[bin]["SM_Stat_Error"]/control[bin]["Yield"] 
          except ZeroDivisionError: control_error = 0
          try :test_error =  test[bin]["SM_Stat_Error"]/test[bin]["Yield"] 
          except ZeroDivisionError: test_error = 0
          self.Dict_For_Table[bin]['Trans_Error'] = self.Dict_For_Table[bin]['Trans'] * m.sqrt((control_error*control_error)+(test_error*test_error))
          self.Dict_For_Table[bin]['Data_Pred'] = control[bin]["Data"]
          self.Dict_For_Table[bin]['Prediction'] = control[bin]["Data"]*self.Dict_For_Table[bin]['Trans']
          self.Dict_For_Table[bin]['Data'] = test[bin]["Data"]
          try:self.Dict_For_Table[bin]['Pred_Error'] = self.Dict_For_Table[bin]['Prediction']*m.sqrt((1/self.Dict_For_Table[bin]['Data_Pred'])+((self.Dict_For_Table[bin]['Trans_Error']/self.Dict_For_Table[bin]['Trans'])*(self.Dict_For_Table[bin]['Trans_Error']/self.Dict_For_Table[bin]['Trans'])))
          except ZeroDivisionError: self.Dict_For_Table[bin]['Pred_Error'] = 0

      if comb:
        for bin in control:
          try:self.Combination_Pred_Table[bin]['Trans'] = comb_test[bin]["Yield"]/comb[bin]["Yield"]
          except ZeroDivisionError: pass
          try: control_error =  comb[bin]["SM_Stat_Error"]/comb[bin]["Yield"] 
          except ZeroDivisionError: control_error = 0
          try :test_error =  comb_test[bin]["SM_Stat_Error"]/comb_test[bin]["Yield"] 
          except ZeroDivisionError: test_error = 0
          self.Combination_Pred_Table[bin]['Trans_Error'] = self.Combination_Pred_Table[bin]['Trans'] * m.sqrt((control_error*control_error)+(test_error*test_error))
          self.Combination_Pred_Table[bin]['Data_Pred'] = comb[bin]["Data"]
          self.Combination_Pred_Table[bin]['Prediction'] = comb[bin]["Data"]*self.Combination_Pred_Table[bin]['Trans']
          self.Combination_Pred_Table[bin]['Data'] = comb_test[bin]["Data"]
          try:self.Combination_Pred_Table[bin]['Pred_Error'] = self.Combination_Pred_Table[bin]['Prediction']*m.sqrt((1/self.Combination_Pred_Table[bin]['Data_Pred'])+((self.Combination_Pred_Table[bin]['Trans_Error']/self.Combination_Pred_Table[bin]['Trans'])*(self.Combination_Pred_Table[bin]['Trans_Error']/self.Combination_Pred_Table[bin]['Trans'])))
          except ZeroDivisionError: self.Combination_Pred_Table[bin]['Pred_Error'] = 0


  def Produce_Tables(self,dict,category="",dict2 =""):
      print "\n\nMaking Tables for %s" % category
      
      if category == "Total_SM": self.Latex_Table(dict,caption = "Binned %s Predictions" %category, 
            rows = [{"label": r'''Hadronic selection MC''',"entryFunc": self.MakeList(self.Had_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''$\mu +$ jets selection MC''',         "entryFunc":self.MakeList(self.Muon_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''Translation factor ''',                "entryFunc":self.MakeList(dict,"Trans","Trans_Error")},
                    {"label": r'''$\mu +$ jets selection yield data''',       "entryFunc":self.MakeList(dict,"Data_Pred")},
                    {"label":r'''Total SM prediction''', "entryFunc":self.MakeList(dict,"Prediction","Pred_Error")},
                    {"label": r'''Hadronic yield data''',       "entryFunc":self.MakeList(dict,"Data")},])
            
      if category == "Muon": self.Latex_Table(dict,caption = "Binned %s Predictions" %category, 
            rows = [{"label": r'''$t\bar{t}$ + W  Hadronic selection MC''',"entryFunc": self.MakeList(self.Had_Muon_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''$\mu +$ jets MC selection''',         "entryFunc":self.MakeList(self.Muon_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''Translation factor''',                "entryFunc":self.MakeList(dict,"Trans","Trans_Error")},
                    {"label": r'''$\mu +$ jets selection yield data''',       "entryFunc":self.MakeList(dict,"Data_Pred")},
                    {"label":r'''$t\bar{t}$ + W prediction''', "entryFunc":self.MakeList(dict,"Prediction","Pred_Error")},])
            
      if category == "Photon_DiMuon": self.Latex_Table(dict,caption = "Binned %s Predictions" %category, 
            rows = [{"label": r'''$\mu\bar{\mu} +$ jets selection MC''',"entryFunc": self.MakeList(self.DiMuon_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r''' $\gamma +$ jets selection MC''',         "entryFunc":self.MakeList(self.Photon_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''Translation factor''',                "entryFunc":self.MakeList(dict,"Trans","Trans_Error")},
                    {"label": r'''$\gamma +$ jets yield data''',       "entryFunc":self.MakeList(dict,"Data_Pred")},
                    {"label":r'''$\mu\bar{\mu} +$ jets  prediction''', "entryFunc":self.MakeList(dict,"Prediction","Pred_Error")},
                    {"label": r'''$\mu\bar{\mu} +$ jets yield data''',       "entryFunc":self.MakeList(dict,"Data")},])

      if category == "Photon_Muon": self.Latex_Table(dict,caption = "Binned %s Predictions" %category, 
            rows = [{"label": r'''$\mu + jets}$ selection  MC''',"entryFunc": self.MakeList(self.Muon_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''$\gamma+$ jets selection MC''',         "entryFunc":self.MakeList(self.Photon_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''Translation factor''',                "entryFunc":self.MakeList(dict,"Trans","Trans_Error")},
                    {"label": r'''$\gamma +$ jets yield data''',       "entryFunc":self.MakeList(dict,"Data_Pred")},
                    {"label":r'''$\mu + jets$ prediction''', "entryFunc":self.MakeList(dict,"Prediction","Pred_Error")},
                    {"label": r'''$\mu + jets$ yield data''',       "entryFunc":self.MakeList(dict,"Data")},])

      if category == "Di_Muon": self.Latex_Table(dict,caption = "Binned %s Predictions" %category, 
            rows = [{"label": r'''$\mu\bar{\mu} +$ jets selection MC''',"entryFunc": self.MakeList(self.DiMuon_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''$\mu +$ jets selection MC''',         "entryFunc":self.MakeList(self.Muon_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''Translation factor''',                "entryFunc":self.MakeList(dict,"Trans","Trans_Error")},
                    {"label": r'''$\mu +$ jets yield data''',       "entryFunc":self.MakeList(dict,"Data_Pred")},
                    {"label":r'''$\mu\bar{\mu} +$ jets selection  prediction''', "entryFunc":self.MakeList(dict,"Prediction","Pred_Error")},
                    {"label": r'''$\mu\bar{\mu} +$ jets selection yield data''',       "entryFunc":self.MakeList(dict,"Data")},])
     
      if category == "Di_Muon_Zinv": self.Latex_Table(dict,caption = "Binned %s Predictions" %category, 
            rows = [{"label": r'''Z$\rightarrow\nu\bar{\nu}$ hadronic selection MC''',"entryFunc": self.MakeList(self.Had_Zmumu_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''$\mu\bar{\mu} +$ jets selection MC''',         "entryFunc":self.MakeList(self.DiMuon_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''Translation factor''',                "entryFunc":self.MakeList(dict,"Trans","Trans_Error")},
                    {"label": r'''\mu\bar{\mu} +$ jets selection yield data''',       "entryFunc":self.MakeList(dict,"Data_Pred")},
                    {"label":r'''Z$\rightarrow\nu\bar{\nu}$ prediction''', "entryFunc":self.MakeList(dict,"Prediction","Pred_Error")}])

      if category == "Photon_Zinv": self.Latex_Table(dict,caption = "Binned %s Predictions" %category, 
            rows = [{"label": r'''Z$\rightarrow\nu\bar{\nu}$ hadronic selection MC''',"entryFunc": self.MakeList(self.Had_Zmumu_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''$\gamma +$ jets selection MC''',         "entryFunc":self.MakeList(self.Photon_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''Translation factor''',                "entryFunc":self.MakeList(dict,"Trans","Trans_Error")},
                    {"label": r'''$\gamma +$ jet selection yield data''',       "entryFunc":self.MakeList(dict,"Data_Pred")},
                    {"label":r'''Z$\rightarrow\nu\bar{\nu}$ prediction''', "entryFunc":self.MakeList(dict,"Prediction","Pred_Error")}])
               
      if category == "Combined_SM": self.Latex_Table(dict,caption = "Binned %s Predictions" %category, 
            rows = [{"label": r'''t$\bar{t}$ + W prediction from $\mu +$ jets''', "entryFunc":self.MakeList(dict,"Prediction","Pred_Error")},
                    {"label": r'''Z$\rightarrow\nu\bar{\nu}$ prediction from $\mu\mu +$ jets''', "entryFunc":self.MakeList(dict2,"Prediction","Pred_Error")},
                    {"label":r'''Total SM prediction''', "entryFunc":self.MakeList(dict,"Prediction","Pred_Error",combined=dict2)},
                    {"label": r'''Hadronic yield from data''',  "entryFunc":self.MakeList(dict,"Data")},])
                   
      if category == "Combined_SM_Photon": self.Latex_Table(dict,caption = "Binned %s Predictions" %category, 
            rows = [{"label": r'''$t\bar{t}$ + W prediction from $\mu +$ jets''', "entryFunc":self.MakeList(dict,"Prediction","Pred_Error")},
                    {"label": r'''$Z\rightarrow\nu\bar{\nu}$ Prediction from $\gamma +$ jets''', "entryFunc":self.MakeList(dict2,"Prediction","Pred_Error")},
                    {"label":r'''Total SM prediction''', "entryFunc":self.MakeList(dict,"Prediction","Pred_Error",combined=dict2)},
                    {"label": r'''Hadronic yield from data''',  "entryFunc":self.MakeList(dict,"Data")},]) 
      
  def MakeList(self,dict,key,error = "",combined = ""):
      List = []
      for entry in sorted(dict.iterkeys()):
        if error: List.append(self.toString("%4.2f" %(dict[entry][key]+combined[entry][key] if combined else dict[entry][key]))+"  $\pm$  "+ self.toString("%4.2f" %(dict[entry][error]+combined[entry][error] if combined else dict[entry][error])))
        else: List.append(self.toString("%4.2f" %(dict[entry][key]+combined[entry][key] if combined else dict[entry][key])))
      return List  
        
  def oneRow(self,label = "", labelWidth = 23, entryList = [], entryWidth = 30, extra = "") :
    s = ""
    s += "\n"+label.ljust(labelWidth)+" & "+" & ".join([(self.toString(entry)).ljust(entryWidth) for entry in entryList])+r"\\ "
    return s 

  def toString(self,item) :
    if type(item) is float : return str(item)
    else : return str(item)
  
  def Latex_Table(self,dict,rows,caption = ""):
      s = "\n"
      s += r'''\begin{table}[ht!]'''
      s += "\n\caption{%s %s fb$^{-1}$}"%(caption,"4.7")
      s += "\n\label{tab:results-W}"
      s += "\n\centering"
      s += "\n"+r'''\footnotesize'''
      s += "\n\\begin{tabular}{ |c|c|c|c|c| }"
      s += "\n\hline"    
      fullBins = list(sorted(dict.iterkeys())) + ["$\infty$"]
      for subTable in range(2) :
          start = 0 + subTable*len(fullBins)/2
          stop = 1 + (1+subTable)*len(fullBins)/2
          indices = range(start,stop-1)[:len(fullBins)/2]
          bins = fullBins[start:stop]
          if subTable == 1:
            s += "\n\hline"
      	  s += self.oneRow(label ="\scalht Bin (GeV)", entryList = [("%s--%s"%(l, u)) for l,u in zip(bins[:-1], bins[1:])], extra = "[0.5ex]")
          s += "\n\hline" 
          for row in rows:
          	s += self.oneRow(label = row["label"], entryList = (row["entryFunc"][i] for i in indices),entryWidth=row["entryWidth"] if "entryWidth" in row else 30)      
      s += "\n\hline"
      s += "\n\end{tabular}"
      s += "\n\end{table}"
      s += "\n\n\n\n"
      self.table.write(s)
      print s

if __name__=="__main__":
  a = Number_Extractor("Hi")

