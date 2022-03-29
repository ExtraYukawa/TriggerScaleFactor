#include "FakeRate_Utils.h"

float MC_eff_lumi(float pt,const char *channel ){
    float lumi;
    if (strcmp(channel,"Electron") == 0 || strcmp(channel , "Muon") == 0){
        if(strcmp(channel,"Electron") == 0){
            if(pt < 35){
                lumi = 35.371;
            }
            else{
                lumi = 37.993;
            }
            return lumi;
        }
        else{
            if(pt<30){
                lumi=2.454;
            }
            else{
                lumi=69.746;
            }
            return lumi;
        }
    }
    
    else{
       throw std::invalid_argument( "received non-existed channel" ); 
    }
    
}

