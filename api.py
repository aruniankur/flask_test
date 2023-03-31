from flask import Flask, request, jsonify
from flask import Flask
from flask_cors import CORS
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import secrets
import random

app = Flask(__name__)
CORS(app)

df2 = pd.read_csv("sheet_with_lat_long.csv")
lst = {"type":'Ayu','id_country':0,"id_state":0}

@app.route("/setfinal",methods = ['GET'])
def setfinal():
    def searchforcountry(cate):
        response_data = {}
        if (cate['id_country'] == 0):
            df = pd.read_csv("dataforcountry.csv")
            df = df[df['category'] == cate['type']]
            df = df.drop_duplicates()
            response_data = {}
            for i in range(len(df)):
                saw2 = list(df.iloc[i,3:])
                for j in range(3,len(saw2)):
                    saw2[j] = int(saw2[j])
                saw =  df.iloc[i,1]
                response_data[saw] = saw2
        elif (cate['id_state'] == 0):
            df = pd.read_csv("dataforstate.csv")
            df = df[(df['category'] == cate['type']) & (df['id_country'] == int(cate['id_country']))]
            df = df.drop_duplicates()
            response_data = {}
            for i in range(len(df)):
                saw2 = list(df.iloc[i,3:])
                for j in range(3,len(saw2)):
                    saw2[j] = int(saw2[j])
                saw =  df.iloc[i,1]
                response_data[saw] = saw2
        else :
            df = pd.read_csv("dataforcity.csv")
            df = df[(df['category'] == cate['type']) & (df['id_state'] == int(cate['id_state']))]
            df = df.drop_duplicates()
            response_data = {}
            for i in range(len(df)):
                saw2 = list(df.iloc[i,3:])
                for j in range(3,len(saw2)):
                    saw2[j] = int(saw2[j])
                saw =  df.iloc[i,1]
                response_data[saw] = saw2
        return response_data
    print(lst)
    response_data = searchforcountry(lst)
    #print(response_data)
    return jsonify(response_data)


@app.route("/finalsend", methods=["POST"])
def handle_selected_values():
    selected_values = request.get_json()
    # Do something with the selected values
    #print(selected_values)
    global lst
    lst['id_state'] = selected_values['id_state']
    #print("this is a code")
    response_data = lst
    return jsonify(response_data)



@app.route("/getstate", methods=["POST"])
def getstate():
    selected_values = request.get_json()
    #print(selected_values)
    def searchstate(df,w):
        w = int(w['id_country'])
        df2 = df[df['id_country'] == w]
        df2 = df2[['State','id_state']]
        df2 = df2.drop_duplicates()
        response_data = {'State': list(df2['State']), 'id_state': list(df2['id_state'])}
        return response_data
    global lst
    lst["id_country"] = selected_values['id_country']
    #print(lst)
    response_data = searchstate(df2, selected_values)
    return jsonify(response_data)
    
@app.route("/getcity", methods=["POST"])
def getcity():
    selected_values = request.get_json()
    #print(selected_values)
    def searchstate(df,w):
        w = int(w['id_state'])
        df2 = df[df['id_state'] == w]
        df2 = df2[['City','id_city']]
        df2 = df2.drop_duplicates()
        response_data = {'State': list(df2['City']), 'id_state': list(df2['id_city'])}
        return response_data
    # global lst
    # lst["id_country"] = selected_values['id_country']
    #print(lst)
    response_data = searchstate(df2, selected_values)
    return jsonify(response_data)
    
@app.route("/getcountry", methods=["POST"])
def getcountry():
    def searchcountry(df):
        df2 = df[['Country','id_country']]
        df2 = df2.drop_duplicates()
        response_data = {'Country': list(df2['Country']), 'id_country': list(df2['id_country'])}
        return response_data
    global lst
    lst = {"type":'Ayu','id_country':0,"id_state":0}
    selected_values = request.get_json()
    #print(selected_values)
    lst["type"] = selected_values['type']
    response_data = searchcountry(df2)
    return jsonify(response_data);

@app.route('/backend', methods=['POST'])
def handle_post_request():
    print('qw')
    data = request.get_json()
    #print(data)
    # do something with the data, such as save it to a database
    response_data = {'message': 'Data received successfully.'}
    return jsonify(response_data)



@app.route('/forspechos', methods=['POST'])
def handlespecforhos():
    data = request.get_json()
    #print(data)
    def creator(sw):
        count = int(sw[list(sw.keys())[0]])
        lst = sw[list(sw.keys())[1]]
        response_data = {}
        for i in range(1,count+1):
            response_data['city'+str(i)] = {'lst' : lst,
                                'cou' : [int(i) for i in list(np.random.randint(0, 20, size= len(lst)))],
}
        return response_data
    # do something with the data, such as save it to a database
    response_data = creator(data)
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)