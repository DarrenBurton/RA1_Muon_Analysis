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
  "Lumo":5.0 
  #"AlphaTSlices":["0.55_10"]
      }

inclusive_samples = {

     "mDiMuon":("../TTbar_NoMET/Had_TTbar_7TeV","","WJetsInc","Had"),
     "mcDiMuonW1":("../TTbar_NoMET/Had_TTbar_8TeV","","TTbar","Had"),
     "mMuon":("../TTbar_NoMET/Muon_TTbar_7TeV","OneMuon_","WJetsInc","Muon"),
     "mcMuonttbar":("../TTbar_NoMET/Muon_TTbar_8TeV","OneMuon_","TTbar","Muon"),
     "mDiMuonittbar":("../TTbar_NoMET/Muon_TTbar_7TeV","DiMuon_","WJetsInc","DiMuon"),
     "mcDiMuonW1ttbar":("../TTbar_NoMET/Muon_TTbar_8TeV","DiMuon_","TTbar","DiMuon"),

    }

btagone_samples = {

     "nDiMuon":("../TTbar_NoMET/Muon_TTbar_7TeV","DiMuon_","WJetsInc","DiMuon"),
     "mcDiMuonW1":("../TTbar_NoMET/Muon_TTbar_8TeV","DiMuon_","TTbar","DiMuon"),
     "nMuon":("../TTbar_NoMET/Muon_TTbar_7TeV","OneMuon_","WJetsInc","Muon"),
     "mcMuonttbar":("../TTbar_NoMET/Muon_TTbar_8TeV","OneMuon_","TTbar","Muon"),

    }


calc_file = {
     "mchad":("../29_May_Vertex_Cuts/Had_MC.root","Had",""),
     "mchadzinv":("../29_May_Vertex_Cuts/Had_Zinv.root","Had_Zinv",""),
     "mcmuon":("../29_May_Vertex_Cuts/Muon_MC.root","Muon","OneMuon_"),
     "mcdimuon":("../29_May_Vertex_Cuts/Muon_MC.root","DiMuon","DiMuon_"),

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
  #g  = Number_Extractor(settings,inclusive_samples,"Inclusive",c_file = LIST_FOR_JAD,Closure = "True",Triggers = "False",AlphaT="True",Calculation=calc_file)
  gb  = Number_Extractor(settings,inclusive_samples,"Inclusive",c_file = LIST_FOR_JAD,Closure = "True",Triggers = "False",AlphaT="True")
  #b = Number_Extractor(settings,btagone_samples,"One_btag",c_file = LIST_FOR_JAD,Closure = "True",Triggers = "False",AlphaT="True",Calculation=calc_file)
  #h = Jad_Compute(LIST_FOR_JAD,Lumo = settings["Lumo"])
