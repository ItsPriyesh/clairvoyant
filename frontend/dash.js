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
let motionHistoryTable = $("#motion_history_table").find('tbody');

var pie;
var chartGlobal;

var API_BASE;
var SOCKET_BASE;

let config = {"api_url": "http://localhost:8081", "socket_url": "ws://localhost:8081"};

$(document).ready(function() {
  // $.getJSON("config.json", (config) => {
    API_BASE = config.api_url;
    SOCKET_BASE = config.socket_url;
  httpGET('/nodes', (nodes) => {
    // console.log('Received nodes ' + JSON.stringify(nodes));
    // bindNodes(nodes);
    // bindNodeSummary(nodes);
  });

  httpGET('/datapoints', (datapoints) => {
    // console.log('Received datapoints ' + JSON.stringify(datapoints));
    // bindEventBreakdown(datapoints);
    bindHistory(datapoints);
  });

  httpGET('/motionevents', (motionevents) => {
     console.log('Received motionevents ' + JSON.stringify(motionevents));
    bindMotionHistory(motionevents);
    
    var node1 = null, node2 = null, node3 = null;
    for (var i = 0; i < motionevents.length; i++) {
      if (node1 != null && node2 != null && node3 != null) {
        break;
      }
      switch (motionevents[i].node_id) {
        case "1": node1 = motionevents[i]; break;
        case "2": node2 = motionevents[i]; break;
        case "3": node3 = motionevents[i]; break;
      }
    }
    if (node1 != null) updateNodeInMesh(node1);
    if (node2 != null) updateNodeInMesh(node2);
    if (node3 != null) updateNodeInMesh(node3);
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
    animateNodeReceived(dp);
    // updateChart(chartGlobal, dp.classification, dp);
  };

  let motionEventSocket = new WebSocket(SOCKET_BASE + '/listenMotionEvent');
  motionEventSocket.onopen = function () {
    motionEventSocket.send(JSON.stringify(credentials));
  }
  motionEventSocket.onmessage = function (msg) {
    var event = JSON.parse(msg.data);
    prependMotionHistory(event);
    updateNodeInMesh(event);
  };
});
  
// });

animateDataPointReceived = function(dp) {
    $("#notif-node").text("Node " + dp["node_id"]);
    $("#notif-class").text(dp["classification"]);
    $("#notif-time-ago").text(dp["created_at"]);

    let notif = $("#datapoint-notif");
    notif.removeClass('animate-idle');
    notif.addClass('animate-pulse');
    notif.animate({opacity: 1}, 200);

    setTimeout(() => {
      notif.removeClass('animate-pulse');
      notif.addClass('animate-idle');
      notif.animate({opacity: .75}, 200);
    }, 3000);
}

animateNodeReceived = function(dp) {

    $("#node-" + dp["node_id"] + "-notif-text").text(dp["classification"]);

    let notif = $("#node-" + dp["node_id"] + "-notif");
    notif.removeClass('animate-idle');
    notif.addClass('animate-pulse');
    notif.animate({opacity: 1}, 200);

    setTimeout(() => {
      notif.removeClass('animate-pulse');
      notif.addClass('animate-idle');
      notif.animate({opacity: .75}, 200);
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
  let row = `<tr class='history_table_body'><td>Node ${d.node_id}</td><td>${d.classification}</td><td>${d.confidence}%</td><td>${d.created_at}</td></tr>`;
  historyTable.append(row);
}

bindMotionHistory = function(motionevents) {
  for (var i = 0; i < motionevents.length; i++) {
    let d = motionevents[i];
    appendMotionHistory(d);
  }
}

appendMotionHistory = function(d) {
  let row = `<tr class='history_table_body'><td>Node ${d.node_id}</td><td>${d.motion_type}</td><td>${d.orientation}</td><td>${d.roll}</td><td>${d.pitch}</td><td>${d.yaw}</td></tr>`;
  motionHistoryTable.append(row);
}

prependHistory = function(d) {
  let histTable = document.getElementById("history_table");
  var row = histTable.insertRow(1);
  var cell1 = row.insertCell(0);
  var cell2 = row.insertCell(1);
  var cell3 = row.insertCell(2);
  var cell4 = row.insertCell(3);
  cell1.innerHTML = `Node ${d.node_id}`;
  cell2.innerHTML = `${d.classification}`;
  cell3.innerHTML = `${d.confidence}%`;
  cell4.innerHTML = `${d.created_at}`;
  row.classList.add('history_table_body');
  //row.innerHTML = `<tr><td>Node ${d.node_id}</td><td>${d.classification}</td><td>${d.confidence}%</td><td>${d.created_at}</td></tr>`;
}

prependMotionHistory = function(d) {
  let histTable = document.getElementById("motion_history_table");
  var row = histTable.insertRow(1);
  var cell1 = row.insertCell(0);
  var cell2 = row.insertCell(1);
  var cell3 = row.insertCell(2);
  var cell4 = row.insertCell(3);
  var cell5 = row.insertCell(4);
  var cell6 = row.insertCell(5);

  cell1.innerHTML = `Node ${d.node_id}`;
  cell2.innerHTML = `${d.motion_type}`;
  cell3.innerHTML = `${d.orientation}`;
  cell4.innerHTML = `${d.roll}`;
  cell5.innerHTML = `${d.pitch}`;
  cell6.innerHTML = `${d.yaw}`;

  row.classList.add('history_table_body');
}

updateNodeInMesh = function(dp) {
    $("#node-" + dp["node_id"] + "-orientation").text(dp.orientation);
    $("#node-" + dp["node_id"] + "-roll").text(dp.roll);
    $("#node-" + dp["node_id"] + "-pitch").text(dp.pitch);
    $("#node-" + dp["node_id"] + "-yaw").text(dp.yaw);
}

bindEventBreakdown = function(datapoints) {
  let eventTypes = countByType(datapoints);
  /*var config = {
    type: 'pie',
    data: {
      datasets: [{
        data: Object.values(eventTypes),
        backgroundColor: ["#0074D9", "#FF4136", "#2ECC40", "#FF851B", "#7FDBFF", "#B10DC9", "#FFDC00", "#001f3f", "#39CCCC", "#01FF70", "#85144b", "#F012BE"],
        borderWidth: 0
      }],
      labels: Object.keys(eventTypes)
    },
    options: {
      responsive: false,
      legend: {
        position: "right",
	labels: { fontColor: "#fff" }
      }
    }
  };

  var ctx = document.getElementById('event-pie').getContext('2d');
  ctx.width = 1;
  ctx.height = 1;
  pie = new Chart(ctx, config);

*/
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
    yValueFormatString: "##0.00\"%\"",
    indexLabel: "{label} {y}",
    dataPoints: dps
  }]
});
chart.render();
chartGlobal = chart;
}

updateChart = function(chart, label, data) {
  /*for(var i = 0; i < chart.data.datasets[0].data.length; i++) {
    if(label === chart.data.labels[i]) {
      chart.data.datasets[0].data[i]++;
    }
  }

  chart.update();*/
  var added = false;
  for(var i = 0; i < chart.options.data[0].dataPoints.length; i++) {
    if (label == chart.options.data[0].dataPoints[i].label) {
      chart.options.data[0].dataPoints[i].y++;
      added = true;
    }
  }
  if (!added) {
    chart.options.data[0].dataPoints.push({y: 1, label: label});
  }
  chart.render();
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

