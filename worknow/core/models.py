from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils import timezone


class Area(models.Model):
    nome_area = models.CharField(max_length=100, verbose_name='Area')

    def __str__(self):
        return self.nome_area


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    profissao = models.CharField(max_length=100, default='', blank=True)
    cidade = models.CharField(max_length=100, default='', blank=True )
    skype = models.CharField(max_length=100, default='', blank=True)
    telefone = models.CharField(max_length=100, default='', blank=True)
    biografia = models.CharField(max_length=250, default='', blank=True)
    image = models.ImageField(upload_to='profile_image', blank=True, verbose_name="Imagem de perfil")
    habilidades = models.ManyToManyField(Area, blank=True)


    def __str__(self):
        return self.user.username

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)


class Post(models.Model):
    author = models.ForeignKey(User, verbose_name="Autor")
    title = models.CharField(max_length=200, verbose_name= "Título")
    text = models.TextField(verbose_name="Conteúdo")
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    area = models.ManyToManyField(Area)


    def publish(self):
        self.published_date = timezone.now()
        self.save()
    def approved_comments(self):
        return self.comments.filter(approved_comment=True)        

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey('Post', related_name='comments')
    author = models.ForeignKey(User, default=1, verbose_name="Autor")
    text = models.TextField(verbose_name="Comentário")
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

