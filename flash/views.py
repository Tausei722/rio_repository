from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponse
from django.views import generic
from django.core.exceptions import ValidationError
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import UserPassesTestMixin

import pdb
import os
from pathlib import Path
MEDIA_ROOT = os.path.join(Path(__file__).resolve().parent.parent, 'media')

from .models import CustomUser, Movie
from .forms import UserRegistrationForm, MovieForm
from .edit import recognition,make_movie,create_thumbnail
from django.views.decorators.csrf import csrf_exempt

class Template(generic.CreateView,generic.ListView):
    model = Movie
    form_class = MovieForm
    template_name = "flash/index.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        # pdb.set_trace()
        context['form'] = self.get_form()
        context['movies'] = Movie.objects.all()

        return context

    def form_valid(form,self,**kwargs):
        try:
            file = self.fields['movie']

            #一旦,動画保存場所に移動
            name = self.cleaned_data['movie'].name
            save_path = os.path.join(MEDIA_ROOT+'\\media\\', 'videos')
            os.makedirs(save_path,exist_ok=True)
            save_path = os.path.join(MEDIA_ROOT+'\\media\\', 'originally')
            os.makedirs(save_path,exist_ok=True)
            with open(os.path.join(save_path, name), 'wb+') as destination:
                for chunk in self.cleaned_data['movie'].chunks():
                    destination.write(chunk)
            saved_path = os.path.join(save_path,name)

            # サムネイルを作る
            thumbnail = create_thumbnail(saved_path)

            #動画を編集
            all_word = recognition(saved_path)
            print(all_word)
                #入れ子になってる配列をならすとき、後ろに連ねてく
            texts = [word for words in all_word['segments'] for word in words['words']]
            movie = make_movie(saved_path,texts)
                #ファイル自体じゃないとDBで保存してくれない
            output_path = os.path.join(MEDIA_ROOT+'\\media\\', movie[1])
            print(output_path)
            save_path = 'media' + output_path.replace(MEDIA_ROOT,"")
            originally_path = 'media' + saved_path.replace(MEDIA_ROOT,"")

        except Exception as e:
            # return render(form.request,'failed_save/failed_save.html',{'e':e})
            return redirect('failed_save')

        if movie:
            #保存
            if type(form.request.user.pk) != type(None):
                post_user = CustomUser.objects.get(id=form.request.user.pk)
            else:
                post_user = CustomUser.objects.get(id=1)
            try:
                Movie.objects.create(
                    movie = save_path,
                    originally_movie = originally_path,
                    post_user = post_user,
                    thumbnail = thumbnail,
                ).save()
                return redirect('success_save')
            except Exception as e:
                return render(form.request,'failed_save',{'e':e})
        else:
            return redirect('failed_save')
        
class FailedTemplate(generic.TemplateView):
    template_name = 'flash/failed_save.html'

class SuccessTemplate(generic.TemplateView):
    template_name = 'flash/success_save.html'

class SigninView(generic.CreateView):
    model = CustomUser
    form_class = UserRegistrationForm
    template_name = 'flash/signin_form.html'

    def form_valid(form,self,**kwargs):
        form = UserRegistrationForm(form.request.POST)
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()

        if user:
            data = user
            return redirect('signin_completion')
        else:
            message = 'サインインに失敗しました。もう一度確認してください'
            return render(form.request, 'singin_form.html', {'message':message, 'form':form})
        
class LoginCompletion(generic.TemplateView):
    template_name = "flash/signin_completion.html"

class LoginView(LoginView):
    form_class = AuthenticationForm
    template_name = "flash/login_form.html"

    #ログインが成功したときに呼び出されるメソッド
    def get_success_url(self):
        return reverse('home')

class LogoutSetView(generic.TemplateView):
    template_name = "flash/logout_set.html"

class LogoutView(LogoutView):
    template_name = "flash/logout.html"

#公開非公開を設定
class MoviePostMixin(generic.UpdateView):
    def post(self,form,*args,**kwargs):
        try:
            len(self.request.POST['private'])
            movie = Movie.objects.get(id=int(self.request.POST['private']))
            movie.public = True
            movie.save()
            
            # pdb.set_trace()
            return reverse(self.request,'flash/mypage',kwargs={'pk':self.request.user.pk})
        except Exception as e:
            print(e)

        try:
            len(self.request.POST['public'])
            movie = Movie.objects.get(id=int(self.request.POST['public']))
            movie.public = False
            movie.save()

            return reverse(self.request,'flash/mypage',kwargs={'pk':self.request.user.pk})
        except Exception as e:
            print(e)
            return super().post(self.request,*args,**kwargs)

#このようにMyPageとMoviePostMixinを分けることで継承したclassによって使えたり使えなかったdefや関数を使い分けることができる
#UserPassesTestMixinで特定のページに対応する権限のある内を判定(mypageViewにアクセスする権限をログインで判断)
class MyPage(UserPassesTestMixin, generic.DetailView, MoviePostMixin):
    model = CustomUser
    form_class = MovieForm
    template_name = 'flash/mypage.html'
    #今のユーザと一致するユーザ情報を持ってくることを許可
    def test_func(self):
        permission = self.request.user.pk == self.kwargs['pk']
        return permission
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)

        #ここから
        movies = Movie.objects.filter(post_user=self.request.user.pk)

        if movies == None:
            context['movies'] = Movie.objects.get(id=7)
        else:
            context['movies'] = movies
        return context
        
        #  def post(form,self,**kwargs):
        # try:
        #     len(form.request.POST['private'])
        #     movie = Movie.objects.get(id=int(form.request.POST['private']))
        #     movie.public = True
        #     movie.save()
            
        #     # pdb.set_trace()
        #     return reverse(form.request,'flash/mypage',kwargs={'pk':form.request.user.pk})
        # except Exception as e:
        #     print(e)

        # try:
        #     len(form.request.POST['public'])
        #     movie = Movie.objects.get(id=int(form.request.POST['public']))
        #     movie.public = False
        #     movie.save()

        #     return reverse(form.request,'flash/mypage',kwargs={'pk':form.request.user.pk})
        # except Exception as e:
        #     print(e)
        #     return super().form_valid(form)