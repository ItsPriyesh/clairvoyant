let datapoints = [
  {
    node_id: 1,
    type: "Gunshot",
    confidence: .96,
    time: "July 4, 16:04:20"
  },
  {
    node_id: 2,
    type: "Vehicle",
    confidence: .94,
    time: "July 4, 16:04:20"
  },
  {
    node_id: 3,
    type: "Missile",
    confidence: .91,
    time: "July 4, 16:04:20"
  }
];

let pieColors = {
  Gunshot: '#ba2c54',
  Missile: '#4275f7',
  Vehicle: '#b4d664',
};

$(document).ready(function() {
  bindEventBreakdown(datapoints);
  bindHistory(datapoints);
  listenForDataPoints();
});

listenForDataPoints = function() {
  let webSocket = new WebSocket('ws://localhost:8081/listenDataPoint/');
  webSocket.onopen = function () {
    let listenRequest = {user_id: 19, session_token: "6594ccfa-e950-4c8a-a408-613c8d87580d"};
    webSocket.send(JSON.stringify(listenRequest)); 
  }
  webSocket.onmessage = function (msg) { 
    console.log('Received datapoint: ' + msg.data);
    // TODO: Update UI
  };
};

fetchDataPoints = function() {
  $.ajax({
    url: 'http://localhost:8081/getDataPoints',
    type: 'GET',
    'data' : {
      'token': sessionToken
    }
  }).done(function(datapoints) {
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
