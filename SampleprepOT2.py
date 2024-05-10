# -*- coding: utf-8 -*-
"""
Created on Fri May 10 12:30:45 2024

@author: oscar
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 15:18:06 2020
#incorrect date
@author: oscar
"""
from opentrons import protocol_api
metadata = {'apiLevel':'2.12',
            'desription':'This is the library preperation of 7 cryptophanes and 9 chlorides. Made listening to UNKLE',
           'author':'Oscar Lloyd Williams'}

def run(protocol: protocol_api.ProtocolContext):
    
    solventsource=protocol.load_labware('olw_2schott_100000ul',3)
    solvents={'MeOH':'A1', 'MeOH2':'A2'}
    
    #plates for final solutions
    finplate1 = protocol.load_labware('olw_40hplc_2000ul', 11)
    finplate2 = protocol.load_labware('olw_40hplc_2000ul', 8)
    
    #plates for stocks
    stockplate=protocol.load_labware('olw_8_wellplate_20000ul', 4)
    stocks={'LiCl':'A1','NaCl':'A2', 'KCl':'A3','RbCl':'A4','CsCl':'B1','MgCl2':'B2','CaCl2':'B3','SrCl2':'B4'}
    stockplate2=protocol.load_labware('olw_8_wellplate_20000ul', 5)
    stocks2={'222':'A1','223':'A2', '233':'A3','233OH7':'A4','224':'B1','222mol1':'B2','222mol2':'B3','AmCl':'B4'}
    
    #tipracks for 2 pippettes
    tiprackbig = protocol.load_labware('opentrons_96_tiprack_1000ul', 1)
    tiprackbig2 = protocol.load_labware('opentrons_96_tiprack_1000ul', 2)
    
    #pippettes
    pipettebig = protocol.load_instrument('p1000_single_gen2', 'left',tip_racks=[tiprackbig, tiprackbig2])
    #pipettesmol = protocol.load_instrument('p300_single_gen2', 'right',tip_racks=[tipracklil])
    pipettebig.well_bottom_clearance.dispense = 3
    
    #count for iterating coloumns of endplates
    colcount=1
    rowcount=1
    #early alphabet to conver rowcount into letters
    earlyalfa=['A','B','C','D','E']
    protocol.set_rail_lights(True)
    #iterating through each cryptophane
    for stock2 in stocks2:
        
        #AMCl is not a cryptophane, replacing the 8th one with a methanol
        if stock2=='AmCl':
            
            pipettebig.transfer(500, solventsource.wells_by_name()['A1'], finplate1.columns_by_name()['8'])
            pipettebig.transfer(500, solventsource.wells_by_name()['A1'], finplate2.columns_by_name()['8'])
            
            donesignal="'Done methanol from A1 into col 8'"
            protocol.comment(donesignal)
            
        else:
            currentcrypt=stocks2.get(stock2)
            
            pipettebig.transfer(500, stockplate2.wells_by_name()[str(currentcrypt)], finplate1.columns_by_name()[str(colcount)])
            pipettebig.transfer(500, stockplate2.wells_by_name()[str(currentcrypt)], finplate2.columns_by_name()[str(colcount)])
            
            colcount=colcount+1
            donesignal="'Done "+str(stock2)+" from "+str(currentcrypt)+" into col "+str(colcount)+"'"
            protocol.comment(donesignal)
            
    protocol.pause('check cryptophanes are done')
    
    rowcount=1
    for stock in stocks:
        if rowcount<6:
            row=earlyalfa[rowcount-1]
            currentchloride=stocks.get(stock)  
            pipettebig.transfer(500, stockplate.wells_by_name()[str(currentchloride)], finplate1.rows_by_name()[row],new_tip='always')
            
            donesignal="'Done "+str(stock)+" from "+str(currentchloride)+" into row "+str(row)+"'"
            protocol.comment(donesignal)
            
        if rowcount >= 6:
            virtualrowcount=rowcount-5
            row=earlyalfa[virtualrowcount-1]
            pipettebig.transfer(500, stockplate.wells_by_name()[str(currentchloride)], finplate2.rows_by_name()[row],new_tip='always')
            print('yay')
            donesignal="'Done "+str(stock)+" from "+str(currentchloride)+" into row "+str(row)+"'"
            protocol.comment(donesignal)
        rowcount=rowcount+1
    
    pipettebig.transfer(500, stockplate2.wells_by_name()['B4'], finplate2.rows_by_name()['D'],new_tip='always')
    donesignal="'Done AmCL from stock2 B4 into row D"
    protocol.comment(donesignal)
    pipettebig.transfer(500, solventsource.wells_by_name()['A1'], finplate2.rows_by_name()['E'],new_tip='always')
    donesignal="'Done methanol from solvents into row E"
    protocol.set_rail_lights(False)
