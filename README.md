
<h1 align="center">
  <br>
  wroovie
  <br>
</h1>

<h4 align="center">Community-based Social Website.</h4>
<h4 align="center">
	<a href="https://wroovie.pythonanywhere.com/"> visit live website 
	</a>
</h4>
<p></p>

<p align="center">
	<a href="http://www.djangoproject.com/">
		<img src="https://www.djangoproject.com/m/img/badges/djangoproject120x25.gif" border="0" alt="A Django project." title="A Django project."/>
	</a>
  <a href="https://www.python.org/">
		<img src="http://ForTheBadge.com/images/badges/made-with-python.svg" alt=" Made with Python.">
  </a>
  <a href="https://www.w3.org/standards/webdesign/htmlcss">
		<img src="http://ForTheBadge.com/images/badges/uses-html.svg" height="30px" alt="Uses HTML.">
  </a>
  <a href="https://www.w3.org/standards/webdesign/htmlcss">
		<img src="http://ForTheBadge.com/images/badges/uses-css.svg" height="30px" alt="Uses CSS.">
  </a>
  <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript">
		<img src="http://ForTheBadge.com/images/badges/uses-js.svg" height="30px" alt="Uses JavaScript.">
  </a>
</p>

<p align="center">
  <a href="#languages">Languages</a> •
  <a href="#dependencies">Dependencies</a> •
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#notes">Notes</a>
</p>

<hr>

## Languages

* Python (Django Framework)
* HTML (Frontend)
* Javascript (jQuery & AJAX Libraries)
* MySQL (Database)

## Dependencies

* Required:
  - [Django Framework](https://www.djangoproject.com/)
* Optional:
  - [MySQL Server](https://dev.mysql.com/downloads/)

## Key Features

* Explore other people’s posts (top and latest)
* Sign up with email
* Verify email to start joining different communities
* Join any community to make their own posts in it
* Get customized home feed for joined communities
* Make different types of posts based on user’s need:
  - Create a discussion Thread
  - Create a professional Article
* Commenting system
  - Leave a comment on any post
  - Leave a reply on any comment/reply
* Upvote favorite content and comments
* Downvote disliked posts and comments
* Create a new community
  - Customize it to the user’s liking
  - Add new moderators from members
* Explore suggested posts and communities (content-based filtering)
* Explore top and popular communities
* Save a post if the user really likes it
* Search for content
  - Search for communities and posts
  - Search for other users
* Explore other users’ profiles and posts 
* Explore user’s own content
  - Get list of user’s own posts and comments
  - Explore user’s upvoted, downvoted, and 
saved posts
* Edit user profile to their liking
* Access all communities that the user moderates on a single page


## How To Use

Make sure [Python](https://www.python.org/) and [pip](https://pip.pypa.io/en/stable/installing/) is installed on your system. 
To clone this application, you'll need [Git](https://git-scm.com). From your command line:

```bash
# Clone this repository (or download from github page)
$ git clone https://github.com/kamiljaved98/wroovie

# Go into the repository
$ cd wroovie

# Install dependencies
$ pip(3) install -r requirements.txt

# Run the server
$ python(3) manage.py runserver

# Go to app-page in browser (localhost)
$ http://localhost:8000/
$ http://127.0.0.1:8000/
```
Or 	<a href="https://wroovie.pythonanywhere.com/">   visit live website</a>.

## Notes

* To avoid having to set up a MySQL server and database, modify wroovie/settings.py to use the default SQLite database.

* Manual Fixes required:

  1. In the installed python libraries, locate the "<b>trix</b>" app folder, and find the following line (usually line no. 10) in "<b>trix/widgets.py</b>":
		
		```python
			def render(self, name, value, attrs=None):
		```
		Change it to:
		
		```python
			def render(self, name, value, attrs=None, renderer=None):
		```

---

> [kamiljaved.pythonanywhere.com](https://kamiljaved.pythonanywhere.com/) &nbsp;&middot;&nbsp;
> GitHub [@kamiljaved](https://github.com/kamiljaved) [@UsmanAhmad4146](https://github.com/UsmanAhmad4146)
