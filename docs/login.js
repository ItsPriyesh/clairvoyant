$(document).ready(function(){
  $("#submit").click(function() {
    $.ajax({
      url: 'http://localhost:8081/login',
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

loadDashboard = function(data) {
  console.log(data);
  localStorage.setItem('token', data.token);
  console.log(localStorage.getItem('token'));
  window.location = "./dash.html";
}