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
from Utils.General_Tool import get_NumberOfEvent,Hist2D_to_Binx_Equal



def Plot(func,**user_settings):
    def decorator(tag):
        return func(tag=tag,**user_settings)
    return decorator


def plot_eff1d(tag:str,**settings):
    
    
    if settings['year'] == '2018' and settings['veto']:

        FileIn = {
                'Data':ROOT.TFile.Open(os.path.join(settings['DirIn'],'EfficiencyForData_vetohemregion.root'),"READ"),
                    'MC':ROOT.TFile.Open(os.path.join(settings['DirIn'],'EfficiencyForMC_vetohemregion.root'),"READ"),
                }
    
    else:
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

    with open(f'./data/year{settings["year"]}/TriggerSF/configuration/lumi.json',"r") as f:
        lumi = json.load(f)[f'{settings["year"]}']
    CMSstyle.SetStyle(pad,year=settings['year'],lumi=lumi)
    leg.SetFillStyle(0)
    leg.Draw('SAME') 
    c.Update()
    if settings['veto']:
        c.SaveAs(os.path.join(settings['DirOut'],'Efficiency_1D_'+tag+'_vetohemregion.png'))
    else:
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
    if settings['year'] == '2018' and settings['veto']:
        FileIn = {
                'Data':ROOT.TFile.Open(os.path.join(settings['DirIn'],'EfficiencyForData_vetohemregion.root'),"READ"),
                    'MC':ROOT.TFile.Open(os.path.join(settings['DirIn'],'EfficiencyForMC_vetohemregion.root'),"READ")
                }
    
    else:
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

        with open(f'./data/year{settings["year"]}/TriggerSF/configuration/lumi.json',"r") as f:
            lumi = json.load(f)[f'{settings["year"]}']
        if settings['veto']:
            with open(f'./data/year{settings["year"]}/TriggerSF/configuration/veto_ratio.json','r') as f:
                ratio = json.load(f)['MET']

            lumi = ratio * lumi


        CMSstyle.SetStyle(pad,year=settings['year'],lumi=lumi)
        pad.SetRightMargin(0.15)
        c.SetGridx(False)
        c.SetGridy(False)
        c.Update()
        if settings['year'] == '2018' and settings['veto']:
            c.SaveAs(os.path.join(settings['DirOut'],'Efficiency_2D_'+Type+'_'+tag+'_vetohemregion.png'))
        else:
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
    
    if settings['year'] == '2018' and settings['veto']:
        FileIn = {
                'Data':ROOT.TFile.Open(os.path.join(settings['DirIn'],'EfficiencyForData_vetohemregion.root'),"READ"),
                    'MC':ROOT.TFile.Open(os.path.join(settings['DirIn'],'EfficiencyForMC_vetohemregion.root'),"READ")
                }
    
    else:
        FileIn = {
                'Data':ROOT.TFile.Open(os.path.join(settings['DirIn'],'EfficiencyForData.root'),"READ"),
                    'MC':ROOT.TFile.Open(os.path.join(settings['DirIn'],'EfficiencyForMC.root'),"READ")
                }
    
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

    with open(f'./data/year{settings["year"]}/TriggerSF/configuration/lumi.json',"r") as f:
        lumi = json.load(f)[f'{settings["year"]}']
    
    
    if settings['year'] == '2018' and settings['veto']:  
        f = ROOT.TFile.Open(os.path.join(settings['DirIn'],'SF'+'_'+nominal_name+'_vetohemregion.root'),'RECREATE')
    else:
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
    
    


    CMSstyle.SetStyle(pad,year=settings['year'],lumi=lumi)
    pad.SetRightMargin(0.15)
    
    c.SetGridx(False)
    c.SetGridy(False)
    c.Update()
    if settings['year'] == '2018' and settings['veto']:  
        c.SaveAs(os.path.join(settings['DirOut'],'SF'+'_'+nominal_name+'_vetohemregion.png'))
    else:
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



