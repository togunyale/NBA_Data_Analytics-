'''
Created on Oct 21, 2019

@author: togunyale
'''

import pandas as pd  
import numpy as np  
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

raw_data = pd.read_csv('/Users/togunyale/eclipse-workspace/ReboundingProject/DataSets/dataset_2019_10_26.csv')
dataset = raw_data.copy()

modelMeasure = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
epoch = 100
for x in xrange(0,epoch):
    dataset = dataset.reindex(np.random.permutation(dataset.index))
    Y_values = ['OR2_per48','DR2_per48','OR3_per48','DR3_per48']
    
    
    features = dataset[['Age','Height' , 'Weight', 'UsageRate' , 'AssistRate' , 'ThreePtRate' , 'FreeThrowRate' , 'TotalFouls',
'TotalBlocks']]
    for values in xrange(len(Y_values)):
        
        label = dataset[[Y_values[values]]]
        
        train_ft , test_ft , train_lb , test_lb = train_test_split(features, label, test_size=0.2, random_state=0, shuffle=False)
        
        regressor = LinearRegression() 
        regressor.fit(train_ft,train_lb)
        
        label_predict = regressor.predict(test_ft)
        
        act_vs_predict = pd.DataFrame()
        act_vs_predict['Actial'] = test_lb[Y_values[values]]
        act_vs_predict['Prediction'] = label_predict
        
        modelMeasure[values][0] += metrics.mean_absolute_error(test_lb, label_predict)
        modelMeasure[values][1] += metrics.mean_squared_error(test_lb, label_predict)
        modelMeasure[values][2] += np.sqrt(metrics.mean_squared_error(test_lb, label_predict))
        
       
    
for values in xrange(len(Y_values)):     
    print "Dependent variable : " + Y_values[values]
    print'Mean Absolute Error :' + str(modelMeasure[values][0]/epoch) 
    print'Mean Squared Error : ' + str(modelMeasure[values][1]/epoch) 
    print'Root Mean Squared Error: ' + str(modelMeasure[values][2]/epoch)
    print " --------------------------------------------"

