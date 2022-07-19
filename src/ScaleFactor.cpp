#include "ScaleFactor.h"


double IDScaleFact(const char *channel="", TH2D*h1=NULL,TH2D*h2=NULL,float l1pt=0,float l2pt=0, float l1eta=0, float l2eta=0){
    
    if(strcmp(channel,"DoubleElectron") ==0 ||strcmp(channel,"DoubleMuon")==0 ){
        return Lepton_IDSF(h1,l1pt,l1eta)*Lepton_IDSF(h1,l2pt,l2eta);
    }  
    else if (strcmp(channel,"ElectronMuon") ==0){
        return Lepton_IDSF(h1,l1pt,l1eta)*Lepton_IDSF(h2,l2pt,l2eta);
    }
    else{
       throw std::invalid_argument( "received negative value" ); 
    }
    return -1;

}

double Muon_IDSF(TH2D *h, float pt, float eta){

    if( pt > 120)
        pt = 119;       
    if(eta < 0)
        eta = -eta;
    return h->GetBinContent(h->FindBin(static_cast<double>(eta),static_cast<double>(pt)));

}

double Electron_IDSF(TH2D *h, float pt, float eta){

    if( pt > 500)
        pt = 499;       
    if(eta < 0)
        eta = -eta;
    return h->GetBinContent(h->FindBin(pt,eta));

}

double RECO_Muon_SF(TH2F *h, float pt, float eta){

    if(pt>40) pt=39;
    return static_cast<double>(h->GetBinContent(h->FindBin(TMath::Abs(eta),pt)));

}
double Trigger_sf_l1l2pt(TH2D *h, float value1, float value2){

    if (value1 >200)
        value1 =199;
    if (value2 >200)
        value2 =199;
    
    if(value1 > value2){
        return h->GetBinContent(h->FindBin(static_cast<double>(value1),static_cast<double>(value2)));
    }

    else{
        return h->GetBinContent(h->FindBin(static_cast<double>(value2),static_cast<double>(value1)));
    }


}

double Trigger_sf_l1l2eta(TH2D *h, float value1, float value2){
    return h->GetBinContent(h->FindBin(TMath::Abs(value1),TMath::Abs(value2)));
}

double Trigger_sf_pteta(TH2D *h, float value1, float value2){
    
    if (value1 >200)
        value1 =199;

    return h->GetBinContent(h->FindBin(static_cast<double>(value1),static_cast<double>(TMath::Abs(value2))));
}

int kinematic(bool activate , float l1_pt, float l2_pt, float l1_eta, float l2_eta){
    
    if (activate){
        std::vector<Float_t> pt_region  = {20., 40., 60., 100., 100000000000.};
        std::vector<Float_t> eta_region = {0.,  0.8, 1.479, 2.5};
        int pt_bins  = pt_region.size() - 1;
        int eta_bins = eta_region.size() - 1;
        int l1_pt_index = -1;
        int l2_pt_index = -1;
        int l1_eta_index = -1;
        int l2_eta_index = -1;
        for(int i = 0; i < pt_bins; i++){
            if(pt_region[i] <= l1_pt && l1_pt < pt_region[i+1]) l1_pt_index = i;
            if(pt_region[i] <= l2_pt && l2_pt < pt_region[i+1]) l2_pt_index = i;
        }
        for(int i = 0; i < eta_bins; i++){
            if(eta_region[i] <= fabs(l1_eta) && fabs(l1_eta) < eta_region[i+1]) l1_eta_index = i;
            if(eta_region[i] <= fabs(l2_eta) && fabs(l2_eta) < eta_region[i+1]) l2_eta_index = i;
        }
        if(l1_pt_index <0 || l2_pt_index <0 || l1_eta_index <0 || l2_eta_index<0) return -1;
        return l2_eta_index + eta_bins*(l2_pt_index) + eta_bins*pt_bins*(l1_eta_index) + eta_bins*pt_bins*eta_bins*(l1_pt_index);
    }
    else{
        return -1;
    }
}


double chargeflip_sf(TH2D*h,int kinematic_region,int reco_isOS,int gen_isOS, float sigma){

    int index = kinematic_region+1;
    float sf = 1.0;
    
    if((reco_isOS == 0 ) && (gen_isOS ==1)){
        float SS_SF = h->GetBinContent(h->FindBin(index));
        float SS_sigma = h->GetBinError(h->FindBin(index));
        sf = SS_SF + sigma*SS_sigma;
    }
    
    
    if(sf < 0.) sf=0.;
    return static_cast<double>(sf);
}

double fr_weight(TH2D* h_fr_l1, TH2D * h_fr_l2, bool Flag_1P1F, bool Flag_0P2F, bool l1_faketag, float l1_pt , float l1_eta, float l2_pt, float l2_eta, bool IsData){
    float w_temp = 1.0;
    float fakerate1 = 1.0;
    float fakerate2 = 1.0;
    int BinX = 0;
    int BinY = 0;
    

    if(Flag_1P1F){
        if(l1_faketag){
            BinX = h_fr_l1->GetXaxis()->FindBin(TMath::Abs(l1_eta));
            BinY = h_fr_l1->GetYaxis()->FindBin(l1_pt);
            if(BinX > h_fr_l1->GetNbinsX()) BinX = h_fr_l1->GetNbinsX();
            if(BinY > h_fr_l1->GetNbinsY()) BinY = h_fr_l1->GetNbinsY();
            fakerate1 = h_fr_l1->GetBinContent(BinX,BinY);
        
        }
        else{
            BinX = h_fr_l2->GetXaxis()->FindBin(TMath::Abs(l2_eta));
            BinY = h_fr_l2->GetYaxis()->FindBin(l2_pt);
            if(BinX > h_fr_l2->GetNbinsX()) BinX = h_fr_l2->GetNbinsX();
            if(BinY > h_fr_l2->GetNbinsY()) BinY = h_fr_l2->GetNbinsY();
            fakerate1 = h_fr_l2->GetBinContent(BinX,BinY);
        } 
        if(IsData) {
            w_temp = fakerate1/(1-fakerate1);
        }
        else{
        
            w_temp = -1 *fakerate1/(1-fakerate1);
        
        }
    }
    if(Flag_0P2F){
    
        BinX = h_fr_l1->GetXaxis()->FindBin(TMath::Abs(l1_eta));
        BinY = h_fr_l1->GetYaxis()->FindBin(l1_pt);
        if(BinX > h_fr_l1->GetNbinsX()) BinX = h_fr_l1->GetNbinsX();
        if(BinY > h_fr_l1->GetNbinsY()) BinY = h_fr_l1->GetNbinsY();
        fakerate1 = h_fr_l1->GetBinContent(BinX,BinY);
    
    
        BinX = h_fr_l2->GetXaxis()->FindBin(TMath::Abs(l2_eta));
        BinY = h_fr_l2->GetYaxis()->FindBin(l2_pt);
        if(BinX > h_fr_l2->GetNbinsX()) BinX = h_fr_l2->GetNbinsX();
        if(BinY > h_fr_l2->GetNbinsY()) BinY = h_fr_l2->GetNbinsY();
        fakerate2 = h_fr_l2->GetBinContent(BinX,BinY);
    
        if(IsData) {
            w_temp = -1.0*fakerate1*fakerate2/((1-fakerate1)*(1-fakerate2));
        }
        else{
            w_temp=fakerate1*fakerate2/((1-fakerate1)*(1-fakerate2));
        }
    }
    return static_cast<double>(w_temp);
}

double CtagSF(TH2D *h_flavc,TH2D *h_flavb,TH2D *h_flavl,int n_tight_jet , ROOT::VecOps::RVec<Int_t> tightJets_id_in24,ROOT::VecOps::RVec<Int_t> JetpuId,ROOT::VecOps::RVec<Float_t> Jet_pt, ROOT::VecOps::RVec<Int_t> Jet_hadflav, ROOT::VecOps::RVec<Float_t> CvsL, ROOT::VecOps::RVec<Float_t> CvsB){
    float sf = 1.0;
    for(int i = 0 ; i < n_tight_jet; i++){
        int index = tightJets_id_in24[i];

        if(JetpuId[index] == 0 && Jet_pt[index] < 50) continue;
        if(Jet_hadflav[index] ==4){
            sf *= h_flavc->GetBinContent(h_flavc->FindBin(CvsL[index],CvsB[index]));
        }
        else if(Jet_hadflav[index] ==5){
            sf *= h_flavb->GetBinContent(h_flavb->FindBin(CvsL[index],CvsB[index]));
        }
        else{
            sf *= h_flavl->GetBinContent(h_flavl->FindBin(CvsL[index],CvsB[index]));
        }
        return sf;
    }
    return sf;
}


int gen_isOS(float l1_pt, float l1_eta, float l1_phi, int l1_pdgid, float l2_pt, float l2_eta, float l2_phi, int l2_pdgid, int ngenlepton, ROOT::VecOps::RVec<Float_t> gen_pt, ROOT::VecOps::RVec<Float_t> gen_eta, ROOT::VecOps::RVec<Float_t> gen_phi, ROOT::VecOps::RVec<Int_t> gen_pdgid){

    int isOS = -1;
    float deltaR_lep1 = 99.;
    float deltaR_lep2 = 99.;
    int genlep1_idx =-1;
    int genlep2_idx = -1;
    
    for(int i = 0 ; i < ngenlepton ; i++){
        if(!(fabs(l1_pdgid) == fabs(gen_pdgid[i]))) continue;
        float deltaR_tmp = deltaR(l1_eta,l1_phi,gen_eta[i],gen_phi[i]);
        if(deltaR_tmp > 0.3) continue;
        if(deltaR_tmp < deltaR_lep1){

            deltaR_lep1 = deltaR_tmp;
            genlep1_idx = i ;
        }
    
    }
    for(int i = 0 ; i < ngenlepton ; i++){
        if(!(fabs(l2_pdgid) == fabs(gen_pdgid[i]))) continue;
        float deltaR_tmp = deltaR(l2_eta,l2_phi,gen_eta[i],gen_phi[i]);
        if(deltaR_tmp > 0.3) continue;
        if(deltaR_tmp < deltaR_lep2){
            deltaR_lep2 = deltaR_tmp;
            genlep2_idx = i ;
        }
    
    }

    if((genlep1_idx == -1) || (genlep2_idx == -1) || (genlep1_idx==genlep2_idx)) return isOS;

    if ((gen_pdgid[genlep1_idx]*gen_pdgid[genlep2_idx])<0) isOS = 1;
    else isOS = 0;
    return isOS;


}




