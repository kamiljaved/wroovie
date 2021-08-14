
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



var url_join = `/c/${community_name}/join/`;
var url_login = '/login';
var url_login_redirect = url_login+'/?next='+request_path;

if (user_is_authenticated && btnJoin !== null)
{
    btnJoin.addEventListener('click', listener_click_btnJoin);
}

function listener_click_btnJoin(e)
{
    e.preventDefault()
    $.ajax({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }, 
        url: url_join, 
        method: "POST",
        data: {},
        success: function(data){
            handler_JoinToggle(data);
        },
        error: function(error){
            console.log(error)
            addNotification(error, "error");
        }

    });
} 

function handler_JoinToggle(data) 
{
    if (data['error'])
    {
        if ('redirect_to_login' in data)
        {
            addNotification(data['message'], "warning");
            if (data['redirect_to_login']) window.location.href = url_login_redirect
        }
        else if ('message' in data)
        {
            addNotification(data['message'], "warning");
        }
    }   
    else
    {
        if (data['joined'])
        {
            if (user_is_authenticated)
            {
                btnJoinText.innerHTML = 'JOINED';
                user_is_member = true
                if(!joinTick.classList.contains('fa-secondary')) joinTick.classList.add('fa-secondary');
            }
        }
        else
        {
            if (user_is_authenticated)
            {
                btnJoinText.innerHTML = 'JOIN';
                user_is_member = false

                if(joinTick.classList.contains('fa-secondary')) joinTick.classList.remove('fa-secondary');
            }
        }
    }

}