
var postEditor = document.querySelector('.post-create-editor-wrap')
var postEditor_sumbitBtn = postEditor.querySelector('.post-btn-submit')



postForm_input_title.addEventListener("input", fixMainSubmitButton)
postForm_input_community.addEventListener("change", fixMainSubmitButton)



function fixMainSubmitButton()
{
    var title_text = postForm_input_title.value.replace(/\s/g,'')
    var community = postForm_input_community.value

    if (title_text !== "" && title_text !== null && community !== null && community !== "")
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
}
