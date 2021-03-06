from django.shortcuts import render
import urllib.request
from urllib.error import HTTPError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import LoginForm, BookForm, UserForm
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import redirect

def user_logged_in(request):
    auth = request.COOKIES.get('auth')
    post_data = {'authenticator': auth}
    post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
    req = urllib.request.Request('http://exp-api:8000/api/v1/check_authenticator', data=post_encoded, method='POST')

    try:
        response = urllib.request.urlopen(req)
    except Exception as e:
        return False
    return True

def get_user_object(request):
    auth = request.COOKIES.get('auth')
    post_data = {'authenticator': auth}
    post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
    req = urllib.request.Request('http://exp-api:8000/api/v1/check_authenticator', data=post_encoded, method='POST')

    try:
        response = urllib.request.urlopen(req).read().decode('utf-8')
    except Exception as e:
        return {}
    response_dict = json.loads(response)
    user_dict = {}
    user_dict['id'] = response_dict['user_id']
    return user_dict

def login_required(f):
    def wrap(request, *args, **kwargs):
        if user_logged_in(request):
            return f(request, *args, **kwargs)
        else:
            return HttpResponseRedirect("login")

    return wrap

def home(request):
    auth = user_logged_in(request)

    req = urllib.request.Request('http://exp-api:8000/api/v1/home')
    try:
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    except HTTPError as e:
        return HttpResponse(json.dumps({"error": e.msg}), status=e.code)
    except Exception as e:
        return HttpResponse(json.dumps({"error": str(type(e))}), status=500)

    book_list = json.loads(resp_json)
    return render(request, "home.html", {"book_list":book_list, "auth":auth})

def book_detail(request, book_id):

    auth = user_logged_in(request)



    req = urllib.request.Request('http://exp-api:8000/api/v1/books/' + str(book_id))
    req1 = urllib.request.Request('http://exp-api:8000/api/v1/recommend/' + str(book_id))

    try:
        auth_cookie = request.COOKIES.get('auth')
        req.add_header("Cookie", "auth="+auth_cookie)
        req1.add_header("Cookie", "auth="+auth_cookie)
    except:
        pass

    try:
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    except HTTPError as e:
        return HttpResponse(json.dumps({"error": e.msg}), status=e.code)
    except Exception as e:
        return HttpResponse(json.dumps({"error": str(type(e))}), status=500)

    book = json.loads(resp_json)


    try:
        resp_json1 = urllib.request.urlopen(req1).read().decode('utf-8')
    except HTTPError as e:
        return HttpResponse(json.dumps({"error": e.msg}), status=e.code)
    except Exception as e:
        return HttpResponse(json.dumps({"error": str(type(e))}), status=500)

    recs = json.loads(resp_json1)

    return render(request, "book_detail.html", {"book":book, "auth":auth, "recs":recs})

def login(request):
    if request.method == 'GET':
        auth = user_logged_in(request)
        form = LoginForm()
        context = {"form": form, "auth": auth}
        return render(request, "login.html", context)

    f = LoginForm(request.POST)

    # Check if the form instance is invalid
    if not f.is_valid():
      context = {"form": f, "error": "Form was invalid"}
      return render(request, 'login.html', context)


    username = f.cleaned_data['username']
    password = f.cleaned_data['password']

    post_data = {'username': username, 'password': password}
    post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
    req = urllib.request.Request('http://exp-api:8000/api/v1/login', data=post_encoded, method='POST')

    try:
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    except HTTPError as e:
        context = {"form": f, "error": "HTTP error: " + e.msg}
        return render(request, 'login.html', context)
    except Exception as e:
        return HttpResponse(json.dumps({"error": str(type(e))}), status=500)

    resp_dict = json.loads(resp_json)
    authenticator = resp_dict['authenticator']
    response = HttpResponseRedirect("/")

    response.set_cookie("auth", authenticator)
    return response

@csrf_exempt
@login_required
def create_listing(request):
    auth = user_logged_in(request)
    if request.method == "GET":
        form = BookForm()
        context = {"form": form, "auth": auth}
        return render(request, "create_listing.html", context)
    elif request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            book_info = form.cleaned_data
            book_info["price"] = float(book_info["price"])
            user_object = get_user_object(request)
            book_info["seller"] = user_object["id"]

        else:
            blank_form = BookForm()
            context = {"form": form, "auth": auth, "error": "The form was invalid, please enter valid data"}
            return render(request, "create_listing.html", context)

        post_encoded = urllib.parse.urlencode(book_info).encode('utf-8')
        req = urllib.request.Request('http://exp-api:8000/api/v1/books/create', data=post_encoded, method='POST')
        try:
            resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        except HTTPError as e:
            return HttpResponse(json.dumps({"error": e.msg}), status=e.code)
        except Exception as e:
            return HttpResponse(json.dumps({"error": str(type(e))}), status=500)
        resp_dict = json.loads(resp_json)
        book_id = resp_dict["id"]
        return redirect("book_detail", book_id=book_id)



@login_required
def logout(request):
    auth = request.COOKIES.get('auth')
    post_data = {'authenticator': auth}
    post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
    req = urllib.request.Request('http://exp-api:8000/api/v1/logout', data=post_encoded, method='POST')
    try:
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    except Exception as e:
        return HttpResponse(json.dumps({"error": str(type(e))}), status=500)

    return HttpResponseRedirect("/")

@csrf_exempt
def create_account(request):
    auth = user_logged_in(request)
    if request.method == "GET":
        form = UserForm()
        context = {"form": form, "auth": auth}
        return render(request, "create_account.html", context)
    elif request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user_info = form.cleaned_data
        else:
            context = {"form": form, "auth": auth, "error": "The form was invalid, please enter valid data"}
            return render(request, "create_account.html", context)

        post_encoded = urllib.parse.urlencode(user_info).encode('utf-8')
        req = urllib.request.Request('http://exp-api:8000/api/v1/create_user', data=post_encoded, method='POST')
        try:
            resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        except HTTPError as e:
            return HttpResponse(json.dumps({"error": e.msg}), status=e.code)
        except Exception as e:
            return HttpResponse(json.dumps({"error": str(type(e))}), status=500)
        return redirect("homepage")


def search(request):
    auth = user_logged_in(request)
    query = request.GET.get('query')
    req = urllib.request.Request('http://exp-api:8000/api/v1/search?query='+urllib.parse.quote(query))
    try:
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    except HTTPError as e:
        return HttpResponse(json.dumps({"error": e.msg}), status=e.code)
    except Exception as e:
        return HttpResponse(json.dumps({"error": str(type(e))}), status=500)

    book_list = json.loads(resp_json)
    return render(request, "search.html", {"book_list":book_list, "auth":auth, "results": len(book_list)})
