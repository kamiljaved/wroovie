var searchItem = document.querySelector(".search")
var searchbar = document.querySelector(".searchbar")
var searchLink = document.querySelector(".search-link")
var searchSVG = searchItem.querySelector("svg")
var mouse_in_search_item = false

searchbar.addEventListener("focus", function() {
    searchLink.style.filter = "grayscale(0%) opacity(1)"
    searchLink.style.background = "var(--bg-secondary)"
    searchLink.style.color = "var(--text-secondary)"

    searchSVG.style.right = "0"
    searchSVG.style.transform = "translateX(0)"
    searchSVG.style.margin = "0rem 2rem"
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
    }
})
