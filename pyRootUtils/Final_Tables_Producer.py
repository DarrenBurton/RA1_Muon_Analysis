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
  "dirs":["275_325","325_375","375_475","475_575","575_675","675_775","775_875","875",],  #HT Bins
  "plots":["AlphaT_all",],  # Histogram that Yields are taken from
  "AlphaTSlices":["0.52_0.53","0.53_0.55","0.55_20"], # AlphaT Slices
  "Lumo":3.79, # Luminosity in fb
  #"AlphaTSlices":["0.55_10"]
      }


'''
Sample Dictionary Instructions

eg "nMuon":("./Root_Files/Muon_Data","OneMuon_","Data","Muon"),
if n at start of name entry then the file is data and will no be scaled to luminosity.
first argument is path to root file
second argument is prefix to ht bin. i.e OneMuon_275_325
third argument is data/mc type, i.e. Data, WJets250 - MC relating to the binned WJets 250-300 HT sample
fourth argument is sample Type, Had/DiMuon/Muon. 

the only thing that will have to be changed is the second argument depending on wether you are running btag multiplicity/baseline

baseline = "OneMuon_"
0>= btag = "btag_morethanzero_OneMuon_"
0 btags = "btag_zero_OneMuon"
etc.....
'''

samples = {
    "nMuon":("./Root_Files/Muon_Data","OneMuon_","Data","Muon"),
    
    #Muon MC
     "mcMuonW1":("./Root_Files/Muon_WJetsInc","OneMuon_","WJetsInc","Muon"),
     "mcMuonW2":("./Root_Files/Muon_WJets250","OneMuon_","WJets250","Muon"),
     "mcMuonW3":("./Root_Files/Muon_WJets300","OneMuon_","WJets300","Muon"),
     "mcMuonTtw":("./Root_Files/Muon_TTbar","OneMuon_","TTbar","Muon"),
     "mcMuonDY":("./Root_Files/Muon_DY","OneMuon_","DY","Muon"),
     "mcMuon_Singt":("./Root_Files/Muon_Single_T_t","OneMuon_","Single_T_t","Muon"),
     "mcMuon_SingtW":("./Root_Files/Muon_Single_T_tW","OneMuon_","Single_T_tW","Muon"),
     "mcMuon_Singtbar_t":("./Root_Files/Muon_Single_Tbar_t","OneMuon_","Single_Tbar_t","Muon"),
     "mcMuon_Singtbar_tw":("./Root_Files/Muon_Single_Tbar_tW","OneMuon_","Single_Tbar_tW","Muon"),
     "mcMuonZZ":("./Root_Files/Muon_ZZ","OneMuon_","ZZ","Muon"),
     "mcMuonWW":("./Root_Files/Muon_WW","OneMuon_","WW","Muon"),
     "mcMuonWZ":("./Root_Files/Muon_WZ","OneMuon_","WZ","Muon"),

    "nDiMuon":("./Root_Files/Muon_Data","DiMuon_","Data","DiMuon"),
    
    #Muon MC
     "mcDiMuonW1":("./Root_Files/Muon_WJetsInc","DiMuon_","WJetsInc","DiMuon"),
     "mcDiMuonW2":("./Root_Files/Muon_WJets250","DiMuon_","WJets250","DiMuon"),
     "mcDiMuonW3":("./Root_Files/Muon_WJets300","DiMuon_","WJets300","DiMuon"),
     "mcDiMuonTtw":("./Root_Files/Muon_TTbar","DiMuon_","TTbar","DiMuon"),
     "mcDiMuonDY":("./Root_Files/Muon_DY","DiMuon_","DY","DiMuon"),
     "mcDiMuon_Singt":("./Root_Files/Muon_Single_T_t","DiMuon_","Single_T_t","DiMuon"),
     "mcDiMuon_SingtW":("./Root_Files/Muon_Single_T_tW","DiMuon_","Single_T_tW","DiMuon"),
     "mcDiMuon_Singtbar_t":("./Root_Files/Muon_Single_Tbar_t","DiMuon_","Single_Tbar_t","DiMuon"),
     "mcDiMuon_Singtbar_tw":("./Root_Files/Muon_Single_Tbar_tW","DiMuon_","Single_Tbar_tW","DiMuon"),
     "mcDiMuonZZ":("./Root_Files/Muon_ZZ","DiMuon_","ZZ","DiMuon"),
     "mcDiMuonWW":("./Root_Files/Muon_WW","DiMuon_","WW","DiMuon"),
     "mcMuonWZ":("./Root_Files/Muon_WZ","DiMuon_","WZ","DiMuon"),

    "nHad":("./Root_Files/Had_Data","","Data","Had"),
    
    #Muon MC
     "mcHadW1":("./Root_Files/Had_WJetsInc","","WJetsInc","Had"),
     "mcHadW2":("./Root_Files/Had_WJets250","","WJets250","Had"),
     "mcHadW3":("./Root_Files/Had_WJets300","","WJets300","Had"),
     "mcHadTtw":("./Root_Files/Had_TTbar","","TTbar","Had"),
     "mcHadZ1":("./Root_Files/Had_Zinv50","","Zinv50","Had"),
     "mcHadZ2":("./Root_Files/Had_Zinv100","","Zinv100","Had"),
     "mcHadZ3":("./Root_Files/Had_Zinv200","","Zinv200","Had"),
     "mcHadDY":("./Root_Files/Had_DY","","DY","Had"),
     "mcHad_Singt":("./Root_Files/Had_Single_T_t","","Single_T_t","Had"),
     "mcHad_SingtW":("./Root_Files/Had_Single_T_tW","","Single_T_tW","Had"),
     "mcHad_Singtbar_t":("./Root_Files/Had_Single_Tbar_t","","Single_Tbar_t","Had"),
     "mcHad_Singtbar_tw":("./Root_Files/Had_Single_Tbar_tW","","Single_Tbar_tW","Had"),
     "mcHadZZ":("./Root_Files/Had_ZZ","","ZZ","Had"),
     "mcHadWW":("./Root_Files/Had_WW","","WW","Had"),
     "mcHadWZ":("./Root_Files/Had_WZ","","WZ","Had"),



    }


'''
Number_Extractor Instructions

Imported from Bryn_Numbers.py
1st/2nd argument never change, just passing the files to be read in and the parameters to produce numbers
3rd argument is prefix that output files are appeneded with, so if using btag analysis change string to something that reflects this

Additional arguments

Triggers = Apply Trigger Corrections
AlphaT = Keeps AlphaT cut for control samples. Use for baseline/ Jads closure tests which go from no alphaT cut to an alphaT cut
Stats = Make Root Output Stats File for use by Sam/Ted. Doesn't produce output tex tables if True
Trans_Plots = Make 2D histos of yields/Translation factors. Not really important anymore.
'''

if __name__=="__main__":
  a = Number_Extractor(settings,samples,"Baseline",Triggers = "False",AlphaT="True")
