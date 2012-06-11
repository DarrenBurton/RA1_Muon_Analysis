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
  "Lumo":2.4, 
  "Multi_Lumi":{'Had':2.4,'Muon':2.28,'DiMuon':2.28}
  #"AlphaTSlices":["0.55_10"]
      }

btag_two_samples = {

    #"nHad":("../UncorrectMET_ICHEP/Had_Data","btag_two_","Data","Had"),
    
     "mcHadW1":("../UncorrectMET_ICHEP/Had_WJets","","WJetsInc","Had"),
     "mcHadttbar":("../UncorrectMET_ICHEP/Had_TTbar","","TTbar","Had"),
     "mcHadzinv":("../UncorrectMET_ICHEP/Had_Zinv","","Zinv50","Had"),
     "mcHadsingt":("../UncorrectMET_ICHEP/Had_SingleTop","","Single_Tbar_t","Had"),
     #"mcHaddiboson":("../UncorrectMET_ICHEP/Had_DiBoson","","ZZ","Had"),
     "mcHadDY":("../UncorrectMET_ICHEP/Had_DY","","DY","Had"),

    "nMuon":("../UncorrectMET_ICHEP/Muon_Data","btag_two_OneMuon_","Data","Muon"),
    
     "mcMuonW1":("../UncorrectMET_ICHEP/Muon_WJets","OneMuon_","WJetsInc","Muon"),
     "mcMuonttbar":("../UncorrectMET_ICHEP/Muon_TTbar","OneMuon_","TTbar","Muon"),
     #"mcMuonzinv":("../UncorrectMET_ICHEP/Muon_Zinv","OneMuon_","Zinv50","Muon"),
     "mcMuonsingt":("../UncorrectMET_ICHEP/Muon_SingleTop","OneMuon_","Single_Tbar_t","Muon"),
     #"mcMuondiboson":("../UncorrectMET_ICHEP/Muon_DiBoson","OneMuon_","ZZ","Muon"),
     "mcMuonDY":("../UncorrectMET_ICHEP/Muon_DY","OneMuon_","DY","Muon"),


    "nDiMuon":("../UncorrectMET_ICHEP/Muon_Data","btag_two_DiMuon_","Data","DiMuon"),
    
     "mcDiMuonW1":("../UncorrectMET_ICHEP/Muon_WJets","DiMuon_","WJetsInc","DiMuon"),
     "mcDiMuonttbar":("../UncorrectMET_ICHEP/Muon_TTbar","DiMuon_","TTbar","DiMuon"),
     #"mcDiMuonzinv":("../UncorrectMET_ICHEP/Muon_Zinv","DiMuon_","Zinv50","DiMuon"),
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
     #"mcDiMuonzinv":("../UncorrectMET_ICHEP/Muon_Zinv","DiMuon_","Zinv50","DiMuon"),
     "mcDiMuonsingt":("../UncorrectMET_ICHEP/Muon_SingleTop","DiMuon_","Single_Tbar_t","DiMuon"),
     #"mcDiMuondiboson":("../UncorrectMET_ICHEP/Muon_DiBoson","DiMuon_","ZZ","DiMuon"),
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
     #"mcMuonzinv":("../UncorrectMET_ICHEP/Muon_Zinv","OneMuon_","Zinv50","Muon"),
     "mcMuonsingt":("../UncorrectMET_ICHEP/Muon_SingleTop","OneMuon_","Single_Tbar_t","Muon"),
     #"mcMuondiboson":("../UncorrectMET_ICHEP/Muon_DiBoson","OneMuon_","ZZ","Muon"),
     "mcMuonDY":("../UncorrectMET_ICHEP/Muon_DY","OneMuon_","DY","Muon"),


    "nDiMuon":("../UncorrectMET_ICHEP/Muon_Data","btag_zero_DiMuon_","Data","DiMuon"),
    
     "mcDiMuonW1":("../UncorrectMET_ICHEP/Muon_WJets","DiMuon_","WJetsInc","DiMuon"),
     "mcDiMuonttbar":("../UncorrectMET_ICHEP/Muon_TTbar","DiMuon_","TTbar","DiMuon"),
    # "mcDiMuonzinv":("../UncorrectMET_ICHEP/Muon_Zinv","DiMuon_","Zinv50","DiMuon"),
     "mcDiMuonsingt":("../UncorrectMET_ICHEP/Muon_SingleTop","DiMuon_","Single_Tbar_t","DiMuon"),
     #"mcDiMuondiboson":("../UncorrectMET_ICHEP/Muon_DiBoson","DiMuon_","ZZ","DiMuon"),
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
    # "mcMuonzinv":("../UncorrectMET_ICHEP/Muon_Zinv","OneMuon_","Zinv50","Muon"),
     "mcMuonsingt":("../UncorrectMET_ICHEP/Muon_SingleTop","OneMuon_","Single_Tbar_t","Muon"),
    # "mcMuondiboson":("../UncorrectMET_ICHEP/Muon_DiBoson","OneMuon_","ZZ","Muon"),
     "mcMuonDY":("../UncorrectMET_ICHEP/Muon_DY","OneMuon_","DY","Muon"),


    "nDiMuon":("../UncorrectMET_ICHEP/Muon_Data","btag_morethantwo_DiMuon_","Data","DiMuon"),
    
     "mcDiMuonW1":("../UncorrectMET_ICHEP/Muon_WJets","DiMuon_","WJetsInc","DiMuon"),
     "mcDiMuonttbar":("../UncorrectMET_ICHEP/Muon_TTbar","DiMuon_","TTbar","DiMuon"),
    # "mcDiMuonzinv":("../UncorrectMET_ICHEP/Muon_Zinv","DiMuon_","Zinv50","DiMuon"),
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
    # "mcHaddiboson":("../UncorrectMET_ICHEP/Had_DiBoson","","ZZ","Had"),
     "mcHadDY":("../UncorrectMET_ICHEP/Had_DY","","DY","Had"),


    "nMuon":("../UncorrectMET_ICHEP/Muon_Data","btag_morethanzero_OneMuon_","Data","Muon"),
    
     "mcMuonW1":("../UncorrectMET_ICHEP/Muon_WJets","OneMuon_","WJetsInc","Muon"),
     "mcMuonttbar":("../UncorrectMET_ICHEP/Muon_TTbar","OneMuon_","TTbar","Muon"),
    # "mcMuonzinv":("../UncorrectMET_ICHEP/Muon_Zinv","OneMuon_","Zinv50","Muon"),
     "mcMuonsingt":("../UncorrectMET_ICHEP/Muon_SingleTop","OneMuon_","Single_Tbar_t","Muon"),
    # "mcMuondiboson":("../UncorrectMET_ICHEP/Muon_DiBoson","OneMuon_","ZZ","Muon"),
     "mcMuonDY":("../UncorrectMET_ICHEP/Muon_DY","OneMuon_","DY","Muon"),


    "nDiMuon":("../UncorrectMET_ICHEP/Muon_Data","btag_morethanzero_DiMuon_","Data","DiMuon"),
    
     "mcDiMuonW1":("../UncorrectMET_ICHEP/Muon_WJets","DiMuon_","WJetsInc","DiMuon"),
     "mcDiMuonttbar":("../UncorrectMET_ICHEP/Muon_TTbar","DiMuon_","TTbar","DiMuon"),
   #  "mcDiMuonzinv":("../UncorrectMET_ICHEP/Muon_Zinv","DiMuon_","Zinv50","DiMuon"),
     "mcDiMuonsingt":("../UncorrectMET_ICHEP/Muon_SingleTop","DiMuon_","Single_Tbar_t","DiMuon"),
    # "mcDiMuondiboson":("../UncorrectMET_ICHEP/Muon_DiBoson","DiMuon_","ZZ","DiMuon"),
     "mcDiMuonDY":("../UncorrectMET_ICHEP/Muon_DY","DiMuon_","DY","DiMuon"),


    }


btag_more_than_one_samples = {

    "nHad":("../UncorrectMET_ICHEP/Had_Data","btag_morethanone_","Data","Had"),
    
     "mcHadW1":("../UncorrectMET_ICHEP/Had_WJets","","WJetsInc","Had"),
     "mcHadttbar":("../UncorrectMET_ICHEP/Had_TTbar","","TTbar","Had"),
     "mcHadzinv":("../UncorrectMET_ICHEP/Had_Zinv","","Zinv50","Had"),
     "mcHadsingt":("../UncorrectMET_ICHEP/Had_SingleTop","","Single_Tbar_t","Had"),
     #"mcHaddiboson":("../UncorrectMET_ICHEP/Had_DiBoson","","ZZ","Had"),
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
    # "mcMuonzinv":("../UncorrectMET_ICHEP/Muon_Zinv","OneMuon_","Zinv50","Muon"),
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
     #"mchadzinv":("../UncorrectMET_ICHEP/Had_Zinv.root","Had_Zinv",""),
     "mchadzinv":("../UncorrectMET_ICHEP/Had_MC.root","Had_Zinv",""),
     "mcmuon":("../UncorrectMET_ICHEP/Muon_MC.root","Muon","OneMuon_"),
     "mcdimuon":("../UncorrectMET_ICHEP/Muon_MC.root","DiMuon","DiMuon_"),

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
  a = Number_Extractor(settings,btag_two_samples,"Two_btags",c_file = LIST_FOR_JAD,Closure = "True",Triggers = "True",AlphaT="True",Calculation=calc_file,Split_Lumi = "True")
  b = Number_Extractor(settings,btag_one_samples,"One_btag",c_file = LIST_FOR_JAD,Closure = "True",Triggers = "True",AlphaT="True",Calculation=calc_file,Split_Lumi = "True")
  c = Number_Extractor(settings,btag_zero_samples,"Zero_btags",c_file = LIST_FOR_JAD,Closure = "True",Triggers = "True",AlphaT="True",Calculation=calc_file,Split_Lumi = "True")
  d = Number_Extractor(settings,btag_more_than_two_samples,"More_Than_Two_btag",c_file = LIST_FOR_JAD,Closure = "True",Triggers = "True",AlphaT="True",Calculation=calc_file,Split_Lumi = "True")
  e  = Number_Extractor(settings,btag_more_than_zero_samples,"More_Than_Zero_btag",c_file = LIST_FOR_JAD,Closure = "True",Triggers = "True",AlphaT="True",Calculation=calc_file,Split_Lumi = "True")
  f  = Number_Extractor(settings,btag_more_than_one_samples,"More_Than_One_btag",c_file = LIST_FOR_JAD,Closure = "True",Triggers = "True",AlphaT="True",Calculation=calc_file,Split_Lumi = "True")
  g  = Number_Extractor(settings,inclusive_samples,"Inclusive",c_file = LIST_FOR_JAD,Closure = "True",Triggers = "True",AlphaT="True",Calculation=calc_file,Split_Lumi = "True")
  h = Jad_Compute(LIST_FOR_JAD,Lumo = settings["Lumo"])
