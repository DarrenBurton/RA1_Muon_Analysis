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
  "Lumo":4.98, # Luminosity in fb
  #"AlphaTSlices":["0.55_10"]
      }


'''
Sample Dictionary Instructions

eg "nMuon":("./Root_Files/Muon_Data","btag_two_OneMuon_","Data","Muon"),
if n at start of name entry then the file is data and will no be scaled to luminosity.
first argument is path to root file
second argument is prefix to ht bin. i.e OneMuon_275_325
third argument is data/mc type, i.e. Data, WJets250 - MC relating to the binned WJets 250-300 HT sample
fourth argument is sample Type, Had/DiMuon/Muon. 

the only thing that will have to be changed is the second argument depending on wether you are running btag multiplicity/baseline

baseline = "btag_two_OneMuon_"
0>= btag = "btag_two_OneMuon_"
0 btags = "btag_two_OneMuon_"
etc.....
'''
btag_morethan_two_samples = {
    "nMuon":("./Root_Files/Muon_Data","btag_morethantwo_OneMuon_","Data","Muon"),
    
    #Muon MC
     "mcMuonW1":("./Root_Files/Muon_WJetsInc","btag_morethantwo_OneMuon_","WJetsInc","Muon"),
     "mcMuonW2":("./Root_Files/Muon_WJets250","btag_morethantwo_OneMuon_","WJets250","Muon"),
     "mcMuonW3":("./Root_Files/Muon_WJets300","btag_morethantwo_OneMuon_","WJets300","Muon"),
     "mcMuonTtw":("./Root_Files/Muon_TTbar","btag_morethantwo_OneMuon_","TTbar","Muon"),
     "mcMuonDY":("./Root_Files/Muon_DY","btag_morethantwo_OneMuon_","DY","Muon"),
     "mcMuon_Singt":("./Root_Files/Muon_Single_T_t","btag_morethantwo_OneMuon_","Single_T_t","Muon"),
     "mcMuon_SingtW":("./Root_Files/Muon_Single_T_tW","btag_morethantwo_OneMuon_","Single_T_tW","Muon"),
     "mcMuon_Singtbar_t":("./Root_Files/Muon_Single_Tbar_t","btag_morethantwo_OneMuon_","Single_Tbar_t","Muon"),
     "mcMuon_Singtbar_tw":("./Root_Files/Muon_Single_Tbar_tW","btag_morethantwo_OneMuon_","Single_Tbar_tW","Muon"),
     "mcMuonZZ":("./Root_Files/Muon_ZZ","btag_morethantwo_OneMuon_","ZZ","Muon"),
     "mcMuonWW":("./Root_Files/Muon_WW","btag_morethantwo_OneMuon_","WW","Muon"),
     "mcMuonWZ":("./Root_Files/Muon_WZ","btag_morethantwo_OneMuon_","WZ","Muon"),

    "nDiMuon":("./Root_Files/Muon_Data","btag_morethantwo_DiMuon_","Data","DiMuon"),
    
    #Muon MC
     "mcDiMuonW1":("./Root_Files/Muon_WJetsInc","btag_morethantwo_DiMuon_","WJetsInc","DiMuon"),
     "mcDiMuonW2":("./Root_Files/Muon_WJets250","btag_morethantwo_DiMuon_","WJets250","DiMuon"),
     "mcDiMuonW3":("./Root_Files/Muon_WJets300","btag_morethantwo_DiMuon_","WJets300","DiMuon"),
     "mcDiMuonTtw":("./Root_Files/Muon_TTbar","btag_morethantwo_DiMuon_","TTbar","DiMuon"),
     "mcDiMuonDY":("./Root_Files/Muon_DY","btag_morethantwo_DiMuon_","DY","DiMuon"),
     "mcDiMuon_Singt":("./Root_Files/Muon_Single_T_t","btag_morethantwo_DiMuon_","Single_T_t","DiMuon"),
     "mcDiMuon_SingtW":("./Root_Files/Muon_Single_T_tW","btag_morethantwo_DiMuon_","Single_T_tW","DiMuon"),
     "mcDiMuon_Singtbar_t":("./Root_Files/Muon_Single_Tbar_t","btag_morethantwo_DiMuon_","Single_Tbar_t","DiMuon"),
     "mcDiMuon_Singtbar_tw":("./Root_Files/Muon_Single_Tbar_tW","btag_morethantwo_DiMuon_","Single_Tbar_tW","DiMuon"),
     "mcDiMuonZZ":("./Root_Files/Muon_ZZ","btag_morethantwo_DiMuon_","ZZ","DiMuon"),
     "mcDiMuonWW":("./Root_Files/Muon_WW","btag_morethantwo_DiMuon_","WW","DiMuon"),
     "mcMuonWZ":("./Root_Files/Muon_WZ","btag_morethantwo_DiMuon_","WZ","DiMuon"),

    "nHad":("./Root_Files/Had_Data","btag_morethantwo_","Data","Had"),
    
    #Muon MC
     "mcHadW1":("./Root_Files/Had_WJetsInc","btag_morethantwo_","WJetsInc","Had"),
     "mcHadW2":("./Root_Files/Had_WJets250","btag_morethantwo_","WJets250","Had"),
     "mcHadW3":("./Root_Files/Had_WJets300","btag_morethantwo_","WJets300","Had"),
     "mcHadTtw":("./Root_Files/Had_TTbar","btag_morethantwo_","TTbar","Had"),
     "mcHadZ1":("./Root_Files/Had_Zinv50","btag_morethantwo_","Zinv50","Had"),
     "mcHadZ2":("./Root_Files/Had_Zinv100","btag_morethantwo_","Zinv100","Had"),
     "mcHadZ3":("./Root_Files/Had_Zinv200","btag_morethantwo_","Zinv200","Had"),
     "mcHadDY":("./Root_Files/Had_DY","btag_morethantwo_","DY","Had"),
     "mcHad_Singt":("./Root_Files/Had_Single_T_t","btag_morethantwo_","Single_T_t","Had"),
     "mcHad_SingtW":("./Root_Files/Had_Single_T_tW","btag_morethantwo_","Single_T_tW","Had"),
     "mcHad_Singtbar_t":("./Root_Files/Had_Single_Tbar_t","btag_morethantwo_","Single_Tbar_t","Had"),
     "mcHad_Singtbar_tw":("./Root_Files/Had_Single_Tbar_tW","btag_morethantwo_","Single_Tbar_tW","Had"),
     "mcHadZZ":("./Root_Files/Had_ZZ","btag_morethantwo_","ZZ","Had"),
     "mcHadWW":("./Root_Files/Had_WW","btag_morethantwo_","WW","Had"),
     "mcHadWZ":("./Root_Files/Had_WZ","btag_morethantwo_","WZ","Had"),

    }

btag_morethan_one_samples = {
    "nMuon":("./Root_Files/Muon_Data","btag_morethanone_OneMuon_","Data","Muon"),
    
    #Muon MC
     "mcMuonW1":("./Root_Files/Muon_WJetsInc","btag_morethanone_OneMuon_","WJetsInc","Muon"),
     "mcMuonW2":("./Root_Files/Muon_WJets250","btag_morethanone_OneMuon_","WJets250","Muon"),
     "mcMuonW3":("./Root_Files/Muon_WJets300","btag_morethanone_OneMuon_","WJets300","Muon"),
     "mcMuonTtw":("./Root_Files/Muon_TTbar","btag_morethanone_OneMuon_","TTbar","Muon"),
     "mcMuonDY":("./Root_Files/Muon_DY","btag_morethanone_OneMuon_","DY","Muon"),
     "mcMuon_Singt":("./Root_Files/Muon_Single_T_t","btag_morethanone_OneMuon_","Single_T_t","Muon"),
     "mcMuon_SingtW":("./Root_Files/Muon_Single_T_tW","btag_morethanone_OneMuon_","Single_T_tW","Muon"),
     "mcMuon_Singtbar_t":("./Root_Files/Muon_Single_Tbar_t","btag_morethanone_OneMuon_","Single_Tbar_t","Muon"),
     "mcMuon_Singtbar_tw":("./Root_Files/Muon_Single_Tbar_tW","btag_morethanone_OneMuon_","Single_Tbar_tW","Muon"),
     "mcMuonZZ":("./Root_Files/Muon_ZZ","btag_morethanone_OneMuon_","ZZ","Muon"),
     "mcMuonWW":("./Root_Files/Muon_WW","btag_morethanone_OneMuon_","WW","Muon"),
     "mcMuonWZ":("./Root_Files/Muon_WZ","btag_morethanone_OneMuon_","WZ","Muon"),

    "nDiMuon":("./Root_Files/Muon_Data","btag_morethanone_DiMuon_","Data","DiMuon"),
    
    #Muon MC
     "mcDiMuonW1":("./Root_Files/Muon_WJetsInc","btag_morethanone_DiMuon_","WJetsInc","DiMuon"),
     "mcDiMuonW2":("./Root_Files/Muon_WJets250","btag_morethanone_DiMuon_","WJets250","DiMuon"),
     "mcDiMuonW3":("./Root_Files/Muon_WJets300","btag_morethanone_DiMuon_","WJets300","DiMuon"),
     "mcDiMuonTtw":("./Root_Files/Muon_TTbar","btag_morethanone_DiMuon_","TTbar","DiMuon"),
     "mcDiMuonDY":("./Root_Files/Muon_DY","btag_morethanone_DiMuon_","DY","DiMuon"),
     "mcDiMuon_Singt":("./Root_Files/Muon_Single_T_t","btag_morethanone_DiMuon_","Single_T_t","DiMuon"),
     "mcDiMuon_SingtW":("./Root_Files/Muon_Single_T_tW","btag_morethanone_DiMuon_","Single_T_tW","DiMuon"),
     "mcDiMuon_Singtbar_t":("./Root_Files/Muon_Single_Tbar_t","btag_morethanone_DiMuon_","Single_Tbar_t","DiMuon"),
     "mcDiMuon_Singtbar_tw":("./Root_Files/Muon_Single_Tbar_tW","btag_morethanone_DiMuon_","Single_Tbar_tW","DiMuon"),
     "mcDiMuonZZ":("./Root_Files/Muon_ZZ","btag_morethanone_DiMuon_","ZZ","DiMuon"),
     "mcDiMuonWW":("./Root_Files/Muon_WW","btag_morethanone_DiMuon_","WW","DiMuon"),
     "mcMuonWZ":("./Root_Files/Muon_WZ","btag_morethanone_DiMuon_","WZ","DiMuon"),

    "nHad":("./Root_Files/Had_Data","btag_morethanone_","Data","Had"),
    
    #Muon MC
     "mcHadW1":("./Root_Files/Had_WJetsInc","btag_morethanone_","WJetsInc","Had"),
     "mcHadW2":("./Root_Files/Had_WJets250","btag_morethanone_","WJets250","Had"),
     "mcHadW3":("./Root_Files/Had_WJets300","btag_morethanone_","WJets300","Had"),
     "mcHadTtw":("./Root_Files/Had_TTbar","btag_morethanone_","TTbar","Had"),
     "mcHadZ1":("./Root_Files/Had_Zinv50","btag_morethanone_","Zinv50","Had"),
     "mcHadZ2":("./Root_Files/Had_Zinv100","btag_morethanone_","Zinv100","Had"),
     "mcHadZ3":("./Root_Files/Had_Zinv200","btag_morethanone_","Zinv200","Had"),
     "mcHadDY":("./Root_Files/Had_DY","btag_morethanone_","DY","Had"),
     "mcHad_Singt":("./Root_Files/Had_Single_T_t","btag_morethanone_","Single_T_t","Had"),
     "mcHad_SingtW":("./Root_Files/Had_Single_T_tW","btag_morethanone_","Single_T_tW","Had"),
     "mcHad_Singtbar_t":("./Root_Files/Had_Single_Tbar_t","btag_morethanone_","Single_Tbar_t","Had"),
     "mcHad_Singtbar_tw":("./Root_Files/Had_Single_Tbar_tW","btag_morethanone_","Single_Tbar_tW","Had"),
     "mcHadZZ":("./Root_Files/Had_ZZ","btag_morethanone_","ZZ","Had"),
     "mcHadWW":("./Root_Files/Had_WW","btag_morethanone_","WW","Had"),
     "mcHadWZ":("./Root_Files/Had_WZ","btag_morethanone_","WZ","Had"),

    }

btag_morethan_zero_samples = {
    "nMuon":("./Root_Files/Muon_Data","btag_morethanzero_OneMuon_","Data","Muon"),
    
    #Muon MC
     "mcMuonW1":("./Root_Files/Muon_WJetsInc","btag_morethanzero_OneMuon_","WJetsInc","Muon"),
     "mcMuonW2":("./Root_Files/Muon_WJets250","btag_morethanzero_OneMuon_","WJets250","Muon"),
     "mcMuonW3":("./Root_Files/Muon_WJets300","btag_morethanzero_OneMuon_","WJets300","Muon"),
     "mcMuonTtw":("./Root_Files/Muon_TTbar","btag_morethanzero_OneMuon_","TTbar","Muon"),
     "mcMuonDY":("./Root_Files/Muon_DY","btag_morethanzero_OneMuon_","DY","Muon"),
     "mcMuon_Singt":("./Root_Files/Muon_Single_T_t","btag_morethanzero_OneMuon_","Single_T_t","Muon"),
     "mcMuon_SingtW":("./Root_Files/Muon_Single_T_tW","btag_morethanzero_OneMuon_","Single_T_tW","Muon"),
     "mcMuon_Singtbar_t":("./Root_Files/Muon_Single_Tbar_t","btag_morethanzero_OneMuon_","Single_Tbar_t","Muon"),
     "mcMuon_Singtbar_tw":("./Root_Files/Muon_Single_Tbar_tW","btag_morethanzero_OneMuon_","Single_Tbar_tW","Muon"),
     "mcMuonZZ":("./Root_Files/Muon_ZZ","btag_morethanzero_OneMuon_","ZZ","Muon"),
     "mcMuonWW":("./Root_Files/Muon_WW","btag_morethanzero_OneMuon_","WW","Muon"),
     "mcMuonWZ":("./Root_Files/Muon_WZ","btag_morethanzero_OneMuon_","WZ","Muon"),

    "nDiMuon":("./Root_Files/Muon_Data","btag_morethanzero_DiMuon_","Data","DiMuon"),
    
    #Muon MC
     "mcDiMuonW1":("./Root_Files/Muon_WJetsInc","btag_morethanzero_DiMuon_","WJetsInc","DiMuon"),
     "mcDiMuonW2":("./Root_Files/Muon_WJets250","btag_morethanzero_DiMuon_","WJets250","DiMuon"),
     "mcDiMuonW3":("./Root_Files/Muon_WJets300","btag_morethanzero_DiMuon_","WJets300","DiMuon"),
     "mcDiMuonTtw":("./Root_Files/Muon_TTbar","btag_morethanzero_DiMuon_","TTbar","DiMuon"),
     "mcDiMuonDY":("./Root_Files/Muon_DY","btag_morethanzero_DiMuon_","DY","DiMuon"),
     "mcDiMuon_Singt":("./Root_Files/Muon_Single_T_t","btag_morethanzero_DiMuon_","Single_T_t","DiMuon"),
     "mcDiMuon_SingtW":("./Root_Files/Muon_Single_T_tW","btag_morethanzero_DiMuon_","Single_T_tW","DiMuon"),
     "mcDiMuon_Singtbar_t":("./Root_Files/Muon_Single_Tbar_t","btag_morethanzero_DiMuon_","Single_Tbar_t","DiMuon"),
     "mcDiMuon_Singtbar_tw":("./Root_Files/Muon_Single_Tbar_tW","btag_morethanzero_DiMuon_","Single_Tbar_tW","DiMuon"),
     "mcDiMuonZZ":("./Root_Files/Muon_ZZ","btag_morethanzero_DiMuon_","ZZ","DiMuon"),
     "mcDiMuonWW":("./Root_Files/Muon_WW","btag_morethanzero_DiMuon_","WW","DiMuon"),
     "mcMuonWZ":("./Root_Files/Muon_WZ","btag_morethanzero_DiMuon_","WZ","DiMuon"),

    "nHad":("./Root_Files/Had_Data","btag_morethanzero_","Data","Had"),
    
    #Muon MC
     "mcHadW1":("./Root_Files/Had_WJetsInc","btag_morethanzero_","WJetsInc","Had"),
     "mcHadW2":("./Root_Files/Had_WJets250","btag_morethanzero_","WJets250","Had"),
     "mcHadW3":("./Root_Files/Had_WJets300","btag_morethanzero_","WJets300","Had"),
     "mcHadTtw":("./Root_Files/Had_TTbar","btag_morethanzero_","TTbar","Had"),
     "mcHadZ1":("./Root_Files/Had_Zinv50","btag_morethanzero_","Zinv50","Had"),
     "mcHadZ2":("./Root_Files/Had_Zinv100","btag_morethanzero_","Zinv100","Had"),
     "mcHadZ3":("./Root_Files/Had_Zinv200","btag_morethanzero_","Zinv200","Had"),
     "mcHadDY":("./Root_Files/Had_DY","btag_morethanzero_","DY","Had"),
     "mcHad_Singt":("./Root_Files/Had_Single_T_t","btag_morethanzero_","Single_T_t","Had"),
     "mcHad_SingtW":("./Root_Files/Had_Single_T_tW","btag_morethanzero_","Single_T_tW","Had"),
     "mcHad_Singtbar_t":("./Root_Files/Had_Single_Tbar_t","btag_morethanzero_","Single_Tbar_t","Had"),
     "mcHad_Singtbar_tw":("./Root_Files/Had_Single_Tbar_tW","btag_morethanzero_","Single_Tbar_tW","Had"),
     "mcHadZZ":("./Root_Files/Had_ZZ","btag_morethanzero_","ZZ","Had"),
     "mcHadWW":("./Root_Files/Had_WW","btag_morethanzero_","WW","Had"),
     "mcHadWZ":("./Root_Files/Had_WZ","btag_morethanzero_","WZ","Had"),

    }



btag_zero_samples = {
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


btag_one_samples = {
    "nMuon":("./Root_Files/Muon_Data","btag_one_OneMuon_","Data","Muon"),
    
    #Muon MC
     "mcMuonW1":("./Root_Files/Muon_WJetsInc","btag_one_OneMuon_","WJetsInc","Muon"),
     "mcMuonW2":("./Root_Files/Muon_WJets250","btag_one_OneMuon_","WJets250","Muon"),
     "mcMuonW3":("./Root_Files/Muon_WJets300","btag_one_OneMuon_","WJets300","Muon"),
     "mcMuonTtw":("./Root_Files/Muon_TTbar","btag_one_OneMuon_","TTbar","Muon"),
     "mcMuonDY":("./Root_Files/Muon_DY","btag_one_OneMuon_","DY","Muon"),
     "mcMuon_Singt":("./Root_Files/Muon_Single_T_t","btag_one_OneMuon_","Single_T_t","Muon"),
     "mcMuon_SingtW":("./Root_Files/Muon_Single_T_tW","btag_one_OneMuon_","Single_T_tW","Muon"),
     "mcMuon_Singtbar_t":("./Root_Files/Muon_Single_Tbar_t","btag_one_OneMuon_","Single_Tbar_t","Muon"),
     "mcMuon_Singtbar_tw":("./Root_Files/Muon_Single_Tbar_tW","btag_one_OneMuon_","Single_Tbar_tW","Muon"),
     "mcMuonZZ":("./Root_Files/Muon_ZZ","btag_one_OneMuon_","ZZ","Muon"),
     "mcMuonWW":("./Root_Files/Muon_WW","btag_one_OneMuon_","WW","Muon"),
     "mcMuonWZ":("./Root_Files/Muon_WZ","btag_one_OneMuon_","WZ","Muon"),

    "nDiMuon":("./Root_Files/Muon_Data","btag_one_DiMuon_","Data","DiMuon"),
    
    #Muon MC
     "mcDiMuonW1":("./Root_Files/Muon_WJetsInc","btag_one_DiMuon_","WJetsInc","DiMuon"),
     "mcDiMuonW2":("./Root_Files/Muon_WJets250","btag_one_DiMuon_","WJets250","DiMuon"),
     "mcDiMuonW3":("./Root_Files/Muon_WJets300","btag_one_DiMuon_","WJets300","DiMuon"),
     "mcDiMuonTtw":("./Root_Files/Muon_TTbar","btag_one_DiMuon_","TTbar","DiMuon"),
     "mcDiMuonDY":("./Root_Files/Muon_DY","btag_one_DiMuon_","DY","DiMuon"),
     "mcDiMuon_Singt":("./Root_Files/Muon_Single_T_t","btag_one_DiMuon_","Single_T_t","DiMuon"),
     "mcDiMuon_SingtW":("./Root_Files/Muon_Single_T_tW","btag_one_DiMuon_","Single_T_tW","DiMuon"),
     "mcDiMuon_Singtbar_t":("./Root_Files/Muon_Single_Tbar_t","btag_one_DiMuon_","Single_Tbar_t","DiMuon"),
     "mcDiMuon_Singtbar_tw":("./Root_Files/Muon_Single_Tbar_tW","btag_one_DiMuon_","Single_Tbar_tW","DiMuon"),
     "mcDiMuonZZ":("./Root_Files/Muon_ZZ","btag_one_DiMuon_","ZZ","DiMuon"),
     "mcDiMuonWW":("./Root_Files/Muon_WW","btag_one_DiMuon_","WW","DiMuon"),
     "mcMuonWZ":("./Root_Files/Muon_WZ","btag_one_DiMuon_","WZ","DiMuon"),

    "nHad":("./Root_Files/Had_Data","btag_one_","Data","Had"),
    
    #Muon MC
     "mcHadW1":("./Root_Files/Had_WJetsInc","btag_one_","WJetsInc","Had"),
     "mcHadW2":("./Root_Files/Had_WJets250","btag_one_","WJets250","Had"),
     "mcHadW3":("./Root_Files/Had_WJets300","btag_one_","WJets300","Had"),
     "mcHadTtw":("./Root_Files/Had_TTbar","btag_one_","TTbar","Had"),
     "mcHadZ1":("./Root_Files/Had_Zinv50","btag_one_","Zinv50","Had"),
     "mcHadZ2":("./Root_Files/Had_Zinv100","btag_one_","Zinv100","Had"),
     "mcHadZ3":("./Root_Files/Had_Zinv200","btag_one_","Zinv200","Had"),
     "mcHadDY":("./Root_Files/Had_DY","btag_one_","DY","Had"),
     "mcHad_Singt":("./Root_Files/Had_Single_T_t","btag_one_","Single_T_t","Had"),
     "mcHad_SingtW":("./Root_Files/Had_Single_T_tW","btag_one_","Single_T_tW","Had"),
     "mcHad_Singtbar_t":("./Root_Files/Had_Single_Tbar_t","btag_one_","Single_Tbar_t","Had"),
     "mcHad_Singtbar_tw":("./Root_Files/Had_Single_Tbar_tW","btag_one_","Single_Tbar_tW","Had"),
     "mcHadZZ":("./Root_Files/Had_ZZ","btag_one_","ZZ","Had"),
     "mcHadWW":("./Root_Files/Had_WW","btag_one_","WW","Had"),
     "mcHadWZ":("./Root_Files/Had_WZ","btag_one_","WZ","Had"),

    }



btag_two_samples = {
    "nMuon":("./Root_Files/Muon_Data","btag_two_OneMuon_","Data","Muon"),
    
    #Muon MC
     "mcMuonW1":("./Root_Files/Muon_WJetsInc","btag_two_OneMuon_","WJetsInc","Muon"),
     "mcMuonW2":("./Root_Files/Muon_WJets250","btag_two_OneMuon_","WJets250","Muon"),
     "mcMuonW3":("./Root_Files/Muon_WJets300","btag_two_OneMuon_","WJets300","Muon"),
     "mcMuonTtw":("./Root_Files/Muon_TTbar","btag_two_OneMuon_","TTbar","Muon"),
     "mcMuonDY":("./Root_Files/Muon_DY","btag_two_OneMuon_","DY","Muon"),
     "mcMuon_Singt":("./Root_Files/Muon_Single_T_t","btag_two_OneMuon_","Single_T_t","Muon"),
     "mcMuon_SingtW":("./Root_Files/Muon_Single_T_tW","btag_two_OneMuon_","Single_T_tW","Muon"),
     "mcMuon_Singtbar_t":("./Root_Files/Muon_Single_Tbar_t","btag_two_OneMuon_","Single_Tbar_t","Muon"),
     "mcMuon_Singtbar_tw":("./Root_Files/Muon_Single_Tbar_tW","btag_two_OneMuon_","Single_Tbar_tW","Muon"),
     "mcMuonZZ":("./Root_Files/Muon_ZZ","btag_two_OneMuon_","ZZ","Muon"),
     "mcMuonWW":("./Root_Files/Muon_WW","btag_two_OneMuon_","WW","Muon"),
     "mcMuonWZ":("./Root_Files/Muon_WZ","btag_two_OneMuon_","WZ","Muon"),

    "nDiMuon":("./Root_Files/Muon_Data","btag_two_DiMuon_","Data","DiMuon"),
    
    #Muon MC
     "mcDiMuonW1":("./Root_Files/Muon_WJetsInc","btag_two_DiMuon_","WJetsInc","DiMuon"),
     "mcDiMuonW2":("./Root_Files/Muon_WJets250","btag_two_DiMuon_","WJets250","DiMuon"),
     "mcDiMuonW3":("./Root_Files/Muon_WJets300","btag_two_DiMuon_","WJets300","DiMuon"),
     "mcDiMuonTtw":("./Root_Files/Muon_TTbar","btag_two_DiMuon_","TTbar","DiMuon"),
     "mcDiMuonDY":("./Root_Files/Muon_DY","btag_two_DiMuon_","DY","DiMuon"),
     "mcDiMuon_Singt":("./Root_Files/Muon_Single_T_t","btag_two_DiMuon_","Single_T_t","DiMuon"),
     "mcDiMuon_SingtW":("./Root_Files/Muon_Single_T_tW","btag_two_DiMuon_","Single_T_tW","DiMuon"),
     "mcDiMuon_Singtbar_t":("./Root_Files/Muon_Single_Tbar_t","btag_two_DiMuon_","Single_Tbar_t","DiMuon"),
     "mcDiMuon_Singtbar_tw":("./Root_Files/Muon_Single_Tbar_tW","btag_two_DiMuon_","Single_Tbar_tW","DiMuon"),
     "mcDiMuonZZ":("./Root_Files/Muon_ZZ","btag_two_DiMuon_","ZZ","DiMuon"),
     "mcDiMuonWW":("./Root_Files/Muon_WW","btag_two_DiMuon_","WW","DiMuon"),
     "mcMuonWZ":("./Root_Files/Muon_WZ","btag_two_DiMuon_","WZ","DiMuon"),

    "nHad":("./Root_Files/Had_Data","btag_two_","Data","Had"),
    
    #Muon MC
     "mcHadW1":("./Root_Files/Had_WJetsInc","btag_two_","WJetsInc","Had"),
     "mcHadW2":("./Root_Files/Had_WJets250","btag_two_","WJets250","Had"),
     "mcHadW3":("./Root_Files/Had_WJets300","btag_two_","WJets300","Had"),
     "mcHadTtw":("./Root_Files/Had_TTbar","btag_two_","TTbar","Had"),
     "mcHadZ1":("./Root_Files/Had_Zinv50","btag_two_","Zinv50","Had"),
     "mcHadZ2":("./Root_Files/Had_Zinv100","btag_two_","Zinv100","Had"),
     "mcHadZ3":("./Root_Files/Had_Zinv200","btag_two_","Zinv200","Had"),
     "mcHadDY":("./Root_Files/Had_DY","btag_two_","DY","Had"),
     "mcHad_Singt":("./Root_Files/Had_Single_T_t","btag_two_","Single_T_t","Had"),
     "mcHad_SingtW":("./Root_Files/Had_Single_T_tW","btag_two_","Single_T_tW","Had"),
     "mcHad_Singtbar_t":("./Root_Files/Had_Single_Tbar_t","btag_two_","Single_Tbar_t","Had"),
     "mcHad_Singtbar_tw":("./Root_Files/Had_Single_Tbar_tW","btag_two_","Single_Tbar_tW","Had"),
     "mcHadZZ":("./Root_Files/Had_ZZ","btag_two_","ZZ","Had"),
     "mcHadWW":("./Root_Files/Had_WW","btag_two_","WW","Had"),
     "mcHadWZ":("./Root_Files/Had_WZ","btag_two_","WZ","Had"),

    }


'''
Number_Extractor Instructions

Imported from Bryn_Numbers.py
1st/2nd argument never change, just passing the files to be read in and the parameters to produce numbers
3rd argument is prefix that output files are appeneded with, so if using btag analysis change string to something that reflects this

Additional arguments

Triggers = Apply Trigger Corrections
AlphaT = Keeps AlphaT cut for control samples. Use for baseline/ Jads closure tests which go from no alphaT cut to an alphaT cut
Stats = Make Root Output Stats File for use by Sam/Ted. Doesn't produce output tex tables if True
Trans_Plots = Make 2D histos of yields/Translation factors. Not really important anymore.
'''

if __name__=="__main__":
  a = Number_Extractor(settings,btag_two_samples,"Two_btags",Triggers = "True",AlphaT="False")
  b = Number_Extractor(settings,btag_one_samples,"One_btag",Triggers = "True",AlphaT="False")
  c = Number_Extractor(settings,btag_zero_samples,"Zero_btags",Triggers = "True",AlphaT="False")
  d = Number_Extractor(settings,btag_morethan_zero_samples,"More_Than_Zero_btags",Triggers = "True",AlphaT="False")
  e = Number_Extractor(settings,btag_morethan_one_samples,"More_Than_One_btags",Triggers = "True",AlphaT="False")
  f = Number_Extractor(settings,btag_morethan_two_samples,"More_Than_Two_btags",Triggers = "True",AlphaT="False")
