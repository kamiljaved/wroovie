

// login & signup modals

// Get the modal
var modal = document.getElementById('mdl-1');

// modal wraps
var modalWrapLogin = modal.querySelector('.modal-wrap-login')
var modalWrapSignup = modal.querySelector('.modal-wrap-signup')

// When the user clicks anywhere outside of the modalLogin, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
        modalWrapLogin.style.display = 'none'
        modalWrapSignup.style.display = 'none'
        document.querySelectorAll(".base-layer > *").forEach((el) => {el.style.filter = "none";})
    }
}

var loginButton = document.querySelector('.login-button');
var signupButton = document.querySelector('.signup-button');

var loginModalCloseButton = document.querySelector('.close-modal-login')
var signupModalCloseButton = document.querySelector('.close-modal-signup')

loginButton.addEventListener('click', function(e) {
    e.preventDefault()    
    modalWrapLogin.style.display = 'flex'
    modal.style.display = 'block'
    document.querySelectorAll(".base-layer > *:not(nav)").forEach((el) => {el.style.transition="filter 250ms ease-in-out"; el.style.filter = "hue-rotate(90deg) opacity(0.7)"; })
})

signupButton.addEventListener('click', function(e) {
    e.preventDefault()
    modalWrapSignup.style.display = 'flex'
    modal.style.display = 'block'
    document.querySelectorAll(".base-layer > *:not(nav)").forEach((el) => {el.style.transition="filter 250ms ease-in-out"; el.style.filter = "hue-rotate(90deg) opacity(0.7)"; })
})

loginModalCloseButton.addEventListener('click', function() {
    modal.style.display='none'
})

loginModalCancelButton.addEventListener('click', function() {
    modal.style.display='none'
})