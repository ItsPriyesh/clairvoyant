

let credentials = {
  user_id: localStorage.getItem('userId'),
  session_token: localStorage.getItem('token')
};

let historyTable = $("#history_table").find('tbody');
let confidenceTable = $("#confidence_table").find('tbody');

const hiMed = 66;
const medLo = 33;

var pie;
var chartGlobal;

var API_BASE;
var SOCKET_BASE;

let config = {"api_url": "http://168.62.177.105:8081", "socket_url": "ws://168.62.177.105:8081"};

$(document).ready(function() {
  // $.getJSON("config.json", (config) => {
  API_BASE = config.api_url;
  SOCKET_BASE = config.socket_url;
  const urlParams = new URLSearchParams(window.location.search);
  const nodeId = urlParams.get('node_id');
  httpGET('/nodeInfo', nodeId, (datapoints) => {
    bindEventBreakdown(datapoints);
    bindHistory(datapoints);
    populateConfidence(datapoints);
    console.log(datapoints);
  });

});

bindEventBreakdown = function(datapoints) {
  let eventTypes = countByType(datapoints);
  var dps = [];
  for (var type in eventTypes) {
    dps.push({ y: eventTypes[type], label: type})
  }
  var chart = new CanvasJS.Chart("chartContainer", {
  animationEnabled: true,
  backgroundColor: '#27272b',
  data: [{
    type: "pie",
    startAngle: 240,
    indexLabelFontColor: "#e3e3e3",
    yValueFormatString: "##0",
    indexLabel: "{label} {y}",
    dataPoints: dps
  }]
  });
  chart.render();
  chartGlobal = chart;
}

countByType = function(datapoints) {
  var groups = {};
  $.each(datapoints, function(i, datapoint) {
    let type = datapoint["classification"];
    if (!(type in groups)) {
      groups[type] = 0;
    }
    groups[type]++;
  });
  return groups;
};

bindHistory = function(datapoints) {
  for (var i = 0; i < datapoints.length; i++) {
    let d = datapoints[i];
    appendHistory(d);
  }
}

appendHistory = function(d) {
  let row = `<tr class='history_table_body'><td>Node ${d.node_id}</td><td>${d.classification}</td><td>${d.confidence}%</td><td>${d.created_at}</td></tr>`;
  historyTable.append(row);
}

appendConfidenceTable = function(type, vals) {
	let row = `<tr><th class='confidence_table_head'>${type}</th><td class='confidence_table_cell' style='background-color:red;'>${vals[0]}</td><td class='confidence_table_cell' style='background-color:orange;'>${vals[1]}</td><td class='confidence_table_cell' style='background-color:green;'>${vals[2]}</td></tr>`;
  confidenceTable.append(row);
}

populateConfidence = function(datapoints) {
	var vals = [];
	for(var i = 0; i < 4; i++) {
		vals[i] = [];
		vals[i][0] = 0;
		vals[i][1] = 0;
		vals[i][2] = 0;
    vals[i][3] = 0;
	}
	for(var i = 0; i < datapoints.length; i++) {
		if(datapoints[i].classification === 'explosive'){
			if(datapoints[i].confidence > hiMed) {
				vals[0][2]++;
			} else if(datapoints[i].confidence > medLo) {
				vals[0][1]++;
			} else {
				vals[0][0]++;
			}
		} else if (datapoints[i].classification === 'vehicle') {
			if(datapoints[i].confidence > hiMed) {
				vals[1][2]++;
			} else if(datapoints[i].confidence > medLo) {
				vals[1][1]++;
			} else {
				vals[1][0]++;
			}
		} else if (datapoints[i].classification === 'gunshot') {
			if(datapoints[i].confidence > hiMed) {
				vals[2][2]++;
			} else if(datapoints[i].confidence > medLo) {
				vals[2][1]++;
			} else {
				vals[2][0]++;
			}
		} else if (datapoints[i].classification === 'human_sound') {
      if(datapoints[i].confidence > hiMed) {
        vals[3][2]++;
      } else if(datapoints[i].confidence > medLo) {
        vals[3][1]++;
      } else {
        vals[3][0]++;
      }
    }
	}

	appendConfidenceTable("EXPLOSIVE", vals[0]);
	appendConfidenceTable("VEHICLE", vals[1]);
	appendConfidenceTable("GUNSHOT", vals[2]);
  appendConfidenceTable("HUMAN SOUND", vals[3]);

}

httpGET = function(endpoint, nodeId, onSuccess) {
    $.ajax({
      url: API_BASE + endpoint,
      // url: 'http://localhost:8081' + endpoint,
      type: 'GET',
      'data' : {
      	user_id: localStorage.getItem('userId'),
  		session_token: localStorage.getItem('token'),
  		node_id: nodeId
		}
    }).done(function(data) {
        onSuccess(data);
    }).fail(function(error) {
        // show error
    });
}