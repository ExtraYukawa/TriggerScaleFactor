


def TrigSF( activate : bool, Type: int ):
    
    if activate:
        if Type==1:
            return 'Trigger_sf_pteta(h_TrigSF,l1pt,l1eta)'
        elif Type ==2:
            return 'Trigger_sf_pteta(h_TrigSF,l2pt,l2eta)'
        elif Type ==3:
            return 'Trigger_sf_l1l2pt(h_TrigSF,l1pt,l2pt)'
        elif Type ==4:
            return 'Trigger_sf_l1l2eta(h_TrigSF,l1eta,l2eta)'
        elif Type == 0:
            return '1.'
        else:
            raise ValueError(f'No such Trigger Scale Factors Type: {Type}!')
    else:
        return '1.'

def DiLeptons_IDSF( activate : bool , channel: str):

    if activate:
        if channel =='DoubleElectron':
            return 'Electron_IDSF(h_IDSF,l1pt,l1eta) * Electron_IDSF(h_IDSF,l2pt,l2eta)'
        elif channel =='DoubleMuon':
            return 'Muon_IDSF(h_IDSF,l1pt,l1eta) * Muon_IDSF(h_IDSF,l2pt,l2eta)'
        elif channel =='ElectronMuon':
            return 'Muon_IDSF(h1_IDSF,l1pt,l1eta) * Electron_IDSF(h2_IDSF,l2pt,l2eta)'

        else:
            raise ValueError(f'No such channel: {channel}')
    else:
        return '1.'




def DiLeptons_RECOSF(activate:bool , channel:str):
    
    if activate:

        if channel == 'DoubleElectron':
            return 'Electron_RECO_SF[l1_id]*Electron_RECO_SF[l2_id]'
        elif channel =='DoubleMuon':
            return 'RECO_Muon_SF(h_RECOSF,l1pt,l1eta) * RECO_Muon_SF(h_RECOSF,l2pt,l2eta)'
        elif channel =='ElectronMuon':
            return 'RECO_Muon_SF(h_RECOSF,l1pt,l1eta)*Electron_RECO_SF[l2_id]'
        else:
            raise ValueError(f'No such channel: {channel}')

    else:
        return '1.'
        



def PreFireWeight(activate:bool, year:str):

    if activate:
        if year =='2017' or year =='2016apv' or year =='2016postapv':
            return 'PrefireWeight'
        elif year =='2018':
            return '1.'
        else:
            raise ValueError(f'No such year: {year}')
    else:
        return '1.'


def ChargeFlipSF(activate:bool,channel:str,Same_Sign:bool,sigma:float):

    if activate:
        if channel=='DoubleElectron':
            if Same_Sign == None:
                raise ValueError('You should Specify the charges condition of two leptons.')
            elif Same_Sign:
                return f'chargeflip_sf(h_SS,K_region,true,{sigma})'
            elif not Same_Sign:
                return f'chargeflip_sf(h_OS,K_region,false,{sigma})'
        else:
            return '1'
    else:
        return '1.'
