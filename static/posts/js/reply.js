// subsequent stuff only runs if user is authenticated

// main reply box

var url_reply_create = `/p/${post_slug}/reply/`;
var url_login = '/u/login';
var url_login_redirect = url_login+'/?next='+request_path;

var replyEditor_main = document.querySelector('.reply-editor.main')
var replyEditor_main_sumbitBtn = replyEditor_main.querySelector('.reply-btn-submit')

var replyEditor_main_parent = replyEditor_main.getAttribute('parent')

var replyEditor_main_input = replyEditor_main.querySelector('input')
var replyEditor_main_element = replyEditor_main.querySelector("trix-editor")

var newReplyPos_main = document.querySelector('#new-main-replies')

function insertAfter(referenceNode, newNode) {
    referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
    fixLinks();
}

function insertAfter_HTML(referenceNode, new_html) {
    var el = document.createElement("span");
    el.innerHTML = new_html;
    insertAfter(referenceNode, el)
}

function insertBefore_HTML(referenceNode, new_html) {
    var el = document.createElement("span");
    el.innerHTML = new_html;
    referenceNode.parentNode.insertBefore(el, referenceNode);
    fixLinks();
}

replyEditor_main_element.addEventListener("trix-change", fixMainSubmitButton)

function stripHTML(html)
{
   var tmp = document.createElement("DIV");
   tmp.innerHTML = html;
   return tmp.textContent || tmp.innerText || "";
}

function fixMainSubmitButton()
{
    var trix_text = stripHTML(replyEditor_main_element.editor.getDocument().toString()).replace(/\s/g,'')

    if (trix_text !== "" && trix_text !== null)
    {
        if (replyEditor_main_sumbitBtn.classList.contains('disabled')) replyEditor_main_sumbitBtn.classList.remove('disabled')
    }
    else
    {
        if (!replyEditor_main_sumbitBtn.classList.contains('disabled')) replyEditor_main_sumbitBtn.classList.add('disabled')
    }
}

replyEditor_main_sumbitBtn.addEventListener('click', listener_click_btnReplySubmit);

function listener_click_btnReplySubmit(e)
{
    if (replyEditor_main_sumbitBtn.classList.contains('disabled')) return;

    var html_text = replyEditor_main_input.getAttribute('value')
    if (html_text === "" || html_text == null) 
    {
        if (!replyEditor_main_sumbitBtn.classList.contains('disabled')) replyEditor_main_sumbitBtn.classList.add('disabled')
        return;
    }

    var trix_text = stripHTML(replyEditor_main_element.editor.getDocument().toString()).replace(/\s/g,'')
    if (trix_text === "" || trix_text == null) 
    {
        if (!replyEditor_main_sumbitBtn.classList.contains('disabled')) replyEditor_main_sumbitBtn.classList.add('disabled')
        return;
    }

    replyEditor_main.style.pointerEvents = "none"
    if (!replyEditor_main_sumbitBtn.classList.contains('disabled')) replyEditor_main_sumbitBtn.classList.add('disabled')

    $.ajax({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }, 
        url: url_reply_create, 
        method: "POST",
        data: {
            'parent':replyEditor_main_parent,
            'content':html_text
        },
        success: function(data){
            handler_createReply(data);
            replyEditor_main.style.pointerEvents = "all"
        },
        error: function(error){
            console.log(error)
            addNotification(error, "error");

            // show error popup

            // enable editor and submit button
            replyEditor_main.style.pointerEvents = "all"
            fixMainSubmitButton();
        }

    });
}


function handler_createReply(data) 
{   
    if (data['redirect_to_login'])
    {
        window.location.href = url_login_redirect
    }
    else
    {
        if (data['added'])
        {
            // empty the reply box, keep submit disabled
            replyEditor_main_element.value = ""
            if (!replyEditor_main_sumbitBtn.classList.contains('disabled')) replyEditor_main_sumbitBtn.classList.add('disabled')

            // if new reply html received in data
            // append new main reply to top of reply list (for now)
            if ("reply_html" in data)
            {
                // listeners already binded in received html
                insertAfter_HTML(newReplyPos_main, data["reply_html"])

                // fix other figures if received (e.g. reply count)
            }
        }
        else
        {
            console.log(data['message'])
            // show message popup (or do action)

            // enable editor and submit button
            replyEditor_main.style.pointerEvents = "all"
            fixMainSubmitButton();
        }
    }
}



// subreplies

function appendReplyCreateBox(id)
{
    var rplyBtn = document.querySelector(`#rply-rply-btn-${id}`)
    if (rplyBtn.classList.contains('sel')) return
    if (!rplyBtn.classList.contains('sel')) rplyBtn.classList.add('sel')

    var ins = document.querySelector(`#repbx-ins-${id}`)
    
    ins.innerHTML = `<div class="post-options">
                        <form class="reply-editor" parent="${id}" id="rply-editor-${id}">
                            <span class="editor-block">
                                <input id="sbrply-${id}" type="hidden" name="content" value="">
                                <trix-editor input="sbrply-${id}"></trix-editor>
                            </span>
                            <div class="community-button p-comm-btn-submit subreply-btn-submit disabled" id="rply-submit-btn-${id}">
                                <div class="community-button-text">REPLY</div>
                            </div>
                            <div class="community-button p-comm-btn-submit subreply-btn-cancel" id="rply-cancel-btn-${id}">
                                <div class="community-button-text">CANCEL</div>
                            </div>
                        </form>
                    </div>`

    // add event listeners 

    var replyEditor_subreply = document.querySelector(`#rply-editor-${id}`)
    var replyEditor_subreply_sumbitBtn = replyEditor_subreply.querySelector(`#rply-submit-btn-${id}`)
    var replyEditor_subreply_cancelBtn = replyEditor_subreply.querySelector(`#rply-cancel-btn-${id}`)

    var replyEditor_subreply_parent = replyEditor_subreply.getAttribute('parent')

    var replyEditor_subreply_input = replyEditor_subreply.querySelector('input')
    var replyEditor_subreply_element = replyEditor_subreply.querySelector("trix-editor")

    var newReplyPos_subreply = document.querySelector(`#new-sub-replies-${id}`)


    replyEditor_subreply_cancelBtn.addEventListener('click', function() {
        ins.innerHTML = ''
        if (rplyBtn.classList.contains('sel')) rplyBtn.classList.remove('sel')
    })

    replyEditor_subreply_element.addEventListener("trix-change", function(e){
        fixReplySubmitButton(replyEditor_subreply_element, replyEditor_subreply_input, replyEditor_subreply_sumbitBtn);
    })

    replyEditor_subreply_sumbitBtn.addEventListener('click', function()
    {
        listener_click_btnSubReplySubmit(id, ins, rplyBtn, replyEditor_subreply_element, replyEditor_subreply_sumbitBtn, replyEditor_subreply_input, replyEditor_subreply, replyEditor_subreply_element, replyEditor_subreply_parent, newReplyPos_subreply);
    });

    replyEditor_subreply_element.focus();
}

function fixReplySubmitButton(replyEditor_subreply_element, replyEditor_subreply_input, replyEditor_subreply_sumbitBtn)
{
    var trix_text = stripHTML(replyEditor_subreply_element.editor.getDocument().toString()).replace(/\s/g,'')

    if (trix_text !== "" && trix_text !== null)
    {
        if (replyEditor_subreply_sumbitBtn.classList.contains('disabled')) replyEditor_subreply_sumbitBtn.classList.remove('disabled')
    }
    else
    {
        if (!replyEditor_subreply_sumbitBtn.classList.contains('disabled')) replyEditor_subreply_sumbitBtn.classList.add('disabled')
    }
}


function listener_click_btnSubReplySubmit(id, ins, rplyBtn, replyEditor_subreply_element, replyEditor_subreply_sumbitBtn, replyEditor_subreply_input, replyEditor_subreply, replyEditor_subreply_element, replyEditor_subreply_parent, newReplyPos_subreply)
{
    if (replyEditor_subreply_sumbitBtn.classList.contains('disabled')) return;

    var html_text = replyEditor_subreply_input.getAttribute('value')
    if (html_text === "" || html_text == null) 
    {
        if (!replyEditor_subreply_sumbitBtn.classList.contains('disabled')) replyEditor_subreply_sumbitBtn.classList.add('disabled')
        return;
    }

    var trix_text = stripHTML(replyEditor_subreply_element.editor.getDocument().toString()).replace(/\s/g,'')
    if (trix_text === "" || trix_text == null) 
    {
        if (!replyEditor_subreply_sumbitBtn.classList.contains('disabled')) replyEditor_subreply_sumbitBtn.classList.add('disabled')
        return;
    }

    replyEditor_subreply.style.pointerEvents = "none"
    if (!replyEditor_subreply_sumbitBtn.classList.contains('disabled')) replyEditor_subreply_sumbitBtn.classList.add('disabled')

    $.ajax({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }, 
        url: url_reply_create, 
        method: "POST",
        data: {
            'parent':replyEditor_subreply_parent,
            'content':html_text
        },
        success: function(data){
            handler_createSubReply(id, data, ins, rplyBtn, replyEditor_subreply_element, replyEditor_subreply, replyEditor_subreply_sumbitBtn, replyEditor_subreply_element, replyEditor_subreply_input, newReplyPos_subreply);
            replyEditor_subreply.style.pointerEvents = "all"
        },
        error: function(error){
            console.log(error)
            addNotification(error, "error");

            // show error popup

            // enable editor and submit button
            replyEditor_subreply.style.pointerEvents = "all"
            fixReplySubmitButton(replyEditor_subreply_element, replyEditor_subreply_input, replyEditor_subreply_sumbitBtn);
        }

    });
}

function handler_createSubReply(id, data, ins, rplyBtn, replyEditor_subreply_element, replyEditor_subreply, replyEditor_subreply_sumbitBtn, replyEditor_subreply_element, replyEditor_subreply_input, newReplyPos_subreply) 
{   
    if (data['redirect_to_login'])
    {
        window.location.href = url_login_redirect
    }
    else
    {
        if (data['added'])
        {
            // empty the reply box, keep submit disabled
            replyEditor_subreply_element.value = ""
            if (!replyEditor_subreply_sumbitBtn.classList.contains('disabled')) replyEditor_subreply_sumbitBtn.classList.add('disabled')

            // hide the reply box
            ins.innerHTML = ''
            if (rplyBtn.classList.contains('sel')) rplyBtn.classList.remove('sel')

            // if new reply html received in data
            // append new reply directly under parent (for now)
            if ("reply_html" in data)
            {
                // listeners already binded in received html
                insertAfter_HTML(newReplyPos_subreply, data["reply_html"])

                // fix other figures if received (e.g. reply count)
            }
            else if (data['show_more_replies'])
            {
                // if not already present, append
                var showMoreReplies_opt = document.querySelector(`#show-reply-more-${id}`)
                if (showMoreReplies_opt == null)
                {
                    var html_text = `<div class="post-options" id="show-reply-more-${id}">
                                        <div class="info-text reply-more">..............................................................</div>
                                        <div class="post-options-button" onclick="event.stopPropagation();">
                                            <svg aria-hidden="true" focusable="false" data-prefix="fad" data-icon="external-link" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" class="svg-inline--fa fa-external-link fa-w-16 fa-9x"><g class="fa-group"><path fill="currentColor" d="M400 320h32a16 16 0 0 1 16 16v128a48 48 0 0 1-48 48H48a48 48 0 0 1-48-48V112a48 48 0 0 1 48-48h160a16 16 0 0 1 16 16v32a16 16 0 0 1-16 16H64v320h320V336a16 16 0 0 1 16-16z" class="fa-secondary"></path><path fill="currentColor" d="M484 224h-17.88a28 28 0 0 1-28-28v-.78L440 128 192.91 376.91A24 24 0 0 1 159 377l-.06-.06L135 353.09a24 24 0 0 1 0-33.94l.06-.06L384 72l-67.21 1.9A28 28 0 0 1 288 46.68V28a28 28 0 0 1 28-28h158.67A37.33 37.33 0 0 1 512 37.33V196a28 28 0 0 1-28 28z" class="fa-primary"></path></g></svg>                                    
                                            <div class="post-options-button-text">
                                                Show full reply-thread
                                            </div>
                                        </div>
                                    </div>`
                    insertBefore_HTML(ins, html_text)
                }
            }
        }
        else
        {
            console.log(data['message'])
            // show message popup (or do action)

            // enable editor and submit button
            replyEditor_subreply.style.pointerEvents = "all"
            fixReplySubmitButton(replyEditor_subreply_element, replyEditor_subreply_input, replyEditor_subreply_sumbitBtn);

        }
    }
}