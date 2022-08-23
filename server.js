const express = require('express');
const serveIndex = require('serve-index');
const bodyParser = require('body-parser');
const path = require('path');
const { JSDOM } = require( "jsdom" );
const { window } = new JSDOM( "" );
const $ = require( "jquery" )( window );
const fs = require( "fs" );
var mqtt = require('mqtt');

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



app.listen(3000, () => console.log('Example app is listening on port 3000.'));


