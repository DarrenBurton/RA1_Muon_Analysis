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
from RA1_8TeV import *


settings = {
  #"dirs":["275_325"],
  "dirs":["275_325","325_375","375_475","475_575","575_675","675_775","775_875","875",],  #HT Bins
  "plots":["AlphaT_all",],  # Histogram that Yields are taken from
  #"AlphaTSlices":["0.52_0.53","0.53_0.55","0.55_20"], # AlphaT Slices
  "AlphaTSlices":["0.55_20"], # AlphaT Slices
  "Lumo":0.101, # Luminosity in fb
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

baseline = "btag_two_OneMuon_"
0>= btag = "btag_two_OneMuon_"
0 btags = "btag_two_OneMuon_"
etc.....
'''
btag_morethan_two_samples = {
    "nMuon":("./Root_Files/Muon_Data","btag_morethantwo_OneMuon_","Data","Muon"),
    
    #Muon MC
     "mcMuonW3":("./Root_Files/Muon_WJets","btag_morethantwo_OneMuon_","WJetsInc","Muon"),
     "mcMuonTtw":("./Root_Files/Muon_TTbar","btag_morethantwo_OneMuon_","TTbar","Muon"),
     "mcMuonDY":("./Root_Files/Muon_DY","btag_morethantwo_OneMuon_","DY","Muon"),
    "nDiMuon":("./Root_Files/Muon_Data","btag_morethantwo_DiMuon_","Data","DiMuon"),
    
    #Muon MC
     "mcDiMuonW2":("./Root_Files/Muon_WJets","btag_morethantwo_DiMuon_","WJetsInc","DiMuon"),
     "mcDiMuonTtw":("./Root_Files/Muon_TTbar","btag_morethantwo_DiMuon_","TTbar","DiMuon"),
     "mcDiMuonDY":("./Root_Files/Muon_DY","btag_morethantwo_DiMuon_","DY","DiMuon"),
         "nHad":("./Root_Files/Had_Data","btag_morethantwo_","Data","Had"),
    
    #Muon MC
     "mcHadW3":("./Root_Files/Had_WJets","btag_morethantwo_","WJetsInc","Had"),
     "mcHadTtw":("./Root_Files/Had_TTbar","btag_morethantwo_","TTbar","Had"),
     "mcHadDY":("./Root_Files/Had_DY","btag_morethantwo_","DY","Had"),
         }

btag_morethan_one_samples = {
    "nMuon":("./Root_Files/Muon_Data","btag_morethanone_OneMuon_","Data","Muon"),
    
    #Muon MC
     "mcMuonW1":("./Root_Files/Muon_WJets","btag_morethanone_OneMuon_","WJetsInc","Muon"),
     "mcMuonTtw":("./Root_Files/Muon_TTbar","btag_morethanone_OneMuon_","TTbar","Muon"),
     "mcMuonDY":("./Root_Files/Muon_DY","btag_morethanone_OneMuon_","DY","Muon"),
         "nDiMuon":("./Root_Files/Muon_Data","btag_morethanone_DiMuon_","Data","DiMuon"),
    
    #Muon MC
     "mcDiMuonW1":("./Root_Files/Muon_WJets","btag_morethanone_DiMuon_","WJetsInc","DiMuon"),
     "mcDiMuonTtw":("./Root_Files/Muon_TTbar","btag_morethanone_DiMuon_","TTbar","DiMuon"),
     "mcDiMuonDY":("./Root_Files/Muon_DY","btag_morethanone_DiMuon_","DY","DiMuon"),

    "nHad":("./Root_Files/Had_Data","btag_morethanone_","Data","Had"),
    
    #Muon MC
     "mcHadW1":("./Root_Files/Had_WJets","btag_morethanone_","WJetsInc","Had"),
     "mcHadTtw":("./Root_Files/Had_TTbar","btag_morethanone_","TTbar","Had"),
     "mcHadDY":("./Root_Files/Had_DY","btag_morethanone_","DY","Had"),

    }

btag_morethan_zero_samples = {
    "nMuon":("./Root_Files/Muon_Data","btag_morethanzero_OneMuon_","Data","Muon"),
    
    #Muon MC
     "mcMuonW1":("./Root_Files/Muon_WJets","btag_morethanzero_OneMuon_","WJetsInc","Muon"),
     "mcMuonTtw":("./Root_Files/Muon_TTbar","btag_morethanzero_OneMuon_","TTbar","Muon"),
     "mcMuonDY":("./Root_Files/Muon_DY","btag_morethanzero_OneMuon_","DY","Muon"),

    "nDiMuon":("./Root_Files/Muon_Data","btag_morethanzero_DiMuon_","Data","DiMuon"),
    
    #Muon MC
     "mcDiMuonW1":("./Root_Files/Muon_WJets","btag_morethanzero_DiMuon_","WJetsInc","DiMuon"),
     "mcDiMuonTtw":("./Root_Files/Muon_TTbar","btag_morethanzero_DiMuon_","TTbar","DiMuon"),
     "mcDiMuonDY":("./Root_Files/Muon_DY","btag_morethanzero_DiMuon_","DY","DiMuon"),

    "nHad":("./Root_Files/Had_Data","btag_morethanzero_","Data","Had"),
    
    #Muon MC
     "mcHadW1":("./Root_Files/Had_WJets","btag_morethanzero_","WJetsInc","Had"),
     "mcHadTtw":("./Root_Files/Had_TTbar","btag_morethanzero_","TTbar","Had"),
     "mcHadDY":("./Root_Files/Had_DY","btag_morethanzero_","DY","Had"),

    }



btag_zero_samples = {
    "nMuon":("./Root_Files/Muon_Data","btag_zero_OneMuon_","Data","Muon"),
    
    #Muon MC
     "mcMuonW1":("./Root_Files/Muon_WJets","btag_zero_OneMuon_","WJetsInc","Muon"),
     "mcMuonTtw":("./Root_Files/Muon_TTbar","btag_zero_OneMuon_","TTbar","Muon"),
     "mcMuonDY":("./Root_Files/Muon_DY","btag_zero_OneMuon_","DY","Muon"),

    "nDiMuon":("./Root_Files/Muon_Data","btag_zero_DiMuon_","Data","DiMuon"),
    
    #Muon MC
     "mcDiMuonW1":("./Root_Files/Muon_WJets","btag_zero_DiMuon_","WJetsInc","DiMuon"),
     "mcDiMuonTtw":("./Root_Files/Muon_TTbar","btag_zero_DiMuon_","TTbar","DiMuon"),
     "mcDiMuonDY":("./Root_Files/Muon_DY","btag_zero_DiMuon_","DY","DiMuon"),

    "nHad":("./Root_Files/Had_Data","btag_zero_","Data","Had"),
    
    #Muon MC
     "mcHadW1":("./Root_Files/Had_WJets","btag_zero_","WJetsInc","Had"),
     "mcHadTtw":("./Root_Files/Had_TTbar","btag_zero_","TTbar","Had"),
     "mcHadDY":("./Root_Files/Had_DY","btag_zero_","DY","Had"),

    }


btag_one_samples = {
    "nMuon":("./Root_Files/Muon_Data","btag_one_OneMuon_","Data","Muon"),
    
    #Muon MC
     "mcMuonW1":("./Root_Files/Muon_WJets","btag_one_OneMuon_","WJetsInc","Muon"),
     "mcMuonTtw":("./Root_Files/Muon_TTbar","btag_one_OneMuon_","TTbar","Muon"),
     "mcMuonDY":("./Root_Files/Muon_DY","btag_one_OneMuon_","DY","Muon"),

    "nDiMuon":("./Root_Files/Muon_Data","btag_one_DiMuon_","Data","DiMuon"),
    
    #Muon MC
     "mcDiMuonW1":("./Root_Files/Muon_WJets","btag_one_DiMuon_","WJetsInc","DiMuon"),
     "mcDiMuonTtw":("./Root_Files/Muon_TTbar","btag_one_DiMuon_","TTbar","DiMuon"),
     "mcDiMuonDY":("./Root_Files/Muon_DY","btag_one_DiMuon_","DY","DiMuon"),

    "nHad":("./Root_Files/Had_Data","btag_one_","Data","Had"),
    
    #Muon MC
     "mcHadW1":("./Root_Files/Had_WJets","btag_one_","WJetsInc","Had"),
     "mcHadTtw":("./Root_Files/Had_TTbar","btag_one_","TTbar","Had"),
     "mcHadDY":("./Root_Files/Had_DY","btag_one_","DY","Had"),

    }



btag_two_samples = {
    "nMuon":("./Root_Files/Muon_Data","btag_two_OneMuon_","Data","Muon"),
    
    #Muon MC
     "mcMuonW1":("./Root_Files/Muon_WJets","btag_two_OneMuon_","WJetsInc","Muon"),
     "mcMuonTtw":("./Root_Files/Muon_TTbar","btag_two_OneMuon_","TTbar","Muon"),
     "mcMuonDY":("./Root_Files/Muon_DY","btag_two_OneMuon_","DY","Muon"),

    "nDiMuon":("./Root_Files/Muon_Data","btag_two_DiMuon_","Data","DiMuon"),
    
    #Muon MC
     "mcDiMuonW1":("./Root_Files/Muon_WJets","btag_two_DiMuon_","WJetsInc","DiMuon"),
     "mcDiMuonTtw":("./Root_Files/Muon_TTbar","btag_two_DiMuon_","TTbar","DiMuon"),
     "mcDiMuonDY":("./Root_Files/Muon_DY","btag_two_DiMuon_","DY","DiMuon"),

    "nHad":("./Root_Files/Had_Data","btag_two_","Data","Had"),
    
    #Muon MC
     "mcHadW1":("./Root_Files/Had_WJets","btag_two_","WJetsInc","Had"),
     "mcHadTtw":("./Root_Files/Had_TTbar","btag_two_","TTbar","Had"),
     "mcHadDY":("./Root_Files/Had_DY","btag_two_","DY","Had"),

    }

inclusive_samples = {
    "nMuon":("./Root_Files/Muon_Data","OneMuon_","Data","Muon"),
    
    #Muon MC
     "mcMuonW1":("./Root_Files/Muon_WJets","OneMuon_","WJetsInc","Muon"),
     "mcMuonTtw":("./Root_Files/Muon_TTbar","OneMuon_","TTbar","Muon"),
     "mcMuonDY":("./Root_Files/Muon_DY","OneMuon_","DY","Muon"),

    "nDiMuon":("./Root_Files/Muon_Data","DiMuon_","Data","DiMuon"),
    
    #Muon MC
     "mcDiMuonW1":("./Root_Files/Muon_WJets","DiMuon_","WJetsInc","DiMuon"),
     "mcDiMuonTtw":("./Root_Files/Muon_TTbar","DiMuon_","TTbar","DiMuon"),
     "mcDiMuonDY":("./Root_Files/Muon_DY","DiMuon_","DY","DiMuon"),

    "nHad":("./Root_Files/Had_Data","","Data","Had"),
    
    #Muon MC
     "mcHadW1":("./Root_Files/Had_WJets","","WJetsInc","Had"),
     "mcHadTtw":("./Root_Files/Had_TTbar","","TTbar","Had"),
     "mcHadDY":("./Root_Files/Had_DY","","DY","Had"),

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
  a = Number_Extractor(settings,btag_two_samples,"Two_btags",Triggers = "False",AlphaT="False")
  b = Number_Extractor(settings,btag_one_samples,"One_btag",Triggers = "False",AlphaT="False")
  c = Number_Extractor(settings,btag_zero_samples,"Zero_btags",Triggers = "False",AlphaT="False")
  d = Number_Extractor(settings,btag_morethan_zero_samples,"More_Than_Zero_btags",Triggers = "False",AlphaT="False")
  e = Number_Extractor(settings,btag_morethan_one_samples,"More_Than_One_btags",Triggers = "False",AlphaT="False")
  f = Number_Extractor(settings,btag_morethan_two_samples,"More_Than_Two_btags",Triggers = "False",AlphaT="False")
  g = Number_Extractor(settings,inclusive_samples,"Inclusive",Triggers = "False",AlphaT="False")
