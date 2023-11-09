from typing import Any
from django.views import generic
from .forms import LoginForm,SignupForm,UserUpdateForm,MyPasswordChangeForm
from django.contrib.auth.views import LoginView,LogoutView,PasswordChangeView,PasswordChangeDoneView
from django.shortcuts import redirect,resolve_url
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy

# Create your views here.
User = get_user_model()


#--------------------------------------------------------------------------
#ログイン画面---------------------------------------------------------------
class Login(LoginView):
    form_class = LoginForm
    template_name = "accounts/login.html"



#--------------------------------------------------------------------------
#ログアウト完了画面----------------------------------------------------------
class Logout(LogoutView):
    template_name = "accounts/logout_done.html"



#--------------------------------------------------------------------------
#サインアップ画面-----------------------------------------------------------
class Signup(generic.CreateView):
    template_name = "accounts/user_form.html"
    form_class =SignupForm

    def form_valid(self, form):
        user = form.save() # formの情報を保存
        return redirect("accounts:signup_done")

    # データ送信
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["process_name"] = "サインアップ"
        return context



#--------------------------------------------------------------------------
#サインアップ完了画面--------------------------------------------------------
class SignupDone(generic.TemplateView):
    template_name = "accounts/signup_done.html"


#--------------------------------------------------------------------------
#マイページ画面--------------------------------------------------------
class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        # 今ログインしてるユーザーのpkと、そのマイページのpkが同じなら許可
        user = self.request.user
        return user.pk == self.kwargs["pk"]


class MyPage(OnlyYouMixin, generic.DetailView):
    model = User
    template_name = "accounts/my_page.html"
    # モデル名小文字(user)でモデルインスタンスがテンプレートファイルに渡される


#--------------------------------------------------------------------------
#ユーザー更新--------------------------------------------------------
class UserUpdate(OnlyYouMixin, generic.UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "accounts/user_form.html"

    def get_success_url(self):
        return resolve_url("accounts:my_page", pk=self.kwargs["pk"])

    # contextデータ作成
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["process_name"] = "ユーザ情報更新"
        return context
    


#--------------------------------------------------------------------------
#パスワード変更--------------------------------------------------------
class PasswordChange(PasswordChangeView):
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy("accounts:password_change_done")
    template_name = "accounts/user_form.html"

    # contextデータ作成
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["process_name"] = "パスワード変更"
        return context


#--------------------------------------------------------------------------
#パスワード変更完了--------------------------------------------------------
class PasswordChangeDone(PasswordChangeDoneView):
    template_name = "accounts/password_change_done.html"


 
