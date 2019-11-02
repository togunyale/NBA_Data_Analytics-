'''
Created on Oct 26, 2019

@author: togunyale
'''
import mysql.connector
import os

sql = ' INSERT INTO nba_player_data_2018_2019' 
sql = sql + '(Player,Team,Age,Height,Weight,UsageRate,AssistRate,'
sql = sql +'MinutesPlayed,ThreePtRate,FreeThrowRate,TotalFouls,TotalBlocks,OffensiveRebound3,OffensiveRebound2,'
sql = sql + 'DefensiveRebound3,DefensiveRebound2)'
sql = sql + ' VALUES ( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
# player - team - age - wt-ht - uasage - assist rate - total minutes played - 3pt rate - freethrow rate  - total foul - bloc 

cnx = mysql.connector.connect(
        user='root', 
        password='Packerkill26',
        host='localhost',
        database='playByPlay_3ptReb')
cnx.autocommit = True
cursor = cnx.cursor(buffered=True)

dataFolder = '/Users/togunyale/eclipse-workspace/ReboundingProject/playerstats'
count = 0
for filename in os.listdir(dataFolder):
        if filename == '.DS_Store':
            continue
        openFile = open(dataFolder + "/" + filename,'r')
        playByplay = openFile.readlines()[0].split(' : ')
        #cursor.execute(sql,[])
        try:
            #cursor.execute(sql,playByplay)
            a = 1
        except:
            print playByplay
            continue
        
        cnx.commit()