#include "IDScaleFactor.h"


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







