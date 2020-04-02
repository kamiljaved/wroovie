var followUrl = '/api/profile/'+profileid+'/follow/'
$("#followBtn").click(function(e){
    e.preventDefault()
    $.ajax({
        url: followUrl, 
        method: "GET",
        data: {},
        success: function(data){
            if (data['followed'])
            {
                $("#followBtnAdd1").css("color", "#4edcff");
                $("#followBtnAdd2").css("text-shadow", "0px 0px 7px");
            }
            else
            {
                $("#followBtnAdd1").css("color", "");
                $("#followBtnAdd2").css("text-shadow", "");
            }
        },
        error: function(error){
        }

    });
});