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
  "Lumo":1.533,
  "Multi_Lumi":{'Had':1.566,'Muon':1.561,'DiMuon':1.561}
  #"AlphaTSlices":["0.55_10"]
      }

btag_two_samples = {

    "nHad":("../28_May_Root_Files/Had_Data","btag_two_","Data","Had"),
    
     "mcHadW1":("../28_May_Root_Files/Had_WJets","btag_two_","WJetsInc","Had"),
     "mcHadttbar":("../28_May_Root_Files/Had_TTbar","btag_two_","TTbar","Had"),
     "mcHadzinv":("../28_May_Root_Files/Had_Zinv","btag_two_","Zinv50","Had"),
     "mcHadsingt":("../28_May_Root_Files/Had_SingleTop","btag_two_","Single_Tbar_t","Had"),
     "mcHaddiboson":("../28_May_Root_Files/Had_DiBoson","btag_two_","ZZ","Had"),
     "mcHadDY":("../28_May_Root_Files/Had_DY","btag_two_","DY","Had"),

    "nMuon":("../28_May_Root_Files/Muon_Data","btag_two_OneMuon_","Data","Muon"),
    
     "mcMuonW1":("../28_May_Root_Files/Muon_WJets","btag_two_OneMuon_","WJetsInc","Muon"),
     "mcMuonttbar":("../28_May_Root_Files/Muon_TTbar","btag_two_OneMuon_","TTbar","Muon"),
     "mcMuonzinv":("../28_May_Root_Files/Muon_Zinv","btag_two_OneMuon_","Zinv50","Muon"),
     "mcMuonsingt":("../28_May_Root_Files/Muon_SingleTop","btag_two_OneMuon_","Single_Tbar_t","Muon"),
     "mcMuondiboson":("../28_May_Root_Files/Muon_DiBoson","btag_two_OneMuon_","ZZ","Muon"),
     "mcMuonDY":("../28_May_Root_Files/Muon_DY","btag_two_OneMuon_","DY","Muon"),


    "nDiMuon":("../28_May_Root_Files/Muon_Data","btag_two_DiMuon_","Data","DiMuon"),
    
     "mcDiMuonW1":("../28_May_Root_Files/Muon_WJets","btag_two_DiMuon_","WJetsInc","DiMuon"),
     "mcDiMuonttbar":("../28_May_Root_Files/Muon_TTbar","btag_two_DiMuon_","TTbar","DiMuon"),
     "mcDiMuonzinv":("../28_May_Root_Files/Muon_Zinv","btag_two_DiMuon_","Zinv50","DiMuon"),
     "mcDiMuonsingt":("../28_May_Root_Files/Muon_SingleTop","btag_two_DiMuon_","Single_Tbar_t","DiMuon"),
     "mcDiMuondiboson":("../28_May_Root_Files/Muon_DiBoson","btag_two_DiMuon_","ZZ","DiMuon"),
     "mcDiMuonDY":("../28_May_Root_Files/Muon_DY","btag_two_DiMuon_","DY","DiMuon"),


    }


btag_one_samples = {

    "nHad":("../28_May_Root_Files/Had_Data","btag_one_","Data","Had"),
    
     "mcHadW1":("../28_May_Root_Files/Had_WJets","btag_one_","WJetsInc","Had"),
     "mcHadttbar":("../28_May_Root_Files/Had_TTbar","btag_one_","TTbar","Had"),
     "mcHadzinv":("../28_May_Root_Files/Had_Zinv","btag_one_","Zinv50","Had"),
     "mcHadsingt":("../28_May_Root_Files/Had_SingleTop","btag_one_","Single_Tbar_t","Had"),
     "mcHaddiboson":("../28_May_Root_Files/Had_DiBoson","btag_one_","ZZ","Had"),
     "mcHadDY":("../28_May_Root_Files/Had_DY","btag_one_","DY","Had"),


    "nMuon":("../28_May_Root_Files/Muon_Data","btag_one_OneMuon_","Data","Muon"),
    
     "mcMuonW1":("../28_May_Root_Files/Muon_WJets","btag_one_OneMuon_","WJetsInc","Muon"),
     "mcMuonttbar":("../28_May_Root_Files/Muon_TTbar","btag_one_OneMuon_","TTbar","Muon"),
     "mcMuonzinv":("../28_May_Root_Files/Muon_Zinv","btag_one_OneMuon_","Zinv50","Muon"),
     "mcMuonsingt":("../28_May_Root_Files/Muon_SingleTop","btag_one_OneMuon_","Single_Tbar_t","Muon"),
     "mcMuondiboson":("../28_May_Root_Files/Muon_DiBoson","btag_one_OneMuon_","ZZ","Muon"),
     "mcMuonDY":("../28_May_Root_Files/Muon_DY","btag_one_OneMuon_","DY","Muon"),


    "nDiMuon":("../28_May_Root_Files/Muon_Data","btag_one_DiMuon_","Data","DiMuon"),
    
     "mcDiMuonW1":("../28_May_Root_Files/Muon_WJets","btag_one_DiMuon_","WJetsInc","DiMuon"),
     "mcDiMuonttbar":("../28_May_Root_Files/Muon_TTbar","btag_one_DiMuon_","TTbar","DiMuon"),
     "mcDiMuonzinv":("../28_May_Root_Files/Muon_Zinv","btag_one_DiMuon_","Zinv50","DiMuon"),
     "mcDiMuonsingt":("../28_May_Root_Files/Muon_SingleTop","btag_one_DiMuon_","Single_Tbar_t","DiMuon"),
     "mcDiMuondiboson":("../28_May_Root_Files/Muon_DiBoson","btag_one_DiMuon_","ZZ","DiMuon"),
     "mcDiMuonDY":("../28_May_Root_Files/Muon_DY","btag_one_DiMuon_","DY","DiMuon"),


    }



btag_zero_samples = {

    "nHad":("../28_May_Root_Files/Had_Data","btag_zero_","Data","Had"),
    
     "mcHadW1":("../28_May_Root_Files/Had_WJets","btag_zero_","WJetsInc","Had"),
     "mcHadttbar":("../28_May_Root_Files/Had_TTbar","btag_zero_","TTbar","Had"),
     "mcHadzinv":("../28_May_Root_Files/Had_Zinv","btag_zero_","Zinv50","Had"),
     "mcHadsingt":("../28_May_Root_Files/Had_SingleTop","btag_zero_","Single_Tbar_t","Had"),
     "mcHaddiboson":("../28_May_Root_Files/Had_DiBoson","btag_zero_","ZZ","Had"),
     "mcHadDY":("../28_May_Root_Files/Had_DY","btag_zero_","DY","Had"),


    "nMuon":("../28_May_Root_Files/Muon_Data","btag_zero_OneMuon_","Data","Muon"),
    
     "mcMuonW1":("../28_May_Root_Files/Muon_WJets","btag_zero_OneMuon_","WJetsInc","Muon"),
     "mcMuonttbar":("../28_May_Root_Files/Muon_TTbar","btag_zero_OneMuon_","TTbar","Muon"),
     "mcMuonzinv":("../28_May_Root_Files/Muon_Zinv","btag_zero_OneMuon_","Zinv50","Muon"),
     "mcMuonsingt":("../28_May_Root_Files/Muon_SingleTop","btag_zero_OneMuon_","Single_Tbar_t","Muon"),
     "mcMuondiboson":("../28_May_Root_Files/Muon_DiBoson","btag_zero_OneMuon_","ZZ","Muon"),
     "mcMuonDY":("../28_May_Root_Files/Muon_DY","btag_zero_OneMuon_","DY","Muon"),


    "nDiMuon":("../28_May_Root_Files/Muon_Data","btag_zero_DiMuon_","Data","DiMuon"),
    
     "mcDiMuonW1":("../28_May_Root_Files/Muon_WJets","btag_zero_DiMuon_","WJetsInc","DiMuon"),
     "mcDiMuonttbar":("../28_May_Root_Files/Muon_TTbar","btag_zero_DiMuon_","TTbar","DiMuon"),
     "mcDiMuonzinv":("../28_May_Root_Files/Muon_Zinv","btag_zero_DiMuon_","Zinv50","DiMuon"),
     "mcDiMuonsingt":("../28_May_Root_Files/Muon_SingleTop","btag_zero_DiMuon_","Single_Tbar_t","DiMuon"),
     "mcDiMuondiboson":("../28_May_Root_Files/Muon_DiBoson","btag_zero_DiMuon_","ZZ","DiMuon"),
     "mcDiMuonDY":("../28_May_Root_Files/Muon_DY","btag_zero_DiMuon_","DY","DiMuon"),


    }


btag_more_than_two_samples = {

    "nHad":("../28_May_Root_Files/Had_Data","btag_morethantwo_","Data","Had"),
    
     "mcHadW1":("../28_May_Root_Files/Had_WJets","btag_morethantwo_","WJetsInc","Had"),
     "mcHadttbar":("../28_May_Root_Files/Had_TTbar","btag_morethantwo_","TTbar","Had"),
     "mcHadzinv":("../28_May_Root_Files/Had_Zinv","btag_morethantwo_","Zinv50","Had"),
     "mcHadsingt":("../28_May_Root_Files/Had_SingleTop","btag_morethantwo_","Single_Tbar_t","Had"),
     "mcHaddiboson":("../28_May_Root_Files/Had_DiBoson","btag_morethantwo_","ZZ","Had"),
     "mcHadDY":("../28_May_Root_Files/Had_DY","btag_morethantwo_","DY","Had"),


    "nMuon":("../28_May_Root_Files/Muon_Data","btag_morethantwo_OneMuon_","Data","Muon"),
    
     "mcMuonW1":("../28_May_Root_Files/Muon_WJets","btag_morethantwo_OneMuon_","WJetsInc","Muon"),
     "mcMuonttbar":("../28_May_Root_Files/Muon_TTbar","btag_morethantwo_OneMuon_","TTbar","Muon"),
     "mcMuonzinv":("../28_May_Root_Files/Muon_Zinv","btag_morethantwo_OneMuon_","Zinv50","Muon"),
     "mcMuonsingt":("../28_May_Root_Files/Muon_SingleTop","btag_morethantwo_OneMuon_","Single_Tbar_t","Muon"),
     "mcMuondiboson":("../28_May_Root_Files/Muon_DiBoson","btag_morethantwo_OneMuon_","ZZ","Muon"),
     "mcMuonDY":("../28_May_Root_Files/Muon_DY","btag_morethantwo_OneMuon_","DY","Muon"),


    "nDiMuon":("../28_May_Root_Files/Muon_Data","btag_morethantwo_DiMuon_","Data","DiMuon"),
    
     "mcDiMuonW1":("../28_May_Root_Files/Muon_WJets","btag_morethantwo_DiMuon_","WJetsInc","DiMuon"),
     "mcDiMuonttbar":("../28_May_Root_Files/Muon_TTbar","btag_morethantwo_DiMuon_","TTbar","DiMuon"),
     "mcDiMuonzinv":("../28_May_Root_Files/Muon_Zinv","btag_morethantwo_DiMuon_","Zinv50","DiMuon"),
     "mcDiMuonsingt":("../28_May_Root_Files/Muon_SingleTop","btag_morethantwo_DiMuon_","Single_Tbar_t","DiMuon"),
     "mcDiMuondiboson":("../28_May_Root_Files/Muon_DiBoson","btag_morethantwo_DiMuon_","ZZ","DiMuon"),
     "mcDiMuonDY":("../28_May_Root_Files/Muon_DY","btag_morethantwo_DiMuon_","DY","DiMuon"),


    }


btag_more_than_zero_samples = {

    "nHad":("../28_May_Root_Files/Had_Data","btag_morethanzero_","Data","Had"),
    
     "mcHadW1":("../28_May_Root_Files/Had_WJets","btag_morethanzero_","WJetsInc","Had"),
     "mcHadttbar":("../28_May_Root_Files/Had_TTbar","btag_morethanzero_","TTbar","Had"),
     "mcHadzinv":("../28_May_Root_Files/Had_Zinv","btag_morethanzero_","Zinv50","Had"),
     "mcHadsingt":("../28_May_Root_Files/Had_SingleTop","btag_morethanzero_","Single_Tbar_t","Had"),
     "mcHaddiboson":("../28_May_Root_Files/Had_DiBoson","btag_morethanzero_","ZZ","Had"),
     "mcHadDY":("../28_May_Root_Files/Had_DY","btag_morethanzero_","DY","Had"),


    "nMuon":("../28_May_Root_Files/Muon_Data","btag_morethanzero_OneMuon_","Data","Muon"),
    
     "mcMuonW1":("../28_May_Root_Files/Muon_WJets","btag_morethanzero_OneMuon_","WJetsInc","Muon"),
     "mcMuonttbar":("../28_May_Root_Files/Muon_TTbar","btag_morethanzero_OneMuon_","TTbar","Muon"),
     "mcMuonzinv":("../28_May_Root_Files/Muon_Zinv","btag_morethanzero_OneMuon_","Zinv50","Muon"),
     "mcMuonsingt":("../28_May_Root_Files/Muon_SingleTop","btag_morethanzero_OneMuon_","Single_Tbar_t","Muon"),
     "mcMuondiboson":("../28_May_Root_Files/Muon_DiBoson","btag_morethanzero_OneMuon_","ZZ","Muon"),
     "mcMuonDY":("../28_May_Root_Files/Muon_DY","btag_morethanzero_OneMuon_","DY","Muon"),


    "nDiMuon":("../28_May_Root_Files/Muon_Data","btag_morethanzero_DiMuon_","Data","DiMuon"),
    
     "mcDiMuonW1":("../28_May_Root_Files/Muon_WJets","btag_morethanzero_DiMuon_","WJetsInc","DiMuon"),
     "mcDiMuonttbar":("../28_May_Root_Files/Muon_TTbar","btag_morethanzero_DiMuon_","TTbar","DiMuon"),
     "mcDiMuonzinv":("../28_May_Root_Files/Muon_Zinv","btag_morethanzero_DiMuon_","Zinv50","DiMuon"),
     "mcDiMuonsingt":("../28_May_Root_Files/Muon_SingleTop","btag_morethanzero_DiMuon_","Single_Tbar_t","DiMuon"),
     "mcDiMuondiboson":("../28_May_Root_Files/Muon_DiBoson","btag_morethanzero_DiMuon_","ZZ","DiMuon"),
     "mcDiMuonDY":("../28_May_Root_Files/Muon_DY","btag_morethanzero_DiMuon_","DY","DiMuon"),


    }


btag_more_than_one_samples = {

    "nHad":("../28_May_Root_Files/Had_Data","btag_morethanone_","Data","Had"),
    
     "mcHadW1":("../28_May_Root_Files/Had_WJets","btag_morethanone_","WJetsInc","Had"),
     "mcHadttbar":("../28_May_Root_Files/Had_TTbar","btag_morethanone_","TTbar","Had"),
     "mcHadzinv":("../28_May_Root_Files/Had_Zinv","btag_morethanone_","Zinv50","Had"),
     "mcHadsingt":("../28_May_Root_Files/Had_SingleTop","btag_morethanone_","Single_Tbar_t","Had"),
     "mcHaddiboson":("../28_May_Root_Files/Had_DiBoson","btag_morethanone_","ZZ","Had"),
     "mcHadDY":("../28_May_Root_Files/Had_DY","btag_morethanone_","DY","Had"),


    "nMuon":("../28_May_Root_Files/Muon_Data","btag_morethanone_OneMuon_","Data","Muon"),
    
     "mcMuonW1":("../28_May_Root_Files/Muon_WJets","btag_morethanone_OneMuon_","WJetsInc","Muon"),
     "mcMuonttbar":("../28_May_Root_Files/Muon_TTbar","btag_morethanone_OneMuon_","TTbar","Muon"),
     "mcMuonzinv":("../28_May_Root_Files/Muon_Zinv","btag_morethanone_OneMuon_","Zinv50","Muon"),
     "mcMuonsingt":("../28_May_Root_Files/Muon_SingleTop","btag_morethanone_OneMuon_","Single_Tbar_t","Muon"),
     "mcMuondiboson":("../28_May_Root_Files/Muon_DiBoson","btag_morethanone_OneMuon_","ZZ","Muon"),
     "mcMuonDY":("../28_May_Root_Files/Muon_DY","btag_morethanone_OneMuon_","DY","Muon"),


    "nDiMuon":("../28_May_Root_Files/Muon_Data","btag_morethanone_DiMuon_","Data","DiMuon"),
    
     "mcDiMuonW1":("../28_May_Root_Files/Muon_WJets","btag_morethanone_DiMuon_","WJetsInc","DiMuon"),
     "mcDiMuonttbar":("../28_May_Root_Files/Muon_TTbar","btag_morethanone_DiMuon_","TTbar","DiMuon"),
     "mcDiMuonzinv":("../28_May_Root_Files/Muon_Zinv","btag_morethanone_DiMuon_","Zinv50","DiMuon"),
     "mcDiMuonsingt":("../28_May_Root_Files/Muon_SingleTop","btag_morethanone_DiMuon_","Single_Tbar_t","DiMuon"),
     "mcDiMuondiboson":("../28_May_Root_Files/Muon_DiBoson","btag_morethanone_DiMuon_","ZZ","DiMuon"),
     "mcDiMuonDY":("../28_May_Root_Files/Muon_DY","btag_morethanone_DiMuon_","DY","DiMuon"),


    }




inclusive_samples = {

    "nHad":("../28_May_Root_Files/Had_Data","","Data","Had"),
    
     "mcHadW1":("../28_May_Root_Files/Had_WJets","","WJetsInc","Had"),
     "mcHadttbar":("../28_May_Root_Files/Had_TTbar","","TTbar","Had"),
     "mcHadzinv":("../28_May_Root_Files/Had_Zinv","","Zinv50","Had"),
     "mcHadsingt":("../28_May_Root_Files/Had_SingleTop","","Single_Tbar_t","Had"),
     "mcHaddiboson":("../28_May_Root_Files/Had_DiBoson","","ZZ","Had"),
     "mcHadDY":("../28_May_Root_Files/Had_DY","","DY","Had"),


    "nMuon":("../28_May_Root_Files/Muon_Data","OneMuon_","Data","Muon"),
    
     "mcMuonW1":("../28_May_Root_Files/Muon_WJets","OneMuon_","WJetsInc","Muon"),
     "mcMuonttbar":("../28_May_Root_Files/Muon_TTbar","OneMuon_","TTbar","Muon"),
     "mcMuonzinv":("../28_May_Root_Files/Muon_Zinv","OneMuon_","Zinv50","Muon"),
     "mcMuonsingt":("../28_May_Root_Files/Muon_SingleTop","OneMuon_","Single_Tbar_t","Muon"),
     "mcMuondiboson":("../28_May_Root_Files/Muon_DiBoson","OneMuon_","ZZ","Muon"),
     "mcMuonDY":("../28_May_Root_Files/Muon_DY","OneMuon_","DY","Muon"),


    "nDiMuon":("../28_May_Root_Files/Muon_Data","DiMuon_","Data","DiMuon"),
    
     "mcDiMuonW1":("../28_May_Root_Files/Muon_WJets","DiMuon_","WJetsInc","DiMuon"),
     "mcDiMuonttbar":("../28_May_Root_Files/Muon_TTbar","DiMuon_","TTbar","DiMuon"),
     "mcDiMuonzinv":("../28_May_Root_Files/Muon_Zinv","DiMuon_","Zinv50","DiMuon"),
     "mcDiMuonsingt":("../28_May_Root_Files/Muon_SingleTop","DiMuon_","Single_Tbar_t","DiMuon"),
     "mcDiMuondiboson":("../28_May_Root_Files/Muon_DiBoson","DiMuon_","ZZ","DiMuon"),
     "mcDiMuonDY":("../28_May_Root_Files/Muon_DY","DiMuon_","DY","DiMuon"),


    }


calc_file = {
     "mchad":("../28_May_Root_Files/Had_MC.root","Had",""),
     "mchadzinv":("../28_May_Root_Files/Had_Zinv.root","Had_Zinv",""),
     "mcmuon":("../28_May_Root_Files/Muon_MC.root","Muon","OneMuon_"),
     "mcdimuon":("../28_May_Root_Files/Muon_MC.root","DiMuon","DiMuon_"),

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
  #a = Number_Extractor(settings,btag_two_samples,"Two_btags",c_file = LIST_FOR_JAD,Closure = "True",Triggers = "True",AlphaT="True",)
  b = Number_Extractor(settings,btag_one_samples,"One_btag",c_file = LIST_FOR_JAD,Closure = "True",Triggers = "True",AlphaT="True",)
  c = Number_Extractor(settings,btag_zero_samples,"Zero_btags",c_file = LIST_FOR_JAD,Closure = "True",Triggers = "True",AlphaT="True",)
  #d = Number_Extractor(settings,btag_more_than_two_samples,"More_Than_Two_btag",c_file = LIST_FOR_JAD,Closure = "True",Triggers = "True",AlphaT="True",)
  e  = Number_Extractor(settings,btag_more_than_zero_samples,"More_Than_Zero_btag",c_file = LIST_FOR_JAD,Closure = "True",Triggers = "True",AlphaT="True",)
  f  = Number_Extractor(settings,btag_more_than_one_samples,"More_Than_One_btag",c_file = LIST_FOR_JAD,Closure = "True",Triggers = "True",AlphaT="True",)
  g  = Number_Extractor(settings,inclusive_samples,"Inclusive",c_file = LIST_FOR_JAD,Closure = "True",Triggers = "True",AlphaT="True",)
  h = Jad_Compute(LIST_FOR_JAD,Lumo = settings["Lumo"])
