from django.shortcuts import render
from django.views import View
from datetime import date, datetime


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
            info = f"Użytkownik {login} nie istnieje !"
            return render(request, "login.html", context={'info': info})
        if user.password == password:
            request.session['logged_user'] = user.id
            info = f"Witaj {user.first_name} {user.last_name} !"
            user.last_log = datetime.now()
            user.save()
            return render(request, "main.html", context={'info': info})
        else:
            info = "Wpisane hasło jest niepoprawne !"
            return render(request, "login.html", context={'info': info})

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
        account_created = date()