let pieColors = {
  GUNSHOT: '#ba2c54',
  EXPLOSION: '#4275f7',
  VEHICLE: '#b4d664',
};

$(document).ready(function() {
  fetchDataPoints();
  listenForDataPoints();
});

let credentials = {user_id: localStorage.getItem('userId'), session_token: localStorage.getItem('token')};
let historyTable = $("#history_table").find('tbody');
var dps = [];

listenForDataPoints = function() {
  let webSocket = new WebSocket('ws://localhost:8081/listenDataPoint/');
  webSocket.onopen = function () {
    webSocket.send(JSON.stringify(credentials)); 
  }
  webSocket.onmessage = function (msg) { 
    var dp = JSON.parse(msg.data);
    dps.push(dp);
    console.log(dps);
    appendHistory(dp);
    bindEventBreakdown(dps);
  };
}

fetchDataPoints = function() {
  $.ajax({
    url: 'http://localhost:8081/datapoints',
    type: 'GET',
    'data' : credentials
  }).done(function(datapoints) {
      console.log('Received datapoints ' + JSON.stringify(datapoints));
      dps = datapoints;
      bindEventBreakdown(datapoints);
      bindHistory(datapoints);
  }).fail(function(error) {
      // show error

  });
}

bindHistory = function(datapoints) {
  for (var i = 0; i < datapoints.length; i++) {
    let d = datapoints[i];
    appendHistory(d);
  }
}

appendHistory = function(d) {
  let row = `<tr><td>Node ${d.node_id}</td><td>${d.classification}</td><td>${d.confidence * 100}%</td><td>${d.created_at}</td></tr>`;
  historyTable.append(row);
}

bindEventBreakdown = function(datapoints) {
  let eventTypes = countByType(datapoints);
  var config = {
    type: 'pie',
    data: {
      datasets: [{
        data: Object.values(eventTypes),
        backgroundColor: Object.keys(eventTypes).map(t => pieColors[t]),
        borderWidth: 0
      }],
      labels: Object.keys(eventTypes)
    },
    options: {
      responsive: false,
      legend: {
        position: "right"
      }
    }
  };

  var ctx = document.getElementById('event-pie').getContext('2d');
  ctx.width = 1;
  ctx.height = 1;
  let pie = new Chart(ctx, config);
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
