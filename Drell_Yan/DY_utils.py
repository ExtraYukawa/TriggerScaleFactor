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


class MyDataFrame(object):
    def __init__(self,settings:dict) -> None:
        '''
        self._channel -> DoubleElectron, DoubleMuon, or ElectronMuon    
        self._Trigger_Condition -> DiLeptons HLT conditions
        self._weight -> Scale Factors for Dileptons
        self._Data(bool) -> Input File(s) is(are) Data/MC
        self._filters -> Offline triggers for Dileptons
        self._File_Paths -> Paths for input Files
        '''
        self.__Data = settings.get('Data')
        self.__SF_mode = settings.get('SF_mode')
        self.__channel = settings.get('channel')
        
        if not self.__Data:
            self.__TriggerSF_File = settings.get('TriggerSF')['file'][self.__channel]
            self.__TriggerSF_Branch = settings.get('TriggerSF')['branchname']
            #ROOT.gInterpreter.ProcessLine(Histogram_Definition['Diff_Type'].format(self.__TriggerSF_File['l1'],self.__TriggerSF_File['l2'],self.__TriggerSF_Branch['l1'],self.__TriggerSF_Branch['l2']))

        
        if self.__channel == 'ElectronMuon':
            DY_region = 2 
            self.__lepton_RECO_SF = 'Electron_RECO_SF[OPS_l2_id]'
        elif self.__channel != None:
            if self.__channel == 'DoubleElectron':
                DY_region = 3
                self.__lepton_RECO_SF = 'Electron_RECO_SF[OPS_l1_id]*Electron_RECO_SF[OPS_l2_id]'
            elif self.__channel == 'DoubleMuon':
                DY_region = 1
                self.__lepton_RECO_SF = '1'
        
        else:
            raise ValueError(f'No such channel{self.__channel}')
        
        self.__filters = 'OPS_region=={0} && OPS_z_mass > 60 && OPS_z_mass<120 && (OPS_l1_pt>30 || OPS_l2_pt>30) && OPS_drll>0.3'.format(DY_region)    
        self.__df_tree = ROOT.RDataFrame
        self.__Hists = Manager().dict()
        
        self.__Trigger_Condition = settings.get('Trigger_Condition')
        
        
        self.__nevents =  settings.get('nevents')       
        
        File_Paths = settings.get('File_Paths')
        self.__File_Paths = ROOT.std.vector('string')()
        self.__weights = '*'.join(settings.get('weights'))
        
        if self.__Data == True:
            for path in File_Paths:
                self.__File_Paths.push_back(path)
        else:
            self.__File_Paths.push_back(File_Paths)
    @property
    def Tree(self) ->ROOT.RDataFrame.Filter:
        return self.__df_tree
    @property
    def IsData(self) ->bool:
        return self.__Data
    @property
    def channel(self)->str:
        return self.__channel
    @channel.setter
    def channel(self,channel:str)->str:
        self.__channel = channel
    @property
    def Trigger_Condition(self)->str:
        return self.__Trigger_Condition
    @property
    def lepton_RECO_SF(self) -> str:
        return self.__lepton_RECO_SF
    @property
    def File_Paths(self) ->ROOT.std.vector('string')():
        return self.__File_Paths
    @property
    def offline_trig(self) -> str:
        return self.__filters 
    @Tree.setter
    def Tree(self, Tree:ROOT.RDataFrame.Filter):
        self.__df_tree = Tree
    @property
    def Hists(self) ->dict():
        return self.__Hists

    @Hists.setter
    def Hists(self, Hists:dict):
        self.__Hists =Hists
    @property
    def nevents(self)->int:
        return self.__nevents
    
    @property
    def SF_mode(self)->bool:
        return self.__SF_mode
    @property
    def p_weight(self)->str:
        return self.__weights
def Filtering(df:MyDataFrame,HistsSettings:dict):
    
    if df.nevents ==-1:
        Tree= ROOT.RDataFrame('Events',df.File_Paths)
    else:
        Tree = ROOT.RDataFrame('Events',df.File_Paths).Range(0,df.nevents)
    if not df.IsData:
        if df.SF_mode == 0:
            Tree = Tree.Define('trigger_SF','1.')
            Tree = Tree.Define('Id_SF','1.')
        elif df.SF_mode ==1:
            Tree = Tree.Define('trigger_SF','1.')
            Tree = Tree.Define('Id_SF',f'IDScaleFact("{df.channel}",h1,h2,OPS_l1_pt,OPS_l2_pt,abs(OPS_l1_eta),abs(OPS_l2_eta))')
        else:
            Tree = Tree.Define('Id_SF',f'IDScaleFact("{df.channel}",h1,h2,OPS_l1_pt,OPS_l2_pt,abs(OPS_l1_eta),abs(OPS_l2_eta))')
            Tree = Tree.Define('trigger_SF','Trigger_sf(h1,OPS_l1_pt,OPS_l1_eta)*Trigger_sf(h2,OPS_l2_pt,OPS_l2_eta)')
        Tree = Tree.Define('genweight',f'{df.p_weight}*{df.lepton_RECO_SF}*trigger_SF*Id_SF*genWeight/abs(genWeight)')

    Tree = Tree.Filter(df.offline_trig)
    df.Tree =Tree.Filter(df.Trigger_Condition)

    Hists =dict()
    for name in HistsSettings.keys():
        setting = HistsSettings[name]
        if df.IsData != None:
            if df.IsData :
                Hists[name] = df.Tree.Histo1D((setting['name'],'',setting['nbins'],setting['lowedge'],setting['highedge']),setting['name'])
            else:
                Hists[name] = df.Tree.Histo1D((setting['name'],'',setting['nbins'],setting['lowedge'],setting['highedge']),setting['name'],'genweight')
        else:
            raise ValueError
    df.Hists = Hists



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
def Plot(Histo:OrderedDict,year:str, x_name:str, lumi:int,SF_mode:int,channel='DoubleElectron'):

    Histo['MC']['DY'].SetFillColor(ROOT.kRed)
    Histo['MC']['WJets'].SetFillColor(ROOT.kBlue - 7)
    Histo['MC']['VV'].SetFillColor(ROOT.kCyan - 9)
    Histo['MC']['VVV'].SetFillColor(ROOT.kSpring - 9)
    Histo['MC']['SingleTop'].SetFillColor(ROOT.kGray)
    Histo['MC']['ttXorXX'].SetFillColor(ROOT.kViolet-4)
    Histo['MC']['tzq'].SetFillColor(ROOT.kYellow-4)
    Histo['MC']['TT'].SetFillColor(ROOT.kBlue)

    for MC in Histo['MC'].keys():
        Histo['MC'][MC].Scale(lumi)

    Histo['Data'].SetMarkerStyle(20)
    Histo['Data'].SetMarkerSize(0.85)
    Histo['Data'].SetMarkerColor(1)
    Histo['Data'].SetLineWidth(1)

    Yield =dict()
    Yield['MC'] =dict()
    for MC in Histo['MC'].keys():
        Yield['MC'][MC] = round(Histo['MC'][MC].Integral(),1)
    Yield['MC'] = OrderedDict(sorted(Yield['MC'].items(),key = lambda x: x[1],reverse=True))
    Yield['Data'] = round(Histo['Data'].Integral(),1)

    h_stack = ROOT.THStack()

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

    h_stack.SetMaximum(max(max_yields,max_yields_data)*1.8)


    h_error = h_stack.GetStack().Last()
    h_error.SetBinErrorOption(ROOT.TH1.kPoisson)

    binsize = h_error.GetSize()-2
    x = []
    y = []
    xerror = []
    yerror_u = []
    yerror_d = []

    for i in range(0,binsize):
        x.append(h_error.GetBinCenter(i+1))
        y.append(h_error.GetBinContent(i+1))
        xerror.append(0.5*h_error.GetBinWidth(i+1))
        yerror_u.append(0.5*h_error.GetBinErrorUp(i+1))
        yerror_d.append(0.5*h_error.GetBinErrorLow(i+1))

    gr = ROOT.TGraphAsymmErrors(len(x), np.array(x), np.array(y),np.array(xerror),np.array(xerror), np.array(yerror_d), np.array(yerror_u))

    

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
    if 'DY_l1_pt' in x_name:set_axis(h_stack,'x', 'pt of leading lepton', True)
    if 'DY_l1_eta' in x_name:set_axis(h_stack,'x', '#eta of leading lepton', False)
    if 'DY_l1_phi' in x_name:set_axis(h_stack,'x', 'phi of leading lepton', False)
    if 'DY_l2_pt' in x_name:set_axis(h_stack,'x', 'pt of subleading lepton', True)
    if 'DY_l2_eta' in x_name:set_axis(h_stack,'x', '#eta of subleading lepton', False)
    if 'DY_l2_phi' in x_name:set_axis(h_stack,'x', 'phi of subleading lepton', False)
    if 'DY_z_mass' in x_name:set_axis(h_stack,'x', 'Z mass', True)
    set_axis(h_stack,'y', 'Event/Bin', False)
    
    import Utils.CMSstyle as CMSstyle
    CMSstyle.SetStyle(pad1,year)

   #legend
    leg1 = ROOT.TLegend(0.66, 0.75, 0.94, 0.88)
    leg2 = ROOT.TLegend(0.44, 0.75, 0.64, 0.88)
    leg3 = ROOT.TLegend(0.17, 0.75, 0.40, 0.88)
    leg1.SetMargin(0.4)
    leg2.SetMargin(0.4)
    leg3.SetMargin(0.4)

    
    leg3.AddEntry(Histo['MC']['DY'],'DY ['+str(Yield['MC']['DY'])+']','f')
    leg3.AddEntry(gr,'Stat. unc','f')
    leg3.AddEntry(Histo['Data'],'Data ['+str(Yield['Data'])+']','pe')

    leg2.AddEntry(Histo['MC']['TT'],'TT ['+str(Yield['MC']['TT'])+']','f')
    leg2.AddEntry(Histo['MC']['WJets'],'WJets ['+str(Yield['MC']['WJets'])+']','f')
    leg2.AddEntry(Histo['MC']['VV'],'VV ['+str(Yield['MC']['VV'])+']','f')

    leg1.AddEntry(Histo['MC']['VVV'],'VVV ['+str(Yield['MC']['VVV'])+']','f')
    leg1.AddEntry(Histo['MC']['SingleTop'],'SingleTop ['+str(Yield['MC']['SingleTop'])+']','f')
    leg1.AddEntry(Histo['MC']['ttXorXX'],'ttXorXX ['+str(Yield['MC']['ttXorXX'])+']','f')
    leg1.AddEntry(Histo['MC']['tzq'],'tzq ['+str(Yield['MC']['tzq'])+']','f')

    leg1.SetFillColor(ROOT.kWhite)
    leg1.Draw('same')
    leg2.SetFillColor(ROOT.kWhite)
    leg2.Draw('same')
    leg3.SetFillColor(ROOT.kWhite)
    leg3.Draw('same')

    pad2.cd()

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
    hData.SetMaximum(1.5)
    hData.SetMinimum(0.5)
    hData.GetYaxis().SetNdivisions(4,kFALSE)
    hData.GetYaxis().SetTitleOffset(0.3)
    hData.GetYaxis().SetTitleSize(0.14)
    hData.GetYaxis().SetLabelSize(0.1)
    hData.GetXaxis().SetTitleSize(0.14)
    hData.GetXaxis().SetLabelSize(0.1)
    hData.Draw()

    c.Update()
    
    with open(f'./data/year{year}/DrellYan/User.json') as f:
        UserName = json.load(f)['UserName']

    Dir = f'/eos/user/{UserName[0]}/{UserName}/ExtraYukawa/DrellYan/year{year}/{channel}/plots'
    if SF_mode == 0:
        c.SaveAs(os.path.join(Dir,x_name+'_noSF.pdf'))
        c.SaveAs(os.path.join(Dir,x_name+'_noSF.png'))
    elif SF_mode ==1:
        c.SaveAs(os.path.join(Dir,x_name+'_only_IDSF'+'.pdf'))
        c.SaveAs(os.path.join(Dir,x_name+'_only_IDSF'+'.png'))
    elif SF_mode ==2:
        c.SaveAs(os.path.join(Dir,x_name+'_ID_Trig_SF'+'.pdf'))
        c.SaveAs(os.path.join(Dir,x_name+'_ID_Trig_SF'+'.png'))
    
    else:
        raise ValueError('weired.')
    c.Close()
    #pad1.Close()
    #pad2.Close()

    del T
    del c
    del hData
    del hMC

