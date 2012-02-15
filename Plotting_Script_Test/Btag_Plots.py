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

class Plotter(object):

  def __init__(self,settings,sample_list):
    #================================== Preamble
    print " Selecting tdr style"
    r.gROOT.ProcessLine(".L tdrstyle.C")
    r.setstyle()
    r.gROOT.SetBatch(True)
    r.gStyle.SetOptStat(0)
    #==================================
    self.settings = settings
    self.sample_list = sample_list
    self.splash_screen()
    self.Hist_Getter(settings,sample_list)
    self.Plotting_Option(settings,sample_list)

  def splash_screen(self):
    print "\n|============================================================================|"
    print "| XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX |"
    print "|==================  STARTING  BINNED ALPHA T PLOTTING ======================|"
    print "| XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX |"
    print "|============================================================================|"

  def ensure_dir(self,dir):
        try: os.makedirs(dir)
        except OSError as exc: pass

  def Hist_Getter(self,settings,sample_list):
       for key,sample in sorted(sample_list.iteritems()):
          if "n" == key[0]:
             self.DATA_FILE = sample[0]
             self.Directory_Name = sample[1]
             temp =  r.TFile.Open(self.DATA_FILE)
             DirKeys = temp.GetListOfKeys()
             self.Path_List =[]
             self.Hist_List = []
             for key in DirKeys:
               subdirect = temp.FindObjectAny(key.GetName())
               for bin in settings["dirs"]:
                dir = sample[1]+bin
                if dir ==  subdirect.GetName():
                  for subkey in subdirect.GetListOfKeys() :
                    if subkey.GetName() in settings["Plots"]:
                      self.Path_List.append("%s/%s" % (subdirect.GetName(),subkey.GetName()))
                      self.Hist_List.append(subkey.GetName())
             temp.Close()
  
  def Directory_Maker(self):
    htBins = self.settings["dirs"]
    self.Dir_Binning = []
    print "\n Making Directory ::: Plots :::" 
    self.ensure_dir("Plots")
    self.base = os.getcwd()
    os.chdir("Plots")
    owd = os.getcwd()
    for bin in htBins: self.Dir_Binning.append(bin)
    for path in self.Dir_Binning: 
      self.ensure_dir(path)
      os.chdir(path)
      for h in self.Hist_List: self.ensure_dir(str(h))
      os.chdir(owd)

  def Plotting_Option(self,settings,sample_list):
        self.Directory_Maker()
        for num,histpath in enumerate(self.Path_List):
          name = self.Hist_List[num]
          ht = (histpath.split('/')[0]).strip(self.Directory_Name)
          self.Make_Plots(ht,name,histpath)
          if ht == "375_475": self.Make_Plots(ht,name,histpath,combine = "True",histpath= (histpath.split('/')[0]).rstrip("375_475")) 
        os.chdir(self.base)
  
  def Make_Plots(self,htbin,histname,rootpath,combine = "",histpath=""):
      print "At Histogram %s %s" %(rootpath,histname)
      self.DataFile =  r.TFile.Open("../%s" %self.DATA_FILE)
      self.Plot_Closer = [self.DataFile]
      plot  = self.DataFile.Get("%s" %rootpath)
      c1 = r.TCanvas("canvas"+str(rootpath),"canname"+str(histname),1200,1200) 
      c1.cd(1)
      if combine == "True":
        for bin in self.settings["dirs"][3:]:
          add_plot = self.DataFile.Get(("%s_%s/%s" %(histpath,bin,histname) if histpath !="" else "%s%s/%s" %(histpath,bin,histname) ))
          plot.Add(add_plot,1)
      else: plot  = self.DataFile.Get("%s" %rootpath) 
      self.iflog = 0
      self.reversed = 0
      self.histclone_keeper = []
      self.total_mc_maker = []
      self.max_maker = [plot]
      self.draw_error = []
      plot.SetMarkerStyle(20)
      self.Hist_Options(histname,plot,canvas = c1,word=True)
      self.Legend_Maker()
      self.leg.AddEntry(plot,"Data","P")
      self.MC_Draw(rootpath,histname, histpath = histpath,combine = combine)
      self.Draw_Total_MC(self.total_mc_maker)
      self.yaxis_maximiser(plot)
      self.Drawer(self.max_maker)
      self.Drawer(self.draw_error,error="True")
      self.leg.Draw("SAME")
      self.TextBox(plot,(rootpath.split("/")[0] if not combine else (rootpath.split("/")[0]).rstrip("475")))
      self.TagBox()
      if combine == "True": c1.SaveAs("%s/%s/%s_%s_upwards.png" %(htbin,histname,histname,(rootpath.split("/")[0]).rsplit('_',1)[0]))
      else: c1.SaveAs("%s/%s/%s_%s.png" %(htbin,histname,histname,rootpath.split("/")[0]))     
      if self.reversed ==1:
        self.ReversedDrawer(histname,c1,self.histclone_keeper,rootpath)
        if combine == "True": c1.SaveAs("%s/%s/%s_%s_upwards_reversed.png" %(htbin,histname,histname,(rootpath.split("/")[0]).rsplit('_',1)[0]))
        else: c1.SaveAs("%s/%s/%s_%s_reversed.png" %(htbin,histname,histname,rootpath.split("/")[0]))
      for file in self.Plot_Closer: file.Close()
  
  def Draw_Total_MC(self,mc_list):
    for num,hist in enumerate(mc_list):
      if num == 0:
        totmcplot = hist.Clone()
      else: 
        totmcplot.Add(hist)
    errorbarplot = TGraphErrors(totmcplot)
    errorbarplot.SetFillColor(3)
    errorbarplot.SetFillStyle(3008)
    self.draw_error.append(errorbarplot)
    totmcplot.SetLineColor(3)
    self.leg.AddEntry(totmcplot,"Combined SM","L")
    totmcplot.SetLineWidth(3)
    self.max_maker.append(totmcplot)

  def Drawer(self,hist_collection,error=''):
    for num,plot in enumerate(hist_collection):
      if error:
        plot.Draw("SAME2")
      else: 
        if num == 0:
          if type(plot) == type(TH2D()): plot.Draw("P")
          else :  plot.Draw("PE0") 
        else: plot.Draw("HISTSAME")

  def ReversedDrawer(self,histname,canvas,hist_collection,rootpath):
    for num,plot in enumerate(hist_collection):
      if num == 0 :self.Hist_Options(histname,plot,canvas = canvas,norebin=true)
      else: self.Hist_Options(histname,plot,norebin=true)
      self.yaxis_maximiser(hist_collection[0])
      self.Drawer(hist_collection)
      self.leg.Draw("SAME")
      self.TextBox(hist_collection[0],rootpath.split("/")[0])
      self.TagBox()
  
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

  def TagBox(self):
    Textbox = TLatex()
    title = "CMS Preliminary 2012"
    lumi= "\int L dt = %s fb^{-1}" % (self.settings['Lumo']/10)
    Textbox.SetNDC()
    Textbox.SetTextAlign(12)
    Textbox.SetTextSize(0.03)
    Textbox.DrawLatex(0.6,0.85,title )
    Textbox.DrawLatex(0.6,0.79,lumi)

  def Plot_Combiner(self,passed_plot,htbins,histpath,histname,File):
    for bin in htbins:
      another_plot = File.Get(("%s_%s/%s" %(histpath,bin,histname) if histpath !="" else "%s%s/%s" %(histpath,bin,histname) ) )
      passed_plot.Add(another_plot,1)

  def MC_Draw(self,rootpath,histname,histpath,combine = ""):
      for key,sample in sorted(self.sample_list.iteritems()):
        if "n" != key[0]:
          #if sample[2] == "MC Combined":
          #  self.MCFile = r.TFile.Open("../%s" %sample[0])
          #  self.Add_MCplot("mc_plot",rootpath,histname,3,"SM Combined",self.MCFile,histpath,combine=combine)
          if sample[2] == "WJets": 
            self.WJetsFile = r.TFile.Open("../%s" %sample[0])
            self.Add_MCplot("wjet_plot",rootpath,histname,4,"W + Jets",self.WJetsFile,histpath,combine=combine) 
          if sample[2] == "Zinv":
            self.ZinvFile = r.TFile.Open("../%s" %sample[0]) 
            self.Add_MCplot("zinv_plot",rootpath,histname,5,"Z\\rightarrow \\nu\\bar{\\nu}",self.ZinvFile,histpath,combine=combine) 
          if sample[2] == "TTbar": 
            self.TTbarFile = r.TFile.Open("../%s" %sample[0])
            self.Add_MCplot("ttbar_plot",rootpath,histname,2,"t\\bar{t}",self.TTbarFile,histpath,combine=combine)           
          if sample[2] == "Top": 
            self.TopFile = r.TFile.Open("../%s" %sample[0])
            self.Add_MCplot("top_plot",rootpath,histname,2,"t\\bar{t}/ Single t",self.TopFile,histpath,combine=combine)  
        
          if sample[2] == "Di-Boson": 
            self.Di_Boson = r.TFile.Open("../%s" %sample[0])
            self.Add_MCplot("di_boson_plot",rootpath,histname,44,"WW/ZZ/WZ",self.Di_Boson,histpath,combine=combine,style="9")
          if sample[2] == "DY": 
            self.DiMuonFile = r.TFile.Open("../%s" %sample[0])
            self.Add_MCplot("dimuon_plot",rootpath,histname,6,"DY + Jets",self.DiMuonFile,histpath,combine=combine)
          if sample[2] == "Single_Top": 
            self.SingleTopFile = r.TFile.Open("../%s" %sample[0]) 
            self.Add_MCplot("sing_top_plot",rootpath,histname,40,"Single Top",self.SingleTopFile,histpath,combine=combine,style="9")
          if sample[2] == "Photons": 
            self.PhotonFile = r.TFile.Open("../%s" %sample[0])
            self.Add_MCplot("photon_plot",rootpath,histname,8,"\gamma + Jets",self.PhotonFile,histpath,combine=combine)
          if sample[2] == "QCD": 
            self.QCDFile = r.TFile.Open("../%s" %sample[0])
            self.Add_MCplot("qcd_plot",rootpath,histname,7,"QCD",self.QCDFile,histpath,combine=combine,style="10")
          
  def Add_MCplot(self,mcplot,rootpath,histname,color,leg_entry,File,histpath,combine = "",style=""):
      mcplot  = File.Get("%s" %rootpath)
      if combine: self.Plot_Combiner(mcplot,self.settings["dirs"][3:],histpath,histname,File) 
      mcplot.GetSumw2()
      mcplot.Scale(float(self.settings["Lumo"]))
      #Temprory Zinv Scale Factor
      if leg_entry =="Z\\rightarrow \\nu\\bar{\\nu}": mcplot.Scale(1.12/1.28)
      mcplot.SetLineColor(int(color))
      self.leg.AddEntry(mcplot,str(leg_entry),"L")
      mcplot.SetLineWidth(3)
      if style: mcplot.SetLineStyle(int(style))
      self.Hist_Options(histname,mcplot)
      if leg_entry == "QCD" or leg_entry == "SM Combined": 
        errorbarplot = TGraphErrors(mcplot)
        errorbarplot.SetFillColor(int(color))
        errorbarplot.SetFillStyle(3008)
        if style: errorbarplot.SetLineStyle(int(style))
      if leg_entry == "QCD" or leg_entry == "SM Combined": self.draw_error.append(errorbarplot)
      self.max_maker.append(mcplot)
      self.total_mc_maker.append(mcplot)
      self.Plot_Closer.append(File)

  def Legend_Maker(self): 
      self.leg = r.TLegend(0.68,0.53,0.90,0.75) 
      self.leg.SetTextSize(0.02)
      self.leg.SetShadowColor(0)
      self.leg.SetBorderSize(0)
      self.leg.SetFillColor(0)
      self.leg.SetLineColor(0)


  def Hist_Options(self,histogram,plot,canvas="",word = "",norebin=""):
 
        if word: print "Applying %s Options" % histogram
       
        if histogram == "EffectiveMass_after_alphaT_55_all":
          if canvas: self.Log_Setter(plot,canvas,0.5)
          if word: 
            plot.GetYaxis().SetTitleOffset(1.3)
            plot.GetYaxis().SetTitle("Events / 40 GeV")
          if not norebin:
            self.OverFlow_Bin(plot,0,3000,1500)
            #self.Reversed_Integrator(plot) 
         
        if histogram == "EffectiveMass_after_alphaT_53_all":
          if canvas: self.Log_Setter(plot,canvas,0.5)
          if word: 
            plot.GetYaxis().SetTitleOffset(1.3)
            plot.GetYaxis().SetTitle("Events / 40 GeV")
          if not norebin:
            self.OverFlow_Bin(plot,0,3000,1500)
            #self.Reversed_Integrator(plot)  

        if histogram == "EffectiveMass_after_alphaT_52_all":
          if canvas: self.Log_Setter(plot,canvas,0.5)
          if word: 
            plot.GetYaxis().SetTitleOffset(1.3)
            plot.GetYaxis().SetTitle("Events / 40 GeV")
          if not norebin:
            self.OverFlow_Bin(plot,0,3000,1500)
            #self.Reversed_Integrator(plot)     

        if histogram == "EffectiveMass_all":
          if canvas: self.Log_Setter(plot,canvas,0.5)
          if word: 
            plot.GetYaxis().SetTitleOffset(1.3)
            plot.GetYaxis().SetTitle("Events / 40 GeV")
          if not norebin:
            self.OverFlow_Bin(plot,0,3000,1500)
            #self.Reversed_Integrator(plot)  

        if histogram == "MHT_all":
          if canvas: self.Log_Setter(plot,canvas,0.5)
          if word: 
            plot.GetYaxis().SetTitleOffset(1.3)
            plot.GetYaxis().SetTitle("Events / 10 GeV")
          self.OverFlow_Bin(plot,0,600,500)
        
        if histogram == "MT__all":
          if canvas: self.Log_Setter(plot,canvas,0.5)
          if word: 
            plot.GetYaxis().SetTitleOffset(1.3)
            plot.GetYaxis().SetTitle("Events / 25 GeV")
          plot.Rebin(25)
          self.OverFlow_Bin(plot,0,2000,800)

        if histogram == "MuCso__all":
          if canvas: self.Log_Setter(plot,canvas,0.5)
          if word: 
            plot.GetYaxis().SetTitleOffset(1.3)
            plot.GetYaxis().SetTitle("Events / 0.02")
          if not norebin:
            plot.Rebin(20)
            self.OverFlow_Bin(plot,0,2.,0.2)
            #self.Reversed_Integrator(plot)  

        if histogram == "MuHIso__all":
          if canvas: self.Log_Setter(plot,canvas,0.5)
          if word: 
            plot.GetYaxis().SetTitleOffset(1.3)
            plot.GetYaxis().SetTitle("Events / 0.02")
          if not norebin:
            plot.Rebin(20)
            self.OverFlow_Bin(plot,0,2.,0.2)
            #self.Reversed_Integrator(plot)  

        if histogram == "MuEIso__all":
          if canvas: self.Log_Setter(plot,canvas,0.5)
          if word: 
            plot.GetYaxis().SetTitleOffset(1.3)
            plot.GetYaxis().SetTitle("Events / 0.02")
          if not norebin:
            plot.Rebin(20)
            self.OverFlow_Bin(plot,0,2.,0.2)
            #self.Reversed_Integrator(plot)  

        if histogram == "MuTrIso__all":
          if canvas: self.Log_Setter(plot,canvas,0.1)
          if word: 
            plot.GetYaxis().SetTitleOffset(1.3)
            plot.GetYaxis().SetTitle("Events / 0.02")
          if not norebin:
            plot.Rebin(20)
            self.OverFlow_Bin(plot,0,2.,0.2)
            #self.Reversed_Integrator(plot)  

        if histogram == "MuPt__all":
          if canvas: self.Log_Setter(plot,canvas,0.5)
          if word: 
            plot.GetYaxis().SetTitleOffset(1.3)
            plot.GetYaxis().SetTitle("Events / 25 GeV")
          plot.Rebin(25)
          self.OverFlow_Bin(plot,10,2010,1000)

        if histogram == "HT_all":
          if canvas: self.Log_Setter(plot,canvas,0.5)
          if word: 
            plot.GetYaxis().SetTitleOffset(1.3)
            plot.GetYaxis().SetTitle("Events / 25 GeV")
          self.OverFlow_Bin(plot,0,2000,1250)

        if histogram == "HT_after_alphaT_55_all":
          if canvas:self.Log_Setter(plot,canvas,0.5)
          if word: 
            plot.GetYaxis().SetTitleOffset(1.3)
            plot.GetYaxis().SetTitle("Events / 25 GeV")
          self.OverFlow_Bin(plot,0,2000,1250)

        
        if histogram == "HT_after_alphaT_53_all":
          if canvas:self.Log_Setter(plot,canvas,0.5)
          if word: 
            plot.GetYaxis().SetTitleOffset(1.3)
            plot.GetYaxis().SetTitle("Events / 25 GeV")
          self.OverFlow_Bin(plot,0,2000,1250)

        if histogram == "HT_after_alphaT_52_all":
          if canvas:self.Log_Setter(plot,canvas,0.5)
          if word: 
            plot.GetYaxis().SetTitleOffset(1.3)
            plot.GetYaxis().SetTitle("Events / 25 GeV")
          self.OverFlow_Bin(plot,0,2000,1250)  

        if histogram == "AlphaT_all":  
          if canvas: self.Log_Setter(plot,canvas,0.5)
          if word: 
            plot.GetYaxis().SetTitleOffset(1.3)
            plot.GetYaxis().SetTitle("Events / 0.1")
          if not norebin: 
            plot.Rebin(10)
            self.OverFlow_Bin(plot,0.0,10,3.0)
            #self.Reversed_Integrator(plot)

        if histogram == "AlphaT_Zoomed_all":
          if canvas: self.Log_Setter(plot,canvas,0.5)
          if word: 
            plot.GetYaxis().SetTitleOffset(1.3)
            plot.GetYaxis().SetTitle("Events / 0.08")
          if not norebin:
            plot.Rebin(5)
            self.OverFlow_Bin(plot,0.45,0.6,0.6)
            #self.Reversed_Integrator(plot)  
            
        if histogram == "JetMultiplicity_all": 
          if canvas: self.Log_Setter(plot,canvas,0.5)
        
        if histogram == "JetMultiplicityAfterAlphaT_55_all": 
          if canvas: self.Log_Setter(plot,canvas,0.5)

        if histogram == "BiasedDeltaPhi_after_alphaT_55_all":
           if canvas: self.Log_Setter(plot,canvas,0.5)
           if word: 
            plot.GetYaxis().SetTitleOffset(1.3)
            plot.GetYaxis().SetTitle("Events / 0.25 rad")
           plot.Rebin(5)

        if histogram == "JetMultiplicityAfterAlphaT_53_all": 
          if canvas: self.Log_Setter(plot,canvas,0.5)

        if histogram == "BiasedDeltaPhi_after_alphaT_53_all":
           if canvas: self.Log_Setter(plot,canvas,0.5)
           if word: 
            plot.GetYaxis().SetTitleOffset(1.3)
            plot.GetYaxis().SetTitle("Events / 0.25 rad")
           plot.Rebin(5)

        if histogram == "JetMultiplicityAfterAlphaT_52_all": 
          if canvas: self.Log_Setter(plot,canvas,0.5)

        if histogram == "BiasedDeltaPhi_after_alphaT_52_all":
           if canvas: self.Log_Setter(plot,canvas,0.5)
           if word: 
            plot.GetYaxis().SetTitleOffset(1.3)
            plot.GetYaxis().SetTitle("Events / 0.25 rad")
           plot.Rebin(5)

        if histogram == "Btag_Pre_AlphaT_4_all": 
          if canvas: self.Log_Setter(plot,canvas,0.5)
 
        if histogram == "Btag_Post_AlphaT_4_55_all": 
          if canvas: self.Log_Setter(plot,canvas,0.5)
 
        if histogram == "Btag_Pre_AlphaT_5_all": 
          if canvas: self.Log_Setter(plot,canvas,0.5)
 
        if histogram == "Btag_Post_AlphaT_5_55_all": 
          if canvas: self.Log_Setter(plot,canvas,0.5)

        if histogram == "Number_Primary_verticies_fter_alphaT_55_all":
          if canvas: self.Log_Setter(plot,canvas,0.5)

        if histogram == "Number_Primary_verticies_fter_alphaT_53_all":
          if canvas: self.Log_Setter(plot,canvas,0.5)


  def Log_Setter(self,plot,canvas,min):
      self.iflog = min
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


class Webpage_Maker(object):

      def __init__(self,plotnames,foldername,category,option=""):
        self.category = category
        self.Make_Page(plotnames,foldername,option)

      def ensure_dir(self,dir):
        try: os.makedirs(dir)
        except OSError as exc: pass
      
      def Make_Page(self,plotnames,foldername,option=""): 
        print "\n       ================================" 
        print "       ======== Making Webpage ========"
        print "       ********************************\n\n"
        self.webdir = str(option)+"_plots_"+strftime("%d_%b_%H")
        self.ensure_dir("./"+self.webdir)
        for root,dirs,files in os.walk('./Plots'):
          for filename in fnmatch.filter(files,'*.png'):
              name = os.path.join(root,filename)
              os.system('cp ' +name+ ' ./'+self.webdir+'/')
        
        if option == "Normal":
          for i in plotnames:
              counter = 0
              htF = open('./'+self.webdir+'/'+i+'.html','w')
              htF.write('Author: Darren Burton <br> \n')
              htF.write('<script language="Javascript"> \n document.write("Last Modified: " + document.lastModified + ""); \n </script> <br> \n ')
              htF.write('<center>\n <p> \n <font size="5"> Binned Muon Control Sample </font>\n </p>\n') 
              htF.write('<font size="3">Results for :  '+i+' </font><br> \n')
              htF.write('Hist Name: ') 
              for k in plotnames:
                counter += 1
                htF.write('<a href=\"'+k+'.html\">'+k+'</a>')
                htF.write('   |    ')
                if counter == 5:
                  htF.write('<br> \n')
                  counter = 0
              htF.write('<br> \n')

              for root,dirs,files in os.walk('./'+self.webdir):
                sorter = []
                for filenames in fnmatch.filter(files,i+'_*.png'): 
                  sorter.append(filenames)
                  sorter.sort()
                for plot in sorter: htF.write('<a href='+plot+'><img height=\"400\" src=\"'+plot+'\"></a> \n') 

        if option == "btag":
          self.btag_slices = {'Zero':"0-btag",'One':"1-btag",'Two':"2-btag","Inclusive":"Inclusive",'More_Than_Zero':"A btag",'More_Than_Two':"More Than Two"}
          self.btag_names = {'More_Than_Two':"btag_morethantwo",'More_Than_Zero':"btag_morethanzero",'Zero':"btag_zero",'One':"btag_one",'Two':"btag_two","Inclusive":self.category }
          self.Alpha_Webpage(foldername,plotnames,link="Zero",outertitle="HT Bins:  ")
          self.Alpha_Webpage(self.btag_slices,plotnames,link=foldername[0],outertitle="Btag Multiplicities:  ",slice="True")

      def Alpha_Webpage(self,outer,inner,link="",outertitle="",slice=""):
 
        for i in outer:
          for j in inner:
            counter = 0
            htF = open('./'+self.webdir+'/'+j+'_'+i+'.html','w')
            htF.write('Author: Darren Burton <br> \n')
            htF.write('<script language="Javascript"> \n document.write("Last Modified: " + document.lastModified + ""); \n </script> <br> \n ')
            htF.write('<center>\n <p> \n <font size="5"> Binned Alpha T </font>\n </p>\n') 
            htF.write('<font size="3">Results for '+j+'_'+i+' </font><br> \n')
            htF.write('Hist Name: ')
            for k in inner:
              counter += 1
              htF.write('<a href=\"'+k+'_'+i+'.html\">'+k+'</a>   ')
              htF.write('    |     ')
              if counter == 4:
                htF.write('<br> \n')
                counter = 0
            htF.write('<br> \n')
            htF.write('<br> \n')
            htF.write(outertitle)
            for k in outer: htF.write('<a href=\"'+j+'_'+k+'.html\">'+(self.btag_slices[k] if slice else k)+'</a>     /    ')
            htF.write('<br> \n')
            htF.write('<br> \n')
            htF.write('Change Evolution Type: <a href=\"'+j+'_'+link+'.html\">'+ ('HT Evolution' if slice else 'Btag Evolution')+'</a>')
            htF.write('<br> \n')
             
            for root,dirs,files in os.walk('./'+self.webdir):
              sorter = []
              if not slice:  
                for filenames in fnmatch.filter(files,j+'*'+i+'*.png'):
                  sorter.append(filenames)
                  sorter.sort()
              else:
                for filenames in fnmatch.filter(files,j+'_'+self.btag_names[i]+ '*.png'):
                  sorter.append(filenames)
                  sorter.sort()
              for plot in sorter: htF.write('<a href='+plot+'><img height=\"400\" src=\"'+plot+'\"></a> \n') 


