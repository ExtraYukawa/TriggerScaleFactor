
def TrigSF( activate : bool, Type: int ,IsFake = False):
    
    if not IsFake:
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
    else:
        return '1.'

def DiLeptons_IDSF( activate : bool , channel: str,IsFake=False):

    if not IsFake:
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
    else:
        return '1.'




def DiLeptons_RECOSF(activate:bool , channel:str,IsFake=False):
    
    if not IsFake:
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


def ChargeFlipSF(activate:bool,channel:str,Same_Sign:bool,sigma:float,IsFake=False):

    if not IsFake:
        if activate:
            if channel=='DoubleElectron':
                if Same_Sign:
                    return f'chargeflip_sf(h_SS,K_region,0,Gen_IsOS,{sigma})'
                elif not Same_Sign:
                    return f'chargeflip_sf(h_OS,K_region,1,Gen_IsOS,{sigma})'
                else:    
                    raise ValueError('You should Specify the charges condition of two leptons.')
            else:
                return '1.'
        else:
            return '1.'
    else:
        return '1.'

def FakeRate(activate:bool, IsData:bool,IsFake:bool,phys_region:str,channel:str)->str:
    
    if activate:
        if channel == 'ElectronMuon':
            l1pt = 'muon_conePt[l1_id]'
            l2pt = 'electron_conePt[l2_id]'
        elif channel == 'DoubleElectron':
            l1pt = 'electron_conePt[l1_id]'
            l2pt = 'electron_conePt[l2_id]'
        else:
            l1pt = 'muon_conePt[l1_id]'
            l2pt = 'muon_conePt[l2_id]'

        if IsFake:
            if IsData:
                return f'fr_weight(h_fr_1,h_fr_2,{phys_region}_1P1F,{phys_region}_0P2F,{phys_region}_lep1_faketag,{l1pt},l1eta,{l2pt},l2eta,true)'
            else:
                return f'fr_weight(h_fr_1,h_fr_2,{phys_region}_1P1F,{phys_region}_0P2F,{phys_region}_lep1_faketag,{l1pt},l1eta,{l2pt},l2eta,false)'
        else:
            return '1.'
    else:
        return '1.'


def CTagSF(activate:bool)->str:
    if activate:
        return f'CtagSF(h_flavc,h_flavb,h_flavl,n_tight_jet,tightJets_id_in24,Jet_puId, Jet_pt_nom, Jet_hadronFlavour,Jet_btagDeepFlavCvL,Jet_btagDeepFlavCvB)'
    else:
        return '1.'


def gen_isOS(activate:bool,channel:str)->str:
    if activate and channel =='DoubleElectron':
    
        return "gen_isOS(l1pt, l1eta, l1phi, l1_pdgid, l2pt, l2eta, l2phi, l2_pdgid, nGenDressedLepton, GenDressedLepton_pt, GenDressedLepton_eta, GenDressedLepton_phi, GenDressedLepton_pdgId)"    
        
    else:
        return '-1'








