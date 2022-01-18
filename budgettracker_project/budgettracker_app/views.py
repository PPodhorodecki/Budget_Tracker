from datetime import date
from dateutil.relativedelta import relativedelta
from django.shortcuts import render, redirect
from django.views import View
from budgettracker_app.models import User, Expense, Category, Note
from django.contrib.auth import authenticate, login, logout


class Main(View):
    def get(self, request):
        ctx_main = {}
        if request.user.is_authenticated:
            exp_with_dl = Expense.objects.filter(user=request.user.id, deadline__isnull=False).order_by('deadline')
            exp_without_dl = Expense.objects.filter(user=request.user.id, deadline__isnull=True).order_by('exp_create')
            categories = Category.objects.filter(user=request.user.id).order_by('name')
            notes = Note.objects.filter(user=request.user.id)
            ctx_main['exp_with_dl'] = exp_with_dl
            ctx_main['exp_without_dl'] = exp_without_dl
            ctx_main['categories'] = categories
            ctx_main['notes'] = notes
        return render(request, "main.html", context=ctx_main)

    def post(self, request):
        if request.user.is_authenticated:
            ctx_main = {}
            exp_with_dl = Expense.objects.filter(user=request.user.id, deadline__isnull=False).order_by('deadline')
            exp_without_dl = Expense.objects.filter(user=request.user.id, deadline__isnull=True).order_by('exp_create')
            categories = Category.objects.filter(user=request.user.id).order_by('name')
            notes = Note.objects.filter(user=request.user.id)
            ctx_main['exp_with_dl'] = exp_with_dl
            ctx_main['exp_without_dl'] = exp_without_dl
            ctx_main['categories'] = categories
            ctx_main['notes'] = notes
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
                main_info = f'Kategoria "{new_category.name}" została dodana.'
                ctx_main['cat_name'] = ""
                ctx_main['cat_description'] = ""
                ctx_main['main_info'] = main_info
            if 'del_category' in request.POST:
                cat_name = request.POST.get('del_cat')
                if cat_name == "Ogólne":
                    cannot_delete = 'Kategorii "Ogólne" nie można usunąć.'
                    ctx_main['cannot_delete'] = cannot_delete
                    return render(request, 'main.html', context=ctx_main)
                cat_overall = Category.objects.get(user=request.user.id, name='Ogólne')
                category = Category.objects.get(user=request.user.id, name=cat_name)
                expenses = Expense.objects.filter(user=request.user.id, category=category.id)
                for expense in expenses:
                    expense.category = cat_overall
                    expense.save()
                main_info = f'Kategoria "{cat_name}" została usunięta.'
                category.delete()
                ctx_main['main_info'] = main_info
            if 'new_expense' in request.POST:
                expense_name = request.POST.get('exp_name')
                expense_value = request.POST.get('exp_value')
                expense_category = request.POST.get('category')
                if expense_name == "" or expense_value == "" or expense_category == "":
                    expense_info = "Nie wszystkie wymagane pola zostały uzupełnione."
                    ctx_main['expense_info'] = expense_info
                    return render(request, 'main.html', context=ctx_main)
                expense_deadline = request.POST.get('exp_deadline')
                expense_continuity = request.POST.get('continuity')
                expense_create = date.today()
                ctx_main['expense_name'] = expense_name
                ctx_main['expense_value'] = expense_value
                ctx_main['expense_deadline'] = expense_deadline
                if expense_continuity == 'yes':
                    expense_days = request.POST.get('days_amount')
                    expense_weeks = request.POST.get('weeks_amount')
                    expense_months = request.POST.get('months_amount')
                    expense_amount = request.POST.get('continuity_amount')
                    if expense_days != "" and expense_weeks == "" and expense_months == "":
                        next_expense = expense_deadline + relativedelta(days=+expense_days)
                        period = f'{expense_days}_days'
                    elif expense_weeks != "" and expense_days == "" and expense_months == "":
                        next_expense = expense_deadline + relativedelta(weeks=+expense_weeks)
                        period = f'{expense_weeks}_weeks'
                    elif expense_months != "" and expense_days == "" and expense_weeks == "":
                        next_expense = expense_deadline + relativedelta(months=+expense_months)
                        period = f'{expense_months}_months'
                    else:
                        expense_info = "Tylko jedno pole częstotliwości płatności może zostać uzupełnione. Reszta musi pozostać pusta."
                        ctx_main['expense_info'] = expense_info
                        return render(request, 'main.html', context=ctx_main)
                    if expense_amount == 'continuity_amount_period':
                        exp_amount = 1000
                    else:
                        exp_amount = request.POST.get('continuity_number')


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
        notes = Note.objects.filter(user=request.user, expense=Expense.objects.get(id=expid)).order_by('mod_date')
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
            expense.category = Category.objects.get(user=request.user.id, name=request.POST.get('category'))
            expense.save()
            return redirect('main')
        if 'add_note' in request.POST:
            note_text = request.POST.get('note')
            expense = Expense.objects.get(id=expid)
            note = Note()
            note.text = note_text
            note.mod_date = datetime.datetime.now()
            note.user = request.user
            note.expense = expense
            note.save()
            return redirect('main')


class Account(View):
    def get(self, request):
        user = request.user
        return render(request, 'account.html', context={'user': user})

    def post(self, request):
        user = request.user
        if "change_data" in request.POST:
            user = request.user
            new_first_name = request.POST.get('first_name')
            new_last_name = request.POST.get('last_name')
            new_email = request.POST.get('email')
            if new_first_name == "" or new_first_name == "-":
                pass
            else:
                user.first_name = new_first_name
            if new_last_name == "" or new_last_name == "-":
                pass
            else:
                user.last_name = new_last_name
            if new_email == "" or new_email == "-":
                pass
            else:
                user.email = new_email
            user.save()
            return render(request, "account.html", context={'user': user})
        if "change_pass" in request.POST:
            new_pass1 = request.POST.get('password1')
            new_pass2 = request.POST.get('password2')
            if new_pass1 =="" and new_pass2 == "":
                pass_info = 'Hasło nie uległo zmianie, ponieważ obydwa pola pozostały puste.'
                return render(request, 'account.html', context={'user': user, 'pass_info': pass_info})
            if new_pass1 != new_pass2:
                pass_info = 'Obydwa wpisane hasła muszą być takie same.'
                return render(request, 'account.html', context={'user': user, 'pass_info': pass_info})
            user.set_password(new_pass1)
            user.save()
            pass_info = 'Hasło zostalo zmienione pomyślnie.'
            return render(request, "account.html", context={'user': user, 'pass_info': pass_info})
        if "delete_account" in request.POST:
            user = User.objects.get(username=request.user.username)
            logout(request)
            user.delete()
            user_success = 'Konto zostało pomyślnie usunięte.'
            return render(request, 'main.html', context={'user_success': user_success})