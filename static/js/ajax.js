function load_page(
    page_url, paginationfield_id, loadbutton_id, pagediv_id, respondbutton_id
){
    var page = parseInt($(paginationfield_id).val());
    $(loadbutton_id).prop("disabled", true);
    $(loadbutton_id).text("Loading ...");

    $.ajax({
        async: true,
        type: "GET",
        url: page_url,
        data: { page: page },
        error: function() {
            $(loadbutton_id).replaceWith("<p></p>");
            $(respondbutton_id).replaceWith("");
        },
        success: function(data){
            $.ajax({
                async: true,
                type: "HEAD",
                url: page_url,
                data: { page: page + 1 },
                error: function(data){
                    $(loadbutton_id).replaceWith("<div class='button'>No more comments</div>");
                    $(respondbutton_id).replaceWith("");
                },
                success: function(response){
                    $(loadbutton_id).text("Load older comments");
                    $(respondbutton_id).replaceWith("");
                    $(paginationfield_id).val(page + 1);
                    $(loadbutton_id).prop("disabled", false);
                }
            });
            $(pagediv_id).append($(data).find("div"));
        }
    });
}

function load_comment(
    page_url, pagediv_id, nick_id, body_id
){
    var nick = $(nick_id).val();
    var body = $(body_id).val();
    $.ajax({
        type : "POST",
        url : page_url,
        data : { nick : nick, body : body },
        success : function(data) {
            $(nick_id).val('');
            $(body_id).val('');
            $.ajax({
                type: "HEAD",
                url: page_url,
                data: { nick: nick, body: body },
                error: function(){
                },
                success: function(response){
                }
            });
            $(pagediv_id).prepend($(data).find("div"));
        },
        error : function(xhr,errmsg,err) {
        }
    });
}

function add_like(page_url, likebutton_id, comment_id, comment_likes){
    var likes = parseInt(comment_likes);
    $.ajax({
        type: "GET",
        url: page_url,
        error: function() {
        },
        success: function() {
            var new_likes = likes + 1;
            var color;
            if(new_likes == 0){
                color = "grey"
            } else if(new_likes >0){
                color = "green"
            } else{
                color = "red"
            }
            $(comment_id).replaceWith("<span class='box " + color + "'><span id='" + comment_id + "'>" + new_likes + "</span></span>");
            $(likebutton_id).parent().replaceWith("<span class='f-green liked'>Liked</span>");
            var name = comment_id.substring(11)
            name = "span_id".concat(name);
            Cookies.set(name, 1);
        }
    });
}

function add_dislike(page_url, dislikebutton_id, comment_id, comment_likes){
    var likes = parseInt(comment_likes);
    $.ajax({
        type: "GET",
        url: page_url,
        error: function() {
        },
        success: function() {
            var new_likes = likes - 1;
            var color;
            if(new_likes == 0){
                color = "grey"
            } else if(new_likes >0){
                color = "green"
            } else{
                color = "red"
            }
            $(comment_id).replaceWith("<span class='box " + color + "'><span id='" + comment_id + "'>" + new_likes + "</span></span>");
            $(dislikebutton_id).parent().replaceWith("<span class='f-red disliked'>Disliked</span>");
            var name = comment_id.substring(11)
            name = "span_id".concat(name);
            Cookies.set(name, 0);
        }
    });
}