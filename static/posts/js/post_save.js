
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




var url_post_save = `/post/save/`;


function postSaveToggle(e, id)
{
    e.preventDefault()
    $.ajax({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }, 
        url: url_post_save, 
        method: "POST",
        data: {
            'post_id':id
        },
        success: function(data){
            handler_postSaveToggle(data, id);
        },
        error: function(error){
            console.log(error)
            addNotification(error, "error");
        }

    });
} 

var saveBtn = document.querySelector(".post-options-button.save-btn")
var saveBtnText = saveBtn.querySelector(".post-options-button-text")

saveBtn.addEventListener("mouseenter", function(e) {
    if (saveBtn.classList.contains("sel")) saveBtnText.innerHTML = "Unsave"
})
saveBtn.addEventListener("mouseleave", function(e) {
    if (saveBtn.classList.contains("sel")) saveBtnText.innerHTML = "Saved"
})


function handler_postSaveToggle(data, id) 
{   
    if (data['redirect_to_login'])
    {
        //window.location.href = login_url
    }
    else
    {
        if (data['saved'])
        {
            if (!saveBtn.classList.contains("sel")) saveBtn.classList.add("sel")
            saveBtnText.innerHTML = "Saved"
        }
        else
        {
            if (saveBtn.classList.contains("sel")) saveBtn.classList.remove("sel")
            saveBtnText.innerHTML = "Save"
        }
    }
}




