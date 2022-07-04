#include "ScaleFactor.h"


float IDScaleFact(const char *channel="", TH2D*h1=NULL,TH2D*h2=NULL,float l1pt=0,float l2pt=0, float l1eta=0, float l2eta=0){
    
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

float Muon_IDSF(TH2D *h, float pt, float eta){

    if( pt > 120)
        pt = 119;       
    if(eta < 0)
        eta = -eta;
    return h->GetBinContent(h->FindBin(eta,pt));

}

float Electron_IDSF(TH2D *h, float pt, float eta){

    if( pt > 500)
        pt = 499;       
    if(eta < 0)
        eta = -eta;
    return h->GetBinContent(h->FindBin(pt,eta));

}

float RECO_Muon_SF(TH2F *h, float pt, float eta){

    if(pt>40) pt=39;
    return h->GetBinContent(h->FindBin(TMath::Abs(eta),pt));

}
float Trigger_sf_l1l2pt(TH2D *h, float value1, float value2){

    if (value1 >200)
        value1 =199;
    if (value2 >200)
        value2 =199;
    
    if(value1 > value2){
        return h->GetBinContent(h->FindBin(value1,value2));
    }

    else{
        return h->GetBinContent(h->FindBin(value2,value1));
    }


}

float Trigger_sf_l1l2eta(TH2D *h, float value1, float value2){
    return h->GetBinContent(h->FindBin(TMath::Abs(value1),TMath::Abs(value2)));
}

float Trigger_sf_pteta(TH2D *h, float value1, float value2){
    
    if (value1 >200)
        value1 =199;

    return h->GetBinContent(h->FindBin(value1,TMath::Abs(value2)));
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


float chargeflip_sf(TH2F*h,int kinematic_region,bool same_sign, float sigma){

    
    int index = kinematic_region+1;
    float sf = 1.0;
    float sign;
    
    if(!same_sign){
        sign = -1;
    }
    else{
        sign = 1 ;
    }

    float r_SF = h->GetBinContent(index);
    float r_sigma = h->GetBinError(index);
    sf = r_SF + sign*sigma * r_sigma;
    if(sf < 0.) return 0.;
    return sf;
}



