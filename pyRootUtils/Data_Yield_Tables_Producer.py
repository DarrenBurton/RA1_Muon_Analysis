#!/usr/bin/env python
from ROOT import *
import ROOT as r
import logging,itertools
import os,fnmatch,sys
import glob, errno
from time import strftime
from optparse import OptionParser
import array, ast
import math as m
from plottingUtils import *
from Bryn_Numbers import *


settings = {
  #"dirs":["275_325"],
  "dirs":["275_325","325_375","375_475","475_575","575_675","675_775","775_875","875",],
  "plots":["AlphaT_all",],
  "AlphaTBins":[(int(0.51/0.01),int(0.52/0.01)),(int(0.52/0.01),int(0.53/0.01)),(int(0.53/0.01),int(0.55/0.01)),(int(0.55/0.01),int(10./0.01)+1),],
  "AlphaTSlices":["0.52_0.53","0.53_0.55","0.55_20"]
  #"AlphaTSlices":["0.55_10"]
      }

samples = {
    "nMuon":("./Root_Files/Muon_Data","OneMuon_","Data","Muon"),
    "nDiMuon":("./Root_Files/Muon_Data","DiMuon_","Data","DiMuon"),
    "nHad":("./Root_Files/Had_Data","","Data","Had"),
   
    }

l1_offset_samples = {
    "nMuon":("./Root_Files/L1_Offset_Had","","Data","Muon"),
    "nHad":("./Root_Files/Data_Had","","Data","Had"),
   
    }



if __name__=="__main__":
  a = Number_Extractor(settings,l1_offset_samples,"HT_Dataset_Offset_vs")
