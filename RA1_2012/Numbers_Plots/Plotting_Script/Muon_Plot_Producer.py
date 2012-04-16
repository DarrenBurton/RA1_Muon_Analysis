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
  #"Plots":["JetMultiplicity_all","JetMultiplicityAfterAlphaT_55_all"],
  #"Plots":["AlphaT_all","HT_all","HT_after_alphaT_55_all","Btag_Post_AlphaT_5_55_all"],
  "Plots":["MuPt__all","MuEIso__all","MuTrIso__all","MuHIso__all","MuCso__all","MT__all","EffectiveMass_after_alphaT_55_all","EffectiveMass_all","MHT_all","BiasedDeltaPhi_after_alphaT_55_all","AlphaT_all","AlphaT_Zoomed_all","JetMultiplicity_all","JetMultiplicityAfterAlphaT_55_all","Number_Primary_verticies_after_alphaT_55_all","HT_all","HT_after_alphaT_55_all",  "Btag_Pre_AlphaT_5__all","Btag_Post_AlphaT_5_55_all",],
  "Lumo" : 46.5,
  "Webpage":"btag",
  "Category":"OneMuon",
  "WebBinning":["275_325","325_375","375_475","475_575","575_675","675_775","775_875","875","375_upwards"],
  "Misc":[]
  #"WebBinning":["275_325","325_375","375_475"]
      }

muon_plots = {
     "nMuon":("./PLOT_ROOT_FILES/Muon_Data.root","OneMuon_","Data","Muon","Inclusive"), 
     #"mc1":("./PLOT_ROOT_FILES/Muon_MC.root","OneMuon_","MC Combined","Muon","Inclusive"),
     "mc2":("./PLOT_ROOT_FILES/Muon_WJets.root","OneMuon_","WJets","Muon","Inclusive"),
     "mc3":("./PLOT_ROOT_FILES/Muon_TTbar.root","OneMuon_","TTbar","Muon","Inclusive"),
     "mc4":("./PLOT_ROOT_FILES/Muon_Zinv.root","OneMuon_","Zinv","Muon","Inclusive"),
     "mc5":("./PLOT_ROOT_FILES/Muon_DY.root","OneMuon_","DY","Muon","Inclusive"),
     "mc7":("./PLOT_ROOT_FILES/Muon_DiBoson.root","OneMuon_","Di-Boson","Muon","Inclusive"),
     #"mc8":("./PLOT_ROOT_FILES/Muon_QCD.root","OneMuon_","QCD","Muon","Inclusive"), 
     "mc9":("./PLOT_ROOT_FILES/Muon_SingleT.root","OneMuon_","Single_Top","Muon","Inclusive"),
    
    }

muon_one_btag_plots = {
     "nbMuon":("./PLOT_ROOT_FILES/Muon_Data.root","btag_one_OneMuon_","Data","Muon","One"), 
     #"mcb1":("./PLOT_ROOT_FILES/Muon_MC.root","btag_one_OneMuon_","MC Combined","Muon","One"),
     "mcb2":("./PLOT_ROOT_FILES/Muon_WJets.root","btag_one_OneMuon_","WJets","Muon","One"),
     "mcb3":("./PLOT_ROOT_FILES/Muon_TTbar.root","btag_one_OneMuon_","TTbar","Muon","One"),
     "mcb4":("./PLOT_ROOT_FILES/Muon_Zinv.root","btag_one_OneMuon_","Zinv","Muon","One"),
     "mcb5":("./PLOT_ROOT_FILES/Muon_DY.root","btag_one_OneMuon_","DY","Muon","One"),
     "mcb6":("./PLOT_ROOT_FILES/Muon_SingleT.root","btag_one_OneMuon_","Single_Top","Muon","One"),
     "mcb7":("./PLOT_ROOT_FILES/Muon_DiBoson.root","btag_one_OneMuon_","Di-Boson","Muon","One"),
     #"mcb8":("./PLOT_ROOT_FILES/Muon_QCD.root","btag_one_OneMuon_","QCD","Muon","One"),
        
    }


muon_two_btag_plots = {
     "nbMuon":("./PLOT_ROOT_FILES/Muon_Data.root","btag_two_OneMuon_","Data","Muon","Two"), 
     #"mcb1":("./PLOT_ROOT_FILES/Muon_MC.root","btag_two_OneMuon_","MC Combined","Muon","Two"),
     "mcb2":("./PLOT_ROOT_FILES/Muon_WJets.root","btag_two_OneMuon_","WJets","Muon","Two"),
     "mcb3":("./PLOT_ROOT_FILES/Muon_TTbar.root","btag_two_OneMuon_","TTbar","Muon","Two"),
     "mcb4":("./PLOT_ROOT_FILES/Muon_Zinv.root","btag_two_OneMuon_","Zinv","Muon","Two"),
     "mcb5":("./PLOT_ROOT_FILES/Muon_DY.root","btag_two_OneMuon_","DY","Muon","Two"),
     "mcb6":("./PLOT_ROOT_FILES/Muon_SingleT.root","btag_two_OneMuon_","Single_Top","Muon","Two"),
     "mcb7":("./PLOT_ROOT_FILES/Muon_DiBoson.root","btag_two_OneMuon_","Di-Boson","Muon","Two"), 
     #"mcb8":("./PLOT_ROOT_FILES/Muon_QCD.root","btag_two_OneMuon_","QCD","Muon","Two"),   
    }


muon_zero_btag_plots = {
     "nbMuon":("./PLOT_ROOT_FILES/Muon_Data.root","btag_zero_OneMuon_","Data","Muon","Zero"), 
     #"mcb1":("./PLOT_ROOT_FILES/Muon_MC.root","btag_zero_OneMuon_","MC Combined","Muon","Zero"),
     "mcb2":("./PLOT_ROOT_FILES/Muon_WJets.root","btag_zero_OneMuon_","WJets","Muon","Zero"),
     "mcb3":("./PLOT_ROOT_FILES/Muon_TTbar.root","btag_zero_OneMuon_","TTbar","Muon","Zero"),
     "mcb4":("./PLOT_ROOT_FILES/Muon_Zinv.root","btag_zero_OneMuon_","Zinv","Muon","Zero"),
     "mcb5":("./PLOT_ROOT_FILES/Muon_DY.root","btag_zero_OneMuon_","DY","Muon","Zero"),
     "mcb6":("./PLOT_ROOT_FILES/Muon_SingleT.root","btag_zero_OneMuon_","Single_Top","Muon","Zero"),
     "mcb7":("./PLOT_ROOT_FILES/Muon_DiBoson.root","btag_zero_OneMuon_","Di-Boson","Muon","Zero"),
     #"mcb8":("./PLOT_ROOT_FILES/Muon_QCD.root","btag_zero_OneMuon_","QCD","Muon","Zero"),
        
    }


muon_morethanzero_btag_plots = {
     "nbMuon":("./PLOT_ROOT_FILES/Muon_Data.root","btag_morethanzero_OneMuon_","Data","Muon","Zero"), 
     #"mcb1":("./PLOT_ROOT_FILES/Muon_MC.root","btag_morethanzero_OneMuon_","MC Combined","Muon","Zero"),
     "mcb2":("./PLOT_ROOT_FILES/Muon_WJets.root","btag_morethanzero_OneMuon_","WJets","Muon","Zero"),
     "mcb3":("./PLOT_ROOT_FILES/Muon_TTbar.root","btag_morethanzero_OneMuon_","TTbar","Muon","Zero"),
     "mcb4":("./PLOT_ROOT_FILES/Muon_Zinv.root","btag_morethanzero_OneMuon_","Zinv","Muon","Zero"),
     "mcb5":("./PLOT_ROOT_FILES/Muon_DY.root","btag_morethanzero_OneMuon_","DY","Muon","Zero"),
     "mcb7":("./PLOT_ROOT_FILES/Muon_DiBoson.root","btag_morethanzero_OneMuon_","Di-Boson","Muon","Zero"),
     #"mcb8":("./PLOT_ROOT_FILES/Muon_QCD.root","btag_morethanzero_OneMuon_","QCD","Muon","Zero"), 
     "mcb9":("./PLOT_ROOT_FILES/Muon_SingleT.root","btag_morethanzero_OneMuon_","Single_Top","Muon","Zero"),
    }




if __name__=="__main__":
  a = Plotter(settings,muon_plots,jet_multiplicity = "True")
  b = Plotter(settings,muon_morethanzero_btag_plots,jet_multiplicity = "True")
  c = Plotter(settings,muon_two_btag_plots,jet_multiplicity = "True")
  d = Plotter(settings,muon_zero_btag_plots,jet_multiplicity = "True")
  e = Plotter(settings,muon_one_btag_plots,jet_multiplicity = "True")




  finish = Webpage_Maker(settings["Plots"],settings["WebBinning"],settings["Category"],option=settings["Webpage"])
