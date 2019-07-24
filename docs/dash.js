let API_BASE = '3.93.231.152:8081';
let HTTP_BASE = 'http://' + API_BASE;
let SOCKET_BASE = 'ws://' + API_BASE;

let pieColors = {
  GUNSHOT: '#ba2c54',
  EXPLOSION: '#4275f7',
  VEHICLE: '#b4d664',
};

let credentials = {
  user_id: localStorage.getItem('userId'), 
  session_token: localStorage.getItem('token')
};

let historyTable = $("#history_table").find('tbody');
var dps = [];

$(document).ready(function() {
  httpGET('/nodes', (nodes) => {
    console.log('Received nodes ' + JSON.stringify(nodes));
    bindNodes(nodes);
  });

  httpGET('/datapoints', (datapoints) => {
    console.log('Received datapoints ' + JSON.stringify(datapoints));
    dps = datapoints;
    bindEventBreakdown(datapoints);
    bindHistory(datapoints);
  });

  let webSocket = new WebSocket(SOCKET_BASE + '/listenDataPoint');
  webSocket.onopen = function () {
    webSocket.send(JSON.stringify(credentials)); 
  }
  webSocket.onmessage = function (msg) {
    var dp = JSON.parse(msg.data);
    dps.push(dp);
    console.log(dps);
    appendHistory(dp);
    bindEventBreakdown(dps);

    let notif = $("#datapoint-notif");
    let html = document.getElementById("datapoint-notif");
    if (window.getComputedStyle(html).visibility === "hidden") {
      notif.css('visibility', 'visible');
    }
    $("#notif-node").text("Node " + dp["node_id"]);
    $("#notif-class").text(dp["classification"]);
    $("#notif-time-ago").text(dp["created_at"]);
  };
});

httpGET = function(endpoint, onSuccess) {
  $.ajax({
    url: HTTP_BASE + endpoint,
    type: 'GET',
    'data' : credentials
  }).done(function(data) {
      onSuccess(data);
  }).fail(function(error) {
      // show error
  });
}

bindNodes = function(nodes) {
  let graphNodes = nodes.map((node, i) => {
    return {
      label: 'Node ' + node,
      id: node,
      x: i,
      y: 0,
      size: 3
    }
  });

  let graphEdges = []
  for (var i = 0; i < nodes.length - 1; i++) {
    graphEdges.push({
      id: 'edge' + i,
      source: nodes[i],
      target: nodes[i+1]
    });
  }

  let s = new sigma({ 
    graph: { nodes: graphNodes, edges: graphEdges },
    container: 'network-container',
    settings: {
        defaultNodeColor: '#e3e3e3',
        defaultLabelColor: '#e3e3e3',
        defaultLabelAlignment: 'top',
        zoomingRatio: 1,
        enableCamera: false,
        enableHovering: false
    }
  });
};

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
  console.log("bindEventBreakdown " +datapoints );
  let eventTypes = countByType(datapoints);
  console.log(eventTypes);
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
