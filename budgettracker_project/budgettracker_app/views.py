from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
from django.shortcuts import render, redirect
from django.views import View
from budgettracker_app.models import User, Expense, Category, Note, Archive
from django.contrib.auth import authenticate, login, logout


class Main(View):
    def get(self, request):
        ctx_main = {}
        if request.user.is_authenticated:
            exp_with_dl = Expense.objects.filter(user=request.user.id, deadline__isnull=False).order_by('deadline')
            exp_without_dl = Expense.objects.filter(user=request.user.id, deadline__isnull=True).order_by('create')
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
            exp_without_dl = Expense.objects.filter(user=request.user.id, deadline__isnull=True).order_by('create')
            categories = Category.objects.filter(user=request.user.id).order_by('name')
            notes = Note.objects.filter(user=request.user.id)
            ctx_main['exp_with_dl'] = exp_with_dl
            ctx_main['exp_without_dl'] = exp_without_dl
            ctx_main['categories'] = categories
            ctx_main['notes'] = notes
            if 'all_archive' in request.POST:
                user = request.user
                expenses = Expense.objects.filter(user=user, is_paid=True).order_by('paid_date')
                for expense in expenses:
                    archive = Archive()
                    archive.name = expense.name
                    archive.value = expense.value
                    archive.category = expense.category.name
                    archive.paid = expense.paid_date
                    archive.user = user
                    archive.save()
                    expense.delete()
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
                    if Category.objects.filter(user=request.user, name=cat_name).count() >= 1:
                        cat_exists = f"Kategoria {cat_name} ju?? istnieje. Podaj inn?? kategori??. "
                        ctx_main['cat_exists'] = cat_exists
                        return render(request, 'main.html', context=ctx_main)
                except:
                    pass
                if len(cat_empty) > 0:
                    cat_empty_field = "Pole nie mo??e pozosta?? puste."
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
                main_info = f'Kategoria "{new_category.name}" zosta??a dodana.'
                ctx_main['cat_name'] = ""
                ctx_main['cat_description'] = ""
                ctx_main['main_info'] = main_info
            if 'del_category' in request.POST:
                cat_name = request.POST.get('del_cat')
                if cat_name == "Og??lne":
                    cannot_delete = 'Kategorii "Og??lne" nie mo??na usun????.'
                    ctx_main['cannot_delete'] = cannot_delete
                    return render(request, 'main.html', context=ctx_main)
                cat_overall = Category.objects.get(user=request.user.id, name='Og??lne')
                category = Category.objects.get(user=request.user.id, name=cat_name)
                expenses = Expense.objects.filter(user=request.user.id, category=category.id)
                for expense in expenses:
                    expense.category = cat_overall
                    expense.save()
                main_info = f'Kategoria "{cat_name}" zosta??a usuni??ta.'
                category.delete()
                ctx_main['main_info'] = main_info
            if 'new_expense' in request.POST:
                expense_name = request.POST.get('exp_name')
                expense_value = request.POST.get('exp_value')
                expense_category = request.POST.get('category')
                ctx_main['expense_name'] = expense_name
                ctx_main['expense_value'] = expense_value
                ctx_main['expense_category'] = expense_category
                exp_empty = []
                if expense_name == "":
                    exp_empty.append('expense_name')
                if expense_value == "":
                    exp_empty.append('expense_value')
                if len(exp_empty) > 0:
                    exp_empty_field = "Pole nie mo??e pozosta?? puste."
                    ctx_main['exp_empty_field'] = exp_empty_field
                    ctx_main['exp_empty'] = exp_empty
                    return render(request, 'main.html', context=ctx_main)
                expense_deadline = request.POST.get('exp_deadline')
                ctx_main['expense_deadline'] = expense_deadline
                expense_continuity = request.POST.get('continuity')
                if expense_continuity == 'true' and expense_deadline != "":
                    exp_continuity = True
                    expense_days = request.POST.get('days_amount')
                    expense_weeks = request.POST.get('weeks_amount')
                    expense_months = request.POST.get('months_amount')
                    expense_amount = request.POST.get('continuity_amount')
                    ctx_main['expense_days'] = expense_days
                    ctx_main['expense_weeks'] = expense_weeks
                    ctx_main['expense_months'] = expense_months
                    ctx_main['expense_amount'] = expense_amount
                    if expense_days != "" and expense_weeks == "" and expense_months == "":
                        next_expense = datetime.strptime(expense_deadline, '%Y-%m-%d')+timedelta(days=int(expense_days))
                        period = f'{expense_days}_days'
                    elif expense_weeks != "" and expense_days == "" and expense_months == "":
                        next_expense = datetime.strptime(expense_deadline, '%Y-%m-%d')+timedelta(weeks=int(expense_weeks))
                        period = f'{expense_weeks}_weeks'
                    elif expense_months != "" and expense_days == "" and expense_weeks == "":
                        next_expense = datetime.strptime(expense_deadline, '%Y-%m-%d')+relativedelta(months=int(expense_months))
                        period = f'{expense_months}_months'
                    elif expense_months == "" and expense_days == "" and expense_weeks == "":
                        expense_info = "Musisz wybra?? okres cz??stotliwo??ci wyst??powania p??atno??ci."
                        ctx_main['expense_info'] = expense_info
                        return render(request, 'main.html', context=ctx_main)
                    else:
                        expense_info = "Wype??niono wi??cej ni?? jedno pole dotycz??ce cz??stotliwo??ci p??atno??ci lub wpisana warto???? nie jest liczb?? ca??kowit??."
                        ctx_main['expense_info'] = expense_info
                        return render(request, 'main.html', context=ctx_main)
                    if expense_amount == 'continuity_amount_period':
                        exp_amount = 1000
                    else:
                        exp_amount = request.POST.get('continuity_number')
                        if exp_amount == "":
                            expense_info = "Warto???? ilo??ci cykli p??atno??ci jest nieprawidlowa lub pusta."
                            ctx_main['expense_info'] = expense_info
                            return render(request, 'main.html', context=ctx_main)
                elif expense_continuity == 'true' and expense_deadline == "":
                    expense_info = "Przy p??atno??ciach cyklicznych nale??y poda?? termin p??atno??ci"
                    ctx_main['expense_info'] = expense_info
                    return render(request, 'main.html', context=ctx_main)
                expense_ispaid = request.POST.get('is_paid')
                if expense_ispaid == 'true':
                    ispaid = True
                else:
                    ispaid = False
                expense = Expense()
                expense.name = expense_name
                expense.value = expense_value
                expense.create = date.today()
                if expense_deadline != "":
                    expense.deadline = expense_deadline
                if expense_continuity == 'true':
                    #expense.deadline = expense_deadline
                    expense.continuity = exp_continuity
                    expense.exp_amount = exp_amount
                    expense.period_delta = period
                    expense.next_exp = next_expense
                expense.is_paid = ispaid
                if expense.is_paid == True:
                    expense.paid_date = date.today()
                expense.user = request.user
                expense.category = Category.objects.get(user=request.user, name=expense_category) #Po id a nie name
                expense.save()
                ctx_main['expense_name'] = ""
                ctx_main['expense_value'] = ""
                ctx_main['expense_deadline'] = ""
                ctx_main['expense_days'] = ""
                ctx_main['expense_weeks'] = ""
                ctx_main['expense_months'] = ""
                ctx_main['expense_amount'] = ""

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
            log_empty_field = "Pole nie mo??e pozosta?? puste."
            log_errors['log_empty'] = log_empty
            log_errors['log_empty_field'] = log_empty_field
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            user_not_exists = f"U??ytkownik lub has??o jest niepoprawne !"
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
            empty_field = "Pole nie mo??e pozosta?? puste. "
            ctx_reg['error_list'] = error_list
            ctx_reg['empty_field'] = empty_field
        try:
            if User.objects.get(username=username):
                user_exists = f"U??ytkownik {username} ju?? istnieje. Podaj inny login. "
                ctx_reg['user_exists'] = user_exists
        except:
            pass
        if password1 != password2:
            diff_pass = "Podane has??a r????ni?? si?? od siebie. Wpisz te same has??a. "
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
        cat.name = "Og??lne"
        cat.description = "Og??lne wydatki"
        cat.user = user
        cat.save()
        user_success = f"U??ytkownik {username} zosta?? utworzony pomy??lnie. Teraz mo??esz si?? zalogowa?? do swojego konta."
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
            expense.paid_date = datetime.today()
            if expense.continuity == True:
                expense.exp_amount -= 1
            expense.save()
            if expense.continuity == True and expense.exp_amount > 0:
                next_exp = Expense()
                next_exp.name = expense.name
                next_exp.value = expense.value
                next_exp.create = date.today()
                next_exp.deadline = expense.next_exp
                next_exp.continuity = expense.continuity
                next_exp.exp_amount = expense.exp_amount
                next_exp.period_delta = expense.period_delta
                number1 = expense.period_delta.find('_')
                number2 = int(expense.period_delta[:number1])
                period = expense.period_delta[-(len(expense.period_delta)-number1-1):]
                if period == 'days':
                    next_exp.next_exp = expense.next_exp + relativedelta(days=number2)
                elif period == 'weeks':
                    next_exp.next_exp = expense.next_exp + relativedelta(weeks=number2)
                elif period == 'months':
                    next_exp.next_exp = expense.next_exp + relativedelta(months=number2)
                next_exp.is_paid = False
                next_exp.user = request.user
                next_exp.category = expense.category
                next_exp.save()
            return redirect('main')
        if 'archive' in request.POST:
            user = request.user
            expense = Expense.objects.get(id=expid)
            archive = Archive()
            archive.name = expense.name
            archive.value = expense.value
            archive.category = expense.category.name
            archive.paid = expense.paid_date
            archive.user = user
            archive.save()
            expense.delete()
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
            expense.new_note = note_text
            expense.save()
            note = Note()
            note.text = note_text
            note.mod_date = datetime.now()
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
                pass_info = 'Has??o nie uleg??o zmianie, poniewa?? obydwa pola pozosta??y puste.'
                return render(request, 'account.html', context={'user': user, 'pass_info': pass_info})
            if new_pass1 != new_pass2:
                pass_info = 'Obydwa wpisane has??a musz?? by?? takie same.'
                return render(request, 'account.html', context={'user': user, 'pass_info': pass_info})
            user.set_password(new_pass1)
            user.save()
            pass_info = 'Has??o zostalo zmienione pomy??lnie.'
            return render(request, "account.html", context={'user': user, 'pass_info': pass_info})
        if "delete_account" in request.POST:
            user = User.objects.get(username=request.user.username)
            logout(request)
            user.delete()
            user_success = 'Konto zosta??o pomy??lnie usuni??te.'
            return render(request, 'main.html', context={'user_success': user_success})


class Arch(View):
    def get(self, request):
        user = request.user
        archive = Archive.objects.filter(user=user).order_by('-paid')
        return render(request, 'archive.html', context={'user': user, 'archive': archive})
