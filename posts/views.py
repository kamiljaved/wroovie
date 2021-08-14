from datetime import date, timedelta
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from .forms import ArticleCreateForm, ThreadCreateForm, ArticleUpdateForm, ThreadUpdateForm, ReplyForm
from .models import Post, Reply, Thread, Article
from common.views import qget_suggPosts, qget_suggCommunities
from django.template.loader import render_to_string
from common.utils import stripTagsHTML
import re

#####~~~~~ RELATED CONSTRAINTS ~~~~~#####
# 1. A User must be a member of a Community to be able to make a Post in that Community.
# 4. A User can make only a certain number of Posts (limit is TBD) in a given Community on a given day (24-hour period).
# 5. A User can leave only a certain number of Replies (limit is TBD) on a given Post.

#####~~~~~ APP VARIABLES ~~~~~#####
BASE_TEMPLATE_URL = 'posts'
# max posts limit in one community for a user
MAX_POSTS_PER_COMMUNITY_PER_24HRS = 5   # per user
# max replies limit on a post for a user
MAX_REPLIES_PER_POST = 10               # per user
MAX_VISIBLE_REPLY_LEVEL = 5

#####~~~~~ VIEW ~~~~~#####
# post detail view
def post(request, slug):
    try:
        post = Post.objects.get(slug__iexact=slug)
    except Post.DoesNotExist:
        raise Http404(f"Post does not exist.")
    # update post views
    # django handles distinctness of users in views
    if request.user.is_authenticated and request.user not in post.views.all():
        post.views.add(request.user)
    user_is_member = False
    if request.user.is_authenticated:
        user_is_member = request.user.joined_communities.filter(pk = post.community.id).exists()
    # suggest other top posts from community (5)
    p_c_top_posts = post.community.get_top_posts(5)
    context = {
        'post': post, 
        'replies': Reply.objects.filter(post=post), 
        'reply_count': post.get_reply_count(),
        'user_is_member': user_is_member,
        'p_c_top_posts': p_c_top_posts,
        'reply_form': ReplyForm(),
    }
    # send suggestions if user is authenticated
    if request.user.is_authenticated:
        sugg_comm = qget_suggCommunities(request.user, 5)
        sugg_posts = qget_suggPosts(sugg_comm, 5)
        context['sugg_comm'] = sugg_comm
        context['sugg_posts'] = sugg_posts
    return render(request, BASE_TEMPLATE_URL+'/post_detail.html', context)

#####~~~~~ VIEW ~~~~~#####
# post create view (accepts a thread or article form)
@login_required
def create(request, Form, post_type='Thread'):
    # TODO: IMPORTANT: check if the content is empty or not before saving
    # test if user email is verified
    if not request.user.profile.email_verified:
        messages.warning(request, f'Please verify your email address first.')
        return redirect("home")
    if request.method == 'POST':
        form = Form(request.user, request.POST)
        if form.is_valid():
            # test passed
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            post.views.add(post.author)
            return redirect('post-detail', post.slug)
        else:
            return render(request, BASE_TEMPLATE_URL+'/create.html', {'form': form, 'post_type': post_type})
    else:
        form = Form(request.user)
        return render(request, BASE_TEMPLATE_URL+'/create.html', {'form': form, 'post_type': post_type})

#####~~~~~ VIEW ~~~~~#####
# article create view
@login_required
def createArticle(request):
    return create(request, ArticleCreateForm, 'Article')

#####~~~~~ VIEW ~~~~~#####
# thread create view
@login_required
def createThread(request):
    return create(request, ThreadCreateForm, 'Thread')

#####~~~~~ VIEW ~~~~~#####
# post update view (accepts a thread or article form)
@login_required
def updatePost(request, slug, post, Form): 
    # test if user is post author, if not redirect to post page
    if post.author != request.user:
        messages.warning(request, f'You are not authorized to view requested page.')
        return redirect('post-detail', slug)
    if request.method == 'POST':
        form = Form(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect('post-detail', post.slug)
        else:
            raise forms.ValidationError("Please fix the errors.")
    else:
        form = Form(instance=post)
        return render(request, BASE_TEMPLATE_URL+'/update.html', {'form': form})

#####~~~~~ VIEW ~~~~~#####
# post update view
@login_required
def update(request, slug):
    # get the post if it exists
    try:
        post = Post.objects.get(slug__iexact=slug)
    except Post.DoesNotExist:
        raise Http404(f"Post does not exist.")
    # post exists: get type, call update 
    if post.get_type() == 'Article':
        return updatePost(request, slug, post, ArticleUpdateForm)
    else:
        return updatePost(request, slug, post, ThreadUpdateForm)

#####~~~~~ VIEW ~~~~~#####
# post delete view
@login_required
def delete(request, slug):
    # get the post if it exists
    try:
        post = Post.objects.get(slug__iexact=slug)
    except Post.DoesNotExist:
        raise Http404(f"Post does not exist.")
    # test if user is post author, if not redirect to post page
    if post.author != request.user:
        messages.warning(request, f'You are not authorized for this action.')
        return redirect('post-detail', slug)
    if request.method == 'POST':
        community = post.community
        post.delete()
        return redirect('community-home', community.name)
    else:    
        return render(request, BASE_TEMPLATE_URL+'/delete.html', {'post': post})

#####~~~~~ VIEW ~~~~~##### (AJAX)
# reply create view (could be reply to post or to another view)
@login_required
def createReply_AJAX(request, slug):
    if not (request.method == "POST" and request.is_ajax()):
        return JsonResponse({'message': f'Not authorized.'})
    # get the post if it exists
    try:
        post = Post.objects.get(slug__iexact=slug)
    except Post.DoesNotExist:
        return JsonResponse({'message': f'Post does not exist.'})
    # test if user email is verified
    if not request.user.profile.email_verified:
        return JsonResponse({'message': f'Please verify your email address first.'})
    #####~~~~~ CONSTRAINT (5) ~~~~~#####
    # test if user has already made replies on this post
    # if no. of replies by user is above limit for this post, dont allow
    prev_replies = post.replies.filter(author=request.user).count()
    if prev_replies >= MAX_REPLIES_PER_POST and not request.user.is_staff:
        return JsonResponse({'message': f"You've already made too many replies on this Post."})
    added = False
    message = ""
    # all tests passed, reply can be added, parse request content
    parent_id = None if request.POST['parent'] == "" else int(request.POST['parent'])
    parent = None
    if parent_id is not None:
        # get the reply parent (from the post) if exists
        try:
            parent = post.replies.get(id=parent_id)
        except Reply.DoesNotExist:
            message = f'Parent Reply does not exist.'
    # if we are here, there either isn't a parent reply, or the parent reply has been successfully found
    # parse rest of request content
    content  = request.POST['content']
    if content is None or content == "":
        message = f'No content in Reply.'
    else:
        # check for text in html
        content_text = re.sub(r'\s+', '', stripTagsHTML(content))
        if content_text is None or content_text == "":
            message = f'No proper content in Reply.'
        else:
            # create and save Reply
            reply = Reply(post=post, author=request.user, parent=parent, content=content)
            reply.save()
            added = True
            message = "Successfully added Reply."
    data = {
        "added": added,
        "message": message
    }
    if data['added']:
        if reply.level < MAX_VISIBLE_REPLY_LEVEL:
            data['reply_html'] = render_to_string(BASE_TEMPLATE_URL+'/reply.html', {
                'user': request.user,
                'reply': reply,      
            }) 
        elif reply.level == MAX_VISIBLE_REPLY_LEVEL:
            data['show_more_replies'] = True
    return JsonResponse(data)

#####~~~~~ VIEW ~~~~~##### (AJAX)
# reply update view
@login_required
def updateReply_AJAX(request):
    if not (request.method == "POST" and request.is_ajax()):
        return JsonResponse({'message': f'Not authorized.'})
    # parse the reply id from request content
    reply_id = request.POST['reply']
    # get the reply if it exists
    try:
        reply = Reply.objects.get(id=reply_id)
    except Reply.DoesNotExist:
        return JsonResponse({'message': f'Reply does not exist.'})
    # test if user is author of reply
    if reply.author != request.user:
        return JsonResponse({'message': f'You are not authorized for this action.'})
    updated = False
    message = ""
    # parse the rest of request content
    content  = request.POST['content']
    if content is None:
        message = f'No content in Reply.'
    else:
        reply.content = content
        reply.save()
        updated = True
        message = "Successfully updated Reply."
    data = {
        "updated": updated,
        "message": message
    }
    return JsonResponse(data)

#####~~~~~ VIEW ~~~~~##### (AJAX)
# reply delete view
@login_required
def deleteReply_AJAX(request):
    if not (request.method == "POST" and request.is_ajax()):
        return JsonResponse({'message': f'Not authorized.'})
    # parse the reply id from request content
    reply_id = request.POST['reply']
    # get the reply if it exists
    try:
        reply = Reply.objects.get(id=reply_id)
    except Reply.DoesNotExist:
        return JsonResponse({'message': f'Reply does not exist.'})
    # test if user is author of reply
    if reply.author != request.user:
        return JsonResponse({'message': f'You are not authorized for this action.'})
    deleted = False
    message = ""
    # parse the rest of request content
    content  = request.POST['content']
    if content is None:
        message = f'No content in Reply.'
    else:
        reply.content = content
        reply.save()
        deleted = True
        message = "Successfully deleted Reply."
    data = {
        "deleted": deleted,
        "message": message
    }
    return JsonResponse(data)

#####~~~~~ VIEW ~~~~~##### (AJAX)
# post vote toggle view
@login_required
def postVoteToggle_AJAX(request):
    if not (request.method == "POST" and request.is_ajax()):
        return JsonResponse({'error':True, 'message': f'Not authorized.'})
    # test if user email is verified
    if not request.user.profile.email_verified:
        return JsonResponse({'error':True, 'message': f'Please verify your email address first.'})
    post_id = request.POST['post_id']
    # get the post if it exists
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({'error':True, 'message': f'Post does not exist.'})
    # parse upvote/downvote
    vote = request.POST['vote']
    upvoted = False
    downvoted = False
    if vote == "up":
        if request.user in post.downvotes.all():
            post.downvotes.remove(request.user)
        if request.user in post.upvotes.all():
            post.upvotes.remove(request.user)
        else:
            post.upvotes.add(request.user)
            upvoted = True
    elif vote == "down":
        if request.user in post.upvotes.all():
            post.upvotes.remove(request.user)
        if request.user in post.downvotes.all():
            post.downvotes.remove(request.user)
        else:
            post.downvotes.add(request.user)
            downvoted = True
    data = {
        'error': False,
        "upvoted": upvoted,
        "downvoted": downvoted,
        'score': post.get_score_string()
    }
    return JsonResponse(data)

#####~~~~~ VIEW ~~~~~##### (AJAX)
# reply vote toggle view
@login_required
def replyVoteToggle_AJAX(request):
    if not (request.method == "POST" and request.is_ajax()):
        return JsonResponse({'error':True, 'message': f'Not authorized.'})
    # test if user email is verified
    if not request.user.profile.email_verified:
        return JsonResponse({'error':True, 'message': f'Please verify your email address first.'})
    reply_id = request.POST['reply_id']
    # get the reply if it exists
    try:
        reply = Reply.objects.get(id=reply_id)
    except Reply.DoesNotExist:
        return JsonResponse({'error':True, 'message': f'Reply does not exist.'})
    # parse upvote/downvote
    vote = request.POST['vote']
    upvoted = False
    downvoted = False
    if vote == "up":
        if request.user in reply.downvotes.all():
            reply.downvotes.remove(request.user)
        if request.user in reply.upvotes.all():
            reply.upvotes.remove(request.user)
        else:
            reply.upvotes.add(request.user)
            upvoted = True
    elif vote == "down":
        if request.user in reply.upvotes.all():
            reply.upvotes.remove(request.user)
        if request.user in reply.downvotes.all():
            reply.downvotes.remove(request.user)
        else:
            reply.downvotes.add(request.user)
            downvoted = True
    data = {
        'error': False,
        "upvoted": upvoted,
        "downvoted": downvoted,
        'score': reply.get_score_string()
    }
    return JsonResponse(data)


#####~~~~~ VIEW ~~~~~##### (AJAX)
# post save toggle view
@login_required
def postSaveToggle_AJAX(request):
    if not (request.method == "POST" and request.is_ajax()):
        return JsonResponse({'message': f'Not authorized.'})
    # test if user email is verified
    if not request.user.profile.email_verified:
        return JsonResponse({'message': f'Please verify your email address first.'})
    post_id = request.POST['post_id']
    # get the post if it exists
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({'message': f'Post does not exist.'})
    # save/unsave
    saved = False
    if post in request.user.profile.saved_posts.all():
        request.user.profile.saved_posts.remove(post)
    else:
        request.user.profile.saved_posts.add(post)
        saved = True
    data = {
        "saved": saved,
    }
    return JsonResponse(data)