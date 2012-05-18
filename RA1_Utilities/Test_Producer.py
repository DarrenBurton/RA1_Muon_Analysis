#!/usr/bin/env python
from ROOT import *
import ROOT as r
import logging,itertools
import os,fnmatch,sys
import glob, errno
from time import strftime
from optparse import OptionParser
import array  #, ast
import math as m
from plottingUtils import *
from Bryn_Numbers import *


settings = {
  #"dirs":["275_325"],
  "dirs":["275_325","325_375","375_475","475_575","575_675","675_775","775_875","875",],  #HT Bins
  "plots":["AlphaT_all",],  # Histogram that Yields are taken from
  #"AlphaTSlices":["0.52_0.53","0.53_0.55","0.55_20"], # AlphaT Slices
  "AlphaTSlices":["0.55_20"], # AlphaT Slices
  "Lumo":0.1, # Luminosity in fb
  #"AlphaTSlices":["0.55_10"]
      }


'''
Sample Dictionary Instructions

eg "nMuon":("./Root_Files/Muon_Data","btag_two_OneMuon_","Data","Muon"),
if n at start of name entry then the file is data and will no be scaled to luminosity.
first argument is path to root file
second argument is prefix to ht bin. i.e OneMuon_275_325
third argument is data/mc type, i.e. Data, WJets250 - MC relating to the binned WJets 250-300 HT sample
fourth argument is sample Type, Had/DiMuon/Muon. 

the only thing that will have to be changed is the second argument depending on wether you are running btag multiplicity/baseline
'''
btag_two_samples = {
     "mcHadW1":("./MC_Test","","WJetsInc","Had"),
     "mcHadW2":("./MC_Test","","Data","Had"),

    }


calc_file = {
     "mcHadW1":("./MC_Test.root","Had",""),
     "mcHadW2":("./MC_Muon_Test.root","Muon","OneMuon_"),
     #"mcHadW3":("./Root_Files/Had_WJets300","DiMuon","DiMuon_"),

}

if __name__=="__main__":
  a = Number_Extractor(settings,btag_two_samples,"Inclusive",Triggers = "True",AlphaT="False",Calculation=calc_file)
