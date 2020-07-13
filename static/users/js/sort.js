

var sorts = [
    document.querySelector('.sort-top'),
    document.querySelector('.sort-all')
]

var fssvgs = [
    document.querySelector(".fssvg-top"),
    document.querySelector(".fssvg-all"),
]


for (let index = 0; index < sorts.length; ++index) {
    if (index!=curr_sort)
    {
        sorts[index].addEventListener('mouseenter', function(e) {
            showFeedSvg(index);
        });
        sorts[index].addEventListener('mouseleave', function(e) {
            showFeedSvg(curr_sort);
        });
    }
}

function showFeedSvg(i=0)
{
    Array.from(fssvgs, function(element) {
        element.classList.remove('sel')
    });
    
    fssvgs[i].classList.add('sel')
}