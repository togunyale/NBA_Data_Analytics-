'''
Created on Oct 20, 2019

@author: togunyale
'''
from selenium import webdriver
import mysql.connector
from time import sleep
import datetime
from pathlib import Path
import os

dataFolder = '/Users/togunyale/eclipse-workspace/ReboundingProject/playbyplaydata'
missFolder = '/Users/togunyale/eclipse-workspace/ReboundingProject/missedshotdata/missedLog.txt'

def main():
    insertMissedShots()

def gatherMissedShots():
    
    teamOff3 = dict()
    teamOff2 = dict()
    misslog = open(missFolder,'a')
    misslog.write('Team:Off2:Off3' + "\n")
    for filename in os.listdir(dataFolder):
        openFile = open(dataFolder + "/" + filename,'r')
        playByplay = openFile.readlines()
        
        for play in xrange(len(playByplay) - 1):
            if 'miss' in playByplay[play] or 'blocks' in playByplay[play]:
                if 'free' not in playByplay[play]:
                    if 'three' in playByplay[play]:
                        print playByplay[play]
                        if playByplay[play].split(" :: ")[0] in teamOff3:
                            teamOff3[playByplay[play].split(" :: ")[0]] += 1
                        else :
                            teamOff3[playByplay[play].split(" :: ")[0]] = 1
                        
                    else :
                        print playByplay[play]
                        print playByplay[play].split(" :: ")[0]    
                        if playByplay[play].split(" :: ")[0] in teamOff2:
                            teamOff2[playByplay[play].split(" :: ")[0]] += 1
                        else :
                            teamOff2[playByplay[play].split(" :: ")[0]] = 1
                                            
    for key in teamOff2:
        print key +":"+ str(teamOff2[key])+ ":" + str(teamOff3[key])
        misslog.write(key +":"+ str(teamOff2[key])+ ":" + str(teamOff3[key]) +"\n")
                      
    misslog.close()

def insertMissedShots():
    cnx = mysql.connector.connect(
        user='root', 
        password='Packerkill26',
        host='localhost',
        database='playByPlay_3ptReb')
    cnx.autocommit = True
    cursor = cnx.cursor(buffered=True)
    
    sql = ' INSERT INTO nba_team_data_missed_shots_2018_2019 (Team,Missed_2s,Missed_3s,Total_Mins_Played)'
    sql = sql + 'VALUES ( %s , %s , %s , %s);'
    
    counter = 0
    with open(missFolder, 'r') as f1:
        for lines in f1:
            if counter == 0 :
                counter = 1
                continue
            data = lines.split(':')
            print lines
            cursor.execute(sql, [data[0],data[1],data[2], (1230*48)])
    
    
if __name__ == '__main__':
    main()
    