async function getCovidInfectedRegion(countryurl) {
    return $.ajax({
        url: countryurl,
        type: 'get'
    }).then(function(response){
      console.log("getRecord response: "+JSON.stringify(response));
      return response;
  });
}


console.log("locations"+typeof(locations))
console.log("airports"+typeof(airports))