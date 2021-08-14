
var postEditor = document.querySelector('.post-create-editor-wrap')
var postEditor_sumbitBtn = postEditor.querySelector('.post-btn-submit')

var postEditor_input = postEditor.querySelector('input')
var postEditor_element = postEditor.querySelector("trix-editor")
postEditor_element.setAttribute('placeholder', 'Content')

var error_postContent = postForm.querySelector(".post-content-error")

var newReplyPos = document.querySelector('#new-main-replies')

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

postEditor_element.addEventListener("trix-change", fixMainSubmitButton)

postForm_input_title.addEventListener("input", fixMainSubmitButton)
postForm_input_community.addEventListener("change", fixMainSubmitButton)

function stripHTML(html)
{
   var tmp = document.createElement("DIV");
   tmp.innerHTML = html;
   return tmp.textContent || tmp.innerText || "";
}

function fixMainSubmitButton()
{
    var trix_text = stripHTML(postEditor_element.editor.getDocument().toString()).replace(/\s/g,'')
    var title_text = postForm_input_title.value.replace(/\s/g,'')
    var community = postForm_input_community.value

    if (trix_text !== "" && trix_text !== null && title_text !== "" && title_text !== null && community !== null && community !== "")
    {
        if (postEditor_sumbitBtn.classList.contains('disabled')) postEditor_sumbitBtn.classList.remove('disabled')
    }
    else
    {
        if (!postEditor_sumbitBtn.classList.contains('disabled')) postEditor_sumbitBtn.classList.add('disabled')
    }
}

fixMainSubmitButton()

postEditor_sumbitBtn.addEventListener('click', listener_click_btnReplySubmit);

function listener_click_btnReplySubmit(e)
{
    fixMainSubmitButton()


    var trix_text = stripHTML(postEditor_element.editor.getDocument().toString()).replace(/\s/g,'')
    var title_text = postForm_input_title.value.replace(/\s/g,'')
    var community = postForm_input_community.value

    // only block submit/action if community, title are valid but content is invalid
    if (title_text !== "" && title_text !== null && community !== null && community !== "")
    {
        if (trix_text === "" || trix_text == null)
        {
            e.preventDefault()
            e.stopPropagation()

            // show error
            if (error_postContent.classList.contains('hidden')) error_postContent.classList.remove('hidden')
        }
        else
        {
            // hide error
            if (!error_postContent.classList.contains('hidden')) error_postContent.classList.add('hidden')
        }
    }
    else
    {
        if (trix_text !== "" && trix_text != null)
        {
            // hide error
            if (!error_postContent.classList.contains('hidden')) error_postContent.classList.add('hidden')
        }
    }
}
