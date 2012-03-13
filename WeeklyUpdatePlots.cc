#include "WeeklyUpdatePlots.hh"
#include "CommonOps.hh"
#include "EventData.hh"
#include "KinSuite.hh"
#include "TH1D.h"
#include "TH2D.h"
#include "Types.hh"
#include "mt2_bisect.hh"
#include "AlphaT.hh"
#include "Jet.hh"
#include "Math/VectorUtil.h"
#include "JetData.hh"
#include "TMath.h"
#include "GenMatrixBin.hh"

using namespace Operation;

// -----------------------------------------------------------------------------
WeeklyUpdatePlots::WeeklyUpdatePlots( const Utils::ParameterSet& ps ) :
// Misc
dirName_( ps.Get<std::string>("DirName") ),
  nMin_( ps.Get<int>("MinObjects") ),
  nMax_( ps.Get<int>("MaxObjects") ),
// MT2
  StandardPlots_( ps.Get<bool>("StandardPlots") )

  {}

// -----------------------------------------------------------------------------
//
WeeklyUpdatePlots::~WeeklyUpdatePlots() {}

// -----------------------------------------------------------------------------
//
void WeeklyUpdatePlots::Start( Event::Data& ev ) {
  initDir( ev.OutputFile(), dirName_.c_str() );
  BookHistos();
}

// -----------------------------------------------------------------------------
//
void WeeklyUpdatePlots::BookHistos() {
  if ( StandardPlots_ )           { StandardPlots(); }
}

// -----------------------------------------------------------------------------
//
bool WeeklyUpdatePlots::Process( Event::Data& ev ) {
  if ( StandardPlots_ )               { StandardPlots(ev); }
  return true;
}

// -----------------------------------------------------------------------------
//
std::ostream& WeeklyUpdatePlots::Description( std::ostream& ostrm ) {
  ostrm << "Hadronic Common Plots ";
  ostrm << "(bins " << nMin_ << " to " << nMax_ << ") ";
  return ostrm;
}

// -----------------------------------------------------------------------------
//
void WeeklyUpdatePlots::StandardPlots() {




  BookHistArray( vertexPtovHT_,
    "vertexPtovHT",
    ";VertexPt / HT (GeV);Events/0.01;",
    1000, 0., 10.,
    nMax_+1, 0, 1, true );


  BookHistArray( vertexPtovHT_afterAlphaT_55_,
    "vertexPtovHT_afterAlphaT_55",
    ";VertexPt / HT (GeV);Events/0.01;",
    1000, 0., 10.,
    nMax_+1, 0, 1, true );

  BookHistArray( vertexPtovHT_afterAlphaT_53_,
    "vertexPtovHT_afterAlphaT_53",
    ";VertexPt / HT (GeV);Events/0.01;",
    1000, 0., 10.,
    nMax_+1, 0, 1, true );

  BookHistArray( vertexPtovHT_afterAlphaT_52_,
    "vertexPtovHT_afterAlphaT_52",
    ";VertexPt / HT (GeV);Events/0.01;",
    1000, 0., 10.,
    nMax_+1, 0, 1, true );

  BookHistArray( NumberVerticiesAfterAlphaT_55_,
    "Number_Primary_verticies_after_alphaT_55",
    ";No.Vertercies;Events;",
    50,0.,50,
    nMax_+1, 0, 1, true );

  BookHistArray( NumberVerticiesAfterAlphaT_53_,
    "Number_Primary_verticies_after_alphaT_53",
    ";No.Vertercies;Events;",
    50,0.,50,
    nMax_+1, 0, 1, true );

  BookHistArray( NumberVerticiesAfterAlphaT_52_,
    "Number_Primary_verticies_after_alphaT_52",
    ";No.Vertercies;Events;",
    50,0.,50,
    nMax_+1, 0, 1, true );


  BookHistArray( NumberVerticies_,
    "Number_Primary_verticies",
    ";No.Vertercies;Events;",
    50,0.,50,
    nMax_+1, 0, 1, true );


  BookHistArray( DPhi_MHT_MHTBaby_,
    "CosDetlaPhi_MHT_MHTBaby",
    ";#Delta Cos#phi(MHT,MHTbaby); Events/0.65 rad;",
    40, -1., 1,
    nMax_+1, 0, 1, true );


  BookHistArray( MissedHT_,
    "MHTRatio_after_alphaT_55",
    ";MHT30/MHT10;Events/0.1;",
    100, 0., 10,
    nMax_+1, 0, 1, true );

  BookHistArray( MHTovMET_,
    "MHTovMET",
    ";MHT/MET;Events/0.1;",
    1000, 0., 100,
    nMax_+1, 0, 1, true );

  BookHistArray( MHTovMET_afterAlphaT_55_,
    "MHTovMET_afterAlphaT_55",
    ";MHT/MET;Events/0.1;",
    1000, 0., 100,
    nMax_+1, 0, 1, true );
 
  BookHistArray( MHTovMET_afterAlphaT_53_,
    "MHTovMET_afterAlphaT_53",
    ";MHT/MET;Events/0.1;",
    1000, 0., 100,
    nMax_+1, 0, 1, true );

  BookHistArray( MHTovMET_afterAlphaT_52_,
    "MHTovMET_afterAlphaT_52",
    ";MHT/MET;Events/0.1;",
    1000, 0., 100,
    nMax_+1, 0, 1, true );
  
  BookHistArray( DetlaPhi_LeadingJets_,
    "DetlaPhi_LeadingJets",
    ";#Delta #phi(j_{1},j_{i}); Events/0.65 rad;",
    40, 0., TMath::Pi(),
    nMax_+1, 0, 1, true );

  BookHistArray( DetlaPhi_NextToLeadingJets_,
    "DetlaPhi_NextToLeadingJets",
    ";#Delta #phi(j_{2},j_{3}); Events/0.65 rad;",
    40, 0., TMath::Pi(),
    nMax_+1, 0, 1, true );

  BookHistArray( DetlaPhi_LeadingJets_afterAlphaT_55_,
    "DetlaPhi_LeadingJets_afterAlphaT_55",
    ";#Delta #phi(j_{1},j_{i}); Events/0.65 rad;",
    40, 0., TMath::Pi(),
    nMax_+1, 0, 1, true );

  BookHistArray( DetlaPhi_NextToLeadingJets_afterAlphaT_55_,
    "DetlaPhi_NextToLeadingJets_afterAlphaT_55",
    ";#Delta #phi(j_{2},j_{3}); Events/0.65 rad;",
    40, 0., TMath::Pi(),
    nMax_+1, 0, 1, true );


  BookHistArray( AlphaT_,
    "AlphaT",
    ";#alpha_{T};Events/0.025;",
    1000,0.,10.,
    nMax_+1, 0, 1, true );



  BookHistArray( AlphaT_Zero_Four_Vertices_,
    "AlphaT_0_4_vertices",
    ";#alpha_{T};Events/0.025;",
    1000,0.,10.,
    nMax_+1, 0, 1, true );

  BookHistArray( AlphaT_Five_Eight_Vertices_,
    "AlphaT_5_8_vertices",
    ";#alpha_{T};Events/0.025;",
    1000,0.,10.,
    nMax_+1, 0, 1, true );

  BookHistArray( AlphaT_Gr_Eight_Vertices_,
    "AlphaT_gr_8_vertices",
    ";#alpha_{T};Events/0.025;",
    1000,0.,10.,
    nMax_+1, 0, 1, true );

  BookHistArray( AlphaT_Zoomed_,
    "AlphaT_Zoomed",
    ";#alpha_{T}; Events/0.0025;",
    60,0.45,0.6,
    nMax_+1, 0, 1, true );


  BookHistArray( AlphaT_Zoomed_Zero_Four_Vertices_,
    "AlphaT_Zoomed_0_4_vertices",
    ";#alpha_{T}; Events/0.0025;",
    60,0.45,0.6,
    nMax_+1, 0, 1, true );

  BookHistArray( AlphaT_Zoomed_Five_Eight_Vertices_,
    "AlphaT_Zoomed_5_8_vertices",
    ";#alpha_{T}; Events/0.0025;",
    60,0.45,0.6,
    nMax_+1, 0, 1, true );

  BookHistArray( AlphaT_Zoomed_Gr_Eight_Vertices_,
    "AlphaT_Zoomed_gr_8_vertices",
    ";#alpha_{T}; Events/0.0025;",
    60,0.45,0.6,
    nMax_+1, 0, 1, true );

    BookHistArray( AlphatCut_Meff_55_,
    "EffectiveMass_after_alphaT_55",
    ";M_{eff} (GeV); Events/40 GeV;",
    3000, 0., 3000.,
    nMax_+1, 0, 1, true );

  BookHistArray( AlphatCut_Meff_53_,
    "EffectiveMass_after_alphaT_53",
    ";M_{eff} (GeV); Events/40 GeV;",
   3000, 0., 3000.,
    nMax_+1, 0, 1, true );

  BookHistArray( AlphatCut_Meff_52_,
    "EffectiveMass_after_alphaT_52",
    ";M_{eff} (GeV); Events/40 GeV;",
    3000, 0., 3000.,
    nMax_+1, 0, 1, true );

  BookHistArray( AlphatCut_HT_55_,
    "HT_after_alphaT_55",
    ";H_{T} (GeV); Events/25 (GeV);",
    2000,0.,2000.,
    nMax_+1, 0, 1, true );


  BookHistArray( AlphatCut_HT_53_,
    "HT_after_alphaT_53",
    ";H_{T} (GeV); Events/25 (GeV);",
    2000,0.,2000.,
    nMax_+1, 0, 1, true );

  BookHistArray( AlphatCut_HT_52_,
    "HT_after_alphaT_52",
    ";H_{T} (GeV); Events/25 (GeV);",
    2000,0.,2000.,
    nMax_+1, 0, 1, true );

  BookHistArray( HT_,
    "HT",
    ";H_{T} (GeV); Events/25 GeV;",
    2500,0.,2500.,
    nMax_+1, 0, 1, true );


  BookHistArray( HT_Zero_Four_Vertices_,
    "HT_0_4_vertices",
    ";H_{T} (GeV); Events/25 GeV;",
    2500,0.,2500.,
    nMax_+1, 0, 1, true );

  BookHistArray( HT_Five_Eight_Vertices_,
    "HT_5_8_vertices",
    ";H_{T} (GeV); Events/25 GeV;",
    2500,0.,2500.,
    nMax_+1, 0, 1, true );

  BookHistArray( HT_Gr_Eight_Vertices_,
    "HT_Gr_8_vertices",
    ";H_{T} (GeV); Events/25 GeV;",
    2500,0.,2500.,
    nMax_+1, 0, 1, true );

  BookHistArray( Meff_,
    "EffectiveMass",
    ";M_{eff} (GeV); Events/40 GeV;",
    2500, 0., 2500.,
    nMax_+1, 0, 1, true );

  BookHistArray( AlphatCut_BiasedDphi_afterAlphaT_55_,
    "BiasedDeltaPhi_after_alphaT_55",
    ";#Delta #phi^{*} (rad); Events/0.05 rad;",
    60, 0., TMath::Pi(),
    nMax_+1, 0, 1, true );

  BookHistArray( BiasedDphi_,
    "BiasedDeltaPhi",
    ";#Delta #phi^{*} (rad); Events/0.05 rad;",
    60, 0., TMath::Pi(),
    nMax_+1, 0, 1, true );

  BookHistArray( MHToverHT_,
    "MHToverHT",
    ";#slash{H}_{T}/H_{T};Events/0.025;",
    40,0.,1.,
    nMax_+1, 0, 1, true );

  BookHistArray( MHToverHT_afterAlphaT_55_,
    "MHToverHT_afterAlphaT_55",
    ";#slash{H}_{T}/H_{T};Events/0.025;",
    40,0.,1.,
    nMax_+1, 0, 1, true );

  BookHistArray( MHToverHT_afterAlphaT_53_,
    "MHToverHT_afterAlphaT_53",
    ";#slash{H}_{T}/H_{T};Events/0.025;",
    40,0.,1.,
    nMax_+1, 0, 1, true );

  BookHistArray( MHToverHT_afterAlphaT_52_,
    "MHToverHT_afterAlphaT_52",
    ";#slash{H}_{T}/H_{T};Events/0.025;",
    40,0.,1.,
    nMax_+1, 0, 1, true );


  BookHistArray( MHT_,
    "MHT",
    ";#slash{H}_{T} (GeV); Events/10 GeV;",
    600,0.,600.,
    nMax_+1, 0, 1, true );

  BookHistArray( MHTAfteraT_55_,
    "MHT after AlphaT 55",
    ";#slash{H}_{T} (GeV); Events/10 GeV;",
    600,0.,600.,
    nMax_+1, 0, 1, true );

  BookHistArray( MHTAfteraT_53_,
    "MHT after AlphaT 53",
    ";#slash{H}_{T} (GeV); Events/10 GeV;",
    600,0.,600.,
    nMax_+1, 0, 1, true );

  BookHistArray( MHTAfteraT_52_,
    "MHT after AlphaT 52",
    ";#slash{H}_{T} (GeV); Events/10 GeV;",
    600,0.,600.,
    nMax_+1, 0, 1, true );

  BookHistArray( MultiplicityAfteraT_55_,
    "JetMultiplicityAfterAlphaT_55",
    ";n",
    15,0.,15.,
    nMax_+1, 0, 1, true );

  BookHistArray( MultiplicityAfteraT_53_,
    "JetMultiplicityAfterAlphaT_53",
    ";n",
    15,0.,15.,
    nMax_+1, 0, 1, true );

  BookHistArray( MultiplicityAfteraT_52_,
    "JetMultiplicityAfterAlphaT_52",
    ";n",
    15,0.,15.,
    nMax_+1, 0, 1, true );

  BookHistArray( Multiplicity_,
    "JetMultiplicity",
    ";n",
    15,0.,15.,
    nMax_+1, 0, 1, true );

  BookHistArray( JetEta_,
    "JetEta",
    ";#eta ; Events/1 eta;",
    60,-5.,5.,
    nMax_+1, 0, 1, true );

  BookHistArray( Number_GenBJets_,
    "Number_GenBJets",
    ";Number ; Events;",
    6,0.,6.,
    nMax_+1, 0, 1, true );


  BookHistArray( GenJetEta_,
    "GenJetEta",
    ";#eta ; Events/1 eta;",
    60,-5.,5.,
    nMax_+1, 0, 1, true );

  BookHistArray( Matched_GenJetEta_,
    "Matched_GenJetEta",
    "#eta Events/1 eta;",
    60,-5.,5.,
    nMax_+1, 0, 1, true );

  BookHistArray( Matched_GenJetPt_vs_GenJetEta_,
    "Matched_GenJetPt_vs_GenJetEta",
    "#eta Events/1 eta; JetPt",
    1500,0.,1500.,
    60,-5.,5.,
    nMax_+1, 0, 1, true );

  BookHistArray( GenJetPt_vs_GenJetEta_,
    "GenJetPt_vs_GenJetEta",
    ";#eta Events/1 eta; JetPt;",
    1500,0.,1500.,
    60,-5.,5.,
    nMax_+1, 0, 1, true );

  BookHistArray( Duplicate_GenJetEta_,
    "Duplicate_GenJetEta",
    ";#eta ; Events;",
    60,-5.,5.,
    nMax_+1, 0, 1, true );

  BookHistArray( JetPt_,
    "JetPt",
    ";GeV ; Events",
    1500,0.,1500.,
    nMax_+1, 0, 1, true );


  BookHistArray( GenJetPt_,
    "GenJetPt",
    ";GeV ; Event ",
    1500,0.,1500.,
    nMax_+1, 0, 1, true );

  BookHistArray( Matched_GenJetPt_,
    "Matched_GenJetPt",
    ";GeV ; Events",
    1500,0.,1500.,
    nMax_+1, 0, 1, true );


  BookHistArray( Duplicate_GenJetPt_,
    "Duplicate_GenJetPt",
    ";GeV ; Events",
    1500,0.,1500.,
    nMax_+1, 0, 1, true );

  BookHistArray( JetEta_afterAlphaT_55_,
    "JetEta_afterAlphaT_55",
    ";#eta ; Events/1 eta;",
    60,-5.,5.,
    nMax_+1, 0, 1, true );

  BookHistArray( JetPt_afterAlphaT_55_,
    "JetPt_afterAlphaT_55",
    ";GeV ; Events/1 eta ",
    1500,0.,1500.,
    nMax_+1, 0, 1, true );

  BookHistArray( hLepPt_,
    "MuPt",
    ";P_{T} [GeV];",
    2000,10.,2010.,
    nMax_+1, 0, 1, true );

  BookHistArray( hLepPt_afterAlphaT_55_,
    "MuPt_afterAlphaT_55",
    ";P_{T} [GeV];",
    2000,10.,2010.,
    nMax_+1, 0, 1, true );

  BookHistArray( hLepPt_afterAlphaT_53_,
    "MuPt_afterAlphaT_53",
    ";P_{T} [GeV];",
    2000,10.,2010.,
    nMax_+1, 0, 1, true );

  BookHistArray( hLepPt_afterAlphaT_52_,
    "MuPt_afterAlphaT_52",
    ";P_{T} [GeV];",
    2000,10.,2010.,
    nMax_+1, 0, 1, true );

  BookHistArray( hLepTrIso_,
    "MuTrIso",
    ";Trk Iso;",
    2000,0.,2.,
    nMax_+1, 0, 1, true );


  BookHistArray( hLepEIso_,
    "MuEIso",
    ";E Iso;",
    2000,0.,2.,
    nMax_+1, 0, 1, true );


  BookHistArray( hLepHIso_,
    "MuHIso",
    ";H Iso;",
    2000,0.,2.,
    nMax_+1, 0, 1, true );

  BookHistArray( hLepCIso_,
    "MuCso",
    ";Combined_Iso;",
    2000,0.,2.,
    nMax_+1, 0, 1, true );

  BookHistArray( hLepTrIso_afterAlphaT_55_,
    "MuTrIso_afterAlphaT_55",
    ";Trk Iso;",
    2000,0.,2.,
    nMax_+1, 0, 1, true );


  BookHistArray( hLepEIso_afterAlphaT_55_,
    "MuEIso_afterAlphaT_55",
    ";E Iso;",
    2000,0.,2.,
    nMax_+1, 0, 1, true );


  BookHistArray( hLepHIso_afterAlphaT_55_,
    "MuHIso_afterAlphaT_55",
    ";H Iso;",
    2000,0.,2.,
    nMax_+1, 0, 1, true );

  BookHistArray( hLepCIso_afterAlphaT_55_,
    "MuCso_afterAlphaT_55",
    ";Combined_Iso;",
    2000,0.,2.,
    nMax_+1, 0, 1, true );

  BookHistArray( hMT_,
    "MT_",
    ";M){T} [GeV];",
    2000,0.,2000.,
    nMax_+1, 0, 1, true );

  BookHistArray( hMT_afterAlphaT_55_,
    "MT_after_alphaT_55",
    ";M){T} [GeV];",
    2000,0.,2000.,
    nMax_+1, 0, 1, true );

  BookHistArray( hMT_afterAlphaT_53_,
    "MT_after_alphaT_53",
    ";M){T} [GeV];",
    2000,0.,2000.,
    nMax_+1, 0, 1, true );

  BookHistArray( hMT_afterAlphaT_52_,
    "MT_after_alphaT_52",
    ";M){T} [GeV];",
    2000,0.,2000.,
    nMax_+1, 0, 1, true );

  BookHistArray( BtagPreAlphaT_4_,
    "Btag_Pre_AlphaT_4_",
    ";Number of Btags;",
    6,0.,6.,
    nMax_+1, 0, 1, true );

  BookHistArray( BtagAfterAlphaT_4_55_,
    "Btag_Post_AlphaT_4_55",
    ";Number of Btags;",
    6,0.,6.,
    nMax_+1, 0, 1, true );

  BookHistArray( BtagAfterAlphaT_4_53_,
    "Btag_Post_AlphaT_4_53",
    ";Number of Btags;",
    6,0.,6.,
    nMax_+1, 0, 1, true );

  BookHistArray( BtagAfterAlphaT_4_52_,
    "Btag_Post_AlphaT_4_52",
    ";Number of Btags;",
    6,0.,6.,
    nMax_+1, 0, 1, true );

  BookHistArray( BtagPreAlphaT_5_,
    "Btag_Pre_AlphaT_5_",
    ";Number of Btags;",
    6,0.,6.,
    nMax_+1, 0, 1, true );

  BookHistArray( BtagAfterAlphaT_5_55_,
    "Btag_Post_AlphaT_5_55",
    ";Number of Btags;",
    6,0.,6.,
    nMax_+1, 0, 1, true );


  BookHistArray( BtagAfterAlphaT_5_53_,
    "Btag_Post_AlphaT_5_53",
    ";Number of Btags;",
    6,0.,6.,
    nMax_+1, 0, 1, true );

  BookHistArray( BtagAfterAlphaT_5_52_,
    "Btag_Post_AlphaT_5_52",
    ";Number of Btags;",
    6,0.,6.,
    nMax_+1, 0, 1, true );
}
// -----------------------------------------------------------------------------
//

Double_t WeeklyUpdatePlots::MT2_Leading( Event::Data& ev ){
  mt2_bisect::mt2 mt2_event;
  std::vector<Event::Jet const *> jet = ev.JD_CommonJets().accepted;
  
  LorentzV lv1 = *jet[0];
  LorentzV lv2 = *jet[1];

  double pa[3]; // px py m of object 1
  double pb[3]; // px py m of object 2
  double pm[3];       //jet1
  pa[1] = lv1.Px();
  pa[2] = lv1.Py();
  pa[0] = 0.;//KS_MT(objects[0]);
            //jet2
  pb[1] = lv2.Px();
  pb[2] = lv2.Py();
  pb[0] = 0.;//KS_MT(objects[1]);

  pm[1]= ev.CommonMHT().Px();
  pm[2]= ev.CommonMHT().Py();

  // set invisable mass
  double mn = 0.;
  mt2_event.set_momenta(pa,pb,pm);
  mt2_event.set_mn(mn);

  return mt2_event.get_mt2();

}


Double_t WeeklyUpdatePlots::DeltaHT( Event::Data& ev){
  std::vector<Event::Jet const *> jet = ev.JD_CommonJets().accepted;
  UInt_t n = jet.size();

  LorentzV lv1(0.,0.,0.,0.);
  LorentzV lv2(0.,0.,0.,0.);

  // Alpha_t variable
  std::vector<bool> pseudo;
  AlphaT()( jet, pseudo, false );
  if ( pseudo.size() != jet.size() ) { abort(); }
    // use this to get the pseudo jets

  if ( n == 2 ) {
    if ( jet[0] ) lv1 = *jet[0];
    if ( jet[1] ) lv2 = *jet[1];
  } else if ( n > 2 ) {
    for ( unsigned int i = 0; i < jet.size(); ++i ) {
      if ( jet[i] ) {
        if ( pseudo[i] ) { lv1 += *jet[i];

        }
        else             { lv2 += *jet[i];

        }
      }
    }
    if ( lv2.Pt() > lv1.Pt() ) { LorentzV tmp = lv1; lv1 = lv2; lv2 = tmp; }

  }

  return lv1.Et()-lv2.Et();

}

std::pair<LorentzV,LorentzV> WeeklyUpdatePlots::PsudoJets( Event::Data & ev ){
  std::vector<Event::Jet const *> jet = ev.JD_CommonJets().accepted;
  UInt_t n = jet.size();
  LorentzV lv1(0.,0.,0.,0.);
  LorentzV lv2(0.,0.,0.,0.);

  // Alpha_t variable
  std::vector<bool> pseudo;
  AlphaT()( jet, pseudo, false );
  if ( pseudo.size() != jet.size() ) { abort(); }
    // use this to get the pseudo jets

  if ( n == 2 ) {
    if ( jet[0] ) lv1 = *jet[0];
    if ( jet[1] ) lv2 = *jet[1];
  } else if ( n > 2 ) {
    for ( unsigned int i = 0; i < jet.size(); ++i ) {
      if ( jet[i] ) {
        if ( pseudo[i] ) { lv1 += *jet[i];

        }
        else             { lv2 += *jet[i];

        }
      }
    }
    if ( lv2.Pt() > lv1.Pt() ) { LorentzV tmp = lv1; lv1 = lv2; lv2 = tmp; }

  }
  std::pair<LorentzV,LorentzV> a(lv1,lv2);
  return a;

}

Double_t WeeklyUpdatePlots::MT2( Event::Data& ev){

  std::vector<Event::Jet const *> jet = ev.JD_CommonJets().accepted;
  UInt_t n = jet.size();

  mt2_bisect::mt2 mt2_event;

  LorentzV lv1(0.,0.,0.,0.);
  LorentzV lv2(0.,0.,0.,0.);

  // Alpha_t variable
  std::vector<bool> pseudo;
  AlphaT()( jet, pseudo, false );
  if ( pseudo.size() != jet.size() ) { abort(); }
    // use this to get the pseudo jets

  if ( n == 2 ) {
    if ( jet[0] ) lv1 = *jet[0];
    if ( jet[1] ) lv2 = *jet[1];
  } else if ( n > 2 ) {
    for ( unsigned int i = 0; i < jet.size(); ++i ) {
      if ( jet[i] ) {
        if ( pseudo[i] ) { lv1 += *jet[i];

        }
        else             { lv2 += *jet[i];

        }
      }
    }
    if ( lv2.Pt() > lv1.Pt() ) { LorentzV tmp = lv1; lv1 = lv2; lv2 = tmp; }

  }

  double pa[3]; //m, px, py, of object 1
  double pb[3]; //m, px ,py, of object 2
  double pm[3];       //jet1
  pa[1] = lv1.Px();
  pa[2] = lv1.Py();
  pa[0] = 0.;//KS_MT(objects[0]);
            //jet2
  pb[1] = lv2.Px();
  pb[2] = lv2.Py();
  pb[0] = 0.;//KS_MT(objects[1]);

  pm[1]= ev.CommonMHT().Px();
  pm[2]= ev.CommonMHT().Py();

  // set invisable mass
  double mn = 0.;
  mt2_event.set_momenta(pa,pb,pm);
  mt2_event.set_mn(mn);
  // mt2_event.print();
  return mt2_event.get_mt2();
}


bool WeeklyUpdatePlots::StandardPlots( Event::Data& ev ) {

  std::vector <Event::Lepton const *> theLepton;
  GenMatrixBin gen(&ev);
  std::vector <Event::GenObject const *> matched_GenB;

  UInt_t nBtags_four = 0;
  UInt_t nBtags_five = 0;
  for(unsigned int i=0; i<ev.JD_CommonJets().accepted.size(); i++) {
  // std::cout << "we are on jet " << i << " the btag discriminator is " << ev.GetBTagResponse(ev.JD_CommonJets().accepted.at(i)->GetIndex(), 4) << std::endl;
  if(ev.GetBTagResponse(ev.JD_CommonJets().accepted.at(i)->GetIndex(), 5) > 0.679) {
  nBtags_five++;
         //if we make it into here, the jet has passed the b-tag requirement
   } 
  if(ev.GetBTagResponse(ev.JD_CommonJets().accepted.at(i)->GetIndex(), 4) > 2.0) {
  nBtags_four++;
         //if we make it into here, the jet has passed the b-tag requirement
   } 
   
  }


  bool isMu= false;
  bool isLep=false;
  bool isdoubleMu = false;

  if (ev.LD_CommonMuons().accepted.size() + ev.LD_CommonElectrons().accepted.size() != 0){
    isLep=true;}

  if(ev.LD_CommonMuons().accepted.size()>0&&ev.LD_CommonElectrons().accepted.size()==0)
    {
      theLepton = ev.LD_CommonMuons().accepted;
      isMu = true;
    }  

  if(ev.LD_CommonMuons().accepted.size()>1&&ev.LD_CommonElectrons().accepted.size()==0)
    {
      theLepton = ev.LD_CommonMuons().accepted;
      isdoubleMu = true;
   } 

  if(ev.LD_CommonMuons().accepted.size()==0&&ev.LD_CommonElectrons().accepted.size()>0)
    {
      theLepton = ev.LD_CommonElectrons().accepted;
    }  

  if(ev.LD_CommonMuons().accepted.size()>0&&ev.LD_CommonElectrons().accepted.size()>0)
    {
      cout << "WARNING: ttWPlottingOps has common muon AND Electron, it does not know what to plot!!!"<<endl;
       return true;
     }


  UInt_t n = ev.JD_CommonJets().accepted.size();

  Double_t weight = ev.GetEventWeight();

  int count_ = 0;
  double biasedDPhi = 100.;
  double biasedDPhi_baby = 100.;
  int counter_ = 0;
  int counterBaby_ = 0;
  int countBaby_ = 0;

  LorentzV loweredMHT = ev.CommonRecoilMET();
  for(std::vector<Event::Jet const*>::const_iterator iM = ev.JD_CommonJets().baby.begin();iM != ev.JD_CommonJets().baby.end();++iM){
    if( (*iM)->Pt() > 30.)
      loweredMHT -= (**iM);
  }



  for( std::vector<Event::Jet const *>::const_iterator i = ev.JD_CommonJets().accepted.begin();
  i != ev.JD_CommonJets().accepted.end();
  ++i ){
    double newBiasDPhi = fabs(ROOT::Math::VectorUtil::DeltaPhi(**i,loweredMHT + (**i))) ;
    if(newBiasDPhi < biasedDPhi){
      biasedDPhi = newBiasDPhi;
      count_ = counter_;
    }
    counter_++;
  }
  for( std::vector<Event::Jet const*>::const_iterator iI = ev.JD_CommonJets().baby.begin(); iI != ev.JD_CommonJets().baby.end();
  ++iI) {
    if((*iI)->Pt() > 30.){
      double newBiasDPhi_2 = fabs( ROOT::Math::VectorUtil::DeltaPhi(**iI, loweredMHT + (**iI) ) );
      if(newBiasDPhi_2 < biasedDPhi_baby){
        biasedDPhi_baby = newBiasDPhi_2;
        countBaby_ = counterBaby_;
      }
    }
    counterBaby_++;
  }

  


  if ( n >= nMin_ && n <= nMax_ && n < BtagPreAlphaT_4_.size()) {
    BtagPreAlphaT_4_[0]->Fill( nBtags_four, weight );
    BtagPreAlphaT_5_[0]->Fill( nBtags_five, weight );
    BtagPreAlphaT_4_[n]->Fill( nBtags_four, weight );
    BtagPreAlphaT_5_[n]->Fill( nBtags_five, weight );
    }




  int nVertex = 0;
  //Make the vertex sum PT for later plots
  double  VertexPt = 0.;
  for(std::vector<floatle>::const_iterator vtx =
    ev.vertexSumPt()->begin();
  vtx != ev.vertexSumPt()->end();++vtx){
    if(!ev.vertexIsFake()->at( vtx-ev.vertexSumPt()->begin()) && fabs((ev.vertexPosition()->at( vtx-ev.vertexSumPt()->begin())).Z()) < 24.0 && ev.vertexNdof()->at( vtx-ev.vertexSumPt()->begin() ) > 4&& (ev.vertexPosition()->at( vtx-ev.vertexSumPt()->begin())).Rho() < 2.0 ){  VertexPt += *vtx;}
  }


  for(std::vector<float>::const_iterator vtx =
    ev.vertexSumPt()->begin();
  vtx != ev.vertexSumPt()->end();++vtx){
    if(!ev.vertexIsFake()->at( vtx-ev.vertexSumPt()->begin()) &&
      fabs((ev.vertexPosition()->at( vtx-ev.vertexSumPt()->begin())).Z()) < 24.0 &&
      ev.vertexNdof()->at( vtx-ev.vertexSumPt()->begin() ) > 4 &&
      (ev.vertexPosition()->at( vtx-ev.vertexSumPt()->begin())).Rho() < 2.0 ){  nVertex++; }
  }

  if ( StandardPlots_ ){

    std::pair<LorentzV,LorentzV> PsudoJets = WeeklyUpdatePlots::PsudoJets( ev );

    

    if ( nVertex < 5){
    if ( n >= nMin_ && n <= nMax_ && n < HT_Zero_Four_Vertices_.size() ) {
      HT_Zero_Four_Vertices_[0]->Fill( ev.CommonHT(), weight );
      HT_Zero_Four_Vertices_[n]->Fill( ev.CommonHT(), weight );
    }
    }


    if ( nVertex >= 5 && nVertex <= 8){
    if ( n >= nMin_ && n <= nMax_ && n < HT_Five_Eight_Vertices_.size() ) {
      HT_Five_Eight_Vertices_[0]->Fill( ev.CommonHT(), weight );
      HT_Five_Eight_Vertices_[n]->Fill( ev.CommonHT(), weight );
    }
    }


    if ( nVertex > 8){
    if ( n >= nMin_ && n <= nMax_ && n < HT_Gr_Eight_Vertices_.size() ) {
      HT_Gr_Eight_Vertices_[0]->Fill( ev.CommonHT(), weight );
      HT_Gr_Eight_Vertices_[n]->Fill( ev.CommonHT(), weight );
    }
    }


    if (nVertex < 5 ){
    if ( n >= nMin_ && n <= nMax_ && n < AlphaT_Zoomed_Zero_Four_Vertices_.size()  ) {
      AlphaT_Zoomed_Zero_Four_Vertices_[0]->Fill( ev.HadronicAlphaT(), weight );
      AlphaT_Zoomed_Zero_Four_Vertices_[n]->Fill( ev.HadronicAlphaT(), weight );
    }
    }


    if (nVertex >= 5 && nVertex <= 8 ){
    if ( n >= nMin_ && n <= nMax_ && n < AlphaT_Zoomed_Five_Eight_Vertices_.size()  ) {
      AlphaT_Zoomed_Five_Eight_Vertices_[0]->Fill( ev.HadronicAlphaT(), weight );
      AlphaT_Zoomed_Five_Eight_Vertices_[n]->Fill( ev.HadronicAlphaT(), weight );
    }
    }

    if (nVertex > 8 ){
    if ( n >= nMin_ && n <= nMax_ && n < AlphaT_Zoomed_Gr_Eight_Vertices_.size()  ) {
      AlphaT_Zoomed_Gr_Eight_Vertices_[0]->Fill( ev.HadronicAlphaT(), weight );
      AlphaT_Zoomed_Gr_Eight_Vertices_[n]->Fill( ev.HadronicAlphaT(), weight );
    }
    }

    if ( nVertex < 5){
    if ( n >= nMin_ && n <= nMax_ && n < AlphaT_Zero_Four_Vertices_.size()  ) {
      AlphaT_Zero_Four_Vertices_[0]->Fill( ev.HadronicAlphaT(), weight );
      AlphaT_Zero_Four_Vertices_[n]->Fill( ev.HadronicAlphaT(), weight );
    }
    }

    if ( nVertex >= 5 && nVertex <= 8){
    if ( n >= nMin_ && n <= nMax_ && n < AlphaT_Five_Eight_Vertices_.size()  ) {
      AlphaT_Five_Eight_Vertices_[0]->Fill( ev.HadronicAlphaT(), weight );
      AlphaT_Five_Eight_Vertices_[n]->Fill( ev.HadronicAlphaT(), weight );
    }
    }

    if ( nVertex > 8){
    if ( n >= nMin_ && n <= nMax_ && n < AlphaT_Gr_Eight_Vertices_.size()  ) {
      AlphaT_Gr_Eight_Vertices_[0]->Fill( ev.HadronicAlphaT(), weight );
      AlphaT_Gr_Eight_Vertices_[n]->Fill( ev.HadronicAlphaT(), weight );
    }
    }


    if ( n >= nMin_ && n <= nMax_ && n < vertexPtovHT_.size()) {
      vertexPtovHT_[0]->Fill(VertexPt/ev.CommonHT(),weight);
      vertexPtovHT_[n]->Fill(VertexPt/ev.CommonHT(),weight);
    }

    if ( n >= nMin_ && n <= nMax_ && n < MHTovMET_.size() ) {
        MHTovMET_[0]->Fill(  ev.CommonMHT().Pt()/LorentzV(*ev.metP4caloTypeII()).Pt(), weight );
        MHTovMET_[n]->Fill(  ev.CommonMHT().Pt()/LorentzV(*ev.metP4caloTypeII()).Pt(), weight );
      }



    if ( n >= nMin_ && n <= nMax_ && n < NumberVerticies_.size()) {
      NumberVerticies_[0]->Fill(nVertex,weight);
      NumberVerticies_[n]->Fill(nVertex,weight);
    }



    


    if ( n >= nMin_ && n <= nMax_ && n < DPhi_MHT_MHTBaby_.size()) {
      DPhi_MHT_MHTBaby_[0]->Fill(cos(ROOT::Math::VectorUtil::DeltaPhi(ev.CommonMHT(),ev.JD_CommonJets().babyHT)),weight);
      DPhi_MHT_MHTBaby_[n]->Fill(cos(ROOT::Math::VectorUtil::DeltaPhi(ev.CommonMHT(),ev.JD_CommonJets().babyHT)),weight);

    }

    if ( n >= nMin_ && n <= nMax_ && n < DPhi_MET_MHTBaby_.size()) {
      DPhi_MET_MHTBaby_[0]->Fill(fabs(ROOT::Math::VectorUtil::DeltaPhi(ev.PFMET(),ev.JD_CommonJets().babyHT)),weight);
      DPhi_MET_MHTBaby_[n]->Fill(fabs(ROOT::Math::VectorUtil::DeltaPhi(ev.PFMET(),ev.JD_CommonJets().babyHT)),weight);

    }

    if ( n >= nMin_ && n <= nMax_ && n < DPhi_MET_MHT_.size()) {
      DPhi_MET_MHT_[0]->Fill(fabs(ROOT::Math::VectorUtil::DeltaPhi(ev.PFMET(),ev.CommonMHT())),weight);
      DPhi_MET_MHT_[n]->Fill(fabs(ROOT::Math::VectorUtil::DeltaPhi(ev.PFMET(),ev.CommonMHT())),weight);

    }


    if ( n >= nMin_ && n <= nMax_ && n < Multiplicity_.size()) {
      Multiplicity_[0]->Fill( n, weight );
      Multiplicity_[n]->Fill( n, weight );
    }

    if ( n >= nMin_ && n <= nMax_ && n < MHT_.size()) {
      MHT_[0]->Fill( ev.CommonMHT().Pt(), weight );
      MHT_[n]->Fill( ev.CommonMHT().Pt(), weight );
    }

    if ( n >= nMin_ && n <= nMax_ && n < HT_.size() ) {
      HT_[0]->Fill( ev.CommonHT(), weight );
      HT_[n]->Fill( ev.CommonHT(), weight );
    }



    if(ev.HadronicAlphaT() >= 0.53 && ev.HadronicAlphaT() <= 0.55){
      AlphatCut_HT_53_[0]->Fill( ev.CommonHT(), weight );
    }


    if ( n >= nMin_ && n <= nMax_ && n < MHToverHT_.size() ) {
      MHToverHT_[0]->Fill( ev.CommonMHT().Pt()/ev.CommonHT(), weight );
      MHToverHT_[n]->Fill( ev.CommonMHT().Pt()/ev.CommonHT(), weight );
    }

    if ( n >= nMin_ && n <= nMax_ && n < Meff_.size()) {
      Meff_[0]->Fill( ev.CommonMHT().Pt()+ev.CommonHT(), weight );
      Meff_[n]->Fill( ev.CommonMHT().Pt()+ev.CommonHT(), weight );
    }


    if ( n >= nMin_ && n <= nMax_ && n < AlphaT_Zoomed_.size()  ) {
      AlphaT_Zoomed_[0]->Fill( ev.HadronicAlphaT(), weight );
      AlphaT_Zoomed_[n]->Fill( ev.HadronicAlphaT(), weight );
    }


    if ( n >= nMin_ && n <= nMax_ && n < AlphaT_.size()  ) {
      AlphaT_[0]->Fill( ev.HadronicAlphaT(), weight );
      AlphaT_[n]->Fill( ev.HadronicAlphaT(), weight );
    }

    

    if( biasedDPhi > biasedDPhi_baby){
      if ( n >= nMin_ && n <= nMax_ && n < BiasedDphi_.size()) {
      BiasedDphi_[0]->Fill(biasedDPhi_baby,weight);
      BiasedDphi_[n]->Fill(biasedDPhi_baby,weight);
      }
    }

    if( biasedDPhi <  biasedDPhi_baby){
      if ( n >= nMin_ && n <= nMax_ && n < BiasedDphi_.size()) {
      BiasedDphi_[0]->Fill(biasedDPhi,weight);
      BiasedDphi_[n]->Fill(biasedDPhi,weight);
      }
    }

    if( n >= nMin_ && n <= nMax_ && n < DetlaPhi_LeadingJets_.size() ){
      DetlaPhi_LeadingJets_[1]->Fill( fabs( ROOT::Math::VectorUtil::DeltaPhi(*ev.JD_CommonJets().accepted[0],*ev.JD_CommonJets().accepted[1])),weight);
      if(n <2){
        DetlaPhi_NextToLeadingJets_[2]->Fill(fabs(ROOT::Math::VectorUtil::DeltaPhi(*ev.JD_CommonJets().accepted[1],*ev.JD_CommonJets().accepted[2])),weight);

      }
    }


    for(unsigned int i = 0; i < ev.JD_CommonJets().accepted.size() && i < 3; i++){
      JetPt_[0]->Fill(ev.JD_CommonJets().accepted[i]->Pt(),weight);
      JetEta_[0]->Fill(ev.JD_CommonJets().accepted[i]->Eta(),weight);
      JetPt_[i+1]->Fill(ev.JD_CommonJets().accepted[i]->Pt(),weight);
      JetEta_[i+1]->Fill(ev.JD_CommonJets().accepted[i]->Eta(),weight);
    }
      
   if (ev.pthat.enabled()){

      if( n >= nMin_ && n <= nMax_ && n < Number_GenBJets_.size() ){
         Number_GenBJets_[0]->Fill(gen.the_GenB.size(),weight);
         Number_GenBJets_[n]->Fill(gen.the_GenB.size(),weight);
      }
      std::set<unsigned> matched;
      //cout << "New event" << endl;
      for(unsigned int i = 0; i < gen.the_GenB.size(); i++){

        float minDeltaR = 2*TMath::Pi();
        int index_keeper = -1;
        for(unsigned int j = 0; j < ev.JD_CommonJets().accepted.size(); j++){
          float aminDeltaR = fabs(ROOT::Math::VectorUtil::DeltaR (*(ev.JD_CommonJets().accepted.at(j)),*(gen.the_GenB.at(i))));
          if(aminDeltaR<minDeltaR) {
            minDeltaR=aminDeltaR;
            index_keeper = j;
              }
            }
        if(index_keeper != -1 && minDeltaR < 0.3){
          //cout << "Reco Jet  " << index_keeper << "Matched to Gen BJet " << i << endl;   
          GenJetPt_[0]->Fill(gen.the_GenB.at(i)->Pt(),weight);
          GenJetEta_[0]->Fill(gen.the_GenB.at(i)->Eta(),weight);
          GenJetPt_[i+1]->Fill(gen.the_GenB.at(i)->Pt(),weight);
          GenJetEta_[i+1]->Fill(gen.the_GenB.at(i)->Eta(),weight);
          GenJetPt_vs_GenJetEta_[0]->Fill(gen.the_GenB.at(i)->Pt(),gen.the_GenB.at(i)->Eta(),weight);
          GenJetPt_vs_GenJetEta_[i+1]->Fill(gen.the_GenB.at(i)->Pt(),gen.the_GenB.at(i)->Eta(),weight);

          if( ev.GetBTagResponse(ev.JD_CommonJets().accepted.at(index_keeper)->GetIndex(), 5) > 0.679){
            
            if ( i != 0 && matched.count(index_keeper)){ 
              //cout << "Duplicate RecoJet matched to GenJet" << endl;
              //cout << index_keeper << endl;
              Duplicate_GenJetPt_[0]->Fill(gen.the_GenB.at(i)->Pt(),weight);
              Duplicate_GenJetEta_[0]->Fill(gen.the_GenB.at(i)->Eta(),weight);
                }
            //cout << "Reco Jet " << index_keeper << "Has been Btagged" << endl; 
            matched.insert(index_keeper);
            matched_GenB.push_back(gen.the_GenB.at(i));
              }
             }
            }
      for(unsigned int i =0; i < matched_GenB.size(); i++){
         Matched_GenJetPt_[0]->Fill(matched_GenB.at(i)->Pt(),weight);
         Matched_GenJetEta_[0]->Fill(matched_GenB.at(i)->Eta(),weight);
         Matched_GenJetPt_[i+1]->Fill(matched_GenB.at(i)->Pt(),weight);
         Matched_GenJetEta_[i+1]->Fill(matched_GenB.at(i)->Eta(),weight);
         Matched_GenJetPt_vs_GenJetEta_[0]->Fill(gen.the_GenB.at(i)->Pt(),gen.the_GenB.at(i)->Eta(),weight);
         Matched_GenJetPt_vs_GenJetEta_[i+1]->Fill(gen.the_GenB.at(i)->Pt(),gen.the_GenB.at(i)->Eta(),weight);
        }
        }

    if (isLep){

     Double_t aMT =  sqrt(2.0 * ev.PFMET().Pt() * (theLepton.at(0))->Pt() * (1.0 - cos(ROOT::Math::VectorUtil::DeltaPhi(*(theLepton.at(0)), ev.PFMET() ) )));
     hLepPt_[0]->Fill(theLepton.at(0)->Pt(),weight);

     if ( n >= nMin_ && n <= nMax_ && n < hMT_.size()){
     hMT_[0]->Fill(aMT,weight);
     hMT_[n]->Fill(aMT,weight);
     }

     if(ev.HadronicAlphaT() > 0.53 && ev.HadronicAlphaT() <= 0.55){
     if ( n >= nMin_ && n <= nMax_ && n < hMT_afterAlphaT_53_.size()){
     hMT_afterAlphaT_53_[0]->Fill(aMT,weight);
     hMT_afterAlphaT_53_[n]->Fill(aMT,weight);
     }
     }

     if(ev.HadronicAlphaT() > 0.52 && ev.HadronicAlphaT() <= 0.53){
     if ( n >= nMin_ && n <= nMax_ && n < hMT_afterAlphaT_52_.size()){
     hMT_afterAlphaT_52_[0]->Fill(aMT,weight);
     hMT_afterAlphaT_52_[n]->Fill(aMT,weight);
     }

     }
     
     if(ev.HadronicAlphaT() > 0.55){
     if ( n >= nMin_ && n <= nMax_ && n < hMT_afterAlphaT_55_.size()){
     hMT_afterAlphaT_55_[0]->Fill(aMT,weight);
     hMT_afterAlphaT_55_[n]->Fill(aMT,weight);
     }
     }
 
     if ( n >= nMin_ && n <= nMax_ && n < hLepTrIso_.size()){
     hLepTrIso_[0]->Fill(((theLepton.at(0))->GetTrkIsolation())/((theLepton.at(0))->Pt()),weight);
     hLepTrIso_[n]->Fill(((theLepton.at(0))->GetTrkIsolation())/((theLepton.at(0))->Pt()),weight);
     }

     if(ev.HadronicAlphaT() > 0.55){
     if ( n >= nMin_ && n <= nMax_ && n < hLepTrIso_afterAlphaT_55_.size()){
     hLepTrIso_afterAlphaT_55_[0]->Fill(((theLepton.at(0))->GetTrkIsolation())/((theLepton.at(0))->Pt()),weight);
     hLepTrIso_afterAlphaT_55_[n]->Fill(((theLepton.at(0))->GetTrkIsolation())/((theLepton.at(0))->Pt()),weight);
     }
     }

     if ( n >= nMin_ && n <= nMax_ && n < hLepEIso_.size()){
     hLepEIso_[0]->Fill(((theLepton.at(0))->GetEcalIsolation())/((theLepton.at(0))->Et()),weight);
     hLepEIso_[n]->Fill(((theLepton.at(0))->GetEcalIsolation())/((theLepton.at(0))->Et()),weight);
     }

     if(ev.HadronicAlphaT() > 0.55){
     if ( n >= nMin_ && n <= nMax_ && n < hLepEIso_afterAlphaT_55_.size()){
     hLepEIso_afterAlphaT_55_[0]->Fill(((theLepton.at(0))->GetEcalIsolation())/((theLepton.at(0))->Et()),weight);
     hLepEIso_afterAlphaT_55_[n]->Fill(((theLepton.at(0))->GetEcalIsolation())/((theLepton.at(0))->Et()),weight);
     }
     }

     if ( n >= nMin_ && n <= nMax_ && n < hLepHIso_.size()){
     hLepHIso_[0]->Fill(((theLepton.at(0))->GetHcalIsolation())/((theLepton.at(0))->Et()),weight);
     hLepHIso_[n]->Fill(((theLepton.at(0))->GetHcalIsolation())/((theLepton.at(0))->Et()),weight);
     }

     if(ev.HadronicAlphaT() > 0.55){
     if ( n >= nMin_ && n <= nMax_ && n < hLepHIso_afterAlphaT_55_.size()){
     hLepHIso_afterAlphaT_55_[0]->Fill(((theLepton.at(0))->GetHcalIsolation())/((theLepton.at(0))->Et()),weight);
     hLepHIso_afterAlphaT_55_[n]->Fill(((theLepton.at(0))->GetHcalIsolation())/((theLepton.at(0))->Et()),weight);
     }
     }
  
     if ( n >= nMin_ && n <= nMax_ && n < hLepCIso_.size()){
     hLepCIso_[0]->Fill((theLepton.at(0))->GetCombIsolation(),weight);
     hLepCIso_[n]->Fill((theLepton.at(0))->GetCombIsolation(),weight);
     }

     if(ev.HadronicAlphaT() > 0.55){
     if ( n >= nMin_ && n <= nMax_ && n < hLepCIso_afterAlphaT_55_.size()){
     hLepCIso_afterAlphaT_55_[0]->Fill((theLepton.at(0))->GetCombIsolation(),weight);
     hLepCIso_afterAlphaT_55_[n]->Fill((theLepton.at(0))->GetCombIsolation(),weight);
     }
     }
     
    }
      

    if(ev.HadronicAlphaT() > 0.53 && ev.HadronicAlphaT() <= 0.55){

      UInt_t nBtags_AT_four_53 = 0;
      UInt_t nBtags_AT_five_53 = 0;
      for(unsigned int i=0; i<ev.JD_CommonJets().accepted.size(); i++) {
      // std::cout << "we are on jet " << i << " the btag discriminator is " << ev.GetBTagResponse(ev.JD_CommonJets().accepted.at(i)->GetIndex(), 4) << std::endl;
      if(ev.GetBTagResponse(ev.JD_CommonJets().accepted.at(i)->GetIndex(), 5) > 0.679) {
      nBtags_AT_five_53++;
            //if we make it into here, the jet has passed the b-tag requirement
      } 
      if(ev.GetBTagResponse(ev.JD_CommonJets().accepted.at(i)->GetIndex(), 4) > 2.0) {
      nBtags_AT_four_53++;
             //if we make it into here, the jet has passed the b-tag requirement
      } 
   
      }

      if ( n >= nMin_ && n <= nMax_ && n < BtagAfterAlphaT_4_53_.size()) {
      BtagAfterAlphaT_4_53_[0]->Fill( nBtags_AT_four_53, weight );
      BtagAfterAlphaT_5_53_[0]->Fill( nBtags_AT_five_53, weight );
      BtagAfterAlphaT_4_53_[n]->Fill( nBtags_AT_four_53, weight );
      BtagAfterAlphaT_5_53_[n]->Fill( nBtags_AT_five_53, weight );
      }

      if ( n >= nMin_ && n <= nMax_ && n < MHToverHT_afterAlphaT_53_.size() ) {
      MHToverHT_afterAlphaT_53_[0]->Fill( ev.CommonMHT().Pt()/ev.CommonHT(), weight );
      MHToverHT_afterAlphaT_53_[n]->Fill( ev.CommonMHT().Pt()/ev.CommonHT(), weight );
      }

      if ( n >= nMin_ && n <= nMax_ && n < vertexPtovHT_afterAlphaT_53_.size()) {
      vertexPtovHT_afterAlphaT_53_[0]->Fill(VertexPt/ev.CommonHT(),weight);
      vertexPtovHT_afterAlphaT_53_[n]->Fill(VertexPt/ev.CommonHT(),weight);
      }

      if ( n >= nMin_ && n <= nMax_ && n < MHTAfteraT_53_.size()) {
        MHTAfteraT_53_[0]->Fill( ev.CommonMHT().Pt(), weight );
        MHTAfteraT_53_[n]->Fill( ev.CommonMHT().Pt(), weight );
      }

      if ( n >= nMin_ && n <= nMax_ && n < AlphatCut_Meff_53_.size()) {
        AlphatCut_Meff_53_[0]->Fill( ev.CommonMHT().Pt()+ev.CommonHT(), weight );
        AlphatCut_Meff_53_[n]->Fill( ev.CommonMHT().Pt()+ev.CommonHT(), weight );
      }

      if ( n >= nMin_ && n <= nMax_ && n < AlphatCut_HT_53_.size() ) {
        AlphatCut_HT_53_[n]->Fill( ev.CommonHT(), weight );
      }

      if ( n >= nMin_ && n <= nMax_ && n < MultiplicityAfteraT_53_.size()) {
        MultiplicityAfteraT_53_[0]->Fill( n, weight );
        MultiplicityAfteraT_53_[n]->Fill( n, weight );
      }

      if ( n >= nMin_ && n <= nMax_ && n < NumberVerticiesAfterAlphaT_53_.size()) {
        NumberVerticiesAfterAlphaT_53_[0]->Fill(nVertex,weight);
        NumberVerticiesAfterAlphaT_53_[n]->Fill(nVertex,weight);
      }

      if ( n >= nMin_ && n <= nMax_ && n < MHTovMET_afterAlphaT_53_.size() ) {
        MHTovMET_afterAlphaT_53_[0]->Fill(  ev.CommonMHT().Pt()/LorentzV(*ev.metP4caloTypeII()).Pt(), weight );
        MHTovMET_afterAlphaT_53_[n]->Fill(  ev.CommonMHT().Pt()/LorentzV(*ev.metP4caloTypeII()).Pt(), weight );
      }
    }

    if(ev.HadronicAlphaT() > 0.52 &&  ev.HadronicAlphaT() <= 0.53){


      UInt_t nBtags_AT_four_52 = 0;
      UInt_t nBtags_AT_five_52 = 0;
      for(unsigned int i=0; i<ev.JD_CommonJets().accepted.size(); i++) {
      // std::cout << "we are on jet " << i << " the btag discriminator is " << ev.GetBTagResponse(ev.JD_CommonJets().accepted.at(i)->GetIndex(), 4) << std::endl;
      if(ev.GetBTagResponse(ev.JD_CommonJets().accepted.at(i)->GetIndex(), 5) > 0.679) {
      nBtags_AT_five_52++;
            //if we make it into here, the jet has passed the b-tag requirement
      } 
      if(ev.GetBTagResponse(ev.JD_CommonJets().accepted.at(i)->GetIndex(), 4) > 2.0) {
      nBtags_AT_four_52++;
             //if we make it into here, the jet has passed the b-tag requirement
      } 
   
      }

      if ( n >= nMin_ && n <= nMax_ && n < MHToverHT_afterAlphaT_52_.size() ) {
      MHToverHT_afterAlphaT_52_[0]->Fill( ev.CommonMHT().Pt()/ev.CommonHT(), weight );
      MHToverHT_afterAlphaT_52_[n]->Fill( ev.CommonMHT().Pt()/ev.CommonHT(), weight );
      }

      if ( n >= nMin_ && n <= nMax_ && n < vertexPtovHT_afterAlphaT_52_.size()) {
      vertexPtovHT_afterAlphaT_52_[0]->Fill(VertexPt/ev.CommonHT(),weight);
      vertexPtovHT_afterAlphaT_52_[n]->Fill(VertexPt/ev.CommonHT(),weight);
      }

      if ( n >= nMin_ && n <= nMax_ && n < BtagAfterAlphaT_4_52_.size()) {
      BtagAfterAlphaT_4_52_[0]->Fill( nBtags_AT_four_52, weight );
      BtagAfterAlphaT_5_52_[0]->Fill( nBtags_AT_five_52, weight );
      BtagAfterAlphaT_4_52_[n]->Fill( nBtags_AT_four_52, weight );
      BtagAfterAlphaT_5_52_[n]->Fill( nBtags_AT_five_52, weight );
      }

      if ( n >= nMin_ && n <= nMax_ && n < MHT_.size()) {
        MHTAfteraT_52_[0]->Fill( ev.CommonMHT().Pt(), weight );
        MHTAfteraT_52_[n]->Fill( ev.CommonMHT().Pt(), weight );
    }

      if ( n >= nMin_ && n <= nMax_ && n < AlphatCut_Meff_52_.size()) {
        AlphatCut_Meff_52_[0]->Fill( ev.CommonMHT().Pt()+ev.CommonHT(), weight );
        AlphatCut_Meff_52_[n]->Fill( ev.CommonMHT().Pt()+ev.CommonHT(), weight );
      }

      if ( n >= nMin_ && n <= nMax_ && n < AlphatCut_HT_52_.size() ) {
        AlphatCut_HT_52_[0]->Fill( ev.CommonHT(), weight );
        AlphatCut_HT_52_[n]->Fill( ev.CommonHT(), weight );
      }

      if ( n >= nMin_ && n <= nMax_ && n < MultiplicityAfteraT_52_.size()) {
        MultiplicityAfteraT_52_[0]->Fill( n, weight );
        MultiplicityAfteraT_52_[n]->Fill( n, weight );
      }

      if ( n >= nMin_ && n <= nMax_ && n < NumberVerticiesAfterAlphaT_52_.size()) {
        NumberVerticiesAfterAlphaT_52_[0]->Fill(nVertex,weight);
        NumberVerticiesAfterAlphaT_52_[n]->Fill(nVertex,weight);
      }

      if ( n >= nMin_ && n <= nMax_ && n < MHTovMET_afterAlphaT_52_.size() ) {
        MHTovMET_afterAlphaT_52_[0]->Fill(  ev.CommonMHT().Pt()/LorentzV(*ev.metP4caloTypeII()).Pt(), weight );
        MHTovMET_afterAlphaT_52_[n]->Fill(  ev.CommonMHT().Pt()/LorentzV(*ev.metP4caloTypeII()).Pt(), weight );
      }

    }

    if(ev.HadronicAlphaT() > 0.55){


      UInt_t nBtags_AT_four_55 = 0;
      UInt_t nBtags_AT_five_55 = 0;
      for(unsigned int i=0; i<ev.JD_CommonJets().accepted.size(); i++) {
      // std::cout << "we are on jet " << i << " the btag discriminator is " << ev.GetBTagResponse(ev.JD_CommonJets().accepted.at(i)->GetIndex(), 4) << std::endl;
      if(ev.GetBTagResponse(ev.JD_CommonJets().accepted.at(i)->GetIndex(), 5) > 0.679) {
      nBtags_AT_five_55++;
            //if we make it into here, the jet has passed the b-tag requirement
      } 
      if(ev.GetBTagResponse(ev.JD_CommonJets().accepted.at(i)->GetIndex(), 4) > 2.0) {
      nBtags_AT_four_55++;
             //if we make it into here, the jet has passed the b-tag requirement
      } 
   
      }


      if( n >= nMin_ && n <= nMax_ && n < DetlaPhi_LeadingJets_afterAlphaT_55_.size() ){
      DetlaPhi_LeadingJets_afterAlphaT_55_[1]->Fill( fabs( ROOT::Math::VectorUtil::DeltaPhi(*ev.JD_CommonJets().accepted[0],*ev.JD_CommonJets().accepted[1])),weight);
      if(n <2){
        DetlaPhi_NextToLeadingJets_afterAlphaT_55_[2]->Fill(fabs(ROOT::Math::VectorUtil::DeltaPhi(*ev.JD_CommonJets().accepted[1],*ev.JD_CommonJets().accepted[2])),weight);

      }
    }


      if ( n >= nMin_ && n <= nMax_ && n < MHToverHT_afterAlphaT_55_.size() ) {
      MHToverHT_afterAlphaT_55_[0]->Fill( ev.CommonMHT().Pt()/ev.CommonHT(), weight );
      MHToverHT_afterAlphaT_55_[n]->Fill( ev.CommonMHT().Pt()/ev.CommonHT(), weight );
      }

      if ( n >= nMin_ && n <= nMax_ && n < BtagAfterAlphaT_4_55_.size()) {
        BtagAfterAlphaT_4_55_[0]->Fill( nBtags_AT_four_55, weight );
        BtagAfterAlphaT_5_55_[0]->Fill( nBtags_AT_five_55, weight );
        BtagAfterAlphaT_4_55_[n]->Fill( nBtags_AT_four_55, weight );
        BtagAfterAlphaT_5_55_[n]->Fill( nBtags_AT_five_55, weight );
        }

      if ( n >= nMin_ && n <= nMax_ && n < vertexPtovHT_afterAlphaT_55_.size()) {
      vertexPtovHT_afterAlphaT_55_[0]->Fill(VertexPt/ev.CommonHT(),weight);
      vertexPtovHT_afterAlphaT_55_[n]->Fill(VertexPt/ev.CommonHT(),weight);
      }
      
      if ( n >= nMin_ && n <= nMax_ && n < NumberVerticiesAfterAlphaT_55_.size()) {
        NumberVerticiesAfterAlphaT_55_[0]->Fill(nVertex,weight);
        NumberVerticiesAfterAlphaT_55_[n]->Fill(nVertex,weight);
      }

      if ( n >= nMin_ && n <= nMax_ && n < MultiplicityAfteraT_55_.size()) {
        MultiplicityAfteraT_55_[0]->Fill( n, weight );
        MultiplicityAfteraT_55_[n]->Fill( n, weight );
      }

     for(unsigned int i = 0; i < ev.JD_CommonJets().accepted.size(); i++){
      JetPt_afterAlphaT_55_[0]->Fill(ev.JD_CommonJets().accepted[i]->Pt(),weight);
      JetEta_afterAlphaT_55_[0]->Fill(ev.JD_CommonJets().accepted[i]->Eta(),weight);
      JetPt_afterAlphaT_55_[i+1]->Fill(ev.JD_CommonJets().accepted[i]->Pt(),weight);
      JetEta_afterAlphaT_55_[i+1]->Fill(ev.JD_CommonJets().accepted[i]->Eta(),weight);
     }



             
      if ( n >= nMin_ && n <= nMax_ && n < MissedHT_.size() ) {
        MissedHT_[0]->Fill(  ev.CommonRecoilMET().Pt()/(ev.CommonRecoilMET()+ev.JD_CommonJets().babyHT).Pt(), weight );
        MissedHT_[n]->Fill( ev.CommonRecoilMET().Pt()/(ev.CommonRecoilMET()+ev.JD_CommonJets().babyHT).Pt(), weight );
      }


      if ( n >= nMin_ && n <= nMax_ && n < AlphatCut_HT_55_.size() ) {
        AlphatCut_HT_55_[0]->Fill( ev.CommonHT(), weight );
        AlphatCut_HT_55_[n]->Fill( ev.CommonHT(), weight );
      }

      if ( n >= nMin_ && n <= nMax_ && n < AlphatCut_Meff_55_.size()) {
        AlphatCut_Meff_55_[0]->Fill( ev.CommonMHT().Pt()+ev.CommonHT(), weight );
        AlphatCut_Meff_55_[n]->Fill( ev.CommonMHT().Pt()+ev.CommonHT(), weight );
      }

    if( biasedDPhi < biasedDPhi_baby){
      if ( n >= nMin_ && n <= nMax_ && n < AlphatCut_BiasedDphi_afterAlphaT_55_.size()) {
      AlphatCut_BiasedDphi_afterAlphaT_55_[0]->Fill(biasedDPhi,weight);
      AlphatCut_BiasedDphi_afterAlphaT_55_[n]->Fill(biasedDPhi,weight);
      }
    }

    if( biasedDPhi > biasedDPhi_baby){
      if ( n >= nMin_ && n <= nMax_ && n < AlphatCut_BiasedDphi_afterAlphaT_55_.size()) {
      AlphatCut_BiasedDphi_afterAlphaT_55_[0]->Fill(biasedDPhi_baby,weight);
      AlphatCut_BiasedDphi_afterAlphaT_55_[n]->Fill(biasedDPhi_baby,weight);
      }
    }

    if ( n >= nMin_ && n <= nMax_ && n < MHTovMET_afterAlphaT_55_.size() ) {
        MHTovMET_afterAlphaT_55_[0]->Fill(  ev.CommonMHT().Pt()/LorentzV(*ev.metP4caloTypeII()).Pt(), weight );
        MHTovMET_afterAlphaT_55_[n]->Fill(  ev.CommonMHT().Pt()/LorentzV(*ev.metP4caloTypeII()).Pt(), weight );
      }

    }

  
  
  
  
  }







  return true;

}
