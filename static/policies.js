async function getPolicy() {

var selectBox = document.getElementById("dropdown");
var selectedValue = selectBox.options[selectBox.selectedIndex].value;
currentMonth = getCurrentMonthYear()
await getDefaultPolicy('https://q2ua1gzvsj.execute-api.ap-southeast-2.amazonaws.com/beta_0_0/getmonthlypolicy?country_name='+selectedValue+'&month='+currentMonth);
await getCovidStats('https://cxfqobcqe8.execute-api.ap-southeast-2.amazonaws.com/dep_1/getCovidCases?country_name='+selectedValue+'&date='+currentMonth+'-01') 
}

function getDefaultPolicy(countryurl) {
    return $.ajax({
        url: countryurl,
        type: 'get'
    }).then(function(response){
      console.log("getRecord response: "+JSON.stringify(response));
      const myNode = document.getElementById("innerPolicy");
      if (myNode.hasChildNodes()){
  while (myNode.hasChildNodes()) {
    myNode.removeChild(myNode.lastChild);
}}
var selectBox = document.getElementById("dropdown");
var selectedValue = selectBox.options[selectBox.selectedIndex].value;
    var heading = document.getElementById('policies')
    var heading_text = heading.childNodes[0]
    heading_text.nodeValue = "Key Policies in "+selectedValue+" on year/month "+getCurrentMonthYear()

      Object.keys(response).reverse().forEach(key => {

          if(response[key]['stay_at_home_requirements_notes']!=null || response[key]['restrictions_on_gatherings_notes']!=null||
          response[key]['international_travel_controls_notes']!=null || response[key]['workplace_closing_notes']!=null ||
          response[key]['cancel_public_events_notes']!=null || response[key]['school_closing_notes']!=null ){

               var newElement = document.createElement('details');
               newElement.className = 'square-container'
               newElement.innerHTML = '<summary>['+  response[key]['date']+ ']' + '</summary>';      
               if(response[key]['stay_at_home_requirements_notes']!=null){
                   newElement.innerHTML += '<p>' + ' STAY AT HOME REQUIREMENTS: ' + '<br>' + response[key]['stay_at_home_requirements_notes'] + '</p>'
                }
               if(response[key]['restrictions_on_gatherings_notes']!=null){
                    newElement.innerHTML += '<p>' +' RESTRICTIONS ON GATHERING: '+ '<br>' +  response[key]['restrictions_on_gatherings_notes'] + '</p>'
                }
                if(response[key]['international_travel_controls_notes']!=null){
                    newElement.innerHTML += '<p>' +' INTERNATIONAL TRAVEL CONTROL: '+ '<br>' +  response[key]['international_travel_controls_notes'] + '</p>'
                }
                if(response[key]['workplace_closing_notes']!=null){
                    newElement.innerHTML += '<p>' + ' WORK PLACE CLOSURES: '+ '<br>' + response[key]['workplace_closing_notes'] + '</p>'
                }
                if(response[key]['cancel_public_events_notes']!=null){
                    newElement.innerHTML += '<p>' + ' PUBLIC EVENTS CANCELLATIONS: '+ '<br>' + response[key]['cancel_public_events_notes'] + '</p>'
                }
                if(response[key]['school_closing_notes']!=null){
                    newElement.innerHTML += '<p>' +' SCHOOL CLOSURES: '+ '<br>' + response[key]['school_closing_notes'] + '</p>'
                }
                if(newElement.innerHTML!==''){
                    document.getElementById("innerPolicy").appendChild(newElement);
                }
          }
     
        
      });
  });


}

function drawChart(dataurl){
    console.log("look here")
    console.log(dataurl);
    return $.ajax({
        url: dataurl,
        type: 'get'
    }).then(function(response){

    var tableData = [];
    var header = ['Date','public event cancellation', 'public transit closure','contact tracing efficacy','gathering restrictions','stay at home restrictions','work place closure']
     tableData.push(header);

    Object.keys(response).forEach(key => {
        console.log("look here");
       temp=[];
       temp.push(new Date(response[key]['date']));
       temp.push(parseFloat(response[key]['cancel_public_events']));
       temp.push(parseFloat(response[key]['close_public_transit']));
       temp.push(parseFloat(response[key]['contact_tracing']));
       temp.push(parseFloat(response[key]['restrictions_on_gatherings']));
       temp.push(parseFloat(response[key]['stay_at_home_requirements']));
       temp.push(parseFloat(response[key]['workplace_closing']));
       tableData.push(temp);
       
    });
    console.log(tableData)
    var options = {
        title: 'Covid Restriction Levels (on daily basis)',
        isStacked: true
      };

    var table = new google.visualization.arrayToDataTable(tableData);

    var chart =  new google.visualization.ColumnChart(document.getElementById('chart'));
    chart.draw(table, options);
    });
}