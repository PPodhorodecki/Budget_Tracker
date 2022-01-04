from django.shortcuts import render
from django.views import View
from datetime import date, datetime
from budgettracker_app.models import User


class Main(View):
    def get(self, request):
        return render(request, "main.html")


class LogUser(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        login = request.POST.get("login")
        password = request.POST.get("password")
        try:
            user = User.objects.get(login=login)
        except NameError:
            user_not_exists = f"Użytkownik {login} nie istnieje !"
            return render(request, "login.html", context={'user_not_exists': user_not_exists})
        if user.password == password:
            request.session['logged_user'] = user.id
            welcome_text = f"Witaj {user.first_name} !"
            user.last_log = datetime.now()
            user.save()
            return render(request, "main.html", context={'welcome_text': welcome_text})
        else:
            wrong_pass = "Wpisane hasło jest niepoprawne !"
            return render(request, "login.html", context={'wrong_pass': wrong_pass})


class LogoutUser(View):
    def get(self, request):
        del request.session['logged_user']
        logout_user = "Użytkownik został bezpiecznie wylogowany"
        return render(request, 'main.html', context={'logout_user': logout_user})


class RegisterUser(View):
    def get(self, request):
        return render(request, "register.html")

    def post(self, request):
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        login = request.POST.get("login")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        error_list = []
        ctx = {'first_name': first_name, 'last_name': last_name, 'email': email, 'login': login, 'password1': password1, 'password2': password2}
        if first_name == "":
            error_list.append('first_name')
        if last_name == "":
            error_list.append('last_name')
        if email == "":
            error_list.append('email')
        if login == "":
            error_list.append('login')
        if password1 == "":
            error_list.append('password1')
        if password2 == "":
            error_list.append('password2')
        if len(error_list) > 0:
            empty_field = "Pole nie może pozostać puste. "
            ctx['error_list'] = error_list
            ctx['empty_field'] = empty_field
        try:
            if User.objects.get(login=login):
                user_exists = f"Użytkownik {login} już istnieje. Podaj inny login. "
                ctx['user_exists'] = user_exists
        except:
            pass
        if password1 != password2:
            diff_pass = "Podane hasła różnią się od siebie. Wpisz te same hasła. "
            ctx['diff_pass'] = diff_pass
        if len(ctx) > 6:
            return render(request, 'register.html', context=ctx)
        user = User()
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.login = login
        user.password = password1
        user.save()
        user_success = f"Użytkownik {login} został utworzony pomyślnie. Teraz możesz się zalogować do swojego konta."
        return render(request, "main.html", context={'user_success': user_success})