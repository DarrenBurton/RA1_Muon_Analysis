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

#================================== Preamble
print " Selecting tdr style"
r.gROOT.ProcessLine(".L tdrstyle.C")
r.setstyle()
r.gROOT.SetBatch(True)
r.gStyle.SetOptStat(0)

htbins = ["275_325","325_375","375_475","475_575","575_675","675_775","775_875","875"]


files = ["./Root_Files/Muon_MC.root","./Root_Files/Had_MC.root"]


btag_holder = []
mistag_holder = []
#file = r.TFile.Open("./Muon_MC_update.root")
#file = r.TFile.Open("./Had_MC_new.root")

#file = r.TFile.Open("./TTbar_20.root")
#file = r.TFile.Open("./WJets_20.root")
#file = r.TFile.Open("./QCD_20.root")
#file = r.TFile.Open("./QCD_Btag.root")

#file = r.TFile.Open("./TTbar_Leptonic_Btag.root")

for label,path in enumerate(files):
  file = r.TFile.Open(path)
  DirKeys = file.GetListOfKeys()
  if label == 0: name = "Muon"
  else: name = "Had"
  gen_pt_list = []
  matched_gen_pt_list = []

  mistag_list = []
  matched_mistag_list = []

  nomatch_list = []
  nomatch_tagged_list = []

  for num,bin in enumerate(htbins):
    for key in DirKeys:
      subdirect = file.FindObjectAny(key.GetName())
      if label == 0:dir = "OneMuon_"+bin
      else: dir = bin
      subdirect.GetName()
      if dir == subdirect.GetName():
        for subkey in subdirect.GetListOfKeys():
          if subkey.GetName() == "GenJetPt_all":
              plot = file.Get(dir+"/"+subkey.GetName())
              gen_pt_list.append(plot)
          if subkey.GetName() == "Btagged_GenJetPt_SFb_all": 
              plot = file.Get(dir+"/"+subkey.GetName())
              matched_gen_pt_list.append(plot)
          if subkey.GetName() == "GenJetPt_noB_all":
              plot = file.Get(dir+"/"+subkey.GetName())
              mistag_list.append(plot)
          if subkey.GetName() == "Btagged_GenJetPt_noB_SFlight_all": 
              plot = file.Get(dir+"/"+subkey.GetName())
              matched_mistag_list.append(plot)
          if subkey.GetName() == "NotMatched_RecoJet__all":
              plot = file.Get(dir+"/"+subkey.GetName())
              nomatch_list.append(plot)
          if subkey.GetName() == "Btagged_NotMatched_RecoJet__all": 
              plot = file.Get(dir+"/"+subkey.GetName())
              nomatch_tagged_list.append(plot)
             
  htbin = [275,325,375,475,575,675,775,875]
  #print nomatch_tagged_list
  #HTBin_efficiency = r.TH1F("HT_Efficiency","",6,0,6)
  HTBin_efficiency = r.TH1F("HT_Efficiency","",8,0,8)

  HTBin_efficiency.GetXaxis().SetTitle("H_{T} (GeV)")
  HTBin_efficiency.GetYaxis().SetTitle("Btag Efficiency")
  HTBin_efficiency.GetYaxis().SetTitleOffset(1.30)
  HTBin_efficiency.GetXaxis().SetTitleSize(0.04)
  HTBin_efficiency.GetYaxis().SetTitleSize(0.04)
  HTBin_efficiency.GetYaxis().SetRangeUser(0.4,1.0)
  HTBin_efficiency.GetSumw2()
  HTBin_efficiency.SetMarkerStyle(20)
  HTBin_efficiency.SetMarkerSize(1.5)
  HTBin_efficiency.SetLineWidth(2)

  HTBin_mistag = HTBin_efficiency.Clone()
  HTBin_mistag.GetYaxis().SetRangeUser(0.0,0.3)

  HTBin_nomatch = HTBin_efficiency.Clone()
  HTBin_nomatch.GetYaxis().SetRangeUser(0.0,0.3)



  for num,hist in enumerate(gen_pt_list):

    gen_pt_list[num].GetSumw2()
    matched_gen_pt_list[num].GetSumw2()
    mistag_list[num].GetSumw2()
    matched_mistag_list[num].GetSumw2()
    nomatch_list[num].GetSumw2()
    nomatch_tagged_list[num].GetSumw2()



    if num == 0:
      Pt_Hist = gen_pt_list[num].Clone()
      Matched_Pt_Hist = matched_gen_pt_list[num].Clone()
      
      Pt_Hist.GetSumw2()
      Matched_Pt_Hist.GetSumw2()

      Mistag_Hist = mistag_list[num].Clone()
      Matched_Mistag_Hist = matched_mistag_list[num].Clone()
      
      Mistag_Hist.GetSumw2()
      Matched_Mistag_Hist.GetSumw2()

      Nomatch_Hist = nomatch_list[num].Clone()
      Nomatch_tagged_Hist = nomatch_tagged_list[num].Clone()
      
      Nomatch_Hist.GetSumw2()
      Nomatch_tagged_Hist.GetSumw2()

    else:

      Nomatch_Hist.Add(nomatch_list[num])
      Nomatch_tagged_Hist.Add(nomatch_tagged_list[num])

      Mistag_Hist.Add(mistag_list[num])
      Matched_Mistag_Hist.Add(matched_mistag_list[num])

      Pt_Hist.Add(gen_pt_list[num])
      Matched_Pt_Hist.Add(matched_gen_pt_list[num])

    #print "Get Entries"
    #print matched_gen_pt_list[num].GetEntries()/gen_pt_list[num].GetEntries()
    #print " Get Integral"
    #print matched_gen_pt_list[num].Integral()/gen_pt_list[num].Integral()
    #print "Fractional Error is"
    #print sqrt((1/matched_gen_pt_list[num].GetEntries())+(1/gen_pt_list[num].GetEntries()))
    #print matched_gen_pt_list[num].GetEntries()
    #print "\n"

    err = r.Double(0.0)
    err_2 = r.Double(0.0)

    err_mistag =r.Double(0.0)
    err_mistag_2 =r.Double(0.0)


    err_nomatch = r.Double(0.0) 
    
    ht_eff = matched_gen_pt_list[num].Clone()
    a = ht_eff.IntegralAndError(0,1000,err)
    ht_eff_2 = gen_pt_list[num].Clone()
    b = ht_eff_2.IntegralAndError(0,1000,err_2)

    ht_mistag = matched_mistag_list[num].Clone()
    c = ht_mistag.IntegralAndError(0,1000,err_mistag)
    ht_mistag_2 = mistag_list[num].Clone()
    d = ht_mistag_2.IntegralAndError(0,1000,err_mistag_2)
    

    HTBin_efficiency.SetBinContent(num+1,matched_gen_pt_list[num].Integral()/gen_pt_list[num].Integral())
    HTBin_efficiency.SetBinError(num+1,(matched_gen_pt_list[num].Integral()/gen_pt_list[num].Integral())*sqrt( pow((err/a),2)+pow((err_2/b),2)))
    
    HTBin_mistag.SetBinContent(num+1,matched_mistag_list[num].Integral()/mistag_list[num].Integral())
    HTBin_mistag.SetBinError(num+1, (matched_mistag_list[num].Integral()/mistag_list[num].Integral())*sqrt( pow((err_mistag/c),2)+pow((err_mistag_2/d),2)))
    

    try: HTBin_nomatch.SetBinContent(num+1,nomatch_tagged_list[num].Integral()/nomatch_list[num].Integral())
    except ZeroDivisionError: HTBin_nomatch.SetBinContent(num+1,0)
    try: HTBin_nomatch.SetBinError(num+1,(nomatch_tagged_list[num].GetEntries()/nomatch_list[num].GetEntries())*sqrt((1/nomatch_tagged_list[num].GetEntries())+(1/nomatch_list[num].GetEntries())))
    except ZeroDivisionError: HTBin_nomatch.SetBinError(num+1,0)


  Pt_Hist.Rebin(20)
  Matched_Pt_Hist.Rebin(20)

  Matched_Pt_Hist.Divide(Pt_Hist)
  Matched_Pt_Hist.GetXaxis().SetRangeUser(0,500)
  Matched_Pt_Hist.GetYaxis().SetRangeUser(0.4,1.0)

  Mistag_Hist.Rebin(20)
  Matched_Mistag_Hist.Rebin(20)

  Matched_Mistag_Hist.Divide(Mistag_Hist)
  Matched_Mistag_Hist.GetXaxis().SetRangeUser(0,500)
  Matched_Mistag_Hist.GetYaxis().SetRangeUser(0.0,0.3)

  Nomatch_Hist.Rebin(20)
  Nomatch_tagged_Hist.Rebin(20)

  Nomatch_tagged_Hist.Divide(Nomatch_Hist)
  Nomatch_tagged_Hist.GetXaxis().SetRangeUser(0,500)
  Nomatch_tagged_Hist.GetYaxis().SetRangeUser(0.0,0.3)


  c1 = r.TCanvas("canvas","canname",1200,1200)
  c1.cd()
  #c1.SetLogy()

  Matched_Pt_Hist.Draw()
  #c1.SaveAs("%s_Norm_Efficiency_Gen_Pt.png" %name)

  Matched_Mistag_Hist.Draw()
  #c1.SaveAs("%s_Norm_Mistag_Gen_Pt.png"% name)

  Nomatch_tagged_Hist.Draw()
  #c1.SaveAs("%s_Norm_Nomatch_Gen_Pt.png"%name)


  #print "HT Mistag Efficiency for jets not matched but then btagged"
  #for i in range(HTBin_nomatch.GetNbinsX()):
  #  print HTBin_nomatch.GetBinContent(i+1)

  txtfile = open('%s_Btag_Efficiency.txt'%name,'w')
  s=""
  for i in range(HTBin_efficiency.GetNbinsX()):
    s +="%s\n" %HTBin_efficiency.GetBinContent(i+1)

  txtfile.write(s)
  txtfile.close()

  misfile = open('%s_Mistag_Efficiency.txt'%name,'w')
  g=""
  for i in range(HTBin_mistag.GetNbinsX()):
    g +="%s\n" %HTBin_mistag.GetBinContent(i+1)
  misfile.write(g)
  misfile.close()

  nomatchfile = open('%s_Nomatch_Efficiency.txt'%name,'w')
  l=""
  for i in range(HTBin_nomatch.GetNbinsX()):
    l +="%s\n" %HTBin_nomatch.GetBinContent(i+1)
  nomatchfile.write(l)
  nomatchfile.close()


  c1.SetLogy(0)
  HTBin_efficiency.Draw("PE0")
  #c1.SaveAs("%s_Norm_Efficiency_HT_Bins.png" %name)

  HTBin_mistag.Draw("PE0")
  #c1.SaveAs("%s_Norm_Mistag_HT_Bins.png" %name)

  HTBin_nomatch.Draw("PE0")
  #c1.SaveAs("%s_Norm_Nomatch_HT_Bins.png" %name)

  btag_holder.append(HTBin_efficiency)
  mistag_holder.append(HTBin_mistag)


print btag_holder
print mistag_holder

muon_list = []
muon_btags = []

had_list = []
had_btags = []


#predict_file = r.TFile("Had_Full_Dataset_Nomatch.root")
#predict_file_muon = r.TFile("Muon_Full_Dataset_Nomatch.root")

predict_file = r.TFile("./Root_Files/Had_MC.root")
predict_file_muon = r.TFile("./Root_Files/Muon_MC.root")


#predict_file = r.TFile("Had_New_Attempt.root")
#predict_file_muon = r.TFile("Muon_New_Attempt.root")



DirKeys_2 = predict_file.GetListOfKeys()
DirKeys_muon = predict_file_muon.GetListOfKeys()

for num,bin in enumerate(htbins):

  for key in DirKeys_2:
    subdirect = predict_file.FindObjectAny(key.GetName())
    #dir = "OneMuon_"+bin
    dir = bin
    subdirect.GetName()
    if dir == subdirect.GetName():
      for subkey in subdirect.GetListOfKeys():
        #print subkey.GetName()
        if subkey.GetName() == "Matched_vs_Matched_noB_alphaT_all":
            plot = predict_file.Get(dir+"/"+subkey.GetName())
            had_list.append(plot)
        if subkey.GetName() == "Btag_Post_AlphaT_5_55_all":
            plot = predict_file.Get(dir+"/"+subkey.GetName())
            #print dir+subkey.GetName()
            had_btags.append(plot)

  for key in DirKeys_muon:
    subdirect = predict_file_muon.FindObjectAny(key.GetName())
    dir = "OneMuon_"+bin
    subdirect.GetName()
    if dir == subdirect.GetName():
      for subkey in subdirect.GetListOfKeys():
        #print subkey.GetName()
        
        if num == 0 or num ==1:
        
        
          if subkey.GetName() == "Matched_vs_Matched_noB_alphaT_all":
              plot = predict_file_muon.Get(dir+"/"+subkey.GetName())
              muon_list.append(plot)
          if subkey.GetName() == "Btag_Post_AlphaT_5_55_all":
              plot = predict_file_muon.Get(dir+"/"+subkey.GetName())
              #print dir+subkey.GetName()
              muon_btags.append(plot)

        else:
        
          if subkey.GetName() == "Matched_vs_Matched_noB_all":
                  plot = predict_file_muon.Get(dir+"/"+subkey.GetName())
                  muon_list.append(plot)
          if subkey.GetName() == "Btag_Pre_AlphaT_5__all":
                  plot = predict_file_muon.Get(dir+"/"+subkey.GetName())
                  #print dir+subkey.GetName()
                  muon_btags.append(plot)
              
c1.cd()

r.gROOT.SetBatch(True)
r.gStyle.SetOptStat(0)
gStyle.SetPalette(1)
diffb0 = r.TH1D("diffb0",";;",30, -1.525, 1.475);
diffb1 = r.TH1D("diffb1",";;",30, -1.525, 1.475);
diffb2 = r.TH1D("diffb2",";;",30, -1.525, 1.475);
diffb3 = r.TH1D("diffb3",";;",30, -1.525, 1.475);


diffb0_muon = r.TH1D("diffb0_mu",";;",30, -1.525, 1.475);
diffb1_muon = r.TH1D("diffb1_mu",";;",30, -1.525, 1.475);
diffb2_muon = r.TH1D("diffb2_mu",";;",30, -1.525, 1.475);
diffb3_muon = r.TH1D("diffb3_mu",";;",30, -1.525, 1.475);

twobtag_bin = open('Three_Btags_Had.txt','w')
twobtag_bin_mu = open('Three_Btags_Muon.txt','w')

ted_yields = open('Ted_Btag_Yields.txt','w')

Table_Make = open('MC_Had.txt','w')
Table_Pred = open('MC_Muon.txt','w')


had_yield = []
had_error = []

had_zero = []
had_zero_error = []

had_one = []
had_one_error = []

had_two = []
had_two_error = []


mu_yield = []
mu_error = []

mu_zero = []
mu_zero_error = []

mu_one = []
mu_one_error = []

mu_two = []
mu_two_error = []


t=""
f=""
l = ""
s = ""

a = " Btag Zero    "
p = " Btag One   "
c = " Btag Two   "
d = " Btag Three   "


a_ob = " Btag Zero Ob  "
p_ob = " Btag One Ob "
c_ob = " Btag Two Ob "
d_ob = " Btag Three Ob "

l += "Muon_Yield =["
s += "Muon_Error = ["
for num,plot in enumerate(muon_list):
  pred_three = 0
  error_three = 0
  pred_zero = 0
  pred_one = 0
  pred_two = 0
  #e = HTBin_efficiency.GetBinContent(num+1)
  #m = HTBin_mistag.GetBinContent(num+1)
  e = btag_holder[0].GetBinContent(num+1)
  m = mistag_holder[0].GetBinContent(num+1)
  print e
  print m
  #for b in range(2,4):
  for b in range(2,plot.GetNbinsX()):
    for i in range(1,plot.GetNbinsY()):
      if b == 3: pred_three += i*m*pow((1-m),i-1)*b*(b-1)*0.5*e*e*pow((1-e),b-2)*plot.GetBinContent(b+1,i+1)
      else: pred_three += i*m*pow((1-m),i-1)*b*(b-1)*0.5*e*e*pow((1-e),b-2)*plot.GetBinContent(b+1,i+1)

  
  for b in range(3,plot.GetNbinsX()):
    for noB in range (1,plot.GetNbinsY()):
      if b == 3:pred_three += pow((1-m),noB)*b*(b-1)*(b-2)*e*e*e*pow((1-e),b-3)*(1/6)*plot.GetBinContent(b+1,noB+1)
      else:pred_three += pow((1-m),noB)*b*(b-1)*(b-2)*e*e*e*pow((1-e),b-3)*(1/6)*plot.GetBinContent(b+1,noB+1)
  
  for b in range (0,plot.GetNbinsX()):
    for noB in range(3,plot.GetNbinsY()):
      if b ==3:pred_three += pow((1-e),b)*noB*(noB-1)*(noB-2)*(1/6)*m*m*m*pow((1-m),noB-3)*plot.GetBinContent(b+1,noB+1)
      else:pred_three += pow((1-e),b)*noB*(noB-1)*(noB-2)*(1/6)*m*m*m*pow((1-m),noB-3)*plot.GetBinContent(b+1,noB+1)
  
  for b in range (1,plot.GetNbinsX()):
    for noB in range(2,plot.GetNbinsY()):
      if b == 3:pred_three += noB*e*pow((1-e),b-1)*noB*(noB-1)*0.5*m*m*pow((1-m),noB-2)*plot.GetBinContent(b+1,noB+1)
      else:pred_three += noB*e*pow((1-e),b-1)*noB*(noB-1)*0.5*m*m*pow((1-m),noB-2)*plot.GetBinContent(b+1,noB+1)
  
  error_three = (e*e*m)*sqrt(pow(plot.GetBinError(3,2),2 )+(4*(1-m)*(1-m)*pow(plot.GetBinError(3,3),2))+(9*pow((1-m),4)*pow(plot.GetBinError(3,4),2))+(16*pow((1-m),6)*pow(plot.GetBinError(3,5),2))+(25*pow((1-m),8)*pow(plot.GetBinError(3,6),2))     )
  
  for b in range (0,plot.GetNbinsX()):
    for noB in range(0,plot.GetNbinsY()):
      #print " b = %s, noB = %s" %(b,noB)
      #print "Normal %f" % float(pow((1-e),b)*pow((1-m),noB)*plot.GetBinContent(b+1,noB+1))
      if b == 3: pred_zero += pow((1-e),b)*pow((1-m),noB)*plot.GetBinContent(b+1,noB+1)
      else:pred_zero += pow((1-e),b)*pow((1-m),noB)*plot.GetBinContent(b+1,noB+1)

  for b in range (0,plot.GetNbinsX()):
    for noB in range(1,plot.GetNbinsY()):
      if b == 3:pred_one += pow((1-e),b)*noB*m*pow((1-m),noB-1)*plot.GetBinContent(b+1,noB+1)
      else:pred_one += pow((1-e),b)*noB*m*pow((1-m),noB-1)*plot.GetBinContent(b+1,noB+1)
  
  for b in range(1,plot.GetNbinsX()):
    for noB in range(0,plot.GetNbinsY()):
      if b ==3:pred_one += pow((1-m),noB)*b*e*pow((1-e),b-1)*plot.GetBinContent(b+1,noB+1)
      else:pred_one += pow((1-m),noB)*b*e*pow((1-e),b-1)*plot.GetBinContent(b+1,noB+1)

  error_zero = 0
  sum_zero = 0
  for b in range(0,plot.GetNbinsX()):
    for noB in range(0,plot.GetNbinsY()):
              sum_zero += pow((plot.GetBinError(b+1,noB+1)*pow((1-e),b)*pow((1-m),noB)),2)

  error_zero = sqrt(sum_zero)
  
  sum_one = 0
  for b in range(1,plot.GetNbinsX()):
    for noB in range(1,plot.GetNbinsY()):
       sum_one += pow((pow((1-e),b-1)*pow((1-m),noB-1)*((noB*m*(1-e))+(noB*e*(1-m)))),2)*pow(plot.GetBinError(b+1,noB+1),2)
  
  error_one = sqrt( (m*m*pow(plot.GetBinError(1,2),2))+(e*e*pow(plot.GetBinError(2,1),2))+sum_one)
      
  
  for b in range (0,plot.GetNbinsX()):
    for noB in range(2,plot.GetNbinsY()):
      if b == 3: pred_two += pow((1-e),b)*noB*0.5*(noB-1)*m*m*pow((1-m),noB-2)*plot.GetBinContent(b+1,noB+1)
      else:pred_two += pow((1-e),b)*noB*0.5*(noB-1)*m*m*pow((1-m),noB-2)*plot.GetBinContent(b+1,noB+1)
  
  for b in range (2,plot.GetNbinsX()):
    for noB in range(0,plot.GetNbinsY()):
      if b == 3:pred_two += pow((1-m),noB)*0.5*b*(b-1)*e*e*pow((1-e),b-2)*plot.GetBinContent(b+1,noB+1)
      else: pred_two += pow((1-m),noB)*0.5*b*(b-1)*e*e*pow((1-e),b-2)*plot.GetBinContent(b+1,noB+1)
  
  for b in range (1,plot.GetNbinsX()):
    for noB in range(1,plot.GetNbinsY()):
      if b ==3:pred_two += b*e*pow((1-e),b-1)*noB*m*pow((1-m),m-1)*plot.GetBinContent(b+1,noB+1)
      else:pred_two += b*e*pow((1-e),b-1)*noB*m*pow((1-m),m-1)*plot.GetBinContent(b+1,noB+1)
 
  sum_two = 0
  for b in range (2,plot.GetNbinsX()):
    for noB in range(2,plot.GetNbinsY()):
      sum_two += pow(plot.GetBinError(b+1,noB+1),2)*(pow((1-e),b)*noB*0.5*(noB-1)*m*m*pow((1-m),noB-2)+pow((1-m),noB)*0.5*b*(b-1)*e*e*pow((1-e),b-2)+b*e*pow((1-e),b-1)*noB*m*pow((1-m),m-1))


  error_two = sqrt(m*m*pow(plot.GetBinError(1,3),2)+(pow(((1-e)*m*m)+(2*e*m*(1-m)) ,2)*pow(plot.GetBinError(2,3),2))+pow(e*plot.GetBinError(3,1),2)+pow(e*m*plot.GetBinError(2,2),2)+pow( (((1-m)*e*e)+(2*e*m*(1-m)))  ,2)*pow(plot.GetBinError(3,2),2)+sum_two) 


 


  diffb0_muon.Fill((pred_zero - muon_btags[num].GetBinContent(1)) / muon_btags[num].GetBinContent(1));
  diffb1_muon.Fill((pred_one - muon_btags[num].GetBinContent(2)) / muon_btags[num].GetBinContent(2));
  diffb2_muon.Fill((pred_two - muon_btags[num].GetBinContent(3)) / muon_btags[num].GetBinContent(3));
  try:diffb3_muon.Fill((pred_three - muon_btags[num].GetBinContent(4)) / muon_btags[num].GetBinContent(4));
  except ZeroDivisionError: diffb3_muon.Fill(0);
  try:ratio = (pred_three - muon_btags[num].GetBinContent(4)) / muon_btags[num].GetBinContent(4)
  except ZeroDivisionError: ratio = 0
  print "noB %s observed  %s error  %s prediction %s with error %s " %(htbins[num],muon_btags[num].GetBinContent(1),muon_btags[num].GetBinError(1),pred_zero,error_zero)
  print "oneB %s obverved %s error %s prediction %s with error %s " %(htbins[num],muon_btags[num].GetBinContent(2),muon_btags[num].GetBinError(2),pred_one,error_one)
  print "twoB %s observed %s error  %s prediction %s with error %s " %(htbins[num],muon_btags[num].GetBinContent(3),muon_btags[num].GetBinError(3),pred_two,error_two)
  print "threeB %s  observed %s error %s  prediction  %s with error %s " %(htbins[num],muon_btags[num].GetBinContent(4),muon_btags[num].GetBinError(4),pred_three,error_three)
  t+="Prediction in %s bin  %s with error %f , Observed in bin %f with error %f \n" %(htbins[num],float(pred_three),float(error_three),float(muon_btags[num].GetBinContent(4)),float(muon_btags[num].GetBinError(4)))
  t+="This gives a ratio of pred-data/data ratio of %f\n\n\n" %ratio
  l+="%f," %float(pred_three*46.5)
  s+="%f," %float(error_three*46.5)
  
  a+=" %5.3f +- %5.3f " %(float(pred_zero),float(error_zero))
  p+=" %5.3f +- %5.3f " %(float(pred_one),float(error_one))
  c+=" %5.3f +- %5.3f " %(float(pred_two),float(error_two))
  d+=" %5.3f +- %5.3f " %(float(pred_three),float(error_three))


  a_ob+=" %5.3f +- %5.3f " %(float(muon_btags[num].GetBinContent(1)),float(muon_btags[num].GetBinError(1))) 
  p_ob+=" %5.3f +- %5.3f " %(float(muon_btags[num].GetBinContent(2)),float(muon_btags[num].GetBinError(2)))
  c_ob+=" %5.3f +- %5.3f " %(float(muon_btags[num].GetBinContent(3)),float(muon_btags[num].GetBinError(3)))
  d_ob+=" %5.3f +- %5.3f " %(float(muon_btags[num].GetBinContent(4)),float(muon_btags[num].GetBinError(4)))
 

  #print "noB %s relative uncertainty %s" %(htbins[num],float(100*(muon_btags[num].GetBinError(1)/muon_btags[num].GetBinContent(1))))
  #print "oneB %s relative uncertainty %s" %(htbins[num],float(100*(muon_btags[num].GetBinError(2)/muon_btags[num].GetBinContent(2))))
  #print "twoB %s relative uncertainty %s" %(htbins[num],float(100*(muon_btags[num].GetBinError(3)/muon_btags[num].GetBinContent(3))))
  #print "threeB %s relative uncertainty %s" %(htbins[num],float(100*(muon_btags[num].GetBinError(4)/muon_btags[num].GetBinContent(4))))

  mu_yield.append(pred_three)
  mu_error.append(error_three)
  
  mu_zero.append(pred_zero)
  mu_zero_error.append(error_zero)


  mu_one.append(pred_one)
  mu_one_error.append(error_one)


  mu_two.append(pred_two)
  mu_two_error.append(error_two)



  plot.Draw("COLZTEXT")
  #c1.SaveAs("Muon_B_vs_noB_%s.C"%htbins[num])
  #c1.SaveAs("OneMuon_B_vs_noB_%s.png"%htbins[num])
l +="]\n"
s +="]\n"

a += "\n"
p += "\n"
c += "\n"
d += "\n"


a_ob += "\n\n\n"
p_ob += "\n\n\n"
c_ob += "\n\n\n"
d_ob += "\n\n\n"



Table_Pred.write(a)
Table_Pred.write(a_ob)

Table_Pred.write(p)
Table_Pred.write(p_ob)

Table_Pred.write(c)
Table_Pred.write(c_ob)

Table_Pred.write(d)
Table_Pred.write(d_ob)



#diffb0_muon.Draw()
#c1.SaveAs("diffb0_muon.png")
#diffb1_muon.Draw()
#c1.SaveAs("diffb1_muon.png")
#diffb2_muon.Draw()
#c1.SaveAs("diffb2_muon.png")
#diffb3_muon.Draw()
#c1.SaveAs("diffb3_muon.png")

#for num,hist in enumerate(muon_btags):
#  t +="%s   %s\n" %(htbins[num],hist.GetBinContent(4))

twobtag_bin_mu.write(t)
twobtag_bin_mu.close()

print "\n\n ================================ \n\n"


a = " Btag Zero    "
p = " Btag One   "
c = " Btag Two   "
d = " Btag Three   "


a_ob = " Btag Zero Ob  "
p_ob = " Btag One Ob "
c_ob = " Btag Two Ob "
d_ob = " Btag Three Ob "


l += "Had_Yield =["
s += "Had_Error = ["
for num,plot in enumerate(had_list):
  pred_three = 0
  error_three = 0
  pred_zero = 0
  pred_one = 0
  pred_two = 0
  e = btag_holder[1].GetBinContent(num+1)
  m = mistag_holder[1].GetBinContent(num+1)
  print e
  print m
  for b in range(2,plot.GetNbinsX()):
    for i in range(1,plot.GetNbinsY()):
      if b == 3: pred_three += i*m*pow((1-m),i-1)*b*(b-1)*0.5*e*e*pow((1-e),b-2)*plot.GetBinContent(b+1,i+1)
      else: pred_three += i*m*pow((1-m),i-1)*b*(b-1)*0.5*e*e*pow((1-e),b-2)*plot.GetBinContent(b+1,i+1)
  
  
  for b in range(3,plot.GetNbinsX()):
    for noB in range (1,plot.GetNbinsY()):
      if b == 3:pred_three += pow((1-m),noB)*b*(b-1)*(b-2)*e*e*e*pow((1-e),b-3)*(1/6)*plot.GetBinContent(b+1,noB+1)
      else:pred_three += pow((1-m),noB)*b*(b-1)*(b-2)*e*e*e*pow((1-e),b-3)*(1/6)*plot.GetBinContent(b+1,noB+1)
  
  for b in range (0,plot.GetNbinsX()):
    for noB in range(3,plot.GetNbinsY()):
      if b ==3:pred_three += pow((1-e),b)*noB*(noB-1)*(noB-2)*(1/6)*m*m*m*pow((1-m),noB-3)*plot.GetBinContent(b+1,noB+1)
      else:pred_three += pow((1-e),b)*noB*(noB-1)*(noB-2)*(1/6)*m*m*m*pow((1-m),noB-3)*plot.GetBinContent(b+1,noB+1)
  
  for b in range (1,plot.GetNbinsX()):
    for noB in range(2,plot.GetNbinsY()):
      if b == 3:pred_three += noB*e*pow((1-e),b-1)*noB*(noB-1)*0.5*m*m*pow((1-m),noB-2)*plot.GetBinContent(b+1,noB+1)
      else:pred_three += noB*e*pow((1-e),b-1)*noB*(noB-1)*0.5*m*m*pow((1-m),noB-2)*plot.GetBinContent(b+1,noB+1)
  
  error_three = (e*e*m)*sqrt(pow(plot.GetBinError(3,2),2 )+(4*(1-m)*(1-m)*pow(plot.GetBinError(3,3),2))+(9*pow((1-m),4)*pow(plot.GetBinError(3,4),2))+(16*pow((1-m),6)*pow(plot.GetBinError(3,5),2))+(25*pow((1-m),8)*pow(plot.GetBinError(3,6),2))     )
  
  for b in range (0,plot.GetNbinsX()):
    for noB in range(0,plot.GetNbinsY()):
      if b == 3: pred_zero += pow((1-e),b)*pow((1-m),noB)*plot.GetBinContent(b+1,noB+1)
      else:pred_zero += pow((1-e),b)*pow((1-m),noB)*plot.GetBinContent(b+1,noB+1)

  for b in range (0,plot.GetNbinsX()):
    for noB in range(1,plot.GetNbinsY()):
      if b == 3:pred_one += pow((1-e),b)*noB*m*pow((1-m),noB-1)*plot.GetBinContent(b+1,noB+1)
      else:pred_one += pow((1-e),b)*noB*m*pow((1-m),noB-1)*plot.GetBinContent(b+1,noB+1)
  
  for b in range(1,plot.GetNbinsX()):
    for noB in range(0,plot.GetNbinsY()):
      if b ==3:pred_one += pow((1-m),noB)*b*e*pow((1-e),b-1)*plot.GetBinContent(b+1,noB+1)
      else:pred_one += pow((1-m),noB)*b*e*pow((1-e),b-1)*plot.GetBinContent(b+1,noB+1)

  error_zero = 0
  sum_zero = 0
  for b in range(0,plot.GetNbinsX()):
    for noB in range(0,plot.GetNbinsY()):
              sum_zero += pow((plot.GetBinError(b+1,noB+1)*pow((1-e),b)*pow((1-m),noB)),2)

  error_zero = sqrt(sum_zero)
  
  sum_one = 0
  for b in range(1,plot.GetNbinsX()):
    for noB in range(1,plot.GetNbinsY()):
       sum_one += pow((pow((1-e),b-1)*pow((1-m),noB-1)*((noB*m*(1-e))+(noB*e*(1-m)))),2)*pow(plot.GetBinError(b+1,noB+1),2)
  
  error_one = sqrt( (m*m*pow(plot.GetBinError(1,2),2))+(e*e*pow(plot.GetBinError(2,1),2))+sum_one)
      
  
  for b in range (0,plot.GetNbinsX()):
    for noB in range(2,plot.GetNbinsY()):
      if b == 3: pred_two += pow((1-e),b)*noB*0.5*(noB-1)*m*m*pow((1-m),noB-2)*plot.GetBinContent(b+1,noB+1)
      else:pred_two += pow((1-e),b)*noB*0.5*(noB-1)*m*m*pow((1-m),noB-2)*plot.GetBinContent(b+1,noB+1)
  
  for b in range (2,plot.GetNbinsX()):
    for noB in range(0,plot.GetNbinsY()):
      if b == 3:pred_two += pow((1-m),noB)*0.5*b*(b-1)*e*e*pow((1-e),b-2)*plot.GetBinContent(b+1,noB+1)
      else: pred_two += pow((1-m),noB)*0.5*b*(b-1)*e*e*pow((1-e),b-2)*plot.GetBinContent(b+1,noB+1)
  
  for b in range (1,plot.GetNbinsX()):
    for noB in range(1,plot.GetNbinsY()):
      if b ==3:pred_two += b*e*pow((1-e),b-1)*noB*m*pow((1-m),m-1)*plot.GetBinContent(b+1,noB+1)
      else:pred_two += b*e*pow((1-e),b-1)*noB*m*pow((1-m),m-1)*plot.GetBinContent(b+1,noB+1)
  
  error_two = 0
  sum_two = 0
  for b in range (2,plot.GetNbinsX()):
    for noB in range(2,plot.GetNbinsY()):
      sum_two += pow(plot.GetBinError(b+1,noB+1),2)*(pow((1-e),b)*noB*0.5*(noB-1)*m*m*pow((1-m),noB-2)+pow((1-m),noB)*0.5*b*(b-1)*e*e*pow((1-e),b-2)+b*e*pow((1-e),b-1)*noB*m*pow((1-m),m-1))


  error_two = sqrt(m*m*pow(plot.GetBinError(1,3),2)+(pow(((1-e)*m*m)+(2*e*m*(1-m)) ,2)*pow(plot.GetBinError(2,3),2))+pow(e*plot.GetBinError(3,1),2)+pow(e*m*plot.GetBinError(2,2),2)+pow( (((1-m)*e*e)+(2*e*m*(1-m)))  ,2)*pow(plot.GetBinError(3,2),2)+sum_two)



  diffb0.Fill((pred_zero - had_btags[num].GetBinContent(1)) / had_btags[num].GetBinContent(1));
  diffb1.Fill((pred_one - had_btags[num].GetBinContent(2)) / had_btags[num].GetBinContent(2));
  diffb2.Fill((pred_two - had_btags[num].GetBinContent(3)) / had_btags[num].GetBinContent(3));
  diffb3.Fill((pred_three - had_btags[num].GetBinContent(4)) / had_btags[num].GetBinContent(4));

  ratio = (pred_three - had_btags[num].GetBinContent(4)) / had_btags[num].GetBinContent(4)

  print "noB %s observed  %s error  %s prediction %s with error %s " %(htbins[num],had_btags[num].GetBinContent(1),had_btags[num].GetBinError(1),pred_zero,error_zero)
  print "oneB %s obverved %s error %s prediction %s with error %s" %(htbins[num],had_btags[num].GetBinContent(2),had_btags[num].GetBinError(2),pred_one,error_one)
  print "twoB %s observed %s error  %s prediction %s with error %s" %(htbins[num],had_btags[num].GetBinContent(3),had_btags[num].GetBinError(3),pred_two,error_two)
  print "threeB %s  observed %s error %s  prediction  %s with error %s " %(htbins[num],had_btags[num].GetBinContent(4),had_btags[num].GetBinError(4),pred_three,error_three)
  f+="Prediction in %s bin  %f with error %f , Observed in bin %f with error %f \n" %(htbins[num],float(pred_three),float(error_three),float(had_btags[num].GetBinContent(4)),float(had_btags[num].GetBinError(4)))
  f+="This gives a ratio of pred-data/data ratio of %s\n\n\n" %ratio

  print "noB %s relative uncertainty %s" %(htbins[num],float(100*(had_btags[num].GetBinError(1)/had_btags[num].GetBinContent(1))))
  print "oneB %s relative uncertainty %s" %(htbins[num],float(100*(had_btags[num].GetBinError(2)/had_btags[num].GetBinContent(2))))
  print "twoB %s relative uncertainty %s" %(htbins[num],float(100*(had_btags[num].GetBinError(3)/had_btags[num].GetBinContent(3))))
  print "threeB %s relative uncertainty %s" %(htbins[num],float(100*(had_btags[num].GetBinError(4)/had_btags[num].GetBinContent(4))))

  a+=" %5.3f +- %5.3f " %(float(pred_zero),float(error_zero))
  p+=" %5.3f +- %5.3f " %(float(pred_one),float(error_one))
  c+=" %5.3f +- %5.3f " %(float(pred_two),float(error_two))
  d+=" %5.3f +- %5.3f " %(float(pred_three),float(error_three))


  a_ob+=" %5.3f +- %5.3f " %(float(had_btags[num].GetBinContent(1)),float(had_btags[num].GetBinError(1))) 
  p_ob+=" %5.3f +- %5.3f " %(float(had_btags[num].GetBinContent(2)),float(had_btags[num].GetBinError(2)))
  c_ob+=" %5.3f +- %5.3f " %(float(had_btags[num].GetBinContent(3)),float(had_btags[num].GetBinError(3)))
  d_ob+=" %5.3f +- %5.3f " %(float(had_btags[num].GetBinContent(4)),float(had_btags[num].GetBinError(4)))


  had_yield.append(pred_three)
  had_error.append(error_three)

  had_zero.append(pred_zero)
  had_zero_error.append(error_zero)


  had_one.append(pred_one)
  had_one_error.append(error_one)


  had_two.append(pred_two)
  had_two_error.append(error_two)


  l+="%f," %float(pred_three*46.5)
  s+="%f," %float(error_three*46.5)

  plot.Draw("COLZTEXT")
  #c1.SaveAs("Had_B_vs_noB_%s.C"%htbins[num])
  #c1.SaveAs("Had_B_vs_noB_%s.png"%htbins[num])

diffb0.Draw()
#c1.SaveAs("diffb0_had.png")
diffb1.Draw()
#c1.SaveAs("diffb1_had.png")
diffb2.Draw()
#c1.SaveAs("diffb2_had.png")
diffb3.Draw()
#c1.SaveAs("diffb3_had.png")
l +="]\n"
s +="]\n"

a += "\n"
p += "\n"
c += "\n"
d += "\n"


a_ob += "\n\n\n"
p_ob += "\n\n\n"
c_ob += "\n\n\n"
d_ob += "\n\n\n"



Table_Make.write(a)
Table_Make.write(a_ob)

Table_Make.write(p)
Table_Make.write(p_ob)

Table_Make.write(c)
Table_Make.write(c_ob)

Table_Make.write(d)
Table_Make.write(d_ob)



twobtag_bin.write(f)
twobtag_bin.close()

"""
ted_yields.write(l)
ted_yields.write(s)
ted_yields.close()

htbin = [275,325,375,475,575,675,775,875]
#File = r.TFile("Btag_Two_Translation_Factors_minus.root","RECREATE") 
#file = r.tfile.open("btag_two_translation_factors.root")

tags = ["zero","one","two","three"]
tag_keeper = []
for entry in tags:
  plot = r.TH1F("%s"%entry,"",8,0,8)
  #plot = r.TH1F("Plus","",8,0,8)
  plot.GetXaxis().SetTitle("H_{T} (GeV)")
  plot.GetYaxis().SetTitle("Translation Factor")
  plot.GetYaxis().SetTitleOffset(1.30)
  plot.GetXaxis().SetTitleSize(0.04)
  plot.GetYaxis().SetTitleSize(0.04)
  plot.GetYaxis().SetRangeUser(0,3)
  plot.GetSumw2()
  plot.SetMarkerStyle(20)
  plot.SetMarkerSize(1.5)
  plot.SetLineWidth(2)
  for num,lab in enumerate(htbin): plot.GetXaxis().SetBinLabel(num+1,str(lab))
  tag_keeper.append(plot)

trans_two_btag = open('Translation_Factors_plus.txt','w')
g = ""

array_keeper = [had_zero,had_one,had_two,had_yield]
array_keeper_error = [had_zero_error,had_one_error,had_two_error,had_error]


mu_array_keeper = [mu_zero,mu_one,mu_two,mu_yield]
mu_array_keeper_error = [mu_zero_error,mu_one_error,mu_two_error,mu_error]


#for histogram in tag_keeper:
for box,entry in enumerate(array_keeper):
    for num,plot in enumerate(had_zero):
      translation = array_keeper[box][num]/mu_array_keeper[box][num]
      #if box == 3:
        #print array_keeper[box][num]*46.5
        #print mu_array_keeper[box][num]*46.5
        #print translation
      histogram = tag_keeper[box]
      trans_error = translation * sqrt(pow((array_keeper_error[box][num]/array_keeper[box][num]),2)+pow((mu_array_keeper_error[box][num]/mu_array_keeper[box][num]),2))
      histogram.SetBinContent(num+1,array_keeper[box][num]/mu_array_keeper[box][num])
      histogram.SetBinError(num+1,translation * sqrt(pow((array_keeper_error[box][num]/array_keeper[box][num]),2)+pow((mu_array_keeper_error[box][num]/mu_array_keeper[box][num]),2)))
      #g += "HTBin: %s  %s  +-   %s\n " %(htbins[num],translation,trans_error)
    histogram.Write()      
trans_two_btag.write(g)
trans_two_btag.close()
File.cd("")



File_had = r.TFile("Btag_Two_Had_Change_minus.root","RECREATE") 
File_mu = r.TFile("Btag_Two_Mu_Change_minus.root","RECREATE") 

had_keeper =[]
mu_keeper = []
#file = r.tfile.open("btag_two_translation_factors.root")
for entry in tags:
  plot = r.TH1F("%s"%entry,"",8,0,8)
  #plot = r.TH1F("Plus","",8,0,8)
  plot.GetXaxis().SetTitle("H_{T} (GeV)")
  plot.GetYaxis().SetTitle("Yield")
  plot.GetYaxis().SetTitleOffset(1.30)
  plot.GetXaxis().SetTitleSize(0.04)
  plot.GetYaxis().SetTitleSize(0.04)
  plot.GetYaxis().SetRangeUser(0,300)
  plot.GetSumw2()
  plot.SetMarkerStyle(20)
  plot.SetMarkerSize(1.5)
  plot.SetLineWidth(2)
  for num,lab in enumerate(htbin): plot.GetXaxis().SetBinLabel(num+1,str(lab))

  mu_plot = plot.Clone()
  had_keeper.append(plot)
  mu_keeper.append(mu_plot)


for box,entry in enumerate(array_keeper):
  for num in range(0,8):
    plot = had_keeper[box]
    mu_plot = mu_keeper[box]
    plot.SetBinContent(num+1,array_keeper[box][num]*46.5)
    mu_plot.SetBinContent(num+1,mu_array_keeper[box][num]*46.5)
  
  File_had.cd()
  plot.Write()
  File_mu.cd()
  mu_plot.Write()
#File_had.Write(plot)
#File_mu.Write(mu_plot)



def Translation_Calc(had,had_error,muon,muon_error,txt,preamble = ""):


  trans_factor = []
  trans_error = []

  for num,entry in enumerate(had):
    trans_factor.append(had[num]/muon[num])
    trans_error.append((had[num]/muon[num])*sqrt(pow((had_error[num]/had[num]),2)+pow((muon_error[num]/muon[num]),2)))

  binning = ["275_325","325_375","375_475","475_575","575_675","675_775","775_875","875"]

  txt += "\n\n"
  txt += "|     %s        |\n\n" %preamble
  for num,entry in enumerate(binning):
    txt += "%s    :     %5.4f   +-   %5.4f \n"  %(entry,float(trans_factor[num]),float(trans_error[num]))
  txt += "\n\n\n"
  Trans_and_Errors.write(txt)

txt = ""
Trans_and_Errors = open('Translation_Factors_Plus_Errors.txt','w')

Translation_Calc(had_zero,had_zero_error,mu_zero,mu_zero_error,txt,preamble = "Zero Btags")
Translation_Calc(had_one,had_one_error,mu_one,mu_one_error,txt,preamble = "One Btags")
Translation_Calc(had_two,had_two_error,mu_two,mu_two_error,txt,preamble = "Two Btags")
Translation_Calc(had_yield,had_error,mu_yield,mu_error,txt,preamble = "More than Two Btags")

"""


"""
mu_data = r.Tfile.open("Muon_Data.root")
had_data = r.Tfile.open("Had_Data.root")


File = r.TFile("Approval_Plots.root","RECREATE") 
hist = r.TH1F("Btag Multiplicity","",6,0,6)
hist.GetXaxis().SetTitle("Num Btags")
hist.GetYaxis().SetTitle("Events")

DirKeys_mu = mu_data.GetListOfKeys()
DirKeys_had = had_data.GetListOfKeys()

keys = ["btag_zero","btag_one","btag_two","btag_morethantwo_"]


histos = []
for sum,entry in enumerate(htbins):
  plot = hist.Clone()
  histos.append(plot)
  

for sum,entry in enumerate(keys):
  for num,bin in enumerate(htbins):
      for key in DirKeys_mu:
        subdirect = file.FindObjectAny(key.GetName())
        dir = "OneMuon_"+category+bin
        subdirect.GetName()
        if dir == subdirect.GetName():
          for subkey in subdirect.GetListOfKeys():
            if num == 0 or num ==1:
              if subkey.GetName() == "Btag_Post_AlphaT_5_55_all":
                plot = predict_file_muon.Get(dir+"/"+subkey.GetName())
                if sum == 3:
                else:plot.GetBinContent(sum+1)
            else: 
              if subkey.GetName() == "Btag_Pre_AlphaT_5__all":
                plot = predict_file_muon.Get(dir+"/"+subkey.GetName())
                if
                else:plot.GetBinContent(sum+1)
"""       
