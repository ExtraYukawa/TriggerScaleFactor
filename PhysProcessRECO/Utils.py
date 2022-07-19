import ROOT,json
import sys
import os 
CURRENT_WORKDIR = os.getcwd()
sys.path.append(CURRENT_WORKDIR)
from ROOT import TH2D,TFile
from array import array
from ROOT import kFALSE
import numpy as np
import math
from math import sqrt
from multiprocessing import Queue, Manager
from Utils.Header import *



def set_axis(histo,coordinate:str,title:str,is_energy:bool):

    if coordinate == 'x':
        axis = histo.GetXaxis()
        axis.SetLabelSize(0.0)
        axis.SetTitleOffset(1.15)
        axis.SetTitleSize(0.0)
    elif coordinate  == 'y':
        axis = histo.GetYaxis()
        axis.SetLabelSize(0.03)
        axis.SetTitleSize(0.04)
        axis.SetTitleOffset(1.2)

    else:
        raise ValueError('Only x and y axis is valid')
    axis.SetLabelFont(42)
    axis.SetLabelOffset(0.015)
    axis.SetNdivisions(505)
    axis.SetTitleFont(42)
    
    if is_energy:
        axis.SetTitle(title + ' [GeV]')
    else:
        axis.SetTitle(title)

from collections import OrderedDict
def Plot(Histo:OrderedDict,year:str, x_name:str, lumi:float,channel='DoubleElectron',veto=False,ylog=0,TrigSF_On=3,IDSF_On=True,RECOSF_On=False,CFSF_On=False,eras=[],FakeRate_On=False,CTSF_On=False,region=''):
    Histo['MC']['DY'].SetFillColor(ROOT.kRed)
    Histo['MC']['VV'].SetFillColor(ROOT.kCyan - 9)
    Histo['MC']['VVV'].SetFillColor(ROOT.kSpring - 9)
    Histo['MC']['SingleTop'].SetFillColor(ROOT.kGray)
    Histo['MC']['ttXorXX'].SetFillColor(ROOT.kViolet-4)
    Histo['MC']['tzq'].SetFillColor(ROOT.kYellow-4)
    Histo['MC']['TT'].SetFillColor(ROOT.kBlue)
     
    if FakeRate_On:
        Histo['MC']['FakeRate'].SetFillColor(ROOT.kBlue-7)
    else:
        Histo['MC']['WJets'].SetFillColor(ROOT.kBlue - 7)

    #for MC in Histo['MC'].keys():
    #    Histo['MC'][MC].Scale(lumi)
    Histo['Data'].SetMarkerStyle(20)
    Histo['Data'].SetMarkerSize(0.85)
    Histo['Data'].SetMarkerColor(1)
    Histo['Data'].SetLineWidth(1)
    
    print('Yield Calculation')
    print('---------------------------')
    Yield =dict()
    Yield['MC'] =dict()
    
    for MC in Histo['MC'].keys():
        Yield['MC'][MC] = round(Histo['MC'][MC].Integral(),1)
        print(f"MC sample({MC}):{Yield['MC'][MC]}")

    Yield['MC'] = OrderedDict(sorted(Yield['MC'].items(),key = lambda x: x[1],reverse=True))

    h_stack = ROOT.THStack()
    Yield['Data'] = Histo['Data'].Integral()
    print(f"Data:{Yield['Data']}")
    print('---------------------------')
    for MC in  Yield['MC'].keys():
        h_stack.Add(Histo['MC'][MC])
    Nbins = h_stack.GetStack().Last().GetNbinsX()
    
    max_yields = 0
    for i in range(1,Nbins+1):
        max_yields_temp = h_stack.GetStack().Last().GetBinContent(i)
        if max_yields_temp>max_yields:max_yields=max_yields_temp
    max_yields_data = 0

    
    for i in range(1,Nbins+1):
        max_yields_data_temp = Histo['Data'].GetBinContent(i)
        if max_yields_data_temp>max_yields_data:max_yields_data=max_yields_data_temp
    if ylog==0:
        y_post_fix =''
        h_stack.SetMaximum(max(max_yields,max_yields_data)*1.8)
    else:
        y_post_fix = '_ylog'
        h_stack.SetMaximum(max(max_yields,max_yields_data)*100)

    h_error = h_stack.GetStack().Last()
    h_error.SetBinErrorOption(ROOT.TH1.kPoisson)
    binsize = h_error.GetSize()-2
    x = []
    y = []
    xerror = []
    yerror_u = []
    yerror_d = []
    xerror_l = []
    xerror_r = []
    y_pad2 = []
    y_pad2_error_u = []
    y_pad2_error_d = []

    
    
    
    
    for i in range(0,binsize):
        x.append(h_error.GetBinCenter(i+1))
        y.append(h_error.GetBinContent(i+1))
        y_pad2.append(1.0)
        xerror_l.append(0.5 * h_error.GetBinWidth(i+1))
        xerror_r.append(0.5 * h_error.GetBinWidth(i+1))
        yerror_u.append(h_error.GetBinErrorUp(i+1))
        yerror_d.append(h_error.GetBinErrorLow(i+1))
        if h_error.GetBinContent(i+1)<=0:
            y_pad2_error_u.append(0)
            y_pad2_error_d.append(0)
        else:
            y_pad2_error_u.append(h_error.GetBinErrorUp(i+1)/(h_error.GetBinContent(i+1)))
            y_pad2_error_d.append(h_error.GetBinErrorLow(i+1)/(h_error.GetBinContent(i+1)))



    gr = ROOT.TGraphAsymmErrors(len(x), np.array(x), np.array(y),np.array(xerror_l),np.array(xerror_r), np.array(yerror_d), np.array(yerror_u))
    gr_pad2 = ROOT.TGraphAsymmErrors(len(x), np.array(x), np.array(y_pad2),np.array(xerror_l),np.array(xerror_r), np.array(y_pad2_error_d), np.array(y_pad2_error_u))
    

    from  Utils.CMSTDRStyle import setTDRStyle
    T = setTDRStyle()
    T.cd()
    c= ROOT.TCanvas()
    c.cd()
    pad1 = ROOT.TPad('pad1','',0.00,0.22,0.99,0.99)
    pad2 = ROOT.TPad('pad1','',0.00, 0.00, 0.99, 0.22)
    pad1.SetBottomMargin(0.02);
    pad2.SetTopMargin(0.035);
    pad2.SetBottomMargin(0.45);
    pad1.Draw()
    pad2.Draw()
    pad1.cd()
    h_stack.Draw('HIST')
    Histo['Data'].Draw("SAME pe")

    gr.SetFillColor(1)
    gr.SetFillStyle(3005)
    gr.Draw("SAME 2")
    print('Set X axis Name')
    if 'DY_l1_pt' in x_name:set_axis(h_stack,'x', 'pt of leading lepton', True)
    if 'DY_l1_eta' in x_name:set_axis(h_stack,'x', '#eta of leading lepton', False)
    if 'DY_l1_phi' in x_name:
        set_axis(h_stack,'x', 'phi of leading lepton', False)
    if 'DY_l2_pt' in x_name:set_axis(h_stack,'x', 'pt of subleading lepton', True)
    if 'DY_l2_eta' in x_name:set_axis(h_stack,'x', '#eta of subleading lepton', False)
    if 'DY_l2_phi' in x_name:set_axis(h_stack,'x', 'phi of subleading lepton', False)
    if 'DY_mll' in x_name:set_axis(h_stack,'x', 'Z mass', True)

    if 'ttc_l1_pt' in x_name:set_axis(h_stack,'x', 'pt of leading lepton', True)
    if 'ttc_l1_eta' in x_name:set_axis(h_stack,'x', '#eta of leading lepton', False)
    if 'ttc_l1_phi' in x_name:set_axis(h_stack,'x', 'phi of leading lepton', False)
    if 'ttc_l2_pt' in x_name:set_axis(h_stack,'x', 'pt of subleading lepton', True)
    if 'ttc_l2_eta' in x_name:set_axis(h_stack,'x', '#eta of subleading lepton', False)
    if 'ttc_l2_phi' in x_name:set_axis(h_stack,'x', 'phi of subleading lepton', False)
    if 'ttc_mll' in x_name:set_axis(h_stack,'x', 'Invariant Mass of Dilepton System', True)
    if 'ttc_mllj1' in x_name:set_axis(h_stack,'x','ttc_mllj1',True)
    if 'ttc_mllj2' in x_name:set_axis(h_stack,'x','ttc_mllj2',True)
    if 'ttc_mllj3' in x_name:set_axis(h_stack,'x','ttc_mllj3',True)
    if 'ttc_met' in x_name:set_axis(h_stack,'x','ttc_met',True)
    if 'HT' in x_name:set_axis(h_stack,'x','HT',False)
    if 'ttc_met_phi' in x_name:set_axis(h_stack,'x','ttc_met_phi',False)
    if 'j1_FlavB' in x_name:set_axis(h_stack,'x','j1_FlavB',False)
    if 'j2_FlavB' in x_name:set_axis(h_stack,'x','j2_FlavB',False)
    if 'j3_FlavB' in x_name:set_axis(h_stack,'x','j3_FlavB',False)
    if 'j1_FlavCvL' in x_name:set_axis(h_stack,'x','j1_FlavCvL',False)
    if 'j2_FlavCvL' in x_name:set_axis(h_stack,'x','j2_FlavCvL',False)
    if 'j3_FlavCvL' in x_name:set_axis(h_stack,'x','j3_FlavCvL',False)
    if 'j1_FlavCvB' in x_name:set_axis(h_stack,'x','j1_FlavCvB',False)
    if 'j2_FlavCvB' in x_name:set_axis(h_stack,'x','j2_FlavCvB',False)
    if 'j3_FlavCvB' in x_name:set_axis(h_stack,'x','j3_FlavCvB',False)
    
    
    set_axis(h_stack,'y', 'Event/Bin', False)
    
    import Utils.CMSstyle as CMSstyle
    CMSstyle.SetStyle(pad1,year,lumi=lumi,ylog=ylog)

   #legend
    print('Histogram Setting')
    leg1 = ROOT.TLegend(0.66, 0.75, 0.94, 0.88)
    leg2 = ROOT.TLegend(0.44, 0.75, 0.64, 0.88)
    leg3 = ROOT.TLegend(0.17, 0.75, 0.40, 0.88)
    leg1.SetMargin(0.4)
    leg2.SetMargin(0.4)
    leg3.SetMargin(0.4)
    print('Legend Entry:DY')
    leg3.AddEntry(Histo['MC']['DY'],'DY ['+str(Yield['MC']['DY'])+']','f')
    print('Legend Entry:stat. unc')
    leg3.AddEntry(gr,'Stat. unc','f')
    print('Legend Entry:Data')
    leg3.AddEntry(Histo['Data'],'Data ['+str(Yield['Data'])+']','pe')
    print('Legend Entry:TT')
    leg2.AddEntry(Histo['MC']['TT'],'TT ['+str(Yield['MC']['TT'])+']','f')
    
    if FakeRate_On:
        print('Legend Entry:FakeRate')
        leg2.AddEntry(Histo['MC']['FakeRate'],'FakeLep ['+str(Yield['MC']['FakeRate'])+']','f')
    else:
        print('Legend Entry:WJets')
        leg2.AddEntry(Histo['MC']['WJets'],'WJets ['+str(Yield['MC']['WJets'])+']','f')
    print('Legend Entry:VV')
    leg2.AddEntry(Histo['MC']['VV'],'VV ['+str(Yield['MC']['VV'])+']','f')

    print('Legend Entry:VVV')
    leg1.AddEntry(Histo['MC']['VVV'],'VVV ['+str(Yield['MC']['VVV'])+']','f')
    print('Legend Entry:SingleTop')
    leg1.AddEntry(Histo['MC']['SingleTop'],'SingleTop ['+str(Yield['MC']['SingleTop'])+']','f')
    print('Legend Entry:ttXorXX')
    leg1.AddEntry(Histo['MC']['ttXorXX'],'ttXorXX ['+str(Yield['MC']['ttXorXX'])+']','f')
    print('Legend Entry:tzq')
    leg1.AddEntry(Histo['MC']['tzq'],'tzq ['+str(Yield['MC']['tzq'])+']','f')
    print('Legend Setting')
    leg1.SetFillColor(ROOT.kWhite)
    leg1.Draw('same')
    leg2.SetFillColor(ROOT.kWhite)
    leg2.Draw('same')
    leg3.SetFillColor(ROOT.kWhite)
    leg3.Draw('same')

    pad2.cd()

    print('pred/MC. plots setting')
    hMC = h_stack.GetStack().Last()
    
    
    hData =Histo['Data'].Clone()
    hData.Divide(hMC)
    hData.SetMarkerStyle(20)
    hData.SetMarkerSize(0.85)
    hData.SetMarkerColor(1)
    hData.SetLineWidth(1)
    
    hData.GetYaxis().SetTitle("Data/MC")
    hData.GetXaxis().SetTitle(h_stack.GetXaxis().GetTitle())
    hData.GetYaxis().CenterTitle()
    hData.SetMaximum(2.0)
    hData.SetMinimum(0.0)
    hData.GetYaxis().SetNdivisions(4,kFALSE)
    hData.GetYaxis().SetTitleOffset(0.3)
    hData.GetYaxis().SetTitleSize(0.13)
    hData.GetYaxis().SetLabelSize(0.1)
    hData.GetXaxis().SetTitleSize(0.14)
    hData.GetXaxis().SetLabelSize(0.1)
    hData.Draw()

    gr_pad2.SetFillColor(1)
    gr_pad2.SetFillStyle(3005)
    gr_pad2.Draw("SAME 2")

    c.Update()

    with open(f'./data/year{year}/TriggerSF/User.json','r') as f:
        UserName = json.load(f)['UserName']

    Dir = f'/eos/user/{UserName[0]}/{UserName}/ExtraYukawa/PhysProcessRECO/year{year}/{channel}/plots/{region}'
    
    if veto:
        veto_postfix = '_vetohemregion'
    else :
        veto_postfix =''
    
    if TrigSF_On != 0:
        if TrigSF_On ==1 :
            TrigSF_postfix = '_TrigSF_l1pteta'
        elif TrigSF_On ==2 :
            TrigSF_postfix = '_TrigSF_l2pteta'
        elif TrigSF_On ==3 :
            TrigSF_postfix = '_TrigSF_l1l2pt'
        elif TrigSF_On ==4 :
            TrigSF_postfix = '_TrigSF_l1l2eta'
    else:
        TrigSF_postfix = ''
    if IDSF_On:
        IDSF_postfix = '_IDSF'
    else:
        IDSF_postfix = ''
    if RECOSF_On:
        RECOSF_postfix = '_RECOSF'
    else:
        RECOSF_postfix = ''
    if CFSF_On:
        CFSF_postfix = '_CFSF'
    else:
        CFSF_postfix =''
    if FakeRate_On:
        FakeRate_postfix = '_FakeRate'
    else:
        FakeRate_postfix =''
    if CTSF_On:
        CTSF_postfix = '_CTSF'
    else:
        CTSF_postfix = ''

    era_post_fix = ''
    for a in eras:
        era_post_fix+='_'+a
    print('Save Plots') 
    
    
    c.SaveAs(os.path.join(Dir,x_name+TrigSF_postfix+IDSF_postfix+RECOSF_postfix+CFSF_postfix+y_post_fix+FakeRate_postfix+CTSF_postfix+era_post_fix+'.pdf'))
    c.SaveAs(os.path.join(Dir,x_name+TrigSF_postfix+IDSF_postfix+RECOSF_postfix+CFSF_postfix+y_post_fix+FakeRate_postfix+CTSF_postfix+era_post_fix+'.png'))
    
    c.Close()
    #pad1.Close()
    #pad2.Close()

    del T
    del c
    del hData
    del hMC

