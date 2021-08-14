var wrapper = document.querySelector(".wrapper");
var footer = document.querySelector('.site-footer');
var navbar = document.querySelector(".navbar")

var footer_fixed = false;
var footer_top_old = footer.offsetTop;
var footer_margin_top = 12; // px



sidebarToggleBtn = document.querySelector(".sidebar-toggle-button")
wrapComm1 = document.querySelector(".wrapper .comm-1")
wrapMainContent = document.querySelector(".comm-1-1.wrap-main-content")
wrapSidebar = document.querySelector(".comm-1-2.wrap-sidebar")

scrlTp_mainContent = 0;


sidebarToggleBtn.addEventListener("click", function(){

    // console.log(sidebarToggleBtn.getAttribute('drag'))

    if (sidebarToggleBtn.getAttribute('drag') == "true")
    {
        // sidebarToggleBtn.setAttribute('drag', false)
        return
    }

    if (sidebarToggleBtn.classList.contains("activated"))
    {
        // deactivate sidebar
        sidebarToggleBtn.classList.remove("activated")

        // ADJUST WRAPPER SIZE
        wrapComm1.style = ""
        
        // wrapSidebar.style.width = "18rem";
        // wrapSidebar.style.marginLeft = "8px";
        // wrapSidebar.style.alignItems = "none"

        wrapSidebar.style = ""

        wrapSidebar.style.display = "none";
        wrapMainContent.style.display = "flex";

        $('.comm-1-1.wrap-main-content').hide().fadeIn(500)

        wrapper.scrollTop = scrlTp_mainContent;
        scrlTp_mainContent = 0;
    }
    else
    {
        // activate sidebar
        sidebarToggleBtn.classList.add("activated")

        // ADJUST WRAPPER SIZE
        wrapComm1.style.minWidth = "18rem"
        wrapComm1.style.width = "18rem"

        wrapSidebar.style.width = `${wrapMainContent.offsetWidth}px`;
        // wrapSidebar.style.marginLeft = "0";
        // wrapSidebar.style.alignItems = "center"

        scrlTp_mainContent = wrapper.scrollTop
        wrapper.scrollTop = 0;



        wrapMainContent.style.display = "none";
        wrapSidebar.style.display = "flex";

        $('.comm-1-2.wrap-sidebar').hide().fadeIn(500)
    }
})





window.addEventListener("resize", function(){

    if (window.innerWidth > 1048)  // 65.5 rem
    {

        wrapSidebar.style = "";
        wrapMainContent.style = "";
        sidebarToggleBtn.style = "";
        
        if (sidebarToggleBtn.classList.contains("activated"))
        {
            // deactivate sidebar
            sidebarToggleBtn.classList.remove("activated")
    
            wrapSidebar.style.width = "18rem";
            wrapSidebar.style.marginLeft = "8px";
            wrapSidebar.style.alignItems = "none"
    
            wrapper.scrollTop = scrlTp_mainContent;
            scrlTp_mainContent = 0;
        }

        doFooterSticky()
    }
    else
    {
        // unstick footer
        if (footer_fixed) 
        {
            footer.classList.remove("site-footer-fixed")
            footer_fixed = false;
        }

        // reposition sidebar button
        fixSidebarToggleBtnPos();
    }
})





// footer fixing

wrapper.addEventListener("scroll", function(e) { 
    if (window.innerWidth > 1048)
    {
        doFooterSticky()
    }
});

function doFooterSticky()
{
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
}

// sidebar button fixing

function fixSidebarToggleBtnPos()
{

    if (sidebarToggleBtn.offsetTop < wrapper.offsetTop)
    {
        sidebarToggleBtn.style.top = wrapper.offsetTop + "px";
    }
    else if (sidebarToggleBtn.offsetTop+sidebarToggleBtn.offsetHeight > wrapper.offsetTop+wrapper.clientHeight)
    {
        sidebarToggleBtn.style.top = (wrapper.offsetTop + wrapper.clientHeight - sidebarToggleBtn.offsetHeight) + "px";
    }

    if (sidebarToggleBtn.offsetLeft < wrapper.offsetLeft)
    {
        sidebarToggleBtn.style.left = wrapper.offsetLeft + "px";
    }
    else if (sidebarToggleBtn.offsetLeft+sidebarToggleBtn.offsetWidth > wrapper.offsetLeft+wrapper.clientWidth)
    {
        sidebarToggleBtn.style.left = (wrapper.offsetLeft + wrapper.clientWidth - sidebarToggleBtn.offsetWidth) + "px";
    }
}










dragElement(sidebarToggleBtn);


// should be added after all other listeners of an element, if click is to be prevented on drag
function dragElement(elmnt) {
  var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
  if (document.getElementById(elmnt.id + "header")) {
    // if present, the header is where you move the DIV from:
    document.getElementById(elmnt.id + "header").onmousedown = dragMouseDown;
  } else {
    // otherwise, move the DIV from anywhere inside the DIV:
    elmnt.onmousedown = function(e) {
        navbar.style.pointerEvents = "none"
        wrapMainContent.style.pointerEvents = "none"
        elmnt.setAttribute('drag', false)
        dragMouseDown(e);
    }
  }

  elmnt.onclick = function() {
    elmnt.setAttribute('drag', false)
  }

  function dragMouseDown(e) {
    e = e || window.event;
    e.preventDefault();
    // get the mouse cursor position at startup:
    pos3 = e.clientX;
    pos4 = e.clientY;
    document.onmouseup = closeDragElement;
    // call a function whenever the cursor moves:
    document.onmousemove = elementDrag;
  }

  function elementDrag(e) {
    elmnt.setAttribute('drag', true)

    e = e || window.event;
    e.preventDefault();
    // calculate the new cursor position:
    pos1 = pos3 - e.clientX;
    pos2 = pos4 - e.clientY;
    pos3 = e.clientX;
    pos4 = e.clientY;
    // set the element's new position:
    elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
    elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
    fixSidebarToggleBtnPos();
  }

  function closeDragElement() {
    // elmnt.setAttribute('drag', false)    // expected to be handled by click event

    // stop moving when mouse button is released:
    document.onmouseup = null;
    document.onmousemove = null;

    navbar.style = ""
    wrapMainContent.style.pointerEvents = "all"
  }
}