// var wrapper = document.querySelector(".wrapper");

// var sidebar = document.querySelector(".comm-sidebar");

// var banner = document.querySelector('.community-header');

// var footer = document.querySelector('.site-footer');

// var navbar = document.querySelector('.navbar');

// var menu = document.querySelector('.comm-menu');

// var comm1 = document.querySelector('.comm-1');


// // feed selection hover actions
// // var feeds = [
// //     document.querySelector('.feed-home'),
// //     document.querySelector('.feed-sugg'),
// //     document.querySelector('.feed-pplr'),
// //     document.querySelector('.feed-top'),
// //     document.querySelector('.feed-all')
// // ]

// // var fsvgs = [
// //     document.querySelector(".fsvg-home"),
// //     document.querySelector(".fsvg-sugg"),
// //     document.querySelector(".fsvg-pplr"),
// //     document.querySelector(".fsvg-top"),
// //     document.querySelector(".fsvg-all"),
// // ]


// // for (let index = 0; index < feeds.length; ++index) {
// //     if (index!=curr_feed)
// //     {
// //         feeds[index].addEventListener('mouseenter', function(e) {
// //             showFeedSvg(index);
// //         });
// //         feeds[index].addEventListener('mouseleave', function(e) {
// //             showFeedSvg(curr_feed);
// //         });
// //     }
// // }

// // function showFeedSvg(i=0)
// // {
// //     Array.from(fsvgs, function(element) {
// //         element.classList.remove('sel')
// //     });
    
// //     fsvgs[i].classList.add('sel')
// // }


// var footer_fixed = false;
// var footer_top_old = footer.offsetTop;
// var footer_margin_top = 12; // px


// //menu.style.minWidth = `${comm1.offsetWidth}px`;

// wrapper.addEventListener("scroll", function(e) { 

//     if (wrapper.scrollTop + footer_margin_top > footer.offsetTop && !footer_fixed)
//     {
//         footer_top_old = footer.offsetTop;
//         footer.classList.add("site-footer-fixed")
//         footer_fixed = true;

//     }

//     if (wrapper.scrollTop + footer_margin_top <= footer_top_old && footer_fixed)
//     {
//         footer.classList.remove("site-footer-fixed")
//         footer_fixed = false;
//     }
    
// });

// window.onresize = function(){
//     menu.style.minWidth = `${comm1.offsetWidth}px`;
// }






