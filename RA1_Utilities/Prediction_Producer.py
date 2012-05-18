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
  "Lumo":0.55, # Luminosity in fb
  "Multi_Lumi":{'Had':0.55,'Muon':0.45,'DiMuon':0.5}
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

    "nHad":("./New_7TeV_MC_8TeV_xSec/Had_Data","btag_two_","Data","Had"),
    
     "mcHadW1":("./New_7TeV_MC_8TeV_xSec/Had_WJets","","WJetsInc","Had"),
     "mcHadttbar":("./New_7TeV_MC_8TeV_xSec/Had_TTbar","","TTbar","Had"),
     "mcHadzinv":("./New_7TeV_MC_8TeV_xSec/Had_Zinv","","Zinv50","Had"),
     "mcHadsingt":("./New_7TeV_MC_8TeV_xSec/Had_SingleTop","","Single_Tbar_t","Had"),
     "mcHaddiboson":("./New_7TeV_MC_8TeV_xSec/Had_DiBoson","","ZZ","Had"),
     "mcHadDY":("./New_7TeV_MC_8TeV_xSec/Had_DY","","DY","Had"),

    "nMuon":("./New_7TeV_MC_8TeV_xSec/Muon_Data","btag_two_OneMuon_","Data","Muon"),
    
     "mcMuonW1":("./New_7TeV_MC_8TeV_xSec/Muon_WJets","OneMuon_","WJetsInc","Muon"),
     "mcMuonttbar":("./New_7TeV_MC_8TeV_xSec/Muon_TTbar","OneMuon_","TTbar","Muon"),
     "mcMuonzinv":("./New_7TeV_MC_8TeV_xSec/Muon_Zinv","OneMuon_","Zinv50","Muon"),
     "mcMuonsingt":("./New_7TeV_MC_8TeV_xSec/Muon_SingleTop","OneMuon_","Single_Tbar_t","Muon"),
     "mcMuondiboson":("./New_7TeV_MC_8TeV_xSec/Muon_DiBoson","OneMuon_","ZZ","Muon"),
     "mcMuonDY":("./New_7TeV_MC_8TeV_xSec/Muon_DY","OneMuon_","DY","Muon"),


    "nDiMuon":("./New_7TeV_MC_8TeV_xSec/Muon_Data","btag_two_DiMuon_","Data","DiMuon"),
    
     "mcDiMuonW1":("./New_7TeV_MC_8TeV_xSec/Muon_WJets","DiMuon_","WJetsInc","DiMuon"),
     "mcDiMuonttbar":("./New_7TeV_MC_8TeV_xSec/Muon_TTbar","DiMuon_","TTbar","DiMuon"),
     "mcDiMuonzinv":("./New_7TeV_MC_8TeV_xSec/Muon_Zinv","DiMuon_","Zinv50","DiMuon"),
     "mcDiMuonsingt":("./New_7TeV_MC_8TeV_xSec/Muon_SingleTop","DiMuon_","Single_Tbar_t","DiMuon"),
     "mcDiMuondiboson":("./New_7TeV_MC_8TeV_xSec/Muon_DiBoson","DiMuon_","ZZ","DiMuon"),
     "mcDiMuonDY":("./New_7TeV_MC_8TeV_xSec/Muon_DY","DiMuon_","DY","DiMuon"),


    }


btag_one_samples = {

    "nHad":("./New_7TeV_MC_8TeV_xSec/Had_Data","btag_one_","Data","Had"),
    
     "mcHadW1":("./New_7TeV_MC_8TeV_xSec/Had_WJets","","WJetsInc","Had"),
     "mcHadttbar":("./New_7TeV_MC_8TeV_xSec/Had_TTbar","","TTbar","Had"),
     "mcHadzinv":("./New_7TeV_MC_8TeV_xSec/Had_Zinv","","Zinv50","Had"),
     "mcHadsingt":("./New_7TeV_MC_8TeV_xSec/Had_SingleTop","","Single_Tbar_t","Had"),
     "mcHaddiboson":("./New_7TeV_MC_8TeV_xSec/Had_DiBoson","","ZZ","Had"),
     "mcHadDY":("./New_7TeV_MC_8TeV_xSec/Had_DY","","DY","Had"),


    "nMuon":("./New_7TeV_MC_8TeV_xSec/Muon_Data","btag_one_OneMuon_","Data","Muon"),
    
     "mcMuonW1":("./New_7TeV_MC_8TeV_xSec/Muon_WJets","OneMuon_","WJetsInc","Muon"),
     "mcMuonttbar":("./New_7TeV_MC_8TeV_xSec/Muon_TTbar","OneMuon_","TTbar","Muon"),
     "mcMuonzinv":("./New_7TeV_MC_8TeV_xSec/Muon_Zinv","OneMuon_","Zinv50","Muon"),
     "mcMuonsingt":("./New_7TeV_MC_8TeV_xSec/Muon_SingleTop","OneMuon_","Single_Tbar_t","Muon"),
     "mcMuondiboson":("./New_7TeV_MC_8TeV_xSec/Muon_DiBoson","OneMuon_","ZZ","Muon"),
     "mcMuonDY":("./New_7TeV_MC_8TeV_xSec/Muon_DY","OneMuon_","DY","Muon"),


    "nDiMuon":("./New_7TeV_MC_8TeV_xSec/Muon_Data","btag_one_DiMuon_","Data","DiMuon"),
    
     "mcDiMuonW1":("./New_7TeV_MC_8TeV_xSec/Muon_WJets","DiMuon_","WJetsInc","DiMuon"),
     "mcDiMuonttbar":("./New_7TeV_MC_8TeV_xSec/Muon_TTbar","DiMuon_","TTbar","DiMuon"),
     "mcDiMuonzinv":("./New_7TeV_MC_8TeV_xSec/Muon_Zinv","DiMuon_","Zinv50","DiMuon"),
     "mcDiMuonsingt":("./New_7TeV_MC_8TeV_xSec/Muon_SingleTop","DiMuon_","Single_Tbar_t","DiMuon"),
     "mcDiMuondiboson":("./New_7TeV_MC_8TeV_xSec/Muon_DiBoson","DiMuon_","ZZ","DiMuon"),
     "mcDiMuonDY":("./New_7TeV_MC_8TeV_xSec/Muon_DY","DiMuon_","DY","DiMuon"),


    }



btag_zero_samples = {

    "nHad":("./New_7TeV_MC_8TeV_xSec/Had_Data","btag_zero_","Data","Had"),
    
     "mcHadW1":("./New_7TeV_MC_8TeV_xSec/Had_WJets","","WJetsInc","Had"),
     "mcHadttbar":("./New_7TeV_MC_8TeV_xSec/Had_TTbar","","TTbar","Had"),
     "mcHadzinv":("./New_7TeV_MC_8TeV_xSec/Had_Zinv","","Zinv50","Had"),
     "mcHadsingt":("./New_7TeV_MC_8TeV_xSec/Had_SingleTop","","Single_Tbar_t","Had"),
     "mcHaddiboson":("./New_7TeV_MC_8TeV_xSec/Had_DiBoson","","ZZ","Had"),
     "mcHadDY":("./New_7TeV_MC_8TeV_xSec/Had_DY","","DY","Had"),


    "nMuon":("./New_7TeV_MC_8TeV_xSec/Muon_Data","btag_zero_OneMuon_","Data","Muon"),
    
     "mcMuonW1":("./New_7TeV_MC_8TeV_xSec/Muon_WJets","OneMuon_","WJetsInc","Muon"),
     "mcMuonttbar":("./New_7TeV_MC_8TeV_xSec/Muon_TTbar","OneMuon_","TTbar","Muon"),
     "mcMuonzinv":("./New_7TeV_MC_8TeV_xSec/Muon_Zinv","OneMuon_","Zinv50","Muon"),
     "mcMuonsingt":("./New_7TeV_MC_8TeV_xSec/Muon_SingleTop","OneMuon_","Single_Tbar_t","Muon"),
     "mcMuondiboson":("./New_7TeV_MC_8TeV_xSec/Muon_DiBoson","OneMuon_","ZZ","Muon"),
     "mcMuonDY":("./New_7TeV_MC_8TeV_xSec/Muon_DY","OneMuon_","DY","Muon"),


    "nDiMuon":("./New_7TeV_MC_8TeV_xSec/Muon_Data","btag_zero_DiMuon_","Data","DiMuon"),
    
     "mcDiMuonW1":("./New_7TeV_MC_8TeV_xSec/Muon_WJets","DiMuon_","WJetsInc","DiMuon"),
     "mcDiMuonttbar":("./New_7TeV_MC_8TeV_xSec/Muon_TTbar","DiMuon_","TTbar","DiMuon"),
     "mcDiMuonzinv":("./New_7TeV_MC_8TeV_xSec/Muon_Zinv","DiMuon_","Zinv50","DiMuon"),
     "mcDiMuonsingt":("./New_7TeV_MC_8TeV_xSec/Muon_SingleTop","DiMuon_","Single_Tbar_t","DiMuon"),
     "mcDiMuondiboson":("./New_7TeV_MC_8TeV_xSec/Muon_DiBoson","DiMuon_","ZZ","DiMuon"),
     "mcDiMuonDY":("./New_7TeV_MC_8TeV_xSec/Muon_DY","DiMuon_","DY","DiMuon"),


    }


btag_more_than_two_samples = {

    "nHad":("./New_7TeV_MC_8TeV_xSec/Had_Data","btag_morethantwo_","Data","Had"),
    
     "mcHadW1":("./New_7TeV_MC_8TeV_xSec/Had_WJets","","WJetsInc","Had"),
     "mcHadttbar":("./New_7TeV_MC_8TeV_xSec/Had_TTbar","","TTbar","Had"),
     "mcHadzinv":("./New_7TeV_MC_8TeV_xSec/Had_Zinv","","Zinv50","Had"),
     "mcHadsingt":("./New_7TeV_MC_8TeV_xSec/Had_SingleTop","","Single_Tbar_t","Had"),
     "mcHaddiboson":("./New_7TeV_MC_8TeV_xSec/Had_DiBoson","","ZZ","Had"),
     "mcHadDY":("./New_7TeV_MC_8TeV_xSec/Had_DY","","DY","Had"),


    "nMuon":("./New_7TeV_MC_8TeV_xSec/Muon_Data","btag_morethantwo_OneMuon_","Data","Muon"),
    
     "mcMuonW1":("./New_7TeV_MC_8TeV_xSec/Muon_WJets","OneMuon_","WJetsInc","Muon"),
     "mcMuonttbar":("./New_7TeV_MC_8TeV_xSec/Muon_TTbar","OneMuon_","TTbar","Muon"),
     "mcMuonzinv":("./New_7TeV_MC_8TeV_xSec/Muon_Zinv","OneMuon_","Zinv50","Muon"),
     "mcMuonsingt":("./New_7TeV_MC_8TeV_xSec/Muon_SingleTop","OneMuon_","Single_Tbar_t","Muon"),
     "mcMuondiboson":("./New_7TeV_MC_8TeV_xSec/Muon_DiBoson","OneMuon_","ZZ","Muon"),
     "mcMuonDY":("./New_7TeV_MC_8TeV_xSec/Muon_DY","OneMuon_","DY","Muon"),


    "nDiMuon":("./New_7TeV_MC_8TeV_xSec/Muon_Data","btag_morethantwo_DiMuon_","Data","DiMuon"),
    
     "mcDiMuonW1":("./New_7TeV_MC_8TeV_xSec/Muon_WJets","DiMuon_","WJetsInc","DiMuon"),
     "mcDiMuonttbar":("./New_7TeV_MC_8TeV_xSec/Muon_TTbar","DiMuon_","TTbar","DiMuon"),
     "mcDiMuonzinv":("./New_7TeV_MC_8TeV_xSec/Muon_Zinv","DiMuon_","Zinv50","DiMuon"),
     "mcDiMuonsingt":("./New_7TeV_MC_8TeV_xSec/Muon_SingleTop","DiMuon_","Single_Tbar_t","DiMuon"),
     "mcDiMuondiboson":("./New_7TeV_MC_8TeV_xSec/Muon_DiBoson","DiMuon_","ZZ","DiMuon"),
     "mcDiMuonDY":("./New_7TeV_MC_8TeV_xSec/Muon_DY","DiMuon_","DY","DiMuon"),


    }


btag_more_than_zero_samples = {

    "nHad":("./New_7TeV_MC_8TeV_xSec/Had_Data","btag_morethanzero_","Data","Had"),
    
     "mcHadW1":("./New_7TeV_MC_8TeV_xSec/Had_WJets","","WJetsInc","Had"),
     "mcHadttbar":("./New_7TeV_MC_8TeV_xSec/Had_TTbar","","TTbar","Had"),
     "mcHadzinv":("./New_7TeV_MC_8TeV_xSec/Had_Zinv","","Zinv50","Had"),
     "mcHadsingt":("./New_7TeV_MC_8TeV_xSec/Had_SingleTop","","Single_Tbar_t","Had"),
     "mcHaddiboson":("./New_7TeV_MC_8TeV_xSec/Had_DiBoson","","ZZ","Had"),
     "mcHadDY":("./New_7TeV_MC_8TeV_xSec/Had_DY","","DY","Had"),


    "nMuon":("./New_7TeV_MC_8TeV_xSec/Muon_Data","btag_morethanzero_OneMuon_","Data","Muon"),
    
     "mcMuonW1":("./New_7TeV_MC_8TeV_xSec/Muon_WJets","OneMuon_","WJetsInc","Muon"),
     "mcMuonttbar":("./New_7TeV_MC_8TeV_xSec/Muon_TTbar","OneMuon_","TTbar","Muon"),
     "mcMuonzinv":("./New_7TeV_MC_8TeV_xSec/Muon_Zinv","OneMuon_","Zinv50","Muon"),
     "mcMuonsingt":("./New_7TeV_MC_8TeV_xSec/Muon_SingleTop","OneMuon_","Single_Tbar_t","Muon"),
     "mcMuondiboson":("./New_7TeV_MC_8TeV_xSec/Muon_DiBoson","OneMuon_","ZZ","Muon"),
     "mcMuonDY":("./New_7TeV_MC_8TeV_xSec/Muon_DY","OneMuon_","DY","Muon"),


    "nDiMuon":("./New_7TeV_MC_8TeV_xSec/Muon_Data","btag_morethanzero_DiMuon_","Data","DiMuon"),
    
     "mcDiMuonW1":("./New_7TeV_MC_8TeV_xSec/Muon_WJets","DiMuon_","WJetsInc","DiMuon"),
     "mcDiMuonttbar":("./New_7TeV_MC_8TeV_xSec/Muon_TTbar","DiMuon_","TTbar","DiMuon"),
     "mcDiMuonzinv":("./New_7TeV_MC_8TeV_xSec/Muon_Zinv","DiMuon_","Zinv50","DiMuon"),
     "mcDiMuonsingt":("./New_7TeV_MC_8TeV_xSec/Muon_SingleTop","DiMuon_","Single_Tbar_t","DiMuon"),
     "mcDiMuondiboson":("./New_7TeV_MC_8TeV_xSec/Muon_DiBoson","DiMuon_","ZZ","DiMuon"),
     "mcDiMuonDY":("./New_7TeV_MC_8TeV_xSec/Muon_DY","DiMuon_","DY","DiMuon"),


    }


btag_more_than_one_samples = {

    "nHad":("./New_7TeV_MC_8TeV_xSec/Had_Data","btag_morethanone_","Data","Had"),
    
     "mcHadW1":("./New_7TeV_MC_8TeV_xSec/Had_WJets","","WJetsInc","Had"),
     "mcHadttbar":("./New_7TeV_MC_8TeV_xSec/Had_TTbar","","TTbar","Had"),
     "mcHadzinv":("./New_7TeV_MC_8TeV_xSec/Had_Zinv","","Zinv50","Had"),
     "mcHadsingt":("./New_7TeV_MC_8TeV_xSec/Had_SingleTop","","Single_Tbar_t","Had"),
     "mcHaddiboson":("./New_7TeV_MC_8TeV_xSec/Had_DiBoson","","ZZ","Had"),
     "mcHadDY":("./New_7TeV_MC_8TeV_xSec/Had_DY","","DY","Had"),


    "nMuon":("./New_7TeV_MC_8TeV_xSec/Muon_Data","btag_morethanone_OneMuon_","Data","Muon"),
    
     "mcMuonW1":("./New_7TeV_MC_8TeV_xSec/Muon_WJets","OneMuon_","WJetsInc","Muon"),
     "mcMuonttbar":("./New_7TeV_MC_8TeV_xSec/Muon_TTbar","OneMuon_","TTbar","Muon"),
     "mcMuonzinv":("./New_7TeV_MC_8TeV_xSec/Muon_Zinv","OneMuon_","Zinv50","Muon"),
     "mcMuonsingt":("./New_7TeV_MC_8TeV_xSec/Muon_SingleTop","OneMuon_","Single_Tbar_t","Muon"),
     "mcMuondiboson":("./New_7TeV_MC_8TeV_xSec/Muon_DiBoson","OneMuon_","ZZ","Muon"),
     "mcMuonDY":("./New_7TeV_MC_8TeV_xSec/Muon_DY","OneMuon_","DY","Muon"),


    "nDiMuon":("./New_7TeV_MC_8TeV_xSec/Muon_Data","btag_morethanone_DiMuon_","Data","DiMuon"),
    
     "mcDiMuonW1":("./New_7TeV_MC_8TeV_xSec/Muon_WJets","DiMuon_","WJetsInc","DiMuon"),
     "mcDiMuonttbar":("./New_7TeV_MC_8TeV_xSec/Muon_TTbar","DiMuon_","TTbar","DiMuon"),
     "mcDiMuonzinv":("./New_7TeV_MC_8TeV_xSec/Muon_Zinv","DiMuon_","Zinv50","DiMuon"),
     "mcDiMuonsingt":("./New_7TeV_MC_8TeV_xSec/Muon_SingleTop","DiMuon_","Single_Tbar_t","DiMuon"),
     "mcDiMuondiboson":("./New_7TeV_MC_8TeV_xSec/Muon_DiBoson","DiMuon_","ZZ","DiMuon"),
     "mcDiMuonDY":("./New_7TeV_MC_8TeV_xSec/Muon_DY","DiMuon_","DY","DiMuon"),


    }




inclusive_samples = {

    "nHad":("./New_7TeV_MC_8TeV_xSec/Had_Data","","Data","Had"),
    
     "mcHadW1":("./New_7TeV_MC_8TeV_xSec/Had_WJets","","WJetsInc","Had"),
     "mcHadttbar":("./New_7TeV_MC_8TeV_xSec/Had_TTbar","","TTbar","Had"),
     "mcHadzinv":("./New_7TeV_MC_8TeV_xSec/Had_Zinv","","Zinv50","Had"),
     "mcHadsingt":("./New_7TeV_MC_8TeV_xSec/Had_SingleTop","","Single_Tbar_t","Had"),
     "mcHaddiboson":("./New_7TeV_MC_8TeV_xSec/Had_DiBoson","","ZZ","Had"),
     "mcHadDY":("./New_7TeV_MC_8TeV_xSec/Had_DY","","DY","Had"),


    "nMuon":("./New_7TeV_MC_8TeV_xSec/Muon_Data","OneMuon_","Data","Muon"),
    
     "mcMuonW1":("./New_7TeV_MC_8TeV_xSec/Muon_WJets","OneMuon_","WJetsInc","Muon"),
     "mcMuonttbar":("./New_7TeV_MC_8TeV_xSec/Muon_TTbar","OneMuon_","TTbar","Muon"),
     "mcMuonzinv":("./New_7TeV_MC_8TeV_xSec/Muon_Zinv","OneMuon_","Zinv50","Muon"),
     "mcMuonsingt":("./New_7TeV_MC_8TeV_xSec/Muon_SingleTop","OneMuon_","Single_Tbar_t","Muon"),
     "mcMuondiboson":("./New_7TeV_MC_8TeV_xSec/Muon_DiBoson","OneMuon_","ZZ","Muon"),
     "mcMuonDY":("./New_7TeV_MC_8TeV_xSec/Muon_DY","OneMuon_","DY","Muon"),


    "nDiMuon":("./New_7TeV_MC_8TeV_xSec/Muon_Data","DiMuon_","Data","DiMuon"),
    
     "mcDiMuonW1":("./New_7TeV_MC_8TeV_xSec/Muon_WJets","DiMuon_","WJetsInc","DiMuon"),
     "mcDiMuonttbar":("./New_7TeV_MC_8TeV_xSec/Muon_TTbar","DiMuon_","TTbar","DiMuon"),
     "mcDiMuonzinv":("./New_7TeV_MC_8TeV_xSec/Muon_Zinv","DiMuon_","Zinv50","DiMuon"),
     "mcDiMuonsingt":("./New_7TeV_MC_8TeV_xSec/Muon_SingleTop","DiMuon_","Single_Tbar_t","DiMuon"),
     "mcDiMuondiboson":("./New_7TeV_MC_8TeV_xSec/Muon_DiBoson","DiMuon_","ZZ","DiMuon"),
     "mcDiMuonDY":("./New_7TeV_MC_8TeV_xSec/Muon_DY","DiMuon_","DY","DiMuon"),


    }


calc_file = {
     "mchad":("./New_7TeV_MC_8TeV_xSec/Had_MC.root","Had",""),
     "mchadzinv":("./New_7TeV_MC_8TeV_xSec/Had_Zinv.root","Had_Zinv",""),
     "mcmuon":("./New_7TeV_MC_8TeV_xSec/Muon_MC.root","Muon","OneMuon_"),
     "mcdimuon":("./New_7TeV_MC_8TeV_xSec/Muon_MC.root","DiMuon","DiMuon_"),

}


#calc_file = {
#     "mchad":("./May_11_root_Files/Had_MC.root","Had",""),
#     "mcmuon":("./May_11_root_Files/Muon_MC.root","Muon","OneMuon_"),
#     "mcdimuon":("./May_11_root_Files/Muon_MC.root","DiMuon","DiMuon_"),
#
#}

if __name__=="__main__":
  #a = Number_Extractor(settings,btag_two_samples,"Two_btags",Triggers = "True",AlphaT="False",Calculation=calc_file)
  #b = Number_Extractor(settings,btag_one_samples,"One_btag",Triggers = "True",AlphaT="False",Calculation=calc_file)
  #c = Number_Extractor(settings,btag_zero_samples,"Zero_btags",Triggers = "True",AlphaT="False",Calculation=calc_file)
  #d = Number_Extractor(settings,btag_more_than_two_samples,"More_Than_Two_btag",Triggers = "True",AlphaT="False",Calculation=calc_file)
  #t = Number_Extractor(settings,btag_zero_samples,"Zero_btags",Triggers = "True",AlphaT="False",Calculation=calc_file)
  #e  = Number_Extractor(settings,btag_more_than_zero_samples,"More_Than_Zero_btag",Triggers = "True",AlphaT="False",Calculation=calc_file)
  #f  = Number_Extractor(settings,btag_more_than_one_samples,"More_Than_One_btag",Triggers = "True",AlphaT="False",Calculation=calc_file)
  g  = Number_Extractor(settings,inclusive_samples,"Inclusive",Triggers = "True",AlphaT="False",Calculation=calc_file,Split_Lumi = "False")
  #g  = Number_Extractor(settings,inclusive_samples,"Inclusive",Triggers = "True",AlphaT="False",Split_Lumi = "False")
