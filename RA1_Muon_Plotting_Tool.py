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

def Data_Scaler(htbin,hist,alphat="",yield_scale="",number_mode=""):
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
          
class Plotter(object):

  def __init__(self):
    #================================== Preamble
    print " Selecting tdr style"
    r.gROOT.ProcessLine(".L tdrstyle.C")
    r.setstyle()
    r.gROOT.SetBatch(True)
    r.gStyle.SetOptStat(0)
    #==================================
    self.ParseOptions()
    self.splash_screen()
    if self.options.Make_Plots is True: 
      self.Hist_Getter(self.options.Root_File)
      self.Plotting_Option()
    else : print "\n\nNot Making Plots then\n\n"

  def splash_screen(self):
    print "\n|============================================================================|"
    print "| XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX |"
    print "|==================  STARTING  BINNED ALPHA T PLOTTING ======================|"
    print "| XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX |"
    print "|============================================================================|"

  def ParseOptions(self):
    parser = OptionParser()
    parser.add_option("-r","--ratios",dest="Make_Ratios",action = "store_true",default=False,help="Make Ratios Plots")
    parser.add_option("-f","--file",dest="Root_File",default=False,help="Root File To Make Plots From")
    parser.add_option("-m","--mcfile",dest="MC_File",default=False,help="Monte Carlo To Make Plots From")
    parser.add_option("-w","--wjetsfile",dest="WJets_File",default=False,help="WJets MC To Make Plots From")
    parser.add_option("-z","--zinvfile",dest="Zinv_File",default=False,help="Zinv MC To Make Plots From")
    parser.add_option("-q","--qcdfile",dest="QCD_File",default=False,help="QCD MC To Make Plots From")
    parser.add_option("-t","--ttbarfile",dest="TTbar_File",default=False,help="TTbar MC To Make Plots From")
    parser.add_option("-d","--dimuonfile",dest="DiMuon_File",default=False,help="DiMuon MC To Make Plots From")
    parser.add_option("-a","--alphat",action = "store_const", const ="alphat", dest="runmode",default=False,help="Binned Alpha T Mode")
    parser.add_option("-c","--control_muon",action = "store_const", const = "muon", dest="runmode",default=False,help="Binned Muon Control Mode")
    parser.add_option("-b","--muon_numbers",action = "store_const", const = "default", dest="runmode",default=False,help="3 Binned Muon Sample")
    parser.add_option("-i","--lumo",dest="Lumo",default=0.1,help="Set Luminosity")
    parser.add_option("-p","--plots",action = "store_false",dest="Make_Plots",default=True,help="Turn plotting off")
    parser.add_option("-l","--leg",action = "store_false",dest="Make_Legend",default=True,help="Draw Legend (Default True)")
    parser.add_option("-n","--numbers",dest="Make_Predictions",default=False,help="Make Numbers, Input txt file with list of MC")
    (self.options,self.args) = parser.parse_args()

  def Hist_Getter(self,file):
       temp =  r.TFile.Open(file)
       DirKeys = temp.GetListOfKeys()
       self.Path_List =[]
       self.Hist_List = []
       for key in DirKeys:
         subdirect = temp.FindObjectAny(key.GetName())
         if subdirect.GetName() == "susyTree" : pass      
         else :
          for subkey in subdirect.GetListOfKeys() :
           if subkey.GetName() != "tree":
               self.Path_List.append("%s/%s" % (subdirect.GetName(),subkey.GetName()))        
       Hist_In_Folder =temp.Get(self.Path_List[0])
       HistNames = Hist_In_Folder.GetListOfKeys() 
       for hist in HistNames: self.Hist_List.append(hist.GetName())
       temp.Close("R")
     
  def ensure_dir(self,dir):
    try: os.makedirs(dir)
    except OSError as exc: pass
  
  def Directory_Maker(self):
    if self.options.runmode == "muon":htBins = [275,325,375,475,575,675,775,875,'inf']
    if self.options.runmode == "alphat":htBins = [275,325,375,475,575,675,775,875,'inf']
    if self.options.runmode == "default":htBins = [275,325,375,'inf']
    self.Dir_Binning = []
    print "\n Making Directory ::: Plots :::" 
    self.ensure_dir("Plots")
    self.base = os.getcwd()
    os.chdir("Plots")
    owd = os.getcwd()
    for lower,upper in zip(htBins[:-1],htBins[1:]+[None]):
        temp = "%s_%s" %(lower,upper if upper else "")
        make_dir = None
        for i in self.Path_List:
          if temp in i: 
            make_dir = temp
            continue
        if make_dir != None : self.Dir_Binning.append(make_dir)
    
    for path in self.Dir_Binning: 
      self.ensure_dir(path)
      os.chdir(path)
      for h in self.Hist_List: self.ensure_dir(str(h))
      os.chdir(owd)

  def Plotting_Option(self):
     if self.options.runmode:
        hist_dict = {}
        self.Directory_Maker()
        for histpath in self.Path_List:
          hist_dict[histpath] = self.Hist_List
          for name in hist_dict[histpath]: 
            for ht in self.Dir_Binning:
              if ht in histpath : self.Make_Plots(ht,name,histpath)
        self.Webpage_Maker(self.Hist_List,self.Dir_Binning,option=self.options.runmode)
        os.chdir(self.base)
  
  def Make_Plots(self,htbin,histname,rootpath):
      print "At Histogram %s %s" %(rootpath,histname)
      DataFile =  r.TFile.Open("../%s" %self.options.Root_File)
      plot  = DataFile.Get("%s/%s" %(rootpath, histname)) 
      c1 = r.TCanvas("canvas"+str(rootpath),"canname"+str(histname),1200,1200) 
      c1.cd(1)
      self.iflog = 0
      self.reversed = 0
      self.histclone_keeper = []
      self.max_maker = [plot]
      plot.SetMarkerStyle(20)
      Data_Scaler(htbin,plot,alphat=(rootpath.split("/")[0]).split('_alphaT_')[1], yield_scale = self.options.runmode)
      self.Hist_Options(histname,plot,canvas = c1,word=True)
      if self.options.Make_Legend is True: 
        self.Legend_Maker()
        self.leg.AddEntry(plot,"Data","L")
      self.MC_Draw(rootpath,histname)
      self.yaxis_maximiser(plot)
      self.Drawer(self.max_maker) 
      self.leg.Draw("SAME")
      self.TextBox(plot,rootpath.split("/")[0])
      c1.SaveAs("%s/%s/%s_%s.png" %(htbin,histname,histname,rootpath.split("/")[0]))
      if self.reversed ==1:
        self.ReversedDrawer(histname,c1,self.histclone_keeper,rootpath)        
        c1.SaveAs("%s/%s/%s_%s_reversed.png" %(htbin,histname,histname,rootpath.split("/")[0]))
      DataFile.Close()
      if self.options.MC_File: self.MCFile.Close()
      if self.options.WJets_File: self.WJetsFile.Close()
      if self.options.TTbar_File: self.TTbarFile.Close()
      if self.options.Zinv_File: self.ZinvFile.Close()
      if self.options.QCD_File: self.QCDFile.Close()
      if self.options.DiMuon_File: self.DiMuonFile.Close()

  def Drawer(self,hist_collection):
    for num,plot in enumerate(hist_collection):
      if num == 0 :
        if type(plot) == type(TH2D()): plot.Draw("P")
        else : plot.Draw("PE0") 
      else: plot.Draw("HISTSAME")

  def ReversedDrawer(self,histname,canvas,hist_collection,rootpath):
    for num,plot in enumerate(hist_collection):
      if num == 0 :self.Hist_Options(histname,plot,canvas = canvas,norebin=true)
      else: self.Hist_Options(histname,plot,norebin=true)
      self.yaxis_maximiser(hist_collection[0])
      self.Drawer(hist_collection)
      self.leg.Draw("SAME")
      self.TextBox(hist_collection[0],rootpath.split("/")[0])

  def yaxis_maximiser(self,plot):
      highest = 0
      if type(plot) != type(TH2D()):
        for max in self.max_maker:
          temp = max.GetMaximum()
          if temp > highest: highest = temp
        if self.iflog: self.ymax = highest * 10
        else: self.ymax = highest * 1.5
        self.max_maker[0].GetYaxis().SetRangeUser(self.iflog,self.ymax)

  def TextBox(self,plot,htbin):
    Textbox = TLatex()
    Textbox.SetNDC()
    Textbox.SetTextAlign(12)
    Textbox.SetTextSize(0.04)
    Textbox.DrawLatex(0.1,0.95, htbin)

  def MC_Draw(self,rootpath,histname):
      if self.options.MC_File:
        self.MCFile = r.TFile.Open("../%s" %self.options.MC_File)
        self.Add_MCplot("mc_plot",rootpath,histname,3,"SM Combined",self.MCFile)
      if self.options.WJets_File: 
        self.WJetsFile = r.TFile.Open("../%s" %self.options.WJets_File)
        self.Add_MCplot("wjet_plot",rootpath,histname,4,"WJets",self.WJetsFile) 
      if self.options.Zinv_File:
        self.ZinvFile = r.TFile.Open("../%s" %self.options.Zinv_File) 
        self.Add_MCplot("zinv_plot",rootpath,histname,5,"Zinv",self.ZinvFile) 
      if self.options.TTbar_File: 
        self.TTbarFile = r.TFile.Open("../%s" %self.options.TTbar_File) 
        self.Add_MCplot("ttbar_plot",rootpath,histname,2,"TTbar",self.TTbarFile)  
      if self.options.QCD_File: 
        self.QCDFile = r.TFile.Open("../%s" %self.options.QCD_File) 
        self.Add_MCplot("qcd_plot",rootpath,histname,6,"QCD",self.QCDFile)
      if self.options.DiMuon_File: 
        self.DiMuonFile = r.TFile.Open("../%s" %self.options.DiMuon_File) 
        self.Add_MCplot("dimuon_plot",rootpath,histname,6,"Zmumu",self.DiMuonFile)

  def Add_MCplot(self,mcplot,rootpath,histname,color,leg_entry,File):
      mcplot  = File.Get("%s/%s" %(rootpath, histname))
      mcplot.SetLineColor(int(color))
      self.leg.AddEntry(mcplot,str(leg_entry),"L")
      mcplot.Scale(float(self.options.Lumo)*10)
      mcplot.SetLineWidth(3)
      self.Hist_Options(histname,mcplot)
      self.max_maker.append(mcplot)

  def Legend_Maker(self): 
      self.leg = r.TLegend(0.67,0.67,0.91,0.85)
      title = "\int L dt = %s fb^{-1}" % self.options.Lumo
      self.leg.SetHeader(title)
      self.leg.SetShadowColor(0)
      self.leg.SetBorderSize(0)
      self.leg.SetFillColor(0)
      self.leg.SetLineColor(0)

  def Webpage_Maker(self,plotnames,foldername,option="",alphat_bin=""):
      print "\n       ================================" 
      print "       ======== Making Webpage ========"
      print "       ********************************\n\n"
      self.webdir = str(option)+"_plots_"+strftime("%d_%b_%H")
      self.ensure_dir("../"+self.webdir)
      for root,dirs,files in os.walk('.'):
        for filename in fnmatch.filter(files,'*.png'):
            name = os.path.join(root,filename)
            os.system('cp ' +name+ ' ../'+self.webdir+'/')
      
      if option == "muon":
        for i in plotnames:
            counter = 0
            htF = open('../'+self.webdir+'/'+i+'.html','w')
            htF.write('Author: Darren Burton <br> \n')
            htF.write('<script language="Javascript"> \n document.write("Last Modified: " + document.lastModified + ""); \n </script> <br> \n ')
            htF.write('<center>\n <p> \n <font size="5"> Binned Muon Control Sample </font>\n </p>\n') 
            htF.write('<font size="3">Results for '+i+' </font><br> \n')
            htF.write('Hist Name: ') 
            for k in plotnames:
              counter += 1
              htF.write('<a href=\"'+k+'.html\">'+k+'</a>    ')
              if counter == 10:
                htF.write('<br> \n')
                counter = 0
            htF.write('<br> \n')

            for root,dirs,files in os.walk('../'+self.webdir):
              sorter = []
              for filenames in fnmatch.filter(files,i+'_*.png'): 
                sorter.append(filenames)
                sorter.sort()
              for plot in sorter: htF.write('<a href='+plot+'><img height=\"400\" src=\"'+plot+'\"></a> \n') 

      if option == "alphat":
        self.alphat_slices = {'51':"0.51-0.52",'52':"0.52-0.53",'53':"0.53-0.55","55":"0.55-0.60","6":"0.60-inf"}
        self.Alpha_Webpage(foldername,plotnames,link="52",outertitle="AlphaT Slices:  ")
        self.Alpha_Webpage(self.alphat_slices,plotnames,link=foldername[0],outertitle="HTBins:  ",slice="True")

  def Alpha_Webpage(self,outer,inner,link="",outertitle="",slice=""):
 
        for i in outer:
          for j in inner:
            counter = 0
            htF = open('../'+self.webdir+'/'+j+'_'+i+'.html','w')
            htF.write('Author: Darren Burton <br> \n')
            htF.write('<script language="Javascript"> \n document.write("Last Modified: " + document.lastModified + ""); \n </script> <br> \n ')
            htF.write('<center>\n <p> \n <font size="5"> Binned Alpha T </font>\n </p>\n') 
            htF.write('<font size="3">Results for '+j+'_'+i+' </font><br> \n')
            htF.write('Hist Name: ')
            for k in inner:
              counter += 1
              htF.write('<a href=\"'+k+'_'+i+'.html\">'+k+'</a>   ')
              if counter == 10:
                htF.write('<br> \n')
                counter = 0
            htF.write('<br> \n')
            htF.write('<br> \n')
            htF.write(outertitle)
            for k in outer: htF.write('<a href=\"'+j+'_'+k+'.html\">'+(self.alphat_slices[k] if slice else k)+'</a>     /    ')
            htF.write('<br> \n')
            htF.write('<br> \n')
            htF.write('Change Evolution Type: <a href=\"'+j+'_'+link+'.html\">'+ ('HT Evolution' if slice else 'Alpha T Evolution')+'</a>')
            htF.write('<br> \n')
             
            for root,dirs,files in os.walk('../'+self.webdir):
              sorter = []
              for filenames in fnmatch.filter(files,j+('_*_alpha*_*' if slice else '_*')+i+'*.png'):
                sorter.append(filenames)
                sorter.sort()
              for plot in sorter: htF.write('<a href='+plot+'><img height=\"400\" src=\"'+plot+'\"></a> \n') 

  def Hist_Options(self,histogram,plot,canvas="",word = "",norebin=""):
 
        if word: print "Applying %s Options" % histogram

        if histogram == "HT":
          plot.Rebin(25)
          self.OverFlow_Bin(plot,250,2000,1250)

        if histogram == "MT":
          plot.Rebin(50)
          self.OverFlow_Bin(plot,0,1000,800)

        if histogram == "NVertices":pass

        if histogram == "aT_H":
          if canvas: self.Log_Setter(plot,canvas,0.1) 
          if not norebin: 
            plot.Rebin(25)
            self.OverFlow_Bin(plot,0.4,10,3.0)
            self.Reversed_Integrator(plot)
        
        if histogram == "aT_L":
          if canvas: self.Log_Setter(plot,canvas,0.1)
          if not norebin:
            plot.Rebin(5)
            self.OverFlow_Bin(plot,0.4,10,3.0)
            self.Reversed_Integrator(plot)  
            
        if histogram == "nJet": pass
        
        if histogram == "HTlep":
          plot.Rebin(10)
          self.OverFlow_Bin(plot,0,2000,1000)
        
        if histogram == "MHT":
          plot.Rebin(50)
          self.OverFlow_Bin(plot,0,2000,1400)

        if histogram == "MuPhi": plot.Rebin(2)

        if histogram == "MuPt":
          plot.Rebin(25)
          self.OverFlow_Bin(plot,10,2010,1010)

        if histogram == "MuEta":pass

        if histogram == "MuDR": plot.Rebin(10)

        if histogram == "Meff":
          plot.Rebin(25)
          self.OverFlow_Bin(plot,0,2000,1200)

        if histogram == "MuTrIso":  
          if canvas: self.Log_Setter(plot,canvas,0.1) 
          plot.Rebin(50)
          self.OverFlow_Bin(plot,0.0,2.0,1)

        if histogram == "MuEIso": 
          if canvas : self.Log_Setter(plot,canvas,0.1) 
          plot.Rebin(50)
          self.OverFlow_Bin(plot,0.0,2.0,1.0)

        if histogram == "MuHIso": 
          if canvas : self.Log_Setter(plot,canvas,0.1)
          plot.Rebin(50)
          self.OverFlow_Bin(plot,0.0,2.0,1.0)

        if histogram == "MuCso": 
          if canvas : self.Log_Setter(plot,canvas,0.1)
          plot.Rebin(50)
          self.OverFlow_Bin(plot,0,2.0,1.5)

        if histogram == "MuiVHits": self.OverFlow_Bin(plot,0,50,40)

        if histogram == "MugVHits": self.OverFlow_Bin(plot,0,100,70)

        if histogram ==  "MuBD0": plot.Rebin(100)

        if histogram ==  "MuVD0": plot.Rebin(100)

        if histogram ==  "MuVD0Sig": plot.Rebin(10)
  
  def Log_Setter(self,plot,canvas,min):
      self.iflog = 0.1
      plot.SetMinimum(float(min))
      canvas.SetLogy(1)

  def OverFlow_Bin(self,hist,xmin,xmax,overflow):
      overflow_bin = int(float(overflow)/float(xmax) * hist.GetNbinsX())
      set_overflow = float(hist.Integral(overflow_bin,hist.GetNbinsX())) 
      hist.SetBinContent(overflow_bin + 1,set_overflow)
      hist.SetBinError(overflow_bin + 1,sqrt(set_overflow))
      hist.SetAxisRange(xmin,overflow,"X")

  def Reversed_Integrator(self,hist):
      self.histclone = hist.Clone()
      integral_keeper = []
      self.reversed = 1
      for i in range(self.histclone.GetNbinsX()): integral_keeper.append(self.histclone.Integral(self.histclone.GetNbinsX()-i,self.histclone.GetNbinsX()))
      for k in range(self.histclone.GetNbinsX()): 
        self.histclone.SetBinContent(self.histclone.GetNbinsX()-k,integral_keeper[k])  
        self.histclone.SetBinError(self.histclone.GetNbinsX()-k,sqrt(integral_keeper[k]))
      self.histclone_keeper.append(self.histclone)  

class Number_Extractor(object):

  def __init__(self):
    if a.options.Make_Predictions:  self.Get_Numbers()
    else : pass

  def Get_Numbers(self):
    print "\n\nGetting Numbers\n\n"
    self.File_List()
    self.Get_Binning(self.Input_Files)
    self.Print_Binning()
    if a.options.Make_Predictions : self.Prediction_Maker(self.Final_Info)
    if a.options.runmode: self.Make_2D_Data_Table(self.Final_Info)

  def File_List(self):
    self.Input_Files = []
    self.SampleInfo = {}
    MC_Weights = {"TTbar":0.00425452,"WJetsInc":0.0666131,"WJets250":0.000450549,"WJets300":0.00102329,"Zinv50":0.00485311,"Zinv100":0.00410382,"Zinv200":0.0013739,"Zmumu":0.00849073,"Data":1.}

    self.f = open(a.options.Make_Predictions, "r")
    for line in self.f.readlines():
      entry = line.strip('\n')
      self.Input_Files.append(entry)
      self.SampleInfo[entry] = {"SampleType":(entry.split('_')[1]).split('.')[0],"AnalysisType":entry.split('_')[0],"Weight":MC_Weights[(entry.split('_')[1]).split('.')[0]] }
  
  def Get_Binning(self,file):

       self.Final_Info = {}
       for input in file:
         self.Bin_List = []
         Path_Bin_List =[]
         temp =  r.TFile.Open(input)
         DirKeys = temp.GetListOfKeys()
         for key in DirKeys:       
           subdirect = temp.FindObjectAny(key.GetName())
           if subdirect.GetName() == "susyTree" : pass      
           else :
            self.Bin_List.append(key.GetName())
            for subkey in subdirect.GetListOfKeys() :
             if subkey.GetName() != "tree":
                 Path_Bin_List.append("%s/%s" % (subdirect.GetName(),subkey.GetName()))        
         Hist_In_Folder =temp.Get(Path_Bin_List[0])
         HistNames = Hist_In_Folder.GetListOfKeys()
         for hist in HistNames:
            if hist.GetName() == "HT": 
                for path in Path_Bin_List:
                  try :
                    Bin_Info = {"Category":0,"SampleType":0,"HT":0,"AlphaT":0,"Yield":0,"MC_Weight":0,"Yield_Error":0}
                    Grab_Integral = temp.Get("%s/%s" %(path,hist.GetName()))
                    Bin_Info["SampleType"] = self.SampleInfo[input]["SampleType"]
                    Bin_Info["Category"] = self.SampleInfo[input]["AnalysisType"]
                    Bin_Info["MC_Weight"] = self.SampleInfo[input]["Weight"]
                    Bin_Info["Yield"] = (Grab_Integral.Integral()*Data_Scaler((path.split('/')[0]).split('_alphaT_')[0],hist, alphat = (path.split('/')[0]).split('_alphaT_')[1],  yield_scale=a.options.runmode,number_mode=True) if self.SampleInfo[input]["SampleType"] == "Data" else Grab_Integral.Integral()*10*float(a.options.Lumo))
                    Bin_Info["Yield_Error"] = (m.sqrt(Grab_Integral.Integral()*float(Bin_Info["MC_Weight"]))*10.0*float(a.options.Lumo) if self.SampleInfo[input]["SampleType"] != "Data" else sqrt(float(Bin_Info["Yield"])))

                    Bin_Info["HT"] = (path.split('/')[0]).split('_alphaT_')[0]
                    Bin_Info["AlphaT"] = (path.split('/')[0]).split('_alphaT_')[1]
                    if Bin_Info["AlphaT"] == '6': Bin_Info["AlphaT"] = '60'
                    self.Final_Info["%s_%s/%s" %(self.SampleInfo[input]["AnalysisType"],self.SampleInfo[input]["SampleType"],path)] = Bin_Info
                  except AttributeError:pass
         temp.Close()
  
  def Prediction_Maker(self,dict):
      
      category = "Muon"

      self.Had_Yield_Per_Bin = {'275':{ "Data":0,"Yield":0,"TotError":[],"SM_Stat_Error":0},'325':{ "Data":0,"Yield":0,"TotError":[],"SM_Stat_Error":0  },'375':{ "Data":0,"Yield":0,"TotError":[], "SM_Stat_Error":0 },'475':{ "Data":0, "Yield":0,"TotError":[], "SM_Stat_Error":0  },'575':{ "Data":0,"Yield":0,"TotError":[], "SM_Stat_Error":0 },'675':{ "Data":0,"Yield":0,"TotError":[], "SM_Stat_Error":0  },'775':{ "Data":0, "Yield":0,"TotError":[], "SM_Stat_Error":0  },'875':{ "Data":0, "Yield":0,"TotError":[], "SM_Stat_Error":0} }

      self.Muon_Yield_Per_Bin = {'275':{ "Data":0,"Yield":0,"TotError":[],"SM_Stat_Error":0, "Muon_Trans":0,"Di_Muon_Trans":0 },'325':{ "Data":0,"Yield":0,"TotError":[],"SM_Stat_Error":0,"Muon_Trans":0,"Di_Muon_Trans":0 },'375':{ "Data":0,"Yield":0,"TotError":[], "SM_Stat_Error":0 ,"Muon_Trans":0,"Di_Muon_Trans":0 },'475':{ "Data":0, "Yield":0,"TotError":[], "SM_Stat_Error":0 , "Muon_Trans":0,"Di_Muon_Trans":0  },'575':{ "Data":0,"Yield":0,"TotError":[], "SM_Stat_Error":0 ,"Muon_Trans":0,"Di_Muon_Trans":0 },'675':{ "Data":0, "Yield":0,"TotError":[], "SM_Stat_Error":0,"Muon_Trans":0,"Di_Muon_Trans":0 },'775':{ "Data":0, "Yield":0,"TotError":[], "SM_Stat_Error":0,"Muon_Trans":0,"Di_Muon_Trans":0 },'875':{ "Data":0, "Yield":0,"TotError":[], "SM_Stat_Error":0,"Muon_Trans":0,"Di_Muon_Trans":0  } }

      self.DiMuon_Yield_Per_Bin = {'275':{ "Data":0,"Yield":0,"TotError":[],"SM_Stat_Error":0 },'325':{ "Data":0,"Yield":0,"TotError":[],"SM_Stat_Error":0  },'375':{ "Data":0,"Yield":0,"TotError":[], "SM_Stat_Error":0 },'475':{ "Data":0, "Yield":0,"TotError":[], "SM_Stat_Error":0  },'575':{ "Data":0,"Yield":0,"TotError":[], "SM_Stat_Error":0 },'675':{ "Data":0, "Yield":0,"TotError":[], "SM_Stat_Error":0  },'775':{"Data":0,  "Yield":0,"TotError":[], "SM_Stat_Error":0  },'875':{ "Data":0, "Yield":0,"TotError":[], "SM_Stat_Error":0} }

      for entry in dict: 
        if dict[entry]["SampleType"] == "Data":
          if dict[entry]["Category"] == "Had": self.Had_Yield_Per_Bin[(dict[entry]["HT"]).split('_')[0]]["Data"] = dict[entry]["Yield"]
          if dict[entry]["Category"] == "Muon": self.Muon_Yield_Per_Bin[(dict[entry]["HT"]).split('_')[0]]["Data"] = dict[entry]["Yield"]
          if dict[entry]["Category"] == "DiMuon": self.DiMuon_Yield_Per_Bin[(dict[entry]["HT"]).split('_')[0]]["Data"] = dict[entry]["Yield"]

        elif dict[entry]["Category"] == "Had" : 
            if dict[entry]["SampleType"] == "Zinv": category = "Total_SM"
            self.Had_Yield_Per_Bin[(dict[entry]["HT"]).split('_')[0]]["Yield"] +=  dict[entry]["Yield"]
            self.Had_Yield_Per_Bin[(dict[entry]["HT"]).split('_')[0]]["TotError"].append(dict[entry]["Yield_Error"])
        elif dict[entry]["Category"] == "Muon":
            self.Muon_Yield_Per_Bin[(dict[entry]["HT"]).split('_')[0]]["Yield"] +=  dict[entry]["Yield"]
            self.Muon_Yield_Per_Bin[(dict[entry]["HT"]).split('_')[0]]["TotError"].append(dict[entry]["Yield_Error"])
        elif dict[entry]["Category"] == "DiMuon":
            category = "Di_Muon"
            self.DiMuon_Yield_Per_Bin[(dict[entry]["HT"]).split('_')[0]]["Yield"] +=  dict[entry]["Yield"]
            self.DiMuon_Yield_Per_Bin[(dict[entry]["HT"]).split('_')[0]]["TotError"].append(dict[entry]["Yield_Error"])
      
      for bin in self.Muon_Yield_Per_Bin:
        Sum_Had = 0
        Sum_Muon = 0
        Sum_DiMuon = 0
        for x in self.Had_Yield_Per_Bin[bin]["TotError"]: Sum_Had += x*x
        self.Had_Yield_Per_Bin[bin]["SM_Stat_Error"] = sqrt(Sum_Had)

        for y in self.Muon_Yield_Per_Bin[bin]["TotError"]: Sum_Muon += y*y
        self.Muon_Yield_Per_Bin[bin]["SM_Stat_Error"] = sqrt(Sum_Muon)

        for z in self.DiMuon_Yield_Per_Bin[bin]["TotError"]: Sum_DiMuon += z*z
        self.DiMuon_Yield_Per_Bin[bin]["SM_Stat_Error"] = sqrt(Sum_DiMuon)
      
      if category == "Di_Muon": self.Table_Prep(self.Muon_Yield_Per_Bin,self.DiMuon_Yield_Per_Bin)
      else: self.Table_Prep(self.Muon_Yield_Per_Bin,self.Had_Yield_Per_Bin)
   
      self.Produce_Tables(self.Dict_For_Table,category = category)
      self.Ratio_Plots(self.Dict_For_Table, category = category)

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

  def Table_Prep(self,control,test):
  
      self.Dict_For_Table = {'275':{'Data_Pred':0,'Prediction':0,'Pred_Error':0,'Data':0,'Trans':0,'Trans_Error':0 }, '325':{'Data_Pred':0,'Prediction':0,'Pred_Error':0,'Data':0,'Trans':0,'Trans_Error':0 }, '375':{'Data_Pred':0,'Prediction':0,'Pred_Error':0,'Data':0,'Trans':0,'Trans_Error':0 }, '475':{'Data_Pred':0,'Prediction':0,'Pred_Error':0,'Data':0,'Trans':0,'Trans_Error':0 }, '575':{'Data_Pred':0,'Prediction':0,'Pred_Error':0,'Data':0,'Trans':0,'Trans_Error':0 }, '675':{'Data_Pred':0,'Prediction':0,'Pred_Error':0,'Data':0,'Trans':0,'Trans_Error':0 }, '775':{'Data_Pred':0,'Prediction':0,'Pred_Error':0,'Data':0,'Trans':0,'Trans_Error':0 }, '875':{'Data_Pred':0,'Prediction':0,'Pred_Error':0,'Data':0,'Trans':0,'Trans_Error':0 } }

      for bin in control: 
          self.Dict_For_Table[bin]['Trans'] = test[bin]["Yield"]/control[bin]["Yield"] 
          control_error =  control[bin]["SM_Stat_Error"]/control[bin]["Yield"] 
          try :test_error =  test[bin]["SM_Stat_Error"]/test[bin]["Yield"] 
          except ZeroDivisionError: test_error = 0
          self.Dict_For_Table[bin]['Trans_Error'] = self.Dict_For_Table[bin]['Trans'] * m.sqrt((control_error*control_error)+(test_error*test_error))
          self.Dict_For_Table[bin]['Data_Pred'] = control[bin]["Data"]
          self.Dict_For_Table[bin]['Prediction'] = control[bin]["Data"]*self.Dict_For_Table[bin]['Trans']
          self.Dict_For_Table[bin]['Data'] = test[bin]["Data"]
          try:self.Dict_For_Table[bin]['Pred_Error'] = self.Dict_For_Table[bin]['Prediction']*m.sqrt((1/self.Dict_For_Table[bin]['Data_Pred'])+((self.Dict_For_Table[bin]['Trans_Error']/self.Dict_For_Table[bin]['Trans'])*(self.Dict_For_Table[bin]['Trans_Error']/self.Dict_For_Table[bin]['Trans'])))
          except ZeroDivisionError: self.Dict_For_Table[bin]['Pred_Error'] = 0

  def Print_Binning(self):
      self.HT_Bin_Total = []
      self.AlphaT_Bin_Total = []
      for name in self.Final_Info:
        if float(self.Final_Info[name]["HT"].split('_')[0]) not in self.HT_Bin_Total : self.HT_Bin_Total.append(float(self.Final_Info[name]["HT"].split('_')[0]))
        if float(self.Final_Info[name]["AlphaT"]) not in self.AlphaT_Bin_Total : self.AlphaT_Bin_Total.append(float(self.Final_Info[name]["AlphaT"]))

      print "Input Types are %s" %len(self.SampleInfo)      
      print "Numbers of HT bins are %s" %len(self.HT_Bin_Total)
      print "Number of Alpha T Slices are %s" %len(self.AlphaT_Bin_Total)

  def Produce_Tables(self,dict,category=""):
      print "\n\nMaking Tables for %s" % category
      self.f = open('LatexTables.tex','w')
      
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
           
      
      self.f.close()

  def MakeList(self,dict,key,error = ""):
      List = []
      for entry in sorted(dict.iterkeys()):
        if error: List.append(self.toString("%4.2f" %dict[entry][key])+"  \pm  "+ self.toString("%4.2f" %dict[entry][error]))
        else: List.append(self.toString("%4.2f" %dict[entry][key]))
      return List  
        
        

  def Make_2D_Data_Table(self,files):
           
      self.HT_Bin_Total.sort()
      self.AlphaT_Bin_Total.sort()
      self.AlphaT_Bin_Total.append(61)
      self.HT_Bin_Total.append(975)
      FinalPlot = r.TH2D("finalPlot","",len(self.HT_Bin_Total)-1,array.array('d',self.HT_Bin_Total),len(self.AlphaT_Bin_Total)-1,array.array('d',self.AlphaT_Bin_Total))
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
      drawhad = False
      drawdimuon = False

      for name in self.Final_Info:
        if self.Final_Info[name]["SampleType"] == "Data" and self.Final_Info[name]["Category"] == "Muon":
          bin = FinalPlot.FindBin(float(self.Final_Info[name]["HT"].split('_')[0]) , float(self.Final_Info[name]["AlphaT"]))
          FinalPlot.SetBinContent(bin,float(self.Final_Info[name]["Yield"]))
        elif self.Final_Info[name]["SampleType"] == "Data" and self.Final_Info[name]["Category"] == "Had":
          bin = HadPlot.FindBin(float(self.Final_Info[name]["HT"].split('_')[0]) , float(self.Final_Info[name]["AlphaT"]))
          HadPlot.SetBinContent(bin,float(self.Final_Info[name]["Yield"]))
          drawhad = True
        elif self.Final_Info[name]["SampleType"] == "Data" and self.Final_Info[name]["Category"] == "DiMuon":
          bin = DiMuonPlot.FindBin(float(self.Final_Info[name]["HT"].split('_')[0]) , float(self.Final_Info[name]["AlphaT"]))
          DiMuonPlot.SetBinContent(bin,float(self.Final_Info[name]["Yield"]))
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
      self.f.write(s)
      print s
      print "\n\n TexTable Output to MakeLatexTables.tex"

if __name__=="__main__":
  a = Plotter()
  Number_Extractor()
