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



if __name__=="__main__":
  LIST_FOR_JAD = []
  d = Number_Extractor(settings,samples,"BaseLine",c_file = LIST_FOR_JAD,Closure="True",Triggers="False",AlphaT="True")
  h = Jad_Compute(LIST_FOR_JAD,classic="True",Lumo = settings["Lumo"])
