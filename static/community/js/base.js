var wrapper = document.querySelector(".wrapper");

var sidebar = document.querySelector(".comm-sidebar");

var banner = document.querySelector('.community-header');

var footer = document.querySelector('.site-footer');

var navbar = document.querySelector('.navbar');

var menu = document.querySelector('.comm-menu');

var comm1 = document.querySelector('.comm-1');

var footer_fixed = false;
var footer_top_old = footer.offsetTop;
var footer_margin_top = 12; // px

menu.style.minWidth = `${comm1.offsetWidth}px`;

wrapper.addEventListener("scroll", function(e) { 

    if (wrapper.scrollTop + footer_margin_top > footer.offsetTop && !footer_fixed)
    {
        footer_top_old = footer.offsetTop;
        footer.classList.add("site-footer-fixed")
        footer_fixed = true;

    }

    if (wrapper.scrollTop + footer_margin_top <= footer_top_old && footer_fixed)
    {
        footer.classList.remove("site-footer-fixed")
        footer_fixed = false;
    }
    
});

window.onresize = function(){
    menu.style.minWidth = `${comm1.offsetWidth}px`;
}

var btnJoin = document.querySelector('.comm-btn-join');
var btnJoinText = document.querySelector('.community-button-text')

var joinTick = document.querySelector('.join-tick')

if (user_is_authenticated)
{
    btnJoin.addEventListener("mouseenter", listener_mouseenter_btnJoin);
    btnJoin.addEventListener("mouseleave", listener_mouseleave_btnJoin);
}

function listener_mouseenter_btnJoin(e)
{
    if (user_is_member) 
    {
        btnJoinText.innerHTML = 'LEAVE';
    }
} 

function listener_mouseleave_btnJoin(e)
{
    if (user_is_member) 
    {
        btnJoinText.innerHTML = 'JOINED';
    }
} 


