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


// ####################################
//
// page 1 - email
//
// ####################################

var pageNo = 1

var btnNext = document.querySelector(".next-btn") 

var btnNextText = document.querySelector(".next-btn-text") 
var btnNextLoader = document.querySelector(".next-btn-loader") 
var btnNextTick = document.querySelector(".next-tick") 
var btnNextCross = document.querySelector(".next-cross") 

var inpEmail = document.querySelector('.input-email')
var inpEmailBox = document.querySelector('.inp-wrap.email-box')
var labelEmail = document.querySelector(".label-email") 

var url_testEmail = '/register/test-email/';

////////
var boolEmailSelected = false
var emailSelected = ''
////////

btnNext.addEventListener('click', listener_click_btnNext);
inpEmail.value = ""

inpEmail.focus()

// inpEmail.addEventListener('input' , function() {
//     var errorPreviously = inpEmailBox.classList.contains('inp-error')
//     if(errorPreviously) inpEmailBox.classList.remove('inp-error')
// })


inpEmail.addEventListener('input' , listener_input_inpEmail)

function listener_input_inpEmail ()
{
    var errorPreviously = inpEmailBox.classList.contains('inp-error')
    if (inpEmail.value.length === 0)
    {
        if(errorPreviously) inpEmailBox.classList.remove('inp-error')
    }
    else if (ValidateEmail(inpEmail.value.trim(), false))
    {   
        if (errorPreviously)
        inpEmailBox.classList.remove('inp-error')
    }
    else if (!errorPreviously)
    {
        inpEmailBox.classList.add('inp-error')
    }
}

ValidateEmail = function (email, bShowMsg=true) 
{
    if (/\s/.test(email) || !(/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email))) 
    {
        // string contains some kind of whitespace or email structure invalid
        if (bShowMsg) showMessagePage1('Invalid EMAIL address', 'error')
        
        return false;
    }

    return true;
}

function listener_click_btnNext(e)
{  
    var errorPreviously = inpEmailBox.classList.contains('inp-error')
    if(!errorPreviously) inpEmailBox.classList.remove('inp-error')

    inpEmail.value = inpEmail.value.trim()
    if (inpEmail.value.length === 0)
    {
        showMessagePage1('Please fill out the EMAIL field', 'error')
    }
    else if (!ValidateEmail(inpEmail.value)) 
    {
        e.preventDefault()
        inpEmail.focus()
        if (!inpEmailBox.classList.contains('inp-error')) inpEmailBox.classList.add('inp-error')
        // showMessagePage1('Invalid Username String')
    }
    else 
    {
        e.preventDefault()
        inpEmail.disabled = true

        btnNext.disabled = true;
        btnNext.classList.remove('enabled')

        labelEmail.classList.add('label-disabled')

        btnNextLoader.hidden = false;
        btnNextText.hidden = true; 
        btnNext.style.cursor = "default"

        showMessagePage1('Please Wait')
        $.ajax({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }, 

            type: 'POST',
            url: url_testEmail,
            data: {
                'email': inpEmail.value,
            },
            success: function(data){
                handler_Email(data);
            },
            error: function(error){
                console.log(error)

                // show error message
                showMessagePage1('An unknown error occurred. Please try again later.', 'error')

                // enable button and input fields
                enableNextButton()
    
                labelEmail.classList.remove('label-disabled')
            
                // do all just in case
                btnNextCross.style.visibility = "hidden"
                btnNextTick.style.visibility = "hidden"
                btnNextLoader.hidden = true;
        
                inpEmail.disabled = false; 
                inpEmail.focus()

            }
        });
    }
};


function handler_Email(data) 
{   
    console.log(data['message'])

    if (data['message'] === 'available')
    {
        emailSelected = data['email']
        if (emailSelected === inpEmail.value)
            boolEmailSelected = true
        else 
        {
            inpEmail.disabled = false

            inpEmail.addEventListener("input", enableNextButton);
            
            labelEmail.classList.remove('label-disabled')
    
            btnNextLoader.hidden = true;
    
            // show cross sign on login button until change/input
            btnNextCross.style.visibility = "visible"
            $('.next-cross').hide().fadeIn(200);
    
            showMessagePage1('An unknown error occurred. Please try again.', 'error')
            inpEmailBox.classList.add('inp-error')

            emailSelected = ''
            return
        }
        btnNextLoader.hidden = true;
        
        btnNextTick.style.visibility = "visible"
        $('.next-tick').hide().fadeIn(200);

        showMessagePage1('EMAIL address is valid and available', 'success', 200, hideMessageBoxPage1, 3000)

        setTimeout(showPage2, 1000)
    }
    else if (data['message'] === 'unavailable')
    {
        inpEmail.disabled = false

        inpEmail.addEventListener("input", enableNextButton);
        
        labelEmail.classList.remove('label-disabled')

        btnNextLoader.hidden = true;

        // show cross sign on login button until change/input
        btnNextCross.style.visibility = "visible"
        $('.next-cross').hide().fadeIn(200);

        showMessagePage1('This EMAIL address is already in use', 'error')
        inpEmailBox.classList.add('inp-error')
    }
    else if (data['message'] === 'invalid')
    {
        console.log(data['error'])
        inpEmail.disabled = false

        inpEmail.addEventListener("input", enableNextButton);
        
        labelEmail.classList.remove('label-disabled')

        btnNextLoader.hidden = true;

        // show cross sign on next button until change/input
        btnNextCross.style.visibility = "visible"
        $('.next-cross').hide().fadeIn(200);

        showMessagePage1('Invalid EMAIL address', 'error')
        inpEmailBox.classList.add('inp-error')
    }
}

function enableNextButton(rmvEvntLstnr = true) {
    btnNext.disabled = false;
    btnNext.classList.add('enabled')
    btnNext.style.cursor = "pointer"

    if (rmvEvntLstnr)
    {
        inpEmail.removeEventListener("input", enableNextButton);
    }
    btnNextCross.style.visibility = "hidden"
    btnNextText.hidden = false
}

var messageBoxPage1 = document.querySelector('.message-box.page-1') 

function showMessagePage1(message, type='info', time=200, callback=null, callback_timeout=null)
{
    messageBoxPage1.innerHTML = message
    
    var color = '#fff'        
    if (type === 'success')           color = 'rgb(119, 235, 119)'
    else if (type === 'error')    color = 'rgb(243, 57, 57)'

    if (callback)
        if (callback_timeout)
            $('.message-box.page-1').hide().css('color', color).fadeIn(time, function() {setTimeout(callback, callback_timeout)});
        else    $('.message-box.page-1').hide().css('color', color).fadeIn(time, callback);
    else    $('.message-box.page-1').hide().css('color', color).fadeIn(time);
}

function hideMessageBoxPage1(time=200, callback=null, callback_timeout=null)
{   
    var color = '#fff'        
    $('.message-box.page-1').fadeOut(time, function() {
        messageBoxPage1.innerHTML = 'No Message'
        $('.message-box.page-1').css('color', color)
        if (callback) 
            if (callback_timeout) setTimeout(callback(), callback_timeout)
            else callback()
    })
}

$('.signup-page-2').css('transform', 'translateX(+100%)').css('opacity', '0')


var previewEmail = document.querySelector('.preview-email')
var previewUsername = document.querySelector('.preview-username')

previewUsername.innerHTML = ""

function showPage2() {
    if (pageNo === 2) return

    // $('.signup-page-1 input').prop('disabled', true)

    if (boolEmailSelected)
    {    
        console.log(emailSelected)

        pageNo = 2
        
        // show next page
        $('.signup-page-1').css('transform', 'translateX(-100%').css('opacity', '0')
        setTimeout(function() {$('.signup-page-1').addClass('signup-page-hidden')},400)
    
        $('.signup-page-2').removeClass('signup-page-hidden').css('transform', 'translateX(0%)').css('opacity', '1')

        // show email on page
        previewEmail.innerHTML = emailSelected.toLowerCase()
        previewUsername.innerHTML = ''

        $('.preview-email').hide().fadeIn(1000)
        $('.preview-username').hide().fadeIn(1000)

        setTimeout(function() {inpUser.focus()}, 500)
        
    }
    else
    {
        // show unknown error
        return
    }
    
}

// ####################################
//
// page 2 - username and password
//
// ####################################

// console.log(document.querySelector('.candy.page-2').offsetHeight)
// $('.signup-page-1 .candy ').css('transition', 'all 400ms ease-in-out').css('opacity', '0')
// $('.signup-page-1 .container > *').not(".signup-page-1 .container > .message-box.page-1").css('transition', 'all 400ms ease-in-out').css('opacity', '0')
// $('.signup-page-1 .container').append("<div class='loader-big'></div>")
// $('.loader-big').hide().fadeIn(2000)
// showMessagePage1("what")

var inpPass1 = document.querySelector('.input-password-1')
var inpPass1Box = document.querySelector('.inp-wrap.password-1-box')
var inpPass2 = document.querySelector('.input-password-2')
var inpPass2Box = document.querySelector('.inp-wrap.password-2-box')

inpPass2.addEventListener('input' , listener_input_inpPass12)
inpPass1.addEventListener('input' , listener_input_inpPass12)

function listener_input_inpPass12 ()
{
    var errorPreviously = inpPass2Box.classList.contains('inp-error')
    if (inpPass2.value.length === 0 || inpPass1.value.length ===0)
    {
        if(errorPreviously) inpPass2Box.classList.remove('inp-error')
    }
    else if (matchPasswords())
    {   
        if (errorPreviously)
        inpPass2Box.classList.remove('inp-error')
    }
    else if (!errorPreviously)
    {
        inpPass2Box.classList.add('inp-error')
    }
}

function matchPasswords() {
    return inpPass1.value === inpPass2.value
}

var btnSignup = document.querySelector(".signup-btn") 
var btnBack = document.querySelector(".back-btn") 

var btnSignupText = document.querySelector(".signup-btn-text") 
var btnSignupLoader = document.querySelector(".signup-btn-loader") 
var btnSignupTick = document.querySelector(".signup-tick") 
var btnSignupCross = document.querySelector(".signup-cross") 

var inpUser = document.querySelector(".input-username") 
var inpPass1 = document.querySelector(".input-password-1") 
var inpPass2 = document.querySelector(".input-password-2") 
var url_signup = '/register/';

var inpUserBox = document.querySelector('.inp-wrap.username-box')

var labelUser = document.querySelector(".label-username") 
var labelPass1 = document.querySelector(".label-password-1")
var labelPass2 = document.querySelector(".label-password-2") 

const MINIMUM_PASSWORD_LENGTH = 8;
const MAXIMUM_PASSWORD_LENGTH = 45;
const MINIMUM_USERNAME_LENGTH = 3;
const MAXIMUM_USERNAME_LENGTH = 20;

btnBack.addEventListener('click', listener_click_btnBack);
btnSignup.addEventListener('click', listener_click_btnSignup);
inpUser.value = ""
inpPass1.value = ""
inpPass2.value = ""

inpUser.addEventListener('input', checkShowPreviewUsername)
inpUser.addEventListener('change', checkShowPreviewUsername)

inpUser.addEventListener('input' , listener_input_inpUser)
inpPass1.addEventListener('input' , listener_input_inpPass1)

function listener_input_inpUser ()
{
    var errorPreviously = inpUserBox.classList.contains('inp-error')
    if (inpUser.value.length === 0)
    {
        if(errorPreviously) inpUserBox.classList.remove('inp-error')
    }
    else if (ValidateUsername(inpUser.value.trim(), false))
    {   
        if (errorPreviously)
        inpUserBox.classList.remove('inp-error')
    }
    else if (!errorPreviously)
    {
        inpUserBox.classList.add('inp-error')
    }
}

function listener_input_inpPass1()
{
    var errorPreviously = inpPass1Box.classList.contains('inp-error')
    if (inpPass1.value.length === 0)
    {
        if(errorPreviously) inpPass1Box.classList.remove('inp-error')
    }
    else if (ValidatePassword(inpPass1.value, false))
    {   
        if (errorPreviously)
        inpPass1Box.classList.remove('inp-error')
    }
    else if (!errorPreviously)
    {
        inpPass1Box.classList.add('inp-error')
    }
}

function checkShowPreviewUsername()
{
    if (ValidateUsername(inpUser.value.trim(), false))
    {
        previewUsername.innerHTML = inpUser.value.trim()
    }
    else
    {
        previewUsername.innerHTML = ''
    }
}

ValidateUsername = function (username, bShowMsg=true) {
    if (username.length < MINIMUM_USERNAME_LENGTH || username.length > MAXIMUM_USERNAME_LENGTH)
    {
        if (bShowMsg) showMessagePage2(`Username must be between ${MINIMUM_USERNAME_LENGTH} and ${MAXIMUM_USERNAME_LENGTH} characters`, 'error')
        return false;
    }
    else if (/\s/.test(username)) {
        // string contains some kind of whitespace
        if(bShowMsg) showMessagePage2('Invalid Username String', 'error')
        return false;
    }
    // check for invalid chars

    return true;
}

ValidatePassword = function (password, bShowMsg=true) {
    if (password.length < MINIMUM_PASSWORD_LENGTH || password.length > MAXIMUM_PASSWORD_LENGTH)
    {
        if (bShowMsg) showMessagePage2(`Password must be between ${MINIMUM_PASSWORD_LENGTH} and ${MAXIMUM_PASSWORD_LENGTH} characters`, 'error')
        return false;
    }

    return true;
}

function listener_click_btnBack(e)
{
    // e.preventDefault() 
    // back button resets the form page 2 fields already (type='reset')

    if (pageNo == 1) return 

    pageNo = 1

    // show previous page
    $('.signup-page-2').css('transform', 'translateX(+100%').css('opacity', '0')
    setTimeout(function() {$('.signup-page-2').addClass('signup-page-hidden')},400)

    $('.signup-page-1').removeClass('signup-page-hidden').css('transform', 'translateX(0%)').css('opacity', '1')

    // disable page-2 elements

    
    
    $('.preview-email').fadeOut(1000, function() { previewEmail.innerHTML = '' })
    $('.preview-username').fadeOut(1000, function() { previewUsername.innerHTML = '' })

    // enable page-1 elements

    setTimeout(function() 
    {
        enableNextButton(false)
    
        labelEmail.classList.remove('label-disabled')
    
        // do all just in case
        btnNextCross.style.visibility = "hidden"
        btnNextTick.style.visibility = "hidden"
        btnNextLoader.hidden = true;

        inpEmail.disabled = false; 
        inpEmail.focus()

    }, 600)
}

function listener_click_btnSignup(e)
{  
    inpUser.value = inpUser.value.trim()
    if (inpUser.value.length === 0 || inpPass1.value.length === 0 || inpPass2.value.length === 0)
    {
        showMessagePage2('Please fill out all the fields', 'error')
    }
    else if (!ValidateUsername(inpUser.value)) 
    {
        e.preventDefault()
        inpUser.focus()
        if (!inpUserBox.classList.contains('inp-error')) inpUserBox.classList.add('inp-error')
        // showMessagePage2('Invalid Username String')
    }
    else if (!ValidatePassword(inpPass1.value)) 
    {
        e.preventDefault()
        inpPass1.focus()
        if (!inpPass1.classList.contains('inp-error')) inpPass1.classList.add('inp-error')
        // showMessagePage2('Invalid Password String')
    }
    else if (!matchPasswords())
    {
        e.preventDefault()
        inpPass2.focus()
        if (!inpPass2.classList.contains('inp-error')) inpPass2.classList.add('inp-error')
        showMessagePage2('Passwords do not match', 'error')
    }
    else 
    {
        e.preventDefault()
        inpUser.disabled = true
        inpPass1.disabled = true
        inpPass2.disabled = true

        btnSignup.disabled = true;
        btnSignup.classList.remove('enabled')
        btnBack.disabled = true;
        btnBack.classList.remove('enabled')

        labelUser.classList.add('label-disabled')
        labelPass1.classList.add('label-disabled')
        labelPass2.classList.add('label-disabled')

        btnSignupLoader.hidden = false;
        btnSignupText.hidden = true; 
        btnSignup.style.cursor = "default"
        btnBack.style.cursor = "default"

        // TODO: hide back button ???

        showMessagePage2('Please Wait')
        $.ajax({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }, 

            type: 'POST',
            url: url_signup,
            data: {
                'username': inpUser.value,
                'password1': inpPass1.value,
                'password2':inpPass2.value,
                'email': emailSelected
            },
            success: function(data){
                handler_Signup(data);
            },
            error: function(error){
                console.log(error)
                
                // show error message
                showMessagePage2('An unknown error occurred. Please try again later.', 'error')
    
                labelUser.classList.remove('label-disabled')
                labelPass1.classList.remove('label-disabled')
                labelPass2.classList.remove('label-disabled')

                // do all just in case
                btnSignupCross.style.visibility = "hidden"
                btnSignupTick.style.visibility = "hidden"
                btnSignupLoader.hidden = true;
        
                inpUser.disabled = false; 
                inpPass1.disabled = false; 
                inpPass2.disabled = false; 
                
                inpUser.focus()
                
                // TODO: show back button if hidden ???

                // enable button and input fields
                enableSignupButton()
                enableBackButton()

                // TODO: reset to page 1 ???
            }
        });
    }
};

function handler_Signup(data) 
{   
    console.log(data['message'])

    if (data['message'] === 'created')
    {
        var account = data['account']

        btnSignupLoader.hidden = true;
        
        btnSignupTick.style.visibility = "visible"
        $('.signup-tick').hide().fadeIn(200);

        showMessagePage2(`Account for \'${account['username']}\' successfully created. You are now being redirected to the login page.`, 'success')
        setTimeout(redirectToLogin, 3000);
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
        btnSignupCross.style.visibility = "visible"
        $('.signup-cross').hide().fadeIn(200);

        showMessagePage2('Incorrect Username or Password', 'error')
    }
}

function enableSignupButton(rmvEvntLstnr = true) {
    btnSignup.disabled = false;
    btnSignup.classList.add('enabled')
    btnSignup.style.cursor = "pointer"

    if (rmvEvntLstnr)
    {
        inpUser.removeEventListener("input", enableSignupButton);
        inpPass1.removeEventListener("input", enableSignupButton);
        inpPass2.removeEventListener("input", enableSignupButton);
    }

    btnSignupCross.style.visibility = "hidden"
    btnSignupText.hidden = false
}

function enableBackButton(rmvEvntLstnr = true) {
    btnBack.disabled = false;
    btnBack.classList.add('enabled')
    btnBack.style.cursor = "pointer"

    btnBackText.hidden = false
}

var messageBoxPage2 = document.querySelector('.message-box.page-2') 

function showMessagePage2(message, type='info', time=200, callback=null, callback_timeout=null)
{
    messageBoxPage2.innerHTML = message
    
    var color = '#fff'        
    if (type === 'success')           color = 'rgb(119, 235, 119)'
    else if (type === 'error')    color = 'rgb(243, 57, 57)'

    if (callback)
        if (callback_timeout)
            $('.message-box.page-2').hide().css('color', color).fadeIn(time, function() {setTimeout(callback, callback_timeout)});
        else    $('.message-box.page-2').hide().css('color', color).fadeIn(time, callback);
    else    $('.message-box.page-2').hide().css('color', color).fadeIn(time);
}

function hideMessageBoxPage2(time=200, callback=null, callback_timeout=null)
{   
    var color = '#fff'        
    $('.message-box.page-2').fadeOut(time, function() {
        messageBoxPage1.innerHTML = 'No Message'
        $('.message-box.page-2').css('color', color)
        if (callback) 
            if (callback_timeout) setTimeout(callback(), callback_timeout)
            else callback()
    })
}

function redirectToHomepage() {
    window.location.replace("/");
}

var url_login = "/login/"

function redirectToLogin() {
    window.location.replace(url_login);
}


