from django.shortcuts import render, redirect
from django.views import View
from budgettracker_app.models import User, Expense, Category
from django.contrib.auth import authenticate, login, logout


class Main(View):
    def get(self, request):
        ctx_main = {}
        if request.user.is_authenticated:
            expenses_cont = Expense.objects.filter(user=request.user.id, continuity=True)
            expenses_uncont = Expense.objects.filter(user=request.user.id, continuity=False)
            categories = Category.objects.filter(user=request.user.id).order_by('name')
            ctx_main['expenses_cont'] = expenses_cont
            ctx_main['expenses_uncont'] = expenses_uncont
            ctx_main['categories'] = categories
        return render(request, "main.html", context=ctx_main)


class LogUser(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        log_errors = {'username': username}
        log_empty = []
        if username == "":
            log_empty.append('username')
        if password == "":
            log_empty.append('password')
        if len(log_empty) > 0:
            log_empty_field = "Pole nie może pozostać puste."
            log_errors['log_empty'] = log_empty
            log_errors['log_empty_field'] = log_empty_field
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            user_not_exists = f"Użytkownik lub hasło jest niepoprawne !"
            log_errors['user_not_exists'] = user_not_exists
        if len(log_errors) > 1:
            return render(request, 'login.html', context=log_errors)
        return redirect('main')


class LogoutUser(View):
    def get(self, request):
        logout(request)
        #logout_user = "Użytkownik został bezpiecznie wylogowany"
        #return render(request, 'main.html', context={'logout_user': logout_user})
        return redirect('main')


class RegisterUser(View):
    def get(self, request):
        return render(request, "register.html")

    def post(self, request):
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        error_list = []
        ctx_reg = {'first_name': first_name, 'last_name': last_name, 'email': email, 'username': username, 'password1': password1, 'password2': password2}
        if first_name == "":
            error_list.append('first_name')
        if last_name == "":
            error_list.append('last_name')
        if email == "":
            error_list.append('email')
        if username == "":
            error_list.append('username')
        if password1 == "":
            error_list.append('password1')
        if password2 == "":
            error_list.append('password2')
        if len(error_list) > 0:
            empty_field = "Pole nie może pozostać puste. "
            ctx_reg['error_list'] = error_list
            ctx_reg['empty_field'] = empty_field
        try:
            if User.objects.get(username=username):
                user_exists = f"Użytkownik {username} już istnieje. Podaj inny login. "
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
        user.username = username
        user.set_password(password1)
        user.save()
        cat = Category()
        cat.name = ""
        cat.description = ""
        cat.user = user
        cat.save()
        user_success = f"Użytkownik {username} został utworzony pomyślnie. Teraz możesz się zalogować do swojego konta."
        return render(request, "main.html", context={'user_success': user_success})