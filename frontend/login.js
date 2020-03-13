let config = {"api_url": "http://localhost:8081", "socket_url": "ws://localhost:8081"};

$(document).ready(function(){
  // $.getJSON("config.json", function(config) {
  $("#submit").click(function() {
    $.ajax({
      url: config.api_url + '/login',
      type: 'GET',
      'data' : {
        'email' : $("#login").val(),
        'password' : md5($("#password").val()),
      }
    }).done(function(data) {
      loadDashboard(data);
    }).fail(function(error) {
      alert(error.responseText);
    });
  });
});
// });

loadDashboard = function(data) {
  console.log(data);
  localStorage.setItem('token', data.session_token);
  localStorage.setItem('userId', data.user_id);
  console.log(localStorage.getItem('token'));
  console.log(localStorage.getItem('userId'));
  window.location = "./dash.html";
}

function handleEnter(e) {
  if(e.keyCode === 13){
      document.getElementById("submit").click();
  }
}

