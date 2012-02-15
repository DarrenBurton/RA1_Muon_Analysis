#!/usr/bin/env python
import setupSUSY
from libFrameworkSUSY import *
from libbryn import *
from libHadronic import *
from libOneLepton import *
from icf.core import PSet,Analysis
from time import strftime
import icf.utils as Utils
from batchGolden_baseline import *
from batchGolden_btag import *
from ra1objectid.vbtfElectronId_cff import *
from ra1objectid.vbtfMuonId_cff import *
from ra1objectid.ra3PhotonId_cff import *



vbtfMuonId_cff = Muon_IDFilter( vbtfmuonidps.ps()  )
cutTreeMC,junkVar,l = MakeMCTree(100.,Muon = True,Split = "Muon_Two")
cutTreeBtagMC,junkVarm,m = MakeBtagMCTree(100.,Muon = True,Split = "Muon_Two")
vbtfElectronIdFilter = Electron_IDFilter( vbtfelectronidWP95ps.ps() )
ra3PhotonIdFilter    = Photon_IDFilter( ra3photonidps.ps() )
CustomMuID = OL_CustomVBTFMuID(mu_id_higher.ps())
CustomMuID_AlphaT = OL_CustomVBTFMuID(mu_id_lower.ps())

def addCutFlowMC(b) :
   b.AddWeightFilter("Weight", vertex_reweight)
   b.AddMuonFilter("PreCC",CustomMuID_AlphaT)
   b.AddPhotonFilter("PreCC",ra3PhotonIdFilter)
   b.AddElectronFilter("PreCC",vbtfElectronIdFilter)
   b+=cutTreeMC

def addCutFlowBtagMC(a) :
  a.AddWeightFilter("Weight",vertex_reweight)
  a.AddPhotonFilter("PreCC",ra3PhotonIdFilter)
  a.AddElectronFilter("PreCC",vbtfElectronIdFilter)
  a.AddMuonFilter("PreCC",CustomMuID)
#  a+=cutTreeBtagMC

#AK5 Calo
conf_ak5_caloMC = deepcopy(defaultConfig)
conf_ak5_caloMC.Ntuple = deepcopy(ak5_calo)
conf_ak5_caloMC.XCleaning = deepcopy(default_cc)
conf_ak5_caloMC.Common = deepcopy(default_common)
#conf_ak5_caloMC.Common.print_out()
anal_ak5_caloMC=Analysis("AK5Calo")
addCutFlowMC(anal_ak5_caloMC)

conf_ak5_caloBtagData = deepcopy(defaultConfig)
conf_ak5_caloBtagData.Ntuple = deepcopy(ak5_calo)
conf_ak5_caloBtagData.XCleaning = deepcopy(default_cc)
conf_ak5_caloBtagData.Common = deepcopy(default_common)
# conf_ak5_calo.Common.print_out()
anal_ak5_caloBtagData=Analysis("AK5Calo")
addCutFlowBtagMC(anal_ak5_caloBtagData)


outDir = "../results_"+strftime("%d_%b")+"//MuonNoSmear_2_Btag/"

#outDir = "../results_"+strftime("%d_%b")+"//MuonNoSmear_2/"
ensure_dir(outDir)

#from CMSSM_Skim import *

#anal_ak5_caloMC.Run(outDir,conf_ak5_caloMC,CMSSM_Skim)

#anal_ak5_caloMC.Run(outDir,conf_ak5_caloMC,L1OffSet_MC_Higher_Bins)
anal_ak5_caloBtagData.Run(outDir,conf_ak5_caloBtagData,L1OffSet_MC_Higher_Bins)

#anal_ak5_caloMC.Run(outDir,conf_ak5_caloMC,Summer11_MC_Higher_Bins)
#anal_ak5_caloBtagData.Run(outDir,conf_ak5_caloBtagData,Summer11_MC_Higher_Bins)
