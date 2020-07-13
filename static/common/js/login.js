



var btnLogin = document.querySelector(".login-btn") 

var btnLoginText = document.querySelector(".login-btn-text") 
var btnLoginLoader = document.querySelector(".login-btn-loader") 
var btnLoginTick = document.querySelector(".login-tick") 
var btnLoginCross = document.querySelector(".login-cross") 

var inpUser = document.querySelector(".input-username") 
var inpPass = document.querySelector(".input-password") 
var url_login = '/login/';

var labelUser = document.querySelector(".label-username") 
var labelPass = document.querySelector(".label-password") 

const MINIMUM_PASSWORD_LENGTH = 8;
const MAXIMUM_PASSWORD_LENGTH = 45;
const MINIMUM_USERNAME_LENGTH = 3;
const MAXIMUM_USERNAME_LENGTH = 20;

btnLogin.addEventListener('click', listener_click_btnLogin);
inpUser.value = ""
inpPass.value = ""

ValidateUsername = function (username) {
    if (username.length < MINIMUM_USERNAME_LENGTH || username.length > MAXIMUM_USERNAME_LENGTH)
    {
        showMessage(`Username must be between ${MINIMUM_USERNAME_LENGTH} and ${MAXIMUM_USERNAME_LENGTH} characters`)
        return false;
    }
    else if (/\s/.test(username)) {
        // string contains some kind of whitespace
        showMessage('Invalid Username String')
        return false;
    }
    // check for invalid chars

    return true;
}

ValidatePassword = function (password) {
    if (password.length < MINIMUM_PASSWORD_LENGTH || password.length > MAXIMUM_PASSWORD_LENGTH)
    {
        showMessage(`Password must be between ${MINIMUM_PASSWORD_LENGTH} and ${MAXIMUM_PASSWORD_LENGTH} characters`)
        return false;
    }

    return true;
}

function listener_click_btnLogin(e)
{
    inpUser.value = inpUser.value.trim()
    if (inpUser.value.length === 0 || inpPass.value.length === 0)
    {
        showMessage('Please Fill Out Both Fields')
    }
    else if (!ValidateUsername(inpUser.value)) 
    {
        e.preventDefault()
        // showMessage('Invalid Username String')
    }
    else if (!ValidatePassword(inpPass.value)) 
    {
        e.preventDefault()
        // showMessage('Invalid Password String')
    }
    else 
    {
        e.preventDefault()
        inpUser.disabled = true
        inpPass.disabled = true

        btnLogin.disabled = true;
        btnLogin.classList.remove('enabled')

        labelUser.classList.add('label-disabled')
        labelPass.classList.add('label-disabled')

        btnLoginLoader.hidden = false;
        btnLoginText.hidden = true; 
        btnLogin.style.cursor = "default"

        showMessage('Please Wait')
        $.ajax({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }, 

            type: 'POST',
            url: url_login,
            data: {
                'username': inpUser.value,
                'password': inpPass.value
            },
            success: function(data){
                handler_Login(data);
            },
            error: function(error){
                console.log(error);
                addNotification(error, "error");
            }
        });
    }
};

const urlParams = new URLSearchParams(window.location.search);
var url_next = '/'
if (urlParams.has('next')) url_next = urlParams.get('next')


function handler_Login(data) 
{   
    console.log(data['message'])

    if (data['message'] === 'success')
    {
        btnLoginLoader.hidden = true;
        
        btnLoginTick.style.visibility = "visible"
        $('.login-tick').hide().fadeIn(200);

        showMessage('You will be redirected soon')
        setTimeout(redirectToUrl(url_next), 2000);
    }
    else if (data['message'] === 'failure')
    {
        inpUser.disabled = false
        inpPass.disabled = false

        inpUser.addEventListener("input", enableLoginButton);
        inpPass.addEventListener("input", enableLoginButton);


        labelUser.classList.remove('label-disabled')
        labelPass.classList.remove('label-disabled')

        btnLoginLoader.hidden = true;

        // show cross sign on login button until change/input
        btnLoginCross.style.visibility = "visible"
        $('.login-cross').hide().fadeIn(200);

        showMessage('Incorrect Username or Password')
    }
}

function enableLoginButton() {
    btnLogin.disabled = false;
    btnLogin.classList.add('enabled')
    btnLogin.style.cursor = "pointer"

    inpUser.removeEventListener("input", enableLoginButton);
    inpPass.removeEventListener("input", enableLoginButton);

    btnLoginCross.style.visibility = "hidden"
    btnLoginText.hidden = false
}

var messageBox = document.querySelector('.message-box') 

function redirectToUrl(url="/") {
    window.location.replace(url);
}

function showMessage(message)
{
    messageBox.innerHTML = message
    $('.message-box').hide().fadeIn(300);

}






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

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

