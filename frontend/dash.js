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
var pie;

var API_BASE;
var SOCKET_BASE;

$(document).ready(function() {
  $.getJSON("config.json", (config) => {
    API_BASE = config.api_url;
    SOCKET_BASE = config.socket_url;
  httpGET('/nodes', (nodes) => {
    // console.log('Received nodes ' + JSON.stringify(nodes));
    bindNodes(nodes);
    bindNodeSummary(nodes);
  });

  httpGET('/datapoints', (datapoints) => {
    // console.log('Received datapoints ' + JSON.stringify(datapoints));
    bindEventBreakdown(datapoints);
    bindHistory(datapoints);
  });

  let webSocket = new WebSocket(SOCKET_BASE + '/listenDataPoint');
  // let webSocket = new WebSocket('ws://localhost:8081' + '/listenDataPoint');
  webSocket.onopen = function () {
    webSocket.send(JSON.stringify(credentials));
  }
  webSocket.onmessage = function (msg) {
    var dp = JSON.parse(msg.data);
    prependHistory(dp);
    animateDataPointReceived(dp);
    updateChart(pie, dp.classification, dp);
  };
  });
});

animateDataPointReceived = function(dp) {
    $("#notif-node").text("Node " + dp["node_id"]);
    $("#notif-class").text(dp["classification"]);
    $("#notif-time-ago").text(dp["created_at"]);

    let notif = $("#datapoint-notif");
    notif.removeClass('animate-idle');
    notif.addClass('animate-pulse');
    notif.animate({opacity: .9}, 200);

    setTimeout(() => {
      notif.removeClass('animate-pulse');
      notif.addClass('animate-idle');
      notif.animate({opacity: .65}, 200);
    }, 3000);
}

bindNodes = function(nodes) {
  let graphNodes = nodes.map((node, i) => {
    return {
      label: 'Node ' + node.id,
      id: node.id,
      x: i,
      y: 0,
      size: 3
    }
  });

  let graphEdges = []
  for (var i = 0; i < nodes.length - 1; i++) {
    graphEdges.push({
      id: 'edge' + i,
      source: nodes[i].id,
      target: nodes[i+1].id
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

bindNodeSummary = function(nodes) {
  let nodesTable = $("#nodes_table").find('tbody');
  for(var i = 0; i < nodes.length; i++) {
    let n = nodes[i];
    let row = `<tr><td>${n.id}</td><td>${n.battery_level}%</td></tr>`;
    nodesTable.append(row);
  }
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

prependHistory = function(d) {
  let histTable = document.getElementById("history_table");
  var row = histTable.insertRow(1);
  row.innerHTML = `<tr><td>Node ${d.node_id}</td><td>${d.classification}</td><td>${d.confidence * 100}%</td><td>${d.created_at}</td></tr>`;

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
  pie = new Chart(ctx, config);
}

updateChart = function(chart, label, data) {
  for(var i = 0; i < chart.data.datasets[0].data.length; i++) {
    if(label === chart.data.labels[i]) {
      chart.data.datasets[0].data[i]++;
    }
  }
  
  chart.update();
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

 httpGET = function(endpoint, onSuccess) {
    $.ajax({
      url: API_BASE + endpoint,
      // url: 'http://localhost:8081' + endpoint,
      type: 'GET',
      'data' : credentials
    }).done(function(data) {
        onSuccess(data);
    }).fail(function(error) {
        // show error
    });
}
