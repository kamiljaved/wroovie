var wrapper = document.querySelector(".wrapper");

var sidebar = document.querySelector(".comm-sidebar");

var banner = document.querySelector('.community-banner');

var footer = document.querySelector('.site-footer');

var navbar = document.querySelector('.navbar');

var footer_fixed = false;
var footer_top_old = footer.offsetTop;
var footer_margin_top = 12; // px

wrapper.addEventListener("scroll", function(e) { 

    if (wrapper.scrollTop + navbar.offsetHeight + footer_margin_top > footer.offsetTop && !footer_fixed)
    {
        footer_top_old = footer.offsetTop;
        footer.classList.add("site-footer-fixed")
        footer_fixed = true;

    }

    if (wrapper.scrollTop + navbar.offsetHeight + footer_margin_top <= footer_top_old && footer_fixed)
    {
        footer.classList.remove("site-footer-fixed")
        footer_fixed = false;
    }
    
});

