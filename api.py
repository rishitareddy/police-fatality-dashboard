from flask import Flask, render_template, request, jsonify

from sklearn.cluster import KMeans

import numpy as np
import pandas as pd
import math
import io
from collections import Counter
from collections import OrderedDict
import datetime
import json
import logging

app = Flask(__name__)

dataframe = pd.read_csv('templates/PFDataset2.csv')

attributes = ['Geography','Victim_age','Victim_race','Date_of_Incident','State','Encounter_Type','Victim_gender','Year']

df = pd.DataFrame(data=dataframe, columns = attributes)

Police_Killings_By_PD = pd.read_csv('templates/Police_Killings_By_PD.csv')

attributes_by_pd = ['City','Avg_Annual_Police_Homicide_Rate','Violent_Crime_Rate']

df_PdKillings = pd.DataFrame(data=Police_Killings_By_PD, columns = attributes_by_pd)

pf3 = pd.read_csv('templates/PFDataset3.csv')


@app.route('/')
def home():

    return render_template('index.html')
#
# @app.route('/kmeans-labels', methods=['GET'])
# def getKmeansClusters():
#     clusterDict={}
#     kmLabels = KMeans(n_clusters = 3).fit(df).labels_
#     clusterDict["clusters"] = kmLabels.tolist()
#     return jsonify(clusterDict)

@app.route('/top10states',methods =['GET'])
def  get_states():

    list1 = df['State'].tolist()
    c = Counter(list1)

    popular = c.most_common(10)

    data = {}
    data["data"] = []
    data["states"] = []
    data["killingcount"] = []
    top10_states = [popular[0] for popular in c.most_common(10)]
    data["states"] = top10_states
    top10_killings = [popular[1] for popular in c.most_common(10)]
    data["killingcount"] = top10_killings
    for i in range(len(top10_states)):
        temp = {}
        temp['state'] = top10_states[i]
        temp['killingcount'] = top10_killings[i]
        data["data"].append(temp)

    jsonify(data)
    return(data)

@app.route('/areachart',methods = ['GET'])
def getStackedData():
    groupedData = df.groupby(['Year', 'Victim_race']).size().reset_index(name="Count")
    pivotedData = groupedData.pivot('Year', 'Victim_race', 'Count')
    print(pivotedData)
    print(pivotedData.to_json())
    return pivotedData.to_json()

@app.route("/most_common_states", methods=['GET'])
def getMostCommonStates():
    stateList = df['State'].tolist()
    stateDict = dict(Counter(stateList).most_common(10))
    return stateDict

@app.route("/sorted_killings_by_pd", methods=['GET'])
def getSortedHomicideRates():
    df.columns=df.columns.str.strip()
    sorted_killings_by_pd = df_PdKillings.sort_values(by=['Violent_Crime_Rate'],ascending=False)
    sliced_sorted_killings = sorted_killings_by_pd.head(25).to_dict()
    # sliced_sorted_killings = sliced_sorted_killings.append(sorted_killings_by_pd.tail(10)).to_dict()
    scatterplot_dict = {}
    scatterplot_dict["homicide_rate"] = list(sliced_sorted_killings['Avg_Annual_Police_Homicide_Rate'].values())
    scatterplot_dict["city"] = list(sliced_sorted_killings['City'].values())
    scatterplot_dict["violent_crime_rate"] = list(sliced_sorted_killings['Violent_Crime_Rate'].values())

    print(scatterplot_dict)
    return jsonify(scatterplot_dict)


@app.route("/get_top_pd",methods = ['POST','GET'])
def getTopPD(): 
    state = 'TX'
    race = 'White'
    if request.method == 'POST':
        val = json.loads(request.data)
        state = val['state']
        race = val['race']
        # t = 0

    if state != "":
        print("In state ", state)
        attributes = ['State_Full','Agency_responsible_for_death', 'Year']
        df3 = pd.DataFrame(data=pf3, columns = attributes)
        pdDf = df3.loc[df3['State_Full'] == state]
    elif race != "":
        print("In race ", race)
        attributes = ['Victim_race','Agency_responsible_for_death', 'Year']
        df3 = pd.DataFrame(data=pf3, columns = attributes)
        pdDf = df3.loc[df3['Victim_race'] == race]
    # else:
    #     t = 1
    #     attributes = ['Agency_responsible_for_death', 'Year']
    #     pdDf = pd.DataFrame(data=pf3, columns = attributes)

    groupedData = pdDf.groupby(['Agency_responsible_for_death']).size().reset_index(name = "Count")
    sortedKillingsByPD = groupedData.sort_values(by=['Count'],ascending=False).head(5)
    topPD = sortedKillingsByPD['Agency_responsible_for_death'].tolist()

    pdDf = pdDf.loc[pdDf['Agency_responsible_for_death'].isin(topPD)]

    # if t! = 1:
    groupedData = pdDf.groupby(['Agency_responsible_for_death','Year']).count().unstack(0).fillna(0).reset_index()
    year = groupedData['Year'].tolist()

    # else:
    #     groupedData = pdDf.groupby(['Agency_responsible_for_death']).count().unstack(0).fillna(0).reset_index()

    groupedData = pdDf.groupby(['Year','Agency_responsible_for_death']).count().unstack(0).fillna(0).reset_index()

    print(groupedData)

    data = []
    i = 0
    max_count = 0

    for i in range(len(topPD)):
        a_dict = {}
        a_dict["name"] = topPD[i]
        values =  []
        j = 0
        for j in range(len(year)):
            y_dict = {}
            y_dict["date"] = year[j]
            if state != "":
                y_dict["count"] = int(groupedData.iloc[i]['State_Full'].iloc[j])
            elif race != "":
                y_dict["count"] = int(groupedData.iloc[i]['Victim_race'].iloc[j])
            values.append(y_dict)

            if max_count < y_dict["count"]:
                max_count = y_dict["count"]
            j += 1
        a_dict["values"] = values
        data.append(a_dict)
        i += 1

    

    data_dict = {}
    data_dict["multi"] = data
    data_dict["extent"] = max_count
    if state != "":
        data_dict["variable"] = state
    elif race != "":
        data_dict["variable"] = race
        
    print(data)

    return jsonify(data_dict)

if __name__ == '__main__':
    app.run(debug=True, port = 5299)
