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
from RA1_8TeV import *
from Jad_Compute import *



'''
Jads Closure Tests are used to show how we can relax the alphaT cut in the control samples
Therefore the AlphaTSlices are given as 0.55-10 and 0.01-10
'''

settings = {
  #"dirs":["275_325"],
  "dirs":["275_325","325_375","375_475","475_575","575_675","675_775","775_875","875",],
  "plots":["AlphaT_all",],
  "AlphaTSlices":["0.55_10","0.01_10"],
  "Lumo":0.194, 
  #"AlphaTSlices":["0.55_10"]
      }

samples = {
    "nMuon":("./Root_Files/Muon_Data","OneMuon_","Data","Muon"),
    
    #Muon MC
     "mcMuonW1":("./Root_Files/Muon_WJets","OneMuon_","WJetsInc","Muon"),
     "mcMuonTtw":("./Root_Files/Muon_TTbar","OneMuon_","TTbar","Muon"),
     "mcMuonDY":("./Root_Files/Muon_DY","OneMuon_","DY","Muon"),

    "nDimuon":("./Root_Files/Muon_Data","DiMuon_","Data","DiMuon"),
    
    #Muon MC
     "mcDimuonW1":("./Root_Files/Muon_WJets","DiMuon_","WJetsInc","DiMuon"),
     "mcDimuonTtw":("./Root_Files/Muon_TTbar","DiMuon_","TTbar","DiMuon"),
     "mcDimuonDY":("./Root_Files/Muon_DY","DiMuon_","DY","DiMuon"),

    }

btag_zero_samples = {

    "nMuon_btag":("./Root_Files/Muon_Data","btag_zero_OneMuon_","Data","Muon"),

    #Muon MC
     "mcMuonW1_btag":("./Root_Files/Muon_WJets","btag_zero_OneMuon_","WJetsInc","Muon"),
     "mcMuonTtw_btag":("./Root_Files/Muon_TTbar","btag_zero_OneMuon_","TTbar","Muon"),
     "mcMuonDY_btag":("./Root_Files/Muon_DY","btag_zero_OneMuon_","DY","Muon"),

    "nDimuon_btag":("./Root_Files/Muon_Data","btag_zero_DiMuon_","Data","DiMuon"),

    #Muon MC
     "mcDimuonW1_btag":("./Root_Files/Muon_WJets","btag_zero_DiMuon_","WJetsInc","DiMuon"),
     "mcDimuonTtw_btag":("./Root_Files/Muon_TTbar","btag_zero_DiMuon_","TTbar","DiMuon"),
     "mcDimuonDY_btag":("./Root_Files/Muon_DY","btag_zero_DiMuon_","DY","DiMuon"),

    }                    



btag_morethan_zero_samples = {

    "nMuon_btag":("./Root_Files/Muon_Data","btag_morethanzero_OneMuon_","Data","Muon"),

    #Muon MC
     "mcMuonW1_btag":("./Root_Files/Muon_WJets","btag_morethanzero_OneMuon_","WJetsInc","Muon"),
     "mcMuonTtw_btag":("./Root_Files/Muon_TTbar","btag_morethanzero_OneMuon_","TTbar","Muon"),
     "mcMuonDY_btag":("./Root_Files/Muon_DY","btag_morethanzero_OneMuon_","DY","Muon"),

    "nDimuon_btag":("./Root_Files/Muon_Data","btag_morethanzero_DiMuon_","Data","DiMuon"),

    #Muon MC
     "mcDimuonW1_btag":("./Root_Files/Muon_WJets","btag_morethanzero_DiMuon_","WJetsInc","DiMuon"),
     "mcDimuonTtw_btag":("./Root_Files/Muon_TTbar","btag_morethanzero_DiMuon_","TTbar","DiMuon"),
     "mcDimuonDY_btag":("./Root_Files/Muon_DY","btag_morethanzero_DiMuon_","DY","DiMuon"),

    }   
btag_one_samples = {

    "nMuon_btag":("./Root_Files/Muon_Data","btag_one_OneMuon_","Data","Muon"),

    #Muon MC
     "mcMuonW1_btag":("./Root_Files/Muon_WJets","btag_one_OneMuon_","WJetsInc","Muon"),
     "mcMuonTtw_btag":("./Root_Files/Muon_TTbar","btag_one_OneMuon_","TTbar","Muon"),
     "mcMuonDY_btag":("./Root_Files/Muon_DY","btag_one_OneMuon_","DY","Muon"),

    "nDimuon_btag":("./Root_Files/Muon_Data","btag_one_DiMuon_","Data","DiMuon"),

    #Muon MC
     "mcDimuonW1_btag":("./Root_Files/Muon_WJets","btag_one_DiMuon_","WJetsInc","DiMuon"),
     "mcDimuonTtw_btag":("./Root_Files/Muon_TTbar","btag_one_DiMuon_","TTbar","DiMuon"),
     "mcDimuonDY_btag":("./Root_Files/Muon_DY","btag_one_DiMuon_","DY","DiMuon"),

    }                    


btag_morethan_one_samples = {

    "nMuon_btag":("./Root_Files/Muon_Data","btag_morethanone_OneMuon_","Data","Muon"),

    #Muon MC
     "mcMuonW1_btag":("./Root_Files/Muon_WJets","btag_morethanone_OneMuon_","WJetsInc","Muon"),
     "mcMuonTtw_btag":("./Root_Files/Muon_TTbar","btag_morethanone_OneMuon_","TTbar","Muon"),
     "mcMuonDY_btag":("./Root_Files/Muon_DY","btag_morethanone_OneMuon_","DY","Muon"),

    "nDimuon_btag":("./Root_Files/Muon_Data","btag_morethanone_DiMuon_","Data","DiMuon"),

    #Muon MC
     "mcDimuonW1_btag":("./Root_Files/Muon_WJets","btag_morethanone_DiMuon_","WJetsInc","DiMuon"),
     "mcDimuonTtw_btag":("./Root_Files/Muon_TTbar","btag_morethanone_DiMuon_","TTbar","DiMuon"),
     "mcDimuonDY_btag":("./Root_Files/Muon_DY","btag_morethanone_DiMuon_","DY","DiMuon"),

    }   


btag_two_samples = {

    "nMuon_btag":("./Root_Files/Muon_Data","btag_two_OneMuon_","Data","Muon"),

    #Muon MC
     "mcMuonW1_btag":("./Root_Files/Muon_WJets","btag_two_OneMuon_","WJetsInc","Muon"),
     "mcMuonTtw_btag":("./Root_Files/Muon_TTbar","btag_two_OneMuon_","TTbar","Muon"),
     "mcMuonDY_btag":("./Root_Files/Muon_DY","btag_two_OneMuon_","DY","Muon"),

    "nDimuon_btag":("./Root_Files/Muon_Data","btag_two_DiMuon_","Data","DiMuon"),

    #Muon MC
     "mcDimuonW1_btag":("./Root_Files/Muon_WJets","btag_two_DiMuon_","WJetsInc","DiMuon"),
     "mcDimuonTtw_btag":("./Root_Files/Muon_TTbar","btag_two_DiMuon_","TTbar","DiMuon"),
     "mcDimuonDY_btag":("./Root_Files/Muon_DY","btag_two_DiMuon_","DY","DiMuon"),

    }                    


btag_morethan_two_samples = {

    "nMuon_btag":("./Root_Files/Muon_Data","btag_morethantwo_OneMuon_","Data","Muon"),

    #Muon MC
     "mcMuonW1_btag":("./Root_Files/Muon_WJets","btag_morethantwo_OneMuon_","WJetsInc","Muon"),
     "mcMuonTtw_btag":("./Root_Files/Muon_TTbar","btag_morethantwo_OneMuon_","TTbar","Muon"),
     "mcMuonDY_btag":("./Root_Files/Muon_DY","btag_morethantwo_OneMuon_","DY","Muon"),

    "nDimuon_btag":("./Root_Files/Muon_Data","btag_morethantwo_DiMuon_","Data","DiMuon"),

    #Muon MC
     "mcDimuonW1_btag":("./Root_Files/Muon_WJets","btag_morethantwo_DiMuon_","WJetsInc","DiMuon"),
     "mcDimuonTtw_btag":("./Root_Files/Muon_TTbar","btag_morethantwo_DiMuon_","TTbar","DiMuon"),
     "mcDimuonDY_btag":("./Root_Files/Muon_DY","btag_morethantwo_DiMuon_","DY","DiMuon"),

    }                    


'''
All Sample are passed through Number_Extractor and each of the relevant dictionaries are output to c_file.
Jad_Compute which is then called and closure test png's are produced.
3rd argument here is entered into dictionary to identify btag multiplicity. Dont change these strings

Addtional options
Classic - If true then produces 'classic baseline' closure tests. i.e. Photon -> dimuon, muon -> dimuon. Use with basline files only, no btags

Look in Jad_Compute.py for any further comments
'''


if __name__=="__main__":
  LIST_FOR_JAD = []
  a = Number_Extractor(settings,btag_zero_samples,"Zero_btags",c_file = LIST_FOR_JAD,Closure = "True",AlphaT="True",Triggers="False") 
  b = Number_Extractor(settings,btag_one_samples,"One_btag",c_file = LIST_FOR_JAD,Closure="True",AlphaT="True",Triggers="False")
  c = Number_Extractor(settings,btag_two_samples,"Two_btags",c_file = LIST_FOR_JAD,Closure="True",AlphaT="True",Triggers="False")
  d = Number_Extractor(settings,samples,"BaseLine",c_file = LIST_FOR_JAD,Closure="True",AlphaT="True",Triggers="False")
  e = Number_Extractor(settings,btag_morethan_one_samples,"More_Than_One_btag",c_file = LIST_FOR_JAD,Closure="True",AlphaT="True",Triggers="False")
  f = Number_Extractor(settings,btag_morethan_two_samples,"More_Than_Two_btag",c_file = LIST_FOR_JAD,Closure="True",AlphaT="True",Triggers="False")
  g = Number_Extractor(settings,btag_morethan_zero_samples,"More_Than_Zero_btag",c_file = LIST_FOR_JAD,Closure="True",AlphaT="True",Triggers="False")
  h = Jad_Compute(LIST_FOR_JAD,Lumo = settings["Lumo"])
