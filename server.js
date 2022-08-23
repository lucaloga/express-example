const express = require('express');
const serveIndex = require('serve-index');
const bodyParser = require('body-parser');
const path = require('path');
const { JSDOM } = require( "jsdom" );
const { window } = new JSDOM( "" );
const $ = require( "jquery" )( window );
const fs = require( "fs" );
var mqtt = require('mqtt');

const util = require('util')

const app = express()

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}))

app.use((req, res, next) => {
    console.log('Time: ', Date.now());
    next();
  });

app.use('/request-type', (req, res, next) => {
console.log('Request type: ', req.method);
next();
});

app.use("/public", express.static("public"));
app.use("/public", serveIndex("public"));

app.get("/", (req, res, next) => {
    res.sendFile(path.join(__dirname, 'index.html'));
})

app.get('/config', (req, res) => {
    
    
    if (fs.existsSync('config.json')) {
        let configurationFileContent = fs.readFileSync('config.json', 'utf8');
        res.send(configurationFileContent);
        return 
      }
    else{
        try{                                                                                        //se la creazione del file va a buon fine inietta il messaggio che dice che il file è stato creato correttamente
            fs.writeFile("config.json", "", function (err) {
                if (err) throw err;
                console.log('File is created successfully.');
            });
        }catch (e) {                                                                                //se non riesce a creare il file inietta nel codice il messaggio di errore della crezione del file
            console.log(e)
        }
    }
    
  });

app.get('/public/:fileName', function(req, res) {

  res.sendFile(__dirname + "/public/" + fileName);
});

app.post("/save", function(req, res) {
  console.log("called save test")
  const dataToSave = req.body
  console.log(dataToSave)
  try{                                                                                        //se la creazione del file va a buon fine inietta il messaggio che dice che il file è stato creato correttamente
    fs.writeFile("config.json", JSON.stringify(dataToSave), function (err) {
      if (err) throw err;
        console.log('File was written successfully.');
        res.send({response: "success"});
    });
  }catch (e) {                                                                                //se non riesce a creare il file inietta nel codice il messaggio di errore della crezione del file
      console.log(e)
  }
})
global.arrayOfClients = []
app.post("/start", function(req, res) {
  arrayOfClients = []
  console.log("called save test")
  const dataToSave = req.body
  console.log(dataToSave)
  if (fs.existsSync('config.json')) {
    let configurationFileContent = JSON.parse(fs.readFileSync('config.json', 'utf8'));
    console.log(configurationFileContent)
    
    configurationFileContent.devices.forEach((element,i )=> {
      let clientName = "client"+ element.id
      let client =  mqtt.connect("tcp://127.0.0.1:1883",{username: element.token})
      console.log("ClientName"+clientName)
      // console.log("Client: " + client)
      // console.log(util.inspect(client, {showHidden: false, depth: null}))
      arrayOfClients.push(client)
      // console.log("arrayOfClients"+util.inspect(arrayOfClients, {showHidden: false, depth: null}))
    })
    console.log("arrayofclient prima del maledetto for each :"+arrayOfClients)
    arrayOfClients.forEach((element,i)=> {
      console.log("element"+util.inspect(element, {showHidden: false, depth: null}))
      console.log("count "+i)
      // console.log("element arrayOfClients: "+element)
      element.on("connect",function(){	
          console.log("connected "+element.connected);
        })
      var options={
        retain:true,
        qos:1
      };
      element.publish("v1/devices/me/telemetry", JSON.stringify({"value": 111, "type": "device"}), options)
      
    })
    
  }
  res.send({response: "success"});
})

app.post("/stop", function(req, res) {
  console.log("called save test")
  const dataToSave = req.body
  console.log(dataToSave)
  arrayOfClients.forEach((element,i)=> {
    console.log("element:"+i)
    element.end();
  })  
})

app.listen(3000, () => console.log('Example app is listening on port 3000.'));


// global.client = mqtt.connect("tcp://127.0.0.1:1883",{username: "h41bSJ2Tis5Kf7xYGfjn"})
    
    // client.on("connect",function(){	
    //   console.log("connected "+client.connected);
    // })
    // client.on("error",function(error){ console.log("Can't connect"+error);});
    // var options={
    //   retain:true,
    //   qos:1};
    // setInterval(function() {
    //   client.publish("v1/devices/me/telemetry", JSON.stringify({"value": 111, "type": "device"}), options)
    // },10000)
    