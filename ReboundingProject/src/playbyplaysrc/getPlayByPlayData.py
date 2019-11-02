'''
Created on Oct 16, 2019

@author: togunyale
'''

from selenium import webdriver
from time import sleep
import datetime
from pathlib import Path
import os

orginUrl = 'https://www.espn.com/nba/playbyplay?gameId='
gameIds = list()
dataFolder = '/Users/togunyale/eclipse-workspace/ReboundingProject/playbyplaydata'



def main():
    consecutive_error_counter = 0
    #Iterate GameIds.txt and them to a list for all gameids in the 2018-2019 NBA Season - According to ESPN.com
    #  401070213 401070223  (401070233 - 401070240)  -- (401070693 - 401071903)
    for x in xrange(401070213,401070224,1): 
        gameIds.append(str(x))
    for x in xrange(401070233,401070241,1): 
        gameIds.append(str(x))
    for x in xrange(401070693,401071904,1): 
        if x == 401070856:
            continue
        gameIds.append(str(x))
        
    for games in gameIds:
        #/Users/togunyale/eclipse-workspace/ReboundingProject/data
        insertErrorLog = open ('/Users/togunyale/eclipse-workspace/ReboundingProject/logs/InsertErrorLog.txt', 'a')
        insertLog = open ('/Users/togunyale/eclipse-workspace/ReboundingProject/logs/InsertLog.txt', 'a')
        if Path('/Users/togunyale/eclipse-workspace/ReboundingProject/data/GameId'+games).is_file():
            print "Already Completed " + orginUrl+games + " File Already Exists"
            insertLog.write( "Already Completed " + orginUrl+games + " File Already Exists" +'\n')
            continue 
        
        try:
            #Selenium Handling 
            options = webdriver.ChromeOptions()
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--incognito')
            options.add_argument('--headless')
            driver = webdriver.Chrome("/Users/togunyale/eclipse-workspace/NBA_Data/chromedriver", chrome_options=options)
            driver.get(orginUrl+games)
            sleep(5)
            
            # Quarter Determining Handling 
            lastqtr = False 
            qtrs = 2 
            
            # Loop #2 through all the quarters in the game & Press the expand button -- Stop when all the Quarters are accounted for 
            while  not lastqtr:
                if driver.find_elements_by_xpath('//*[@id="gamepackage-qtrs-wrap"]/ul/li['+ str(qtrs)+']/div[1]/a') :
                    driver.execute_script("arguments[0].click();",driver.find_elements_by_xpath('//*[@id="gamepackage-qtrs-wrap"]/ul/li['+str(qtrs)+']/div[1]/a')[0])
                    qtrs += 1
                else :
                    lastqtr = True
            
            # Loop # 3 through all the Quarters 
            for quarter in range(1,qtrs,1):
                
                # Gather the table that contains the information for the quarter 
                quater_current = driver.find_element_by_xpath('//*[@id="gp-quarter-'+str(quarter)+'"]/table/tbody')
                plays = quater_current.find_elements_by_tag_name('tr')
                
                
                # Loop 4 --- go through all the plays per quarter
                gameData = open('/Users/togunyale/eclipse-workspace/ReboundingProject/data/GameId'+games,'a')
                for play in range(len(plays)):
                    
                    team = plays[play].find_elements_by_tag_name('td')[1].find_elements_by_tag_name('img')[0].get_attribute('src').encode().split("/")[9].split('.')[0].upper()   

                    gameData.write(team + " :: "+plays[play].find_elements_by_tag_name('td')[2].text+"\n")
                    
                            
        except Exception as e:
            print "Error!!"
            insertErrorLog.write(str(datetime.datetime.now()) + " : Error At : " + orginUrl+games + "     ---- " + str(e) + "\n")
            driver.close()
            consecutive_error_counter += 1
            
            if consecutive_error_counter > 5 :
                insertErrorLog.write(str(datetime.datetime.now()) + " --> TOO MANY CONSECUTIVE ERRORS " + "\n")
                insertErrorLog.close()
                break
            else:
                insertErrorLog.close() 
                continue 
        insertLog.write( "Completed :: " + orginUrl+games +'\n')
        print "Completed :: " + orginUrl+games 
        insertErrorLog.close()
        insertLog.close()
        driver.close()
        
if __name__ == '__main__':
    main()