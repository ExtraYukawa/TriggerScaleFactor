import ROOT,os
import numpy as np

import sys
import os 
CURRENT_WORKDIR = os.getcwd()
sys.path.append(CURRENT_WORKDIR)

import Utils.CMSTDRStyle as CMSTDRStyle
import Utils.CMSstyle as CMSstyle
import Utils.plot_settings as plt_set
import os,sys 
import json
import fnmatch 
CURRENT_WORKDIR = os.getcwd()
sys.path.append(CURRENT_WORKDIR)
from Utils.General_Tool import get_NumberOfEvent


def Hist2D_to_Binx_Equal(h_original:ROOT.TH2D)->ROOT.TH2D:


    nx = h_original.GetXaxis().GetNbins()
    ny = h_original.GetYaxis().GetNbins()
    xmax = h_original.GetXaxis().GetXmax()
    ymax = h_original.GetYaxis().GetXmax()
    xmin = h_original.GetXaxis().GetXmin()
    ymin = h_original.GetYaxis().GetXmin()
    xtitle = h_original.GetXaxis().GetTitle()
    ytitle = h_original.GetYaxis().GetTitle()
    
    h_new = ROOT.TH2D("new_h","",nx,xmin,xmax,ny,ymin,ymax)

    h_new.GetXaxis().SetTitle(xtitle)
    h_new.GetYaxis().SetTitle(ytitle)
    
    
    for i in range(1,nx+1):
        for j in range(1,ny+1):
            BinContent= h_original.GetBinContent(i,j)
            BinError = h_original.GetBinError(i,j)
            h_new.SetBinContent(i,j,BinContent)
            h_new.SetBinError(i,j,BinError)
    h_new.GetXaxis().SetLabelOffset(999)
    h_new.GetYaxis().SetLabelOffset(999)

#    h_new.Draw('COLZ TEXT E')


    label = ROOT.TText()
    label.SetTextFont(42)
    label.SetTextSize(0.04)
    label.SetTextAlign(22)
    ylabel = h_new.GetYaxis().GetBinLowEdge(1) - 0.15*h_new.GetYaxis().GetBinWidth(1)
    xlabel = h_new.GetXaxis().GetBinLowEdge(1) - 0.25*h_new.GetXaxis().GetBinWidth(1)
    h_new.SetEntries(h_original.GetEntries())

    h_new.Draw('COLZ TEXT E')
    for i in range(nx+1):
        xlow = h_original.GetXaxis().GetBinUpEdge(i)
        xnew = h_new.GetXaxis().GetBinLowEdge(i+1)
        label.DrawText(xnew,ylabel,f"{int(xlow)}")
    for i in range(ny+1):
        ylow = h_original.GetYaxis().GetBinUpEdge(i)
        ynew = h_new.GetYaxis().GetBinLowEdge(i+1)
        label.DrawText(xlabel,ynew,f"{ylow:.1f}")

    #mypalette.colorPalette()
    return h_new

def Plot(func,**user_settings):
    def decorator(tag):
        return func(tag=tag,**user_settings)
    return decorator


def plot_eff1d(tag:str,**settings):
    
    FileIn = {
            'Data':ROOT.TFile.Open(os.path.join(settings['DirIn'],'EfficiencyForData.root'),"READ"),
                'MC':ROOT.TFile.Open(os.path.join(settings['DirIn'],'EfficiencyForMC.root'),"READ"),
            }
    
    TS = CMSTDRStyle.setTDRStyle()
    TS.cd()
    c = ROOT.TCanvas()
    c.cd()
    pad = ROOT.TPad()
    pad.Draw()
    leg = ROOT.TLegend(0.5,0.2,0.65,0.2+0.05*2)
    
    for Type in ['MC','Data']:
        name, Histogram = create_hist(FileIn[Type],tag)
        Histogram.SetLineColor(settings['colors'][Type])
        Histogram.SetMarkerStyle(20)
        Histogram.SetMarkerSize(0.5)
        Histogram.SetMarkerColor(settings['colors'][Type])
        gr = Histogram.CreateGraph()
        gr.SetMinimum(0.5)
        gr.SetMaximum(1.0)
        if Type =='MC':
            gr.Draw("AP")
        else:
            gr.Draw("samep")
        leg.AddEntry(Histogram,Type)
    CMSstyle.SetStyle(pad,year=settings['year'])
    leg.SetFillStyle(0)
    leg.Draw('SAME') 
    c.Update()
    c.SaveAs(os.path.join(settings['DirOut'],'Efficiency_1D_'+tag+'.png'))
    c.Close()
    pad.Close()
    del c
    del TS
    del pad
    del leg

def create_hist(infile:ROOT.TFile,tag:str):
    '''
    A lazy function to get histogram in root file.
    '''
    histoname = 'Eff_'+tag
    print(histoname)
    histotemp = infile.Get(histoname)
    histotemp.SetNameTitle(tag,"")
    
    return histoname ,histotemp

def plot_eff2d(tag:str,**settings):
    FileIn = {
            'Data':ROOT.TFile.Open(os.path.join(settings['DirIn'],'EfficiencyForData.root'),"READ"),
                'MC':ROOT.TFile.Open(os.path.join(settings['DirIn'],'EfficiencyForMC.root'),"READ")
            }
    for Type in ['MC','Data']: 
        TS = CMSTDRStyle.setTDRStyle()
        TS.cd()
        
        c = ROOT.TCanvas()
        c.cd() 
        
        pad = ROOT.TPad()
        pad.Draw()
        pad.cd()
        
        hist2D = FileIn[Type].Get(tag)
        hist2D = Hist2D_to_Binx_Equal(hist2D)

        
        CMSstyle.SetStyle(pad,year=settings['year'])
        pad.SetRightMargin(0.15)
        c.SetGridx(False)
        c.SetGridy(False)
        c.Update()
        c.SaveAs(os.path.join(settings['DirOut'],'Efficiency_2D_'+Type+'_'+tag+'.png'))
        pad.Close()
        c.Close()
        del c 
        del TS
        del pad
        del hist2D
        FileIn[Type].Close()

import numpy as np

    
def ScaleFactors(nominal_name:str,**settings):

    '''
    Calculate ScaleFactor for a single certain nominal variable.
    '''
    
    FileIn = dict()
    FileIn['Data'] = ROOT.TFile.Open(os.path.join(settings['DirIn'],"EfficiencyForData.root"),"READ")
    FileIn['MC'] = ROOT.TFile.Open(os.path.join(settings['DirIn'],"EfficiencyForMC.root"),"READ")
    
    data_types = ['MC','Data']

    args = {
            'FileIn':FileIn,
            'nominal_name':nominal_name
            }
    
    etabin = plt_set.abs_etabin
    ptbin = plt_set.ptbin
    
    SF_Central = Get_SF_Central(File=FileIn,nominal_name=nominal_name)
    SF_Corr_SystUncertainty = Get_SystematicUncertainty('Correlation Type',nominal_name)(Correlation_Err_Calc,**args)
    SF_Diff_SystUncertainty = Get_SystematicUncertainty('Criteria Difference Type',nominal_name)(CriteriaDiff_Err_Calc,**args)

    SF_SystematicUncertainty = np.sqrt((SF_Corr_SystUncertainty * SF_Central)**2+ (SF_Diff_SystUncertainty* SF_Central)**2)
    
    
    SF_hist = ROOT.TH2D(nominal_name,nominal_name,len(ptbin)-1,ptbin,len(etabin)-1,etabin)
    SF_hist.SetStats(0) 
    #SF_hist.SetTitle('')
    if 'l1' in args['nominal_name']:
        SF_hist.GetXaxis().SetTitle('Leading Lepton P_{T}[GeV]')
        SF_hist.GetYaxis().SetTitle('Leading Lepton |#eta|')
    else:
        SF_hist.GetXaxis().SetTitle('Subleading Lepton P_{T}[GeV]')
        SF_hist.GetYaxis().SetTitle('Subleading Lepton |#eta|')
    for i in range(SF_hist.GetNbinsX()):
        for j in range(SF_hist.GetNbinsY()):
            SF_hist.SetBinContent(i+1,j+1,SF_Central[i][j])
            SF_hist.SetBinError(i+1,j+1,SF_SystematicUncertainty[i][j])

    
    f = ROOT.TFile.Open(os.path.join(settings['DirIn'],'SF'+'_'+nominal_name+'.root'),'RECREATE')
    f.cd()
    
    SF_hist.Write()
    
    f.Close()
    
    TS = CMSTDRStyle.setTDRStyle()
    TS.cd()
    
    c = ROOT.TCanvas()
        
    pad = ROOT.TPad()
    pad.Draw()
    pad.cd()
    
    SF_hist = Hist2D_to_Binx_Equal(SF_hist)
    #mypalette.colorPalette()
    #SF_hist.Draw('COLZ TEXT E')
    
    CMSstyle.SetStyle(pad,year=settings['year'])
    pad.SetRightMargin(0.15)
    
    c.SetGridx(False)
    c.SetGridy(False)
    c.Update()
    c.SaveAs(os.path.join(settings['DirOut'],'SF'+'_'+nominal_name+'.png'))
    
    pad.Close()
    c.Close()
    del c 
    del TS
    del pad
    del SF_hist

def Get_SystematicUncertainty(Uncertainty_type:str,nominal_name:str):
    def SF_syst_type(func,**args) ->float:
        print('Calculating Systematic Uncertainty: {} for {}'.format(Uncertainty_type,nominal_name))
        return func(**args)
    return SF_syst_type

def Get_SF_Central(File:dict(),nominal_name:str) -> np.ndarray:
    eff_hist2D = dict()
    
    for Type in ['Data','MC']:
        eff_hist2D[Type] = File[Type].Get(nominal_name)

    eff_hist2D['Data'].Divide(eff_hist2D['MC'])
    
    SF_hist2D = eff_hist2D['Data']
    
    SF_Central = np.zeros(shape=(SF_hist2D.GetNbinsX(),SF_hist2D.GetNbinsY()),dtype=np.float32)
    for i in range(SF_hist2D.GetNbinsX()):
        for j in range(SF_hist2D.GetNbinsY()):
            SF_Central[i][j] = SF_hist2D.GetBinContent(i+1,j+1)
    return SF_Central


def Correlation_Err_Calc(**args) -> np.ndarray:
    
    hist2D =  args['FileIn']['Data'].Get(args['nominal_name'])
    
    mettrigger = ROOT.TEfficiency()
    leptrigger = ROOT.TEfficiency()
    lepmettrigger = ROOT.TEfficiency()

    mettrigger = args['FileIn']['Data'].Get('Eff_HLT_MET')
    leptrigger = args['FileIn']['Data'].Get('Eff_HLT_LEP')
    lepmettrigger = args['FileIn']['Data'].Get('Eff_HLT_LEPMET')
    
    alpha = mettrigger.GetEfficiency(1)*leptrigger.GetEfficiency(1)/lepmettrigger.GetEfficiency(1)

    err_array = np.zeros(shape=(hist2D.GetNbinsX(),hist2D.GetNbinsY()),dtype=np.float32)
    for i in range(hist2D.GetNbinsX()):
        for j in range(hist2D.GetNbinsY()):
            err_array[i][j] = 1 -alpha
    return err_array

def CriteriaDiff_Err_Calc(**args) -> np.ndarray:
    
    tags = ['jet','pv']
    eff_hist2D = dict()
    eff_hist2D['Data'] = dict()
    eff_hist2D['MC'] = dict()

    
    for Type in ['Data','MC']:
        eff_hist2D[Type]=dict()
        for tag in ['jet','pv']:
        
            eff_hist2D[Type]['nominal'] = ROOT.TH2D()
            eff_hist2D[Type]['nominal'] =args['FileIn'][Type].Get(args['nominal_name'])
            eff_hist2D[Type][tag] = dict()
            for criteria in ['low','high']:
                eff_hist2D[Type][tag][criteria] = ROOT.TH2D()
                eff_hist2D[Type][tag][criteria] = args['FileIn'][Type].Get(args['nominal_name']+'_'+criteria+tag)
    
      
    SF_hist2D = dict()
    
    SF_hist2D['nominal'] = ROOT.TH2D()
    eff_hist2D['Data']['nominal'].Divide(eff_hist2D['MC']['nominal'])
    SF_hist2D['nominal'] = eff_hist2D['Data']['nominal']
    SF_hist2D['jet'] = dict()
    SF_hist2D['pv'] = dict()

    for tag in ['jet','pv']:
        for criteria in ['low','high']:
            SF_hist2D[tag][criteria] = ROOT.TH2D()
            eff_hist2D['Data'][tag][criteria].Divide(eff_hist2D['MC'][tag][criteria])
            SF_hist2D[tag][criteria] = eff_hist2D['Data'][tag][criteria]
            
            
    SF_Uncertainty = dict() 
    SF_Uncertainty['jet'] = np.zeros(shape=(SF_hist2D['nominal'].GetNbinsX(),SF_hist2D['nominal'].GetNbinsY()),dtype=np.float32) 
    SF_Uncertainty['pv'] = np.zeros(shape=(SF_hist2D['nominal'].GetNbinsX(),SF_hist2D['nominal'].GetNbinsY()),dtype=np.float32) 

    for tag in ['jet','pv']:
        for i in range(SF_hist2D['nominal'].GetNbinsX()):
            for j in range(SF_hist2D['nominal'].GetNbinsY()):
                uncertainty = abs(SF_hist2D[tag]['low'].GetBinContent(i+1,j+1) - SF_hist2D[tag]['high'].GetBinContent(i+1,j+1))
                uncertainty /= SF_hist2D['nominal'].GetBinContent(i+1,j+1)*2.
                SF_Uncertainty[tag][i][j] += uncertainty
    SF_Uncertainty['nominal'] =np.sqrt(SF_Uncertainty['jet']**2 + SF_Uncertainty['pv']**2)
    
    return SF_Uncertainty['nominal']



def GenPaths_HLTTrigger_File(year:str):
    '''
    
    Build JSON file to record trigger conditions for Each particular channels.
    
    '''
    trigger = dict()
    if year=='2017' or year=='2018':
    
        trigger['DoubleElectron'] = ["HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL", "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ", "HLT_passEle32WPTight", "HLT_Ele35_WPTight_Gsf"]
        trigger['DoubleMuon'] = ["HLT_IsoMu27", "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8"]
        trigger["ElectronMuon"] = ["HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ", "HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ", "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ", "HLT_IsoMu27", "HLT_passEle32WPTight", "HLT_passEle32WPTight"]
        trigger['MET'] = ["HLT_PFMET120_PFMHT120_IDTight", "HLT_PFMETNoMu120_PFMHTNoMu120_IDTight", "HLT_PFHT500_PFMET100_PFMHT100_IDTight", "HLT_PFHT700_PFMET85_PFMHT85_IDTight", "HLT_PFHT800_PFMET75_PFMHT75_IDTight"]

    else:
        raise ValueError("year{year} HLT Path has not been specified yet!")
    with open(f'./data/year{year}/TriggerSF/configuration/HLTTrigger.json','w')  as f:
        json.dump(trigger,f,indent=4)



def GenTrigEffInput_File(year:str):
    '''
    
    Build JSON file to record Input path for TriggerEfficiency Calculation Stage.
    
    '''
    if year=='2017' :
        path = {
                "Data":['/eos/cms/store/group/phys_top/ExtraYukawa/TTC_version9/METB.root'
                    ,'/eos/cms/store/group/phys_top/ExtraYukawa/TTC_version9/METC.root'
                    ,'/eos/cms/store/group/phys_top/ExtraYukawa/TTC_version9/METD.root'
                    ,'/eos/cms/store/group/phys_top/ExtraYukawa/TTC_version9/METE.root'
                    ,'/eos/cms/store/group/phys_top/ExtraYukawa/TTC_version9/METF.root'],
                "MC":['/eos/cms/store/group/phys_top/ExtraYukawa/TTC_version9/TTTo2L.root']
                }
    elif year=='2018':
        path = {
                "Data":['/eos/cms/store/group/phys_top/ExtraYukawa/2018/MET_A.root',
                    '/eos/cms/store/group/phys_top/ExtraYukawa/2018/MET_B.root',
                    '/eos/cms/store/group/phys_top/ExtraYukawa/2018/MET_C.root',
                    '/eos/cms/store/group/phys_top/ExtraYukawa/2018/MET_D_0.root',
                    '/eos/cms/store/group/phys_top/ExtraYukawa/2018/MET_D_1.root'
                    ],
                "MC":['/eos/cms/store/group/phys_top/ExtraYukawa/2018/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8.root']
                
                }
    
    else:
        raise ValueError("year{year} HLT Path has not been specified yet!")
    with open(f'./data/year{year}/TriggerSF/path/filein.json','w') as f:
        json.dump(path,f,indent=4)

def GenMCWeightsName_File(year:str):
    if year == '2017':
        weights={
                'Data':'1.',
                'MC':['puWeight','PrefireWeight']
                }
    elif year =='2018':
        weights={
                'Data':'1.',
                'MC':['puWeight']
                }
    else:
        raise ValueError("year{year} HLT Path has not been specified yet!")
    with open(f'./data/year{year}/TriggerSF/configuration/weights.json','w') as f:
        json.dump(weights,f,indent=4)


def GenLeptonIDSF_File(year:str):
    if year=='2017' or year == '2018':
        path = {
                'DoubleElectron':{ 
                    'path':f'/afs/cern.ch/user/m/melu/public/eleIDSF_{year}.root',
                        'name':'EleIDDataEff'},
                'DoubleMuon':{
                    'path':f'/eos/user/t/tihsu/share/muonID_SF/{year}UL/muonIdSF_{year}UL.root',
                    'name':'muIdSF'
                    },
                'ElectronMuon':{
                    'path':{
                        'Muon':f'/eos/user/t/tihsu/share/muonID_SF/{year}UL/muonIdSF_{year}UL.root',
                        'Electron':f'/afs/cern.ch/user/m/melu/public/eleIDSF_{year}.root'
                    },
                    'name':{
                        'Muon':'muIdSF',
                        'Electron':'EleIDDataEff'
                        }

                    }
        }
    else:
        raise ValueError("year{year} HLT Path has not been specified yet!")
    with open(f'./data/year{year}/TriggerSF/path/LeptonsID_SF.json','w') as f:
        json.dump(path,f,indent=4)


def GenVariableNames_File(year:str):
    '''
    
    Build JSON file to record Variable names.
    
    '''
    channels = ['DoubleElectron','DoubleMuon','ElectronMuon']

    property_name = dict()
    if year=='2017' or year =='2018':

        for channel in channels:
            property_name[channel] = dict()

        property_name['DoubleElectron']['region']=3
        property_name['DoubleElectron']['weight'] = {'l1':'Electron_RECO_SF','l2':'Electron_RECO_SF'}

        property_name['DoubleElectron']['OPS_p4'] = {'l1':['OPS_l1_pt','OPS_l1_eta','OPS_l1_phi','OPS_l1_mass'],'l2':['OPS_l2_pt','OPS_l2_eta','OPS_l2_phi','OPS_l2_mass']}

        property_name['DoubleMuon']['region']=1
        property_name['DoubleMuon']['weight'] = {'l1':None,'l2':None}
        property_name['DoubleMuon']['OPS_p4'] = {'l1':['OPS_l1_pt','OPS_l1_eta','OPS_l1_phi','OPS_l1_mass'],'l2':['OPS_l2_pt','OPS_l2_eta','OPS_l2_phi','OPS_l2_mass']}


        property_name['ElectronMuon']['region']=2
        property_name['ElectronMuon']['weight'] = {'l1':None,'l2':['Electron_RECO_SF']}
        property_name['ElectronMuon']['OPS_p4'] = {'l1':['Muon_corrected_pt','Muon_eta','Muon_phi','Muon_mass'],'l2':['Electron_pt','Electron_eta','Electron_phi','Electron_mass']}


        for channel in channels:
            property_name[channel]['ttc_p4'] = {'l1':['ttc_l1_pt','ttc_l1_eta','ttc_l1_phi','ttc_l1_mass'],'l2':['ttc_l2_pt','ttc_l2_eta','ttc_l2_phi','ttc_l2_mass']}

    else:
        raise ValueError("year{year} HLT Path has not been specified yet!")
    with open(f'./data/year{year}/TriggerSF/configuration/name.json','wt') as f:
        json.dump(property_name, f,indent=4)

def GenGoodFlag_File(year:str):
    '''
    Build Json file which contents Flag Name.
    '''
    if year=='2017' or year == '2018':

        Flags = ['Flag_goodVertices','Flag_globalSuperTightHalo2016Filter', 'Flag_HBHENoiseFilter', 'Flag_HBHENoiseIsoFilter', 'Flag_EcalDeadCellTriggerPrimitiveFilter', 'Flag_BadPFMuonFilter', 'Flag_eeBadScFilter', 'Flag_ecalBadCalibFilter']
    else:
        raise ValueError("year{year} HLT Path has not been specified yet!")
    with open(f'./data/year{year}/TriggerSF/configuration/flag.json','wt') as f :
        json.dump(Flags,f,indent=4)



