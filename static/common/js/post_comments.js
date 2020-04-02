myurl = '/comment/list/' + postid

var w = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
var h = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;


$(function () {
    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });
});

$(document).ready(function () {
    $.notify.defaults({ className: "success" });
    displaycomments()
  });

$(document).on('submit', '#comment-main', function (e) {
    e.preventDefault();
    
    content = $("#comment-main").find("#id_content").val();

    $.ajax({
        url: "/comment/create/"+postid,
        type: 'post',
        dataType: 'html',
        data: {
            'start': $('#id_startTime').val(),
            'end': $('#id_endTime').val(),
            'content': content,
            'csrfmiddlewaretoken': $("#csrfmiddlewaretoken").val()
        },
        success: function (data) {
            $("#comment-main").find("#id_content").val('')
            
            displaycomments()
            $('#pre-comment').load(document.URL + ' #pre-comment');
            $("#new-comment-submit").notify("Comment Added!", { position: "left" });
        }
    })
    
});


function displaycomments()
{
    $.ajax({
        url: myurl,
        type: 'get',
        dataType: 'html',
        success: function (data) {
            $('#comment-list').html(data)
    
            $('.deleteBtn').each((i, elm) => {
                $(elm).on("click", (e) => {
                    commentId = $(elm).data('id')
                    deletecomment(commentId)
                })
            })
    
            $('.updateBtn').each((i, elm) => {
                $(elm).on("click", (e) => {
                    commentId = $(elm).data('id')
                    editcomment(commentId)
                })
            })

            $('.replyBtn').each((i, elm) => {
                $(elm).on("click", (e) => {
                    e.preventDefault()
                    commentId = $(elm).data('id')
                    addreplybox(commentId)
                })
            })

            $('.likeBtnC').each((i, elm) => {
                $(elm).on("click", (e) => {
                    e.preventDefault()
                    commentId = $(elm).data('id')
                    likecomment(commentId)
                })
            })

            $('.dislikeBtnC').each((i, elm) => {
                $(elm).on("click", (e) => {
                    e.preventDefault()
                    commentId = $(elm).data('id')
                    dislikecomment(commentId)
                })
            })

            $('.likeBtnR').each((i, elm) => {
                $(elm).on("click", (e) => {
                    e.preventDefault()
                    replyId = $(elm).data('id')
                    likereply(replyId)
                })
            })

            $('.deleteBtnR').each((i, elm) => {
                $(elm).on("click", (e) => {
                    e.preventDefault()
                    replyId = $(elm).data('id')
                    deletereply(replyId)
                })
            })
    
        },
        error: function (data) {
        }
    });
}

function addreplybox(commentId)
{
    $.ajax({
        url: `/comment/${commentId}/reply`,
        type: 'get',
        dataType: 'html',
        data: {
            'start': $('#id_startTime').val(),
            'end': $('#id_endTime').val(),
            'csrfmiddlewaretoken': $("#csrfmiddlewaretoken").val()
        },
        success: function (data) {
            myid = "comment-" + commentId;
            
            $(".replyBtn[data-id=" + commentId + "]").hide()
            $(".commentReplies[data-id=" + commentId + "]").prepend(data)
            $(".commentReplyBox[data-id=" + commentId + "]").find("#id_content").hide()

            $(".cancelReplyBtn[data-id=" + commentId + "]").on("click", (e) => {
                $(".commentReplyBox[data-id=" + commentId + "]").remove()
                $(".replyBtn[data-id=" + commentId + "]").show()
            })

            $(".submitReplyBtn[data-id=" + commentId + "]").on("click", (e) => {
                submitreply(commentId)
            })
            $(".commentReplyBox[data-id=" + commentId + "]").find("#id_content").slideToggle("fast")
            $(".commentReplyBox[data-id=" + commentId + "]").find("#id_content").focus()
        },
    });

}

function submitreply(commentId)
{
    content = $(".commentReplyBox[data-id=" + commentId + "]").find("#id_content").val()

    if (content==="")
    {
        $(".commentReplyBox[data-id=" + commentId + "]").remove()
        $(".replyBtn[data-id=" + commentId + "]").show()
    }
    else
    {
        $.ajax({
            url: `/comment/${commentId}/reply`,
            type: 'post',
            dataType: 'html',
            data: {
                'start': $('#id_startTime').val(),
                'end': $('#id_endTime').val(),
                'content': content,
                'csrfmiddlewaretoken': $("#csrfmiddlewaretoken").val()
            },
            success: function (data) {

                $(".commentReplyBox[data-id=" + commentId + "]").remove()
                $(".replyBtn[data-id=" + commentId + "]").show()

                var replyId = $(data).data('id')
                var replyCount = $(data).data('crc')

                $(".commentReplies[data-id=" + commentId + "]").append(data)
                document.getElementById("repliesCntC-"+commentId).innerHTML = replyCount
                
                $(".likeBtnR[data-id=" + replyId + "]").on("click", (e) => {
                    likereply(replyId)
                })
    
                $(".deleteBtnR[data-id=" + replyId + "]").on("click", (e) => {
                    deletereply(replyId)
                })

                $('.replyM[data-id=' + replyId + ']').notify("Reply Added!", { position: "right" });
                
            },
        });        
    }
}

function deletereply(replyId)
{
    $.ajax({
        url: `/reply/delete/${replyId}`,
        type: 'post',
        dataType: 'json',
        data: {
            'start': $('#id_startTime').val(),
            'end': $('#id_endTime').val(),
            'csrfmiddlewaretoken': $("#csrfmiddlewaretoken").val()
        },
        success: function (data) {
            console.log(data)
            replyCount = data['crc']
            commentId = data['comment_id']
            $(".replyM[data-id=" + replyId + "]").remove()
            document.getElementById("repliesCntC-"+commentId).innerHTML = replyCount

            
        },
    });
}

function likereply(replyId)
{
    $.ajax({
        url: "/api/reply/"+replyId+"/like/", 
        method: "GET",
        data: {},
        success: function(data){
            if (data['liked'])
            {
                $(".likeBtnR[data-id=" + replyId + "]").css("color", "#4edcff")
                $(".likeBtnR1[data-id=" + replyId + "]").css("text-shadow", "0px 0px 7px")
            }
            else
            {
                $(".likeBtnR[data-id=" + replyId + "]").css("color", "")
                $(".likeBtnR1[data-id=" + replyId + "]").css("text-shadow", "")
            }

            document.getElementById("likesR-"+replyId).innerHTML = data['likes']        
        },
        error: function(error){

        }

    });
}


function deletecomment(commentId) {

    $.ajax({
        url: `/comment/delete/${commentId}`,
        type: 'post',
        dataType: 'json',
        success: function (data) {

            myid = "comment-" + commentId;
            $(document.getElementById(myid)).remove()

            $('#pre-comment').load(document.URL + ' #pre-comment');
        }
    });
}

function editcomment(commentId) {

    $.ajax({
        url: `/comment/update/${commentId}`,
        type: 'get',
        dataType: 'html',
        data: {
            'start': $('#id_startTime').val(),
            'end': $('#id_endTime').val(),
            'csrfmiddlewaretoken': $("#csrfmiddlewaretoken").val()
        },
        success: function (data) {
            myid = "comment-" + commentId;
            $(document.getElementById(myid)).html(data)


            $(".cancelBtn[data-id=" + commentId + "]").on("click", (e) => {
                cancel(commentId)
            })

            $(".saveBtn[data-id=" + commentId + "]").on("click", (e) => {
                updatecomment(commentId)
            })

            $(".likeBtnC[data-id=" + commentId + "]").on("click", (e) => {
                likecomment(commentId)
            })

            $(".dislikeBtnC[data-id=" + commentId + "]").on("click", (e) => {
                dislikecomment(commentId)
            })
        },
    });

    $('#pre-comment').load(document.URL + ' #pre-comment');
}



function cancel(commentId) {

    $.ajax({
        url: `/comment/${commentId}`,
        type: 'get',
        dataType: 'html',
        data: {
            'start': $('#id_startTime').val(),
            'end': $('#id_endTime').val(),
            'csrfmiddlewaretoken': $("#csrfmiddlewaretoken").val()
        },
        success: function (data) {
            myid = "comment-" + commentId;



            $(document.getElementById(myid)).html(data)


            $(".deleteBtn[data-id=" + commentId + "]").on("click", (e) => {
                deletecomment(commentId)
            })

            $(".updateBtn[data-id=" + commentId + "]").on("click", (e) => {
                editcomment(commentId)
            })

            $(".replyBtn[data-id=" + commentId + "]").on("click", (e) => {
                addreplybox(commentId)
            })

            $(".likeBtnC[data-id=" + commentId + "]").on("click", (e) => {
                likecomment(commentId)
            })

            $(".dislikeBtnC[data-id=" + commentId + "]").on("click", (e) => {
                dislikecomment(commentId)
            })
        },
    });

}


function updatecomment(commentId) {

    new_content = $(".commentForm[data-id=" + commentId + "]").find("#id_content").val()


    commentDict = "new_content"
    $.ajax({
        url: `/comment/updatefinal/${commentId}`,
        type: 'post',
        dataType: 'html',
        data: {
            'start': $('#id_startTime').val(),
            'end': $('#id_endTime').val(),
            'new_content': new_content,
            'csrfmiddlewaretoken': $("#csrfmiddlewaretoken").val()
        },
        success: function (data) {
            myid = "comment-" + commentId;
            $(document.getElementById(myid)).html(data)

            $(".deleteBtn[data-id=" + commentId + "]").on("click", (e) => {
                deletecomment(commentId)
            })

            $(".updateBtn[data-id=" + commentId + "]").on("click", (e) => {
                editcomment(commentId)
            })

            $(".replyBtn[data-id=" + commentId + "]").on("click", (e) => {
                addreplybox(commentId)
            })

            $(".likeBtnC[data-id=" + commentId + "]").on("click", (e) => {
                likecomment(commentId)
            })

            $(".dislikeBtnC[data-id=" + commentId + "]").on("click", (e) => {
                dislikecomment(commentId)
            })
        },
    });

}

function likecomment(commentId)
{
    $.ajax({
        url: "/api/comment/"+commentId+"/like/", 
        method: "GET",
        data: {},
        success: function(data){
            if (data['liked'])
            {
                $(".likeBtnC[data-id=" + commentId + "]").css("color", "#4edcff")
                $(".likeBtnC1[data-id=" + commentId + "]").css("text-shadow", "0px 0px 7px")
            }
            else
            {
                $(".likeBtnC[data-id=" + commentId + "]").css("color", "")
                $(".likeBtnC1[data-id=" + commentId + "]").css("text-shadow", "")
            }

            if (data['disliked'])
            {
                $(".dislikeBtnC[data-id=" + commentId + "]").css("color", "#4edcff")
                $(".dislikeBtnC1[data-id=" + commentId + "]").css("text-shadow", "0px 0px 7px")
            }
            else
            {
                $(".dislikeBtnC[data-id=" + commentId + "]").css("color", "")
                $(".dislikeBtnC1[data-id=" + commentId + "]").css("text-shadow", "")
            }

            document.getElementById("likesC-"+commentId).innerHTML = data['likes']
            document.getElementById("dislikesC-"+commentId).innerHTML = data['dislikes']
        
        },
        error: function(error){

        }

    });
}

function dislikecomment(commentId)
{
    $.ajax({
        url: "/api/comment/"+commentId+"/dislike/", 
        method: "GET",
        data: {},
        success: function(data){

            if (data['liked'])
            {
                $(".likeBtnC[data-id=" + commentId + "]").css("color", "#4edcff")
                $(".likeBtnC1[data-id=" + commentId + "]").css("text-shadow", "0px 0px 7px")
            }
            else
            {
                $(".likeBtnC[data-id=" + commentId + "]").css("color", "")
                $(".likeBtnC1[data-id=" + commentId + "]").css("text-shadow", "")
            }

            if (data['disliked'])
            {
                $(".dislikeBtnC[data-id=" + commentId + "]").css("color", "#4edcff")
                $(".dislikeBtnC1[data-id=" + commentId + "]").css("text-shadow", "0px 0px 7px")
            }
            else
            {
                $(".dislikeBtnC[data-id=" + commentId + "]").css("color", "")
                $(".dislikeBtnC1[data-id=" + commentId + "]").css("text-shadow", "")
            }
            
            document.getElementById("likesC-"+commentId).innerHTML = data['likes']
            document.getElementById("dislikesC-"+commentId).innerHTML = data['dislikes']
        
        },
        error: function(error){

        }

    });
}

function getCookie(c_name) {
    if (document.cookie.length > 0) {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1) {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start, c_end));
        }
    }
    return "";
}