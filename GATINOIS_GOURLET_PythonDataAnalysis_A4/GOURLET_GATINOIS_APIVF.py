# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 17:37:47 2020

@author: katel
"""
# Python for data analysis
# Marion GATINOIS and Katell GOURLET
# ESILV A.4 DIA.1

# PART 1 : API :
    
#sur anaconda prompt
#conda install -c anaconda flask (ou peut être juste pip install flask)
#pip install flask_wtf

from flask import Flask
from flask import render_template
from flask import request
from flask_script import Manager
from flask_bootstrap import Bootstrap

app = Flask(__name__, template_folder="templatesForms") 
manager = Manager(app)
bootstrap = Bootstrap(app)

app.config["SECRET_KEY"] = "katellmarion"
    
@app.route('/')
def test():
    return render_template("forms.html")

@app.route('/results/', methods=['GET', 'POST'])
def results():

    dicoRep = {}

    if request.method == "POST":
        #Ligne 1
        name = request.form['name']
        
        #Ligne 2
        n_tokens_title = request.form['n_tokens_title']
        if(n_tokens_title != ''):
            dicoRep.update({" n_tokens_title":n_tokens_title})
        
        
        #Ligne 3
        n_tokens_content = request.form['n_tokens_content']
        if(n_tokens_content != ''):
            dicoRep.update({" n_tokens_content":n_tokens_content})
            
        #Ligne 4
        num_imgs = request.form['num_imgs']
        if(num_imgs!= ''):
            dicoRep.update({" num_imgs":num_imgs})

        #Ligne 6 -> 11 : Radio Button        
        data_channel = request.form['data_channel']
        if(data_channel == 'option1'):
            dicoRep.update({" data_channel_is_lifestyle":1})
        else:
            dicoRep.update({" data_channel_is_lifestyle":0})
            
        if(data_channel == 'option2'):
            dicoRep.update({" data_channel_is_entertainment":1})
        else:
            dicoRep.update({" data_channel_is_entertainment":0})
            
        if(data_channel == 'option3'):
            dicoRep.update({" data_channel_is_bus":1})
        else:
            dicoRep.update({" data_channel_is_bus":0})
            
        if(data_channel == 'option4'):
            dicoRep.update({" data_channel_is_socmed":1})
        else:
            dicoRep.update({" data_channel_is_socmed":0})
            
        if(data_channel == 'option5'):
            dicoRep.update({" data_channel_is_tech":1})
        else:
            dicoRep.update({" data_channel_is_tech":0})
            
        if(data_channel == 'option6'):
            dicoRep.update({" data_channel_is_world":1})
        else:
            dicoRep.update({" data_channel_is_world":0})
            
        #Ligne 5 : option
        weekday = request.form['weekday']
        if(weekday != ''):
            stringweekday = str(' is_'+weekday)
            dicoRep.update({stringweekday:1})


    print("Your answers :")
    print(dicoRep)
    
    dfdico = pd.DataFrame(dicoRep, index=[0])
    print(dfdico)
    
    # We are going to use only the colum we ask for the form
    dfPop=pd.read_csv('OnlineNewsPopularity.csv')
    dfPop.drop(dfPop.iloc[:,39:60], inplace=True, axis=1)
    dfPop.drop(dfPop.iloc[:,19:38], inplace=True, axis=1)
    dfPop.drop(dfPop.iloc[:,10:13], inplace=True, axis=1)
    dfPop.drop(dfPop.iloc[:,4:9], inplace=True, axis=1)
    dfPop.drop(dfPop.iloc[:,0:2], inplace=True, axis=1)

    RFClass = modelTrain(dfPop)
         
    computeResult = resultat(RFClass, dfdico)
    
    if(computeResult):
        rep = "Congratulation, your article is going to be very successful !"
    else:
        rep = "Sorry but your article is not ready to be popular, according to our prediction...Improuve it and try again !"
    
    print(rep)

    return render_template("results.html", rep = rep, name= name, answer = dicoRep )
   

#pip install sklearn
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
    
def modelTrain(dfPop):
    
    print("The modelisation is starting") 
    
    Y = dfPop[' shares']
    X = dfPop.drop(columns=[' shares'])
    
    #=> Random Forest Classification 
    #The mean of all share : 3395.3801836343455 
    #We transformed the task into a binary task using a decision threshold of 3395, approximatly the mean :
    mean = 3395
    
    #True : popular
    #False : unpopular
    YClass = []
    for i in range (0,len(Y)):
        if Y[i]>mean :
            YClass.append(True)
        else:
            YClass.append(False)

    #Create a Gaussian Classifier
    RFClass = RandomForestClassifier()
    #Train the model using the training sets 
    RFClass.fit(X,YClass)
    
    print("The modelisation is complete")
    
    return RFClass
    

def resultat(RFClass, toPredict):

    # prediction on test set
    Ypred = RFClass.predict(toPredict)
    print(Ypred)
    
    return Ypred


if __name__ == "__main__":

    #Launch our Website
    print("Launch :")
    app.run()
    
    
