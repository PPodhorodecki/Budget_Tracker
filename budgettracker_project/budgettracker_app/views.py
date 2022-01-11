from django.shortcuts import render, redirect
from django.views import View
from budgettracker_app.models import User, Expense, Category, Note
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

    def post(self, request):
        if request.user.is_authenticated:
            ctx_main = {}
            expenses_cont = Expense.objects.filter(user=request.user.id, continuity=True)
            expenses_uncont = Expense.objects.filter(user=request.user.id, continuity=False)
            categories = Category.objects.filter(user=request.user.id).order_by('name')
            ctx_main['expenses_cont'] = expenses_cont
            ctx_main['expenses_uncont'] = expenses_uncont
            ctx_main['categories'] = categories
            if 'new_category' in request.POST:
                cat_name = request.POST.get('cat_name')
                cat_description = request.POST.get('cat_description')
                cat_user = request.user
                cat_empty = []
                if cat_name == "":
                    cat_empty.append('category_name')
                if cat_description == "":
                    cat_empty.append('category_description')
                try:
                    if Category.objects.filter(name=cat_name).count() >= 1:
                        cat_exists = f"Kategoria {cat_name} już istnieje. Podaj inną kategorię. "
                        ctx_main['cat_exists'] = cat_exists
                except:
                    pass
                if len(cat_empty) > 0:
                    cat_empty_field = "Pole nie może pozostać puste."
                    ctx_main['cat_empty'] = cat_empty
                    ctx_main['cat_empty_field'] = cat_empty_field
                    ctx_main['cat_name'] = cat_name
                    ctx_main['cat_description'] = cat_description
                    return render(request, 'main.html', context=ctx_main)
                new_category = Category()
                new_category.name = cat_name
                new_category.description = cat_description
                new_category.user = cat_user
                new_category.save()
                ctx_main['cat_name'] = ""
                ctx_main['cat_description'] = ""
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
        cat.name = "Ogólne"
        cat.description = "Ogólne wydatki"
        cat.user = user
        cat.save()
        user_success = f"Użytkownik {username} został utworzony pomyślnie. Teraz możesz się zalogować do swojego konta."
        return render(request, "main.html", context={'user_success': user_success})


class Details(View):
    def get(self, request, expid):
        expense = Expense.objects.get(id=expid)
        categories = Category.objects.filter(user=request.user.id).exclude(name=expense.category.name).order_by('name')
        notes = Note.objects.filter(expense=Expense.objects.get(id=expid)).order_by('mod_date')
        return render(request, 'details.html', context={'expense': expense, 'categories': categories, 'notes': notes})

    def post(self, request, expid):
        if 'paid' in request.POST:
            expense = Expense.objects.get(id=expid)
            expense.is_paid = True
            expense.save()
            return redirect('main')
        if 'delete' in request.POST:
            expense = Expense.objects.get(id=expid)
            expense.delete()
            return redirect('main')
        if 'change_cat' in request.POST:
            expense = Expense.objects.get(id=expid)
            expense.category = Category.objects.get(name=request.POST.get('category'))
            expense.save()
            return redirect('main')
