var a = $("#listaDio")
console.log(a.data)
var configurationData = []
var device = {}

// GET DATA FROM CONFIG JSON
function getConfig(){
    fetch("config")
    .then((response) => response.json())
    .then((data) => {
        console.log(data)
        data.devices.forEach((element,i )=> {
            console.log(element.name);
            
            $("#configurationFileContainer").append('<div class="containerInsert" data-key="'+ element.id +'">'+
            '<div class="card" style="width: 100%; key="'+element.id+'">'+
                '<div class="card-body">'+
                  '<h6 class="card-title">Device Name: ' + element.name + '</h6>'+
                  '<h6 class="card-text">Device Token: ' + element.token + '</h6>'+
                '</div>'+
              '</div>'+
        
            '<div class="buttonContainer">'+
                '<button type="button" class="btn btn-danger" onclick="'+removeCard()+'"><i class="fas fa-minus"></i></button>'+
            '</div>'+
        '</div>')

        // attach on click event on button for remove card
        var newCardAdded = $("#configurationFileContainer").find(".btn-danger").last();
        newCardAdded.on("click", removeCard)

        });
        // saving data on local var
        configurationData = data.devices
    }
    );
}

getConfig()
// /GET DATA FROM CONFIG JSON

// CARD ADDER
function addCard(){
    // take input fileds values
    var deviceName = $("#device-name").val();
    var deviceToken = $("#device-token").val();
    let unique = true
    // take input fileds values
    console.log("Name : " + deviceName + " Token : " + deviceToken);
    configurationData.forEach(element =>{
        if(element.token.toLowerCase() == deviceToken.toLowerCase())
            unique = false
    })
    if(deviceName && deviceToken && unique == true){
        $("#configurationFileContainer").append('<div class="containerInsert" data-key="'+ (configurationData.length + 1 )+'">'+
        '<div class="card '+ (configurationData.length + 1 )+'" style="width: 100%;" >'+
            '<div class="card-body">'+
              '<h5 class="card-title">' + deviceName + '</h5>'+
              '<p class="card-text">' + deviceToken + '</p>'+
            '</div>'+
          '</div>'+
    
        '<div class="buttonContainer">'+
            '<button type="button" class="btn btn-danger" onclick="'+removeCard()+'"><i class="fas fa-minus"></i></button>'+
        '</div>'+
    '</div>');
        
        // attach on click event on button for remove card
        var newCardAdded = $("#configurationFileContainer").find(".btn-danger").last();
        newCardAdded.on("click", removeCard)
        

        // object creation and relative push on array of devices
        device = {
            id: configurationData.length + 1,
            name: $("#device-name").val(),
            token: $("#device-token").val()
        }
        console.log("oggetto device:"+device)
        configurationData.push(device)
        console.log(configurationData)


        //clear the input fileds
        $("#device-name").val([]);
        $("#device-token").val([]);
        //clear the input fileds
    }else if(unique == false){
        alert("Token Device already exists")
    }else{
        alert("Insert Device Data")
    }
    
}
// /CARD ADDER

// CARD REMOVER
function removeCard(){
    var numCards = $('.containerInsert').length;

    if(numCards > 1){
        let key = $(this).parent().parent().data("key")
        $(this).parent().parent().remove()
        configurationData = configurationData.filter(element => element.id !== key)
        console.log(configurationData)
    }
}
// /CARD REMOVER

// SAVE DATI DISPOSITIVI
function save(){
    console.log("save")
    $("#device-name").prop("disabled", true);
    $("#device-token").prop("disabled", true); 
    $("#addButton").prop("disabled", true);
    $(".btn-danger").prop("disabled", true);
    $("#saveButton").prop("disabled", true);

    $.ajax({
        url: "/save",
        type: "POST",
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify( {devices:configurationData} ),
        success: function(result) {
            console.log(result)
            $("#device-name").prop("disabled", false);
            $("#device-token").prop("disabled", false); 
            $("#addButton").prop("disabled", false);
            $(".btn-danger").prop("disabled", false);
            $("#saveButton").prop("disabled", false);
        },
        error: function(result){
            console.log(result)
            alert("Post Request Failed")
        }
        });

        
}
// /SAVE DATI DISPOSITIVI

// LOGICA START CLIENT todo: aggiungere logiche di controllo dello start
var toggleSave = false;
function start(){
    toggleSave = !toggleSave
    $("#device-name").prop("disabled", toggleSave);
    $("#device-token").prop("disabled", toggleSave); 
    $("#addButton").prop("disabled", toggleSave);
    $(".btn-danger").prop("disabled", toggleSave);
    $("#saveButton").prop("disabled", toggleSave);
    if(toggleSave){
        $("#startButton").text("Stop")
        $("#startButton").removeClass("btn-success")
        $("#startButton").addClass("btn-danger")
        //Chiamata per avviare la logica dei/del client mqtt
    }else{
        $("#startButton").text("Start")
        $("#startButton").removeClass("btn-danger")
        $("#startButton").addClass("btn-success")
        //Chiamata per arrestare la logica dei/del client mqtt
    }
    // implementare logica e relativa chiamata per attivare il parser dei file txt e i diversi client mqtt 
}
// /LOGICA START CLIENT
