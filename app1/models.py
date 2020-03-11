from django.db import models
import re


class UserManager(models.Manager):
    def basic_validator(self, data):
        errors = {}
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(data["register_name"]) < 2:
            errors["first_name"] = "Name should be at least 2 characters."
        if len(data["register_username"]) < 2:
            errors["user_name"] = "Username should be at least 2 characters."
        if not email_regex.match(data["register_email"]):
            errors["email"] = "Email must be valid."
        user = User.objects.filter(email = data["register_email"])
        if user:
            errors["email2"] = "Email has already been registered"
        if len(data["register_password"]) < 8:
            errors["password"] = "Password should be at least 8 characters."
        if (data["register_password"] != data["register_confirmation"]):
            errors["password_match"] = "Passwords do not match."
        return errors

    def edit_validator(self,data, id):
        errors = {}
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(data["register_name"]) < 2:
            errors["first_name"] = "Name should be at least 2 characters."
        if len(data["register_username"]) < 2:
            errors["user_name"] = "Username should be at least 2 characters."
        if not email_regex.match(data["register_email"]):
            errors["email"] = "Email must be valid."
        user = User.objects.filter(email = data["register_email"])
        user_email = User.objects.get(id = id)
        if not (data["register_email"] == user_email.email):
            if user:
                errors["email2"] = "Email has already been registered"
        return errors

class QuoteManager(models.Manager):
    def basic_validator(self, data):
        errors = {}
        if len(data["quote_author"]) < 3:
            errors["quote_author"] = "Author name should be at least 3 characters."
        if len(data["quote"]) < 10:
            errors["quote"] = "Quote should be at least 10 characters."
        return errors

class User(models.Model):
    name = models.CharField(max_length = 255)
    username = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password_hash = models.CharField(max_length = 255)
    number_reviews = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    #user_quotes
    #user_likes

class Quote(models.Model):
    author = models.CharField(max_length = 255)
    quote = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()
    user = models.ForeignKey(User, related_name = "user_quotes", on_delete = models.CASCADE)
    #quote_likes

class Like(models.Model):
    user = models.ForeignKey(User, related_name = "user_likes", on_delete = models.CASCADE)
    quote = models.ForeignKey(Quote, related_name = "quote_likes", on_delete = models.CASCADE)