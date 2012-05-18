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
  "Lumo":4.65 
  #"AlphaTSlices":["0.55_10"]
      }

samples = {
    "nMuon":("./Root_Files/Muon_Data","OneMuon_","Data","Muon"),
    
    #Muon MC
     "mcMuonW1":("./Root_Files/Muon_WJetsInc","OneMuon_","WJetsInc","Muon"),
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
     "mcDimuonW1":("./Root_Files/Muon_WJetsInc","DiMuon_","WJetsInc","DiMuon"),
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

btag_zero_samples = {

    "nMuon_btag":("./Root_Files/Muon_Data","btag_zero_OneMuon_","Data","Muon"),

    #Muon MC
     "mcMuonW1_btag":("./Root_Files/Muon_WJetsInc","btag_zero_OneMuon_","WJetsInc","Muon"),
     "mcMuonW2_btag":("./Root_Files/Muon_WJets250","btag_zero_OneMuon_","WJets250","Muon"),
     "mcMuonW3_btag":("./Root_Files/Muon_WJets300","btag_zero_OneMuon_","WJets300","Muon"),
     "mcMuonTtw_btag":("./Root_Files/Muon_TTbar","btag_zero_OneMuon_","TTbar","Muon"),
     "mcMuonZ1_btag":("./Root_Files/Muon_Zinv50","btag_zero_OneMuon_","Zinv50","Muon"),
     "mcMuonZ2_btag":("./Root_Files/Muon_Zinv100","btag_zero_OneMuon_","Zinv100","Muon"),
     "mcMuonZ3_btag":("./Root_Files/Muon_Zinv200","btag_zero_OneMuon_","Zinv200","Muon"),
     "mcMuonDY_btag":("./Root_Files/Muon_DY","btag_zero_OneMuon_","DY","Muon"),
     "mcMuon_Singt_btag":("./Root_Files/Muon_Single_T_t","btag_zero_OneMuon_","Single_T_t","Muon"),
     "mcMuon_SingtW_btag":("./Root_Files/Muon_Single_T_tW","btag_zero_OneMuon_","Single_T_tW","Muon"),
     "mcMuon_Singtbar_t_btag":("./Root_Files/Muon_Single_Tbar_t","btag_zero_OneMuon_","Single_Tbar_t","Muon"),
     "mcMuon_Singtbar_tw_btag":("./Root_Files/Muon_Single_Tbar_tW","btag_zero_OneMuon_","Single_Tbar_tW","Muon"),
     "mcMuonZZ_btag":("./Root_Files/Muon_ZZ","btag_zero_OneMuon_","ZZ","Muon"),
     "mcMuonWW_btag":("./Root_Files/Muon_WW","btag_zero_OneMuon_","WW","Muon"),
     "mcMuonWZ_btag":("./Root_Files/Muon_WZ","btag_zero_OneMuon_","WZ","Muon"),

    "nDimuon_btag":("./Root_Files/Muon_Data","btag_zero_DiMuon_","Data","DiMuon"),

    #Muon MC
     "mcDimuonW1_btag":("./Root_Files/Muon_WJetsInc","btag_zero_DiMuon_","WJetsInc","DiMuon"),
     "mcDimuonW2_btag":("./Root_Files/Muon_WJets250","btag_zero_DiMuon_","WJets250","DiMuon"),
     "mcDimuonW3_btag":("./Root_Files/Muon_WJets300","btag_zero_DiMuon_","WJets300","DiMuon"),
     "mcDimuonTtw_btag":("./Root_Files/Muon_TTbar","btag_zero_DiMuon_","TTbar","DiMuon"),
     "mcDimuonZ1_btag":("./Root_Files/Muon_Zinv50","btag_zero_DiMuon_","Zinv50","DiMuon"),
     "mcDimuonZ2_btag":("./Root_Files/Muon_Zinv100","btag_zero_DiMuon_","Zinv100","DiMuon"),
     "mcDimuonZ3_btag":("./Root_Files/Muon_Zinv200","btag_zero_DiMuon_","Zinv200","DiMuon"),
     "mcDimuonDY_btag":("./Root_Files/Muon_DY","btag_zero_DiMuon_","DY","DiMuon"),
     "mcDimuon_Singt_btag":("./Root_Files/Muon_Single_T_t","btag_zero_DiMuon_","Single_T_t","DiMuon"),
     "mcDimuon_SingtW_btag":("./Root_Files/Muon_Single_T_tW","btag_zero_DiMuon_","Single_T_tW","DiMuon"),
     "mcDimuon_Singtbar_t_btag":("./Root_Files/Muon_Single_Tbar_t","btag_zero_DiMuon_","Single_Tbar_t","DiMuon"),
     "mcDimuon_Singtbar_tw_btag":("./Root_Files/Muon_Single_Tbar_tW","btag_zero_DiMuon_","Single_Tbar_tW","DiMuon"),
     "mcDimuonZZ_btag":("./Root_Files/Muon_ZZ","btag_zero_DiMuon_","ZZ","DiMuon"),
     "mcDimuonWW_btag":("./Root_Files/Muon_WW","btag_zero_DiMuon_","WW","DiMuon"),
     "mcDimuonWZ_btag":("./Root_Files/Muon_WZ","btag_zero_DiMuon_","WZ","DiMuon"),

    }                    



btag_morethan_zero_samples = {

    "nMuon_btag":("./Root_Files/Muon_Data","btag_morethanzero_OneMuon_","Data","Muon"),

    #Muon MC
     "mcMuonW1_btag":("./Root_Files/Muon_WJetsInc","btag_morethanzero_OneMuon_","WJetsInc","Muon"),
     "mcMuonW2_btag":("./Root_Files/Muon_WJets250","btag_morethanzero_OneMuon_","WJets250","Muon"),
     "mcMuonW3_btag":("./Root_Files/Muon_WJets300","btag_morethanzero_OneMuon_","WJets300","Muon"),
     "mcMuonTtw_btag":("./Root_Files/Muon_TTbar","btag_morethanzero_OneMuon_","TTbar","Muon"),
     "mcMuonZ1_btag":("./Root_Files/Muon_Zinv50","btag_morethanzero_OneMuon_","Zinv50","Muon"),
     "mcMuonZ2_btag":("./Root_Files/Muon_Zinv100","btag_morethanzero_OneMuon_","Zinv100","Muon"),
     "mcMuonZ3_btag":("./Root_Files/Muon_Zinv200","btag_morethanzero_OneMuon_","Zinv200","Muon"),
     "mcMuonDY_btag":("./Root_Files/Muon_DY","btag_morethanzero_OneMuon_","DY","Muon"),
     "mcMuon_Singt_btag":("./Root_Files/Muon_Single_T_t","btag_morethanzero_OneMuon_","Single_T_t","Muon"),
     "mcMuon_SingtW_btag":("./Root_Files/Muon_Single_T_tW","btag_morethanzero_OneMuon_","Single_T_tW","Muon"),
     "mcMuon_Singtbar_t_btag":("./Root_Files/Muon_Single_Tbar_t","btag_morethanzero_OneMuon_","Single_Tbar_t","Muon"),
     "mcMuon_Singtbar_tw_btag":("./Root_Files/Muon_Single_Tbar_tW","btag_morethanzero_OneMuon_","Single_Tbar_tW","Muon"),
     "mcMuonZZ_btag":("./Root_Files/Muon_ZZ","btag_morethanzero_OneMuon_","ZZ","Muon"),
     "mcMuonWW_btag":("./Root_Files/Muon_WW","btag_morethanzero_OneMuon_","WW","Muon"),
     "mcMuonWZ_btag":("./Root_Files/Muon_WZ","btag_morethanzero_OneMuon_","WZ","Muon"),

    "nDimuon_btag":("./Root_Files/Muon_Data","btag_morethanzero_DiMuon_","Data","DiMuon"),

    #Muon MC
     "mcDimuonW1_btag":("./Root_Files/Muon_WJetsInc","btag_morethanzero_DiMuon_","WJetsInc","DiMuon"),
     "mcDimuonW2_btag":("./Root_Files/Muon_WJets250","btag_morethanzero_DiMuon_","WJets250","DiMuon"),
     "mcDimuonW3_btag":("./Root_Files/Muon_WJets300","btag_morethanzero_DiMuon_","WJets300","DiMuon"),
     "mcDimuonTtw_btag":("./Root_Files/Muon_TTbar","btag_morethanzero_DiMuon_","TTbar","DiMuon"),
     "mcDimuonZ1_btag":("./Root_Files/Muon_Zinv50","btag_morethanzero_DiMuon_","Zinv50","DiMuon"),
     "mcDimuonZ2_btag":("./Root_Files/Muon_Zinv100","btag_morethanzero_DiMuon_","Zinv100","DiMuon"),
     "mcDimuonZ3_btag":("./Root_Files/Muon_Zinv200","btag_morethanzero_DiMuon_","Zinv200","DiMuon"),
     "mcDimuonDY_btag":("./Root_Files/Muon_DY","btag_morethanzero_DiMuon_","DY","DiMuon"),
     "mcDimuon_Singt_btag":("./Root_Files/Muon_Single_T_t","btag_morethanzero_DiMuon_","Single_T_t","DiMuon"),
     "mcDimuon_SingtW_btag":("./Root_Files/Muon_Single_T_tW","btag_morethanzero_DiMuon_","Single_T_tW","DiMuon"),
     "mcDimuon_Singtbar_t_btag":("./Root_Files/Muon_Single_Tbar_t","btag_morethanzero_DiMuon_","Single_Tbar_t","DiMuon"),
     "mcDimuon_Singtbar_tw_btag":("./Root_Files/Muon_Single_Tbar_tW","btag_morethanzero_DiMuon_","Single_Tbar_tW","DiMuon"),
     "mcDimuonZZ_btag":("./Root_Files/Muon_ZZ","btag_morethanzero_DiMuon_","ZZ","DiMuon"),
     "mcDimuonWW_btag":("./Root_Files/Muon_WW","btag_morethanzero_DiMuon_","WW","DiMuon"),
     "mcDimuonWZ_btag":("./Root_Files/Muon_WZ","btag_morethanzero_DiMuon_","WZ","DiMuon"),



    }   
btag_one_samples = {

    "nMuon_btag":("./Root_Files/Muon_Data","btag_one_OneMuon_","Data","Muon"),

    #Muon MC
     "mcMuonW1_btag":("./Root_Files/Muon_WJetsInc","btag_one_OneMuon_","WJetsInc","Muon"),
     "mcMuonW2_btag":("./Root_Files/Muon_WJets250","btag_one_OneMuon_","WJets250","Muon"),
     "mcMuonW3_btag":("./Root_Files/Muon_WJets300","btag_one_OneMuon_","WJets300","Muon"),
     "mcMuonTtw_btag":("./Root_Files/Muon_TTbar","btag_one_OneMuon_","TTbar","Muon"),
     "mcMuonZ1_btag":("./Root_Files/Muon_Zinv50","btag_one_OneMuon_","Zinv50","Muon"),
     "mcMuonZ2_btag":("./Root_Files/Muon_Zinv100","btag_one_OneMuon_","Zinv100","Muon"),
     "mcMuonZ3_btag":("./Root_Files/Muon_Zinv200","btag_one_OneMuon_","Zinv200","Muon"),
     "mcMuonDY_btag":("./Root_Files/Muon_DY","btag_one_OneMuon_","DY","Muon"),
     "mcMuon_Singt_btag":("./Root_Files/Muon_Single_T_t","btag_one_OneMuon_","Single_T_t","Muon"),
     "mcMuon_SingtW_btag":("./Root_Files/Muon_Single_T_tW","btag_one_OneMuon_","Single_T_tW","Muon"),
     "mcMuon_Singtbar_t_btag":("./Root_Files/Muon_Single_Tbar_t","btag_one_OneMuon_","Single_Tbar_t","Muon"),
     "mcMuon_Singtbar_tw_btag":("./Root_Files/Muon_Single_Tbar_tW","btag_one_OneMuon_","Single_Tbar_tW","Muon"),
     "mcMuonZZ_btag":("./Root_Files/Muon_ZZ","btag_one_OneMuon_","ZZ","Muon"),
     "mcMuonWW_btag":("./Root_Files/Muon_WW","btag_one_OneMuon_","WW","Muon"),
     "mcMuonWZ_btag":("./Root_Files/Muon_WZ","btag_one_OneMuon_","WZ","Muon"),

    "nDimuon_btag":("./Root_Files/Muon_Data","btag_one_DiMuon_","Data","DiMuon"),

    #Muon MC
     "mcDimuonW1_btag":("./Root_Files/Muon_WJetsInc","btag_one_DiMuon_","WJetsInc","DiMuon"),
     "mcDimuonW2_btag":("./Root_Files/Muon_WJets250","btag_one_DiMuon_","WJets250","DiMuon"),
     "mcDimuonW3_btag":("./Root_Files/Muon_WJets300","btag_one_DiMuon_","WJets300","DiMuon"),
     "mcDimuonTtw_btag":("./Root_Files/Muon_TTbar","btag_one_DiMuon_","TTbar","DiMuon"),
     "mcDimuonZ1_btag":("./Root_Files/Muon_Zinv50","btag_one_DiMuon_","Zinv50","DiMuon"),
     "mcDimuonZ2_btag":("./Root_Files/Muon_Zinv100","btag_one_DiMuon_","Zinv100","DiMuon"),
     "mcDimuonZ3_btag":("./Root_Files/Muon_Zinv200","btag_one_DiMuon_","Zinv200","DiMuon"),
     "mcDimuonDY_btag":("./Root_Files/Muon_DY","btag_one_DiMuon_","DY","DiMuon"),
     "mcDimuon_Singt_btag":("./Root_Files/Muon_Single_T_t","btag_one_DiMuon_","Single_T_t","DiMuon"),
     "mcDimuon_SingtW_btag":("./Root_Files/Muon_Single_T_tW","btag_one_DiMuon_","Single_T_tW","DiMuon"),
     "mcDimuon_Singtbar_t_btag":("./Root_Files/Muon_Single_Tbar_t","btag_one_DiMuon_","Single_Tbar_t","DiMuon"),
     "mcDimuon_Singtbar_tw_btag":("./Root_Files/Muon_Single_Tbar_tW","btag_one_DiMuon_","Single_Tbar_tW","DiMuon"),
     "mcDimuonZZ_btag":("./Root_Files/Muon_ZZ","btag_one_DiMuon_","ZZ","DiMuon"),
     "mcDimuonWW_btag":("./Root_Files/Muon_WW","btag_one_DiMuon_","WW","DiMuon"),
     "mcDimuonWZ_btag":("./Root_Files/Muon_WZ","btag_one_DiMuon_","WZ","DiMuon"),



    }                    


btag_morethan_one_samples = {

    "nMuon_btag":("./Root_Files/Muon_Data","btag_morethanone_OneMuon_","Data","Muon"),

    #Muon MC
     "mcMuonW1_btag":("./Root_Files/Muon_WJetsInc","btag_morethanone_OneMuon_","WJetsInc","Muon"),
     "mcMuonW2_btag":("./Root_Files/Muon_WJets250","btag_morethanone_OneMuon_","WJets250","Muon"),
     "mcMuonW3_btag":("./Root_Files/Muon_WJets300","btag_morethanone_OneMuon_","WJets300","Muon"),
     "mcMuonTtw_btag":("./Root_Files/Muon_TTbar","btag_morethanone_OneMuon_","TTbar","Muon"),
     "mcMuonZ1_btag":("./Root_Files/Muon_Zinv50","btag_morethanone_OneMuon_","Zinv50","Muon"),
     "mcMuonZ2_btag":("./Root_Files/Muon_Zinv100","btag_morethanone_OneMuon_","Zinv100","Muon"),
     "mcMuonZ3_btag":("./Root_Files/Muon_Zinv200","btag_morethanone_OneMuon_","Zinv200","Muon"),
     "mcMuonDY_btag":("./Root_Files/Muon_DY","btag_morethanone_OneMuon_","DY","Muon"),
     "mcMuon_Singt_btag":("./Root_Files/Muon_Single_T_t","btag_morethanone_OneMuon_","Single_T_t","Muon"),
     "mcMuon_SingtW_btag":("./Root_Files/Muon_Single_T_tW","btag_morethanone_OneMuon_","Single_T_tW","Muon"),
     "mcMuon_Singtbar_t_btag":("./Root_Files/Muon_Single_Tbar_t","btag_morethanone_OneMuon_","Single_Tbar_t","Muon"),
     "mcMuon_Singtbar_tw_btag":("./Root_Files/Muon_Single_Tbar_tW","btag_morethanone_OneMuon_","Single_Tbar_tW","Muon"),
     "mcMuonZZ_btag":("./Root_Files/Muon_ZZ","btag_morethanone_OneMuon_","ZZ","Muon"),
     "mcMuonWW_btag":("./Root_Files/Muon_WW","btag_morethanone_OneMuon_","WW","Muon"),
     "mcMuonWZ_btag":("./Root_Files/Muon_WZ","btag_morethanone_OneMuon_","WZ","Muon"),

    "nDimuon_btag":("./Root_Files/Muon_Data","btag_morethanone_DiMuon_","Data","DiMuon"),

    #Muon MC
     "mcDimuonW1_btag":("./Root_Files/Muon_WJetsInc","btag_morethanone_DiMuon_","WJetsInc","DiMuon"),
     "mcDimuonW2_btag":("./Root_Files/Muon_WJets250","btag_morethanone_DiMuon_","WJets250","DiMuon"),
     "mcDimuonW3_btag":("./Root_Files/Muon_WJets300","btag_morethanone_DiMuon_","WJets300","DiMuon"),
     "mcDimuonTtw_btag":("./Root_Files/Muon_TTbar","btag_morethanone_DiMuon_","TTbar","DiMuon"),
     "mcDimuonZ1_btag":("./Root_Files/Muon_Zinv50","btag_morethanone_DiMuon_","Zinv50","DiMuon"),
     "mcDimuonZ2_btag":("./Root_Files/Muon_Zinv100","btag_morethanone_DiMuon_","Zinv100","DiMuon"),
     "mcDimuonZ3_btag":("./Root_Files/Muon_Zinv200","btag_morethanone_DiMuon_","Zinv200","DiMuon"),
     "mcDimuonDY_btag":("./Root_Files/Muon_DY","btag_morethanone_DiMuon_","DY","DiMuon"),
     "mcDimuon_Singt_btag":("./Root_Files/Muon_Single_T_t","btag_morethanone_DiMuon_","Single_T_t","DiMuon"),
     "mcDimuon_SingtW_btag":("./Root_Files/Muon_Single_T_tW","btag_morethanone_DiMuon_","Single_T_tW","DiMuon"),
     "mcDimuon_Singtbar_t_btag":("./Root_Files/Muon_Single_Tbar_t","btag_morethanone_DiMuon_","Single_Tbar_t","DiMuon"),
     "mcDimuon_Singtbar_tw_btag":("./Root_Files/Muon_Single_Tbar_tW","btag_morethanone_DiMuon_","Single_Tbar_tW","DiMuon"),
     "mcDimuonZZ_btag":("./Root_Files/Muon_ZZ","btag_morethanone_DiMuon_","ZZ","DiMuon"),
     "mcDimuonWW_btag":("./Root_Files/Muon_WW","btag_morethanone_DiMuon_","WW","DiMuon"),
     "mcDimuonWZ_btag":("./Root_Files/Muon_WZ","btag_morethanone_DiMuon_","WZ","DiMuon"),



    }   


btag_two_samples = {

    "nMuon_btag":("./Root_Files/Muon_Data","btag_two_OneMuon_","Data","Muon"),

    #Muon MC
     "mcMuonW1_btag":("./Root_Files/Muon_WJetsInc","btag_two_OneMuon_","WJetsInc","Muon"),
     "mcMuonW2_btag":("./Root_Files/Muon_WJets250","btag_two_OneMuon_","WJets250","Muon"),
     "mcMuonW3_btag":("./Root_Files/Muon_WJets300","btag_two_OneMuon_","WJets300","Muon"),
     "mcMuonTtw_btag":("./Root_Files/Muon_TTbar","btag_two_OneMuon_","TTbar","Muon"),
     "mcMuonZ1_btag":("./Root_Files/Muon_Zinv50","btag_two_OneMuon_","Zinv50","Muon"),
     "mcMuonZ2_btag":("./Root_Files/Muon_Zinv100","btag_two_OneMuon_","Zinv100","Muon"),
     "mcMuonZ3_btag":("./Root_Files/Muon_Zinv200","btag_two_OneMuon_","Zinv200","Muon"),
     "mcMuonDY_btag":("./Root_Files/Muon_DY","btag_two_OneMuon_","DY","Muon"),
     "mcMuon_Singt_btag":("./Root_Files/Muon_Single_T_t","btag_two_OneMuon_","Single_T_t","Muon"),
     "mcMuon_SingtW_btag":("./Root_Files/Muon_Single_T_tW","btag_two_OneMuon_","Single_T_tW","Muon"),
     "mcMuon_Singtbar_t_btag":("./Root_Files/Muon_Single_Tbar_t","btag_two_OneMuon_","Single_Tbar_t","Muon"),
     "mcMuon_Singtbar_tw_btag":("./Root_Files/Muon_Single_Tbar_tW","btag_two_OneMuon_","Single_Tbar_tW","Muon"),
     "mcMuonZZ_btag":("./Root_Files/Muon_ZZ","btag_two_OneMuon_","ZZ","Muon"),
     "mcMuonWW_btag":("./Root_Files/Muon_WW","btag_two_OneMuon_","WW","Muon"),
     "mcMuonWZ_btag":("./Root_Files/Muon_WZ","btag_two_OneMuon_","WZ","Muon"),

    "nDimuon_btag":("./Root_Files/Muon_Data","btag_two_DiMuon_","Data","DiMuon"),

    #Muon MC
     "mcDimuonW1_btag":("./Root_Files/Muon_WJetsInc","btag_two_DiMuon_","WJetsInc","DiMuon"),
     "mcDimuonW2_btag":("./Root_Files/Muon_WJets250","btag_two_DiMuon_","WJets250","DiMuon"),
     "mcDimuonW3_btag":("./Root_Files/Muon_WJets300","btag_two_DiMuon_","WJets300","DiMuon"),
     "mcDimuonTtw_btag":("./Root_Files/Muon_TTbar","btag_two_DiMuon_","TTbar","DiMuon"),
     "mcDimuonZ1_btag":("./Root_Files/Muon_Zinv50","btag_two_DiMuon_","Zinv50","DiMuon"),
     "mcDimuonZ2_btag":("./Root_Files/Muon_Zinv100","btag_two_DiMuon_","Zinv100","DiMuon"),
     "mcDimuonZ3_btag":("./Root_Files/Muon_Zinv200","btag_two_DiMuon_","Zinv200","DiMuon"),
     "mcDimuonDY_btag":("./Root_Files/Muon_DY","btag_two_DiMuon_","DY","DiMuon"),
     "mcDimuon_Singt_btag":("./Root_Files/Muon_Single_T_t","btag_two_DiMuon_","Single_T_t","DiMuon"),
     "mcDimuon_SingtW_btag":("./Root_Files/Muon_Single_T_tW","btag_two_DiMuon_","Single_T_tW","DiMuon"),
     "mcDimuon_Singtbar_t_btag":("./Root_Files/Muon_Single_Tbar_t","btag_two_DiMuon_","Single_Tbar_t","DiMuon"),
     "mcDimuon_Singtbar_tw_btag":("./Root_Files/Muon_Single_Tbar_tW","btag_two_DiMuon_","Single_Tbar_tW","DiMuon"),
     "mcDimuonZZ_btag":("./Root_Files/Muon_ZZ","btag_two_DiMuon_","ZZ","DiMuon"),
     "mcDimuonWW_btag":("./Root_Files/Muon_WW","btag_two_DiMuon_","WW","DiMuon"),
     "mcDimuonWZ_btag":("./Root_Files/Muon_WZ","btag_two_DiMuon_","WZ","DiMuon"),

    }                    


btag_morethan_two_samples = {

    "nMuon_btag":("./Root_Files/Muon_Data","btag_morethantwo_OneMuon_","Data","Muon"),

    #Muon MC
     "mcMuonW1_btag":("./Root_Files/Muon_WJetsInc","btag_morethantwo_OneMuon_","WJetsInc","Muon"),
     "mcMuonW2_btag":("./Root_Files/Muon_WJets250","btag_morethantwo_OneMuon_","WJets250","Muon"),
     "mcMuonW3_btag":("./Root_Files/Muon_WJets300","btag_morethantwo_OneMuon_","WJets300","Muon"),
     "mcMuonTtw_btag":("./Root_Files/Muon_TTbar","btag_morethantwo_OneMuon_","TTbar","Muon"),
     "mcMuonZ1_btag":("./Root_Files/Muon_Zinv50","btag_morethantwo_OneMuon_","Zinv50","Muon"),
     "mcMuonZ2_btag":("./Root_Files/Muon_Zinv100","btag_morethantwo_OneMuon_","Zinv100","Muon"),
     "mcMuonZ3_btag":("./Root_Files/Muon_Zinv200","btag_morethantwo_OneMuon_","Zinv200","Muon"),
     "mcMuonDY_btag":("./Root_Files/Muon_DY","btag_morethantwo_OneMuon_","DY","Muon"),
     "mcMuon_Singt_btag":("./Root_Files/Muon_Single_T_t","btag_morethantwo_OneMuon_","Single_T_t","Muon"),
     "mcMuon_SingtW_btag":("./Root_Files/Muon_Single_T_tW","btag_morethantwo_OneMuon_","Single_T_tW","Muon"),
     "mcMuon_Singtbar_t_btag":("./Root_Files/Muon_Single_Tbar_t","btag_morethantwo_OneMuon_","Single_Tbar_t","Muon"),
     "mcMuon_Singtbar_tw_btag":("./Root_Files/Muon_Single_Tbar_tW","btag_morethantwo_OneMuon_","Single_Tbar_tW","Muon"),
     "mcMuonZZ_btag":("./Root_Files/Muon_ZZ","btag_morethantwo_OneMuon_","ZZ","Muon"),
     "mcMuonWW_btag":("./Root_Files/Muon_WW","btag_morethantwo_OneMuon_","WW","Muon"),
     "mcMuonWZ_btag":("./Root_Files/Muon_WZ","btag_morethantwo_OneMuon_","WZ","Muon"),

    "nDimuon_btag":("./Root_Files/Muon_Data","btag_morethantwo_DiMuon_","Data","DiMuon"),

    #Muon MC
     "mcDimuonW1_btag":("./Root_Files/Muon_WJetsInc","btag_morethantwo_DiMuon_","WJetsInc","DiMuon"),
     "mcDimuonW2_btag":("./Root_Files/Muon_WJets250","btag_morethantwo_DiMuon_","WJets250","DiMuon"),
     "mcDimuonW3_btag":("./Root_Files/Muon_WJets300","btag_morethantwo_DiMuon_","WJets300","DiMuon"),
     "mcDimuonTtw_btag":("./Root_Files/Muon_TTbar","btag_morethantwo_DiMuon_","TTbar","DiMuon"),
     "mcDimuonZ1_btag":("./Root_Files/Muon_Zinv50","btag_morethantwo_DiMuon_","Zinv50","DiMuon"),
     "mcDimuonZ2_btag":("./Root_Files/Muon_Zinv100","btag_morethantwo_DiMuon_","Zinv100","DiMuon"),
     "mcDimuonZ3_btag":("./Root_Files/Muon_Zinv200","btag_morethantwo_DiMuon_","Zinv200","DiMuon"),
     "mcDimuonDY_btag":("./Root_Files/Muon_DY","btag_morethantwo_DiMuon_","DY","DiMuon"),
     "mcDimuon_Singt_btag":("./Root_Files/Muon_Single_T_t","btag_morethantwo_DiMuon_","Single_T_t","DiMuon"),
     "mcDimuon_SingtW_btag":("./Root_Files/Muon_Single_T_tW","btag_morethantwo_DiMuon_","Single_T_tW","DiMuon"),
     "mcDimuon_Singtbar_t_btag":("./Root_Files/Muon_Single_Tbar_t","btag_morethantwo_DiMuon_","Single_Tbar_t","DiMuon"),
     "mcDimuon_Singtbar_tw_btag":("./Root_Files/Muon_Single_Tbar_tW","btag_morethantwo_DiMuon_","Single_Tbar_tW","DiMuon"),
     "mcDimuonZZ_btag":("./Root_Files/Muon_ZZ","btag_morethantwo_DiMuon_","ZZ","DiMuon"),
     "mcDimuonWW_btag":("./Root_Files/Muon_WW","btag_morethantwo_DiMuon_","WW","DiMuon"),
     "mcDimuonWZ_btag":("./Root_Files/Muon_WZ","btag_morethantwo_DiMuon_","WZ","DiMuon"),

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
  a = Number_Extractor(settings,btag_zero_samples,"Zero_btags",c_file = LIST_FOR_JAD,Closure = "True",AlphaT="True",Triggers="False") 
  b = Number_Extractor(settings,btag_one_samples,"One_btag",c_file = LIST_FOR_JAD,Closure="True",AlphaT="True",Triggers="False")
  #c = Number_Extractor(settings,btag_two_samples,"Two_btags",c_file = LIST_FOR_JAD,Closure="True",AlphaT="True",Triggers="False")
  #d = Number_Extractor(settings,samples,"BaseLine",c_file = LIST_FOR_JAD,Closure="True",AlphaT="True",Triggers="False")
  #e = Number_Extractor(settings,btag_morethan_one_samples,"More_Than_One_btag",c_file = LIST_FOR_JAD,Closure="True",AlphaT="True",Triggers="False")
  #f = Number_Extractor(settings,btag_morethan_two_samples,"More_Than_Two_btag",c_file = LIST_FOR_JAD,Closure="True",AlphaT="True",Triggers="False")
  #g = Number_Extractor(settings,btag_morethan_zero_samples,"More_Than_Zero_btag",c_file = LIST_FOR_JAD,Closure="True",AlphaT="True",Triggers="False")
  h = Jad_Compute(LIST_FOR_JAD,Lumo = settings["Lumo"])
