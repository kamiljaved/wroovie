var searchItem = document.querySelector(".search")
var searchbar = document.querySelector(".searchbar")
var searchLink = document.querySelector(".search-link")
var searchSVG = searchItem.querySelector(".search-svg")
var searchClear = searchItem.querySelector(".search-clear")
var mouse_in_search_item = false

var url_search = '/search/'

searchClear.addEventListener("click", function() {
    searchClear.style.display = "none";
    searchbar.value = ""
    searchbar.focus()
})

searchbar.addEventListener("input", function() { 
    if (searchbar.value) {
        searchClear.style.display = "flex";
        searchClear.style.cursor = "pointer"
    }
    else
    {
        searchClear.style.display = "none";
        searchClear.style.cursor = "text"
    }
});

searchbar.addEventListener("focus", function() {
    searchLink.style.filter = "grayscale(0%) opacity(1)"
    searchLink.style.background = "var(--bg-secondary)"
    searchLink.style.color = "var(--text-secondary)"

    searchSVG.style.right = "0"
    searchSVG.style.transform = "translateX(0)"
    searchSVG.style.margin = "0rem 2rem"

    searchSVG.style.cursor = "pointer"
});

searchbar.addEventListener("focusout", function() {
    if (!searchbar.value && !mouse_in_search_item)
    {
        searchLink.style.filter = "grayscale(100%) opacity(0.7)"
        searchLink.style.background = "none"
        searchLink.style.color = "var(--text-primary)"

        searchSVG.style.right = "calc(100% - 8rem)"
        searchSVG.style.transform = "translateX(50%)"
        searchSVG.style.margin = "0rem 0rem"

        searchSVG.style.cursor = "text"
    }
});

searchItem.addEventListener("mouseenter", function() {
    mouse_in_search_item = true
    searchLink.style.filter = "grayscale(0%) opacity(1)"
    searchLink.style.background = "var(--bg-secondary)"
    searchLink.style.color = "var(--text-secondary)"

    searchSVG.style.right = "0"
    searchSVG.style.transform = "translateX(0)"
    searchSVG.style.margin = "0rem 2rem"

    searchSVG.style.cursor = "pointer"
})

searchItem.addEventListener("mouseleave", function() {
    mouse_in_search_item = false
    if (document.activeElement !== searchbar && !searchbar.value)
    {
        searchLink.style.filter = "grayscale(100%) opacity(0.7)"
        searchLink.style.background = "none"
        searchLink.style.color = "var(--text-primary)"

        searchSVG.style.right = "calc(100% - 8rem)"
        searchSVG.style.transform = "translateX(50%)"
        searchSVG.style.margin = "0rem 0rem"

        searchSVG.style.cursor = "text"
    }
})

searchLink.addEventListener('click', function() {
    searchbar.focus()
})

searchSVG.addEventListener("click", function() {
    if (searchbar.value === "" || searchbar.value == null) return
    window.location.href = url_search + searchbar.value;
})

searchbar.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        if (searchbar.value === "" || searchbar.value == null) return
        window.location.href = url_search + searchbar.value;
    }
});

var ddUserOptions = document.querySelector(".user-options")
var userBox = document.querySelector(".user-box")

var ddBrowseOptions = document.querySelector(".browse-options")
var browseBox = document.querySelector(".browse-box")

var settingsBox = document.querySelector(".settings-box")
var ddSettingsOptions = settingsBox.querySelector(".settings-options")

var settingsBox_droplinks = settingsBox.querySelectorAll(".dropdown .drop-link")
var settingsBox_droplinks_ind = settingsBox.querySelectorAll(".dropdown .nav-indicator .drop-link")

settingsBox.addEventListener("mouseenter", function() {
    ddSettingsOptions.style.zIndex = "-1";
})

settingsBox.addEventListener("mouseleave", function() {
    ddSettingsOptions.style.zIndex = "0";
})

/* 
.settings-box:hover .dropdown .drop-link{
    height: calc(var(--nav-height) - 1rem) !important;
}
      
.settings-box:hover .dropdown .nav-indicator .drop-link{
    height: calc(var(--nav-height) - 1rem - 1px) !important;
}
      
.settings-box:hover #dd-settings-options{
    height: calc(6 * calc(var(--nav-height) - 1rem));
}
*/

// settingsBox.addEventListener("click", function() {
//     console.log("HI")
//     ddSettingsOptions.style.height = "calc(6 * calc(var(--nav-height) - 1rem))";
//     settingsBox_droplinks.forEach(function(el) {console.log(el); el.style.height = "calc(var(--nav-height) - 1rem) !important"})
//     settingsBox_droplinks_ind.forEach(function(el) {el.style.height = "calc(var(--nav-height) - 1rem - 1px) !important;"})
// })

      
// tasks on complete page & resources load
document.addEventListener('readystatechange', event => {

    if (event.target.readyState === "complete") 
    {        
        if (user_is_authenticated)
        {
            navbarFixes();
            setTimeout(navbarFixes, 1000)
        }
    }

});

document.onload = function() {
    if (user_is_authenticated) navbarFixes();
}

window.onresize = function() {
    if (user_is_authenticated) navbarFixes();
}   

function navbarFixes() {
    if (userBox.clientWidth > ddUserOptions.clientWidth)        // ddUserOptions.clientWidth should initially be min-width
    {
        ddUserOptions.style.minWidth = `${userBox.clientWidth}px`
    }
    ddUserOptions.style.right = `${window.innerWidth - userBox.getBoundingClientRect().right}px`
}

if (user_is_authenticated)
browseBox.addEventListener("mouseenter", function() {
    ddBrowseOptions.scrollTop = 0;
})


function fixLinks()
{
    var allLinks = document.querySelectorAll("div.post-text a");
    for(var i=0;i<allLinks.length;i++)
    {
        var currentLink = allLinks[i];
        currentLink.setAttribute("target","_blank");
        currentLink.addEventListener("click", function(e) {
            e.stopPropagation()
        })
    }
} 

window.onload = function()
{
    fixLinks()
}


if (searchbar.value) {
    searchClear.style.display = "flex";
    searchClear.style.cursor = "pointer"
}
else
{
    searchClear.style.display = "none";
    searchClear.style.cursor = "text"
}
