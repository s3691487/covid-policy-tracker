async function getCovidStats(covidStatsEndpoint) {
    console.log(covidStatsEndpoint)
    
    var covidApi = covidStatsEndpoint;
   await $.ajax({
        url: covidApi,
        type: 'GET',
        success: function (data){
            console.log(data)
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
    var newElement = document.createElement('h3');
    newElement.innerHTML = 
    'Date: ' + data['date'] + "<br>" +
    'Confirmed cases: ' + data['confirmed'] + "<br>" +
    'Active cases: ' + data['active']  + "<br>" +
    'Death toll: ' + data['deaths']  + "<br>" ;
    document.getElementById("covid-stats").appendChild(newElement);
}
