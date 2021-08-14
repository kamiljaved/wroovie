
const searchMemberInput = document.getElementById("id_member_search_input");
const searchMemberButton = document.getElementById("id_member_search_button");
const removeModeratorsElement = document.getElementById("id_remove_moderators");
const searchResultsElement = document.getElementById("id_search_results");
const search_url = searchMemberButton.getAttribute("url") 
const modify_url = document.getElementById("modify_url").getAttribute("url"); 

var url_user_profile = '/u/'

function addModeratorMinHTML(username, modify_url) {
    return `<div id="search_${username}" class="search-results">
                <a href="${url_user_profile}${username}/" >u/${username}</a>
                <div class="community-button p-comm-btn-submit post-btn-submit" id="add_btn_${username}"> 
                    <div class="community-button-text" onclick="modifyModerator('${username}', true, '${modify_url}')">
                        Add as Moderator
                    </div> 
                </div>
            </div>`;
}

function removeModeratorMinHTML(username, modify_url) {
    return `<div id="remove_${username}" style="margin-bottom: 10px" class="mods-list">
                <a href="${url_user_profile}${username}/" >u/${username}</a>
                <div class="community-button p-comm-btn-submit post-btn-submit" id="remove_btn_${username}"  onclick="modifyModerator('${username}', false, '${modify_url}');"> 
                    <div class="community-button-text">
                        Remove Moderator
                    </div> 
                </div>
            </div>`;
}

function addSearchHTML(username, modify_url) {
    searchResultsElement.innerHTML += "\n" + addModeratorMinHTML(username, modify_url);
}

function removeModeratorHTML(username, modify_url) {
    removeModeratorsElement.innerHTML += "\n" + removeModeratorMinHTML(username, modify_url);
}


function handleSearchSuccessData(data) {
    // console.log(data);
    result = data.result;
    // console.log(result);
    searchResultsElement.innerHTML = "";
    let count = 0;
    Object.keys(result).forEach(function(id) {
        count += 1;
        // console.log(id, result[id]);
        addSearchHTML(result[id], modify_url);
    });

    // console.log(count);

    if (count == 0) {
        searchResultsElement.innerHTML = "No matching results in community members...";
    }
}

searchMemberInput.addEventListener("keypress", function(e) {
    if (e.key == 'Enter')
    {
        searchMemberButton.click()
    }
})

searchMemberButton.addEventListener("click", function(event) {

    let searchQry = searchMemberInput.value;

    // console.log("url: "+search_url);

    if (/\s/.test(searchQry)) {
        // there are white spaces
        addNotification("There must not be any spaces in search query", "error");
        return;
    }

    $.ajax({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }, 

        type: 'POST',
        url: search_url,
        data: {
            'search_qry': searchQry,
        },
        success: function(data){
            handleSearchSuccessData(data);
        },
        error: function(error){
            console.log(error);
            addNotification("Server Error", "error");
        }
    });
});

function handleModifyModeratorSuccess(data, username) {
    isError = data["error"];
    if (isError) {
        addNotification(data["message"], "error");
    } else {
        addNotification(data["message"], "success");

        if (data['admin']) {
            // remove from search panel
            document.getElementById(`search_${username}`).remove();
            // add to remove panel
            removeModeratorHTML(username, modify_url);

        } else {
            // user in no longer an admin 
            // remove from moderator remove panel
            document.getElementById(`remove_${username}`).remove();
        }
    }
}

// send ajax request to server to modify the moderators
function modifyModerator(username, to_do, modify_url) {

    $.ajax({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }, 

        type: 'POST',
        url: modify_url,
        data: {
            'username': username,
            'to_do': to_do,
        },
        success: function(data){
            handleModifyModeratorSuccess(data, username);
        },
        error: function(error){
            console.log(error);
            addNotification("Server Error", "error");
        }
    });
}