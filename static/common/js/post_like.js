var likeUrl = '/api/post/'+postid+'/like/'
var dislikeUrl = '/api/post/'+postid+'/dislike/'

$("#likeBtn").click(function(e){
    e.preventDefault()
    $.ajax({
        url: likeUrl, 
        method: "GET",
        data: {},
        success: function(data){
            $('#likeBtn').load(document.URL +  ' #likeBtn');
            $('#dislikeBtn').load(document.URL +  ' #dislikeBtn');
            $('#viewsCnt').load(document.URL +  ' #viewsCnt');
        },
        error: function(error){

        }

    });
});

$("#dislikeBtn").click(function(e){
    e.preventDefault()
    $.ajax({
        url: dislikeUrl, 
        method: "GET",
        data: {},
        success: function(data){
            $('#likeBtn').load(document.URL +  ' #likeBtn');
            $('#dislikeBtn').load(document.URL +  ' #dislikeBtn');
            $('#viewsCnt').load(document.URL +  ' #viewsCnt');
        },
        error: function(error){

        }

    });
});