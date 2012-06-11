#!/usr/bin/env python
from ROOT import *
import ROOT as r
from math import *
import logging,itertools
import os,fnmatch,sys
import glob, errno
from time import strftime
from optparse import OptionParser
import array, ast

file = sys.argv[1]
path = sys.argv[2]

htbins = ["275_325","325_375","375_475","475_575","575_675","675_775","775_875","875"]


temp = r.TFile.Open(file)
DirKeys = temp.GetListOfKeys()
plots = []
#single_eff = 0.913
single_eff = 0.88
for key in DirKeys:
  subdirect = temp.FindObjectAny(key.GetName())
  for bin in htbins:
    dir = path+bin
    if dir == subdirect.GetName():
      for subkey in subdirect.GetListOfKeys():
        if subkey.GetName() == "TwoMuPt_all":
          plot = temp.Get(dir+"/"+subkey.GetName())
          plots.append(plot)



for num,entry in enumerate(plots):
   
  tot = entry.GetBinContent(1)+entry.GetBinContent(2)
  lower_eff = entry.GetBinContent(1)/tot
  higher_eff = entry.GetBinContent(2)/tot
  efficiency = (single_eff*lower_eff)+((1-pow((1-single_eff),2))*higher_eff)
  print "%s: %s" %(htbins[num],efficiency)
