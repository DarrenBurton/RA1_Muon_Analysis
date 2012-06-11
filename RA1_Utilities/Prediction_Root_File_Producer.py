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
  "Lumo":2.4, # Luminosity in fb
  "Multi_Lumi":{'Had':2.4,'Muon':2.28,'DiMuon':2.28}
  #"AlphaTSlices":["0.55_10"]
      }


'''
Sample Dictionary Instructions

eg "nMuon":("../UncorrectMET_ICHEP/Muon_Data","btag_two_OneMuon_","Data","Muon"),
if n at start of name entry then the file is data and will no be scaled to luminosity.
first argument is path to root file
second argument is prefix to ht bin. i.e OneMuon_275_325
third argument is data/mc type, i.e. Data, WJets250 - MC relating to the binned WJets 250-300 HT sample
fourth argument is sample Type, Had/DiMuon/Muon. 

the only thing that will have to be changed is the second argument depending on wether you are running btag multiplicity/baseline
'''
btag_two_samples = {

    "nHad":("../UncorrectMET_ICHEP/Had_Data","btag_two_","Data","Had"),
    
     "mcHadW1":("../UncorrectMET_ICHEP/Had_WJets","","WJetsInc","Had"),
     "mcHadttbar":("../UncorrectMET_ICHEP/Had_TTbar","","TTbar","Had"),
     "mcHadzinv":("../UncorrectMET_ICHEP/Had_Zinv","","Zinv50","Had"),
     "mcHadsingt":("../UncorrectMET_ICHEP/Had_SingleTop","","Single_Tbar_t","Had"),
    # "mcHaddiboson":("../UncorrectMET_ICHEP/Had_DiBoson","","ZZ","Had"),
     "mcHadDY":("../UncorrectMET_ICHEP/Had_DY","","DY","Had"),

    "nMuon":("../UncorrectMET_ICHEP/Muon_Data","btag_two_OneMuon_","Data","Muon"),
    
     "mcMuonW1":("../UncorrectMET_ICHEP/Muon_WJets","OneMuon_","WJetsInc","Muon"),
     "mcMuonttbar":("../UncorrectMET_ICHEP/Muon_TTbar","OneMuon_","TTbar","Muon"),
    # "mcMuonzinv":("../UncorrectMET_ICHEP/Muon_Zinv","OneMuon_","Zinv50","Muon"),
     "mcMuonsingt":("../UncorrectMET_ICHEP/Muon_SingleTop","OneMuon_","Single_Tbar_t","Muon"),
    # "mcMuondiboson":("../UncorrectMET_ICHEP/Muon_DiBoson","OneMuon_","ZZ","Muon"),
     "mcMuonDY":("../UncorrectMET_ICHEP/Muon_DY","OneMuon_","DY","Muon"),


    "nDiMuon":("../UncorrectMET_ICHEP/Muon_Data","btag_two_DiMuon_","Data","DiMuon"),
    
     "mcDiMuonW1":("../UncorrectMET_ICHEP/Muon_WJets","DiMuon_","WJetsInc","DiMuon"),
     "mcDiMuonttbar":("../UncorrectMET_ICHEP/Muon_TTbar","DiMuon_","TTbar","DiMuon"),
    # "mcDiMuonzinv":("../UncorrectMET_ICHEP/Muon_Zinv","DiMuon_","Zinv50","DiMuon"),
     "mcDiMuonsingt":("../UncorrectMET_ICHEP/Muon_SingleTop","DiMuon_","Single_Tbar_t","DiMuon"),
     #"mcDiMuondiboson":("../UncorrectMET_ICHEP/Muon_DiBoson","DiMuon_","ZZ","DiMuon"),
     "mcDiMuonDY":("../UncorrectMET_ICHEP/Muon_DY","DiMuon_","DY","DiMuon"),


    }


btag_one_samples = {

    "nHad":("../UncorrectMET_ICHEP/Had_Data","btag_one_","Data","Had"),
    
     "mcHadW1":("../UncorrectMET_ICHEP/Had_WJets","","WJetsInc","Had"),
     "mcHadttbar":("../UncorrectMET_ICHEP/Had_TTbar","","TTbar","Had"),
     "mcHadzinv":("../UncorrectMET_ICHEP/Had_Zinv","","Zinv50","Had"),
     "mcHadsingt":("../UncorrectMET_ICHEP/Had_SingleTop","","Single_Tbar_t","Had"),
     #"mcHaddiboson":("../UncorrectMET_ICHEP/Had_DiBoson","","ZZ","Had"),
     "mcHadDY":("../UncorrectMET_ICHEP/Had_DY","","DY","Had"),


    "nMuon":("../UncorrectMET_ICHEP/Muon_Data","btag_one_OneMuon_","Data","Muon"),
    
     "mcMuonW1":("../UncorrectMET_ICHEP/Muon_WJets","OneMuon_","WJetsInc","Muon"),
     "mcMuonttbar":("../UncorrectMET_ICHEP/Muon_TTbar","OneMuon_","TTbar","Muon"),
     #"mcMuonzinv":("../UncorrectMET_ICHEP/Muon_Zinv","OneMuon_","Zinv50","Muon"),
     "mcMuonsingt":("../UncorrectMET_ICHEP/Muon_SingleTop","OneMuon_","Single_Tbar_t","Muon"),
     #"mcMuondiboson":("../UncorrectMET_ICHEP/Muon_DiBoson","OneMuon_","ZZ","Muon"),
     "mcMuonDY":("../UncorrectMET_ICHEP/Muon_DY","OneMuon_","DY","Muon"),


    "nDiMuon":("../UncorrectMET_ICHEP/Muon_Data","btag_one_DiMuon_","Data","DiMuon"),
    
     "mcDiMuonW1":("../UncorrectMET_ICHEP/Muon_WJets","DiMuon_","WJetsInc","DiMuon"),
     "mcDiMuonttbar":("../UncorrectMET_ICHEP/Muon_TTbar","DiMuon_","TTbar","DiMuon"),
    # "mcDiMuonzinv":("../UncorrectMET_ICHEP/Muon_Zinv","DiMuon_","Zinv50","DiMuon"),
     "mcDiMuonsingt":("../UncorrectMET_ICHEP/Muon_SingleTop","DiMuon_","Single_Tbar_t","DiMuon"),
    # "mcDiMuondiboson":("../UncorrectMET_ICHEP/Muon_DiBoson","DiMuon_","ZZ","DiMuon"),
     "mcDiMuonDY":("../UncorrectMET_ICHEP/Muon_DY","DiMuon_","DY","DiMuon"),


    }



btag_zero_samples = {

    "nHad":("../UncorrectMET_ICHEP/Had_Data","btag_zero_","Data","Had"),
    
     "mcHadW1":("../UncorrectMET_ICHEP/Had_WJets","","WJetsInc","Had"),
     "mcHadttbar":("../UncorrectMET_ICHEP/Had_TTbar","","TTbar","Had"),
     "mcHadzinv":("../UncorrectMET_ICHEP/Had_Zinv","","Zinv50","Had"),
     "mcHadsingt":("../UncorrectMET_ICHEP/Had_SingleTop","","Single_Tbar_t","Had"),
     #"mcHaddiboson":("../UncorrectMET_ICHEP/Had_DiBoson","","ZZ","Had"),
     "mcHadDY":("../UncorrectMET_ICHEP/Had_DY","","DY","Had"),


    "nMuon":("../UncorrectMET_ICHEP/Muon_Data","btag_zero_OneMuon_","Data","Muon"),
    
     "mcMuonW1":("../UncorrectMET_ICHEP/Muon_WJets","OneMuon_","WJetsInc","Muon"),
     "mcMuonttbar":("../UncorrectMET_ICHEP/Muon_TTbar","OneMuon_","TTbar","Muon"),
    # "mcMuonzinv":("../UncorrectMET_ICHEP/Muon_Zinv","OneMuon_","Zinv50","Muon"),
     "mcMuonsingt":("../UncorrectMET_ICHEP/Muon_SingleTop","OneMuon_","Single_Tbar_t","Muon"),
    # "mcMuondiboson":("../UncorrectMET_ICHEP/Muon_DiBoson","OneMuon_","ZZ","Muon"),
     "mcMuonDY":("../UncorrectMET_ICHEP/Muon_DY","OneMuon_","DY","Muon"),


    "nDiMuon":("../UncorrectMET_ICHEP/Muon_Data","btag_zero_DiMuon_","Data","DiMuon"),
    
     "mcDiMuonW1":("../UncorrectMET_ICHEP/Muon_WJets","DiMuon_","WJetsInc","DiMuon"),
     "mcDiMuonttbar":("../UncorrectMET_ICHEP/Muon_TTbar","DiMuon_","TTbar","DiMuon"),
     #"mcDiMuonzinv":("../UncorrectMET_ICHEP/Muon_Zinv","DiMuon_","Zinv50","DiMuon"),
     "mcDiMuonsingt":("../UncorrectMET_ICHEP/Muon_SingleTop","DiMuon_","Single_Tbar_t","DiMuon"),
    # "mcDiMuondiboson":("../UncorrectMET_ICHEP/Muon_DiBoson","DiMuon_","ZZ","DiMuon"),
     "mcDiMuonDY":("../UncorrectMET_ICHEP/Muon_DY","DiMuon_","DY","DiMuon"),


    }


btag_more_than_two_samples = {

    "nHad":("../UncorrectMET_ICHEP/Had_Data","btag_morethantwo_","Data","Had"),
    
     "mcHadW1":("../UncorrectMET_ICHEP/Had_WJets","","WJetsInc","Had"),
     "mcHadttbar":("../UncorrectMET_ICHEP/Had_TTbar","","TTbar","Had"),
     "mcHadzinv":("../UncorrectMET_ICHEP/Had_Zinv","","Zinv50","Had"),
     "mcHadsingt":("../UncorrectMET_ICHEP/Had_SingleTop","","Single_Tbar_t","Had"),
    # "mcHaddiboson":("../UncorrectMET_ICHEP/Had_DiBoson","","ZZ","Had"),
     "mcHadDY":("../UncorrectMET_ICHEP/Had_DY","","DY","Had"),


    "nMuon":("../UncorrectMET_ICHEP/Muon_Data","btag_morethantwo_OneMuon_","Data","Muon"),
    
     "mcMuonW1":("../UncorrectMET_ICHEP/Muon_WJets","OneMuon_","WJetsInc","Muon"),
     "mcMuonttbar":("../UncorrectMET_ICHEP/Muon_TTbar","OneMuon_","TTbar","Muon"),
     #"mcMuonzinv":("../UncorrectMET_ICHEP/Muon_Zinv","OneMuon_","Zinv50","Muon"),
     "mcMuonsingt":("../UncorrectMET_ICHEP/Muon_SingleTop","OneMuon_","Single_Tbar_t","Muon"),
     #"mcMuondiboson":("../UncorrectMET_ICHEP/Muon_DiBoson","OneMuon_","ZZ","Muon"),
     "mcMuonDY":("../UncorrectMET_ICHEP/Muon_DY","OneMuon_","DY","Muon"),


    "nDiMuon":("../UncorrectMET_ICHEP/Muon_Data","btag_morethantwo_DiMuon_","Data","DiMuon"),
    
     "mcDiMuonW1":("../UncorrectMET_ICHEP/Muon_WJets","DiMuon_","WJetsInc","DiMuon"),
     "mcDiMuonttbar":("../UncorrectMET_ICHEP/Muon_TTbar","DiMuon_","TTbar","DiMuon"),
     #"mcDiMuonzinv":("../UncorrectMET_ICHEP/Muon_Zinv","DiMuon_","Zinv50","DiMuon"),
     "mcDiMuonsingt":("../UncorrectMET_ICHEP/Muon_SingleTop","DiMuon_","Single_Tbar_t","DiMuon"),
    # "mcDiMuondiboson":("../UncorrectMET_ICHEP/Muon_DiBoson","DiMuon_","ZZ","DiMuon"),
     "mcDiMuonDY":("../UncorrectMET_ICHEP/Muon_DY","DiMuon_","DY","DiMuon"),


    }


btag_more_than_zero_samples = {

    "nHad":("../UncorrectMET_ICHEP/Had_Data","btag_morethanzero_","Data","Had"),
    
     "mcHadW1":("../UncorrectMET_ICHEP/Had_WJets","","WJetsInc","Had"),
     "mcHadttbar":("../UncorrectMET_ICHEP/Had_TTbar","","TTbar","Had"),
     "mcHadzinv":("../UncorrectMET_ICHEP/Had_Zinv","","Zinv50","Had"),
     "mcHadsingt":("../UncorrectMET_ICHEP/Had_SingleTop","","Single_Tbar_t","Had"),
     #"mcHaddiboson":("../UncorrectMET_ICHEP/Had_DiBoson","","ZZ","Had"),
     "mcHadDY":("../UncorrectMET_ICHEP/Had_DY","","DY","Had"),


    "nMuon":("../UncorrectMET_ICHEP/Muon_Data","btag_morethanzero_OneMuon_","Data","Muon"),
    
     "mcMuonW1":("../UncorrectMET_ICHEP/Muon_WJets","OneMuon_","WJetsInc","Muon"),
     "mcMuonttbar":("../UncorrectMET_ICHEP/Muon_TTbar","OneMuon_","TTbar","Muon"),
     #"mcMuonzinv":("../UncorrectMET_ICHEP/Muon_Zinv","OneMuon_","Zinv50","Muon"),
     "mcMuonsingt":("../UncorrectMET_ICHEP/Muon_SingleTop","OneMuon_","Single_Tbar_t","Muon"),
     #"mcMuondiboson":("../UncorrectMET_ICHEP/Muon_DiBoson","OneMuon_","ZZ","Muon"),
     "mcMuonDY":("../UncorrectMET_ICHEP/Muon_DY","OneMuon_","DY","Muon"),


    "nDiMuon":("../UncorrectMET_ICHEP/Muon_Data","btag_morethanzero_DiMuon_","Data","DiMuon"),
    
     "mcDiMuonW1":("../UncorrectMET_ICHEP/Muon_WJets","DiMuon_","WJetsInc","DiMuon"),
     "mcDiMuonttbar":("../UncorrectMET_ICHEP/Muon_TTbar","DiMuon_","TTbar","DiMuon"),
     #"mcDiMuonzinv":("../UncorrectMET_ICHEP/Muon_Zinv","DiMuon_","Zinv50","DiMuon"),
     "mcDiMuonsingt":("../UncorrectMET_ICHEP/Muon_SingleTop","DiMuon_","Single_Tbar_t","DiMuon"),
     #"mcDiMuondiboson":("../UncorrectMET_ICHEP/Muon_DiBoson","DiMuon_","ZZ","DiMuon"),
     "mcDiMuonDY":("../UncorrectMET_ICHEP/Muon_DY","DiMuon_","DY","DiMuon"),


    }


btag_more_than_one_samples = {

    "nHad":("../UncorrectMET_ICHEP/Had_Data","btag_morethanone_","Data","Had"),
    
     "mcHadW1":("../UncorrectMET_ICHEP/Had_WJets","","WJetsInc","Had"),
     "mcHadttbar":("../UncorrectMET_ICHEP/Had_TTbar","","TTbar","Had"),
     "mcHadzinv":("../UncorrectMET_ICHEP/Had_Zinv","","Zinv50","Had"),
     "mcHadsingt":("../UncorrectMET_ICHEP/Had_SingleTop","","Single_Tbar_t","Had"),
    # "mcHaddiboson":("../UncorrectMET_ICHEP/Had_DiBoson","","ZZ","Had"),
     "mcHadDY":("../UncorrectMET_ICHEP/Had_DY","","DY","Had"),


    "nMuon":("../UncorrectMET_ICHEP/Muon_Data","btag_morethanone_OneMuon_","Data","Muon"),
    
     "mcMuonW1":("../UncorrectMET_ICHEP/Muon_WJets","OneMuon_","WJetsInc","Muon"),
     "mcMuonttbar":("../UncorrectMET_ICHEP/Muon_TTbar","OneMuon_","TTbar","Muon"),
     #"mcMuonzinv":("../UncorrectMET_ICHEP/Muon_Zinv","OneMuon_","Zinv50","Muon"),
     "mcMuonsingt":("../UncorrectMET_ICHEP/Muon_SingleTop","OneMuon_","Single_Tbar_t","Muon"),
     #"mcMuondiboson":("../UncorrectMET_ICHEP/Muon_DiBoson","OneMuon_","ZZ","Muon"),
     "mcMuonDY":("../UncorrectMET_ICHEP/Muon_DY","OneMuon_","DY","Muon"),


    "nDiMuon":("../UncorrectMET_ICHEP/Muon_Data","btag_morethanone_DiMuon_","Data","DiMuon"),
    
     "mcDiMuonW1":("../UncorrectMET_ICHEP/Muon_WJets","DiMuon_","WJetsInc","DiMuon"),
     "mcDiMuonttbar":("../UncorrectMET_ICHEP/Muon_TTbar","DiMuon_","TTbar","DiMuon"),
     #"mcDiMuonzinv":("../UncorrectMET_ICHEP/Muon_Zinv","DiMuon_","Zinv50","DiMuon"),
     "mcDiMuonsingt":("../UncorrectMET_ICHEP/Muon_SingleTop","DiMuon_","Single_Tbar_t","DiMuon"),
     #"mcDiMuondiboson":("../UncorrectMET_ICHEP/Muon_DiBoson","DiMuon_","ZZ","DiMuon"),
     "mcDiMuonDY":("../UncorrectMET_ICHEP/Muon_DY","DiMuon_","DY","DiMuon"),


    }




inclusive_samples = {

    "nHad":("../UncorrectMET_ICHEP/Had_Data","","Data","Had"),
    
     "mcHadW1":("../UncorrectMET_ICHEP/Had_WJets","","WJetsInc","Had"),
     "mcHadttbar":("../UncorrectMET_ICHEP/Had_TTbar","","TTbar","Had"),
     "mcHadzinv":("../UncorrectMET_ICHEP/Had_Zinv","","Zinv50","Had"),
     "mcHadsingt":("../UncorrectMET_ICHEP/Had_SingleTop","","Single_Tbar_t","Had"),
     #"mcHaddiboson":("../UncorrectMET_ICHEP/Had_DiBoson","","ZZ","Had"),
     "mcHadDY":("../UncorrectMET_ICHEP/Had_DY","","DY","Had"),


    "nMuon":("../UncorrectMET_ICHEP/Muon_Data","OneMuon_","Data","Muon"),
    
     "mcMuonW1":("../UncorrectMET_ICHEP/Muon_WJets","OneMuon_","WJetsInc","Muon"),
     "mcMuonttbar":("../UncorrectMET_ICHEP/Muon_TTbar","OneMuon_","TTbar","Muon"),
     #"mcMuonzinv":("../UncorrectMET_ICHEP/Muon_Zinv","OneMuon_","Zinv50","Muon"),
     "mcMuonsingt":("../UncorrectMET_ICHEP/Muon_SingleTop","OneMuon_","Single_Tbar_t","Muon"),
     #"mcMuondiboson":("../UncorrectMET_ICHEP/Muon_DiBoson","OneMuon_","ZZ","Muon"),
     "mcMuonDY":("../UncorrectMET_ICHEP/Muon_DY","OneMuon_","DY","Muon"),


    "nDiMuon":("../UncorrectMET_ICHEP/Muon_Data","DiMuon_","Data","DiMuon"),
    
     "mcDiMuonW1":("../UncorrectMET_ICHEP/Muon_WJets","DiMuon_","WJetsInc","DiMuon"),
     "mcDiMuonttbar":("../UncorrectMET_ICHEP/Muon_TTbar","DiMuon_","TTbar","DiMuon"),
     #"mcDiMuonzinv":("../UncorrectMET_ICHEP/Muon_Zinv","DiMuon_","Zinv50","DiMuon"),
     "mcDiMuonsingt":("../UncorrectMET_ICHEP/Muon_SingleTop","DiMuon_","Single_Tbar_t","DiMuon"),
     #"mcDiMuondiboson":("../UncorrectMET_ICHEP/Muon_DiBoson","DiMuon_","ZZ","DiMuon"),
     "mcDiMuonDY":("../UncorrectMET_ICHEP/Muon_DY","DiMuon_","DY","DiMuon"),


    }


calc_file = {
     "mchad":("../UncorrectMET_ICHEP/Had_MC.root","Had",""),
     "mchadzinv":("../UncorrectMET_ICHEP/Had_MC.root","Had_Zinv",""),
     "mcmuon":("../UncorrectMET_ICHEP/Muon_MC.root","Muon","OneMuon_"),
     "mcdimuon":("../UncorrectMET_ICHEP/Muon_MC.root","DiMuon","DiMuon_"),

}


#calc_file = {
#     "mchad":("../UncorrectMET_ICHEP/Had_MC.root","Had",""),
#     "mcmuon":("../UncorrectMET_ICHEP/Muon_MC.root","Muon","OneMuon_"),
#     "mcdimuon":("../UncorrectMET_ICHEP/Muon_MC.root","DiMuon","DiMuon_"),
#
#}

if __name__=="__main__":
  a = Number_Extractor(settings,btag_two_samples,"Two_btags",Triggers = "False",AlphaT="False",Calculation=calc_file,Stats = "True",Split_Lumi = "True")
  b = Number_Extractor(settings,btag_one_samples,"One_btag",Triggers = "False",AlphaT="False",Calculation=calc_file,Stats = "True",Split_Lumi = "True")
  c = Number_Extractor(settings,btag_zero_samples,"Zero_btags",Triggers = "False",AlphaT="True",Calculation=calc_file,Stats = "True",Split_Lumi = "True")
  d = Number_Extractor(settings,btag_more_than_two_samples,"More_Than_Two_btag",Triggers = "False",AlphaT="False",Calculation=calc_file,Stats = "True",Split_Lumi = "True")
  #e  = Number_Extractor(settings,btag_more_than_zero_samples,"More_Than_Zero_btag",Triggers = "False",AlphaT="False",Calculation=calc_file,Stats = "True",Split_Lumi = "True")
  #f  = Number_Extractor(settings,btag_more_than_one_samples,"More_Than_One_btag",Triggers = "False",AlphaT="False",Calculation=calc_file,Stats = "True",Split_Lumi = "True")
  g  = Number_Extractor(settings,inclusive_samples,"Inclusive",Triggers = "False",AlphaT="False",Calculation=calc_file,Stats = "True",Split_Lumi = "True")
