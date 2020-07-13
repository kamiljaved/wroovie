var feedTabs = document.querySelectorAll('.feed-tab')
var feedTabSvgs = document.querySelectorAll('.feed-tsvg')


for (let index = 0; index < feedTabs.length; ++index) {
    if (index!=curr_feed)
    {
        feedTabs[index].addEventListener('mouseenter', function(e) {
            showfeedTabSvg(feedTabs[index].getAttribute('id'));
        });
        feedTabs[index].addEventListener('mouseleave', function(e) {
            showfeedTabSvg(curr_feed);
        });
    }
}

function showfeedTabSvg(i=0)
{
    Array.from(feedTabSvgs, function(element) {
        element.classList.remove('sel')
    });
    
    feedTabSvgs[i].classList.add('sel')
}