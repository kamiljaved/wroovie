
// ####################################
//
// csrf cookie
//
// ####################################

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


var csrftoken = getCookie('csrftoken');

var headers = new Headers();
headers.append('X-CSRFToken', csrftoken);

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}




const url_vote_post = '/post/vote/'

const url_vote_reply = '/reply/vote/'

function postUpvote(e, id)
{
    e.preventDefault()
    btn_upvote = document.getElementById(`pst-upvt-btn-${id}`)
    btn_downvote = document.getElementById(`pst-dnvt-btn-${id}`)
    div_score = document.getElementById(`pst-score-div-${id}`)
    voteAJAX({'post_id': id, 'vote': 'up'}, url_vote_post, btn_upvote, btn_downvote, div_score)
}

function postDownvote(e, id)
{
    e.preventDefault()
    btn_upvote = document.getElementById(`pst-upvt-btn-${id}`)
    btn_downvote = document.getElementById(`pst-dnvt-btn-${id}`)
    div_score = document.getElementById(`pst-score-div-${id}`)
    voteAJAX({'post_id': id, 'vote': 'down'}, url_vote_post, btn_upvote, btn_downvote, div_score)
}

function replyUpvote(e, id)
{
    e.preventDefault()
    btn_upvote = document.getElementById(`rply-upvt-btn-${id}`)
    btn_downvote = document.getElementById(`rply-dnvt-btn-${id}`)
    div_score = document.getElementById(`rply-score-div-${id}`)
    voteAJAX({'reply_id': id, 'vote': 'up'}, url_vote_reply, btn_upvote, btn_downvote, div_score)
}

function replyDownvote(e, id)
{
    e.preventDefault()
    btn_upvote = document.getElementById(`rply-upvt-btn-${id}`)
    btn_downvote = document.getElementById(`rply-dnvt-btn-${id}`)
    div_score = document.getElementById(`rply-score-div-${id}`)
    voteAJAX({'reply_id': id, 'vote': 'down'}, url_vote_reply, btn_upvote, btn_downvote, div_score)
}

function voteHandler(data, btn_upvote, btn_downvote, div_score) {
    if (data['error'])
    {
        addNotification(data["message"], "error");
    }
    else
    {
        if (data['upvoted'])
        {
            if (!btn_upvote.classList.contains('sel')) btn_upvote.classList.add('sel')
        }
        else
        {
            if (btn_upvote.classList.contains('sel')) btn_upvote.classList.remove('sel')
        }

        if (data['downvoted'])  
        {
            if (!btn_downvote.classList.contains('sel')) btn_downvote.classList.add('sel')
        }
        else
        {
            if (btn_downvote.classList.contains('sel')) btn_downvote.classList.remove('sel')
        }

        if('score' in data)
        {
            div_score.innerHTML = data['score']
        }
    }
}

function voteAJAX(data, url_vote, btn_upvote, btn_downvote, div_score)
{
    $.ajax({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }, 
        url: url_vote, 
        method: "POST",
        data: data,
        success: function(data){
            voteHandler(data, btn_upvote, btn_downvote, div_score);
        },
        error: function(error){
            console.log(error)
            addNotification(error, "error");
        }

    });
}