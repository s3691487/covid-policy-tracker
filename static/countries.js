function getDistinctCountry(countryurl) {
    return $.ajax({
        url: countryurl,
        type: 'get'
    }).then(function(response){
      console.log("getRecord response: "+JSON.stringify(response));
      return response;
  });
}

function updateResult(data) { 
    console.log('distinct country')
    console.log(data)
 Object.keys(data).forEach(key => {
   var newElement = document.createElement('a');
   newElement.innerHTML = data[key];
   document.getElementById("dropdown-content").appendChild(newElement);
  });
}

