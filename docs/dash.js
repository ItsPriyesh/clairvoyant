let pieColors = {
  GUNSHOT: '#ba2c54',
  EXPLOSION: '#4275f7',
  VEHICLE: '#b4d664',
};

$(document).ready(function() {
  fetchDataPoints();
  listenForDataPoints();
});

// TODO: read this from local storage / cookies
let credentials = {user_id: 1, session_token: localStorage.getItem('token')};

listenForDataPoints = function() {
  let webSocket = new WebSocket('ws://localhost:8081/listenDataPoint/');
  webSocket.onopen = function () {
    webSocket.send(JSON.stringify(credentials)); 
  }
  webSocket.onmessage = function (msg) { 
    console.log('Received datapoint: ' + msg.data);
    // TODO: Update UI
  };
};

fetchDataPoints = function() {
  $.ajax({
    url: 'http://localhost:8081/datapoints',
    type: 'GET',
    'data' : credentials
  }).done(function(datapoints) {
      console.log('Received datapoints ' + JSON.stringify(datapoints))
      bindEventBreakdown(datapoints);
      bindHistory(datapoints);
  }).fail(function(error) {
      // show error

  });
}

bindHistory = function(datapoints) {
  let table = $("#history_table").find('tbody');
  for (var i = 0; i < datapoints.length; i++) {
    let d = datapoints[i];
    let row = `<tr><td>Node ${d.node_id}</td><td>${d.type}</td><td>${d.confidence * 100}%</td><td>${d.time}</td></tr>`;
    table.append(row);
  }
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
    let type = datapoint["type"];
    if (!(type in groups)) {
      groups[type] = 0;
    }
    groups[type]++;
  });
  return groups;
};
