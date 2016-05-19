from django import template


register = template.Library()


@register.assignment_tag(name="get_pageloader")
def get_pageloader(page_url, *args, **kwargs):
    pagediv_id = kwargs.get("pagediv_id", "pagediv-id")
    loadbutton_id = kwargs.get("loadbutton_id", "load-id")
    respondbutton_id = kwargs.get("respondbutton_id", "respond-id")
    pagination_id = kwargs.get("pagination_id", "pagination-id")
    button_script = """$("#%s").click(function(){load_page("%s", "#%s", "#%s", "#%s", "#%s");});""" % \
                    (loadbutton_id, page_url, pagination_id, loadbutton_id, pagediv_id, respondbutton_id)
    respond_button_script = """$("#%s").click(function(){load_page("%s", "#%s", "#%s", "#%s", "#%s");});""" % \
                            (respondbutton_id, page_url, pagination_id, loadbutton_id, pagediv_id, respondbutton_id)
    if pagediv_id == "pagediv-id":
        page = "div"
    else:
        page = "p"
    if loadbutton_id == "load-id":
        button = " main"
    else:
        button = " sub"
    return {
        # "pagediv": "<div class='comments' id='" + pagediv_id + "'></div>",
        "pagediv": "<" + page + " class='comments' id='" + pagediv_id + "'></" + page + ">",
        "respondbutton": "<button class='nothing2 f-grey' id='" + respondbutton_id + "' type='submit'>Respond</button>",
        "loadbutton": "<button class='center" + button + "' id='" + loadbutton_id + "' type='submit'>Show comments</button>",
        "pagination": "<input type='hidden' id='" + pagination_id + "' value='1'>",
        "button_script": button_script,
        "respond_button_script": respond_button_script,
        }


@register.assignment_tag(name="get_respondloader")
def get_respondloader(page_url, *args, **kwargs):
    pagediv_id = kwargs.get("pagediv_id", "pagediv-id")
    respondbutton_id = kwargs.get("respondbutton_id", "respond-id")
    pagination_id = kwargs.get("pagination_id", "pagination-id")
    respond_button_script = """$("#%s").click(function(){load_respond("%s", "#%s", "#%s", "#%s");});""" % \
                            (respondbutton_id, page_url, pagination_id, respondbutton_id, pagediv_id)
    return {
        "pagediv": "<p class='comments' id='" + pagediv_id + "'></p>",
        "respondbutton": "<button class='nothing f-grey' id='" + respondbutton_id + "' type='submit'>Respond</button>",
        "pagination": "<input type='hidden' id='" + pagination_id + "' value='1'>",
        "button_script": respond_button_script,
        }


@register.assignment_tag(name="get_commentloader")
def get_commentloader(page_url, *args, **kwargs):
    nick_id = kwargs.get("nick_id", "nick")
    body_id = kwargs.get("body_id", "body")
    pagediv_id = kwargs.get("pagediv_id", "pagediv-id")
    submit_button_id = kwargs.get("submit_button_id", "submit-button-id")
    submit_button_script = """$("#%s").on('submit', function(event){event.preventDefault(); load_comment("%s", "#added_%s", "#%s", "#%s");});""" % \
                           (submit_button_id, page_url, pagediv_id, nick_id, body_id)
    return {
        "pagediv": "<div class='comments' id='added_" + pagediv_id + "'></div>",
        "submit_button": "<input type='submit' name='submit' value='Add comment' class='form-button'>",
        "submit_button_script": submit_button_script,
        }


@register.assignment_tag(name="get_likes")
def get_likes(page_url, page_url2, *args, **kwargs):
    comment_id = kwargs.get("comment_id", "comment-id")
    comment_likes = kwargs.get("comment_likes", "0")
    likebutton_id = kwargs.get("likebutton_id", "likebutton-id")
    dislikebutton_id = kwargs.get("dislikebutton_id", "dislikebutton-id")
    like_script = """$("#%s").click(function(){add_like("%s", "#%s", "#%s", "%s");});""" % \
                  (likebutton_id, page_url, likebutton_id, comment_id, comment_likes)
    dislike_script = """$("#%s").click(function(){add_dislike("%s", "#%s", "#%s", "%s");});""" % (dislikebutton_id, page_url2, dislikebutton_id, comment_id, comment_likes)
    return {
        "comment_id": "<span id='" + comment_id + "'>" + comment_likes + "</span>",
        "likebutton_id": "<button class='nothing f-green' id='" + likebutton_id + "' type='submit'><i class='fa fa-plus'></i></button>",
        "dislikebutton_id": "<button class='nothing f-red' id='" + dislikebutton_id + "' type='submit'><i class='fa fa-minus'></i></button>",
        "like_script": like_script,
        "dislike_script": dislike_script,
        }


@register.assignment_tag(name="tag_comment_create")
def tag_comment_create(page_url, *args, **kwargs):
    post_form_id = kwargs.get("post_form_id", "post-form-id")
    comment_script = """$("#%s").on('submit', function(event){event.preventDefault(); comment_create("%s", "%s");});""" % (post_form_id, page_url, post_form_id)
    return {
        "comment_script": comment_script,
        }