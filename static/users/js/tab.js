var profTabs = document.querySelectorAll('.prof-tab')
var profTabSvgs = document.querySelectorAll('.prof-tsvg')


for (let index = 0; index < profTabs.length; ++index) {
    if (index!=curr_tab)
    {
        profTabs[index].addEventListener('mouseenter', function(e) {
            showProfTabSvg(profTabs[index].getAttribute('id'));
        });
        profTabs[index].addEventListener('mouseleave', function(e) {
            showProfTabSvg(curr_tab);
        });
    }
}

function showProfTabSvg(i=0)
{
    Array.from(profTabSvgs, function(element) {
        element.classList.remove('sel')
    });
    
    profTabSvgs[i].classList.add('sel')
}