#uvicorn main:app --reload
from typing import Optional
from urllib import response

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

import pickle

#import model prediction elements
import os
import sklearn
import pandas

#load website elements
import json

#load model
with open('model_pickle', 'rb') as f:
    newGrid = pickle.load(f)
#load test set with wrong predictions
with open('wrongValues_pickle', 'rb') as f:
    wrongValues = pickle.load(f)
#load transform pipeline
with open('full_pipeline_pickle', 'rb') as f:
    full_pipeline = pickle.load(f)
#load encoder for transform
with open('target_encoder_pickle', 'rb') as f:
    target_encoder = pickle.load(f)
#load original logs used to train model
with open('logs', 'rb') as f:
    original_logs = pickle.load(f)
#load test set of logs
with open('test_logs', 'rb') as f:
    test_logs = pickle.load(f)

with open('testLogs/newLogs', 'rb') as f:
    newLogs = pickle.load(f)


#testTail = newLogs.iloc[0]
#print(testTail.name)
#print(testTail)
#print(len(testTail))
#print(testTail.index[0])
#print(testTail[0])

#start tbe server
app = FastAPI()

#dashboard entry point
@app.get("/", response_class=HTMLResponse)
def read_root():
    html_content= """
        <html>
            <head>
                <title>dashboard</title>
                <meta name="viewport" content="width=device-width, initial-scale=1">
            </head>
            <style>

                #topBox {
                    display: flex;
                    flex-direction: row;
                    justify-content: space-around;
                    width:100%;
                    margin-bottom:20px;
                }
                #charts {
                    display:flex;
                    flex-direction: row;
                    width: 50%;
                    justify-content: space-around;
                }
                #ratioText{
                    text-align:center;
                }
                #accuracyText {
                    text-align: center;
                }
                #stats {
                    display:flex;
                    flex-direction: column;
                    justify-content: space-evenly;
                    width: 50%;
                }
                #attackNumber {
                    text-align: center;
                }
                #wrongPredictions {
                    text-align: center;
                }

                #main {
                    display:flex;
                    flex-direction: column;
                    justify-content: space-evenly;
                    width: 100%;
                }

                #logBox {
                    display: flex;
                    justify-self: center;
                    max-height: 300px;
                    overflow-x: auto;
                    overflow-y: auto;

                }
                .title {
                    width:100%
                    justify-content: center;
                    text-align: center;
                }
                #newLogBox {
                    display: flex;
                    justify-self: center;
                    max-height: 300px;
                    overflow-x: auto;
                    overflow-y: auto;
                }

                .tooltiptext {
                    visibility: hidden;
                    width: 120px;
                    background-color: black;
                    color: #fff;
                    text-align: center;
                    border-radius: 6px;
                    padding: 5px 0;
                    
                    /* Position the tooltip */
                    position: absolute;
                    z-index: 1;
                    top: 100%;
                    left: 50%;
                    margin-left: -60px;
                }
                .tooltip:hover .tooltiptext {
                    visibility: visible;
                }
                .tooltip {
                    position: relative;
                }
                table, th, td {
                    border: 1px solid grey;
                    border-collapse: collapse;
                    font-size: 20px;
                }
                th {
                    background-color: orange;
                }

                tr {
                    text-align: center;
                    vertical-align: text-top;
                }

                .normal {
                    text-align: center;
                    vertical-align: text-top;
                    background-color: #8cff8c;
                }
                .malicious {
                    text-align: center;
                    vertical-align: text-top;
                    background-color: #ff7979;
                }



                @property --p{
                syntax: '<number>';
                inherits: true;
                initial-value: 1;
                }

                .pie {
                --p:20;      /* the percentage */
                --b:30px;    /* the thickness */
                --c:darkred; /* the color */
                --w:200px;   /* the size*/
                
                width:var(--w);
                aspect-ratio:1/1;
                position:relative;
                display:inline-grid;
                margin:5px;
                place-content:center;
                font-size:25px;
                font-weight:bold;
                font-family:sans-serif;
                }
                .pie:before,
                .pie:after {
                content:"";
                position:absolute;
                border-radius:50%;
                }
                .pie:before {
                inset:0;
                background:
                    radial-gradient(farthest-side,var(--c) 98%,#0000) top/var(--b) var(--b) no-repeat,
                    conic-gradient(var(--c) calc(var(--p)*1%),#0000 0);
                -webkit-mask:radial-gradient(farthest-side,#0000 calc(99% - var(--b)),#000 calc(100% - var(--b)));
                        mask:radial-gradient(farthest-side,#0000 calc(99% - var(--b)),#000 calc(100% - var(--b)));
                }
                .pie:after {
                inset:calc(50% - var(--b)/2);
                background:var(--c);
                transform:rotate(calc(var(--p)*3.6deg - 90deg)) translate(calc(var(--w)/2 - 50%));
                }
                .animate {
                animation:p 1s .5s both;
                }
                .no-round:before {
                background-size:0 0,auto;
                }
                .no-round:after {
                content:none;
                }
                @keyframes p{
                from{--p:0;}
                }
            </style>
            <body onload="makeRequest()">
                
                <!--<input id="input1">
                <input id="input2">
                <button id="button1" onclick="doStuff()">press me</button>
                <button id="button2" onclick="wrongPredictions()">Wrong Predictions</button>
                <button id="button3" onclick="ratio()">Ratio</button>
                <button id="button4" onclick="accuracy()">Accuracy</button>
                <button id="button5" onclick="attackNumber()">AttackNumber</button>
                -->
                <div id="topBox">
                    <div id="charts">
                        <div id="ratioBox">
                            <div id="ratio" class="pie animate" style="--p:0;--c:orange;"></div>
                            <div id="ratioText">Percentage of attacks</div>
                        </div>
                        <div id="accuracyBox">
                            <div id="accuracy" class="pie animate" style="--p:80;--c:orange;"></div>
                            <div id="accuracyText">Model prediction accuracy</div>
                        </div>
                    </div>
                    <div id="stats">
                        <div id="attackNumber"></div>
                        <div id="wrongPredictions"></div>
                    </div>
                </div>
                <div class="title">
                <h1>Recent predictions</h1>
                </div>
                <div id="main">
                
                    <div id="logBox">
                        <table id="logs">
                            <thead>
                                <tr>
                                    <th class="tooltip">dur<span class="tooltiptext">duration</span></th>
                                    <th class="tooltip">protocol<span class="tooltiptext">protocol type</span></th>
                                    <th class="tooltip">service<span class="tooltiptext">service</span></th>
                                    <th class="tooltip">flag<span class="tooltiptext">flag</span></th>
                                    <th class="tooltip">src_b<span class="tooltiptext">number of source bytes</span></th>
                                    <th class="tooltip">dst_b<span class="tooltiptext">number of destination bytes</span></th>
                                    <th class="tooltip">land<span class="tooltiptext">is the connection from the same host; 1-yes, 0-no</span></th>
                                    <th class="tooltip">frag<span class="tooltiptext">number of wrong fragments</span></th>
                                    <th class="tooltip">ur<span class="tooltiptext">number of urgent packets</span></th>
                                    <th class="tooltip">hot<span class="tooltiptext">number of hot indicators</span></th>
                                    <th class="tooltip">fail<span class="tooltiptext">number of failed login attempts</span></th>
                                    <th class="tooltip">logg<span class="tooltiptext">is the connection logged in; 1-yes, 0-no</span></th>
                                    <th class="tooltip">num_c<span class="tooltiptext">number of compromised conditions</span></th>
                                    <th class="tooltip">r_shell<span class="tooltiptext">is root shell obtained; 1-yes, 0-no</span></th>
                                    <th class="tooltip">su<span class="tooltiptext">is "su root" command attempted; 1-yes, 0-no</span></th>
                                    <th class="tooltip">root<span class="tooltiptext">number of "root" accesses</span></th>
                                    <th class="tooltip">create<span class="tooltiptext">number of file creation operations</span></th>
                                    <th class="tooltip">shells<span class="tooltiptext">number of shell prompts</span></th>
                                    <th class="tooltip">a_files<span class="tooltiptext">number of operations to access control files</span></th>
                                    <th class="tooltip">cmds<span class="tooltiptext">number of outbound commands in an ftp session</span></th>
                                    <th class="tooltip">hot_l<span class="tooltiptext">does login belong to "hot" list; 1-yes, 0-no</span></th>
                                    <th class="tooltip">guest<span class="tooltiptext">is it a "gues" login; 1-yes, 0-no</span></th>
                                    <th class="tooltip">count<span class="tooltiptext">number of connections to the same host</span></th>
                                    <th class="tooltip">s_1<span class="tooltiptext">number of connections to the same service</span></th>
                                    <th class="tooltip">s_2<span class="tooltiptext">percentage of connection with "SYN" error</span></th>
                                    <th class="tooltip">s_3<span class="tooltiptext">ratio of serror rate</span></th>
                                    <th class="tooltip">r_1<span class="tooltiptext">percentage of connections with "REJ" error</span></th>
                                    <th class="tooltip">r_2<span class="tooltiptext">ratio of rerror rate</span></th>
                                    <th class="tooltip">r_3<span class="tooltiptext">percentage of connections to the same service</span></th>
                                    <th class="tooltip">d_1<span class="tooltiptext">percentage of connections to different service</span></th>
                                    <th class="tooltip">d_2<span class="tooltiptext">percentage of connections to different hosts</span></th>
                                    <th class="tooltip">d_3<span class="tooltiptext">number of connections to host</span></th>
                                    <th class="tooltip">d_4<span class="tooltiptext">number of connections to host services</span></th>
                                    <th class="tooltip">d_5<span class="tooltiptext">percentage of connections to same service at host</span></th>
                                    <th class="tooltip">d_6<span class="tooltiptext">percentage of connections to different service at host</span></th>
                                    <th class="tooltip">d_7<span class="tooltiptext">percentage of connections to the same port at host</span></th>
                                    <th class="tooltip">d_8<span class="tooltiptext">percentage of connections to different port at host</span></th>
                                    <th class="tooltip">d_9<span class="tooltiptext">percentage of connections with "SYN" error at host</span></th>
                                    <th class="tooltip">d_10<span class="tooltiptext">ratio of serror rate at host </span></th>
                                    <th class="tooltip">d_11<span class="tooltiptext">percentage of connection with "REJ" error at host</span></th>
                                    <th class="tooltip">d_12<span class="tooltiptext">ratio of rerror rate at host</span></th>
                                    <th>STATUS</th>
                                </tr>
                            </thead>
                            <tbody id="recentLogs">
                            </tbody>
                        </table>
                    </div>
                    
                    <div class="title">
                    <h1>New connection logs</h1>
                    </div>

                    <div id="newlogBox">
                        <table id="newlogs">
                            <thead>
                                <tr>
                                    <th class="tooltip">dur<span class="tooltiptext">duration</span></th>
                                    <th class="tooltip">protocol<span class="tooltiptext">protocol type</span></th>
                                    <th class="tooltip">service<span class="tooltiptext">service</span></th>
                                    <th class="tooltip">flag<span class="tooltiptext">flag</span></th>
                                    <th class="tooltip">src_b<span class="tooltiptext">number of source bytes</span></th>
                                    <th class="tooltip">dst_b<span class="tooltiptext">number of destination bytes</span></th>
                                    <th class="tooltip">land<span class="tooltiptext">is the connection from the same host; 1-yes, 0-no</span></th>
                                    <th class="tooltip">frag<span class="tooltiptext">number of wrong fragments</span></th>
                                    <th class="tooltip">ur<span class="tooltiptext">number of urgent packets</span></th>
                                    <th class="tooltip">hot<span class="tooltiptext">number of hot indicators</span></th>
                                    <th class="tooltip">fail<span class="tooltiptext">number of failed login attempts</span></th>
                                    <th class="tooltip">logg<span class="tooltiptext">is the connection logged in; 1-yes, 0-no</span></th>
                                    <th class="tooltip">num_c<span class="tooltiptext">number of compromised conditions</span></th>
                                    <th class="tooltip">r_shell<span class="tooltiptext">is root shell obtained; 1-yes, 0-no</span></th>
                                    <th class="tooltip">su<span class="tooltiptext">is "su root" command attempted; 1-yes, 0-no</span></th>
                                    <th class="tooltip">root<span class="tooltiptext">number of "root" accesses</span></th>
                                    <th class="tooltip">create<span class="tooltiptext">number of file creation operations</span></th>
                                    <th class="tooltip">shells<span class="tooltiptext">number of shell prompts</span></th>
                                    <th class="tooltip">a_files<span class="tooltiptext">number of operations to access control files</span></th>
                                    <th class="tooltip">cmds<span class="tooltiptext">number of outbound commands in an ftp session</span></th>
                                    <th class="tooltip">hot_l<span class="tooltiptext">does login belong to "hot" list; 1-yes, 0-no</span></th>
                                    <th class="tooltip">guest<span class="tooltiptext">is it a "gues" login; 1-yes, 0-no</span></th>
                                    <th class="tooltip">count<span class="tooltiptext">number of connections to the same host</span></th>
                                    <th class="tooltip">s_1<span class="tooltiptext">number of connections to the same service</span></th>
                                    <th class="tooltip">s_2<span class="tooltiptext">percentage of connection with "SYN" error</span></th>
                                    <th class="tooltip">s_3<span class="tooltiptext">ratio of serror rate</span></th>
                                    <th class="tooltip">r_1<span class="tooltiptext">percentage of connections with "REJ" error</span></th>
                                    <th class="tooltip">r_2<span class="tooltiptext">ratio of rerror rate</span></th>
                                    <th class="tooltip">r_3<span class="tooltiptext">percentage of connections to the same service</span></th>
                                    <th class="tooltip">d_1<span class="tooltiptext">percentage of connections to different service</span></th>
                                    <th class="tooltip">d_2<span class="tooltiptext">percentage of connections to different hosts</span></th>
                                    <th class="tooltip">d_3<span class="tooltiptext">number of connections to host</span></th>
                                    <th class="tooltip">d_4<span class="tooltiptext">number of connections to host services</span></th>
                                    <th class="tooltip">d_5<span class="tooltiptext">percentage of connections to same service at host</span></th>
                                    <th class="tooltip">d_6<span class="tooltiptext">percentage of connections to different service at host</span></th>
                                    <th class="tooltip">d_7<span class="tooltiptext">percentage of connections to the same port at host</span></th>
                                    <th class="tooltip">d_8<span class="tooltiptext">percentage of connections to different port at host</span></th>
                                    <th class="tooltip">d_9<span class="tooltiptext">percentage of connections with "SYN" error at host</span></th>
                                    <th class="tooltip">d_10<span class="tooltiptext">ratio of serror rate at host </span></th>
                                    <th class="tooltip">d_11<span class="tooltiptext">percentage of connection with "REJ" error at host</span></th>
                                    <th class="tooltip">d_12<span class="tooltiptext">ratio of rerror rate at host</span></th>
                                    <th class="predict">PREDICT</th>
                                </tr>
                            </thead>
                            <tbody id="newLogs">
                            </tbody>
                        </table>
                    </div>
                </div>
            </body>
            <script>
                function wrongPredictions(){
                    var xhttp = new XMLHttpRequest();
                    xhttp.onreadystatechange = function() {
                        if (this.readyState == 4 && this.status == 200) {
                            wrongStat = document.getElementById("wrongPredictions");
                            wrongStat.innerHTML = "Number of wrong predictions: " + this.responseText;
                        }
                    };
                    xhttp.open("GET", "/wrongPredictions/", true);
                    xhttp.send();
                }
                function accuracy(){
                    var xhttp = new XMLHttpRequest();
                    xhttp.onreadystatechange = function() {
                        if (this.readyState == 4 && this.status == 200) {
                            accuracyPie = document.getElementById("accuracy");
                            var acc = this.responseText*100;
                            acc = acc.toFixed(2);
                            accuracyPie.innerHTML = acc + "%";
                            accuracyPie.style.setProperty("--p", acc);
                        }
                    };
                    xhttp.open("GET", "/accuracy/", true);
                    xhttp.send();
                }
                function attackNumber(){
                    var xhttp = new XMLHttpRequest();
                    xhttp.onreadystatechange = function() {
                        if (this.readyState == 4 && this.status == 200) {
                            attackStat = document.getElementById("attackNumber");
                            attackStat.innerHTML = "Number of attacks: " + this.responseText;
                        }
                    };
                    xhttp.open("GET", "/attackNumber/", true);
                    xhttp.send();
                }
                function ratio(){
                    var xhttp = new XMLHttpRequest();
                    xhttp.onreadystatechange = function() {
                        if (this.readyState == 4 && this.status == 200) {
                            ratioPie = document.getElementById("ratio");
                            var rat = this.responseText*100
                            rat = rat.toFixed(2)
                            ratioPie.innerHTML = rat + "%";
                            ratioPie.style.setProperty("--p", rat);
                        }
                    };
                    xhttp.open("GET", "/ratio/", true);
                    xhttp.send();
                }
                function getRecent() {
                    var xhttp = new XMLHttpRequest();
                    xhttp.onreadystatechange = function() {
                        if (this.readyState == 4 && this.status == 200) {
                            var myArr = JSON.parse(this.responseText);
                            
                            tbody = document.getElementsByTagName("tbody")[0];
                            for(var k in myArr){
                                row = document.createElement("tr");
                                row.setAttribute("id", k);
                                if(myArr[k].target == "normal"){
                                    row.setAttribute("class", "normal");
                                }
                                else{
                                    row.setAttribute("class", "malicious");
                                }
                                for(var n in myArr[k]){
                                    cell = document.createElement("td");
                                    cell.innerHTML = myArr[k][n];
                                    row.appendChild(cell);
                                }


                                tbody.appendChild(row);
                                let dropDown = document.createElement("select");
                                dropDown.setAttribute("class", "dropDown");
                                var option1 = document.createElement("option");
                                option1.value = "normal";
                                option1.innerHTML = "normal";
                                var option2 = document.createElement("option");
                                option2.value = "dos";
                                option2.innerHTML = "dos";
                                var option3 = document.createElement("option");
                                option3.value = "r2l";
                                option3.innerHTML = "r2l";
                                var option4 = document.createElement("option");
                                option4.value = "probe";
                                option4.innerHTML = "probe";
                                var option5 = document.createElement("option");
                                option5.value = "u2r";
                                option5.innerHTML = "u2r";
                                dropDown.appendChild(option1);
                                dropDown.appendChild(option2);
                                dropDown.appendChild(option3);
                                dropDown.appendChild(option4);
                                dropDown.appendChild(option5);
                                let currentChoice = row.lastChild.innerHTML;
                                dropDown.value = currentChoice;
                                let temp=row.id;
                                dropDown.addEventListener("change", (event)=>{
                                    let status = dropDown.value;
                                    selectStatus(temp, status);
                                });

                                row.lastChild.replaceWith(dropDown);
                            }
                        }
                    };
                    xhttp.open("GET", "/items/5", true);
                    xhttp.send();
                }

                function getNew() {
                    var xhttp = new XMLHttpRequest();
                    xhttp.onreadystatechange = function() {
                        if (this.readyState == 4 && this.status == 200) {
                            var myArr = JSON.parse(this.responseText);
                            
                            tbody = document.getElementsByTagName("tbody")[1];
                            for(var k in myArr){
                                row = document.createElement("tr");
                                row.setAttribute("id", k);
                                for(var n in myArr[k]){
                                    cell = document.createElement("td");
                                    cell.innerHTML = myArr[k][n];
                                    row.appendChild(cell);
                                }
                                let predictButton = document.createElement("button");
                                predictButton.setAttribute("class", "predictButton");
                                predictButton.value = k;
                                predictButton.innerHTML = "predict";
                                let temp = row.id;
                                predictButton.addEventListener("click", (event)=>{
                                    //TODO
                                    alert("predict" + temp);
                                })
                                row.appendChild(predictButton);
                                tbody.appendChild(row);
                            }
                        }
                    };
                    xhttp.open("GET", "/newItems/5", true);
                    xhttp.send();
                }

                async function makeRequest(){
                    ratio();
                    accuracy();
                    attackNumber();
                    wrongPredictions();
                    getRecent();
                    getNew();
                }
                function selectStatus(id, status){
                    console.log("selected: " + id + "newStatus: " + status);
                    
                    var xhttp = new XMLHttpRequest();
                    xhttp.onreadystatechange = function() {
                        if (this.readyState == 4 && this.status == 200) {
                        }
                    };
                    xhttp.open("GET", "/selectStatus/" + id + "/" + status, true);
                    xhttp.send();
                }
            </script>
        </html>
    """
    
    return HTMLResponse(content=html_content, status_code=200)

#return list of logs
@app.get("/items/{items_number}")
def read_item(items_number: int, q: Optional[str] = None):

    with open('testLogs/newLogs', 'rb') as f:
        newLogs = pickle.load(f)
    #i stands for how many iterations should there be
    if(items_number > len(newLogs)):
        i = len(newLogs)
    else:
        i = items_number
    
    #get data and JSONify output
    total = {}
    items = {}
    for index, row in newLogs.iterrows():

        if i<=0:
            break
        item = {
            "duration": row[0],
            "protocol_type": row[1],
            "service": row[2],
            "flag": row[3],
            "src_bytes": row[4],
            "dst_bytes": row[5],
            "land": row[6],
            "wrong_fragment": row[7],
            "urgent": row[8],
            "hot": row[9],
            "num_failed_logins": row[10],
            "logged_in": row[11],
            "num_compromised": row[12],
            "root_shell": row[13],
            "su_attempted": row[14],
            "num_root": row[15],
            "num_file_creations": row[16],
            "num_shells": row[17],
            "num_access_files": row[18],
            "num_outbound_cmds": row[19],
            "is_host_login": row[20],
            "is_guest_login": row[21],
            "count": row[22],                              
            "srv_count": row[23],                          
            "serror_rate": row[24],                   
            "srv_serror_rate": row[25],                   
            "rerror_rate": row[26],                       
            "srv_rerror_rate": row[27],                   
            "same_srv_rate": row[28],                     
            "diff_srv_rate": row[29],                     
            "srv_diff_host_rate": row[30],               
            "dst_host_count": row[31],                      
            "dst_host_srv_count": row[32],                
            "dst_host_same_srv_rate": row[33],            
            "dst_host_diff_srv_rate": row[34],            
            "dst_host_same_src_port_rate": row[35],       
            "dst_host_srv_diff_host_rate": row[36],      
            "dst_host_serror_rate": row[37],              
            "dst_host_srv_serror_rate": row[38],        
            "dst_host_rerror_rate": row[39],              
            "dst_host_srv_rerror_rate": row[40],          
            "target": row[41]                         


        }
        items = {
            index: item   
            }
        total.update(items)
        i=i-1
    return total

#new items that weren't predicted yet
@app.get("/newItems/{items_number}")
def read_newitem(items_number: int, q: Optional[str] = None):

    with open('testLogs/newLogs', 'rb') as f:
        newLogs = pickle.load(f)
    #i stands for how many iterations should there be
    if(items_number > len(newLogs)):
        i = len(newLogs)
    else:
        i = items_number
    #get data and JSONify output
    newtotal = {}
    newitems = {}
    for index, row in newLogs.iterrows():

        if i<=0:
            break
        newitem = {
            "duration": row[0],
            "protocol_type": row[1],
            "service": row[2],
            "flag": row[3],
            "src_bytes": row[4],
            "dst_bytes": row[5],
            "land": row[6],
            "wrong_fragment": row[7],
            "urgent": row[8],
            "hot": row[9],
            "num_failed_logins": row[10],
            "logged_in": row[11],
            "num_compromised": row[12],
            "root_shell": row[13],
            "su_attempted": row[14],
            "num_root": row[15],
            "num_file_creations": row[16],
            "num_shells": row[17],
            "num_access_files": row[18],
            "num_outbound_cmds": row[19],
            "is_host_login": row[20],
            "is_guest_login": row[21],
            "count": row[22],                              
            "srv_count": row[23],                          
            "serror_rate": row[24],                   
            "srv_serror_rate": row[25],                   
            "rerror_rate": row[26],                       
            "srv_rerror_rate": row[27],                   
            "same_srv_rate": row[28],                     
            "diff_srv_rate": row[29],                     
            "srv_diff_host_rate": row[30],               
            "dst_host_count": row[31],                      
            "dst_host_srv_count": row[32],                
            "dst_host_same_srv_rate": row[33],            
            "dst_host_diff_srv_rate": row[34],            
            "dst_host_same_src_port_rate": row[35],       
            "dst_host_srv_diff_host_rate": row[36],      
            "dst_host_serror_rate": row[37],              
            "dst_host_srv_serror_rate": row[38],        
            "dst_host_rerror_rate": row[39],              
            "dst_host_srv_rerror_rate": row[40]                          
        }
        newitems = {
            index: newitem   
            }
        newtotal.update(newitems)
        i=i-1
    return newtotal


#return model prediction
@app.get("/predict/{logs}")
def predict(array):
    prediction = newGrid.best_estimator_.predict(array)
    return prediction

@app.get("/selectStatus/{index}/{newValue}")
def select_status(index: int, newValue):
    with open('testLogs/newLogs', 'rb') as f:
        newLogs2 = pickle.load(f)
    newLogs2.at[index, "target"] = newValue
    with open('testLogs/newLogs', 'wb') as f:
        pickle.dump(newLogs2, f)

    
    return 0

#How accurate the model is
@app.get("/accuracy/")
def accuracy():
    with open('model_pickle', 'rb') as f:
        newGridModel = pickle.load(f)
        CurrentAcc = newGridModel.best_score_
    return CurrentAcc

#Ratio of attacks to total number of logs
@app.get("/ratio/")
def ratio():
    with open('testLogs/test_Logs', 'rb') as f:
        allLogs = pickle.load(f)
        totalTested = allLogs["target"].value_counts()
        totalNormal = totalTested["normal"]
        totalRatio = (len(allLogs)-totalNormal)/len(allLogs)
    return totalRatio

#How many attacks occured
@app.get("/attackNumber/")
def attackNumber():
    with open('testLogs/test_logs', 'rb') as f:
        allLogs = pickle.load(f)
        tested = allLogs["target"].value_counts()
        normal1 = tested['normal']
        difference = len(allLogs) - normal1
        results = int(difference)
    return results

#How many wrong predictions
@app.get("/wrongPredictions/")
def wrongPredictions():
    with open('wrongLogs/wrongValues_pickle', 'rb') as f:
        wrongValues = pickle.load(f)
        number = len(wrongValues)
    return number