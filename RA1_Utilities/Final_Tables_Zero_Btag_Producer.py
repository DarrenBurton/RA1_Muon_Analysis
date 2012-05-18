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
  "AlphaTSlices":["0.52_0.53","0.53_0.55","0.55_10"]
  #"AlphaTSlices":["0.55_10"]
      }

samples = {
    "nMuon":("./Root_Files/Muon_Data","btag_zero_OneMuon_","Data","Muon"),
    
    #Muon MC
     "mcMuonW1":("./Root_Files/Muon_WJetsInc","btag_zero_OneMuon_","WJetsInc","Muon"),
     "mcMuonW2":("./Root_Files/Muon_WJets250","btag_zero_OneMuon_","WJets250","Muon"),
     "mcMuonW3":("./Root_Files/Muon_WJets300","btag_zero_OneMuon_","WJets300","Muon"),
     "mcMuonTtw":("./Root_Files/Muon_TTbar","btag_zero_OneMuon_","TTbar","Muon"),
     "mcMuonDY":("./Root_Files/Muon_DY","btag_zero_OneMuon_","DY","Muon"),
     "mcMuon_Singt":("./Root_Files/Muon_Single_T_t","btag_zero_OneMuon_","Single_T_t","Muon"),
     "mcMuon_SingtW":("./Root_Files/Muon_Single_T_tW","btag_zero_OneMuon_","Single_T_tW","Muon"),
     "mcMuon_Singtbar_t":("./Root_Files/Muon_Single_Tbar_t","btag_zero_OneMuon_","Single_Tbar_t","Muon"),
     "mcMuon_Singtbar_tw":("./Root_Files/Muon_Single_Tbar_tW","btag_zero_OneMuon_","Single_Tbar_tW","Muon"),
     "mcMuonZZ":("./Root_Files/Muon_ZZ","btag_zero_OneMuon_","ZZ","Muon"),
     "mcMuonWW":("./Root_Files/Muon_WW","btag_zero_OneMuon_","WW","Muon"),
     "mcMuonWZ":("./Root_Files/Muon_WZ","btag_zero_OneMuon_","WZ","Muon"),

    "nDiMuon":("./Root_Files/Muon_Data","btag_zero_DiMuon_","Data","DiMuon"),
    
    #Muon MC
     "mcDiMuonW1":("./Root_Files/Muon_WJetsInc","btag_zero_DiMuon_","WJetsInc","DiMuon"),
     "mcDiMuonW2":("./Root_Files/Muon_WJets250","btag_zero_DiMuon_","WJets250","DiMuon"),
     "mcDiMuonW3":("./Root_Files/Muon_WJets300","btag_zero_DiMuon_","WJets300","DiMuon"),
     "mcDiMuonTtw":("./Root_Files/Muon_TTbar","btag_zero_DiMuon_","TTbar","DiMuon"),
     "mcDiMuonDY":("./Root_Files/Muon_DY","btag_zero_DiMuon_","DY","DiMuon"),
     "mcDiMuon_Singt":("./Root_Files/Muon_Single_T_t","btag_zero_DiMuon_","Single_T_t","DiMuon"),
     "mcDiMuon_SingtW":("./Root_Files/Muon_Single_T_tW","btag_zero_DiMuon_","Single_T_tW","DiMuon"),
     "mcDiMuon_Singtbar_t":("./Root_Files/Muon_Single_Tbar_t","btag_zero_DiMuon_","Single_Tbar_t","DiMuon"),
     "mcDiMuon_Singtbar_tw":("./Root_Files/Muon_Single_Tbar_tW","btag_zero_DiMuon_","Single_Tbar_tW","DiMuon"),
     "mcDiMuonZZ":("./Root_Files/Muon_ZZ","btag_zero_DiMuon_","ZZ","DiMuon"),
     "mcDiMuonWW":("./Root_Files/Muon_WW","btag_zero_DiMuon_","WW","DiMuon"),
     "mcMuonWZ":("./Root_Files/Muon_WZ","btag_zero_DiMuon_","WZ","DiMuon"),

    "nHad":("./Root_Files/Had_Data","btag_zero_","Data","Had"),
    
    #Muon MC
     "mcHadW1":("./Root_Files/Had_WJetsInc","btag_zero_","WJetsInc","Had"),
     "mcHadW2":("./Root_Files/Had_WJets250","btag_zero_","WJets250","Had"),
     "mcHadW3":("./Root_Files/Had_WJets300","btag_zero_","WJets300","Had"),
     "mcHadTtw":("./Root_Files/Had_TTbar","btag_zero_","TTbar","Had"),
     "mcHadZ1":("./Root_Files/Had_Zinv50","btag_zero_","Zinv50","Had"),
     "mcHadZ2":("./Root_Files/Had_Zinv100","btag_zero_","Zinv100","Had"),
     "mcHadZ3":("./Root_Files/Had_Zinv200","btag_zero_","Zinv200","Had"),
     "mcHadDY":("./Root_Files/Had_DY","btag_zero_","DY","Had"),
     "mcHad_Singt":("./Root_Files/Had_Single_T_t","btag_zero_","Single_T_t","Had"),
     "mcHad_SingtW":("./Root_Files/Had_Single_T_tW","btag_zero_","Single_T_tW","Had"),
     "mcHad_Singtbar_t":("./Root_Files/Had_Single_Tbar_t","btag_zero_","Single_Tbar_t","Had"),
     "mcHad_Singtbar_tw":("./Root_Files/Had_Single_Tbar_tW","btag_zero_","Single_Tbar_tW","Had"),
     "mcHadZZ":("./Root_Files/Had_ZZ","btag_zero_","ZZ","Had"),
     "mcHadWW":("./Root_Files/Had_WW","btag_zero_","WW","Had"),
     "mcHadWZ":("./Root_Files/Had_WZ","btag_zero_","WZ","Had"),



    }


if __name__=="__main__":
  a = Number_Extractor(settings,samples,"Mu_HT_Zero_Btags")
