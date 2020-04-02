var rateUrl_1 = '/api/post/' + postid + '/rate/1'
var rateUrl_2 = '/api/post/' + postid + '/rate/2'
var rateUrl_3 = '/api/post/' + postid + '/rate/3'
var rateUrl_4 = '/api/post/' + postid + '/rate/4'
var rateUrl_5 = '/api/post/' + postid + '/rate/5'

$(document).ready(function () {
  addstarclicks()
  animatebars(ratings_1_percentage, ratings_2_percentage, ratings_3_percentage, ratings_4_percentage, ratings_5_percentage)
  showuserrating(user_rating_initial)
});


function addstarclicks()
{ 
  $("i#star1").on('click', function(e){
    e.preventDefault()
    $.ajax({
        url: rateUrl_1, 
        method: "GET",
        data: {},
        success: function(data){
          document.getElementById("rnum").innerHTML = data["new_rating"].toFixed(1)
          document.getElementById("rct").innerText = " " + data["ratings_count"].toString() + " total"
          $("#strper").css("width", data["rating_percentage"].toString() + "%");
          document.getElementById("rc5").innerHTML = data["ratings_5"]
          document.getElementById("rc4").innerHTML = data["ratings_4"]
          document.getElementById("rc3").innerHTML = data["ratings_3"]
          document.getElementById("rc2").innerHTML = data["ratings_2"]
          document.getElementById("rc1").innerHTML = data["ratings_1"]         
          showuserrating(data["user_rating"])
          animatebars(data["ratings_1_percentage"], data["ratings_2_percentage"], data["ratings_3_percentage"], data["ratings_4_percentage"], data["ratings_5_percentage"])
        },
        error: function(error){

        }

    });
  })
  $("i#star2").on('click', function(e){
    e.preventDefault()
    $.ajax({
        url: rateUrl_2, 
        method: "GET",
        data: {},
        success: function(data){
          document.getElementById("rnum").innerHTML = data["new_rating"].toFixed(1)
          document.getElementById("rct").innerText = " " + data["ratings_count"].toString() + " total"
          $("#strper").css("width", data["rating_percentage"].toString() + "%");
          document.getElementById("rc5").innerHTML = data["ratings_5"]
          document.getElementById("rc4").innerHTML = data["ratings_4"]
          document.getElementById("rc3").innerHTML = data["ratings_3"]
          document.getElementById("rc2").innerHTML = data["ratings_2"]
          document.getElementById("rc1").innerHTML = data["ratings_1"]         
          showuserrating(data["user_rating"])
          animatebars(data["ratings_1_percentage"], data["ratings_2_percentage"], data["ratings_3_percentage"], data["ratings_4_percentage"], data["ratings_5_percentage"])
        },
        error: function(error){

        }

    });
  })
  $("i#star3").on('click', function(e){
    e.preventDefault()
    $.ajax({
        url: rateUrl_3, 
        method: "GET",
        data: {},
        success: function(data){
          document.getElementById("rnum").innerHTML = data["new_rating"].toFixed(1)
          document.getElementById("rct").innerText = " " + data["ratings_count"].toString() + " total"
          $("#strper").css("width", data["rating_percentage"].toString() + "%");
          document.getElementById("rc5").innerHTML = data["ratings_5"]
          document.getElementById("rc4").innerHTML = data["ratings_4"]
          document.getElementById("rc3").innerHTML = data["ratings_3"]
          document.getElementById("rc2").innerHTML = data["ratings_2"]
          document.getElementById("rc1").innerHTML = data["ratings_1"]         
          showuserrating(data["user_rating"])
          animatebars(data["ratings_1_percentage"], data["ratings_2_percentage"], data["ratings_3_percentage"], data["ratings_4_percentage"], data["ratings_5_percentage"])
        },
        error: function(error){

        }

    });
  })
  $("i#star4").on('click', function(e){
    e.preventDefault()
    $.ajax({
        url: rateUrl_4, 
        method: "GET",
        data: {},
        success: function(data){
          document.getElementById("rnum").innerHTML = data["new_rating"].toFixed(1)
          document.getElementById("rct").innerText = " " + data["ratings_count"].toString() + " total"
          $("#strper").css("width", data["rating_percentage"].toString() + "%");
          document.getElementById("rc5").innerHTML = data["ratings_5"]
          document.getElementById("rc4").innerHTML = data["ratings_4"]
          document.getElementById("rc3").innerHTML = data["ratings_3"]
          document.getElementById("rc2").innerHTML = data["ratings_2"]
          document.getElementById("rc1").innerHTML = data["ratings_1"]         
          showuserrating(data["user_rating"])
          animatebars(data["ratings_1_percentage"], data["ratings_2_percentage"], data["ratings_3_percentage"], data["ratings_4_percentage"], data["ratings_5_percentage"])
        },
        error: function(error){

        }

    });
  })
  $("i#star5").on('click', function(e){
    e.preventDefault()
    $.ajax({
        url: rateUrl_5, 
        method: "GET",
        data: {},
        success: function(data){
          document.getElementById("rnum").innerHTML = data["new_rating"].toFixed(1)
          document.getElementById("rct").innerText = " " + data["ratings_count"].toString() + " total"
          $("#strper").css("width", data["rating_percentage"].toString() + "%");
          document.getElementById("rc5").innerHTML = data["ratings_5"]
          document.getElementById("rc4").innerHTML = data["ratings_4"]
          document.getElementById("rc3").innerHTML = data["ratings_3"]
          document.getElementById("rc2").innerHTML = data["ratings_2"]
          document.getElementById("rc1").innerHTML = data["ratings_1"]         
          showuserrating(data["user_rating"])
          animatebars(data["ratings_1_percentage"], data["ratings_2_percentage"], data["ratings_3_percentage"], data["ratings_4_percentage"], data["ratings_5_percentage"])
        },
        error: function(error){

        }

    });
  })
}

function showuserrating(r)
{
  $("#star1").removeClass("active");
  $("#star2").removeClass("active");
  $("#star3").removeClass("active");
  $("#star4").removeClass("active");
  $("#star5").removeClass("active");
  if (r>0) { $("#star1").addClass("active"); }
  if (r>1) { $("#star2").addClass("active"); }
  if (r>2) { $("#star3").addClass("active"); }
  if (r>3) { $("#star4").addClass("active"); }
  if (r>4) { $("#star5").addClass("active"); }
}

function animatebars(r1, r2, r3, r4, r5) {
  $('.bar span').hide();
  $('#bar-five').animate({
    width: r5
  }, 1000);
  $('#bar-four').animate({
    width: r4
  }, 1000);
  $('#bar-three').animate({
    width: r3
  }, 1000);
  $('#bar-two').animate({
    width: r2
  }, 1000);
  $('#bar-one').animate({
    width: r1
  }, 1000);

  setTimeout(function () {
    $('.bar span').fadeIn('slow');
  }, 1000);
}


$("#star1").hover(function () {
  $(this).css("text-shadow", " 0px 0px 2px rgb(0, 0, 0)");
  $(this).css("color", "yellow");
}, function () {
  $(this).css("text-shadow", " 0px 0px 0px");
  $(this).css("color", "");
});

$("#star2").hover(function () {
  $("#star1").css("text-shadow", " 0px 0px 2px rgb(0, 0, 0)"); $("#star1").css("color", "yellow");
  $(this).css("text-shadow", " 0px 0px 2px rgb(0, 0, 0)"); $(this).css("color", "yellow");
}, function () {
  $("#star1").css("text-shadow", " 0px 0px 0px"); $("#star1").css("color", "");
  $(this).css("text-shadow", " 0px 0px 0px"); $(this).css("color", "");
});

$("#star3").hover(function () {
  $("#star1").css("text-shadow", " 0px 0px 2px rgb(0, 0, 0)"); $("#star1").css("color", "yellow");
  $("#star2").css("text-shadow", " 0px 0px 2px rgb(0, 0, 0)"); $("#star2").css("color", "yellow");
  $(this).css("text-shadow", " 0px 0px 2px rgb(0, 0, 0)"); $(this).css("color", "yellow");
}, function () {
  $("#star1").css("text-shadow", " 0px 0px 0px"); $("#star1").css("color", "");
  $("#star2").css("text-shadow", " 0px 0px 0px"); $("#star2").css("color", "");
  $(this).css("text-shadow", " 0px 0px 0px"); $(this).css("color", "");
});

$("#star4").hover(function () {
  $("#star1").css("text-shadow", " 0px 0px 2px rgb(0, 0, 0)"); $("#star1").css("color", "yellow");
  $("#star2").css("text-shadow", " 0px 0px 2px rgb(0, 0, 0)"); $("#star2").css("color", "yellow");
  $("#star3").css("text-shadow", " 0px 0px 2px rgb(0, 0, 0)"); $("#star3").css("color", "yellow");
  $(this).css("text-shadow", " 0px 0px 2px rgb(0, 0, 0)"); $(this).css("color", "yellow");
}, function () {
  $("#star1").css("text-shadow", " 0px 0px 0px"); $("#star1").css("color", "");
  $("#star2").css("text-shadow", " 0px 0px 0px"); $("#star2").css("color", "");
  $("#star3").css("text-shadow", " 0px 0px 0px"); $("#star3").css("color", "");
  $(this).css("text-shadow", " 0px 0px 0px"); $(this).css("color", "");
});

$("#star5").hover(function () {
  $("#star1").css("text-shadow", " 0px 0px 2px rgb(0, 0, 0)"); $("#star1").css("color", "yellow");
  $("#star2").css("text-shadow", " 0px 0px 2px rgb(0, 0, 0)"); $("#star2").css("color", "yellow");
  $("#star3").css("text-shadow", " 0px 0px 2px rgb(0, 0, 0)"); $("#star3").css("color", "yellow");
  $("#star4").css("text-shadow", " 0px 0px 2px rgb(0, 0, 0)"); $("#star4").css("color", "yellow");
  $(this).css("text-shadow", " 0px 0px 2px rgb(0, 0, 0)"); $(this).css("color", "yellow");
}, function () {
  $("#star1").css("text-shadow", " 0px 0px 0px"); $("#star1").css("color", "");
  $("#star2").css("text-shadow", " 0px 0px 0px"); $("#star2").css("color", "");
  $("#star3").css("text-shadow", " 0px 0px 0px"); $("#star3").css("color", "");
  $("#star4").css("text-shadow", " 0px 0px 0px"); $("#star4").css("color", "");
  $(this).css("text-shadow", " 0px 0px 0px"); $(this).css("color", "");
});

