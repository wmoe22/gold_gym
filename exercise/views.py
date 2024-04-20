from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseBadRequest
from django.shortcuts import render
import requests
from django.urls import reverse
from django.core.paginator import Paginator
import random
from django.contrib import messages

from datetime import date
from datetime import timedelta



from .models import User,Exercises,Streak

# Create your views here.


def index(request):
    return render(request,"exercise/index.html")
   
def exc_library(request):
    headers = {
        "X-RapidAPI-Key": "abfff46e62msh26dafa5ba772b8cp16ce3bjsna99497868e69",
        "X-RapidAPI-Host": "exercisedb.p.rapidapi.com"
    }

    try:
        querystring = {"limit":"210"}
        response = requests.get('https://exercisedb.p.rapidapi.com/exercises', headers=headers,params=querystring)
        
        if response.status_code == 200:
            data = response.json()
            for exercise_data in data:
                exercise, created = Exercises.objects.get_or_create(
                    id=exercise_data['id'],
                    defaults={
                        'name': exercise_data['name'],
                        'bodyPart': exercise_data['bodyPart'],
                        'equipment': exercise_data['equipment'],
                        'gifUrl': exercise_data['gifUrl'],
                        'target': exercise_data['target'],
                        'secondaryMuscles': exercise_data['secondaryMuscles'],
                        'instructions': exercise_data['instructions'],
                        "difficulty":random.choice(['easy','medium','hard'])
                    }
                )
                if not created:
                    exercise.name = exercise_data['name']
                    exercise.bodyPart = exercise_data['bodyPart']
                    exercise.equipment = exercise_data['equipment']
                    exercise.gifUrl = exercise_data['gifUrl']
                    exercise.target = exercise_data['target']
                    exercise.secondaryMuscles = exercise_data['secondaryMuscles']
                    exercise.instructions = exercise_data['instructions']
                    exercise.save()

            exercises = Exercises.objects.all()
            query = request.GET.get('q', '')
            exercises = exercises.filter(name__icontains=query)
            paginator  = Paginator(exercises,10)
            pg_number = request.GET.get('page')
            exc_per_page = paginator.get_page(pg_number)
            
                
            return render(request, 'exercise/exc_library.html', {'exercises': exercises,"exc_per_page":exc_per_page,'query': query})
        else:
            print(f"Failed to fetch data: {response.status_code}")
            return render(request, 'exercise/exc_library.html', {'error': 'Failed to fetch data from the API'})
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return render(request, 'exercise/exc_library.html', {'error': 'An error occurred during the request'})




def results(request):
    if request.method == "GET":
        query = request.GET.get('q','')
        foundExercise = [exercise for exercise in Exercises.objects.all() if query.lower() in exercise.name.lower()]
        paginator  = Paginator(foundExercise,10)
        pg_number = request.GET.get('page')
        exc_per_page = paginator.get_page(pg_number)
        
        return render(request,"exercise/results.html",{
                "query":query,
                "exc_per_page":exc_per_page
            })  

    else:
        return HttpResponseBadRequest("Bad request. ")      


def update_streak(request):

    user = request.user
    today = date.today()
    streak,created = Streak.objects.get_or_create(user=user,defaults={'start_date':today})

    if not created:
        #if the previous streak was yesterday we update
        if streak.start_date == today - timedelta(days=1):
            streak.current_streak += 1
        else:
            streak.current_streak = 1

        streak.longest_day_streak = max(int(streak.longest_day_streak), streak.current_streak)    
    else:
        streak.start_date = today
        streak.current_streak = 1
        streak.longest_day_streak = 1

    streak.save()     

    return render(request,"exercise/progress.html",{
        "user":user,
        "streak":streak
    })   


def login_view(request):
    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request,"exercise/login.html",{
                "message":"Invalid username or password"
            })
    else:
        return render(request,"exercise/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST['email']
        password = request.POST['password']
        confirmation = request.POST['confirmation']
        if password != confirmation:
            return render(request,"/login.html",{
                "message":"Passwords must match."
            })
        
        try:
            user  = User.objects.create_user(username,email,password)
            user.save()
        except IntegrityError:
            return render(request,"exercise/register.html",{
                "message":"Username already taken."
            })
        login(request,user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request,"exercise/register.html")


def filtered_exercises(request):
    if request.method == "GET":
        equipment = request.GET.get('equipment')
        musclegroup = request.GET.get("musclegroup")
        difficulty = request.GET.get("difficulty")

    exercises = Exercises.objects.all() 

    if equipment:
        exercises = exercises.filter(equipment=equipment.lower())  
    
    if musclegroup:
        exercises = exercises.filter(bodyPart=musclegroup.lower())  
    
    if difficulty:
        exercises = exercises.filter(difficulty=difficulty.lower())  
    return render(request, 'exercise/filtered_exercises.html',{
        "equipment":equipment,
        "musclegroup":musclegroup,
        "difficulty":difficulty,
        "exercises":exercises
    })

def filter_exercises(request):
    return render (request,"exercise/filter_exercises.html")

def save_exercise(request,id):
    if request.method == "POST":
        current_user = request.user
        data = Exercises.objects.get(pk=id)
        data.saved.add(current_user)
        return HttpResponseRedirect(reverse("detail",args=(id, )))
    
def unsave_exercise(request,id):
    if request.method == "POST":
        current_user = request.user
        data = Exercises.objects.get(pk=id)
        data.saved.remove(current_user)
        return HttpResponseRedirect(reverse("detail",args=(id, )))
    
def saved_exercise(request):
    current_user = request.user
    exercises = current_user.save_exc.all()
    return render(request,'exercise/saved_exc.html',{
        "exercises":exercises
    })    

def complete_exercise(request,id):
    if request.method == "POST":
        current_user = request.user
        data = Exercises.objects.get(pk=id)
        data.completed.add(current_user)
        messages.success(request, "Add to completed")
        return HttpResponseRedirect(reverse("detail",args=(id, )))


def completed_exercise(request):
    current_user = request.user
    exercises = current_user.complete_exercise.all()
    return exercises  

def detail(request, id):
        exercise = Exercises.objects.get(pk=id)
        in_saved_list  = request.user in exercise.saved.all()
        return render(request, "exercise/detail.html", {"id": id, "exercise": exercise,"in_saved_list":in_saved_list})


def progress(request):
    streak = Streak.objects.get(user=request.user)
    exercises = completed_exercise(request)

    return render(request, "exercise/progress.html", {
        "streak": streak,
        "exercises": exercises
    })