from re import A
from unicodedata import category
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.mail import send_mail
from datetime import datetime, timedelta
from django.http import HttpResponse
from numpy import empty
from .forms import SignUpForm
from .models import Fields, Category, Sub_Category, Link

User = get_user_model()

class homePage(TemplateView):
    def get(self, request, **kwargs):
        search_word = ""
        if request.method == "POST":
            search_word = request.POST["data"]

        #     list1 = []
        #     if search_word != "":
        #         list1 = [{"field":"fuck","category":'you',"subcategory":'shyam'},{"field":"fuck","category":'you',"subcategory":'shyam'},{"field":"fuck","category":'you',"subcategory":'shyam'}]
        #     # book = homePage.objects.create(field='hello', category='hello', subcategory='hello')
        return render(request, "homepage.html")

    def post(self, request, **kwargs):
        search_word = ""
        search_word = request.POST["search1"]
        if search_word == "" or search_word == " ":
            return render(request, "homepage.html")
        context = self.search(search_word)
        if context:
            return render(request, "homepage.html", {"context": context})
        return render(request, "homepage.html")

    def search(self, search_word):
        datasets_sub = Sub_Category.objects.filter(Sub_Name__contains=search_word)
        dataset_category = Category.objects.filter(Category_Name__contains=search_word)
        dataset_field = Fields.objects.filter(Field_Name__contains=search_word)
        context = []

        if dataset_field:
            for f in dataset_field:
                categories = Category.objects.filter(FieldFK=f)
                subs = Sub_Category.objects.filter(CategoryFK__in=categories)
                for d in subs:
                    context.append(
                        {
                            "subcategory": d.Sub_Name,
                            "category": d.CategoryFK.Category_Name,
                            "fields": d.CategoryFK.FieldFK.Field_Name,
                            "links": Link.objects.filter(Sub_CategoryFK=d),
                        }
                    )
            print(context)
            return context

        if dataset_category:
            for d in dataset_category:
                subs = Sub_Category.objects.filter(CategoryFK=d)
                for d in subs:
                    context.append(
                        {
                            "subcategory": d.Sub_Name,
                            "category": d.CategoryFK.Category_Name,
                            "fields": d.CategoryFK.FieldFK.Field_Name,
                            "links": Link.objects.filter(Sub_CategoryFK=d),
                        }
                    )
            print(context)
            return context

        if datasets_sub:
            for d in datasets_sub:
                context.append(
                    {
                        "subcategory": d.Sub_Name,
                        "category": d.CategoryFK.Category_Name,
                        "fields": d.CategoryFK.FieldFK.Field_Name,
                        "links": Link.objects.filter(Sub_CategoryFK=d),
                    }
                )
            print(context)
            return context

        if not dataset_field and not dataset_category and not datasets_sub:
            context = []
            return context    

        # print(datasets)
        # for c in datasets:
        # # print(c.get('Category_FK', None))
        #     print(c.Sub_Name, c.CategoryFK.Category_Name)


class loginView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, "userlogin.html", context=None)

    def post(self, request, **kwargs):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        print(username, password)
        if user is not None:
            login(request, user)
            return redirect(to="/")
        print(user)
        return render(
            request, "userlogin.html", context={"msg": "Incorrect Username/Password"}
        )


class signup(TemplateView):
    def get(self, request, **kwargs):
        return render(request, "usersignup.html", context=None)

    def post(self, request, **kwargs):
        data = request.POST.copy()
        # data['contact'] = data['contact']
        data["password"] = data["password1"]
        data["password2"] = data["password1"]
        data["date_joined"] = datetime.now()
        data["is_active"] = True
        # print(data)
        form = SignUpForm(data)
        if form.is_valid():
            print("yes")
            form.save()
            return redirect(to="/login/")
        print(form.errors)
        return render(request, "usersignup.html", context={"msg": form.errors})


class aboutpage(TemplateView):
    def get(self, request, **kwargs):
        return render(request, "aboutus.html")


class terms(TemplateView):
    def get(self, request, **kwargs):
        return render(request, "terms.html")


class addlink(TemplateView):
    def get(self, request, **kwargs):
        return render(request, "addlink.html")

    def post(self, request, **kwargs):
        subcat = Sub_Category.objects.get(pk=request.POST["subcategory"])
        link = Link.objects.create(
            Data_link=request.POST["link"],
            Count=0,
            link_description=request.POST["description"],
            Sub_CategoryFK=subcat,
        )
        link.save()
        print(link)
        print(Link.objects.filter(link_description=request.POST["description"]))
        return render(request, "addlink.html", {"msg": "Link Added"})

class contactus(TemplateView):
    def get(self, request, **kwargs):
        return render(request, "contactus.html")

    def post(self, request, **kwargs):
        FullName = request.POST["first"]
        user_email =request.POST["email"]
        suggestion = request.POST["suggestion"]

        send_mail(
            'Suggestion from:-' + FullName, # fullname as subject of mail
            suggestion, # suggestion
            user_email, # from
            ['rishishukla507@gmail.com'], # to
        )

        return render(request, "contactus.html")

class LogoutView(TemplateView):
    def get(self, request, **kwargs):
        logout(request)
        return redirect(to="/")
