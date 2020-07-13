import random
import re
from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import redirect, render
from community.models import Community, Membership
from posts.models import Post
from collections import Counter
from django.contrib import messages


from django.contrib.auth.models import User

import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
nltk.download('stopwords')
nltk.download('punkt')

#####~~~~~ APP VARIABLES ~~~~~#####
BASE_TEMPLATE_URL = 'common'
# max posts-to-send limits
MAX_POSTS = 25
MAX_LATEST_POSTS = 50
MAX_TOP_POSTS = 50
HOME_MAX_DAYS = 7
MAX_SUGGESTED_COMMUNITIES = 10
MAX_LIST_SIZE = 500
POPULAR_MAX_DAYS = 15
MAX_TOP_COMMUNITIES = 50
POPULAR_SCORE_THRESH = 1

MAX_SEARCH_QUERY_LEN = 100

#####~~~~~ VIEW ~~~~~#####
# site homepage view
def home(request):    
    if request.user.is_authenticated:
        if request.user.profile.email_verified:
            ##### USER AUTHENTICATED ##### (SHOW PERSONALIZED JOINED-COMM-CONTENT)
            # send user followed communities latest (within 7x24 hours) posts (latest first)
            jc = request.user.joined_communities.values_list('id')
            posts = Post.objects.filter(community__in=jc, dt_creation__gte=(date.today() - timedelta(days=HOME_MAX_DAYS))).order_by('-dt_creation')
            # show/add old posts if nothing new in this week
            count = posts.count()
            if count < MAX_POSTS:
                posts = posts | Post.objects.filter(community__in=jc).exclude(id__in=posts.values_list('id', flat=True)).order_by('-dt_creation')
                posts = posts[:MAX_POSTS]
            elif count > MAX_POSTS:
                posts = posts[:MAX_POSTS]
            # ----- also send (few) ----
            # recently joined communities   (5)     # user's posts                  (5)
            # top communities               (5)     # trending communities          (5)
            # suggested posts               (5)     # suggested communities         (5)
            rec_memb = Membership.objects.filter(user=request.user).order_by('-dt_join')[:5]
            usr_posts = request.user.posts.order_by('-dt_creation')[:5]
            top_comm = qget_topCommunities(5)
            trnd_comm = qget_trendingCommunities(5)
            sugg_comm = qget_suggCommunities(request.user, 5)
            sugg_posts = qget_suggPosts(sugg_comm, 5)
            context = {
                'user': request.user,
                'posts': posts,
                'rec_memb': rec_memb,
                'usr_posts': usr_posts,
                'top_comm': top_comm,
                'trnd_comm': trnd_comm,
                'sugg_comm': sugg_comm,
                'sugg_posts': sugg_posts,
                'show_comm_info': True, # feed-view
                'empty_text': "Its a little lonely here :(",
                'feed': 'home',
            }
            return render(request, 'common/home.html', context)
        else:
            # messages.warning(request, f'Please verify your email address.')
            # redirect to top posts
            return redirect('top')
    else:
        ##### NOT AUTHENTICATED #####
        # redirect to top posts
        return redirect('top')

#####~~~~~ UTILITY FUNCTION ~~~~~#####
# basic feed data
def getFeedContext(request, posts, feed, empty_text):
    # ----- also send (few) ----
    # top communities               (5)     # trending communities          (5)
    top_comm = qget_topCommunities(5)
    trnd_comm = qget_trendingCommunities(5)
    context = {
        'posts': posts,
        'top_comm': top_comm,
        'trnd_comm': trnd_comm,
        'show_comm_info': True, # feed-view
        'empty_text': empty_text,
        'feed': feed,
    }
    if request.user.is_authenticated:
        rec_memb = Membership.objects.filter(user=request.user).order_by('-dt_join')[:5]
        usr_posts = request.user.posts.order_by('-dt_creation')[:5]
        sugg_comm = qget_suggCommunities(request.user, 5)
        sugg_posts = qget_suggPosts(sugg_comm, 5)
        context.update({
            'rec_memb': rec_memb,
            'usr_posts': usr_posts,
            'sugg_comm': sugg_comm,
            'sugg_posts': sugg_posts,
        })
    return context

#####~~~~~ UTILITY FUNCTION ~~~~~#####
# basic feed data
def getFeedContextMin(request, incl_top_comm=True, incl_trnd_comm=True, incl_rec_memb=False, incl_usr_posts=False):
    context = {}
    if incl_top_comm:
        top_comm = qget_topCommunities(5)
        context.update({
            'top_comm': top_comm,
        })
    if incl_trnd_comm:
        trnd_comm = qget_trendingCommunities(5)
        context.update({
            'trnd_comm': trnd_comm,
        })
    if request.user.is_authenticated:
        sugg_comm = qget_suggCommunities(request.user, 5)
        sugg_posts = qget_suggPosts(sugg_comm, 5)
        context.update({
            'sugg_comm': sugg_comm,
            'sugg_posts': sugg_posts,
        })
        if incl_rec_memb:
            rec_memb = Membership.objects.filter(user=request.user).order_by('-dt_join')[:5]
            context.update({
                'rec_memb': rec_memb,
            })
        if incl_usr_posts:
            usr_posts = request.user.posts.order_by('-dt_creation')[:5]
            context.update({
                'usr_posts': usr_posts,
            })
    return context

#####~~~~~ VIEW ~~~~~#####
# latest posts view (all)
# across-entire-site
def latest(request):
    # posts are already stored as latest first
    # TODO: add upvote/downvote/comments (involvement) level to qualify for latest feed
    posts = Post.objects.all()[:MAX_LATEST_POSTS]
    context = getFeedContext(request, posts, 'all', "No Latest Posts Yet")
    return render(request, BASE_TEMPLATE_URL+'/home.html', context)

#####~~~~~ VIEW ~~~~~#####
# top posts (all-time highest score) view
# across-entire-site
def top(request):
    # filter all posts based on (upvotes-downvotes)
    posts = Post.objects.annotate(count=(Count('upvotes__id')-Count('downvotes__id'))).order_by('-count', '-dt_creation')[:MAX_TOP_POSTS]
    context = getFeedContext(request, posts, 'top', "No Top Posts Yet")
    return render(request, BASE_TEMPLATE_URL+'/home.html', context)

#####~~~~~ VIEW ~~~~~#####
# top posts (recent high score) view
# across-entire-site
def popular(request):
    # filter recent month posts based on (upvotes-downvotes)
    # filter out posts with low score (below POPULAR_SCORE_THRESH)
    posts = Post.objects.filter(dt_creation__gte=(date.today() - timedelta(days=POPULAR_MAX_DAYS))).annotate(count=(Count('upvotes__id')-Count('downvotes__id'))).exclude(count__lt=POPULAR_SCORE_THRESH).order_by('-count', '-dt_creation')[:MAX_TOP_POSTS]
    context = getFeedContext(request, posts, 'popular', "No Popular Posts these days")
    return render(request, BASE_TEMPLATE_URL+'/home.html', context)

#####~~~~~ VIEW ~~~~~#####
# suggested communities and posts view (for registered users)
# suggest users communities of posts they've visited but don't follow that community
# and shows some of their posts
@login_required
def suggested(request):
    # joined communities
    jc = request.user.joined_communities.all().values_list('id', flat=True)
    # (distinct) communities for which posts viewed
    vpc = request.user.viewed_posts.all().values_list('community__id', flat=True).distinct().order_by()
    # communities for which posts viewed but not joined (also randomize)
    sugg_communities = Community.objects.filter(id__in=vpc).exclude(id__in=jc)
    sugg_communities = sorted(sugg_communities[:MAX_LIST_SIZE], key=lambda x: random.random())[:MAX_SUGGESTED_COMMUNITIES]
    # suggest some top posts from suggested communities (also randomize)
    sugg_posts_top = Post.objects.filter(community__in=sugg_communities).annotate(count=(Count('upvotes__id')-Count('downvotes__id'))).order_by('-count', '-dt_creation')
    sugg_posts_top = sorted(sugg_posts_top[:MAX_LIST_SIZE], key=lambda x: random.random())[:MAX_POSTS]
    # suggest some latest posts from suggested communities (also randomize)
    sugg_posts_latest = Post.objects.filter(community__in=sugg_communities, dt_creation__gte=(date.today() - timedelta(days=HOME_MAX_DAYS))).order_by('-dt_creation')
    sugg_posts_latest = sorted(sugg_posts_latest[:MAX_LIST_SIZE], key=lambda x: random.random())[:MAX_POSTS]
    context = {
        'communities': sugg_communities,
        'posts_top': sugg_posts_top,
        'posts_latest': sugg_posts_latest,
    }
    # sidebar+feed stuff
    top_comm = qget_topCommunities(5)
    trnd_comm = qget_trendingCommunities(5)
    context.update({
        'top_comm': top_comm,
        'trnd_comm': trnd_comm,
        'show_comm_info': True, # feed-view
        'empty_text': 'No Suggestions for You right now',
        'feed': 'suggested',
    })
    return render(request, BASE_TEMPLATE_URL+'/home.html', context)

#####~~~~~ QUERY FUNCTION ~~~~~#####
def qget_suggCommunities(user, cnt=MAX_SUGGESTED_COMMUNITIES):
    # joined communities
    jc = user.joined_communities.all().values_list('id', flat=True)
    # (distinct) communities for which posts viewed
    vpc = user.viewed_posts.all().values_list('community__id', flat=True).distinct().order_by()
    # communities for which posts viewed but not joined (also randomize)
    sugg_communities = Community.objects.filter(id__in=vpc).exclude(id__in=jc)
    return sorted(sugg_communities[:MAX_LIST_SIZE], key=lambda x: random.random())[:cnt]

#####~~~~~ QUERY FUNCTION ~~~~~#####
def qget_suggPosts(sugg_comm, cnt=MAX_POSTS):
    # suggest some top posts from suggested communities (also randomize)
    sugg_posts_top = Post.objects.filter(community__in=sugg_comm).annotate(count=(Count('upvotes__id')-Count('downvotes__id'))).order_by('-count', '-dt_creation')
    sugg_posts_latest = Post.objects.filter(community__in=sugg_comm, dt_creation__gte=(date.today() - timedelta(days=HOME_MAX_DAYS))).order_by('-dt_creation')
    sugg_posts = (sugg_posts_top | sugg_posts_latest).distinct()
    return sorted(sugg_posts[:MAX_LIST_SIZE], key=lambda x: random.random())[:cnt]

#####~~~~~ QUERY FUNCTION ~~~~~#####
def qget_topCommunities(cnt=MAX_TOP_COMMUNITIES):
    return Community.objects.all().annotate(count=Count('members')).order_by('-count')[:cnt]

#####~~~~~ QUERY FUNCTION ~~~~~#####
def qget_trendingCommunities(cnt=MAX_TOP_COMMUNITIES):
    comm_ids = list(dict(Counter(Post.objects.filter(dt_creation__gte=(date.today() - timedelta(days=50))).values_list('community__id', flat=True)).most_common()).keys())[:cnt]
    comm = Community.objects.in_bulk(comm_ids)
    return [comm[x] for x in comm_ids]

HTML_TAGS = ["a","abbr","acronym","address","area","b","base","bdo","big","blockquote","body","br","button","caption","cite","code","col","colgroup","dd","del","dfn","div","dl","DOCTYPE","dt","em","fieldset","form","h1","h2","h3","h4","h5","h6","head","html","hr","i","img","input","ins","kbd","label","legend","li","link","map","meta","noscript","object","ol","optgroup","option","p","param","pre","q","samp","script","select","small","span","strong","style","sub","sup","table","tbody","td","textarea","tfoot","th","thead","title","tr","tt","ul","var"]
# ENGLISH_STOPWORDS = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
STOPWORDS = set(stopwords.words('english'))
CUSTOM_STOPWORDS = []
for x in CUSTOM_STOPWORDS:
    STOPWORDS.append(x)
CUSTOM_REMOVES = []
for x in CUSTOM_REMOVES:
    STOPWORDS.remove(x)
    
# search throught communities, posts, and users
def search(search_qry, max_communities=10, max_posts=20, max_users=10):
    word_list = word_tokenize(search_qry)

    # filter the stop-words
    filtered_words = [w for w in word_list if not w in STOPWORDS]

    stemmed_list = []
    # stem the filtered words
    ps = PorterStemmer()
    for word in filtered_words:
        stemmed = ps.stem(word)
        if stemmed not in stemmed_list:
            stemmed_list.append(stemmed)

    final_word_list = stemmed_list

    b_moreComm = False
    b_morePosts = False
    b_moreUsers = False

    # get the communities with similar titles
    communities = []
    if max_communities > 0:
        q_object = None
        for word in filtered_words:
            q = Q(name__icontains=word) | Q(title__icontains=word)
            if q_object is not None:
                q_object &= q
            else:
                q_object = q

        if q_object is not None:
            communities = Community.objects.filter(q_object)
            if communities.count() > max_communities:
                b_moreComm = True
                communities = communities[:max_communities]

    # get the users with similar usernames
    users = []
    if max_users > 0:
        q_object = None
        for word in filtered_words:
            q = Q(username__icontains=word)
            if q_object is not None:
                q_object &= q
            else:
                q_object = q
        
        if q_object is not None:
            users = User.objects.filter(q_object)
            if users.count() > max_users:
                b_moreUsers = True
                users = users[:max_users]

    # get the posts with similar title
    posts = []
    if max_posts > 0:
        q_object = None
        for word in filtered_words:
            q = Q(title__icontains=word)
            if q_object is not None:
                q_object &= q
            else:
                q_object = q

        if q_object is not None:
            posts = Post.objects.filter(q_object)
            if posts.count() > max_posts:
                b_morePosts = True
                posts = posts[:max_posts]

        # match content?
        # words_without_html_tags = []
        # for word in filtered_words:
        #     if word not in HTML_TAGS and word not in words_without_html_tags:
        #         words_without_html_tags.append(word)

        # for word in words_without_html_tags:
        #     q = Q(content__icontains=word)
        #     if q_object is not None:
        #         q_object |= q
        #     else:
        #         q_object = q

    return {'posts': posts, 'communities': communities, 'users': users, 'more_comm':b_moreComm, 'more_posts':b_morePosts, 'more_users':b_moreUsers}

def search_view(request, search_qry):
    search_qry = re.sub(r'\s+', ' ', search_qry.strip())[:MAX_SEARCH_QUERY_LEN]
    search_result = search(search_qry)
    search_result['search_qry'] = search_qry
    search_result['show_comm_info'] = True

    return render(request, BASE_TEMPLATE_URL + '/search.html', search_result)

#####~~~~~ VIEW ~~~~~#####
# default HTTP 404 (ERROR: NOT FOUND) page view
def handler404(request, exception):
    return render(request, '404.html', {})
