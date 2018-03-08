$(document).ready(function() {

  var form = $('#artist_form'),
      artist = $('#artist_name'),
      submit = $("#submit");
  
  	var searchRequest = null;
	
	$("input#artist_name").autocomplete({
	    minLength: 3,
	    source: function(request, response) {
	        $.ajax({
	            type: "POST",
	            url: "autocomplete.php",
	            dataType: "json",
	            data: form.serialize(),
	            delay: 100,
	            success: function(data) {
	                response($.map(data.items, function(item) {
                    return {
                        value: item.artist,
                        label: item.artist
                    };
                }));
	            }
	        });
		}
	});        


  form.on('input', '#artist_name', function() {
    //$(this).css('border-color', 'red');
  });
  
  submit.on('click', function(e) {

    e.preventDefault();
    $.ajax({
		type: "POST",
  		url: "artists.php",
  		data: form.serialize(),
  		dataType: "json",
  		success: function(data) {
  			$("ui-menu").hide();
  			$("#suggested_artists ul").empty();

			$("section#artist").animate({
  				top: 0
  			},function(){
  				var d = data.items;
  				for(var i = 0; i < d.length; i++) {
  					console.log(d[i].artist);
  					$("#suggested_artists ul").append('<li>'+d[i].artist+'</li>');
  				} 	
  			})

  					
  		}
	});
    /*if(validate()) {
     	$.ajax({
        type: "POST",
        url: "artists.php",
        data: form.serialize(),
        dataType: "json"
      }).done(function(data) {
      	console.log("DONE");
        if(data.success) {
       		artist.val('');
          //info.html('Message sent!').css('color', 'green').slideDown();
        } else {
          //info.html('Could not send mail! Sorry!').css('color', 'red').slideDown();
        }
      });
  	}*/
  });
  
  function validate() {
  	return true;
    /*var valid = true;
    var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    
    if(!regex.test(email.val())) {
      email.css('border-color', 'red');
      valid = false;
    }
    if($.trim(subject.val()) === "") {
      subject.css('border-color', 'red');
      valid = false;
    }
    if($.trim(message.val()) === "") {
      message.css('border-color', 'red');
      valid = false;
    }
    
    return valid;*/
  }

});
