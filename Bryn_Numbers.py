#!/usr/bin/env python
from ROOT import *
import ROOT as r
import logging,itertools
import os,fnmatch,sys
import glob, errno
from time import strftime
from optparse import OptionParser
import array
import math as m

def Data_Scaler(htbin,hist,alphat="",yield_scale="",number_mode="",scale= ""):

      if scale is False: return float(1.0)
      else :
        if yield_scale is "alphat":
          Scale_Amount = {"275_325":{"55":float(1./0.843),"6":float(1/0.88)},"325_375":{"53":float(1/0.893),"55":float(1/0.955),"6":1.},"375_475":{"52":float(1/0.862),"53":float(1/0.972),"55":float(1/0.971),"6":1.},"475_575":{"51":float(1/0.87),"52":float(1/0.86),"53":float(1/0.972),"55":1.,"6":1.},"575_675":{"51":float(1/0.877),"52":float(1/0.849),"53":1.,"55":1.,"6":1.},"675_775": {"51":float(1/0.848),"52":1.,"53":1.,"55":1.,"6":1.},"775_875": {"51":1.,"52":1.,"53":1.,"55":1.,"6":1.} ,"875_inf": {"51":1.,"52":1.,"53":1.,"55":1.,"6":1.} }
          if htbin in Scale_Amount: 
            if alphat in Scale_Amount[htbin] and Scale_Amount[htbin][alphat] != 1: 
              print "Scaling data due to Trigger efficiency of %s percent " % ((1/Scale_Amount[htbin][alphat])*100)
              if number_mode: return float(Scale_Amount[htbin][alphat])
              else: hist.Scale(Scale_Amount[htbin][alphat])
            else : return float(1.0)  
        else:
          Scale_Amount = {"275_325":float(1/0.9153),"325_375":float(1/0.9562),"375_475":float(1/0.9688),"475_575":float(1/0.9789),"575_675":1,"675_775":1,"775_875":1,"875_inf":1}
          if htbin in Scale_Amount and Scale_Amount[htbin] != 1:
              print "Scaling data due to Trigger efficiency of %s percent " % ((1/Scale_Amount[htbin]) * 100)
              if number_mode: return float(Scale_Amount[htbin])
              else:  hist.Scale(Scale_Amount[htbin])
          else: return float(1.0)
class Number_Extractor(object):

  def __init__(self):
    print "\n\nGetting Numbers\n\n"
    self.f = open('dictionaries.txt',"r")
    for line in self.f.readlines():
      i = 1
      dict = line
      self.table = open('Table_%s.tex'%i,'w')
      self.Prediction_Maker(dict)
      self.table.close()
      i += 1
 
  def Prediction_Maker(self,dict):
      
      inhad_zinv = False
      inhad_wjets = False
      indimuon = False
      inmuon = False
      inphoton = False

      MC_Weights = {"TTbar":0.00425452,"WJetsInc":0.0666131,"WJets250":0.000450549,"WJets300":0.00102329,"Zinv50":0.00485311,"Zinv100":0.00410382,"Zinv200":0.0013739,"Zmumu":0.00849073,"Photon":1.,"Data":1.}

      self.bins = ('275','325','375','475','575','675','775','875')
      entries = ('Data','Yield','SM_Stat_Error','Muon_Trans','DiMuon_Trans','TotError')

      self.Had_Yield_Per_Bin = dict.fromkeys(self.bins)
      self.Had_Muon_Yield_Per_Bin = dict.fromkeys(self.bins)
      self.Had_Zmumu_Yield_Per_Bin = dict.fromkeys(self.bins)
      self.Muon_Yield_Per_Bin = dict.fromkeys(self.bins)
      self.DiMuon_Yield_Per_Bin = dict.fromkeys(self.bins)
      self.Photon_Yield_Per_Bin = dict.fromkeys(self.bins)

      dictionaries = [self.Had_Yield_Per_Bin,self.Had_Muon_Yield_Per_Bin,self.Had_Zmumu_Yield_Per_Bin,self.DiMuon_Yield_Per_Bin,self.Muon_Yield_Per_Bin,self.Photon_Yield_Per_Bin]
      for dicto in dictionaries:
        for key in self.bins:
          dicto[key] = dict.fromkeys(entries,0)
          dicto[key]['TotError'] = [] 

      for entry in dict:
        Error = 0
        if dict[entry]["SampleType"] == "Data":
          if dict[entry]["Category"] == "Had": 
            self.Had_Yield_Per_Bin[dict[entry]["HT"]]["Data"] = dict[entry]["Yield"]
            self.Had_Muon_Yield_Per_Bin[dict[entry]["HT"]]["Data"] = dict[entry]["Yield"]
            self.Had_Zmumu_Yield_Per_Bin[dict[entry]["HT"]]["Data"] = dict[entry]["Yield"]
          if dict[entry]["Category"] == "Muon": self.Muon_Yield_Per_Bin[dict[entry]["HT"]]["Data"] = dict[entry]["Yield"]
          if dict[entry]["Category"] == "DiMuon": self.DiMuon_Yield_Per_Bin[dict[entry]["HT"]]["Data"] = dict[entry]["Yield"]

        Error = sqrt(dict[entry]["Yield"]*float(MC_Weights[dict[entry]["SampleType"]])*47)
        elif dict[entry]["Category"] == "Had" :
            if dict[entry]["SampleType"] == "Zinv50" or dict[entry]["SampleType"] == "Zinv100" or dict[entry]["SampleType"] == "Zinv200": 
              inhad_zinv = True
              self.Had_Zmumu_Yield_Per_Bin[dict[entry]["HT"]]["Yield"] +=  dict[entry]["Yield"]
              self.Had_Zmumu_Yield_Per_Bin[dict[entry]["HT"]]["TotError"].append(Error)
            else:  
              inhad_wjet = True
              self.Had_Muon_Yield_Per_Bin[dict[entry]["HT"]]["Yield"] +=  dict[entry]["Yield"]
              self.Had_Muon_Yield_Per_Bin[dict[entry]["HT"]]["TotError"].append(Error)
            
            self.Had_Yield_Per_Bin[dict[entry]["HT"]]["Yield"] +=  dict[entry]["Yield"]
            self.Had_Yield_Per_Bin[dict[entry]["HT"]]["TotError"].append(Error)

        elif dict[entry]["Category"] == "Muon":
            inmuon = True
            self.Muon_Yield_Per_Bin[dict[entry]["HT"]]["Yield"] +=  dict[entry]["Yield"]
            self.Muon_Yield_Per_Bin[dict[entry]["HT"]]["TotError"].append(Error)
        elif dict[entry]["Category"] == "DiMuon":
            indimuon = True
            self.DiMuon_Yield_Per_Bin[dict[entry]["HT"]]["Yield"] +=  dict[entry]["Yield"]
            self.DiMuon_Yield_Per_Bin[dict[entry]["HT"]]["TotError"].append(Error)
        elif dict[entry]["Category"] == "Photon":
            inphoton = True
            self.Photon_Yield_Per_Bin[(dict[entry]["HT"]).split('_')[0]]["Yield"] +=  dict[entry]["Yield"]
            self.Photon_Yield_Per_Bin[(dict[entry]["HT"]).split('_')[0]]["TotError"].append(Error)
      
      for bin in self.Muon_Yield_Per_Bin: 
        for dict in dictionaries: 
          try:  dict[bin]["SM_Stat_Error"] = sqrt(reduce(lambda x,y : x+y,map(lambda x: x*x, dict[bin]["TotError"])))
          except TypeError: pass
       
      if inhad_wjet and indimuon and inmuon and inhad_zinv:
        category = "Combined_SM"
        self.Table_Prep(self.Muon_Yield_Per_Bin,self.Had_Muon_Yield_Per_Bin, comb = self.DiMuon_Yield_Per_Bin, comb_test=self.Had_Zmumu_Yield_Per_Bin)
        self.Produce_Tables(self.Dict_For_Table,category = category, dict2 = self.Combination_Pred_Table)

      if inmuon and inhad_zinv and inhad_wjet:
        category = "Total_SM"
        self.Table_Prep(self.Muon_Yield_Per_Bin,self.Had_Yield_Per_Bin)
        self.Produce_Tables(self.Dict_For_Table,category = category)
        self.Ratio_Plots(self.Dict_For_Table, category = category)

      if inhad_zinv and indimuon:
        category = "Di_Muon_Zinv"
        self.Table_Prep(self.DiMuon_Yield_Per_Bin,self.Had_Zmumu_Yield_Per_Bin)
        self.Produce_Tables(self.Dict_For_Table,category = category)
        self.Ratio_Plots(self.Dict_For_Table, category = category)

      if inmuon and indimuon:
        category = "Di_Muon"
        self.Table_Prep(self.Muon_Yield_Per_Bin,self.DiMuon_Yield_Per_Bin)
        self.Produce_Tables(self.Dict_For_Table,category = category)
        self.Ratio_Plots(self.Dict_For_Table, category = category)

      if inhad_wjet and inmuon:
        category = "Muon"
        self.Table_Prep(self.Muon_Yield_Per_Bin,self.Had_Muon_Yield_Per_Bin)
        self.Produce_Tables(self.Dict_For_Table,category = category)
        self.Ratio_Plots(self.Dict_For_Table, category = category)

      if inphoton: pass  

      self.f.close()

  def Ratio_Plots(self,dict,category =""):
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
      c1.SaveAs("%s_Prediction_Traslation_Factor.png" %category)

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
      c1.SaveAs("%s_Prediction_Numbers.png" %category)

  def Table_Prep(self,control,test,comb="",comb_test=""):
      
      self.Dict_For_Table = dict.fromkeys(self.bins)
      self.Combination_Pred_Table = dict.fromkeys(self.bins)
      entries = ('Data_Pred','Prediction','Pred_Error','Data','Trans','Trans_Error')
      dictionaries = [self.Dict_For_Table,self.Combination_Pred_Table]

      for dicto in dictionaries:
        for key in self.bins: dicto[key] = dict.fromkeys(entries,0)

      for bin in control: 
          try:self.Dict_For_Table[bin]['Trans'] = test[bin]["Yield"]/control[bin]["Yield"]
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


  def Produce_Tables(self,dict,category="",dict2 =""):
      print "\n\nMaking Tables for %s" % category
      
      if category == "Total_SM": self.Latex_Table(dict,caption = "Binned %s Predictions" %category, 
            rows = [{"label": r'''Total Had Selection MC''',"entryFunc": self.MakeList(self.Had_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''MC $\mu +$~jets''',         "entryFunc":self.MakeList(self.Muon_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''MC Ratio''',                "entryFunc":self.MakeList(dict,"Trans","Trans_Error")},
                    {"label": r'''Data $\mu +$~jets''',       "entryFunc":self.MakeList(dict,"Data_Pred")},
                    {"label":r'''Total SM Prediction''', "entryFunc":self.MakeList(dict,"Prediction","Pred_Error")},
                    {"label": r'''Data Had Selection''',       "entryFunc":self.MakeList(dict,"Data")},])
            
      if category == "Muon": self.Latex_Table(dict,caption = "Binned %s Predictions" %category, 
            rows = [{"label": r'''W + TTbar Had MC''',"entryFunc": self.MakeList(self.Had_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''W + TTbar MC $\mu +$~jets''',         "entryFunc":self.MakeList(self.Muon_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''MC Ratio''',                "entryFunc":self.MakeList(dict,"Trans","Trans_Error")},
                    {"label": r'''Data $\mu +$~jets''',       "entryFunc":self.MakeList(dict,"Data_Pred")},
                    {"label":r'''W + TTbar Prediction''', "entryFunc":self.MakeList(dict,"Prediction","Pred_Error")},
                    {"label": r'''Data Had Selection''',       "entryFunc":self.MakeList(dict,"Data")},])
               
      if category == "Di_Muon": self.Latex_Table(dict,caption = "Binned %s Predictions" %category, 
            rows = [{"label": r'''Z mumu Selection MC''',"entryFunc": self.MakeList(self.DiMuon_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''MC $\mu +$~jets''',         "entryFunc":self.MakeList(self.Muon_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''MC Ratio''',                "entryFunc":self.MakeList(dict,"Trans","Trans_Error")},
                    {"label": r'''Data $\mu +$~jets''',       "entryFunc":self.MakeList(dict,"Data_Pred")},
                    {"label":r'''Z mu mu Prediction''', "entryFunc":self.MakeList(dict,"Prediction","Pred_Error")},
                    {"label": r'''Data Z mumu''',       "entryFunc":self.MakeList(dict,"Data")},])
     
      if category == "Di_Muon_Zinv": self.Latex_Table(dict,caption = "Binned %s Predictions" %category, 
            rows = [{"label": r'''Z nunu Had Selection MC''',"entryFunc": self.MakeList(self.Had_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''Z mumu Selection MC''',         "entryFunc":self.MakeList(self.DiMuon_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''MC Ratio''',                "entryFunc":self.MakeList(dict,"Trans","Trans_Error")},
                    {"label": r'''Data Z mu mu''',       "entryFunc":self.MakeList(dict,"Data_Pred")},
                    {"label":r'''Z nunu Prediction''', "entryFunc":self.MakeList(dict,"Prediction","Pred_Error")}])
               
      if category == "Combined_SM": self.Latex_Table(dict,caption = "Binned %s Predictions" %category, 
            rows = [{"label": r'''TTbar + W Prediction from Muon''', "entryFunc":self.MakeList(dict,"Prediction","Pred_Error")},
                    {"label": r'''Zinv Prediction from DiMuon''', "entryFunc":self.MakeList(dict2,"Prediction","Pred_Error")},
                    {"label":r'''Combined SM Prediction''', "entryFunc":self.MakeList(dict,"Prediction","Pred_Error",combined=dict2)},
                    {"label": r'''Data  Had Selection''',  "entryFunc":self.MakeList(dict,"Data")},])
      
  def MakeList(self,dict,key,error = "",combined = ""):
      List = []
      for entry in sorted(dict.iterkeys()):
        if error: List.append(self.toString("%4.2f" %(dict[entry][key]+combined[entry][key] if combined else dict[entry][key]))+"  \pm  "+ self.toString("%4.2f" %(dict[entry][error]+combined[entry][error] if combined else dict[entry][error])))
        else: List.append(self.toString("%4.2f" %(dict[entry][key]+combined[entry][key] if combined else dict[entry][key])))
      return List  
        
   def oneRow(self,label = "", labelWidth = 23, entryList = [], entryWidth = 30, extra = "") :
    s = ""
    s += "\n"+label.ljust(labelWidth)+" & "+" & ".join([(self.toString(entry)).ljust(entryWidth) for entry in entryList])+r"\\ "
    return s 

  def toString(self,item) :
    if type(item) is float : return str(item)
    else : return str(item)
  
  def Latex_Table(self,dict,rows,caption = ""):
      s = "\n"
      s += r'''\begin{table}[ht!]'''
      s += "\n\caption{%s %s fb$^{-1}$}"%(caption,a.options.Lumo)
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
          	s += self.oneRow(label = row["label"], entryList = (row["entryFunc"][i] for i in indices),entryWidth=row["entryWidth"] if "entryWidth" in row else 30)      
      s += "\n\hline"
      s += "\n\end{tabular}"
      s += "\n\end{table}"
      s += "\n\n\n\n"
      self.table.write(s)
      print s

#if __name__=="__main__":
#  a = Number_Extractor()
