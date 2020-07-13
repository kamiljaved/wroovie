from django import forms
from django.forms import TextInput, ChoiceField
from django.contrib.auth.models import User
from django.forms import ModelForm
from django_summernote.widgets import SummernoteWidget
from trix.widgets import TrixEditor
from .models import Article, Post, Thread
from community.models import Community
from common.utils import stripTagsHTML
from datetime import date, timedelta
import re 

#####~~~~~ APP VARIABLES ~~~~~#####
BASE_TEMPLATE_URL = 'posts'
# max posts limit in one community for a user
MAX_POSTS_PER_COMMUNITY_PER_24HRS = 5   # per user


#####~~~~~ FORM ~~~~~#####
# article creation form
class ArticleCreateForm(forms.ModelForm):
    class Meta:
        model = Article
        
        widgets = {
            'content': SummernoteWidget(),
            'title': TextInput(attrs={'placeholder':'Title'}),
        }
        fields = ['community', 'title', 'content']
    
    def __init__(self, user, *args, **kwargs):
        super(ArticleCreateForm, self).__init__(*args, **kwargs)
        community = [('', '*  Choose a Community')] + [(i.name, f'c/{i.name}') for i in user.joined_communities.all()]
        self.fields['community'] = forms.ChoiceField(choices=community)
        self.user = user

    def clean_community(self):
        comm_name = self.cleaned_data.get('community')
        try:
            community = Community.objects.get(name=comm_name)
        except Post.DoesNotExist:
            raise forms.ValidationError(f"Please select a valid community.")
            return comm_name 

        #####~~~~~ CONSTRAINT (1) ~~~~~#####
        # test if user is member of this commuity
        if self.user not in community.members.all():
            raise forms.ValidationError(f"You must be a member of c/{community.name} to post there.")
            return comm_name 

        #####~~~~~ CONSTRAINT (4) ~~~~~#####
        # test if user has made any other posts in this community in the last 24 hrs (not allow if limit exceeds) 
        posts_24hrs = community.posts.filter(dt_creation__gte=(date.today() - timedelta(days=1)), author=self.user).count()
        if posts_24hrs >= MAX_POSTS_PER_COMMUNITY_PER_24HRS:
            raise forms.ValidationError("You've already contributed a lot today! Choose a different community or try again in a few hours.")
            return comm_name 

        # tests for community passed (return community object)
        return community

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if content is None or content == "":
            raise forms.ValidationError(f"No content in Post.")
        else:
            # check for text in html
            content_text = re.sub(r'\s+', '', stripTagsHTML(content))
            if content_text is None or content_text == "":
                raise forms.ValidationError(f"No proper content in Post.")
        return content

#####~~~~~ FORM ~~~~~#####
# thread creation form
class ThreadCreateForm(forms.ModelForm):
    content = forms.CharField(widget=TrixEditor)

    class Meta:
        model = Thread
        fields = ['community', 'title', 'content']

        widgets = {
            'title': TextInput(attrs={'placeholder':'Title'}),
        }

    def __init__(self, user, *args, **kwargs):
        super(ThreadCreateForm, self).__init__(*args, **kwargs)
        community = [('', '*  Choose a Community')] + [(i.name, f'c/{i.name}') for i in user.joined_communities.all()]
        self.fields['community'] = forms.ChoiceField(choices=community)
        self.user = user

    def clean_community(self):
        comm_name = self.cleaned_data.get('community')
        try:
            community = Community.objects.get(name=comm_name)
        except Post.DoesNotExist:
            raise forms.ValidationError(f"Please select a valid community.")
            return comm_name 

        #####~~~~~ CONSTRAINT (1) ~~~~~#####
        # test if user is member of this commuity
        if self.user not in community.members.all():
            raise forms.ValidationError(f"You must be a member of c/{community.name} to post there.")
            return comm_name 

        #####~~~~~ CONSTRAINT (4) ~~~~~#####
        # test if user has made any other posts in this community in the last 24 hrs (not allow if limit exceeds) 
        posts_24hrs = community.posts.filter(dt_creation__gte=(date.today() - timedelta(days=1)), author=self.user).count()
        if posts_24hrs >= MAX_POSTS_PER_COMMUNITY_PER_24HRS:
            raise forms.ValidationError("You've already contributed a lot today! Choose a different community or try again in a few hours.")
            return comm_name 

        # tests for community passed (return community object)
        return community

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if content is None or content == "":
            raise forms.ValidationError(f"No content in Post.")
        else:
            # check for text in html
            content_text = re.sub(r'\s+', '', stripTagsHTML(content))
            if content_text is None or content_text == "":
                raise forms.ValidationError(f"No proper content in Post.")
        return content

#####~~~~~ FORM ~~~~~#####
# article update form
class ArticleUpdateForm(forms.ModelForm):
    class Meta:
        model = Article
        widgets = {
            'content': SummernoteWidget(),
        }
        fields = ['title', 'content']

#####~~~~~ FORM ~~~~~#####
# thread update form
class ThreadUpdateForm(forms.ModelForm):
    content = forms.CharField(widget=TrixEditor)

    class Meta:
        model = Thread
        fields = ['title', 'content']
    
#####~~~~~ FORM ~~~~~#####
# reply create form
class ReplyForm(forms.ModelForm):
    content = forms.CharField(widget=TrixEditor)

    class Meta:
        model = Thread
        fields = ['content']
