from django.views.generic.edit import UpdateView
from django import forms
from .import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserProfile, Area, Post, Comment


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            )


    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class ProfileForm(forms.ModelForm):
    habilidades = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Area.objects.all())
    biografia = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = UserProfile
        fields = ('image',
                  'biografia',
                  'telefone',
                  'profissao', 
                  'cidade', 
                  'skype',  
                  'habilidades'
                  )
        
class EditProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email',
                  'first_name',
                  'last_name',
                  'password'
                  )


class PostForm(forms.ModelForm):
    #area = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Area.objects.all())
    
    class Meta:
        model = Post
        fields = ('title', 
                  'text',
                  'area'
                  )


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',
                  )

'''        

class PostForm(forms.ModelForm):
  area = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Area.objects.all())
  post = forms.CharField(widget=forms.Textarea)
  
  class Meta:
    model = Post
    fields = ('titulo', 
              'post',
              'area'
              )

class PostForm(forms.ModelForm):
  area = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Areas.objects.all())
  
  class Meta:
    model = Post
    fields = ('titulo', 'post','anexo', 'exibir_perfil','area')
'''