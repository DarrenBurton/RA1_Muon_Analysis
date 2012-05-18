#!/usr/bin/env python
from ROOT import *
import ROOT as r
import logging,itertools
import os,fnmatch,sys
import glob, errno
from time import strftime
from optparse import OptionParser
import array, ast


btag = {'Zero':{},'One':{},'Two':{},'Three':{}}
samples = {'DiMuon':{},'Muon':{},'TotalSM':{}}
dict_entries = ('Trans','Trans_Error','Formula','Formula_Error')

for key in btag:
   btag[key] = dict.fromkeys(samples)
   for entry in samples:
        btag[key][entry] = dict.fromkeys(dict_entries,0)

for num in btag:
  for key in samples:
    for entry in dict_entries:
       btag[num][key][entry] = []

def Insert_Dictionary(mu,mu_err,di,di_err,tot,tot_err,f_mu,f_mu_err,f_di,f_di_err,f_tot,f_tot_err,btag_mult):
     
    for entry in btag[btag_mult]:
          for an in btag[btag_mult][entry]:
             if entry == "Muon":
                btag[btag_mult][entry]['Trans'] = mu
                btag[btag_mult][entry]['Trans_Error'] = mu_err
                btag[btag_mult][entry]['Formula'] = f_mu
                btag[btag_mult][entry]['Formula_Error'] = f_mu_err
             if entry == "DiMuon":
                btag[btag_mult][entry]['Trans'] = di
                btag[btag_mult][entry]['Trans_Error'] = di_err
                btag[btag_mult][entry]['Formula'] = f_di
                btag[btag_mult][entry]['Formula_Error'] = f_di_err
             if entry == "TotalSM":   
                btag[btag_mult][entry]['Trans'] = tot
                btag[btag_mult][entry]['Trans_Error'] = tot_err
                btag[btag_mult][entry]['Formula'] = f_tot
                btag[btag_mult][entry]['Formula_Error'] = f_tot_err

#======= Zero ============
mu_zero = [1.41,1.13,0.20,0.16,0.13,0.10,0.07,0.04 ]
mu_err_zero = [ 0.11,0.15,0.00,0.01,0.01,0.01,0.01,0.01]
di_zero = [ 13.68,9.64,1.84,1.45,1.24,0.90,0.72,0.61]
di_err_zero = [0.93,0.91,0.09,0.12,0.14,0.14,0.21,0.14]
tot_zero = [2.73,2.32,0.45,0.36,0.30,0.23,0.18,0.10]
tot_err_zero = [0.18,0.24,0.01,0.02,0.02,0.02,0.02,0.01]

f_mu_zero = [1.38,1.13,0.2,0.16,0.12,0.09,0.07,0.04]
f_mu_err_zero = [0.10,0.14,0.01,0.01,0.01,0.01,0.01,0.00]
f_di_zero = [12.83,9.51,1.80,1.45,1.26,0.93,0.68,0.58]
f_di_err_zero = [0.83,0.96,0.08,0.12,0.14,0.14,0.18,0.13]
f_tot_zero = [2.66,2.31,0.45,0.36,0.31,0.22,0.18,0.10]
f_tot_err_zero = [0.16,0.22,0.01,0.02,0.02,0.02,0.02,0.01]

#Insert_Dictionary(mu,mu_err,di,di_err,tot,tot_err,f_mu,f_mu_err,f_di,f_di_err,f_tot,f_tot_err,"Zero")

# ===== One =======


tot_one = [1.56,1.61,0.33,0.26,0.19,0.22,0.11,0.06]
tot_err_one = [0.12,0.20,0.01,0.02,0.02,0.04,0.03,0.01]
di_one = [8.94,10.74,1.75,1.58,0.93,0.94,0.87,0.43]
di_err_one = [1.38,2.89,1.75,1.58,0.93,0.94,0.87,0.43]
mu_one = [1.11,1.17,0.24,0.18,0.13,0.17,0.08,0.03]
mu_err_one = [0.09,0.17,0.01,0.02,0.02,0.04,0.02,0.01]

f_mu_one = [1.14,1.07,0.23,0.19,0.14,0.15,0.07,0.05]
f_mu_err_one = [0.06,0.08,0.02,0.03,0.03,0.05,0.03,0.01]
f_di_one = [9.58,9.07,1.76,1.46,1.06,0.90,1.24,0.52]
f_di_err_one = [1.33,2.00,0.16,0.18,0.14,0.31,0.16,0.47]
f_tot_one = [1.54,1.49,0.32,0.27,0.20,0.21,0.11,0.07] 
f_tot_err_one = [0.07,0.10,0.02,0.03,0.03,0.05,0.03,0.02]


#Insert_Dictionary(mu,mu_err,di,di_err,tot,tot_err,f_mu,f_mu_err,f_di,f_di_err,f_tot,f_tot_err,"One")

# ===== Two =======

mu_two = [1.22,1.05,0.18,0.18,0.13,0.14,0.05,0.08]
mu_err_two = [0.16,0.16,0.02,0.03,0.03,0.04,0.03,0.04]
di_two = [ 6.28,1.91,0.84,0.88,1.55,0.42,2.86,0]
di_err_two =[1.80,1.74,0.18,0.28,0.80,0.32,3.27,0]
tot_two = [1.36,1.19,0.21,0.20,0.15,0.15,0.02,0.08]
tot_err_two = [0.17,0.17,0.02,0.03,0.03,0.04,0.03,0.04]

f_tot_two = [1.19,1.04,0.21,0.19,0.13,0.23,0.06,0.06]
f_tot_err_two = [0.08,0.11,0.01,0.02,0.02,0.06,0.03,0.03]
f_di_two = [5.55,2.83,0.75,0.90,0.85,0.71,0.66,0.52]
f_di_err_two = [1.31,3.09,0.14,0.26,0.33,0.54,0.86,0.21]
f_mu_two = [1.05,0.91,0.19,0.17,0.11,0.21,0.05,0.05]
f_mu_err_two = [0.07,0.10,0.01,0.02,0.02,0.06,0.03,0.03]


#Insert_Dictionary(mu,mu_err,di,di_err,tot,tot_err,f_mu,f_mu_err,f_di,f_di_err,f_tot,f_tot_err,"Two")

# ==== Three ===

mu_three = [1.13,1.17,0.16,0.19,0.07,0.13,0.01,0.03]
mu_err_three = [4.27,3.61,1.20,1.34,0.04,0.12,0.01,0.04]
di_three = [0,0,0,0,0,0,0,0]
di_err_three = [0,0,0,0,0,0,0,0]
tot_three = [1.22,1.32,0.17,0.20,0.07,0.17,0.01,0.03]
tot_err_three = [0.31,0.40,0.04,0.07,0.04,0.12,0.01,0.04]

f_mu_three = [1.06,1.01,0.22,0.22,0.14,0.30,0.06,0.05]
f_mu_err_three = [0.05,0.08,0.01,0.02,0.02,0.05,0.02,0.01]
f_di_three = [0,0,0,0,0,0,0,0]
f_di_err_three = [0,0,0,0,0,0,0,0]
f_tot_three = [1.11,1.06,0.23,0.23,0.15,0.30,0.06,0.05]
f_tot_err_three = [0.05,0.08,0.01,0.02,0.02,0.05,0.02,0.01]


#Insert_Dictionary(mu,mu_err,di,di_err,tot,tot_err,f_mu,f_mu_err,f_di,f_di_err,f_tot,f_tot_err,"Three")

c1 = r.TCanvas("canvas","canvas")
c1.cd()

plotmu_0 = TH1F("Muon_0","",8,0.5,8.5)
plotmu_f_0 = TH1F("Muon_0f","",8,0.5,8.5)
plotmu_1 = TH1F("Muon_1","",8,0.5,8.5)
plotmu_f_1 = TH1F("Muon_1f","",8,0.5,8.5)
plotmu_2 = TH1F("Muon_2","",8,0.5,8.5)
plotmu_f_2 = TH1F("Muon_2f","",8,0.5,8.5)
plotmu_3 = TH1F("Muon_3","",8,0.5,8.5)
plotmu_f_3 = TH1F("Muon_3f","",8,0.5,8.5)

for num in range(0,8):
  plotmu_0.SetBinContent(num+1,mu_zero[num])
  plotmu_0.SetBinError(num+1,mu_err_zero[num])

  plotmu_f_0.SetBinContent(num+1,f_mu_zero[num])
  plotmu_f_0.SetBinError(num+1,f_mu_err_zero[num])

  plotmu_1.SetBinContent(num+1,mu_one[num])
  plotmu_1.SetBinError(num+1,mu_err_one[num])

  plotmu_f_1.SetBinContent(num+1,f_mu_one[num])
  plotmu_f_1.SetBinError(num+1,f_mu_err_one[num])

  plotmu_2.SetBinContent(num+1,mu_two[num])
  plotmu_2.SetBinError(num+1,mu_err_two[num])

  plotmu_f_2.SetBinContent(num+1,f_mu_two[num])
  plotmu_f_2.SetBinError(num+1,f_mu_err_two[num])

  plotmu_3.SetBinContent(num+1,mu_three[num])
  plotmu_3.SetBinError(num+1,mu_err_three[num])

  plotmu_f_3.SetBinContent(num+1,f_mu_three[num])
  plotmu_f_3.SetBinError(num+1,f_mu_err_three[num])

c1.SetLogy()


leg = r.TLegend(0.68,0.53,0.80,0.75)
leg.SetTextSize(0.02)
leg.SetFillColor(0)
leg.SetLineColor(0)


plotmu_0.SetLineColor(kBlack)
plotmu_0.SetMarkerSize(10)
leg.AddEntry(plotmu_0,"Event Reweighted","L")
plotmu_0.Draw("P")
leg.AddEntry(plotmu_f_0,"Formula","L")
plotmu_f_0.Draw("PSAME")
leg.Draw("SAME")
c1.SaveAs("Mu_Zero.png")

plotmu_1.SetLineColor(kBlack)
plotmu_1.Draw("P")
plotmu_f_1.Draw("PSAME")

leg.Draw("SAME")
c1.SaveAs("Mu_One.png")

plotmu_2.SetLineColor(kBlack)
plotmu_2.Draw("P")
plotmu_f_2.Draw("PSAME")
leg.Draw("SAME")
c1.SaveAs("Mu_Two.png")

plotmu_3.SetLineColor(kBlack)
plotmu_3.Draw("P")
plotmu_f_3.Draw("PSAME")
leg.Draw("SAME")
c1.SaveAs("Mu_Three.png")



plotdimu_0 = TH1F("DiMuon_0","",8,0.5,8.5)
plotdimu_f_0 = TH1F("DiMuon_0f","",8,0.5,8.5)
plotdimu_1 = TH1F("DiMuon_1","",8,0.5,8.5)
plotdimu_f_1 = TH1F("DiMuon_1f","",8,0.5,8.5)
plotdimu_2 = TH1F("DiMuon_2","",8,0.5,8.5)
plotdimu_f_2 = TH1F("DiMuon_2f","",8,0.5,8.5)
plotdimu_3 = TH1F("DiMuon_3","",8,0.5,8.5)
plotdimu_f_3 = TH1F("DiMuon_3f","",8,0.5,8.5)


for num in range(0,8):
  plotdimu_0.SetBinContent(num+1,di_zero[num])
  plotdimu_0.SetBinError(num+1,di_err_zero[num])

  plotdimu_f_0.SetBinContent(num+1,f_di_zero[num])
  plotdimu_f_0.SetBinError(num+1,f_di_err_zero[num])

  plotdimu_1.SetBinContent(num+1,di_one[num])
  plotdimu_1.SetBinError(num+1,di_err_one[num])

  plotdimu_f_1.SetBinContent(num+1,f_di_one[num])
  plotdimu_f_1.SetBinError(num+1,f_di_err_one[num])

  plotdimu_2.SetBinContent(num+1,di_two[num])
  plotdimu_2.SetBinError(num+1,di_err_two[num])

  plotdimu_f_2.SetBinContent(num+1,f_di_two[num])
  plotdimu_f_2.SetBinError(num+1,f_di_err_two[num])

  plotdimu_3.SetBinContent(num+1,di_three[num])
  plotdimu_3.SetBinError(num+1,di_err_three[num])

  plotdimu_f_3.SetBinContent(num+1,f_di_three[num])
  plotdimu_f_3.SetBinError(num+1,f_di_err_three[num])

c1.SetLogy()


leg = r.TLegend(0.68,0.53,0.80,0.75)
leg.SetTextSize(0.02)
leg.SetFillColor(0)
leg.SetLineColor(0)


plotdimu_0.SetLineColor(kBlack)
plotdimu_0.SetMarkerSize(10)
leg.AddEntry(plotdimu_0,"Event Reweighted","L")
plotdimu_0.Draw("P")
leg.AddEntry(plotdimu_f_0,"Formula","L")
plotdimu_f_0.Draw("PSAME")
leg.Draw("SAME")
c1.SaveAs("DiMu_Zero.png")

plotdimu_1.SetLineColor(kBlack)
plotdimu_1.Draw("P")
plotdimu_f_1.Draw("PSAME")

leg.Draw("SAME")
c1.SaveAs("DiMu_One.png")

plotdimu_2.SetLineColor(kBlack)
plotdimu_2.Draw("P")
plotdimu_f_2.Draw("PSAME")
leg.Draw("SAME")
c1.SaveAs("DiMu_Two.png")

plotdimu_3.SetLineColor(kBlack)
plotdimu_3.Draw("P")
plotdimu_f_3.Draw("PSAME")
leg.Draw("SAME")
c1.SaveAs("DiMu_Three.png")


plot_tot_0 = TH1F("TotSM_0","",8,0.5,8.5)
plot_tot_f_0 = TH1F("TotSM_0f","",8,0.5,8.5)
plot_tot_1 = TH1F("TotSM_1","",8,0.5,8.5)
plot_tot_f_1 = TH1F("TotSM_1f","",8,0.5,8.5)
plot_tot_2 = TH1F("TotSM_2","",8,0.5,8.5)
plot_tot_f_2 = TH1F("TotSM_2f","",8,0.5,8.5)
plot_tot_3 = TH1F("TotSM_3","",8,0.5,8.5)
plot_tot_f_3 = TH1F("TotSM_3f","",8,0.5,8.5)


for num in range(0,8):
  plot_tot_0.SetBinContent(num+1,tot_zero[num])
  plot_tot_0.SetBinError(num+1,tot_err_zero[num])

  plot_tot_f_0.SetBinContent(num+1,f_tot_zero[num])
  plot_tot_f_0.SetBinError(num+1,f_tot_err_zero[num])

  plot_tot_1.SetBinContent(num+1,tot_one[num])
  plot_tot_1.SetBinError(num+1,tot_err_one[num])

  plot_tot_f_1.SetBinContent(num+1,f_tot_one[num])
  plot_tot_f_1.SetBinError(num+1,f_tot_err_one[num])

  plot_tot_2.SetBinContent(num+1,tot_two[num])
  plot_tot_2.SetBinError(num+1,tot_err_two[num])

  plot_tot_f_2.SetBinContent(num+1,f_tot_two[num])
  plot_tot_f_2.SetBinError(num+1,f_tot_err_two[num])

  plot_tot_3.SetBinContent(num+1,tot_three[num])
  plot_tot_3.SetBinError(num+1,tot_err_three[num])

  plot_tot_f_3.SetBinContent(num+1,f_tot_three[num])
  plot_tot_f_3.SetBinError(num+1,f_tot_err_three[num])

c1.SetLogy()


leg = r.TLegend(0.68,0.53,0.80,0.75)
leg.SetTextSize(0.02)
leg.SetFillColor(0)
leg.SetLineColor(0)


plot_tot_0.SetLineColor(kBlack)
plot_tot_0.SetMarkerSize(10)
leg.AddEntry(plot_tot_0,"Event Reweighted","L")
plot_tot_0.Draw("P")
leg.AddEntry(plot_tot_f_0,"Formula","L")
plot_tot_f_0.Draw("PSAME")
leg.Draw("SAME")
c1.SaveAs("TotSM_Zero.png")

plot_tot_1.SetLineColor(kBlack)
plot_tot_1.Draw("P")
plot_tot_f_1.Draw("PSAME")

leg.Draw("SAME")
c1.SaveAs("TotSM_One.png")

plot_tot_2.SetLineColor(kBlack)
plot_tot_2.Draw("P")
plot_tot_f_2.Draw("PSAME")
leg.Draw("SAME")
c1.SaveAs("TotSM_Two.png")

plot_tot_3.SetLineColor(kBlack)
plot_tot_3.Draw("P")
plot_tot_f_3.Draw("PSAME")
leg.Draw("SAME")
c1.SaveAs("TotSM_Three.png")





 
"""
for entry in btag:
    print "Making %s plots" %entry
    for dir in btag[entry]:
        if dir == "Muon":
             plotmu_%s = TH1F("Muon","",8,0,8)
             plotmu_2_%s = TH1F("Muon","",8,0,8)
             for num in range(0,8):
                plotmu.SetBinContent(num,btag[entry][dir]["Formula"][num])
                plotmu.SetBinError(num,btag[entry][dir]["Formula_Error"][num])
             
                plotmu_2.SetBinContent(num,btag[entry][dir]["Trans"][num])
                plotmu_2.SetBinError(num,btag[entry][dir]["Trans_Error"][num])
             plotmu.Draw("PSAME")
             plotmu_2.Draw("PSAME")

    c1.SaveAs("Test.png")  
"""  
