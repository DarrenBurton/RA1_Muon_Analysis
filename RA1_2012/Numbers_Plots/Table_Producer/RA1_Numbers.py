#!/usr/bin/env python
from ROOT import *
import ROOT as r
import logging,itertools
import os,fnmatch,sys
import glob, errno
from time import strftime
from optparse import OptionParser
import array, ast
from math import *
from plottingUtils import *
from Jad_Compute import *

def MC_Scaler(htbin,alphat_slice,mc_yield,sample = '',error = '',Keep_AlphaT = ''):
	  
    AlphaT_Scale = {"275_0.55":float(0.727),"325_0.55":float(0.869),"375_0.55":float(0.943),"475_0.55":float(1.0),"575_0.55":1.,"675_0.55":1.,"775_0.55":1.,"875_0.55":1.,"575_0.53":float(0.970),"675_0.53":float(0.970),"775_0.53":float(0.970),"875_0.53":float(0.970),"775_0.52":1.,"875_0.52":1.}

    AlphaT_Error = {"275_0.55":float(0.018),"325_0.55":float(0.028),"375_0.55":float(0.009),"475_0.55":float(0.048),"575_0.55":float(0.048),"675_0.55":float(0.048),"775_0.55":float(0.048),"875_0.55":float(0.048),"575_0.53":float(0.05),"675_0.53":float(0.05),"775_0.53":float(0.05),"875_0.53":float(0.05),"775_0.52":float(0.207),"875_0.52":float(0.207)}

    scale_factor = htbin +'_'+ alphat_slice
    if mc_yield == 0: return float(mc_yield)    
    if sample == "Muon" and str(htbin) not in ["275","325"] and Keep_AlphaT != "True":
      #print "In Muon Trigger Scaling"
      if error:
        return float((error*0.95)*math.sqrt(((mc_yield/error)*(mc_yield/error))+(0.01*0.01)))
      else:return float(mc_yield*0.95)    
    else:
      #print "In AlphaT Trigger Scaling"
      if alphat_slice == '0.01': scale_factor = htbin +'_0.55'
      if error: return float((error*AlphaT_Scale[scale_factor])*math.sqrt(((mc_yield/error)*(mc_yield/error))+(AlphaT_Error[scale_factor]*AlphaT_Error[scale_factor])))
      else:return float(mc_yield*AlphaT_Scale[scale_factor])

class Number_Extractor(object):

  def __init__(self,sample_settings,sample_list,number,c_file = "",Triggers = "",Closure = "",Stats = "",AlphaT='',Trans_Plots = ''):

    print "\n\nGetting Numbers\n\n"
    self.Settings = sample_settings
    self.Keep_AlphaT = AlphaT
    self.Make_Root_Stats_File = Stats
    self.Make_Closure_Tests = Closure
    self.Trigger_Scaling = Triggers
    self.c_file = c_file
    self.Make_2D_Histos = Trans_Plots
    self.number = number
    print "Luminosity of Sample is %s fb\n\n" %self.Settings["Lumo"]
    r.gROOT.SetBatch(True)
    self.Create_Dictionary(sample_settings,sample_list)
    if self.Make_Root_Stats_File == "True": self.Begin_Stats_Root_Output(sample_settings)
    self.Prediction_Maker(sample_settings,self.return_dict)
    if self.Make_2D_Histos: self.Make_2D_Table(sample_settings,self.return_dict,self.Translation_Dict)

  def Make_2D_Table(self,settings,dict,translation_dict):
      HT_List = []
      Alpha_List = []
      for num in settings["dirs"] : HT_List.append(int(num.split('_')[0]))
      for slice in settings["AlphaTSlices"]:  Alpha_List.append(float(slice.split('_')[0])*100)
      HT_List.append(975)
      Alpha_List.append(60)

      FinalPlot = r.TH2D("finalPlot","",len(settings["dirs"]),array.array('d',HT_List),len(settings["AlphaTSlices"]),array.array('d',Alpha_List))
      FinalPlot.GetXaxis().SetTitle("H_{T} (GeV)")
      FinalPlot.GetYaxis().SetTitle("#alpha_{T}")
      FinalPlot.GetYaxis().SetTitleSize(0.055)
      FinalPlot.GetYaxis().SetTitleOffset(.85)
      FinalPlot.GetXaxis().SetTitleSize(0.06)
      FinalPlot.GetYaxis().SetTitleSize(0.06)
      FinalPlot.GetYaxis().SetRangeUser(51.,61.)
      FinalPlot.GetZaxis().SetTitleSize(0.06)
      FinalPlot.GetZaxis().SetTitle("Yield")
      FinalPlot.GetZaxis().SetTitleOffset(1.07)
      FinalPlot.GetZaxis().SetRangeUser(0.0,5000.)

      HadPlot = FinalPlot.Clone()
      DiMuonPlot = FinalPlot.Clone()

      #Trans Factor Plots
      Muon_SM_RatioPlot = FinalPlot.Clone()
      Muon_SM_RatioPlot.GetZaxis().SetRangeUser(0.0,3)
      Muon_RatioPlot = FinalPlot.Clone()
      Muon_RatioPlot.GetZaxis().SetRangeUser(0.0,2)
      DiMuon_ZinvRatioPlot = FinalPlot.Clone()
      DiMuon_ZinvRatioPlot.GetZaxis().SetRangeUser(0.0,50)
      Photon_ZinvRatioPlot = FinalPlot.Clone()
      Photon_ZinvRatioPlot.GetZaxis().SetRangeUser(0.0,10)
      
      for name in translation_dict:
        for key in translation_dict[name]:
          for entry in translation_dict[name][key]:
           if entry  == "Tot_SM_Trans":
              bin = Muon_SM_RatioPlot.FindBin(float(key),float(name)*100)
              Muon_SM_RatioPlot.SetBinContent(bin,float(translation_dict[name][key][entry]))
           if entry  == "Muon_Trans":
              bin = Muon_RatioPlot.FindBin(float(key),float(name)*100)
              Muon_RatioPlot.SetBinContent(bin,float(translation_dict[name][key][entry])) 
           if entry  == "DiMuon_Trans":
              bin = DiMuon_ZinvRatioPlot.FindBin(float(key),float(name)*100)
              DiMuon_ZinvRatioPlot.SetBinContent(bin,float(translation_dict[name][key][entry]))   
           if entry  == "Photon_Trans":
              bin = Photon_ZinvRatioPlot.FindBin(float(key),float(name)*100)
              Photon_ZinvRatioPlot.SetBinContent(bin,float(translation_dict[name][key][entry]))     
      
      drawhad = False
      drawdimuon = False

      for name in dict:
        if dict[name]["SampleType"] == "Data" and dict[name]["Category"] == "Muon":
          bin = FinalPlot.FindBin(float(dict[name]["HT"].split('_')[0]) , float(dict[name]["AlphaT"])*100)
          FinalPlot.SetBinContent(bin,float(dict[name]["Yield"]))
        elif dict[name]["SampleType"] == "Data" and dict[name]["Category"] == "Had":
          bin = HadPlot.FindBin(float(dict[name]["HT"].split('_')[0]) , float(dict[name]["AlphaT"])*100)
          HadPlot.SetBinContent(bin,float(dict[name]["Yield"]))
          drawhad = True
        elif dict[name]["SampleType"] == "Data" and dict[name]["Category"] == "DiMuon":
          bin = DiMuonPlot.FindBin(float(dict[name]["HT"].split('_')[0]) , float(dict[name]["AlphaT"])*100)
          DiMuonPlot.SetBinContent(bin,float(dict[name]["Yield"]))
          drawdimuon = True

      c2 = r.TCanvas("canvas","mycanvas")
      c2.cd()
      c2.SetMargin(0.1,0.17,0.15,0.05)

      FinalPlot.Draw("COLZtext")
      c2.SaveAs("MuonYield.pdf")
      if drawhad:
        HadPlot.Draw("COLZtext")
        c2.SaveAs("HadYield.pdf")
      if drawdimuon:
        DiMuonPlot.Draw("COLZtext")
        c2.SaveAs("DiMuonYield.pdf")
      Muon_SM_RatioPlot.Draw("COLZtext")
      c2.SaveAs("Muon_Total_SM_Ratio_Plot.pdf")
      Muon_RatioPlot.Draw("COLZtext")
      c2.SaveAs("Muon_Ratio_Plot.pdf")
      DiMuon_ZinvRatioPlot.Draw("COLZtext")
      c2.SaveAs("DiMuon_Zinv_Ratio_Plot.pdf")
      Photon_ZinvRatioPlot.Draw("COLZtext")
      c2.SaveAs("Photon_Zinv_Ratio_Plot.pdf")

  def Create_Dictionary(self,settings,samples):

         table_entries = "{" 
         for key,fi in sorted(samples.iteritems()):
           i = 0
           for dir in settings['dirs']:
              fixed_dir = dir
              for alphat in settings['AlphaTSlices']:
                dir = fixed_dir
                lower = alphat.split('_')[0]
                higher = alphat.split('_')[1]
                if dir[0:3] not in ["775","875"] and lower == "0.52": continue
                elif dir[0:3] not in ["575","675","775","875"] and lower == "0.53": continue
                table_entries += "\t\"%s_%d\"  : "%(key,i)
                i+=1
                table_entries += "{\"HT\":\"%s\","%(dir[0:3])
                for histName in settings['plots']:
                    checkht = dir
                    dir = fi[1]+dir
                    normal =  GetSumHist(File = ["%s.root"%fi[0]], Directories = [dir], Hist = histName, Col = r.kBlack, Norm = None if "n" == key[0] else [float(self.Settings["Lumo"]*1000)/100.], LegendText = "nBtag")  
                    normal.HideOverFlow()
                    if self.Keep_AlphaT == "True":
                      #print "Keeping AlphaT Cut"
                      err = r.Double(0.0)
                      normal.hObj.IntegralAndError(int(float(lower)/0.01)+1,int(float(higher)/0.01),err)
                      table_entries +=" \"Yield\": %.3e ,\"Error\":\"%s\",\"SampleType\":\"%s\",\"Category\":\"%s\",\"AlphaT\":%s},\n"%((normal.hObj.Integral(int(float(lower)/0.01)+1,int(float(higher)/0.01))),err,fi[2],fi[3],lower)
                      #table_entries +=" \"Yield\": %.3e ,\"Error\":\"%s\",\"SampleType\":\"%s\",\"Category\":\"%s\",\"AlphaT\":%s},\n"%((normal.hObj.Integral(int(float(0.55)/0.01)+1,int(float(10)/0.01)) if fi[3] =="Had" or str(checkht[0:3]) == "275" or str(checkht[0:3]) == "325" else (normal.hObj.Integral(int(float(lower)/0.01)+1,int(float(higher)/0.01)))),err,fi[2],fi[3],lower)
                    else:
                      #print "No AlphaT for Control Sample Higher Bins"
                      err = r.Double(0.0)
                      if (fi[3] == "Had" or str(checkht[0:3]) == "275" or str(checkht[0:3]) == "325"):normal.hObj.IntegralAndError(int(float(lower)/0.01)+1,int(float(higher)/0.01),err)
                      else: normal.hObj.IntegralAndError(1,2000,err)

                      table_entries +=" \"Yield\": %.3e ,\"Error\":\"%s\",\"SampleType\":\"%s\",\"Category\":\"%s\",\"AlphaT\":%s},\n"%((normal.hObj.Integral(int(float(lower)/0.01)+1,int(float(higher)/0.01)) if fi[3] =="Had" or str(checkht[0:3]) == "275" or str(checkht[0:3]) == "325" else (normal.hObj.Integral())),err,fi[2],fi[3],lower)
                    normal.a.Close()
         '''
         Photon dictionaries, uncomment as necessary
         '''
         if self.number == "Zero_btags": table_entries += self.photon_dict_zero_btag()  
         if self.number == "One_btag": table_entries += self.photon_dict_one_btag()  
         #table_entries += self.photon_dict_btag()          
         if self.number == "BaseLine": table_entries += self.photon_dict()

         table_entries +="}"
         #print table_entries
         #print table_entries
         self.return_dict = ast.literal_eval(table_entries)
         return self.return_dict


  def photon_dict_btag(self):
    s= "\"phot1\":{\"HT\":\"275\",\"Yield\":0,\"SampleType\":\"Photon\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":0},\n"
    s+= "\"phot2\":{\"HT\":\"325\",\"Yield\":0,\"SampleType\":\"Photon\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":0},\n"
    s+= "\"phot3\":{\"HT\":\"375\",\"Yield\":148.,\"SampleType\":\"Photon\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":10.},\n"
    s+= "\"phot4\":{\"HT\":\"475\",\"Yield\":47.,\"SampleType\":\"Photon\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":7.},\n"
    s+= "\"phot5\":{\"HT\":\"575\",\"Yield\":20.,\"SampleType\":\"Photon\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":5.},\n"
    s+= "\"phot6\":{\"HT\":\"675\",\"Yield\":9.,\"SampleType\":\"Photon\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":3.0},\n"
    s+= "\"phot7\":{\"HT\":\"775\",\"Yield\":3.,\"SampleType\":\"Photon\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":2.0},\n"
    s+= "\"phot8\":{\"HT\":\"875\",\"Yield\":3.,\"SampleType\":\"Photon\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":2.0},\n"
    s+= "\"nphot1\":{\"HT\":\"275\",\"Yield\":0,\"SampleType\":\"Data\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":0},\n"
    s+= "\"nphot2\":{\"HT\":\"325\",\"Yield\":0,\"SampleType\":\"Data\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":0},\n"
    s+= "\"nphot3\":{\"HT\":\"375\",\"Yield\":137.,\"SampleType\":\"Data\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":0},\n"
    s+= "\"nphot4\":{\"HT\":\"475\",\"Yield\":47.,\"SampleType\":\"Data\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":0},\n"
    s+= "\"nphot5\":{\"HT\":\"575\",\"Yield\":21.,\"SampleType\":\"Data\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":0},\n"
    s+= "\"nphot6\":{\"HT\":\"675\",\"Yield\":9.,\"SampleType\":\"Data\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":0},\n"
    s+= "\"nphot7\":{\"HT\":\"775\",\"Yield\":5.,\"SampleType\":\"Data\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":0},\n"
    s+= "\"nphot8\":{\"HT\":\"875\",\"Yield\":2.,\"SampleType\":\"Data\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":0},\n"

    return s

  def photon_dict_one_btag(self):
    s= "\"phot1\":{\"HT\":\"275\",\"Yield\":0,\"SampleType\":\"Photon\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":0},\n"
    s+= "\"phot2\":{\"HT\":\"325\",\"Yield\":0,\"SampleType\":\"Photon\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":0},\n"
    s+= "\"phot3\":{\"HT\":\"375\",\"Yield\":128.,\"SampleType\":\"Photon\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":10.},\n"
    s+= "\"phot4\":{\"HT\":\"475\",\"Yield\":41.,\"SampleType\":\"Photon\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":7.},\n"
    s+= "\"phot5\":{\"HT\":\"575\",\"Yield\":19.,\"SampleType\":\"Photon\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":5.},\n"
    s+= "\"phot6\":{\"HT\":\"675\",\"Yield\":6.,\"SampleType\":\"Photon\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":3.0},\n"
    s+= "\"phot7\":{\"HT\":\"775\",\"Yield\":3.,\"SampleType\":\"Photon\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":2.0},\n"
    s+= "\"phot8\":{\"HT\":\"875\",\"Yield\":3.,\"SampleType\":\"Photon\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":1.0},\n"
    s+= "\"nphot1\":{\"HT\":\"275\",\"Yield\":0,\"SampleType\":\"Data\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":0},\n"
    s+= "\"nphot2\":{\"HT\":\"325\",\"Yield\":0,\"SampleType\":\"Data\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":0},\n"
    s+= "\"nphot3\":{\"HT\":\"375\",\"Yield\":126.,\"SampleType\":\"Data\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":0},\n"
    s+= "\"nphot4\":{\"HT\":\"475\",\"Yield\":43.,\"SampleType\":\"Data\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":0},\n"
    s+= "\"nphot5\":{\"HT\":\"575\",\"Yield\":19.,\"SampleType\":\"Data\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":0},\n"
    s+= "\"nphot6\":{\"HT\":\"675\",\"Yield\":5.,\"SampleType\":\"Data\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":0},\n"
    s+= "\"nphot7\":{\"HT\":\"775\",\"Yield\":5.,\"SampleType\":\"Data\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":0},\n"
    s+= "\"nphot8\":{\"HT\":\"875\",\"Yield\":2.,\"SampleType\":\"Data\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":0},\n"

    return s

  def photon_dict_zero_btag(self):
    s= "\"phot1\":{\"HT\":\"275\",\"Yield\":0,\"SampleType\":\"Photon\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":0},\n"
    s+= "\"phot2\":{\"HT\":\"325\",\"Yield\":0,\"SampleType\":\"Photon\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":0},\n"
    s+= "\"phot3\":{\"HT\":\"375\",\"Yield\":1142.,\"SampleType\":\"Photon\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":40.},\n"
    s+= "\"phot4\":{\"HT\":\"475\",\"Yield\":393.,\"SampleType\":\"Photon\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":20.},\n"
    s+= "\"phot5\":{\"HT\":\"575\",\"Yield\":158.,\"SampleType\":\"Photon\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":10.},\n"
    s+= "\"phot6\":{\"HT\":\"675\",\"Yield\":49.,\"SampleType\":\"Photon\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":8.0},\n"
    s+= "\"phot7\":{\"HT\":\"775\",\"Yield\":17.,\"SampleType\":\"Photon\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":5.0},\n"
    s+= "\"phot8\":{\"HT\":\"875\",\"Yield\":11.,\"SampleType\":\"Photon\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":3.0},\n"
    s+= "\"nphot1\":{\"HT\":\"275\",\"Yield\":0,\"SampleType\":\"Data\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":0},\n"
    s+= "\"nphot2\":{\"HT\":\"325\",\"Yield\":0,\"SampleType\":\"Data\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":0},\n"
    s+= "\"nphot3\":{\"HT\":\"375\",\"Yield\":909.,\"SampleType\":\"Data\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":0},\n"
    s+= "\"nphot4\":{\"HT\":\"475\",\"Yield\":328.,\"SampleType\":\"Data\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":0},\n"
    s+= "\"nphot5\":{\"HT\":\"575\",\"Yield\":109.,\"SampleType\":\"Data\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":0},\n"
    s+= "\"nphot6\":{\"HT\":\"675\",\"Yield\":50.,\"SampleType\":\"Data\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":0},\n"
    s+= "\"nphot7\":{\"HT\":\"775\",\"Yield\":13.,\"SampleType\":\"Data\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":0},\n"
    s+= "\"nphot8\":{\"HT\":\"875\",\"Yield\":12.,\"SampleType\":\"Data\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":0},\n"

    return s




  def photon_dict(self):
    s= "\"phot1\":{\"HT\":\"275\",\"Yield\":0,\"SampleType\":\"Photon\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":0},\n"
    s+= "\"phot2\":{\"HT\":\"325\",\"Yield\":0,\"SampleType\":\"Photon\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":0},\n"
    s+= "\"phot3\":{\"HT\":\"375\",\"Yield\":1316.,\"SampleType\":\"Photon\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":40.},\n"
    s+= "\"phot4\":{\"HT\":\"475\",\"Yield\":444.,\"SampleType\":\"Photon\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":20.},\n"
    s+= "\"phot5\":{\"HT\":\"575\",\"Yield\":180.,\"SampleType\":\"Photon\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":10.},\n"
    s+= "\"phot6\":{\"HT\":\"675\",\"Yield\":58.,\"SampleType\":\"Photon\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":8.0},\n"
    s+= "\"phot7\":{\"HT\":\"775\",\"Yield\":20.,\"SampleType\":\"Photon\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":5.0},\n"
    s+= "\"phot8\":{\"HT\":\"875\",\"Yield\":14.,\"SampleType\":\"Photon\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":3.0},\n"
    s+= "\"nphot1\":{\"HT\":\"275\",\"Yield\":0,\"SampleType\":\"Data\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":0},\n"
    s+= "\"nphot2\":{\"HT\":\"325\",\"Yield\":0,\"SampleType\":\"Data\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":0},\n"
    s+= "\"nphot3\":{\"HT\":\"375\",\"Yield\":1046.,\"SampleType\":\"Data\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":0},\n"
    s+= "\"nphot4\":{\"HT\":\"475\",\"Yield\":375.,\"SampleType\":\"Data\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":0},\n"
    s+= "\"nphot5\":{\"HT\":\"575\",\"Yield\":130.,\"SampleType\":\"Data\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":0},\n"
    s+= "\"nphot6\":{\"HT\":\"675\",\"Yield\":59.,\"SampleType\":\"Data\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":0},\n"
    s+= "\"nphot7\":{\"HT\":\"775\",\"Yield\":18.,\"SampleType\":\"Data\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":0},\n"
    s+= "\"nphot8\":{\"HT\":\"875\",\"Yield\":14.,\"SampleType\":\"Data\",\"Category\":\"Photon\",\"AlphaT\":0.55,\"Error\":0},\n"

    s+= "\"aphot1\":{\"HT\":\"275\",\"Yield\":0,\"SampleType\":\"Photon\",\"Category\":\"Photon\",\"AlphaT\":0.53,\"Error\":0},\n"
    s+= "\"aphot2\":{\"HT\":\"325\",\"Yield\":0,\"SampleType\":\"Photon\",\"Category\":\"Photon\",\"AlphaT\":0.53,\"Error\":0},\n"
    s+= "\"aphot3\":{\"HT\":\"375\",\"Yield\":0.,\"SampleType\":\"Photon\",\"Category\":\"Photon\",\"AlphaT\":0.53,\"Error\":0},\n"
    s+= "\"aphot4\":{\"HT\":\"475\",\"Yield\":0.,\"SampleType\":\"Photon\",\"Category\":\"Photon\",\"AlphaT\":0.53,\"Error\":0},\n"
    s+= "\"aphot5\":{\"HT\":\"575\",\"Yield\":42.4,\"SampleType\":\"Photon\",\"Category\":\"Photon\",\"AlphaT\":0.53,\"Error\":7.0},\n"
    s+= "\"aphot6\":{\"HT\":\"675\",\"Yield\":13.1,\"SampleType\":\"Photon\",\"Category\":\"Photon\",\"AlphaT\":0.53,\"Error\":4.0},\n"
    s+= "\"aphot7\":{\"HT\":\"775\",\"Yield\":6.0,\"SampleType\":\"Photon\",\"Category\":\"Photon\",\"AlphaT\":0.53,\"Error\":3.0},\n"
    s+= "\"aphot8\":{\"HT\":\"875\",\"Yield\":7.0,\"SampleType\":\"Photon\",\"Category\":\"Photon\",\"AlphaT\":0.53,\"Error\":2.0},\n"
    s+= "\"anphot1\":{\"HT\":\"275\",\"Yield\":0,\"SampleType\":\"Data\",\"Category\":\"Photon\",\"AlphaT\":0.53,\"Error\":0},\n"
    s+= "\"anphot2\":{\"HT\":\"325\",\"Yield\":0,\"SampleType\":\"Data\",\"Category\":\"Photon\",\"AlphaT\":0.53,\"Error\":0},\n"
    s+= "\"anphot3\":{\"HT\":\"375\",\"Yield\":0.,\"SampleType\":\"Data\",\"Category\":\"Photon\",\"AlphaT\":0.53,\"Error\":0},\n"
    s+= "\"anphot4\":{\"HT\":\"475\",\"Yield\":0.,\"SampleType\":\"Data\",\"Category\":\"Photon\",\"AlphaT\":0.53,\"Error\":0},\n"
    s+= "\"anphot5\":{\"HT\":\"575\",\"Yield\":32.0,\"SampleType\":\"Data\",\"Category\":\"Photon\",\"AlphaT\":0.53,\"Error\":0},\n"
    s+= "\"anphot6\":{\"HT\":\"675\",\"Yield\":7.,\"SampleType\":\"Data\",\"Category\":\"Photon\",\"AlphaT\":0.53,\"Error\":0},\n"
    s+= "\"anphot7\":{\"HT\":\"775\",\"Yield\":4.,\"SampleType\":\"Data\",\"Category\":\"Photon\",\"AlphaT\":0.53,\"Error\":0},\n"
    s+= "\"anphot8\":{\"HT\":\"875\",\"Yield\":7.,\"SampleType\":\"Data\",\"Category\":\"Photon\",\"AlphaT\":0.53,\"Error\":0},\n"

    s+= "\"bphot1\":{\"HT\":\"275\",\"Yield\":0,\"SampleType\":\"Photon\",\"Category\":\"Photon\",\"AlphaT\":0.52,\"Error\":0},\n"
    s+= "\"bphot2\":{\"HT\":\"325\",\"Yield\":0,\"SampleType\":\"Photon\",\"Category\":\"Photon\",\"AlphaT\":0.52,\"Error\":0},\n"
    s+= "\"bphot3\":{\"HT\":\"375\",\"Yield\":0,\"SampleType\":\"Photon\",\"Category\":\"Photon\",\"AlphaT\":0.52,\"Error\":0},\n"
    s+= "\"bphot4\":{\"HT\":\"475\",\"Yield\":0,\"SampleType\":\"Photon\",\"Category\":\"Photon\",\"AlphaT\":0.52,\"Error\":0},\n"
    s+= "\"bphot5\":{\"HT\":\"575\",\"Yield\":0,\"SampleType\":\"Photon\",\"Category\":\"Photon\",\"AlphaT\":0.52,\"Error\":0},\n"
    s+= "\"bphot6\":{\"HT\":\"675\",\"Yield\":0,\"SampleType\":\"Photon\",\"Category\":\"Photon\",\"AlphaT\":0.52,\"Error\":0},\n"
    s+= "\"bphot7\":{\"HT\":\"775\",\"Yield\":2.0,\"SampleType\":\"Photon\",\"Category\":\"Photon\",\"AlphaT\":0.52,\"Error\":2},\n"
    s+= "\"bphot8\":{\"HT\":\"875\",\"Yield\":3.0,\"SampleType\":\"Photon\",\"Category\":\"Photon\",\"AlphaT\":0.52,\"Error\":1},\n"
    s+= "\"bnphot1\":{\"HT\":\"275\",\"Yield\":0,\"SampleType\":\"Data\",\"Category\":\"Photon\",\"AlphaT\":0.52,\"Error\":0},\n"
    s+= "\"bnphot2\":{\"HT\":\"325\",\"Yield\":0,\"SampleType\":\"Data\",\"Category\":\"Photon\",\"AlphaT\":0.52,\"Error\":0},\n"
    s+= "\"bnphot3\":{\"HT\":\"375\",\"Yield\":0,\"SampleType\":\"Data\",\"Category\":\"Photon\",\"AlphaT\":0.52,\"Error\":0},\n"
    s+= "\"bnphot4\":{\"HT\":\"475\",\"Yield\":0,\"SampleType\":\"Data\",\"Category\":\"Photon\",\"AlphaT\":0.52,\"Error\":0},\n"
    s+= "\"bnphot5\":{\"HT\":\"575\",\"Yield\":0,\"SampleType\":\"Data\",\"Category\":\"Photon\",\"AlphaT\":0.52,\"Error\":0},\n"
    s+= "\"bnphot6\":{\"HT\":\"675\",\"Yield\":0,\"SampleType\":\"Data\",\"Category\":\"Photon\",\"AlphaT\":0.52,\"Error\":0},\n"
    s+= "\"bnphot7\":{\"HT\":\"775\",\"Yield\":2,\"SampleType\":\"Data\",\"Category\":\"Photon\",\"AlphaT\":0.52,\"Error\":0},\n"
    s+= "\"bnphot8\":{\"HT\":\"875\",\"Yield\":3,\"SampleType\":\"Data\",\"Category\":\"Photon\",\"AlphaT\":0.52,\"Error\":0}\n"
    return s
  
  def Prediction_Maker(self,settings,dict):
    
      self.bins = ('275','325','375','475','575','675','775','875')
      #self.alphat = ('0.52','0.53','0.55')
      self.alphat = ('0.55','0.01')
      #self.alphat = ('0.55')
      entries = ('Data','Yield','SM_Stat_Error','Muon_Trans','DiMuon_Trans','TotError','AlphaT','Btag','SampleName')
      trans_entries = ('Tot_SM_Trans','Tot_SM_Trans_Error','Muon_Trans','Muon_Trans_Error','DiMuon_Trans','DiMuon_Trans_Error','Photon_Trans','Photon_Trans_Error')
      MC_Weights = {"TTbar":0.00425452,"WJetsInc":0.0666131,"WJets250":0.000450549,"WJets300":0.00102329,"Zinv50":0.00485311,"Zinv100":0.00410382,"Zinv200":0.0013739,"DY":0.00849073,"Single_Tbar_tW":0.000921006,"Single_Tbar_t":0.000947643,"Single_T_tW":0.00091676,"Single_T_t":0.000915857,"WW":0.000722991,"WZ":0.000253803,"ZZ":0.00010278,"QCDb":1,"Photon":1.,"Data":1.}

      #L1 OffSet MC Weights
      #MC_Weights = {"TTbar":0.00425455,"WJetsInc":0.0507652,"WJets250":0.000400796,"WJets300":0.00102321,"Zinv50":0.00379111,"Zinv100":0.00318891,"Zinv200":0.00137389,"DY":0.00965997,"Single_Tbar_tW":0.00097485,"Single_Tbar_t":0.000947641,"Single_T_tW":0.000938672,"Single_T_t":0.00102475,"WW":0.000658555,"WZ":0.000246629,"ZZ":0.00010229,"QCDb":1,"Photon":1.,"Data":1.}



      #========
      self.Translation_Dict = dict.fromkeys(self.alphat)
      Trans_Dicts = [self.Translation_Dict]
      for file in Trans_Dicts:
        for key in self.alphat: 
          file[key] = dict.fromkeys(self.bins)
          for a in self.bins: file[key][a] = dict.fromkeys(trans_entries,0)
      #========

      self.table = open('Predictions_AlphaT_%s.tex' % self.number  ,'w')
      for slices in settings['AlphaTSlices']:
        print "Making Predictions for %s" %slices
        self.current_slice = str(slices).split('_')[0]
     
        inhad_zinv = False
        inhad_wjet = False
        indimuon = False
        inmuon = False
        inphoton = False
        inextras = False

        self.Had_Yield_Per_Bin = dict.fromkeys(self.bins)
        self.Had_Muon_Yield_Per_Bin = dict.fromkeys(self.bins)
        self.Had_Muon_WJets_Yield_Per_Bin = dict.fromkeys(self.bins)
        self.Had_Muon_TTbar_Yield_Per_Bin = dict.fromkeys(self.bins)
        self.Had_Zmumu_Yield_Per_Bin = dict.fromkeys(self.bins)
        self.Had_Single_Top_Yield_Per_Bin = dict.fromkeys(self.bins)
        self.Had_DY_Yield_Per_Bin = dict.fromkeys(self.bins)

        self.Had_WW_Yield_Per_Bin = dict.fromkeys(self.bins)
        self.Had_WZ_Yield_Per_Bin = dict.fromkeys(self.bins)
        self.Had_ZZ_Yield_Per_Bin = dict.fromkeys(self.bins)
        self.Had_QCD_B_Yield_Per_Bin = dict.fromkeys(self.bins)

        self.Muon_Yield_Per_Bin = dict.fromkeys(self.bins)
        self.Muon_TTbar_Yield_Per_Bin = dict.fromkeys(self.bins)
        self.Muon_WJets_Yield_Per_Bin = dict.fromkeys(self.bins)
        self.Muon_Single_Top_Yield_Per_Bin = dict.fromkeys(self.bins)
        self.Muon_DY_Yield_Per_Bin = dict.fromkeys(self.bins)

        self.Muon_WW_Yield_Per_Bin = dict.fromkeys(self.bins)
        self.Muon_WZ_Yield_Per_Bin = dict.fromkeys(self.bins)
        self.Muon_ZZ_Yield_Per_Bin = dict.fromkeys(self.bins)
        self.Muon_QCD_B_Yield_Per_Bin = dict.fromkeys(self.bins)
        self.Muon_Zinv_Yield_Per_Bin = dict.fromkeys(self.bins)

        self.DiMuon_Yield_Per_Bin = dict.fromkeys(self.bins)
        self.DiMuon_TTbar_Yield_Per_Bin = dict.fromkeys(self.bins)
        self.DiMuon_WJets_Yield_Per_Bin = dict.fromkeys(self.bins)
        self.DiMuon_Single_Top_Yield_Per_Bin = dict.fromkeys(self.bins)
        self.DiMuon_DY_Yield_Per_Bin = dict.fromkeys(self.bins)

        self.DiMuon_WW_Yield_Per_Bin = dict.fromkeys(self.bins)
        self.DiMuon_WZ_Yield_Per_Bin = dict.fromkeys(self.bins)
        self.DiMuon_ZZ_Yield_Per_Bin = dict.fromkeys(self.bins)
        self.DiMuon_QCD_B_Yield_Per_Bin = dict.fromkeys(self.bins)
        self.DiMuon_Zinv_Yield_Per_Bin = dict.fromkeys(self.bins)

        self.Photon_Yield_Per_Bin = dict.fromkeys(self.bins)

        dictionaries = [self.Had_Yield_Per_Bin,self.Had_Muon_WJets_Yield_Per_Bin,self.Had_Muon_TTbar_Yield_Per_Bin,self.Had_Muon_Yield_Per_Bin,self.Had_Zmumu_Yield_Per_Bin,        self.Had_Single_Top_Yield_Per_Bin,self.Had_DY_Yield_Per_Bin,self.Muon_Single_Top_Yield_Per_Bin, self.Muon_DY_Yield_Per_Bin,self.DiMuon_Yield_Per_Bin,self.Muon_Yield_Per_Bin,self.Muon_TTbar_Yield_Per_Bin,self.Muon_WJets_Yield_Per_Bin,self.DiMuon_Single_Top_Yield_Per_Bin, self.DiMuon_DY_Yield_Per_Bin,self.DiMuon_TTbar_Yield_Per_Bin,self.DiMuon_WJets_Yield_Per_Bin,self.Photon_Yield_Per_Bin, self.DiMuon_WW_Yield_Per_Bin, self.DiMuon_WZ_Yield_Per_Bin,self.DiMuon_ZZ_Yield_Per_Bin, self.DiMuon_QCD_B_Yield_Per_Bin,self.Muon_WW_Yield_Per_Bin, self.Muon_WZ_Yield_Per_Bin,self.Muon_ZZ_Yield_Per_Bin, self.Muon_QCD_B_Yield_Per_Bin,self.Had_WW_Yield_Per_Bin, self.Had_WZ_Yield_Per_Bin,self.Had_ZZ_Yield_Per_Bin, self.Had_QCD_B_Yield_Per_Bin,self.DiMuon_Zinv_Yield_Per_Bin, self.Muon_Zinv_Yield_Per_Bin ]

        #List of Dictionaries for Trigger Corrections

        had_dict = [self.Had_Yield_Per_Bin,self.Had_Muon_WJets_Yield_Per_Bin,self.Had_Muon_TTbar_Yield_Per_Bin,self.Had_Muon_Yield_Per_Bin,self.Had_Zmumu_Yield_Per_Bin,        self.Had_Single_Top_Yield_Per_Bin,self.Had_DY_Yield_Per_Bin,self.Had_WW_Yield_Per_Bin, self.Had_WZ_Yield_Per_Bin,self.Had_ZZ_Yield_Per_Bin, self.Had_QCD_B_Yield_Per_Bin]

        muon_dict = [self.Muon_Single_Top_Yield_Per_Bin, self.Muon_DY_Yield_Per_Bin,self.DiMuon_Yield_Per_Bin,self.Muon_Yield_Per_Bin,self.Muon_TTbar_Yield_Per_Bin,self.Muon_WJets_Yield_Per_Bin,self.DiMuon_Single_Top_Yield_Per_Bin, self.DiMuon_DY_Yield_Per_Bin,self.DiMuon_TTbar_Yield_Per_Bin,self.DiMuon_WJets_Yield_Per_Bin, self.DiMuon_WW_Yield_Per_Bin, self.DiMuon_WZ_Yield_Per_Bin,self.DiMuon_ZZ_Yield_Per_Bin, self.DiMuon_QCD_B_Yield_Per_Bin,self.Muon_WW_Yield_Per_Bin, self.Muon_WZ_Yield_Per_Bin,self.Muon_ZZ_Yield_Per_Bin, self.Muon_QCD_B_Yield_Per_Bin, self.Muon_Zinv_Yield_Per_Bin,self.DiMuon_Zinv_Yield_Per_Bin  ]

        # List of Dictionaries for Jad's Closure Tests

        jad_dictionaries = [self.Muon_Yield_Per_Bin,self.DiMuon_Yield_Per_Bin,self.Photon_Yield_Per_Bin]
        for dicto in dictionaries:
          for key in self.bins:
            dicto[key] = dict.fromkeys(entries,0)
            dicto[key]['TotError'] = []
            dicto[key]['AlphaT'] = self.current_slice
            dicto[key]['Btag'] = self.number
       
 
        #print self.Muon_Yield_Per_Bin

        for entry,fi in dict.iteritems():
          if str(fi['AlphaT']) == str(slices).split('_')[0] :
            Error = 0
            if dict[entry]["Category"] == "Photon": Error = dict[entry]["Error"]
            else : 
              #Error = math.sqrt(dict[entry]["Yield"]*float(MC_Weights[dict[entry]["SampleType"]])*float(self.Settings["Lumo"]*10))
              Error = float(dict[entry]["Error"])
            if dict[entry]["SampleType"] == "Data":
              if dict[entry]["Category"] == "Had": 
                self.Had_Yield_Per_Bin[dict[entry]["HT"]]["Data"] = dict[entry]["Yield"]
                self.Had_Muon_Yield_Per_Bin[dict[entry]["HT"]]["Data"] = dict[entry]["Yield"]
                self.Had_Zmumu_Yield_Per_Bin[dict[entry]["HT"]]["Data"] = dict[entry]["Yield"]
              if dict[entry]["Category"] == "Muon":
                  self.Muon_Yield_Per_Bin[dict[entry]["HT"]]["Data"] = dict[entry]["Yield"]
                  self.Muon_Yield_Per_Bin[dict[entry]["HT"]]["SampleName"] = "Muon" 
              if dict[entry]["Category"] == "DiMuon": 
                  self.DiMuon_Yield_Per_Bin[dict[entry]["HT"]]["Data"] = dict[entry]["Yield"]
                  self.DiMuon_Yield_Per_Bin[dict[entry]["HT"]]["SampleName"] = "DiMuon"
              if dict[entry]["Category"] == "Photon": 
                  self.Photon_Yield_Per_Bin[dict[entry]["HT"]]["Data"] = dict[entry]["Yield"]
                  self.Photon_Yield_Per_Bin[dict[entry]["HT"]]["SampleName"] = "Photon"

            elif dict[entry]["Category"] == "Had" :
               
                if dict[entry]["SampleType"] == "Zinv50" or dict[entry]["SampleType"] == "Zinv100" or dict[entry]["SampleType"] == "Zinv200": 
                  inhad_zinv = True
                  self.Had_Zmumu_Yield_Per_Bin[dict[entry]["HT"]]["Yield"] +=  dict[entry]["Yield"]
                  self.Had_Zmumu_Yield_Per_Bin[dict[entry]["HT"]]["TotError"].append(Error)

                else:  
                  inhad_wjet = True
                  if dict[entry]["SampleType"] == "WW":
                    inextras = True
                    self.Had_WW_Yield_Per_Bin[dict[entry]["HT"]]["Yield"] += dict[entry]["Yield"]
                    self.Had_WW_Yield_Per_Bin[dict[entry]["HT"]]["TotError"].append(Error)
                  elif dict[entry]["SampleType"] == "WZ":
                    inextras = True
                    self.Had_WZ_Yield_Per_Bin[dict[entry]["HT"]]["Yield"] += dict[entry]["Yield"]
                    self.Had_WZ_Yield_Per_Bin[dict[entry]["HT"]]["TotError"].append(Error)
                  elif dict[entry]["SampleType"] == "ZZ":
                    inextras = True
                    self.Had_ZZ_Yield_Per_Bin[dict[entry]["HT"]]["Yield"] += dict[entry]["Yield"]
                    self.Had_ZZ_Yield_Per_Bin[dict[entry]["HT"]]["TotError"].append(Error)
                  elif dict[entry]["SampleType"] == "QCDb":
                    inextras = True
                    self.Had_QCD_B_Yield_Per_Bin[dict[entry]["HT"]]["Yield"] += dict[entry]["Yield"]
                    self.Had_QCD_B_Yield_Per_Bin[dict[entry]["HT"]]["TotError"].append(Error)
                  elif dict[entry]["SampleType"] == "TTbar":
                     self.Had_Muon_TTbar_Yield_Per_Bin[dict[entry]["HT"]]["Yield"] +=  dict[entry]["Yield"]
                     self.Had_Muon_TTbar_Yield_Per_Bin[dict[entry]["HT"]]["TotError"].append(Error)
                  elif dict[entry]["SampleType"] == "WJetsInc" or dict[entry]["SampleType"] == "WJets250" or dict[entry]["SampleType"] == "WJets300":
                      self.Had_Muon_WJets_Yield_Per_Bin[dict[entry]["HT"]]["Yield"] +=  dict[entry]["Yield"]
                      self.Had_Muon_WJets_Yield_Per_Bin[dict[entry]["HT"]]["TotError"].append(Error)
                  elif dict[entry]["SampleType"] == "DY":
                      self.Had_DY_Yield_Per_Bin[dict[entry]["HT"]]["Yield"] +=  dict[entry]["Yield"]
                      self.Had_DY_Yield_Per_Bin[dict[entry]["HT"]]["TotError"].append(Error)
                  elif dict[entry]["SampleType"] == "Single_Tbar_tW" or dict[entry]["SampleType"] == "Single_Tbar_t" or dict[entry]["SampleType"] == "Single_T_t" or dict[entry]["SampleType"] == "Single_T_tW" :
                      self.Had_Single_Top_Yield_Per_Bin[dict[entry]["HT"]]["Yield"] +=  dict[entry]["Yield"]
                      self.Had_Single_Top_Yield_Per_Bin[dict[entry]["HT"]]["TotError"].append(Error)
             
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
                elif dict[entry]["SampleType"] == "WJetsInc" or dict[entry]["SampleType"] == "WJets250" or dict[entry]["SampleType"] == "WJets300":
                     self.Muon_WJets_Yield_Per_Bin[dict[entry]["HT"]]["Yield"] +=  dict[entry]["Yield"]
                     self.Muon_WJets_Yield_Per_Bin[dict[entry]["HT"]]["TotError"].append(Error)
                elif dict[entry]["SampleType"] == "DY":
                      self.Muon_DY_Yield_Per_Bin[dict[entry]["HT"]]["Yield"] +=  dict[entry]["Yield"]
                      self.Muon_DY_Yield_Per_Bin[dict[entry]["HT"]]["TotError"].append(Error)
                elif dict[entry]["SampleType"] == "Single_Tbar_tW" or dict[entry]["SampleType"] == "Single_Tbar_t" or dict[entry]["SampleType"] == "Single_T_t" or dict[entry]["SampleType"] == "Single_T_tW" :
                      self.Muon_Single_Top_Yield_Per_Bin[dict[entry]["HT"]]["Yield"] +=  dict[entry]["Yield"]
                      self.Muon_Single_Top_Yield_Per_Bin[dict[entry]["HT"]]["TotError"].append(Error)
                elif dict[entry]["SampleType"] == "WW":
                  inextras = True
                  self.Muon_WW_Yield_Per_Bin[dict[entry]["HT"]]["Yield"] += dict[entry]["Yield"]
                  self.Muon_WW_Yield_Per_Bin[dict[entry]["HT"]]["TotError"].append(Error)
                elif dict[entry]["SampleType"] == "WZ":
                  inextras = True
                  self.Muon_WZ_Yield_Per_Bin[dict[entry]["HT"]]["Yield"] += dict[entry]["Yield"]
                  self.Muon_WZ_Yield_Per_Bin[dict[entry]["HT"]]["TotError"].append(Error)
                elif dict[entry]["SampleType"] == "ZZ":
                  inextras = True
                  self.Muon_ZZ_Yield_Per_Bin[dict[entry]["HT"]]["Yield"] += dict[entry]["Yield"]
                  self.Muon_ZZ_Yield_Per_Bin[dict[entry]["HT"]]["TotError"].append(Error)
                elif dict[entry]["SampleType"] == "QCDb":
                  inextras = True
                  self.Muon_QCD_B_Yield_Per_Bin[dict[entry]["HT"]]["Yield"] += dict[entry]["Yield"]
                  self.Muon_QCD_B_Yield_Per_Bin[dict[entry]["HT"]]["TotError"].append(Error)
                elif dict[entry]["SampleType"] == "Zinv50" or dict[entry]["SampleType"] == "Zinv100" or dict[entry]["SampleType"] == "Zinv200": 
                  inzinv = True
                  self.Muon_Zinv_Yield_Per_Bin[dict[entry]["HT"]]["Yield"] += dict[entry]["Yield"]
                  self.Muon_Zinv_Yield_Per_Bin[dict[entry]["HT"]]["TotError"].append(Error)

            elif dict[entry]["Category"] == "DiMuon":
                indimuon = True
                self.DiMuon_Yield_Per_Bin[dict[entry]["HT"]]["Yield"] +=  dict[entry]["Yield"]
                self.DiMuon_Yield_Per_Bin[dict[entry]["HT"]]["TotError"].append(Error)
                if dict[entry]["SampleType"] == "TTbar":
                     self.DiMuon_TTbar_Yield_Per_Bin[dict[entry]["HT"]]["Yield"] +=  dict[entry]["Yield"]
                     self.DiMuon_TTbar_Yield_Per_Bin[dict[entry]["HT"]]["TotError"].append(Error)
                elif dict[entry]["SampleType"] == "WJetsInc" or dict[entry]["SampleType"] == "WJets250" or dict[entry]["SampleType"] == "WJets300":
                     self.DiMuon_WJets_Yield_Per_Bin[dict[entry]["HT"]]["Yield"] +=  dict[entry]["Yield"]
                     self.DiMuon_WJets_Yield_Per_Bin[dict[entry]["HT"]]["TotError"].append(Error)
                elif dict[entry]["SampleType"] == "DY":
                      self.DiMuon_DY_Yield_Per_Bin[dict[entry]["HT"]]["Yield"] +=  dict[entry]["Yield"]
                      self.DiMuon_DY_Yield_Per_Bin[dict[entry]["HT"]]["TotError"].append(Error)
                elif dict[entry]["SampleType"] == "Single_Tbar_tW" or dict[entry]["SampleType"] == "Single_Tbar_t" or dict[entry]["SampleType"] == "Single_T_t" or dict[entry]["SampleType"] == "Single_T_tW" :
                      self.DiMuon_Single_Top_Yield_Per_Bin[dict[entry]["HT"]]["Yield"] +=  dict[entry]["Yield"]
                      self.DiMuon_Single_Top_Yield_Per_Bin[dict[entry]["HT"]]["TotError"].append(Error)
                elif dict[entry]["SampleType"] == "WW":
                  inextras = True
                  self.DiMuon_WW_Yield_Per_Bin[dict[entry]["HT"]]["Yield"] += dict[entry]["Yield"]
                  self.DiMuon_WW_Yield_Per_Bin[dict[entry]["HT"]]["TotError"].append(Error)
                elif dict[entry]["SampleType"] == "WZ":
                  inextras = True
                  self.DiMuon_WZ_Yield_Per_Bin[dict[entry]["HT"]]["Yield"] += dict[entry]["Yield"]
                  self.DiMuon_WZ_Yield_Per_Bin[dict[entry]["HT"]]["TotError"].append(Error)
                elif dict[entry]["SampleType"] == "ZZ":
                  inextras = True
                  self.DiMuon_ZZ_Yield_Per_Bin[dict[entry]["HT"]]["Yield"] += dict[entry]["Yield"]
                  self.DiMuon_ZZ_Yield_Per_Bin[dict[entry]["HT"]]["TotError"].append(Error)
                elif dict[entry]["SampleType"] == "QCDb":
                  inextras = True
                  self.DiMuon_QCD_B_Yield_Per_Bin[dict[entry]["HT"]]["Yield"] += dict[entry]["Yield"]
                  self.DiMuon_QCD_B_Yield_Per_Bin[dict[entry]["HT"]]["TotError"].append(Error)
                elif dict[entry]["SampleType"] == "Zinv50" or dict[entry]["SampleType"] == "Zinv100" or dict[entry]["SampleType"] == "Zinv200": 
                  inzinv = True
                  self.DiMuon_Zinv_Yield_Per_Bin[dict[entry]["HT"]]["Yield"] += dict[entry]["Yield"]
                  self.DiMuon_Zinv_Yield_Per_Bin[dict[entry]["HT"]]["TotError"].append(Error)


            elif dict[entry]["Category"] == "Photon":
                inphoton = True
                self.Photon_Yield_Per_Bin[dict[entry]["HT"]]["Yield"] +=  dict[entry]["Yield"]
                self.Photon_Yield_Per_Bin[dict[entry]["HT"]]["TotError"].append(Error)
          
        for bin in self.Muon_Yield_Per_Bin: 
          for sample in dictionaries: 
            try:  sample[bin]["SM_Stat_Error"] = math.sqrt(reduce(lambda x,y : x+y,map(lambda x: x*x, sample[bin]["TotError"])))
            except TypeError: pass

        if self.Trigger_Scaling == "True":
          print "Apply MC Correction For Scaling"
          for bin in self.Muon_Yield_Per_Bin:
            for had_sample in had_dict:
              had_sample[bin]["Yield"] = MC_Scaler(bin,had_sample[bin]['AlphaT'],had_sample[bin]["Yield"],sample = "Had")
              had_sample[bin]["SM_Stat_Error"] = MC_Scaler(bin,had_sample[bin]['AlphaT'],had_sample[bin]["SM_Stat_Error"],sample = "Had",error = had_sample[bin]["Yield"])
            for muon_sample in muon_dict:
              muon_sample[bin]["Yield"] = MC_Scaler(bin,muon_sample[bin]['AlphaT'],muon_sample[bin]["Yield"],sample = "Muon",Keep_AlphaT = self.Keep_AlphaT)
              muon_sample[bin]["SM_Stat_Error"] = MC_Scaler(bin,muon_sample[bin]['AlphaT'],muon_sample[bin]["SM_Stat_Error"],sample = "Muon",error = muon_sample[bin]["Yield"],Keep_AlphaT = self.Keep_AlphaT)

       
        if inhad_wjet and indimuon and inmuon and inhad_zinv:
          category = "Combined_SM"
          self.Table_Prep(self.Muon_Yield_Per_Bin,self.Had_Muon_Yield_Per_Bin, comb = self.DiMuon_Yield_Per_Bin, comb_test=self.Had_Zmumu_Yield_Per_Bin)
          self.Produce_Tables(self.Dict_For_Table,category = category, dict2 = self.Combination_Pred_Table,alphat_slice=str(slices))

        if inhad_wjet and inphoton and inmuon and inhad_zinv:
          category = "Combined_SM_Photon"
          self.Table_Prep(self.Muon_Yield_Per_Bin,self.Had_Muon_Yield_Per_Bin, comb = self.Photon_Yield_Per_Bin, comb_test=self.Had_Zmumu_Yield_Per_Bin)
          self.Produce_Tables(self.Dict_For_Table,category = category, dict2 = self.Combination_Pred_Table,alphat_slice=str(slices))

        if inmuon and inhad_zinv and inhad_wjet:
          category = "Total_SM"
          self.Table_Prep(self.Muon_Yield_Per_Bin,self.Had_Yield_Per_Bin,category=category)
          self.Produce_Tables(self.Dict_For_Table,category = category,alphat_slice=str(slices))

        if inhad_wjet and inmuon:
          category = "Muon"
          self.Table_Prep(self.Muon_Yield_Per_Bin,self.Had_Muon_Yield_Per_Bin,category=category)
          self.Produce_Tables(self.Dict_For_Table,category = category,alphat_slice=str(slices))

        if inphoton and inhad_zinv:
          category = "Photon_Zinv"
          self.Table_Prep(self.Photon_Yield_Per_Bin,self.Had_Zmumu_Yield_Per_Bin,category=category)
          self.Produce_Tables(self.Dict_For_Table,category = category,alphat_slice=str(slices))

        if inhad_zinv and indimuon:
          category = "Di_Muon_Zinv"
          self.Table_Prep(self.DiMuon_Yield_Per_Bin,self.Had_Zmumu_Yield_Per_Bin,category=category)
          self.Produce_Tables(self.Dict_For_Table,category = category,alphat_slice=str(slices))

        if inmuon and indimuon:
          category = "Di_Muon"
          self.Table_Prep(self.Muon_Yield_Per_Bin,self.DiMuon_Yield_Per_Bin)
          self.Produce_Tables(self.Dict_For_Table,category = category,alphat_slice=str(slices))

        if inphoton and indimuon:
          category = "Photon_DiMuon"
          self.Table_Prep(self.Photon_Yield_Per_Bin,self.DiMuon_Yield_Per_Bin)
          self.Produce_Tables(self.Dict_For_Table,category = category,alphat_slice=str(slices))

        if inphoton and inmuon:
          category = "Photon_Muon"
          self.Table_Prep(self.Photon_Yield_Per_Bin,self.Muon_Yield_Per_Bin)
          self.Produce_Tables(self.Dict_For_Table,category = category,alphat_slice=str(slices))

        if inhad_zinv or inhad_wjet: 
          category = "Jad_Had_Tables"
          self.Table_Prep(self.Photon_Yield_Per_Bin,self.Muon_Yield_Per_Bin)
          self.Produce_Tables(self.Dict_For_Table,category = category,alphat_slice=str(slices))
        if inmuon:
          category = "Jad_Muon_Tables"
          self.Table_Prep(self.Photon_Yield_Per_Bin,self.Muon_Yield_Per_Bin)
          self.Produce_Tables(self.Dict_For_Table,category = category,alphat_slice=str(slices))
        if indimuon:
          category = "Jad_DiMuon_Tables"
          self.Table_Prep(self.Photon_Yield_Per_Bin,self.Muon_Yield_Per_Bin)
          self.Produce_Tables(self.Dict_For_Table,category = category,alphat_slice=str(slices))
        
        category = "Data_Numbers"
        self.Table_Prep(self.Photon_Yield_Per_Bin,self.Muon_Yield_Per_Bin)
        self.Produce_Tables(self.Dict_For_Table,category=category,alphat_slice=str(slices))

        # Additional Functions Jads Closure Tests, Stat File Root Maker
        if self.Make_Closure_Tests == "True" :self.Jad_Output(jad_dictionaries)    
        if self.Make_Root_Stats_File == "True": self.Format_Stats_Root_Output(dictionaries,settings)
        
  def Jad_Output(self,input):
    print "\n\n"
    for file in input:
      print input
      print "\n\n\n\n"
      self.c_file.append(file)

  def Begin_Stats_Root_Output(self,settings): 
      Lumi = (self.Settings["Lumo"]*1000)
      Photon_Lumi = 4650
      directories = ['had','muon','mumu']
      th1_plots = ["lumiData","lumiMc"]
      th2_plots = ["obs","Zinv","tt","WW","ZZ","t","DY","WZ","WJets"]
            
      self.Stats = r.TFile("RA1_Stats_%s.root" %self.number,"RECREATE") 
      HT_List = []
      Alpha_List = []
      for num in settings["dirs"] : HT_List.append(int(num.split('_')[0]))
      for slice in settings["AlphaTSlices"]:  Alpha_List.append(float(slice.split('_')[0])*100)
      HT_List.append(975)
      Alpha_List.append(60)

      for dir in directories:
        self.Stats.cd("/")
        self.Stats.mkdir(dir)
        self.Stats.cd(dir)
        for hist in th1_plots:
          plot = TH1F(hist,"",1,0,1)
          plot.SetBinContent(1,Lumi)
          if dir == "photon": plot.SetBinContent(1,Photon_Lumi) 
          plot.Write()
        for second_hist in th2_plots:
          plots = r.TH2D(second_hist,"",len(settings["dirs"]),array.array('d',HT_List),len(settings["AlphaTSlices"]),array.array('d',Alpha_List))
          plots.GetXaxis().SetTitle("H_{T} (GeV)")
          plots.GetYaxis().SetTitle("#alpha_{T}")
          plots.GetZaxis().SetTitle("Yield")
          plots.Write()
      self.Stats.cd("/")   
  
  def Format_Stats_Root_Output(self,dictnames,settings):
     
      directories = {"had":{'obs':self.Had_Yield_Per_Bin,'Zinv':self.Had_Zmumu_Yield_Per_Bin,'tt':self.Had_Muon_TTbar_Yield_Per_Bin,'WW':self.Had_WW_Yield_Per_Bin,'ZZ':self.Had_ZZ_Yield_Per_Bin,'WZ':self.Had_WZ_Yield_Per_Bin,'t':self.Had_Single_Top_Yield_Per_Bin,'DY':self.Had_DY_Yield_Per_Bin,'WJets':self.Had_Muon_WJets_Yield_Per_Bin} ,"muon": {'obs':self.Muon_Yield_Per_Bin,'tt':self.Muon_TTbar_Yield_Per_Bin,'WW':self.Muon_WW_Yield_Per_Bin,'ZZ':self.Muon_ZZ_Yield_Per_Bin,'WZ':self.Muon_WZ_Yield_Per_Bin,'t':self.Muon_Single_Top_Yield_Per_Bin,'DY':self.Muon_DY_Yield_Per_Bin,'WJets':self.Muon_WJets_Yield_Per_Bin},"mumu" : {'obs':self.DiMuon_Yield_Per_Bin,'tt':self.DiMuon_TTbar_Yield_Per_Bin,'WW':self.DiMuon_WW_Yield_Per_Bin,'ZZ':self.DiMuon_ZZ_Yield_Per_Bin,'WZ':self.DiMuon_WZ_Yield_Per_Bin,'t':self.DiMuon_Single_Top_Yield_Per_Bin,'DY':self.DiMuon_DY_Yield_Per_Bin,'WJets':self.DiMuon_WJets_Yield_Per_Bin}}
            
      HT_List = []
      Alpha_List = []
      for num in settings["dirs"] : HT_List.append(int(num.split('_')[0]))
      for slice in settings["AlphaTSlices"]:  Alpha_List.append(float(slice.split('_')[0])*100)
      HT_List.append(975)
      Alpha_List.append(60)

      for dir in directories:
        for second_hist in directories[dir]:
          for name in sorted(directories[dir][second_hist].iterkeys()):
            plots = self.Stats.Get("%s/%s"%(dir,second_hist)) 
            self.Stats.cd("%s"%dir)
            if second_hist == 'obs':     
                bin = plots.FindBin(float(name) , float(directories[dir][second_hist][name]["AlphaT"])*100)
                plots.SetBinContent(bin,float(directories[dir][second_hist][name]["Data"]))
                plots.Write("",r.TObject.kOverwrite)
            else:  
                bin = plots.FindBin(float(name) , float(directories[dir][second_hist][name]["AlphaT"])*100)
                plots.SetBinContent(bin,float(directories[dir][second_hist][name]["Yield"]))
                plots.SetBinError(bin,float(directories[dir][second_hist][name]["SM_Stat_Error"]))
                plots.Write("",r.TObject.kOverwrite)

  def Table_Prep(self,control,test,comb="",comb_test="",category=""):

      eh =  [1.15, 1.36, 1.53, 1.73, 1.98, 2.21, 2.42, 2.61, 2.80, 3.00 ]
      el =  [0.00, 1.00, 2.00, 2.14, 2.30, 2.49, 2.68, 2.86, 3.03, 3.19 ]
      self.Dict_For_Table = dict.fromkeys(self.bins)
      self.Combination_Pred_Table = dict.fromkeys(self.bins)
      entries = ('Data_Pred','Prediction','Pred_Error','Data','Data_Error','Trans','Trans_Error')
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
          self.Dict_For_Table[bin]['Trans_Error'] = self.Dict_For_Table[bin]['Trans'] * math.sqrt((control_error*control_error)+(test_error*test_error))
          self.Dict_For_Table[bin]['Data_Pred'] = control[bin]["Data"]
          self.Dict_For_Table[bin]['Data_Error'] = sqrt(control[bin]["Data"]) if control[bin]["Data"] > 9 else float(eh[int(control[bin]["Data"])])
          self.Dict_For_Table[bin]['Prediction'] = control[bin]["Data"]*self.Dict_For_Table[bin]['Trans']
          self.Dict_For_Table[bin]['Data'] = test[bin]["Data"]
          try:self.Dict_For_Table[bin]['Pred_Error'] = self.Dict_For_Table[bin]['Prediction']*math.sqrt(((self.Dict_For_Table[bin]['Data_Error']/self.Dict_For_Table[bin]['Data_Pred'])*(self.Dict_For_Table[bin]['Data_Error']/self.Dict_For_Table[bin]['Data_Pred'])) +((self.Dict_For_Table[bin]['Trans_Error']/self.Dict_For_Table[bin]['Trans'])*(self.Dict_For_Table[bin]['Trans_Error']/self.Dict_For_Table[bin]['Trans'])))
          except ZeroDivisionError: self.Dict_For_Table[bin]['Pred_Error'] = 0

      if comb:
        for bin in control:
          try:self.Combination_Pred_Table[bin]['Trans'] = comb_test[bin]["Yield"]/comb[bin]["Yield"]
          except ZeroDivisionError: pass
          try: control_error =  comb[bin]["SM_Stat_Error"]/comb[bin]["Yield"] 
          except ZeroDivisionError: control_error = 0
          try :test_error =  comb_test[bin]["SM_Stat_Error"]/comb_test[bin]["Yield"] 
          except ZeroDivisionError: test_error = 0
          self.Combination_Pred_Table[bin]['Trans_Error'] = self.Combination_Pred_Table[bin]['Trans'] * math.sqrt((control_error*control_error)+(test_error*test_error))
          self.Combination_Pred_Table[bin]['Data_Pred'] = comb[bin]["Data"]
          self.Combination_Pred_Table[bin]['Data_Error'] = sqrt(comb[bin]["Data"]) if comb[bin]["Data"] > 9 else float(eh[int(comb[bin]["Data"])])
          self.Combination_Pred_Table[bin]['Prediction'] = comb[bin]["Data"]*self.Combination_Pred_Table[bin]['Trans']
          self.Combination_Pred_Table[bin]['Data'] = comb_test[bin]["Data"]
          try:self.Combination_Pred_Table[bin]['Pred_Error'] = self.Combination_Pred_Table[bin]['Prediction']*math.sqrt(((self.Combination_Pred_Table[bin]['Data_Error']/self.Combination_Pred_Table[bin]['Data_Pred'])*(self.Combination_Pred_Table[bin]['Data_Error']/self.Combination_Pred_Table[bin]['Data_Pred'])) +((self.Combination_Pred_Table[bin]['Trans_Error']/self.Combination_Pred_Table[bin]['Trans'])*(self.Combination_Pred_Table[bin]['Trans_Error']/self.Combination_Pred_Table[bin]['Trans'])))
          except ZeroDivisionError: self.Combination_Pred_Table[bin]['Pred_Error'] = 0

      for bin in self.Dict_For_Table:
         if category == "Total_SM": self.Translation_Dict[self.current_slice][bin]["Tot_SM_Trans"] = self.Dict_For_Table[bin]["Trans"] 
         if category == "Muon": self.Translation_Dict[self.current_slice][bin]["Muon_Trans"] = self.Dict_For_Table[bin]["Trans"]  
         if category == "Di_Muon_Zinv":self.Translation_Dict[self.current_slice][bin]["DiMuon_Trans"] = self.Dict_For_Table[bin]["Trans"]  
         if category == "Photon_Zinv":self.Translation_Dict[self.current_slice][bin]["Photon_Trans"] = self.Dict_For_Table[bin]["Trans"]  
             
  def Produce_Tables(self,dict,category="",dict2 ="",alphat_slice=""):
      print "\n\nMaking Tables for %s" % category
      print alphat_slice[:4]
      self.table_reducer = alphat_slice[:4]
      
      if category == "Total_SM": self.Latex_Table(dict,caption = "AlphaT: %s Total SM prediction from Muon sample"%alphat_slice[:4], 
            rows = [{"label": r'''Hadronic selection MC''',"entryFunc": self.MakeList(self.Had_Yield_Per_Bin,"Yield","SM_Stat_Error"),"addhline":True},
                    {"label": r'''WJets Had MC''',"entryFunc": self.MakeList(self.Had_Muon_WJets_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''$t\bar{t}$ Had MC''',"entryFunc": self.MakeList(self.Had_Muon_TTbar_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''Single $t$ Had MC''',"entryFunc": self.MakeList(self.Had_Single_Top_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''DY Had MC''',"entryFunc": self.MakeList(self.Had_DY_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''Zinv Had MC''',"entryFunc": self.MakeList(self.Had_Zmumu_Yield_Per_Bin,"Yield","SM_Stat_Error"),"adddouble":True},
                    {"label": r'''$\mu +$ jets selection MC''',         "entryFunc":self.MakeList(self.Muon_Yield_Per_Bin,"Yield","SM_Stat_Error"),"addhline":True},
                    {"label": r'''WJets Muon MC''',"entryFunc": self.MakeList(self.Muon_WJets_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''$t\bar{t}$ Muon MC''',"entryFunc": self.MakeList(self.Muon_TTbar_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''Single $t$ Muon MC''',"entryFunc": self.MakeList(self.Muon_Single_Top_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''DY Muon MC''',"entryFunc": self.MakeList(self.Muon_DY_Yield_Per_Bin,"Yield","SM_Stat_Error"),"adddouble":True},
                    {"label": r'''Translation factor ''',                "entryFunc":self.MakeList(dict,"Trans","Trans_Error")},
                    {"label": r'''$\mu +$ jets selection yield data''',       "entryFunc":self.MakeList(dict,"Data_Pred")},
                    {"label":r'''Total SM prediction''', "entryFunc":self.MakeList(dict,"Prediction","Pred_Error")},
                    {"label": r'''Hadronic yield data''',       "entryFunc":self.MakeList(dict,"Data")},])
            
      if category == "Muon": self.Latex_Table(dict,caption = "AlphaT: %s TTbar + W prediction from Muon sample"%alphat_slice[:4], 
            rows = [{"label": r'''$t\bar{t}$ + W  Hadronic selection MC''',"entryFunc": self.MakeList(self.Had_Muon_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''$\mu +$ jets selection MC''',         "entryFunc":self.MakeList(self.Muon_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''Translation factor''',                "entryFunc":self.MakeList(dict,"Trans","Trans_Error")},
                    {"label": r'''$\mu +$ jets selection yield data''',       "entryFunc":self.MakeList(dict,"Data_Pred")},
                    {"label":r'''$t\bar{t}$ + W prediction''', "entryFunc":self.MakeList(dict,"Prediction","Pred_Error")},])
            
      if category == "Photon_DiMuon": self.Latex_Table(dict,caption = "AlphaT: %s Photon to predict DiMuon closure test"%alphat_slice[:4], 
            rows = [{"label": r'''$\mu\bar{\mu} +$ jets selection MC''',"entryFunc": self.MakeList(self.DiMuon_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r''' $\gamma +$ jets selection MC''',         "entryFunc":self.MakeList(self.Photon_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''Translation factor''',                "entryFunc":self.MakeList(dict,"Trans","Trans_Error")},
                    {"label": r'''$\gamma +$ jets yield data''',       "entryFunc":self.MakeList(dict,"Data_Pred")},
                    {"label":r'''$\mu\bar{\mu} +$ jets  prediction''', "entryFunc":self.MakeList(dict,"Prediction","Pred_Error")},
                    {"label": r'''$\mu\bar{\mu} +$ jets yield data''',       "entryFunc":self.MakeList(dict,"Data")},])

      if category == "Photon_Muon": self.Latex_Table(dict,caption = "AlphaT: %s Photon to predict Muon closure test"%alphat_slice[:4], 
            rows = [{"label": r'''$\mu + $jets selection  MC''',"entryFunc": self.MakeList(self.Muon_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''$\gamma+$ jets selection MC''',         "entryFunc":self.MakeList(self.Photon_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''Translation factor''',                "entryFunc":self.MakeList(dict,"Trans","Trans_Error")},
                    {"label": r'''$\gamma +$ jets yield data''',       "entryFunc":self.MakeList(dict,"Data_Pred")},
                    {"label":r'''$\mu + $jets prediction''', "entryFunc":self.MakeList(dict,"Prediction","Pred_Error")},
                    {"label": r'''$\mu +$ jets yield data''',       "entryFunc":self.MakeList(dict,"Data")},])

      if category == "Di_Muon": self.Latex_Table(dict,caption = "AlphaT: %s Muon to Predict DiMuon closure test"%alphat_slice[:4], 
            rows = [{"label": r'''$\mu\bar{\mu} +$ jets selection MC''',"entryFunc": self.MakeList(self.DiMuon_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''WJets DiMuon MC''',"entryFunc": self.MakeList(self.DiMuon_TTbar_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''$t\bar{t}$ DiMuon MC''',"entryFunc": self.MakeList(self.DiMuon_WJets_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''Single $t$ DiMuon MC''',"entryFunc": self.MakeList(self.DiMuon_Single_Top_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''DY DiMuon MC''',"entryFunc": self.MakeList(self.DiMuon_DY_Yield_Per_Bin,"Yield","SM_Stat_Error"),"addhline":True},
                    {"label": r'''$\mu +$ jets selection MC''',         "entryFunc":self.MakeList(self.Muon_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''Translation factor''',                "entryFunc":self.MakeList(dict,"Trans","Trans_Error")},
                    {"label": r'''$\mu +$ jets yield data''',       "entryFunc":self.MakeList(dict,"Data_Pred")},
                    {"label":r'''$\mu\bar{\mu} +$ jets selection  prediction''', "entryFunc":self.MakeList(dict,"Prediction","Pred_Error")},
                    {"label": r'''$\mu\bar{\mu} +$ jets selection yield data''',       "entryFunc":self.MakeList(dict,"Data")},])
     
      if category == "Di_Muon_Zinv": self.Latex_Table(dict,caption = "AlphaT: %s Zinv prediction from DiMuon sample "%alphat_slice[:4], 
            rows = [{"label": r'''Z$\rightarrow\nu\bar{\nu}$ hadronic selection MC''',"entryFunc": self.MakeList(self.Had_Zmumu_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''$\mu\bar{\mu} +$ jets selection MC''',         "entryFunc":self.MakeList(self.DiMuon_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''Translation factor''',                "entryFunc":self.MakeList(dict,"Trans","Trans_Error")},
                    {"label": r'''$\mu\bar{\mu} +$ jets selection yield data''',       "entryFunc":self.MakeList(dict,"Data_Pred")},
                    {"label":r'''Z$\rightarrow\nu\bar{\nu}$ prediction''', "entryFunc":self.MakeList(dict,"Prediction","Pred_Error")}])

      if category == "Photon_Zinv": self.Latex_Table(dict,caption = "AlphaT: %s Zinv prediction from Photon sample"%alphat_slice[:4], 
            rows = [{"label": r'''Z$\rightarrow\nu\bar{\nu}$ hadronic selection MC''',"entryFunc": self.MakeList(self.Had_Zmumu_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''$\gamma +$ jets selection MC''',         "entryFunc":self.MakeList(self.Photon_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''Translation factor''',                "entryFunc":self.MakeList(dict,"Trans","Trans_Error")},
                    {"label": r'''$\gamma +$ jet selection yield data''',       "entryFunc":self.MakeList(dict,"Data_Pred")},
                    {"label":r'''Z$\rightarrow\nu\bar{\nu}$ prediction''', "entryFunc":self.MakeList(dict,"Prediction","Pred_Error")}])
               
      if category == "Combined_SM": self.Latex_Table(dict,caption = "AlphaT: %s Total SM Prediction (Muon + DiMuon)"%alphat_slice[:4], 
            rows = [{"label": r'''t$\bar{t}$ + W prediction from $\mu +$ jets''', "entryFunc":self.MakeList(dict,"Prediction","Pred_Error")},
                    {"label": r'''Z$\rightarrow\nu\bar{\nu}$ prediction from $\mu\mu +$ jets''', "entryFunc":self.MakeList(dict2,"Prediction","Pred_Error")},
                    {"label":r'''Total SM prediction''', "entryFunc":self.MakeList(dict,"Prediction","Pred_Error",combined=dict2)},
                    {"label": r'''Hadronic yield from data''',  "entryFunc":self.MakeList(dict,"Data")},])
                   
      if category == "Combined_SM_Photon": self.Latex_Table(dict,caption = "AlphaT: %s Total SM Prediction (Muon + Photon)"%alphat_slice[:4], 
            rows = [{"label": r'''$t\bar{t}$ + W prediction from $\mu +$ jets''', "entryFunc":self.MakeList(dict,"Prediction","Pred_Error")},
                    {"label": r'''$Z\rightarrow\nu\bar{\nu}$ Prediction from $\gamma +$ jets''', "entryFunc":self.MakeList(dict2,"Prediction","Pred_Error")},
                    {"label":r'''Total SM prediction''', "entryFunc":self.MakeList(dict,"Prediction","Pred_Error",combined=dict2)},
                    {"label": r'''Hadronic yield from data''',  "entryFunc":self.MakeList(dict,"Data")},])

      if category == "Jad_Had_Tables": self.Latex_Table(dict,caption = "AlphaT: %s Had Yields and MC Breakdown"%alphat_slice[:4],
            rows = [ {"label": r'''Hadronic yield data''',       "entryFunc":self.MakeList(self.Had_Yield_Per_Bin,"Data")},
                    {"label": r'''Hadronic selection MC''',"entryFunc": self.MakeList(self.Had_Yield_Per_Bin,"Yield","SM_Stat_Error"),"addhline":True},
                    {"label": r'''WJets Had MC''',"entryFunc": self.MakeList(self.Had_Muon_WJets_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''$t\bar{t}$ Had MC''',"entryFunc": self.MakeList(self.Had_Muon_TTbar_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''Single $t$ Had MC''',"entryFunc": self.MakeList(self.Had_Single_Top_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''DY Had MC''',"entryFunc": self.MakeList(self.Had_DY_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''Zinv Had MC''',"entryFunc": self.MakeList(self.Had_Zmumu_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''Had WW''', "entryFunc":self.MakeList(self.Had_WW_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''Had WZ''', "entryFunc":self.MakeList(self.Had_WZ_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label":r'''Had ZZ''', "entryFunc":self.MakeList(self.Had_ZZ_Yield_Per_Bin,"Yield","SM_Stat_Error"),"adddouble":True},])
                    
      if category == "Jad_Muon_Tables": self.Latex_Table(dict,caption = "AlphaT: %s Muon Yields and MC Breakdown"%alphat_slice[:4],
            rows = [ {"label": r'''Muon yield data''',       "entryFunc":self.MakeList(self.Muon_Yield_Per_Bin,"Data")},
                    {"label": r'''Muon selection MC''',"entryFunc": self.MakeList(self.Muon_Yield_Per_Bin,"Yield","SM_Stat_Error"),"addhline":True},
                    {"label": r'''WJets Muon MC''',"entryFunc": self.MakeList(self.Muon_WJets_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''$t\bar{t}$ Muon MC''',"entryFunc": self.MakeList(self.Muon_TTbar_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''Single $t$ Muon MC''',"entryFunc": self.MakeList(self.Muon_Single_Top_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''DY Muon MC''',"entryFunc": self.MakeList(self.Muon_DY_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''Muon WW''', "entryFunc":self.MakeList(self.Muon_WW_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''Muon WZ''', "entryFunc":self.MakeList(self.Muon_WZ_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label":r'''Muon ZZ''', "entryFunc":self.MakeList(self.Muon_ZZ_Yield_Per_Bin,"Yield","SM_Stat_Error"),"adddouble":True},])

      if category == "Jad_DiMuon_Tables": self.Latex_Table(dict,caption = "AlphaT: %s DiMuon Yields and MC Breakdown"%alphat_slice[:4],
            rows = [ {"label": r'''DiMuon yield data''',       "entryFunc":self.MakeList(self.DiMuon_Yield_Per_Bin,"Data")},
                    {"label": r'''DiMuon selection MC''',"entryFunc": self.MakeList(self.DiMuon_Yield_Per_Bin,"Yield","SM_Stat_Error"),"addhline":True},
                    {"label": r'''WJets DiMuon MC''',"entryFunc": self.MakeList(self.DiMuon_WJets_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''$t\bar{t}$ DiMuon MC''',"entryFunc": self.MakeList(self.DiMuon_TTbar_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''Single $t$ DiMuon MC''',"entryFunc": self.MakeList(self.DiMuon_Single_Top_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''DY DiMuon MC''',"entryFunc": self.MakeList(self.DiMuon_DY_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''DiMuon WW''', "entryFunc":self.MakeList(self.DiMuon_WW_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label": r'''DiMuon WZ''', "entryFunc":self.MakeList(self.DiMuon_WZ_Yield_Per_Bin,"Yield","SM_Stat_Error")},
                    {"label":r'''DiMuon ZZ''', "entryFunc":self.MakeList(self.DiMuon_ZZ_Yield_Per_Bin,"Yield","SM_Stat_Error"),"adddouble":True},])
                   
      if category == "Data_Numbers": self.Latex_Table(dict,caption = "AlphaT: %s Data Yields"%alphat_slice[:4],
            rows = [ {"label": r'''Had yield data''',       "entryFunc":self.MakeList(self.Had_Yield_Per_Bin,"Data")},
                    {"label": r'''Muon yield data''',"entryFunc": self.MakeList(self.Muon_Yield_Per_Bin,"Data")},
                    {"label": r'''Di_Muon yield data''',"entryFunc": self.MakeList(self.DiMuon_Yield_Per_Bin,"Data")},]) 

  def MakeList(self,dict,key,error = "",combined = ""):
      List = []
      for entry in sorted(dict.iterkeys()):
        if error: 
          if dict[entry][error] == 0 and dict[entry][key] == 0:List.append('-')
          else: List.append(self.toString("%4.2f" %(dict[entry][key]+combined[entry][key] if combined else dict[entry][key]))+"  $\pm$  "+ self.toString("%4.2f" % (sqrt((dict[entry][error]*dict[entry][error])+(combined[entry][error]*combined[entry][error])) if combined else dict[entry][error])))
        else: 
          if dict[entry][key] == 0: List.append('-')
          else: List.append(self.toString("%4.2f" %(dict[entry][key]+combined[entry][key] if combined else dict[entry][key])))  
      return List  
        
  def oneRow(self,label = "", labelWidth = 23, entryList = [], entryWidth = 30, extra = "",addhline = "",adddouble = "") :
    s = ""
    s += "\n"+label.ljust(labelWidth)+" & "+" & ".join([(self.toString(entry)).ljust(entryWidth) for entry in entryList])+r"\\ "
    if addhline: s += "\n\hline"
    if adddouble: s+="\n\hline\hline"
    return s 

  def toString(self,item) :
    if type(item) is float : return str(item)
    else : return str(item)
  
  def Latex_Table(self,dict,rows,caption = ""):
      s = "\n"
      s += r'''\begin{table}[ht!]'''
      s += "\n\caption{%s %s fb$^{-1}$}"%(caption,str(self.Settings["Lumo"]))
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
          if  self.table_reducer == "0.55" or subTable != 0 or self.table_reducer == "0.01":
      	    s += self.oneRow(label ="$H_{\\textrm{T}}$ Bin (GeV)", entryList = [("%s--%s"%(l, u)) for l,u in zip(bins[:-1], bins[1:])], extra = "[0.5ex]")
            s += "\n\hline" 
            for row in rows:
          	  s += self.oneRow(label = row["label"], entryList = (row["entryFunc"][i] for i in indices),entryWidth=row["entryWidth"] if "entryWidth" in row else 30, addhline=True if "addhline" in row else False,adddouble=True if "adddouble" in row else False)      
      s += "\n\hline"
      s += "\n\end{tabular}"
      s += "\n\end{table}"
      s += "\n\n\n\n"
      self.table.write(s)

