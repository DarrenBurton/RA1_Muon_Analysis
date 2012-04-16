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


settings = {
  #"dirs":["275_325"],
  "dirs":["275_325","325_375","375_475","475_575","575_675","675_775","775_875","875",],
  "plots":["AlphaT_all",],
  "AlphaTSlices":["0.55_10","0.01_10"],
  "Lumo":4.65
  
  #"AlphaTSlices":["0.55_10"]
      }

samples = {
    "nMuon":("./Root_Files/Muon_Data","OneMuon_","Data","Muon"),
    
    #Muon MC
     #"mcMuonW1":("./Root_Files/Muon_WJetsInc","OneMuon_","WJetsInc","Muon"),
     "mcMuonW2":("./Root_Files/Muon_WJets250","OneMuon_","WJets250","Muon"),
     "mcMuonW3":("./Root_Files/Muon_WJets300","OneMuon_","WJets300","Muon"),
     "mcMuonTtw":("./Root_Files/Muon_TTbar","OneMuon_","TTbar","Muon"),
     "mcMuonZ1":("./Root_Files/Muon_Zinv50","OneMuon_","Zinv50","Muon"),
     "mcMuonZ2":("./Root_Files/Muon_Zinv100","OneMuon_","Zinv100","Muon"),
     "mcMuonZ3":("./Root_Files/Muon_Zinv200","OneMuon_","Zinv200","Muon"),
     "mcMuonDY":("./Root_Files/Muon_DY","OneMuon_","DY","Muon"),
     "mcMuon_Singt":("./Root_Files/Muon_Single_T_t","OneMuon_","Single_T_t","Muon"),
     "mcMuon_SingtW":("./Root_Files/Muon_Single_T_tW","OneMuon_","Single_T_tW","Muon"),
     "mcMuon_Singtbar_t":("./Root_Files/Muon_Single_Tbar_t","OneMuon_","Single_Tbar_t","Muon"),
     "mcMuon_Singtbar_tw":("./Root_Files/Muon_Single_Tbar_tW","OneMuon_","Single_Tbar_tW","Muon"),
     "mcMuonZZ":("./Root_Files/Muon_ZZ","OneMuon_","ZZ","Muon"),
     "mcMuonWW":("./Root_Files/Muon_WW","OneMuon_","WW","Muon"),
     "mcMuonWZ":("./Root_Files/Muon_WZ","OneMuon_","WZ","Muon"),

    "nDimuon":("./Root_Files/Muon_Data","DiMuon_","Data","DiMuon"),
    
    #Muon MC
     #"mcDimuonW1":("./Root_Files/Muon_WJetsInc","DiMuon_","WJetsInc","DiMuon"),
     "mcDimuonW2":("./Root_Files/Muon_WJets250","DiMuon_","WJets250","DiMuon"),
     "mcDimuonW3":("./Root_Files/Muon_WJets300","DiMuon_","WJets300","DiMuon"),
     "mcDimuonTtw":("./Root_Files/Muon_TTbar","DiMuon_","TTbar","DiMuon"),
     "mcDimuonZ1":("./Root_Files/Muon_Zinv50","DiMuon_","Zinv50","DiMuon"),
     "mcDimuonZ2":("./Root_Files/Muon_Zinv100","DiMuon_","Zinv100","DiMuon"),
     "mcDimuonZ3":("./Root_Files/Muon_Zinv200","DiMuon_","Zinv200","DiMuon"),
     "mcDimuonDY":("./Root_Files/Muon_DY","DiMuon_","DY","DiMuon"),
     "mcDimuon_Singt":("./Root_Files/Muon_Single_T_t","DiMuon_","Single_T_t","DiMuon"),
     "mcDimuon_SingtW":("./Root_Files/Muon_Single_T_tW","DiMuon_","Single_T_tW","DiMuon"),
     "mcDimuon_Singtbar_t":("./Root_Files/Muon_Single_Tbar_t","DiMuon_","Single_Tbar_t","DiMuon"),
     "mcDimuon_Singtbar_tw":("./Root_Files/Muon_Single_Tbar_tW","DiMuon_","Single_Tbar_tW","DiMuon"),
     "mcDimuonZZ":("./Root_Files/Muon_ZZ","DiMuon_","ZZ","DiMuon"),
     "mcDimuonWW":("./Root_Files/Muon_WW","DiMuon_","WW","DiMuon"),
     "mcDimuonWZ":("./Root_Files/Muon_WZ","DiMuon_","WZ","DiMuon"),


     

    }



if __name__=="__main__":
  LIST_FOR_JAD = []
  d = Number_Extractor(settings,samples,"BaseLine",c_file = LIST_FOR_JAD,Closure="True",Triggers="True",AlphaT="True")
  h = Jad_Compute(LIST_FOR_JAD,classic="True",Lumo = settings["Lumo"])
