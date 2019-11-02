'''
Created on Oct 17, 2019

@author: togunyale
'''
from selenium import webdriver
from time import sleep
import datetime
from pathlib import Path
import os

homeUrl = 'https://www.basketball-reference.com'
dataFolder = '/Users/togunyale/eclipse-workspace/ReboundingProject/playbyplaydata'
name_excepts = { "CHA" : "CHO" , "NY" : "NYK" , "UTAH" : "UTA" , "GS" : "GSW" , "PHX" : "PHO" , "NO" : "NOP" , "WSH" : "WAS", "BKN" : "BRK", "SA" : "SAS"}
activePlayers = set()
confirmedPlayers = set()
Offensive3 = dict()
Defensive3 = dict()
Offensive2 = dict()
Defensive2 = dict()
errorPlayer = list()
def main():
    getPlayers()
    showStats()
    
    
def getPlayers():
    with open('/Users/togunyale/eclipse-workspace/ReboundingProject/logs/InsertErrorLogV2.txt', 'r') as f2:
        for line in f2:
            if 'Trail' not in line:
                stat = line.split('  ::')[0].split(' : ')[1].rstrip()
                team = stat.split(' :: ')[0]
                player = stat.split(' :: ')[1]
                
                if 'Jr.' in player:
                    player = player.split(' Jr.')[0]
                if 'III' in player:
                    player = player.split(' III')[0]
                if 'IV' in player:
                    player = player.split(' IV')[0]
                    
                errorPlayer.append(team+" :: "+player)

    for filename in os.listdir(dataFolder):
        openFile = open(dataFolder + "/" + filename,'r')
        playByplay = openFile.readlines()
        
        for play in xrange(len(playByplay) - 1):
            if 'miss' in playByplay[play] or 'blocks' in playByplay[play]:
                if 'free' not in playByplay[play]:
                    player = ' '
                    if 'three' in playByplay[play]:
                        if 'offensive' in playByplay[play + 1]:
                            
                            player = playByplay[play + 1].split('offensive')[0]
                            
                            for temp in errorPlayer:
                                if temp in player:
                                    player = temp
                                    break
                            
                            if player in Offensive3:
                                Offensive3[player] += 1
                                activePlayers.add(player)
                            else :
                                Offensive3[player] = 1
                                activePlayers.add(player)
                            
                        elif 'defensive' in playByplay[play + 1]:
                            
                            player = playByplay[play + 1].split('defensive')[0] 
                            
                            for temp in errorPlayer:
                                if temp in player:
                                    player = temp
                                    break
                            
                            if player in Defensive3:
                                Defensive3[player] += 1
                                activePlayers.add(player)
                                
                            else :
                                Defensive3[player] = 1
                                activePlayers.add(player)
                        
                    else :
                        if 'offensive' in playByplay[play + 1]:
                            
                            player = playByplay[play + 1].split('offensive')[0] 
                            for temp in errorPlayer:
                                if temp in player:
                                    player = temp
                                    break
                            
                            if player in Offensive2:
                                Offensive2[player] += 1
                                activePlayers.add(player)
                                
                            else :
                                Offensive2[player] = 1
                                activePlayers.add(player)
                        
                        elif 'defensive' in playByplay[play + 1]:
                            
                            player = playByplay[play + 1].split('defensive')[0] 
                            
                            for temp in errorPlayer:
                                if temp in player:
                                    player = temp
                                    break
                            
                            if player in Defensive2:
                                Defensive2[player] += 1
                                activePlayers.add(player)
                                
                            else :
                                Defensive2[player] = 1
                                activePlayers.add(player)
    
def showStats():
    count = 0
    for player in activePlayers:
        if player :
            if len(player.split(' :: '))>1 and 'Trail Blazers' not in player.split(' :: ')[1]:
                if len(player.split(' :: ')[1].split()) != 1 :
                    if Path('/Users/togunyale/eclipse-workspace/ReboundingProject/playerstats/player='+player.rstrip()+'.txt').is_file():
                        print player + " : ALREADY EXISTS"
                        continue
                    with open('/Users/togunyale/eclipse-workspace/ReboundingProject/playerstats/player='+player.rstrip()+'.txt', 'a') as f1:
                             
                        rebs =[0,0,0,0]
                        
                        if player in Offensive3:
                            rebs[0] =  Offensive3[player]
                        
                        if player in Offensive2:
                            rebs[1] =  Offensive2[player] 
                        
                        if player in Defensive3:
                            rebs[2] =  Defensive3[player]
                        
                        if player in Defensive2:
                            rebs[3] =  Defensive2[player]
                            
                        insertErrorLog = open ('/Users/togunyale/eclipse-workspace/ReboundingProject/logs/InsertErrorLogV3.txt', 'a')

                        try:
                            attributes_player = getAttributes(player.split(' :: ')[1].rstrip(),player.split(' :: ')[0])                                                                                   #Offensive 3         Offensive 2              Defensive2           Defensive3                   
                            f1.write(attributes_player + " : " + str(rebs[0]) + " : " + str(rebs[1]) + " : " + str(rebs[2]) + " : " + str(rebs[3]) +"\n")
                            f1.write('END \n')
                            
                            if attributes_player.split(':')[2] == 0 or attributes_player.split(':')[2] == '0': 
                                os.remove('/Users/togunyale/eclipse-workspace/ReboundingProject/playerstats/player='+player.rstrip()+'.txt')
                                print player + " Removed because data was not gather correctly"
                        except Exception as e:
                            
                            insertErrorLog.write( "Error with : " + player + " ::" + str(e) +   "\n")
                            insertErrorLog.close()
                            os.remove('/Users/togunyale/eclipse-workspace/ReboundingProject/playerstats/player='+player.rstrip()+'.txt')
                            count+=1
                            print player + "Removed because of error "
                            continue
                        insertErrorLog.close()
                        print str(count) + " ; " + player
        count+=1
def getAttributes(Player,team): 
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        driver = webdriver.Chrome("/Users/togunyale/eclipse-workspace/NBA_Data/chromedriver", chrome_options=options)
        driver.get(homeUrl)
        sleep(1) 
        
        search = driver.find_elements_by_xpath('/html/body/div[2]/div[1]/div[3]/form/div/div/input[2]')[0]
        search.send_keys(Player)
        driver.execute_script("arguments[0].click();",driver.find_elements_by_xpath('/html/body/div[2]/div[1]/div[3]/form/input[1]')[0])
        
        wt_ht = 0
        teamCheck = 0
        usage = 0
        tot_ast = 0
        mp = 0
        Rate_ft = 0
        Rate_3pt = 0
        tot_pf = 0
        age = 0
        tot_block = 0
        
        
        if team in name_excepts.keys():
            teamCheck = name_excepts[team]
        else :
            teamCheck = team
        
        if driver.find_elements_by_class_name('search-item-url'):
                    
            driver2 = webdriver.Chrome("/Users/togunyale/eclipse-workspace/NBA_Data/chromedriver", chrome_options=options)
            driver2.get(homeUrl+driver.find_elements_by_class_name('search-item-url')[0].text)
            
            sleep(1)
            
            for p in driver2.find_elements_by_tag_name('p'):
                if 'cm' in p.text:
                    wt_ht = p.text 
                    break
                
            totals_table = driver2.find_elements_by_id('totals.2019') 
            
            for stat_line in totals_table:
                if stat_line.find_elements_by_tag_name('td')[1].text == teamCheck:
                    tot_pf = stat_line.find_elements_by_tag_name('td')[27].text
                    age = stat_line.find_elements_by_tag_name('td')[0].text
                    tot_block = stat_line.find_elements_by_tag_name('td')[25].text 
            
            advance_table = driver2.find_elements_by_id('advanced.2019')
            
            for stat_line in advance_table:
                if stat_line.find_elements_by_tag_name('td')[1].text == teamCheck:
                    usage = stat_line.find_elements_by_tag_name('td')[17].text
                    tot_ast = stat_line.find_elements_by_tag_name('td')[13].text
                    mp = stat_line.find_elements_by_tag_name('td')[5].text
                    Rate_3pt = stat_line.find_elements_by_tag_name('td')[8].text
                    Rate_ft = stat_line.find_elements_by_tag_name('td')[9].text
            
            driver2.close()
            driver.close()
            return str(Player) + " : " + str(team) + " : " +str(age)+" : " + extractHtAndWt(wt_ht) + " : " + str(usage) + " : " + str(tot_ast) + " : " + str(mp) + " : " + str(Rate_3pt) + " : "+str(Rate_ft) + " : " + str(tot_pf) +  " : " + str(tot_block) 
            # player - team - age - wt-ht - uasage - assist rate - total minutes played - 3pt rate - freethrow rate  - total foul - bloc 
        else:
            
            for p in driver.find_elements_by_tag_name('p'):
                if 'cm' in p.text:
                    wt_ht = p.text 
                    break
                
            totals_table = driver.find_elements_by_id('totals.2019') 
            
            for stat_line in totals_table:
                if stat_line.find_elements_by_tag_name('td')[1].text == teamCheck:
                    tot_pf = stat_line.find_elements_by_tag_name('td')[27].text
                    age = stat_line.find_elements_by_tag_name('td')[0].text    
                    tot_block = stat_line.find_elements_by_tag_name('td')[25].text
            
            advance_table = driver.find_elements_by_id('advanced.2019')
            
            for stat_line in advance_table:
                if stat_line.find_elements_by_tag_name('td')[1].text == teamCheck:
                    usage = stat_line.find_elements_by_tag_name('td')[17].text
                    tot_ast = stat_line.find_elements_by_tag_name('td')[13].text
                    mp = stat_line.find_elements_by_tag_name('td')[5].text
                    Rate_3pt = stat_line.find_elements_by_tag_name('td')[8].text
                    Rate_ft = stat_line.find_elements_by_tag_name('td')[9].text
                    
            driver.close()      
            return str(Player) + " : " + str(team) + " : " +str(age)+" : " + extractHtAndWt(wt_ht) + " : " + str(usage) + " : " + str(tot_ast) + " : " + str(mp) + " : " + str(Rate_3pt) + " : "+str(Rate_ft) + " : " + str(tot_pf) +  " : " + str(tot_block) 
            # player - team - age - wt-ht - uasage - assist rate - total minutes played - 3pt rate - freethrow rate  -total foul 
    except Exception as e:
        raise e
def extractHtAndWt(data):  
    data = data.split('(')[1]   
    ht = data.split('cm, ')[0]
    wt = data.split('cm, ')[1]  
    wt = wt.split('kg')[0] 
    return str(ht) + " : " + str(wt) 

if __name__ == '__main__':
    main() 
