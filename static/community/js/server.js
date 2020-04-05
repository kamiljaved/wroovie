
var url_join = `/c/${community_name}/join`;
var url_login = '/u/login';

if (user_is_authenticated)
{
    btnJoin.addEventListener('click', listener_click_btnJoin);
}

function listener_click_btnJoin(e)
{
    e.preventDefault()
    $.ajax({
        url: url_join, 
        method: "GET",
        data: {},
        success: function(data){
            handler_JoinToggle(data);
        },
        error: function(error){
            console.log(error)
        }

    });
} 

function handler_JoinToggle(data) 
{   
    if (data['redirect_to_login'])
    {

    }
    else
    {
        if (data['joined'])
        {
            if (user_is_authenticated)
            {
                btnJoinText.innerHTML = 'LEAVE';
                user_is_member = true
            }
        }
        else
        {
            if (user_is_authenticated)
            {
                btnJoinText.innerHTML = 'JOIN';
                user_is_member = false
            }
        }
    }
}