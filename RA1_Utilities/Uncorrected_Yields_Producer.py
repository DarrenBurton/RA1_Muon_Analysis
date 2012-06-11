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
  "Lumo":1.533, # Luminosity in fb
  "Multi_Lumi":{'Had':1.566,'Muon':1.561,'DiMuon':1.561}
  #"AlphaTSlices":["0.55_10"]
      }


'''
Sample Dictionary Instructions

eg "nMuon":("./May_11_root_Files/Muon_Data","btag_two_OneMuon_","Data","Muon"),
if n at start of name entry then the file is data and will no be scaled to luminosity.
first argument is path to root file
second argument is prefix to ht bin. i.e OneMuon_275_325
third argument is data/mc type, i.e. Data, WJets250 - MC relating to the binned WJets 250-300 HT sample
fourth argument is sample Type, Had/DiMuon/Muon. 

the only thing that will have to be changed is the second argument depending on wether you are running btag multiplicity/baseline
'''
btag_two_samples = {

    "nHad":("../29_May_8TeV_xSec/Had_Data","btag_two_","Data","Had"),
    
     "mcHadW1":("../29_May_8TeV_xSec/Had_WJets","btag_two_","WJetsInc","Had"),
     "mcHadttbar":("../29_May_8TeV_xSec/Had_TTbar","btag_two_","TTbar","Had"),
     "mcHadzinv":("../29_May_8TeV_xSec/Had_Zinv","btag_two_","Zinv50","Had"),
     "mcHadsingt":("../29_May_8TeV_xSec/Had_SingleTop","btag_two_","Single_Tbar_t","Had"),
     "mcHaddiboson":("../29_May_8TeV_xSec/Had_DiBoson","btag_two_","ZZ","Had"),
     "mcHadDY":("../29_May_8TeV_xSec/Had_DY","btag_two_","DY","Had"),

    "nMuon":("../29_May_8TeV_xSec/Muon_Data","btag_two_OneMuon_","Data","Muon"),
    
     "mcMuonW1":("../29_May_8TeV_xSec/Muon_WJets","btag_two_OneMuon_","WJetsInc","Muon"),
     "mcMuonttbar":("../29_May_8TeV_xSec/Muon_TTbar","btag_two_OneMuon_","TTbar","Muon"),
     "mcMuonzinv":("../29_May_8TeV_xSec/Muon_Zinv","btag_two_OneMuon_","Zinv50","Muon"),
     "mcMuonsingt":("../29_May_8TeV_xSec/Muon_SingleTop","btag_two_OneMuon_","Single_Tbar_t","Muon"),
     "mcMuondiboson":("../29_May_8TeV_xSec/Muon_DiBoson","btag_two_OneMuon_","ZZ","Muon"),
     "mcMuonDY":("../29_May_8TeV_xSec/Muon_DY","btag_two_OneMuon_","DY","Muon"),


    "nDiMuon":("../29_May_8TeV_xSec/Muon_Data","btag_two_DiMuon_","Data","DiMuon"),
    
     "mcDiMuonW1":("../29_May_8TeV_xSec/Muon_WJets","btag_two_DiMuon_","WJetsInc","DiMuon"),
     "mcDiMuonttbar":("../29_May_8TeV_xSec/Muon_TTbar","btag_two_DiMuon_","TTbar","DiMuon"),
     "mcDiMuonzinv":("../29_May_8TeV_xSec/Muon_Zinv","btag_two_DiMuon_","Zinv50","DiMuon"),
     "mcDiMuonsingt":("../29_May_8TeV_xSec/Muon_SingleTop","btag_two_DiMuon_","Single_Tbar_t","DiMuon"),
     "mcDiMuondiboson":("../29_May_8TeV_xSec/Muon_DiBoson","btag_two_DiMuon_","ZZ","DiMuon"),
     "mcDiMuonDY":("../29_May_8TeV_xSec/Muon_DY","btag_two_DiMuon_","DY","DiMuon"),


    }


btag_one_samples = {

    "nHad":("../29_May_8TeV_xSec/Had_Data","btag_one_","Data","Had"),
    
     "mcHadW1":("../29_May_8TeV_xSec/Had_WJets","btag_one_","WJetsInc","Had"),
     "mcHadttbar":("../29_May_8TeV_xSec/Had_TTbar","btag_one_","TTbar","Had"),
     "mcHadzinv":("../29_May_8TeV_xSec/Had_Zinv","btag_one_","Zinv50","Had"),
     "mcHadsingt":("../29_May_8TeV_xSec/Had_SingleTop","btag_one_","Single_Tbar_t","Had"),
     "mcHaddiboson":("../29_May_8TeV_xSec/Had_DiBoson","btag_one_","ZZ","Had"),
     "mcHadDY":("../29_May_8TeV_xSec/Had_DY","btag_one_","DY","Had"),


    "nMuon":("../29_May_8TeV_xSec/Muon_Data","btag_one_OneMuon_","Data","Muon"),
    
     "mcMuonW1":("../29_May_8TeV_xSec/Muon_WJets","btag_one_OneMuon_","WJetsInc","Muon"),
     "mcMuonttbar":("../29_May_8TeV_xSec/Muon_TTbar","btag_one_OneMuon_","TTbar","Muon"),
     "mcMuonzinv":("../29_May_8TeV_xSec/Muon_Zinv","btag_one_OneMuon_","Zinv50","Muon"),
     "mcMuonsingt":("../29_May_8TeV_xSec/Muon_SingleTop","btag_one_OneMuon_","Single_Tbar_t","Muon"),
     "mcMuondiboson":("../29_May_8TeV_xSec/Muon_DiBoson","btag_one_OneMuon_","ZZ","Muon"),
     "mcMuonDY":("../29_May_8TeV_xSec/Muon_DY","btag_one_OneMuon_","DY","Muon"),


    "nDiMuon":("../29_May_8TeV_xSec/Muon_Data","btag_one_DiMuon_","Data","DiMuon"),
    
     "mcDiMuonW1":("../29_May_8TeV_xSec/Muon_WJets","btag_one_DiMuon_","WJetsInc","DiMuon"),
     "mcDiMuonttbar":("../29_May_8TeV_xSec/Muon_TTbar","btag_one_DiMuon_","TTbar","DiMuon"),
     "mcDiMuonzinv":("../29_May_8TeV_xSec/Muon_Zinv","btag_one_DiMuon_","Zinv50","DiMuon"),
     "mcDiMuonsingt":("../29_May_8TeV_xSec/Muon_SingleTop","btag_one_DiMuon_","Single_Tbar_t","DiMuon"),
     "mcDiMuondiboson":("../29_May_8TeV_xSec/Muon_DiBoson","btag_one_DiMuon_","ZZ","DiMuon"),
     "mcDiMuonDY":("../29_May_8TeV_xSec/Muon_DY","btag_one_DiMuon_","DY","DiMuon"),


    }



btag_zero_samples = {

    "nHad":("../29_May_8TeV_xSec/Had_Data","btag_zero_","Data","Had"),
    
     "mcHadW1":("../29_May_8TeV_xSec/Had_WJets","btag_zero_","WJetsInc","Had"),
     "mcHadttbar":("../29_May_8TeV_xSec/Had_TTbar","btag_zero_","TTbar","Had"),
     "mcHadzinv":("../29_May_8TeV_xSec/Had_Zinv","btag_zero_","Zinv50","Had"),
     "mcHadsingt":("../29_May_8TeV_xSec/Had_SingleTop","btag_zero_","Single_Tbar_t","Had"),
     "mcHaddiboson":("../29_May_8TeV_xSec/Had_DiBoson","btag_zero_","ZZ","Had"),
     "mcHadDY":("../29_May_8TeV_xSec/Had_DY","btag_zero_","DY","Had"),


    "nMuon":("../29_May_8TeV_xSec/Muon_Data","btag_zero_OneMuon_","Data","Muon"),
    
     "mcMuonW1":("../29_May_8TeV_xSec/Muon_WJets","btag_zero_OneMuon_","WJetsInc","Muon"),
     "mcMuonttbar":("../29_May_8TeV_xSec/Muon_TTbar","btag_zero_OneMuon_","TTbar","Muon"),
     "mcMuonzinv":("../29_May_8TeV_xSec/Muon_Zinv","btag_zero_OneMuon_","Zinv50","Muon"),
     "mcMuonsingt":("../29_May_8TeV_xSec/Muon_SingleTop","btag_zero_OneMuon_","Single_Tbar_t","Muon"),
     "mcMuondiboson":("../29_May_8TeV_xSec/Muon_DiBoson","btag_zero_OneMuon_","ZZ","Muon"),
     "mcMuonDY":("../29_May_8TeV_xSec/Muon_DY","btag_zero_OneMuon_","DY","Muon"),


    "nDiMuon":("../29_May_8TeV_xSec/Muon_Data","btag_zero_DiMuon_","Data","DiMuon"),
    
     "mcDiMuonW1":("../29_May_8TeV_xSec/Muon_WJets","btag_zero_DiMuon_","WJetsInc","DiMuon"),
     "mcDiMuonttbar":("../29_May_8TeV_xSec/Muon_TTbar","btag_zero_DiMuon_","TTbar","DiMuon"),
     "mcDiMuonzinv":("../29_May_8TeV_xSec/Muon_Zinv","btag_zero_DiMuon_","Zinv50","DiMuon"),
     "mcDiMuonsingt":("../29_May_8TeV_xSec/Muon_SingleTop","btag_zero_DiMuon_","Single_Tbar_t","DiMuon"),
     "mcDiMuondiboson":("../29_May_8TeV_xSec/Muon_DiBoson","btag_zero_DiMuon_","ZZ","DiMuon"),
     "mcDiMuonDY":("../29_May_8TeV_xSec/Muon_DY","btag_zero_DiMuon_","DY","DiMuon"),


    }


btag_more_than_two_samples = {

    "nHad":("../29_May_8TeV_xSec/Had_Data","btag_morethantwo_","Data","Had"),
    
     "mcHadW1":("../29_May_8TeV_xSec/Had_WJets","btag_morethantwo_","WJetsInc","Had"),
     "mcHadttbar":("../29_May_8TeV_xSec/Had_TTbar","btag_morethantwo_","TTbar","Had"),
     "mcHadzinv":("../29_May_8TeV_xSec/Had_Zinv","btag_morethantwo_","Zinv50","Had"),
     "mcHadsingt":("../29_May_8TeV_xSec/Had_SingleTop","btag_morethantwo_","Single_Tbar_t","Had"),
     "mcHaddiboson":("../29_May_8TeV_xSec/Had_DiBoson","btag_morethantwo_","ZZ","Had"),
     "mcHadDY":("../29_May_8TeV_xSec/Had_DY","btag_morethantwo_","DY","Had"),


    "nMuon":("../29_May_8TeV_xSec/Muon_Data","btag_morethantwo_OneMuon_","Data","Muon"),
    
     "mcMuonW1":("../29_May_8TeV_xSec/Muon_WJets","btag_morethantwo_OneMuon_","WJetsInc","Muon"),
     "mcMuonttbar":("../29_May_8TeV_xSec/Muon_TTbar","btag_morethantwo_OneMuon_","TTbar","Muon"),
     "mcMuonzinv":("../29_May_8TeV_xSec/Muon_Zinv","btag_morethantwo_OneMuon_","Zinv50","Muon"),
     "mcMuonsingt":("../29_May_8TeV_xSec/Muon_SingleTop","btag_morethantwo_OneMuon_","Single_Tbar_t","Muon"),
     "mcMuondiboson":("../29_May_8TeV_xSec/Muon_DiBoson","btag_morethantwo_OneMuon_","ZZ","Muon"),
     "mcMuonDY":("../29_May_8TeV_xSec/Muon_DY","btag_morethantwo_OneMuon_","DY","Muon"),


    "nDiMuon":("../29_May_8TeV_xSec/Muon_Data","btag_morethantwo_DiMuon_","Data","DiMuon"),
    
     "mcDiMuonW1":("../29_May_8TeV_xSec/Muon_WJets","btag_morethantwo_DiMuon_","WJetsInc","DiMuon"),
     "mcDiMuonttbar":("../29_May_8TeV_xSec/Muon_TTbar","btag_morethantwo_DiMuon_","TTbar","DiMuon"),
     "mcDiMuonzinv":("../29_May_8TeV_xSec/Muon_Zinv","btag_morethantwo_DiMuon_","Zinv50","DiMuon"),
     "mcDiMuonsingt":("../29_May_8TeV_xSec/Muon_SingleTop","btag_morethantwo_DiMuon_","Single_Tbar_t","DiMuon"),
     "mcDiMuondiboson":("../29_May_8TeV_xSec/Muon_DiBoson","btag_morethantwo_DiMuon_","ZZ","DiMuon"),
     "mcDiMuonDY":("../29_May_8TeV_xSec/Muon_DY","btag_morethantwo_DiMuon_","DY","DiMuon"),


    }


btag_more_than_zero_samples = {

    "nHad":("../29_May_8TeV_xSec/Had_Data","btag_morethanzero_","Data","Had"),
    
     "mcHadW1":("../29_May_8TeV_xSec/Had_WJets","btag_morethanzero_","WJetsInc","Had"),
     "mcHadttbar":("../29_May_8TeV_xSec/Had_TTbar","btag_morethanzero_","TTbar","Had"),
     "mcHadzinv":("../29_May_8TeV_xSec/Had_Zinv","btag_morethanzero_","Zinv50","Had"),
     "mcHadsingt":("../29_May_8TeV_xSec/Had_SingleTop","btag_morethanzero_","Single_Tbar_t","Had"),
     "mcHaddiboson":("../29_May_8TeV_xSec/Had_DiBoson","btag_morethanzero_","ZZ","Had"),
     "mcHadDY":("../29_May_8TeV_xSec/Had_DY","btag_morethanzero_","DY","Had"),


    "nMuon":("../29_May_8TeV_xSec/Muon_Data","btag_morethanzero_OneMuon_","Data","Muon"),
    
     "mcMuonW1":("../29_May_8TeV_xSec/Muon_WJets","btag_morethanzero_OneMuon_","WJetsInc","Muon"),
     "mcMuonttbar":("../29_May_8TeV_xSec/Muon_TTbar","btag_morethanzero_OneMuon_","TTbar","Muon"),
     "mcMuonzinv":("../29_May_8TeV_xSec/Muon_Zinv","btag_morethanzero_OneMuon_","Zinv50","Muon"),
     "mcMuonsingt":("../29_May_8TeV_xSec/Muon_SingleTop","btag_morethanzero_OneMuon_","Single_Tbar_t","Muon"),
     "mcMuondiboson":("../29_May_8TeV_xSec/Muon_DiBoson","btag_morethanzero_OneMuon_","ZZ","Muon"),
     "mcMuonDY":("../29_May_8TeV_xSec/Muon_DY","btag_morethanzero_OneMuon_","DY","Muon"),


    "nDiMuon":("../29_May_8TeV_xSec/Muon_Data","btag_morethanzero_DiMuon_","Data","DiMuon"),
    
     "mcDiMuonW1":("../29_May_8TeV_xSec/Muon_WJets","btag_morethanzero_DiMuon_","WJetsInc","DiMuon"),
     "mcDiMuonttbar":("../29_May_8TeV_xSec/Muon_TTbar","btag_morethanzero_DiMuon_","TTbar","DiMuon"),
     "mcDiMuonzinv":("../29_May_8TeV_xSec/Muon_Zinv","btag_morethanzero_DiMuon_","Zinv50","DiMuon"),
     "mcDiMuonsingt":("../29_May_8TeV_xSec/Muon_SingleTop","btag_morethanzero_DiMuon_","Single_Tbar_t","DiMuon"),
     "mcDiMuondiboson":("../29_May_8TeV_xSec/Muon_DiBoson","btag_morethanzero_DiMuon_","ZZ","DiMuon"),
     "mcDiMuonDY":("../29_May_8TeV_xSec/Muon_DY","btag_morethanzero_DiMuon_","DY","DiMuon"),


    }


btag_more_than_one_samples = {

    "nHad":("../29_May_8TeV_xSec/Had_Data","btag_morethanone_","Data","Had"),
    
     "mcHadW1":("../29_May_8TeV_xSec/Had_WJets","btag_morethanone_","WJetsInc","Had"),
     "mcHadttbar":("../29_May_8TeV_xSec/Had_TTbar","btag_morethanone_","TTbar","Had"),
     "mcHadzinv":("../29_May_8TeV_xSec/Had_Zinv","btag_morethanone_","Zinv50","Had"),
     "mcHadsingt":("../29_May_8TeV_xSec/Had_SingleTop","btag_morethanone_","Single_Tbar_t","Had"),
     "mcHaddiboson":("../29_May_8TeV_xSec/Had_DiBoson","btag_morethanone_","ZZ","Had"),
     "mcHadDY":("../29_May_8TeV_xSec/Had_DY","btag_morethanone_","DY","Had"),


    "nMuon":("../29_May_8TeV_xSec/Muon_Data","btag_morethanone_OneMuon_","Data","Muon"),
    
     "mcMuonW1":("../29_May_8TeV_xSec/Muon_WJets","btag_morethanone_OneMuon_","WJetsInc","Muon"),
     "mcMuonttbar":("../29_May_8TeV_xSec/Muon_TTbar","btag_morethanone_OneMuon_","TTbar","Muon"),
     "mcMuonzinv":("../29_May_8TeV_xSec/Muon_Zinv","btag_morethanone_OneMuon_","Zinv50","Muon"),
     "mcMuonsingt":("../29_May_8TeV_xSec/Muon_SingleTop","btag_morethanone_OneMuon_","Single_Tbar_t","Muon"),
     "mcMuondiboson":("../29_May_8TeV_xSec/Muon_DiBoson","btag_morethanone_OneMuon_","ZZ","Muon"),
     "mcMuonDY":("../29_May_8TeV_xSec/Muon_DY","btag_morethanone_OneMuon_","DY","Muon"),


    "nDiMuon":("../29_May_8TeV_xSec/Muon_Data","btag_morethanone_DiMuon_","Data","DiMuon"),
    
     "mcDiMuonW1":("../29_May_8TeV_xSec/Muon_WJets","btag_morethanone_DiMuon_","WJetsInc","DiMuon"),
     "mcDiMuonttbar":("../29_May_8TeV_xSec/Muon_TTbar","btag_morethanone_DiMuon_","TTbar","DiMuon"),
     "mcDiMuonzinv":("../29_May_8TeV_xSec/Muon_Zinv","btag_morethanone_DiMuon_","Zinv50","DiMuon"),
     "mcDiMuonsingt":("../29_May_8TeV_xSec/Muon_SingleTop","btag_morethanone_DiMuon_","Single_Tbar_t","DiMuon"),
     "mcDiMuondiboson":("../29_May_8TeV_xSec/Muon_DiBoson","btag_morethanone_DiMuon_","ZZ","DiMuon"),
     "mcDiMuonDY":("../29_May_8TeV_xSec/Muon_DY","btag_morethanone_DiMuon_","DY","DiMuon"),


    }




inclusive_samples = {

    "nHad":("../29_May_8TeV_xSec/Had_Data","","Data","Had"),
    
     "mcHadW1":("../29_May_8TeV_xSec/Had_WJets","","WJetsInc","Had"),
     "mcHadttbar":("../29_May_8TeV_xSec/Had_TTbar","","TTbar","Had"),
     "mcHadzinv":("../29_May_8TeV_xSec/Had_Zinv","","Zinv50","Had"),
     "mcHadsingt":("../29_May_8TeV_xSec/Had_SingleTop","","Single_Tbar_t","Had"),
     "mcHaddiboson":("../29_May_8TeV_xSec/Had_DiBoson","","ZZ","Had"),
     "mcHadDY":("../29_May_8TeV_xSec/Had_DY","","DY","Had"),


    "nMuon":("../29_May_8TeV_xSec/Muon_Data","OneMuon_","Data","Muon"),
    
     "mcMuonW1":("../29_May_8TeV_xSec/Muon_WJets","OneMuon_","WJetsInc","Muon"),
     "mcMuonttbar":("../29_May_8TeV_xSec/Muon_TTbar","OneMuon_","TTbar","Muon"),
     "mcMuonzinv":("../29_May_8TeV_xSec/Muon_Zinv","OneMuon_","Zinv50","Muon"),
     "mcMuonsingt":("../29_May_8TeV_xSec/Muon_SingleTop","OneMuon_","Single_Tbar_t","Muon"),
     "mcMuondiboson":("../29_May_8TeV_xSec/Muon_DiBoson","OneMuon_","ZZ","Muon"),
     "mcMuonDY":("../29_May_8TeV_xSec/Muon_DY","OneMuon_","DY","Muon"),


    "nDiMuon":("../29_May_8TeV_xSec/Muon_Data","DiMuon_","Data","DiMuon"),
    
     "mcDiMuonW1":("../29_May_8TeV_xSec/Muon_WJets","DiMuon_","WJetsInc","DiMuon"),
     "mcDiMuonttbar":("../29_May_8TeV_xSec/Muon_TTbar","DiMuon_","TTbar","DiMuon"),
     "mcDiMuonzinv":("../29_May_8TeV_xSec/Muon_Zinv","DiMuon_","Zinv50","DiMuon"),
     "mcDiMuonsingt":("../29_May_8TeV_xSec/Muon_SingleTop","DiMuon_","Single_Tbar_t","DiMuon"),
     "mcDiMuondiboson":("../29_May_8TeV_xSec/Muon_DiBoson","DiMuon_","ZZ","DiMuon"),
     "mcDiMuonDY":("../29_May_8TeV_xSec/Muon_DY","DiMuon_","DY","DiMuon"),


    }


calc_file = {
     "mchad":("../29_May_8TeV_xSec/Had_MC.root","Had",""),
     "mchadzinv":("../29_May_8TeV_xSec/Had_Zinv.root","Had_Zinv",""),
     "mcmuon":("../29_May_8TeV_xSec/Muon_MC.root","Muon","OneMuon_"),
     "mcdimuon":("../29_May_8TeV_xSec/Muon_MC.root","DiMuon","DiMuon_"),

}


#calc_file = {
#     "mchad":("./May_11_root_Files/Had_MC.root","Had",""),
#     "mcmuon":("./May_11_root_Files/Muon_MC.root","Muon","OneMuon_"),
#     "mcdimuon":("./May_11_root_Files/Muon_MC.root","DiMuon","DiMuon_"),
#
#}

if __name__=="__main__":
  #a = Number_Extractor(settings,btag_two_samples,"Two_btags",Triggers = "True",AlphaT="False")
  #b = Number_Extractor(settings,btag_one_samples,"One_btag",Triggers = "True",AlphaT="False")
  #c = Number_Extractor(settings,btag_zero_samples,"Zero_btags",Triggers = "True",AlphaT="False")
  #d = Number_Extractor(settings,btag_more_than_two_samples,"More_Than_Two_btag",Triggers = "True",AlphaT="False")
  #t = Number_Extractor(settings,btag_zero_samples,"Zero_btags",Triggers = "True",AlphaT="False")
  #e  = Number_Extractor(settings,btag_more_than_zero_samples,"More_Than_Zero_btag",Triggers = "True",AlphaT="False")
  #f  = Number_Extractor(settings,btag_more_than_one_samples,"More_Than_One_btag",Triggers = "True",AlphaT="False")
  g  = Number_Extractor(settings,inclusive_samples,"Inclusive",Triggers = "True",AlphaT="False",Split_Lumi = "True")
  #g  = Number_Extractor(settings,inclusive_samples,"Inclusive",Triggers = "True",AlphaT="False",Split_Lumi = "False")
