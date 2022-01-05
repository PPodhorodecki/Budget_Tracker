from django.shortcuts import render
from django.views import View
from datetime import date, datetime
from budgettracker_app.models import User, Session


class Main(View):
    def get(self, request):
        ctx_main = {}
        session_check = Session.objects.all()
        if session_check.count() == 1:
            auth = 1
            ctx_main['auth'] = auth
            #logoutuser = '<a href="/logout">Wyloguj</a>'
            #ctx_main['logoutuser'] = logoutuser
        elif session_check.count() == 0:
            auth = 0
            ctx_main['auth'] = auth
            #loguser = '<a href="/login">Zaloguj się</a>'
            #reguser = '<a href="/register">Zarejestruj się</a>'
            #ctx_main['loguser'] = loguser
            #ctx_main['reguser'] = reguser
        return render(request, "main.html", context=ctx_main)


class LogUser(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        login = request.POST.get("login")
        password = request.POST.get("password")
        log_errors = {'login': login}
        log_empty = []
        if login == "":
            log_empty.append('login')
        if password == "":
            log_empty.append('password')
        if len(log_empty) > 0:
            log_empty_field = "Pole nie może pozostać puste."
            log_errors['log_empty'] = log_empty
            log_errors['log_empty_field'] = log_empty_field
        try:
            user = User.objects.get(login=login)
            if user.password != password:
                wrong_pass = "Wpisane hasło jest niepoprawne !"
                log_errors['wrong_pass'] = wrong_pass
        except:
            user_not_exists = f"Użytkownik {login} nie istnieje !"
            log_errors['user_not_exists'] = user_not_exists

        if len(log_errors) > 1:
            return render(request, 'login.html', context=log_errors)
        if user.password == password:
            request.session['logged_user'] = user.id
            session_open = Session()
            session_open.session_name = user.id
            session_open.save()
            welcome_text = f"Witaj {user.first_name} !"
            #user.last_log = datetime.now()
            #user.save()
            return render(request, "main.html", context={'welcome_text': welcome_text})



class LogoutUser(View):
    def get(self, request):
        session_close = Session.objects.get(session_name=request.session['logged_user'])
        session_close.delete()
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
        ctx_reg = {'first_name': first_name, 'last_name': last_name, 'email': email, 'login': login, 'password1': password1, 'password2': password2}
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
            ctx_reg['error_list'] = error_list
            ctx_reg['empty_field'] = empty_field
        try:
            if User.objects.get(login=login):
                user_exists = f"Użytkownik {login} już istnieje. Podaj inny login. "
                ctx_reg['user_exists'] = user_exists
        except:
            pass
        if password1 != password2:
            diff_pass = "Podane hasła różnią się od siebie. Wpisz te same hasła. "
            ctx_reg['diff_pass'] = diff_pass
        if len(ctx_reg) > 6:
            return render(request, 'register.html', context=ctx_reg)
        user = User()
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.login = login
        user.password = password1
        user.save()
        user_success = f"Użytkownik {login} został utworzony pomyślnie. Teraz możesz się zalogować do swojego konta."
        return render(request, "main.html", context={'user_success': user_success})