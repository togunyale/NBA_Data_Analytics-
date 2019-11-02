'''
Created on Oct 19, 2019

@author: togunyale
'''

import mysql.connector

cnx = mysql.connector.connect(
        user='root', 
        password='Packerkill26',
        host='localhost',
        database='playByPlay_3ptReb')
cnx.autocommit = True
cursor = cnx.cursor(buffered=True)

sql = ' INSERT INTO nba_player_data_2018_2019' 
sql = sql + '(Player,Team,Height,Weight,UsageRate,AssistRate,'
sql = sql +'MinutesPlayed,ThreePtRate,FreeThrowRate,OffensiveRebound3,OffensiveRebound2,'
sql = sql + 'DefensiveRebound3,DefensiveRebound2)'
sql = sql + ' VALUES ( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
with open('/Users/togunyale/eclipse-workspace/ReboundingProject/insertIntoMySql/playerData.txt','r') as f:
    for lines in f:
        
        stat = lines.split(' : ')
        if 'ATL' in stat:
            print lines
        for x in xrange(len(stat)):
            if not stat[x]:
                stat[x] = 0
        data = [stat[0],stat[1],stat[2],stat[3],stat[4],stat[5],stat[6],stat[7],stat[8],stat[9],stat[10],stat[11],stat[12]] 
        #cursor.execute(sql,data)
        #cnx.commit()
        