
// TODO: maybe a waiting graphic section? wait times aren't long but could be confusing
// TODO: resize input or text to fit input for long band names
// TODO: size suggested artists text based on screen width?
// TODO: sizing for mobile
// TODO: how will autocomplete scale w/ userbase?

// TODO: hiding autocomplete after submit (clunky but done?)

$(document).ready(function() {

  var form = $('#artist_form'),
      artist = $('#artist_name'),
      submit = $("#submit");
  	
	var autocomp = $("input#artist_name").autocomplete({
	    select: function(event, ui) { 
        $(this).val(ui.item.label);
        submit.click();
      },
      minLength: 3,
	    source: function(request, response) {
	        $.ajax({
	            type: "POST",
	            url: "autocomplete.php",
	            dataType: "json",
	            data: form.serialize(),
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
	}).keypress(function (e) {
        if(e.which === 13) {
            $(this).autocomplete('disable');
            $(this).autocomplete('close');
        } else if (e.which != 13) {
          $(this).autocomplete('enable'); // todo: maybe a bit much?
        }     
  });      
  
  // todo: not quite a solution if we never lose focus on the input
  $("input#artist_name").focus(function(){
    $(this).autocomplete('enable');  
  })

  submit.on('click', function(e) {
    e.preventDefault();

    $.ajax({
		type: "POST",
  		url: "artists.php",
  		data: form.serialize(),
  		dataType: "json",
  		success: function(data) {
        if(!data) {
          alert("artist not in database, try the autocomplete feature");
          return;
        }

  			$("#suggested_artists ul").empty().hide();
        $("#suggested_albums ul").empty().hide();			

        if($("section#artist").css('top') != '0px') {
          $("section#artist").animate({
      				top: 0
      			},function(){
              getArtists(data);
      			})
        } else {
          getArtists(data);
        }
  		}
    });   
  });
});

$(window).resize(function(){
  setPosition($("#suggestions"));
})

function setPosition(elem,child) {
  var offset = $("input#artist_name").offset();
  var height = $("input#artist_name").outerHeight(true);

  $(elem).offset({
    left: offset.left,
    top: height - 20
  })

  if(child) {
    child.show({effect:'slide','duration':1000}); 
  }
}

function getArtists(data) {
  $("#suggested_artists ul").empty();

  $("#suggested_artists ul").append('<li id="you_might_like">You might like...</li>')
  colorize($('li#you_might_like'));

  for(var i = 0; i < data.length; i++) {
    $("#suggested_artists ul").append('<li><a class="artist_link" id="'+data[i].artist+'">'+data[i].artist +'</a></li>');
  } 

  $("a.artist_link").click(function(){
    getAlbums($(this));
  })
  
  setPosition($("#suggestions"),$("#suggested_artists ul"));
}

function getAlbums(elem) {
  let d = elem.attr('id');

  $.ajax({
    type: "POST",
    url: "albums.php",
    dataType: "json",
    data: {'artist': d },
    success: function(data) {

      $("#suggested_albums ul").empty();
      $("#suggested_albums ul").append('<li class="artist_title">'+data[0].artist+'</li>');

      for(var i = 0; i < data.length; i++) {
        $("#suggested_albums ul").append(
          '<li><a class="artist_link" id="'+data[i].name+'">'+data[i].name +
          ' ('+(data[i].mc_rating===null?'tbd':data[i].mc_rating)+')</a></li>');
      }

      $("#suggested_albums ul").append('<li class="back_to_artists">(back to artists)</li>');
      colorize($('li.artist_title'));

      $('li.artist_title').click(function(){
        $("input#artist_name").val(elem.text());

        //todo: set this up as a callback to avoid race condition!
        submit.click();
      })

      $('.back_to_artists').click(function(){
        $("#suggested_albums ul").hide({
            effect:'slide',
            duration: 300, 
            complete: function(){
              $("#suggested_artists ul").show({effect:'slide','duration':500})
            }
        });
        
      });
      
      $("#suggested_artists ul").hide({
        effect:'slide',
        'duration':300,
        complete: function(){
          setPosition($("#suggestions"),$("#suggested_albums ul"));
        }
      });
    }
  });
}

// assign random color to element
function colorize(elem) {
  var colors = ['darkorchid','darkgoldenrod','darkcyan','darkorange'];
  var random_color = colors[Math.floor(Math.random() * colors.length)];
  elem.css('color',random_color);
}
