from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def login(request):
    if "userid" not in request.session:
        request.session["userid"] = 0
    context = {
        "users": User.objects.all()
    }
    return render(request, "login.html", context)

def login_process(request):
    user = User.objects.filter(email = request.POST["login_email"])
    if user:
        user = User.objects.get(email = request.POST["login_email"])
        if bcrypt.checkpw(request.POST["login_password"].encode(), user.password_hash.encode()):
            request.session["userid"] = user.id
            return redirect("/home")
        else:
            messages.error(request, "Password is incorrect")
            return redirect("/")
    else:
        messages.error(request, "Email does not exist")
        return redirect("/")

def register_process(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for i, values in errors.items():
            messages.error(request, values)
        return redirect("/")
    name = request.POST["register_name"]
    username = request.POST["register_username"]
    email = request.POST["register_email"]
    password = request.POST["register_password"]
    passhash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user = User.objects.create(name = name, username = username, email = email, password_hash = passhash, number_reviews = 0)
    request.session["userid"] = user.id
    return redirect("/home")

def logout_process(request):
    if "userid" not in request.session:
        request.session["userid"] = 0
    if request.session["userid"] == 0:
        messages.error(request, "Not logged in!")
        return redirect("/")
        
    
    request.session["userid"] = 0

    # request.session.clear()
    return redirect("/")

def home(request):
    if "userid" not in request.session:
        request.session["userid"] = 0
    if request.session["userid"] == 0:
    # if "userid" not in request.session:
        messages.error(request, "Not logged in!")
        return redirect("/")

    user = User.objects.get(id = request.session["userid"])

    context = {
        "name": user.name,
        "namel": user.username,
        "id": user.id,
        "quotes": Quote.objects.all(),
        "user_id": request.session["userid"],
    }
    return render(request, "home.html", context)

# Above are login/user management


def add_quote_process(request):
    if "userid" not in request.session:
        request.session["userid"] = 0
    if request.session["userid"] == 0:
    # if "userid" not in request.session:
        messages.error(request, "Not logged in!")
        return redirect("/")

    errors = Quote.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for i, values in errors.items():
            messages.error(request, values)
        return redirect("/home")
    user = User.objects.get(id = request.session["userid"])
    quote = request.POST["quote"]
    author = request.POST["quote_author"]
    Quote.objects.create(author = author, quote = quote, user = user)
    return redirect("/home")

def user(request, id):
    if "userid" not in request.session:
        request.session["userid"] = 0
    if request.session["userid"] == 0:
    # if "userid" not in request.session:
        messages.error(request, "Not logged in!")
        return redirect("/")
    try:
        user = User.objects.get(id = id)
    except:
        messages.error(request, "User does not exist")
        return redirect("/home")

    context = {
        "name": user.name,
        "namel": user.username,
        "quotes": user.user_quotes.all()
    }
    return render(request, "user.html", context)

def edit(request, id):
    if "userid" not in request.session:
        request.session["userid"] = 0
    if request.session["userid"] == 0:
    # if "userid" not in request.session:
        messages.error(request, "Not logged in!")
        return redirect("/")

    try:
        user = User.objects.get(id = id)
    except:
        messages.error(request, "User does not exist")
        return redirect("/home")

    context = {
        "first_name": user.name,
        "last_name": user.username,
        "email": user.email
    }
        
    return render(request, "edit.html", context)

def edit_process(request):
    if "userid" not in request.session:
        request.session["userid"] = 0
    if request.session["userid"] == 0:
    # if "userid" not in request.session:
        messages.error(request, "Not logged in!")
        return redirect("/home")

    errors = User.objects.edit_validator(request.POST, request.session["userid"])
    if len(errors) > 0:
        for i, values in errors.items():
            messages.error(request, values)
        return redirect("/home")

    user = User.objects.get(id= request.session["userid"])
    name = request.POST["register_name"]
    username = request.POST["register_username"]
    email = request.POST["register_email"]
    user.name = name
    user.username = username
    user.email = email
    user.save()
    return redirect("/home")

def process_like(request, id):
    if "userid" not in request.session:
        request.session["userid"] = 0
    if request.session["userid"] == 0:
    # if "userid" not in request.session:
        messages.error(request, "Not logged in!")
        return redirect("/home")

    user = User.objects.get(id = request.session["userid"])
    quote = Quote.objects.get(id = id)

    try:
        check = quote.quote_likes.get(user = user)
        messages.error(request, "You aready liked this!")
        return redirect("/home")

    except:
        Like.objects.create(user = user, quote = quote)

    return redirect("/home")

def delete_process(request, id):
    if "userid" not in request.session:
        request.session["userid"] = 0
    if request.session["userid"] == 0:
    # if "userid" not in request.session:
        messages.error(request, "Not logged in!")
        return redirect("/home")

    try:
        temp = Quote.objects.get(id = id)
    except:
        messages.error(request, "Quote does not exist")
        return redirect("/home")

    if not request.session["userid"] == temp.user.id:
        messages.error(request, "That ain't you!")
        return redirect("/home")

    temp.delete()
    return redirect("/home")