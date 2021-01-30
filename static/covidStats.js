async function getCovidStats(covidStatsEndpoint) {
    console.log(covidStatsEndpoint)
    
    var covidApi = covidStatsEndpoint;
   await $.ajax({
        url: covidApi,
        type: 'GET',
        success: function (data){
            
            updateCovidResult(data);
        },
        error: function (response) {
            console.log("could not retrieve covid stats.");
            if (response.status == "404") {
                refreshAWSCredentials();
            }
        }
    });
}




function updateCovidResult(data) { 
    const myNode = document.getElementById("covid-stats").innerHTML= ""
    var newElement = document.createElement('div');
    if(data['date'] === undefined){
        newElement.innerHTML = 
        '<h3>Date: <span>' + getCurrentDate() + "</span></h3>" +
        '<h3>Confirmed cases: <span> ' + "Lucky Us, No Confirmed Cases" + "</span></h3>" +
        '<h3>Active cases: <span>' + "Neither any Active Cases" + "</span></h3>" +
        '<h3>Death toll: <span>' + "No Deaths, God Bless us All" + "</span></h3>" ;
        // console.log(data['confirmed'])

    }
    else{
    newElement.innerHTML = 
    "<h3>Date: <span>"+data['date']+"</span></h3>"+
    "<h3>Confirmed cases:  <span>"+data['confirmed']+"</span></h3>"+
    "<h3>Active cases: <span>"+data['active']  +"</span></h3>"+
    "<h3>Death toll: <span>"+data['deaths'] +"</span></h3>";
    }
    document.getElementById("covid-stats").appendChild(newElement);
}
