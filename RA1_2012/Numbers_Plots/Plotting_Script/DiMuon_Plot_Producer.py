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
#from plottingUtils import *
from Btag_Plots import *


settings = {
  "dirs":["275_325","325_375","375_475","475_575","575_675","675_775","775_875","875",],
  "AlphaTSlices":["0.52_0.53","0.53_0.55","0.55_10"],
  "Plots":["HT_all","HT_after_alphaT_55_all","AlphaT_all","Btag_Post_AlphaT_5_55_all"],
  #"Plots":["MuPt__all","MuEIso__all","MuTrIso__all","MuHIso__all","MuCso__all","MT__all","EffectiveMass_after_alphaT_55_all","EffectiveMass_all","MHT_all","BiasedDeltaPhi_after_alphaT_55_all","AlphaT_all","AlphaT_Zoomed_all","HT_all","HT_after_alphaT_55_all","JetMultiplicity_all","JetMultiplicityAfterAlphaT_55_all","JetMultiplicityAfterAlphaT_53_all","JetMultiplicityAfterAlphaT_52_all","Number_Primary_verticies_after_alphaT_55_all","Number_Primary_verticies_after_alphaT_53_all","Btag_Pre_AlphaT_4__all","Btag_Pre_AlphaT_5__all","Btag_Post_AlphaT_4_55_all","Btag_Post_AlphaT_5_55_all" ],
  "Lumo" : 46.5,
  "Webpage":"btag",
  "Category":"DiMuon",
  "WebBinning":["275_325","325_375","375_475","475_575","575_675","675_775","775_875","875","375_upwards"],
  #"WebBinning":["275_325","325_375","375_475"]
      }

muon_plots = {
     "nMuon":("./PLOT_ROOT_FILES/Muon_Data.root","DiMuon_","Data","DiMuon","Inclusive"), 
     #"mc1":("./PLOT_ROOT_FILES/Muon_MC.root","DiMuon_","MC Combined","DiMuon","Inclusive"),
     "mc2":("./PLOT_ROOT_FILES/Muon_WJets.root","DiMuon_","WJets","DiMuon","Inclusive"),
     "mc3":("./PLOT_ROOT_FILES/Muon_TTbar.root","DiMuon_","TTbar","DiMuon","Inclusive"),
     "mc4":("./PLOT_ROOT_FILES/Muon_Zinv.root","DiMuon_","Zinv","DiMuon","Inclusive"),
     "mc5":("./PLOT_ROOT_FILES/Muon_DY.root","DiMuon_","DY","DiMuon","Inclusive"),
     "mc6":("./PLOT_ROOT_FILES/Muon_SingleT.root","DiMuon_","Single_Top","DiMuon","Inclusive"),
     "mc7":("./PLOT_ROOT_FILES/Muon_DiBoson.root","DiMuon_","Di-Boson","DiMuon","Inclusive"),
     #"mc8":("./PLOT_ROOT_FILES/Muon_QCD.root","DiMuon_","QCD","DiMuon","Inclusive"),
    
    
    }

muon_one_btag_plots = {
     "nbMuon":("./PLOT_ROOT_FILES/Muon_Data.root","btag_one_DiMuon_","Data","DiMuon","One"), 
     "mcb1":("./PLOT_ROOT_FILES/Muon_MC.root","btag_one_DiMuon_","MC Combined","DiMuon","One"),
     "mcb2":("./PLOT_ROOT_FILES/Muon_WJets.root","btag_one_DiMuon_","WJets","DiMuon","One"),
     "mcb3":("./PLOT_ROOT_FILES/Muon_TTbar.root","btag_one_DiMuon_","TTbar","DiMuon","One"),
     "mcb4":("./PLOT_ROOT_FILES/Muon_Zinv.root","btag_one_DiMuon_","Zinv","DiMuon","One"),
     "mcb5":("./PLOT_ROOT_FILES/Muon_DY.root","btag_one_DiMuon_","DY","DiMuon","One"),
     "mcb6":("./PLOT_ROOT_FILES/Muon_SingleT.root","btag_one_DiMuon_","Single_Top","DiMuon","One"),
     "mcb7":("./PLOT_ROOT_FILES/Muon_DiBoson.root","btag_one_DiMuon_","Di-Boson","DiMuon","One"),
     "mcb8":("./PLOT_ROOT_FILES/Muon_QCD.root","btag_one_DiMuon_","QCD","DiMuon","One"),
        
    }


muon_two_btag_plots = {
     "nbMuon":("./PLOT_ROOT_FILES/Muon_Data.root","btag_two_DiMuon_","Data","DiMuon","Two"), 
     #"mcb1":("./PLOT_ROOT_FILES/Muon_MC.root","btag_two_DiMuon_","MC Combined","DiMuon","Two"),
     "mcb2":("./PLOT_ROOT_FILES/Muon_WJets.root","btag_two_DiMuon_","WJets","DiMuon","Two"),
     "mcb3":("./PLOT_ROOT_FILES/Muon_TTbar.root","btag_two_DiMuon_","TTbar","DiMuon","Two"),
     "mcb4":("./PLOT_ROOT_FILES/Muon_Zinv.root","btag_two_DiMuon_","Zinv","DiMuon","Two"),
     "mcb5":("./PLOT_ROOT_FILES/Muon_DY.root","btag_two_DiMuon_","DY","DiMuon","Two"),
     "mcb6":("./PLOT_ROOT_FILES/Muon_SingleT.root","btag_two_DiMuon_","Single_Top","DiMuon","Two"),
     "mcb7":("./PLOT_ROOT_FILES/Muon_DiBoson.root","btag_two_DiMuon_","Di-Boson","DiMuon","Two"), 
     #"mcb8":("./PLOT_ROOT_FILES/Muon_QCD.root","btag_two_DiMuon_","QCD","DiMuon","Two"),   
    }


muon_zero_btag_plots = {
     "nbMuon":("./PLOT_ROOT_FILES/Muon_Data.root","btag_zero_DiMuon_","Data","DiMuon","Zero"), 
     #"mcb1":("./PLOT_ROOT_FILES/Muon_MC.root","btag_zero_DiMuon_","MC Combined","DiMuon","Zero"),
     "mcb2":("./PLOT_ROOT_FILES/Muon_WJets.root","btag_zero_DiMuon_","WJets","DiMuon","Zero"),
     "mcb3":("./PLOT_ROOT_FILES/Muon_TTbar.root","btag_zero_DiMuon_","TTbar","DiMuon","Zero"),
     "mcb4":("./PLOT_ROOT_FILES/Muon_Zinv.root","btag_zero_DiMuon_","Zinv","DiMuon","Zero"),
     "mcb5":("./PLOT_ROOT_FILES/Muon_DY.root","btag_zero_DiMuon_","DY","DiMuon","Zero"),
     "mcb6":("./PLOT_ROOT_FILES/Muon_SingleT.root","btag_zero_DiMuon_","Single_Top","DiMuon","Zero"),
     "mcb7":("./PLOT_ROOT_FILES/Muon_DiBoson.root","btag_zero_DiMuon_","Di-Boson","DiMuon","Zero"),
     #"mcb8":("./PLOT_ROOT_FILES/Muon_QCD.root","btag_zero_DiMuon_","QCD","DiMuon","Zero"),
        
    }


muon_morethanzero_btag_plots = {
     "nbMuon":("./PLOT_ROOT_FILES/Muon_Data.root","btag_morethanzero_DiMuon_","Data","DiMuon","Zero"), 
     #"mcb1":("./PLOT_ROOT_FILES/Muon_MC.root","btag_morethanzero_DiMuon_","MC Combined","DiMuon","Zero"),
     "mcb2":("./PLOT_ROOT_FILES/Muon_WJets.root","btag_morethanzero_DiMuon_","WJets","DiMuon","Zero"),
     "mcb3":("./PLOT_ROOT_FILES/Muon_TTbar.root","btag_morethanzero_DiMuon_","TTbar","DiMuon","Zero"),
     "mcb4":("./PLOT_ROOT_FILES/Muon_Zinv.root","btag_morethanzero_DiMuon_","Zinv","DiMuon","Zero"),
     "mcb5":("./PLOT_ROOT_FILES/Muon_DY.root","btag_morethanzero_DiMuon_","DY","DiMuon","Zero"),
     "mcb6":("./PLOT_ROOT_FILES/Muon_SingleT.root","btag_morethanzero_DiMuon_","Single_Top","DiMuon","Zero"),
     "mcb7":("./PLOT_ROOT_FILES/Muon_DiBoson.root","btag_morethanzero_DiMuon_","Di-Boson","DiMuon","Zero"),
     #"mcb8":("./PLOT_ROOT_FILES/Muon_QCD.root","btag_morethanzero_DiMuon_","QCD","DiMuon","Zero"),
        
    }


if __name__=="__main__":
  a = Plotter(settings,muon_plots,jet_multiplicity = "True")
  b = Plotter(settings,muon_one_btag_plots,jet_multiplicity = "True")
  c = Plotter(settings,muon_two_btag_plots,jet_multiplicity = "True")
  d = Plotter(settings,muon_morethanzero_btag_plots,jet_multiplicity = "True")



  finish = Webpage_Maker(settings["Plots"],settings["WebBinning"],settings["Category"],option=settings["Webpage"])
