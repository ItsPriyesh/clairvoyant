$(document).ready(function(){
  $('.test').click(function() {
    $.ajax({
      url: 'http://localhost:8081/createUser',
      type: 'POST',
      'data' : {
        'firstName' : 'value',
        'lastName' : 'another value',
        'email' : 'another value',
        'password' : 'another value',
      }
    }).done(function(data) {
        console.log('done!');
        console.log(data);
    });
  });
});