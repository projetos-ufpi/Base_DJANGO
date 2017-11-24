
from django.contrib.auth.models import User
from .models import Area, UserProfile, Post, Comment
from django.shortcuts import render, get_object_or_404,render_to_response,redirect
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.template.context_processors import csrf
from .forms import RegistrationForm, EditProfileForm, ProfileForm, PostForm, CommentForm
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.utils import timezone

def teste(request):
    args = {'user': request.user}
    return render(request, 'teste.html', {'full_name': request.user.first_name, 'args': args})

def login_redirect(request):
	return redirect('/login')

def change_password_redirect(request):
	return redirect('/change-password')

def login(request):
    if not request.user.is_authenticated():
        c = {}
        c.update(csrf(request))
        return render_to_response("login.html",c)
    else:
        return HttpResponseRedirect('/profile')
            

def auth_view(request):
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	user = auth.authenticate(username=username, password=password)

	if user is not None:
		auth.login(request, user)
		return HttpResponseRedirect('/profile')
	else:
		return HttpResponseRedirect('/invalid')


def invalid_login(request):
	return render_to_response('invalid_login.html')

def logout(request):
	auth.logout(request)
	return render_to_response('logout.html')

def register_user(request):
	if not request.user.is_authenticated():
		form = RegistrationForm(request.POST or None)        
		if form.is_valid():
			user = form.save(commit=False)
			username = form.cleaned_data['username']
			first_name = form.cleaned_data['first_name']
			last_name = form.cleaned_data['last_name']			
			email = form.cleaned_data['email']
			password = form.cleaned_data['password1']
			password2 = form.cleaned_data['password2']
			if password != password2:
				if first_name == '' or last_name == '' or email == '':
					return render(request, 'register.html')
				else:
					return render(request, 'register.html')
			elif first_name == '' or last_name == '' or email == '':
				return render(request, 'register.html')
			user.set_password(password)
			user.save()


			if user is not None:
				if user.is_active:
					return redirect('/register_success')                    
		return render(request, 'register.html', {'form':form})
	else:
		return HttpResponseRedirect('/profile')


def register_success(request):
        return render(request, 'register_success.html')


def profile(request, pk=None):
    if not request.user.is_authenticated():
        return redirect('/login')
    else:
        if request.user.is_staff:
            return redirect('/admin')
        else:
            if pk:
                user = User.objects.get(pk=pk)
            else:
                user = request.user
            args = {'user': user}
            posts = Post.objects.filter(author=user)
            #posts = posts.objects.filter(published_date__lte=timezone.now()).order_by('published_date')


            return render(request, 'profile.html', {'full_name': request.user.first_name, 'args': args, 'posts': posts})

                


def edit_profile(request):
    if not request.user.is_authenticated():
        return redirect('/login')
    else:      
        if request.method == 'POST':
            form = EditProfileForm(request.POST, instance=request.user)

            if form.is_valid():
                form.save()
                return redirect('/profile')
        else:
            form = EditProfileForm(instance=request.user)
            args = {'form': form}
            return render(request, 'edit_profile.html', args)

                


def edit_habilidades(request, pk):
    if not request.user.is_authenticated():
        return redirect('/login')
    else:        
        usr = get_object_or_404(UserProfile, pk=pk)

        if request.method == 'POST':
            form = ProfileForm(request.POST, instance=usr)

            if form.is_valid():
                usr = form.save(commit=False)
                usr.save()
                return redirect('/profile')
        else:
            form = ProfileForm(instance=usr)   
            
        return render(request, 'edit_habilidades.html', {'form': form})
                

def change_password(request):
    if not request.user.is_authenticated():
        return redirect('/login')
    else: 
        if request.method == 'POST':
            form = PasswordChangeForm(data=request.POST, user=request.user)

            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                return redirect('/profile')
            else:
                return redirect('/change-password')
        else:
            form = PasswordChangeForm(user=request.user)

            args = {'form': form}
            return render(request, 'change_password.html', args)



def post_list(request):
    if not request.user.is_authenticated():
        return redirect('/login')
    else:
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return redirect('/post/'+str(post.pk)+'/')
        else:
            form = PostForm()
        
        return render(request, 'home.html', {'posts': posts, 'form': form,})

def post_detail(request, pk):
    if not request.user.is_authenticated():
        return redirect('/login')
    else:    
        post = get_object_or_404(Post, pk=pk)

        if request.method == "POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.save()
                return redirect('/post/'+str(post.pk)+'/')
        else:
            form = CommentForm()

        return render(request, 'post_detail.html', {'post': post, 'form': form})

def post_new(request):
    if not request.user.is_authenticated():
        return redirect('/login')
    else:    
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return redirect('/post/'+str(post.pk)+'/')
        else:
            form = PostForm()
        
        args = "Publicar"
        return render(request, 'post_edit.html', {'form': form, 'args': args})

def post_edit(request, pk):
    if not request.user.is_authenticated():
        return redirect('/login')
    else:    
        post = get_object_or_404(Post, pk=pk)
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return redirect('/post/'+str(post.pk)+'/')
        else:
            form = PostForm(instance=post)

        args = "Alterar"
        return render(request, 'post_edit.html', {'form': form, 'args': args, 'pk': pk})

def post_remove(request, pk):
    if not request.user.is_authenticated():
        return redirect('/login')
    else:    
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return redirect('/profile')

def add_comment_to_post(request, pk):
    if not request.user.is_authenticated():
        return redirect('/login')
    else:    
        post = get_object_or_404(Post, pk=pk)
        if request.method == "POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.save()
                return redirect('/post/'+str(post.pk)+'/')
        else:
            form = CommentForm()
        return render(request, 'add_comment_to_post.html', {'form': form})


def comment_approve(request, pk):
    if not request.user.is_authenticated():
        return redirect('/login')
    else:    
        comment = get_object_or_404(Comment, pk=pk)
        comment.approve()
        return redirect('/post/'+str(comment.post.pk)+'/')


def comment_remove(request, pk):
    if not request.user.is_authenticated():
        return redirect('/login')
    else:    
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return redirect('/post/'+str(comment.post.pk)+'/')
