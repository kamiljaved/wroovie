// subsequent stuff only runs if user is authenticated

// main reply box

var url_login = '/u/login';
var url_login_redirect = url_login+'/?next='+request_path;

var postForm = document.querySelector('.post-create-form')
var postForm_input_community = postForm.querySelector("select[name='community']")
var postForm_input_title = postForm.querySelector("input[name='title']")




const pc_urlParams = new URLSearchParams(window.location.search);

var pc_url_article = '/create/article/'
var pc_url_thread = '/create/thread/'

// redirection functions
function redirectToCreate(url)
{
    // get community name from url args
    var community = postForm_input_community.value
    var title = postForm_input_title.value
    var url_create = url

    if (community != null && community !== "" )
    {
        url_create += `?comm=${community}`
        if (title != null && title !== "" )
            url_create += `&title=${title}`
    }
    else if (title != null && title !== "" )
        url_create += `?title=${title}`

    window.location.href = url_create
}

function redirectToCreateArticle()
{
    redirectToCreate(pc_url_article)
}

function redirectToCreateThread()
{
    redirectToCreate(pc_url_thread)
}

if (pc_urlParams.has('comm')) postForm_input_community.value = pc_urlParams.get('comm')
if (pc_urlParams.has('title')) postForm_input_title.value = pc_urlParams.get('title').substring(0, postForm_input_title.maxLength)























































































































