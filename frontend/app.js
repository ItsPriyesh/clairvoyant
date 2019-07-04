$(document).ready(function(){
	$('.test').click(function() {
  $.ajax({
    url: 'http://localhost:8081/createUser',
    type: 'GET',
    // 'data' : {
    //   'paramater1' : 'value',
    //   'parameter2' : 'another value'
    // }
    
  }).done(function(data) {
  		console.log("done!");
        console.log(data);
  });
});
});