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
  "AlphaTSlices":["0.52_0.53","0.53_0.54","0.55_10"]
      }

samples = {
    #"nHad":("./Root_Files/Had_Data","","Data","Had"),
    #"nSingleMu":("./Root_Files/Muon_Data","OneMuon_","Data","Muon"),
    #"nDiMu":("./Root_Files/Muon_Data,"DiMuon_","Data","DiMuon"),
    
    #Had MC
    # "mcHadW1":("./Root_Files/Had_WJetsInc","","WJetsInc","Had"),
    # "mcHadW2":("./Root_Files/Had_WJets250","","WJets250","Had"),
    # "mcHadW3":("./Root_Files/Had_WJets300","","WJets300","Had"),
    # "mcHadTtw":("./Root_Files/Had_TTbar","","TTbar","Had"),
    # "mcHadZ1":("./Root_Files/Had_Zinv50","","Zinv50","Had"),
    # "mcHadZ2":("./Root_Files/Had_Zinv100","","Zinv100","Had"),
    # "mcHadZ3":("./Root_Files/Had_Zinv200","","Zinv200","Had"),
    # "mcHadDY":("./Root_Files/Had_DY","","Zmumu","Had"),

    #Muon MC
    # "mcMuonW1":("./Root_Files/Muon_WJetsInc","OneMuon_","WJetsInc","Muon"),
    # "mcMuonW2":("./Root_Files/Muon_WJets250","OneMuon_","WJets250","Muon"),
    # "mcMuonW3":("./Root_Files/Muon_WJets300","OneMuon_","WJets300","Muon"),
    # "mcMuonTtw":("./Root_Files/Muon_TTbar","OneMuon_","TTbar","Muon"),
    # "mcMuonDY":("./Root_Files/Muon_DY","OneMuon","Zmumu","Muon"),

    
    #DiMuon MC
    # "mcDiMuonW1":("./Root_Files/Muon_WJetsInc","DiMuon_","WJetsInc","DiMuon"),
    # "mcDiMuonW2":("./Root_Files/Muon_WJets250","DiMuon_","WJets250","DiMuon"),
    # "mcDiMuonW3":("./Root_Files/Muon_WJets300","DiMuon_","WJets300","DiMuon"),
    # "mcDiMuonTtw":("./Root_Files/Muon_TTbar","DiMuon_","TTbar","DiMuon"),
    # "mcDiMuonZ1":("./Root_Files/Muon_Zinv50","DiMuon_","Zinv50","DiMuon"),
    # "mcDiMuonZ2":("./Root_Files/Muon_Zinv100","DiMuon_","Zinv100","DiMuon"),
    # "mcDiMuonZ3":("./Root_Files/Muon_Zinv200","DiMuon_","Zinv200","DiMuon"),
    # "mcDiMuonDY":("./Root_Files/Muon_DY","DiMuon_","Zmumu","DiMuon"),
    }

btag_samples = {

    "nHad_btag":("./Root_Files/Had_Data","btag_","Data","Had"),
    #"nSingleMu_btag":("./Root_Files/Muon_Data","btag_OneMuon_","Data","Muon"),
    #"nDiMu_btag":("./Root_Files/Muon_Data,"btag_DiMuon_","Data","DiMuon"),

    #Had MC
    # "mcHadW1_btag":("./Root_Files/Had_WJetsInc","btag_","WJetsInc","Had"),
    # "mcHadW2_btag":("./Root_Files/Had_WJets250","btag_","WJets250","Had"),
    # "mcHadW3_btag":("./Root_Files/Had_WJets300","btag_","WJets300","Had"),
    # "mcHadTtw_btag":("./Root_Files/Had_TTbar","btag_","TTbar","Had"),
    # "mcHadZ1_btag":("./Root_Files/Had_Zinv50","btag_","Zinv50","Had"),
    # "mcHadZ2_btag":("./Root_Files/Had_Zinv100","btag_","Zinv100","Had"),
    # "mcHadZ3_btag":("./Root_Files/Had_Zinv200","btag_","Zinv200","Had"),
    # "mcHadDY_btag":("./Root_Files/Had_DY","btag_","Zmumu","Had"),

    #Muon MC
    # "mcMuonW1_btag":("./Root_Files/Muon_WJetsInc","btag_OneMuon_","WJetsInc","Muon"),
    # "mcMuonW2_btag":("./Root_Files/Muon_WJets250","btag_OneMuon_","WJets250","Muon"),
    # "mcMuonW3_btag":("./Root_Files/Muon_WJets300","btag_OneMuon_","WJets300","Muon"),
    # "mcMuonTtw_btag":("./Root_Files/Muon_TTbar","btag_OneMuon_","TTbar","Muon"),
    # "mcMuonDY_btag":("./Root_Files/Muon_DY","btag_OneMuon","Zmumu","Muon"),

    
    #DiMuon MC
    # "mcDiMuonW1_btag":("./Root_Files/Muon_WJetsInc","btag_DiMuon_","WJetsInc","DiMuon"),
    # "mcDiMuonW2_btag":("./Root_Files/Muon_WJets250","btag_DiMuon_","WJets250","DiMuon"),
    # "mcDiMuonW3_btag":("./Root_Files/Muon_WJets300","btag_DiMuon_","WJets300","DiMuon"),
    # "mcDiMuonTtw_btag":("./Root_Files/Muon_TTbar","btag_DiMuon_","TTbar","DiMuon"),
    # "mcDiMuonZ1_btag":("./Root_Files/Muon_Zinv50","btag_DiMuon_","Zinv50","DiMuon"),
    # "mcDiMuonZ2_btag":("./Root_Files/Muon_Zinv100","btag_DiMuon_","Zinv100","DiMuon"),
    # "mcDiMuonZ3_btag":("./Root_Files/Muon_Zinv200","btag_DiMuon_","Zinv200","DiMuon"),
    # "mcDiMuonDY_btag":("./Root_Files/Muon_DY","btag_DiMuon_","Zmumu","DiMuon"),
    
    
    }                    

if __name__=="__main__":
  a = Number_Extractor(settings,samples)
