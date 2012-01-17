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

def Data_Scaler(htbin,hist):
	  
          return float(hist)
          #Scale_Amount = {"275":float(1/0.9153),"325":float(1/0.9562),"375":float(1/0.9688),"475":float(1/0.9789),"575":1,"675":1,"775":1,"875":1}
          #if htbin in Scale_Amount and Scale_Amount[htbin] != 1:
          #    print "Scaling data due to Trigger efficiency of %s percent " % ((1/Scale_Amount[htbin]) * 100)
          #    return float(Scale_Amount[htbin])*float(hist)
          #else: return float(1.0)

class Number_Extractor(object):

  def __init__(self,sample_settings,sample_list):


    print "\n\nGetting Numbers\n\n"
 
    self.Create_Dictionary(sample_settings,sample_list)
    self.Prediction_Maker(sample_settings,self.return_dict)

  def Create_Dictionary(self,settings,samples):
        
         table_entries = "{" 
         for key,fi in sorted(samples.iteritems()):
           i = 0
           for dir in settings['dirs']:
              for alphat in settings['AlphaTSlices']:
                lower = alphat.split('_')[0]
                higher = alphat.split('_')[1]
                if dir[0:3] not in ["775","875"] and lower == "0.52": continue
                if dir[0:3] not in ["575","675","775","875"] and lower == "0.53": continue
                table_entries += "\t\"%s_%d\"  : "%(key,i)
                i+=1
                table_entries += "{\"HT\":\"%s\","%(dir[0:3])
                for histName in settings['plots']:
                    dir = fi[1]+dir
                    normal =  GetSumHist(File = ["%s.root"%fi[0]], Directories = [dir], Hist = histName, Col = r.kBlack, Norm = None if "n" == key[0] else [4650./100.], LegendText = "nBtag")  
                    normal.HideOverFlow()
                    table_entries +=" \"Yield\": %.3e ,\"SampleType\":\"%s\",\"Category\":\"%s\",\"AlphaT\":%s},\n"%(normal.hObj.Integral(int(float(lower)/0.01),int(float(higher)/0.01)),fi[2],fi[3],lower)
         table_entries +="}"
         self.return_dict = ast.literal_eval(table_entries)
         return self.return_dict

  def Prediction_Maker(self,settings,dict):
    
      self.bins = ('275','325','375','475','575','675','775','875')
      entries = ('Data','Yield','SM_Stat_Error','Muon_Trans','DiMuon_Trans','TotError')
      MC_Weights = {"TTbar":0.00425452,"WJetsInc":0.0666131,"WJets250":0.000450549,"WJets300":0.00102329,"Zinv50":0.00485311,"Zinv100":0.00410382,"Zinv200":0.0013739,"Zmumu":0.00849073,"Photon":1.,"Data":1.}

      for slices in settings['AlphaTSlices']:
        print "Making Predictions for %s" %slices
        self.table = open('Predictions_AlphaT_%s.tex' %slices,'w')

        inhad_zinv = False
        inhad_wjet = False
        indimuon = False
        inmuon = False
        inphoton = False

        self.Had_Yield_Per_Bin = dict.fromkeys(self.bins)
        self.Had_Muon_Yield_Per_Bin = dict.fromkeys(self.bins)
        self.Had_Muon_WJets_Yield_Per_Bin = dict.fromkeys(self.bins)
        self.Had_Muon_TTbar_Yield_Per_Bin = dict.fromkeys(self.bins)
        self.Had_Zmumu_Yield_Per_Bin = dict.fromkeys(self.bins)
        self.Muon_Yield_Per_Bin = dict.fromkeys(self.bins)
        self.Muon_TTbar_Yield_Per_Bin = dict.fromkeys(self.bins)
        self.Muon_WJets_Yield_Per_Bin = dict.fromkeys(self.bins)
        self.DiMuon_Yield_Per_Bin = dict.fromkeys(self.bins)
        self.Photon_Yield_Per_Bin = dict.fromkeys(self.bins)

        dictionaries = [self.Had_Yield_Per_Bin,self.Had_Muon_WJets_Yield_Per_Bin,self.Had_Muon_TTbar_Yield_Per_Bin,self.Had_Muon_Yield_Per_Bin,self.Had_Zmumu_Yield_Per_Bin,self.DiMuon_Yield_Per_Bin,self.Muon_Yield_Per_Bin,self.Muon_TTbar_Yield_Per_Bin,self.Muon_WJets_Yield_Per_Bin,self.Photon_Yield_Per_Bin]
        for dicto in dictionaries:
          for key in self.bins:
            dicto[key] = dict.fromkeys(entries,0)
            dicto[key]['TotError'] = []
        print dict
        for entry,fi in dict.iteritems():
          if str(fi['AlphaT']) != str(slices).split('_')[0] : continue
          Error = 0
          if dict[entry]["Category"] is not "Photon" or  dict[entry]["SampleType"] is "Data": Error = m.sqrt(dict[entry]["Yield"]*float(MC_Weights[dict[entry]["SampleType"]])*46.5)
          else: Error = dict[entry]["Error"]

          if dict[entry]["SampleType"] == "Data":
            if dict[entry]["Category"] == "Had": 
              self.Had_Yield_Per_Bin[dict[entry]["HT"]]["Data"] = Data_Scaler(dict[entry]["HT"],dict[entry]["Yield"])
              self.Had_Muon_Yield_Per_Bin[dict[entry]["HT"]]["Data"] = Data_Scaler(dict[entry]["HT"],dict[entry]["Yield"])
              self.Had_Zmumu_Yield_Per_Bin[dict[entry]["HT"]]["Data"] = Data_Scaler(dict[entry]["HT"],dict[entry]["Yield"])
            if dict[entry]["Category"] == "Muon": self.Muon_Yield_Per_Bin[dict[entry]["HT"]]["Data"] = Data_Scaler(dict[entry]["HT"],dict[entry]["Yield"])
            if dict[entry]["Category"] == "DiMuon": self.DiMuon_Yield_Per_Bin[dict[entry]["HT"]]["Data"] = Data_Scaler(dict[entry]["HT"],dict[entry]["Yield"])
            if dict[entry]["Category"] == "Photon": self.Photon_Yield_Per_Bin[dict[entry]["HT"]]["Data"] = Data_Scaler(dict[entry]["HT"],dict[entry]["Yield"])

          elif dict[entry]["Category"] == "Had" :
              if dict[entry]["SampleType"] == "Zinv50" or dict[entry]["SampleType"] == "Zinv100" or dict[entry]["SampleType"] == "Zinv200": 
                inhad_zinv = True
                self.Had_Zmumu_Yield_Per_Bin[dict[entry]["HT"]]["Yield"] +=  dict[entry]["Yield"]
                self.Had_Zmumu_Yield_Per_Bin[dict[entry]["HT"]]["TotError"].append(Error)
              else:  
                inhad_wjet = True
                if dict[entry]["SampleType"] == "TTbar":
                   self.Had_Muon_TTbar_Yield_Per_Bin[dict[entry]["HT"]]["Yield"] +=  dict[entry]["Yield"]
                   self.Had_Muon_TTbar_Yield_Per_Bin[dict[entry]["HT"]]["TotError"].append(Error)
                else:
                    self.Had_Muon_WJets_Yield_Per_Bin[dict[entry]["HT"]]["Yield"] +=  dict[entry]["Yield"]
                    self.Had_Muon_WJets_Yield_Per_Bin[dict[entry]["HT"]]["TotError"].append(Error)
            
                self.Had_Muon_Yield_Per_Bin[dict[entry]["HT"]]["Yield"] +=  dict[entry]["Yield"]
                self.Had_Muon_Yield_Per_Bin[dict[entry]["HT"]]["TotError"].append(Error)
              
              self.Had_Yield_Per_Bin[dict[entry]["HT"]]["Yield"] +=  dict[entry]["Yield"]
              self.Had_Yield_Per_Bin[dict[entry]["HT"]]["TotError"].append(Error)

          elif dict[entry]["Category"] == "Muon":
              inmuon = True
              self.Muon_Yield_Per_Bin[dict[entry]["HT"]]["Yield"] +=  dict[entry]["Yield"]
              self.Muon_Yield_Per_Bin[dict[entry]["HT"]]["TotError"].append(Error)
              if dict[entry]["SampleType"] == "TTbar":
                   self.Muon_TTbar_Yield_Per_Bin[dict[entry]["HT"]]["Yield"] +=  dict[entry]["Yield"]
                   self.Muon_TTbar_Yield_Per_Bin[dict[entry]["HT"]]["TotError"].append(Error)
              else:
                   self.Muon_WJets_Yield_Per_Bin[dict[entry]["HT"]]["Yield"] +=  dict[entry]["Yield"]
                   self.Muon_WJets_Yield_Per_Bin[dict[entry]["HT"]]["TotError"].append(Error)

          elif dict[entry]["Category"] == "DiMuon":
              indimuon = True
              self.DiMuon_Yield_Per_Bin[dict[entry]["HT"]]["Yield"] +=  dict[entry]["Yield"]
              self.DiMuon_Yield_Per_Bin[dict[entry]["HT"]]["TotError"].append(Error)
          elif dict[entry]["Category"] == "Photon":
              inphoton = True
              self.Photon_Yield_Per_Bin[dict[entry]["HT"]]["Yield"] +=  dict[entry]["Yield"]
              self.Photon_Yield_Per_Bin[dict[entry]["HT"]]["TotError"].append(Error)
        
        for bin in self.Muon_Yield_Per_Bin: 
          for sample in dictionaries: 
            try:  sample[bin]["SM_Stat_Error"] = sqrt(reduce(lambda x,y : x+y,map(lambda x: x*x, sample[bin]["TotError"])))
            except TypeError: pass
        
        if inhad_wjet and indimuon and inmuon and inhad_zinv:
          category = "Combined_SM"
          self.Table_Prep(self.Muon_Yield_Per_Bin,self.Had_Muon_Yield_Per_Bin, comb = self.DiMuon_Yield_Per_Bin, comb_test=self.Had_Zmumu_Yield_Per_Bin)
          self.Produce_Tables(self.Dict_For_Table,category = category, dict2 = self.Combination_Pred_Table)

        if inhad_wjet and inphoton and inmuon and inhad_zinv:
          category = "Combined_SM_Photon"
          self.Table_Prep(self.Muon_Yield_Per_Bin,self.Had_Muon_Yield_Per_Bin, comb = self.Photon_Yield_Per_Bin, comb_test=self.Had_Zmumu_Yield_Per_Bin)
          self.Produce_Tables(self.Dict_For_Table,category = category, dict2 = self.Combination_Pred_Table)

        if inmuon and inhad_zinv and inhad_wjet:
          category = "Total_SM"
          self.Table_Prep(self.Muon_Yield_Per_Bin,self.Had_Yield_Per_Bin)
          self.Produce_Tables(self.Dict_For_Table,category = category,alphat_slice=str(slices))
          self.Ratio_Plots(self.Dict_For_Table,str(slices), category = category)

        if inhad_wjet and inmuon:
          category = "Muon"
          self.Table_Prep(self.Muon_Yield_Per_Bin,self.Had_Muon_Yield_Per_Bin)
          self.Produce_Tables(self.Dict_For_Table,category = category,alphat_slice=str(slices))
          self.Ratio_Plots(self.Dict_For_Table,str(slices), category = category)

        if inphoton and inhad_zinv:
          category = "Photon_Zinv"
          self.Table_Prep(self.Photon_Yield_Per_Bin,self.Had_Zmumu_Yield_Per_Bin)
          self.Produce_Tables(self.Dict_For_Table,category = category,alphat_slice=str(slices))
          self.Ratio_Plots(self.Dict_For_Table,str(slices), category = category)

        if inhad_zinv and indimuon:
          category = "Di_Muon_Zinv"
          self.Table_Prep(self.DiMuon_Yield_Per_Bin,self.Had_Zmumu_Yield_Per_Bin)
          self.Produce_Tables(self.Dict_For_Table,category = category,alphat_slice=str(slices))
          self.Ratio_Plots(self.Dict_For_Table,str(slices), category = category)

        if inmuon and indimuon:
          category = "Di_Muon"
          self.Table_Prep(self.Muon_Yield_Per_Bin,self.DiMuon_Yield_Per_Bin)
          self.Produce_Tables(self.Dict_For_Table,category = category,alphat_slice=str(slices))
          self.Ratio_Plots(self.Dict_For_Table,str(slices), category = category)

        if inphoton and indimuon:
          category = "Photon_DiMuon"
          self.Table_Prep(self.Photon_Yield_Per_Bin,self.DiMuon_Yield_Per_Bin)
          self.Produce_Tables(self.Dict_For_Table,category = category,alphat_slice=str(slices))
          self.Ratio_Plots(self.Dict_For_Table,str(slices), category = category)

        if inphoton and inmuon:
          category = "Photon_Muon"
          self.Table_Prep(self.Photon_Yield_Per_Bin,self.Muon_Yield_Per_Bin)
          self.Produce_Tables(self.Dict_For_Table,category = category,alphat_slice=str(slices))
          self.Ratio_Plots(self.Dict_For_Table,str(slices), category = category)
        
        dictnames = ["self.Had_Yield_Per_Bin","self.Had_Muon_WJets_Yield_Per_Bin","self.Had_Muon_TTbar_Yield_Per_Bin","self.Had_Muon_Yield_Per_Bin","self.Had_Zmumu_Yield_Per_Bin","self.DiMuon_Yield_Per_Bin","self.Muon_Yield_Per_Bin","self.Muon_TTbar_Yield_Per_Bin","self.Muon_WJets_Yield_Per_Bin", "self.Photon_Yield_Per_Bin"]
        
        self.Make_Stats_Table(dictionaries,dictnames,slices)  
    
  def Make_Stats_Table(self,dictnames,filename,alphat):
      
      Data_Yields={"Had":[],"Muon":[],"DiMuon":[],"Photon":[]}
      MC_Yields = {"MuonMC":[],"MuonMCerror":[],"DiMuonMC":[],"DiMuonMCerror":[],"PhotonMC":[],"PhotonMCerror":[],"HadTTwMC":[],"HadTTwMCerror":[],"HadZinvMC":[],"HadZinvMCerror":[]}
      for num,dict in enumerate(dictnames):
        for entry in sorted(dict.iterkeys()):
           if filename[num] == "self.Had_Yield_Per_Bin":Data_Yields["Had"].append(float(dict[entry]["Data"])) 
           if filename[num] == "self.Had_Muon_Yield_Per_Bin":
              MC_Yields["HadTTwMC"].append(dict[entry]["Yield"])
              MC_Yields["HadTTwMCerror"].append(dict[entry]["SM_Stat_Error"])
           if filename[num] == "self.Had_Zmumu_Yield_Per_Bin":
              MC_Yields["HadZinvMC"].append(dict[entry]["Yield"])
              MC_Yields["HadZinvMCerror"].append(dict[entry]["SM_Stat_Error"])
           if filename[num] == "self.Muon_Yield_Per_Bin":
              Data_Yields["Muon"].append(float(dict[entry]["Data"]))
              MC_Yields["MuonMC"].append(dict[entry]["Yield"])
              MC_Yields["MuonMCerror"].append(dict[entry]["SM_Stat_Error"])
           if filename[num] == "self.DiMuon_Yield_Per_Bin":
              Data_Yields["DiMuon"].append(float(dict[entry]["Data"]))
              MC_Yields["DiMuonMC"].append(dict[entry]["Yield"])
              MC_Yields["DiMuonMCerror"].append(dict[entry]["SM_Stat_Error"])
           if filename[num] == "self.Photon_Yield_Per_Bin": 
              Data_Yields["Photon"].append(float(dict[entry]["Data"]))
              MC_Yields["PhotonMC"].append(dict[entry]["Yield"])
              MC_Yields["PhotonMCerror"].append(dict[entry]["SM_Stat_Error"])

      self.stats = open('Stats_%s.txt'%alphat,'w')
      s = ""
      s += "observations\n"
      s += "------------------\n"
      s += "nHad (%s )\n" % [i for i in Data_Yields["Had"]]
      s += "nMuon (%s)\n" % [i for i in Data_Yields["Muon"]]
      s += "nMuMu (%s)\n" %[i for i in Data_Yields["DiMuon"]]
      s += "nPhoton (%s)\n" % [i for i in Data_Yields["Photon"]]
      s += "\n\n"
      s += "mcExpectations\n"
      s += "------------------------\n"
      s += "mcGJets (%s)\n" %[i for i in MC_Yields["PhotonMC"]]
      s += "mcMuon (%s)\n" %[i for i in MC_Yields["MuonMC"]]
      s += "mcTtw (%s)\n" %[i for i in MC_Yields["HadTTwMC"]]
      s += "mcZinv (%s)\n" %[i for i in MC_Yields["HadZinvMC"]]
      s += "mcZmumu (%s)\n" %[i for i in MC_Yields["DiMuonMC"]]
      s += "\n\n"
      s += "mcStatError\n"
      s += "------------------------\n"
      s += "mcGJetsErr (%s)\n" %[i for i in MC_Yields["PhotonMCerror"]]
      s += "mcMuonErr (%s)\n" %[i for i in MC_Yields["MuonMCerror"]]
      s += "mcTtwErr (%s)\n" %[i for i in MC_Yields["HadTTwMCerror"]]
      s += "mcZinvErr (%s)\n" %[i for i in MC_Yields["HadZinvMCerror"]]
      s += "mcZmumuErr (%s)\n" %[i for i in MC_Yields["DiMuonMCerror"]]

      print s
      self.stats.write(s)
      self.stats.close()
      
  def Ratio_Plots(self,dict,slice,category =""):
      c1 = TCanvas() 
      ratio_plot = TH1F("ratio_plot","",8,0,8)
      ratio_plot.GetXaxis().SetTitle("H_{T} (GeV)")
      ratio_plot.GetYaxis().SetTitle("Translation Factor")
      ratio_plot.GetYaxis().SetTitleSize(0.055)
      ratio_plot.GetYaxis().SetTitleOffset(.85)
      ratio_plot.GetXaxis().SetTitleSize(0.05)
      ratio_plot.GetYaxis().SetTitleSize(0.06)
      ratio_plot.SetTitle("%s Sample" %category)
      data_plot = ratio_plot.Clone()
      pred_plot = ratio_plot.Clone()
      RatioTitleEntries = ["275","325","375","475","575","675","775","875"]
      for num,bin in enumerate(sorted(dict.iterkeys())):
        ratio_plot.SetBinContent(num+1,dict[bin]["Trans"])
        ratio_plot.SetBinError(num+1,dict[bin]["Trans_Error"])
        ratio_plot.GetXaxis().SetBinLabel(num+1,RatioTitleEntries[num])
      ratio_plot.SetStats(0)
      ratio_plot.Draw("P")
      c1.SaveAs("%s_Prediction_Traslation_Factor_AlphaT_%s.png" %(category,slice))

      data_plot.GetYaxis().SetTitle("Events")
      for num,bin in enumerate(sorted(dict.iterkeys())):
        data_plot.SetBinContent(num+1,dict[bin]["Data"])
        data_plot.SetBinError(num+1,m.sqrt(dict[bin]["Data"]))
        data_plot.GetXaxis().SetBinLabel(num+1,RatioTitleEntries[num])
        pred_plot.SetBinContent(num+1,dict[bin]["Prediction"])
        pred_plot.SetBinError(num+1,dict[bin]["Pred_Error"])
      pred_plot.SetLineColor(4)
      pred_plot.SetMarkerColor(4)
      data_plot.Draw("P")
      pred_plot.Draw("Psame")
      c1.SaveAs("%s_Prediction_Numbers_AlphaT_%s.png" %(category,slice))

  def Table_Prep(self,control,test,comb="",comb_test=""):

      self.Dict_For_Table = dict.fromkeys(self.bins)
      self.Combination_Pred_Table = dict.fromkeys(self.bins)
      entries = ('Data_Pred','Prediction','Pred_Error','Data','Trans','Trans_Error')
      dictionaries = [self.Dict_For_Table,self.Combination_Pred_Table]

      for dicto in dictionaries:
        for key in self.bins: dicto[key] = dict.fromkeys(entries,0)

      for bin in control: 
          try:
            self.Dict_For_Table[bin]['Trans'] = test[bin]["Yield"]/control[bin]["Yield"]
          except ZeroDivisionError: pass
          try: control_error =  control[bin]["SM_Stat_Error"]/control[bin]["Yield"] 
          except ZeroDivisionError: control_error = 0
          try :test_error =  test[bin]["SM_Stat_Error"]/test[bin]["Yield"] 
          except ZeroDivisionError: test_error = 0
          self.Dict_For_Table[bin]['Trans_Error'] = self.Dict_For_Table[bin]['Trans'] * m.sqrt((control_error*control_error)+(test_error*test_error))
          self.Dict_For_Table[bin]['Data_Pred'] = control[bin]["Data"]
          self.Dict_For_Table[bin]['Prediction'] = control[bin]["Data"]*self.Dict_For_Table[bin]['Trans']
          self.Dict_For_Table[bin]['Data'] = test[bin]["Data"]
          try:self.Dict_For_Table[bin]['Pred_Error'] = self.Dict_For_Table[bin]['Prediction']*m.sqrt((1/self.Dict_For_Table[bin]['Data_Pred'])+((self.Dict_For_Table[bin]['Trans_Error']/self.Dict_For_Table[bin]['Trans'])*(self.Dict_For_Table[bin]['Trans_Error']/self.Dict_For_Table[bin]['Trans'])))
          except ZeroDivisionError: self.Dict_For_Table[bin]['Pred_Error'] = 0

      if comb:
        for bin in control:
          try:self.Combination_Pred_Table[bin]['Trans'] = comb_test[bin]["Yield"]/comb[bin]["Yield"]
          except ZeroDivisionError: pass
          try: control_error =  comb[bin]["SM_Stat_Error"]/comb[bin]["Yield"] 
          except ZeroDivisionError: control_error = 0
          try :test_error =  comb_test[bin]["SM_Stat_Error"]/comb_test[bin]["Yield"] 
          except ZeroDivisionError: test_error = 0
          self.Combination_Pred_Table[bin]['Trans_Error'] = self.Combination_Pred_Table[bin]['Trans'] * m.sqrt((control_error*control_error)+(test_error*test_error))
          self.Combination_Pred_Table[bin]['Data_Pred'] = comb[bin]["Data"]
          self.Combination_Pred_Table[bin]['Prediction'] = comb[bin]["Data"]*self.Combination_Pred_Table[bin]['Trans']
          self.Combination_Pred_Table[bin]['Data'] = comb_test[bin]["Data"]
          try:self.Combination_Pred_Table[bin]['Pred_Error'] = self.Combination_Pred_Table[bin]['Prediction']*m.sqrt((1/self.Combination_Pred_Table[bin]['Data_Pred'])+((self.Combination_Pred_Table[bin]['Trans_Error']/self.Combination_Pred_Table[bin]['Trans'])*(self.Combination_Pred_Table[bin]['Trans_Error']/self.Combination_Pred_Table[bin]['Trans'])))
          except ZeroDivisionError: self.Combination_Pred_Table[bin]['Pred_Error'] = 0


  def Produce_Tables(self,dict,category="",dict2 ="",alphat_slice=""):
      print "\n\nMaking Tables for %s" % category
      
      if category == "Total_SM": self.Latex_Table(dict,caption = "AlphaT: %s Total SM prediction from Muon sample"%alphat_slice, 
            rows = [{"label": r'''Hadronic selection MC''',"entryFunc": self.MakeList(self.Had_Yield_Per_Bin,"Yield","SM_Stat_Error"),"addhline":True},
                    {"label": r'''WJets Had MC''',"entryFunc": self.MakeList(self.Had_Muon_TTbar_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''$t\bar{t}$ Had MC''',"entryFunc": self.MakeList(self.Had_Muon_WJets_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''Zinv Had MC''',"entryFunc": self.MakeList(self.Had_Zmumu_Yield_Per_Bin,"Yield","SM_Stat_Error"),"addhline":True},
                    {"label": r'''$\mu +$ jets selection MC''',         "entryFunc":self.MakeList(self.Muon_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''WJets Muon MC''',"entryFunc": self.MakeList(self.Muon_TTbar_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''$t\bar{t}$ Muon MC''',"entryFunc": self.MakeList(self.Muon_WJets_Yield_Per_Bin,"Yield","SM_Stat_Error"),"addhline":True},
                    {"label": r'''Translation factor ''',                "entryFunc":self.MakeList(dict,"Trans","Trans_Error")},
                    {"label": r'''$\mu +$ jets selection yield data''',       "entryFunc":self.MakeList(dict,"Data_Pred")},
                    {"label":r'''Total SM prediction''', "entryFunc":self.MakeList(dict,"Prediction","Pred_Error")},
                    {"label": r'''Hadronic yield data''',       "entryFunc":self.MakeList(dict,"Data")},])
            
      if category == "Muon": self.Latex_Table(dict,caption = "TTbar + W prediction from Muon sample", 
            rows = [{"label": r'''$t\bar{t}$ + W  Hadronic selection MC''',"entryFunc": self.MakeList(self.Had_Muon_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''$\mu +$ jets selection MC''',         "entryFunc":self.MakeList(self.Muon_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''Translation factor''',                "entryFunc":self.MakeList(dict,"Trans","Trans_Error")},
                    {"label": r'''$\mu +$ jets selection yield data''',       "entryFunc":self.MakeList(dict,"Data_Pred")},
                    {"label":r'''$t\bar{t}$ + W prediction''', "entryFunc":self.MakeList(dict,"Prediction","Pred_Error")},])
            
      if category == "Photon_DiMuon": self.Latex_Table(dict,caption = "Photon to predict DiMuon closure test", 
            rows = [{"label": r'''$\mu\bar{\mu} +$ jets selection MC''',"entryFunc": self.MakeList(self.DiMuon_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r''' $\gamma +$ jets selection MC''',         "entryFunc":self.MakeList(self.Photon_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''Translation factor''',                "entryFunc":self.MakeList(dict,"Trans","Trans_Error")},
                    {"label": r'''$\gamma +$ jets yield data''',       "entryFunc":self.MakeList(dict,"Data_Pred")},
                    {"label":r'''$\mu\bar{\mu} +$ jets  prediction''', "entryFunc":self.MakeList(dict,"Prediction","Pred_Error")},
                    {"label": r'''$\mu\bar{\mu} +$ jets yield data''',       "entryFunc":self.MakeList(dict,"Data")},])

      if category == "Photon_Muon": self.Latex_Table(dict,caption = "Photon to predict Muon closure test", 
            rows = [{"label": r'''$\mu + $jets selection  MC''',"entryFunc": self.MakeList(self.Muon_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''$\gamma+$ jets selection MC''',         "entryFunc":self.MakeList(self.Photon_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''Translation factor''',                "entryFunc":self.MakeList(dict,"Trans","Trans_Error")},
                    {"label": r'''$\gamma +$ jets yield data''',       "entryFunc":self.MakeList(dict,"Data_Pred")},
                    {"label":r'''$\mu + jets$ prediction''', "entryFunc":self.MakeList(dict,"Prediction","Pred_Error")},
                    {"label": r'''$\mu + jets$ yield data''',       "entryFunc":self.MakeList(dict,"Data")},])

      if category == "Di_Muon": self.Latex_Table(dict,caption = "Muon to Predict DiMuon closure test", 
            rows = [{"label": r'''$\mu\bar{\mu} +$ jets selection MC''',"entryFunc": self.MakeList(self.DiMuon_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''$\mu +$ jets selection MC''',         "entryFunc":self.MakeList(self.Muon_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''Translation factor''',                "entryFunc":self.MakeList(dict,"Trans","Trans_Error")},
                    {"label": r'''$\mu +$ jets yield data''',       "entryFunc":self.MakeList(dict,"Data_Pred")},
                    {"label":r'''$\mu\bar{\mu} +$ jets selection  prediction''', "entryFunc":self.MakeList(dict,"Prediction","Pred_Error")},
                    {"label": r'''$\mu\bar{\mu} +$ jets selection yield data''',       "entryFunc":self.MakeList(dict,"Data")},])
     
      if category == "Di_Muon_Zinv": self.Latex_Table(dict,caption = "Zinv prediction from DiMuon sample ", 
            rows = [{"label": r'''Z$\rightarrow\nu\bar{\nu}$ hadronic selection MC''',"entryFunc": self.MakeList(self.Had_Zmumu_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''$\mu\bar{\mu} +$ jets selection MC''',         "entryFunc":self.MakeList(self.DiMuon_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''Translation factor''',                "entryFunc":self.MakeList(dict,"Trans","Trans_Error")},
                    {"label": r'''\mu\bar{\mu} +$ jets selection yield data''',       "entryFunc":self.MakeList(dict,"Data_Pred")},
                    {"label":r'''Z$\rightarrow\nu\bar{\nu}$ prediction''', "entryFunc":self.MakeList(dict,"Prediction","Pred_Error")}])

      if category == "Photon_Zinv": self.Latex_Table(dict,caption = "Zinv prediction from Photon sample", 
            rows = [{"label": r'''Z$\rightarrow\nu\bar{\nu}$ hadronic selection MC''',"entryFunc": self.MakeList(self.Had_Zmumu_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''$\gamma +$ jets selection MC''',         "entryFunc":self.MakeList(self.Photon_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''Translation factor''',                "entryFunc":self.MakeList(dict,"Trans","Trans_Error")},
                    {"label": r'''$\gamma +$ jet selection yield data''',       "entryFunc":self.MakeList(dict,"Data_Pred")},
                    {"label":r'''Z$\rightarrow\nu\bar{\nu}$ prediction''', "entryFunc":self.MakeList(dict,"Prediction","Pred_Error")}])
               
      if category == "Combined_SM": self.Latex_Table(dict,caption = "Total SM Prediction (Muon + DiMuon)", 
            rows = [{"label": r'''t$\bar{t}$ + W prediction from $\mu +$ jets''', "entryFunc":self.MakeList(dict,"Prediction","Pred_Error")},
                    {"label": r'''Z$\rightarrow\nu\bar{\nu}$ prediction from $\mu\mu +$ jets''', "entryFunc":self.MakeList(dict2,"Prediction","Pred_Error")},
                    {"label":r'''Total SM prediction''', "entryFunc":self.MakeList(dict,"Prediction","Pred_Error",combined=dict2)},
                    {"label": r'''Hadronic yield from data''',  "entryFunc":self.MakeList(dict,"Data")},])
                   
      if category == "Combined_SM_Photon": self.Latex_Table(dict,caption = "Total SM Prediction (Muon + Photon)", 
            rows = [{"label": r'''$t\bar{t}$ + W prediction from $\mu +$ jets''', "entryFunc":self.MakeList(dict,"Prediction","Pred_Error")},
                    {"label": r'''$Z\rightarrow\nu\bar{\nu}$ Prediction from $\gamma +$ jets''', "entryFunc":self.MakeList(dict2,"Prediction","Pred_Error")},
                    {"label":r'''Total SM prediction''', "entryFunc":self.MakeList(dict,"Prediction","Pred_Error",combined=dict2)},
                    {"label": r'''Hadronic yield from data''',  "entryFunc":self.MakeList(dict,"Data")},]) 
      
  def MakeList(self,dict,key,error = "",combined = ""):
      List = []
      for entry in sorted(dict.iterkeys()):
        if error: 
          if dict[entry][error] == 0 and dict[entry][key] == 0:List.append('-')
          else: List.append(self.toString("%4.2f" %(dict[entry][key]+combined[entry][key] if combined else dict[entry][key]))+"  $\pm$  "+ self.toString("%4.2f" %(dict[entry][error]+combined[entry][error] if combined else dict[entry][error])))
        else: 
          if dict[entry][key] == 0: List.append('-')
          else: List.append(self.toString("%4.2f" %(dict[entry][key]+combined[entry][key] if combined else dict[entry][key])))  
      return List  
        
  def oneRow(self,label = "", labelWidth = 23, entryList = [], entryWidth = 30, extra = "",addhline = "") :
    s = ""
    s += "\n"+label.ljust(labelWidth)+" & "+" & ".join([(self.toString(entry)).ljust(entryWidth) for entry in entryList])+r"\\ "
    if addhline: s += "\n\hline"
    return s 

  def toString(self,item) :
    if type(item) is float : return str(item)
    else : return str(item)
  
  def Latex_Table(self,dict,rows,caption = ""):
      s = "\n"
      s += r'''\begin{table}[ht!]'''
      s += "\n\caption{%s %s fb$^{-1}$}"%(caption,"4.7")
      s += "\n\label{tab:results-W}"
      s += "\n\centering"
      s += "\n"+r'''\footnotesize'''
      s += "\n\\begin{tabular}{ |c|c|c|c|c| }"
      s += "\n\hline"    
      fullBins = list(sorted(dict.iterkeys())) + ["$\infty$"]
      for subTable in range(2) :
          start = 0 + subTable*len(fullBins)/2
          stop = 1 + (1+subTable)*len(fullBins)/2
          indices = range(start,stop-1)[:len(fullBins)/2]
          bins = fullBins[start:stop]
          if subTable == 1:
            s += "\n\hline"
      	  s += self.oneRow(label ="\scalht Bin (GeV)", entryList = [("%s--%s"%(l, u)) for l,u in zip(bins[:-1], bins[1:])], extra = "[0.5ex]")
          s += "\n\hline" 
          for row in rows:
          	s += self.oneRow(label = row["label"], entryList = (row["entryFunc"][i] for i in indices),entryWidth=row["entryWidth"] if "entryWidth" in row else 30, addhline=True if "addhline" in row else False)      
      s += "\n\hline"
      s += "\n\end{tabular}"
      s += "\n\end{table}"
      s += "\n\n\n\n"
      self.table.write(s)
      print s

#if __name__=="__main__":
#  a = Number_Extractor("Hi","Hi")

