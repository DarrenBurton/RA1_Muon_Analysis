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


class Jad_Compute(object):
  
  def __init__(self,dict_list,Lumo = "",classic = ""):

      print "\n\n Now Computing Jad Translation Plots\n\n"
      self.Lumo = Lumo
      self.Classic = classic
      self.MakeVectors(dict_list)

  def MakeVectors(self,dict_list):
    r.gROOT.ProcessLine(".L tdrstyle.C")
    r.setstyle()
    #r.gROOT.SetBatch(True)
    r.gStyle.SetErrorX(0.)
    r.gStyle.SetEndErrorSize(0.)
    r.gStyle.SetOptStat(1)
    r.gStyle.SetOptFit(1)
    self.c1= r.TCanvas("Yields", "Yields",0,0,900,600)
    self.c1.SetHighLightColor(2)
    self.c1.SetFillColor(0)
    self.c1.SetBorderMode(0)
    self.c1.SetBorderSize(2)
    self.c1.SetTickx(1)
    self.c1.SetTicky(1)
    self.c1.SetFrameBorderMode(0)
    self.c1.SetFrameBorderMode(0)
    self.c1.cd(1)
    self.axis = [275,325,375, 475, 575, 675, 775, 875, 975]
    

    '''
    option reduce, fits the line from 375 upwards. Used if making closure tests with photons as they are no lower 2 bins. Another example where reduce is used if comparing 
    just the high stats mu-had control samples for the full dataset. Just change the option in the box accordingly. Used for classic mode only.
    '''

    if self.Classic == "True" :
      print "In classic mode"
      test_1 = {'MCS' : [], 'MCSE': [],'MCC': [], 'MCCE':[],'DC':[],'DS':[],'option' : -1.,'box' : "True", 'plot_title':"#mu + jets #rightarrow #mu#mu + jets",'scale':None,'reduce':"False" } 
      test_2 = {'MCS' : [], 'MCSE': [],'MCC': [], 'MCCE':[],'DC':[],'DS':[],'option' : -2.,'box' : "True", 'plot_title':"#gamma + jets #rightarrow #mu#mu + jets ",'scale':None,'reduce':"True" } 
      test_3 = {'MCS' : [], 'MCSE': [],'MCC': [], 'MCCE':[],'DC':[],'DS':[],'option' : -3.,'box' : "True", 'plot_title':"#gamma + jets #rightarrow #mu + jets",'scale':None,'reduce':"True" }

      test_dicts = [test_1,test_2,test_3]
    else:

      test_1 = {'MCS' : [], 'MCSE': [],'MCC': [], 'MCCE':[],'DC':[],'DS':[],'option' : -100.,'box' : "True", 'plot_title':"#mu + jets (#alpha_{T}>0.55) #rightarrow #mu#mu + jets (#alpha_{T}>0.55)",'scale':None } 
      test_2 = {'MCS' : [], 'MCSE': [],'MCC': [], 'MCCE':[],'DC':[],'DS':[],'option' : -1.,'box' : "True",'plot_title':"#mu + jets (no #alpha_{T}) #rightarrow #mu#mu + jets (no #alpha_{T})" ,'scale':None  } 
      test_3 = {'MCS' : [], 'MCSE': [],'MCC': [], 'MCCE':[],'DC':[],'DS':[],'option' : -2.,'box' : "False",'plot_title':"#mu + jets (no #alpha_{T}) #rightarrow #mu + jets (#alpha_{T}>0.55)",'scale':None  } 
      test_4 = {'MCS' : [], 'MCSE': [],'MCC': [], 'MCCE':[],'DC':[],'DS':[],'option' : -3.,'box' : "False",'plot_title':"#mu#mu + jets (no #alpha_{T}) #rightarrow #mu#mu + jets (#alpha_{T}>0.55)",'scale':None   } 
      test_5 = {'MCS' : [], 'MCSE': [],'MCC': [], 'MCCE':[],'DC':[],'DS':[],'option' : -4.,'box' : "False",'plot_title':"#mu + jets (0-b-tag) #rightarrow #mu + jets (1-b-tag) (no #alpha_{T})",'scale': "True"  } 
      test_6 = {'MCS' : [], 'MCSE': [],'MCC': [], 'MCCE':[],'DC':[],'DS':[],'option' : -5.,'box' : "False",'plot_title':"#mu + jets (0-b-tag) #rightarrow #mu + jets (>1-b-tag) (no #alpha_{T})",'scale':"Double"   }
      test_7 = {'MCS' : [], 'MCSE': [],'MCC': [], 'MCCE':[],'DC':[],'DS':[],'option' : -6.,'box' : "False",'plot_title':"#mu + jets (1-b-tag) #rightarrow #mu + jets (>1-b-tag) (no #alpha_{T})",'scale': 'True'   }
      test_8 = {'MCS' : [], 'MCSE': [],'MCC': [], 'MCCE':[],'DC':[],'DS':[],'option' : -7.,'box' : "True",'plot_title':"#mu + jets (1-b-tag) #rightarrow #mu#mu + jets (1-b-tag) (no #alpha_{T})",'scale':None   }
      test_9 = {'MCS' : [], 'MCSE': [],'MCC': [], 'MCCE':[],'DC':[],'DS':[],'option' : -8,'box' : "False",'plot_title':"#mu + jets (1-b-tag)(no #alpha_{T}) #rightarrow #mu + jets (1-b-tag) (#alpha_{T} > 0.55)" ,'scale':None  }
      test_10 = {'MCS' : [], 'MCSE': [],'MCC': [], 'MCCE':[],'DC':[],'DS':[],'option' : -9,'box' : "False",'plot_title':"#mu#mu + jets (1-b-tag)(no #alpha_{T}) #rightarrow #mu#mu + jets (1-b-tag) (#alpha_{T} > 0.55)" ,'scale':None  }
      test_11 = {'MCS' : [], 'MCSE': [],'MCC': [], 'MCCE':[],'DC':[],'DS':[],'option' : -9,'box' : "False",'plot_title':"#mu + jets (>1-b-tag)(no #alpha_{T}) #rightarrow #mu + jets (>1-b-tag) (#alpha_{T} > 0.55)" ,'scale':None  }

      test_dicts = [test_1,test_2,test_3,test_4,test_5,test_6,test_7,test_8,test_9,test_10,test_11]

    for self.file in dict_list:
      for self.entry in sorted(self.file.iterkeys()):
        if self.Classic == "True":

          if self.file[self.entry]['AlphaT'] == '0.55' and self.file[self.entry]['Btag'] == 'BaseLine':
            self.Fill_Dictionary(test_1,Control = "Muon", Signal = "DiMuon")

          if self.file[self.entry]['AlphaT'] == '0.55' and self.file[self.entry]['Btag'] == 'BaseLine':
            self.Fill_Dictionary(test_2,Control = "Photon", Signal = "DiMuon")

          if self.file[self.entry]['AlphaT'] == '0.55' and self.file[self.entry]['Btag'] == 'BaseLine':
            self.Fill_Dictionary(test_3,Control = "Photon", Signal = "Muon")

        else:

          if self.file[self.entry]['AlphaT'] == '0.55' and self.file[self.entry]['Btag'] == 'BaseLine':
            self.Fill_Dictionary(test_1,Control = "Muon", Signal = "DiMuon")

          if self.file[self.entry]['AlphaT'] == '0.01' and self.file[self.entry]['Btag'] == 'BaseLine':
            self.Fill_Dictionary(test_2,Control = "Muon", Signal = "DiMuon") 

          if self.file[self.entry]['AlphaT'] == '0.01' and self.file[self.entry]['Btag'] == 'BaseLine' :
            self.Fill_Dictionary(test_3,Control = "Muon", Signal = "Muon",Not_Do = 'Signal') 
          if self.file[self.entry]['AlphaT'] == '0.55' and self.file[self.entry]['Btag'] == 'BaseLine' :
            self.Fill_Dictionary(test_3,Control = "Muon", Signal = "Muon",Not_Do = 'Control')         

          if self.file[self.entry]['AlphaT'] == '0.01' and self.file[self.entry]['Btag'] == 'BaseLine' :
            self.Fill_Dictionary(test_4,Control = "DiMuon", Signal = "DiMuon",Not_Do = 'Signal') 
          if self.file[self.entry]['AlphaT'] == '0.55' and self.file[self.entry]['Btag'] == 'BaseLine' :
            self.Fill_Dictionary(test_4,Control = "DiMuon", Signal = "DiMuon",Not_Do = 'Control')

          if self.file[self.entry]['AlphaT'] == '0.01' and self.file[self.entry]['Btag'] == 'Zero_btags' :
            self.Fill_Dictionary(test_5,Control = "Muon", Signal = "Muon",Not_Do = 'Signal') 
          if self.file[self.entry]['AlphaT'] == '0.01' and self.file[self.entry]['Btag'] == 'One_btag' :
            self.Fill_Dictionary(test_5,Control = "Muon", Signal = "Muon",Not_Do = 'Control')


          if self.file[self.entry]['AlphaT'] == '0.01' and self.file[self.entry]['Btag'] == 'Zero_btags' :
            self.Fill_Dictionary(test_6,Control = "Muon", Signal = "Muon",Not_Do = 'Signal') 
          if self.file[self.entry]['AlphaT'] == '0.01' and self.file[self.entry]['Btag'] == 'More_Than_One_btag' :
            self.Fill_Dictionary(test_6,Control = "Muon", Signal = "Muon",Not_Do = 'Control')


          if self.file[self.entry]['AlphaT'] == '0.01' and self.file[self.entry]['Btag'] == 'One_btag' :
            self.Fill_Dictionary(test_7,Control = "Muon", Signal = "Muon",Not_Do = 'Signal') 
          if self.file[self.entry]['AlphaT'] == '0.01' and self.file[self.entry]['Btag'] == 'More_Than_One_btag' :
            self.Fill_Dictionary(test_7,Control = "Muon", Signal = "Muon",Not_Do = 'Control')

          if self.file[self.entry]['AlphaT'] == '0.01' and self.file[self.entry]['Btag'] == 'One_btag' :
            self.Fill_Dictionary(test_8,Control = "Muon", Signal = "Muon",Not_Do = 'Signal') 
          if self.file[self.entry]['AlphaT'] == '0.01' and self.file[self.entry]['Btag'] == 'One_btag' :
            self.Fill_Dictionary(test_8,Control = "DiMuon", Signal = "DiMuon",Not_Do = 'Control')

          if self.file[self.entry]['AlphaT'] == '0.01' and self.file[self.entry]['Btag'] == 'One_btag' :
            self.Fill_Dictionary(test_9,Control = "Muon", Signal = "Muon",Not_Do = 'Signal') 
          if self.file[self.entry]['AlphaT'] == '0.55' and self.file[self.entry]['Btag'] == 'One_btag' :
            self.Fill_Dictionary(test_9,Control = "Muon", Signal = "Muon",Not_Do = 'Control')

          if self.file[self.entry]['AlphaT'] == '0.01' and self.file[self.entry]['Btag'] == 'One_btag' :
            self.Fill_Dictionary(test_10,Control = "DiMuon", Signal = "DiMuon",Not_Do = 'Signal') 
          if self.file[self.entry]['AlphaT'] == '0.55' and self.file[self.entry]['Btag'] == 'One_btag' :
            self.Fill_Dictionary(test_10,Control = "DiMuon", Signal = "DiMuon",Not_Do = 'Control')

          if self.file[self.entry]['AlphaT'] == '0.01' and self.file[self.entry]['Btag'] == 'More_Than_One_btag' :
            self.Fill_Dictionary(test_11,Control = "Muon", Signal = "Muon",Not_Do = 'Signal') 
          if self.file[self.entry]['AlphaT'] == '0.55' and self.file[self.entry]['Btag'] == 'More_Than_One_btag' :
            self.Fill_Dictionary(test_11,Control = "Muon", Signal = "Muon",Not_Do = 'Control')

    for test in test_dicts:
       if self.Classic == "True":
        self.Make_Plots(test['MCS'],test['MCSE'],test['MCC'],test['MCCE'],test['DC'],test['DS'],test['option'],test['box'],test['plot_title'],test['scale'],reduce = test['reduce'])
       else:  
        self.Make_Plots(test['MCS'],test['MCSE'],test['MCC'],test['MCCE'],test['DC'],test['DS'],test['option'],test['box'],test['plot_title'],test['scale'])

  def Fill_Dictionary(self,closure_dictionary,Control = '',Signal = '',Not_Do = ''):
          
          if self.file[self.entry]['SampleName'] == Control and Not_Do != 'Control':
            closure_dictionary['MCC'].append(self.file[self.entry]['Yield'])
            closure_dictionary['MCCE'].append(self.file[self.entry]['SM_Stat_Error'])
            closure_dictionary['DC'].append(self.file[self.entry]['Data'])
          elif self.file[self.entry]['SampleName'] == Signal and Not_Do != 'Signal':
            closure_dictionary['MCS'].append(self.file[self.entry]['Yield'])
            closure_dictionary['MCSE'].append(self.file[self.entry]['SM_Stat_Error'])
            closure_dictionary['DS'].append(self.file[self.entry]['Data'])

          return closure_dictionary 

  def Make_Plots(self,MCS,MCSE,MCC,MCCE,DC,DS,option,box = '',plot_title='',scale='',reduce=''):
     if reduce == "True": hist_low = 375
     else: hist_low = 275

     max = 2.0
     min = -2.
     data = r.TGraphAsymmErrors(8)
     # If need to change scaling factor to correct for Data/MC btag efficiency. 5% correction = scaling factor of 1.05
     scaling_factor = 1.0
     print "Plot Title is \n"
     print plot_title
     if scale:
      print "Scaling Plot"
      for i in range(0,len(MCS)):
        if scale == "True":
          MCS[i]=MCS[i]*scaling_factor
          MCC[i]=MCC[i]-MCS[i]*(1-scaling_factor)
        if scale == "Double":
          MCS[i]=MCS[i]*(scaling_factor*scaling_factor)
          MCC[i]=MCC[i]-MCS[i]*(1-(scaling_factor*scaling_factor))
     for i in range(0,len(MCS)):
        if option <3: j = 0
        else: j = 2
        if i+j < 2: offset = 25.
        else: offset = 50
        #Prediction
        try: prediction = ((MCS[i] / MCC[i]) * DC[i])
        except ZeroDivisionError: prediction = 0.0
        try:val = DS[i] / prediction
        except ZeroDivisionError:val = 0.0
        data.SetPoint(i+1,self.axis[i+j]+offset,val-1.0)
        #Make Errors
        eh = sqrt(DC[i])
        el = sqrt(DC[i])
        if DC[i] < 10.: self.Poission(DC[i],eh,el)

        #Total Error on prediction
        try:errh = prediction * sqrt( ((MCSE[i] / MCS[i]) * (MCSE[i] / MCS[i])) + ((MCCE[i] / MCC[i]) * (MCCE[i] / MCC[i])) + ((eh / DC[i]) * (eh / DC[i])) )
        except ZeroDivisionError: errh = 0
        try: errl = prediction * sqrt( ((MCSE[i] / MCS[i]) * (MCSE[i] / MCS[i])) + ((MCCE[i] / MCC[i]) * (MCCE[i] / MCC[i])) + ((el / DC[i]) * (el / DC[i])) )
        except ZeroDivisionError : errl = 0
        # Add to the prediction an extra error = to its statistical error
        ehextra = sqrt(prediction)
        elextra = sqrt(prediction)
        
        if prediction < 10.: self.Poission(prediction,ehextra,elextra)

        #Add these bad boys in quadrature
        errh = sqrt((errh*errh) + (ehextra*elextra))
        errl = sqrt((errl*errl) + (ehextra*elextra))

        # make the numerator: Nobs - Npred
        diffobspred = DS[i] - prediction

        try:errh = fabs((diffobspred / prediction) * sqrt(((errh / diffobspred)*(errh / diffobspred)) + ((errh / prediction)*(errh / prediction))))
        except ZeroDivisionError: errh = 0
        try:errl = fabs((diffobspred / prediction) * sqrt(((errl / diffobspred)*(errl / diffobspred)) + ((errl / prediction)*(errl / prediction))))
        except ZeroDivisionError: errl = 0 
        # Now set errors
        data.SetPointEYhigh(i+1,errh)
        data.SetPointEYlow(i+1,errl)

        if val > 2.2 or min < -2.2:
          max = val*1.1
          min = -val*1.1
        #if val < -2.2: min = val*1.1
        #print "Prediction %s\n" % val
        #print "Error High %s\n" %errh
        #/print "Error Low %s\n" %errl
     data.SetTitle("")
     data.GetXaxis().SetRangeUser(hist_low,975.)
     data.GetYaxis().SetRangeUser(min,max)
     data.GetXaxis().SetTitle("H_{T} (GeV)")
     data.GetYaxis().SetTitle("(N_{obs} - N_{pred}) / N_{pred}")
     data.GetYaxis().SetTitleOffset(1.1)
     data.SetLineWidth(3)
     data.SetMarkerStyle(20)
     data.SetMarkerSize(1.5)
     data.Draw("AP")

     if box == 'True':
        bv = r.TBox(hist_low,-0.2,975.,0.2)
        bv.SetFillColor(kGray) 
        bv.Draw()
        data.Draw("p")
        
        
     fit = r.TF1("fit","pol0", hist_low, 975.)
     data.Fit(fit)
     fit.SetLineColor(2)
     fit.Draw("SAME")
     #else: 
     leg = r.TLatex(0.42,0.84, "#chi^{2} /  nfd = %d Prob = %f, p0 = %f" %(fit.GetParameter(0),fit.GetParameter(2),fit.GetParameter(3)))
     leg.SetNDC()
     leg.SetTextSize(0.04)
     #leg.Draw("SAME")

     tex = r.TLatex(0.12,0.84,"CMS, %s fb^{-1}, #sqrt{s} = 7 TeV" % self.Lumo )
     tex.SetNDC()
     tex.SetTextSize(0.04)
     tex.Draw("SAME")
     pt = r.TPaveText(0.12,0.90,0.5,0.95,"blNDC")
     pt.SetBorderSize(0)
     pt.SetFillColor(0)
     pt.SetTextSize(0.04)
     pt.AddText(plot_title)
     pt.Draw("SAME")
     self.c1.SaveAs("%s.png" %plot_title)
     #self.c1.Modified()
     #self.c1.cd()
     #self.c1.SetSelected(c1)



  def Poission(self,x,errh,errl):
    poisson_eh = [ 1.15, 1.36, 1.53, 1.73, 1.98, 2.21, 2.42, 2.61, 2.80, 3.00, 3.16 ]
    poisson_el = [ 0.00, 1.00, 2.00, 2.14, 2.30, 2.49, 2.68, 2.86, 3.03, 3.19, 3.16 ]

    if x<10:
    # Apply Poission errors
      n = int(x)
      f = x - float(int(x))
      errh = poisson_eh[n] + f*( poisson_eh[n+1] - poisson_eh[n])
      errl = poisson_el[n] + f*(poisson_eh[n+1] - poisson_el[n])
    return errh,errl
      
          

