$(document).ready(function(){
  $("#submit").click(function() {
    $.ajax({
      url: 'http://localhost:8081/login',
      type: 'GET',
      'data' : {
        'email' : $("#login").val(),
        'password' : $("#password").val(),
      }
    }).done(function(data) {
        console.log('done!');
        console.log(data);
        // load user dashboard
    });
  });
});

loadDashboard = function() {
  
}