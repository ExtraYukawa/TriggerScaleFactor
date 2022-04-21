#include "Lepton_Info.h"

lzp4 LeptonP4(bool ttc_flag,bool OPS_flag,float ttc_lep_pt,float ttc_lep_eta,float ttc_lep_phi,float ttc_lep_m,float OPS_lep_pt,float OPS_lep_eta,float OPS_lep_phi,float OPS_lep_m){
    lzp4 lep_p4;
    if(ttc_flag && !OPS_flag){
        lep_p4.SetPtEtaPhiM(ttc_lep_pt,ttc_lep_eta,ttc_lep_phi,ttc_lep_m);
        return lep_p4;
    
    }
    else if(!ttc_flag && OPS_flag){
        lep_p4.SetPtEtaPhiM(OPS_lep_pt,OPS_lep_eta,OPS_lep_phi,OPS_lep_m);
        return lep_p4;
    }
    else{    
        throw std::invalid_argument("Region Definition Contraction!");
    }
}
