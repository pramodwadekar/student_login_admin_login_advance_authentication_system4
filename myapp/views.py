from django.shortcuts import render, redirect
from .models import student
from django.contrib import messages
from django.db.models import Q
import json
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


# Main Page Code Start

def mainpage(request):
    return render(request, "mainpage.html")

# Main Page Code End


# admin login logout system start

# def admin_signup_page(request):
#     # def SignupPage(request):
#     if request.method=='POST':
#         uname=request.POST.get('username')
#         email=request.POST.get('email')
#         pass1=request.POST.get('password1')
#         pass2=request.POST.get('password2')

#         if pass1!=pass2:
#             massage = "Your password and confirm password are not Same!!"
#             return render (request, "admin_signup.html", {"msg":massage})
#         else:

#             my_user=User.objects.create_user(uname,email,pass1)
#             my_user.save()
#             return redirect('admin')
    
#     return render(request, "admin_signup.html" )

def AdminLoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        User=authenticate(request,username=username,password=pass1)
        if User is not None:
            login(request,User)
            return redirect('index')
        else:
            return render(request, "admin_login.html")
    return render (request,'admin_login.html')


def LogoutPage(request):
    logout(request)
    return render(request,'admin_login.html')   
# admin login logout system end



# student/user registration login laogout page code start
def Register_page(request):
    return render(request, 'register.html')


def User_Register(request):
    if request.method == "POST":
        fname = request.POST['fname']
        dob = request.POST['dob']
        email = request.POST['email']
        age = request.POST['age']
        gender = request.POST['gender']
        country = request.POST['country']
        state = request.POST['state']
        city = request.POST['city']
        qualification = request.POST['qualification']
        subject = request.POST.getlist('subject')
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        # First we will validate thet user already exist
        user = student.objects.filter(Email = email)
        if user:
            message = ("User Already Exist.....")
            return render(request, 'register.html', {"msg":message})
        else:
            if password == cpassword:
                newuser = student.objects.create(Fullname = fname, DOB = dob, Email = email, Age = age,
                                   Gender = gender, Country = country, State = state, City = city, 
                                   Qualification = qualification, Subject =subject, Password = password)
                message =("User Register Successfull")
                return render(request, "login.html",{"msg":message})
            else:
                message = ("Password and Confirm password Doen't Match")
                return render(request, 'register.html', {"msg":message})
            

def loginpage(request):
    return render(request, "login.html")


def LoginUser(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password'] 
        
        #Checking email id with database 
        try:
            user = student.objects.get(Email = email) 
            if user:
                if user.Password == password:
                    request.session['id'] = user.id
                    request.session['Fullname'] = user.Fullname
                    request.session['Email'] = user.Email
                    request.session['Age'] = user.Age
                    request.session['Gender'] = user.Gender
                    request.session['Country'] = user.Country
                    request.session['State'] = user.State
                    request.session['City'] = user.City
                    request.session['Qualification'] = user.Qualification
                    request.session['Subject'] = user.Subject
                    return redirect ('home')
                else:
                    message ="Password Does Not Match"
                    return render(request, "login.html",{"msg":message})
        except student.DoesNotExist:
            message = "User Does Not Exist Please Register"
            return render(request, "login.html", {"msg": message})
    else:
        return render(request, "login.html")  
    
#student data edit code 

def Edit_student_data(request):
    if request.method == "POST":
        user_id = request.session.get('id')
        user = student.objects.get(id=user_id)
        return render(request, "update_student.html", {"key2": user})
    


# student data update code 

def update_student_data(request):
    if request.method == "POST":
        user_id = request.session.get('id')
        user = student.objects.get(id=user_id)
        user.Fullname = request.POST['fname']
        user.DOB = request.POST['dob']
        user.Email = request.POST['email']
        user.Age = request.POST['age']
        user.Gender = request.POST['gender']
        user.Country = request.POST['country']
        user.State = request.POST['state']
        user.City = request.POST['city']
        user.Qualification = request.POST['qualification']
        user.Subject = request.POST.getlist('subject')
        user.save()
        return redirect("home")
    


 
def forgot_pass(request):
    return render(request, 'fpassword.html')


def fpassword(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST['cpassword']

        try:
            user = student.objects.get(Email=email)  # Assuming you have a User model with an 'Email' field
            if password == cpassword:
                user.Password = password  # This line should be changed
                user.save()
                message = ("Password Updated Successfully")
                return render(request,'login.html',{"msg":message})
            else:
                message = ("Passwords do not match")
                return render(request, 'fpassword.html', {'msg':message})
        except student.DoesNotExist:
            message = ("User Does Not Exist. Please Register")
            return render(request, "register.html", {"msg": message})
    return render(request, 'fpassword.html')

def homepage(request):
    return render(request, "home.html")

# student/user register login logout page code end 







# database code start
# @login_required(login_url='admin')
def index(request):
    
    students = student.objects.all().order_by("Fullname")
    query = ""
    page = request.GET.get('page', 1)
 
    paginator = Paginator(students, 5)
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)
 
    # return render(request, 'index.html', { 'students': students })
    
    if request.method == "POST":
        if "add" in request.POST:
            name = request.POST.get("name")
            dob = request.POST.get("dob")
            email = request.POST.get("email")
            Age = request.POST.get("Age")
            gender = request.POST.get("gender")
            country = request.POST.get("country")
            state = request.POST.get("state")
            city = request.POST.get("city")
            qualification = request.POST.get("qualification")
            subject = request.POST.getlist("subject")
            student.objects.create(Fullname = name, DOB = dob, Email = email, Age = Age,
                                   Gender = gender, Country = country, State = state, City = city, 
                                   Qualification = qualification, Subject =subject)
            messages.success(request, "New Student Added Successfull")
            return redirect('index')
        
        
        elif "update" in request.POST:
            id = request.POST.get("id")
            name = request.POST.get("name")
            dob = request.POST.get("dob")
            email = request.POST.get("email")
            Age = request.POST.get("Age")
            gender = request.POST.get("gender")
            country = request.POST.get("country")
            state = request.POST.get("state")
            city = request.POST.get("city")
            qualification = request.POST.get("qualification")
            subject = request.POST.getlist("subject")

            Update_student = student.objects.get(id=id)
            Update_student.Fullname = name
            Update_student.DOB = dob
            Update_student.Email = email
            Update_student.Age = Age
            Update_student.Gender = gender
            Update_student.Country = country
            Update_student.State = state
            Update_student.City = city
            Update_student.Qualification = qualification
            Update_student.Subject = subject
            Update_student.save()

            messages.success(request, "Student Data Updated Successfull")
            return redirect('index')
    


        elif "delete" in request.POST:
            id = request.POST.get("id")
            student.objects.get(id=id).delete()  
            messages.success(request, "Student Deleted Successfully")
            return redirect('index')
        
        # elif "namesearch" in request.POST:
        #     namequery = request.POST.get("namesearchquery")
        #     students = student.objects.filter(Fullname = namequery)
        #     context = {"students" : students, "namequery" : namequery}

        elif "dobsearch" in request.POST:
            dobquery = request.POST.get("dobsearchquery")
            students = student.objects.filter(DOB__contains = dobquery)
            context = {"students" : students, "dobquery" : dobquery}

        elif "emailsearch" in request.POST:
            emailquery = request.POST.get("emailsearchquery")
            students = student.objects.filter(Email = emailquery)
            context = {"students" : students, "emailquery" : emailquery}

 

        elif "search" in request.POST:
            query = request.POST.get("searchquery")
            students = student.objects.filter(Q(Fullname__icontains=query) | Q(DOB__icontains=query) | Q(Email__icontains=query) |
                                              Q(Age__icontains=query) | Q(Gender__icontains=query) | Q(City__icontains=query) | 
                                              Q(Qualification__icontains=query) | Q(State__icontains=query))


    context = {"students" : students, "query" : query}
    return render(request,'index.html', context = context)

# database code end


# chart code start 
def pie_chart(request):
    # Query the database to get the data you need
    students = student.objects.all()

    # Extract age data and labels for the chart
    age_data = [student.Age for student in students]
    labels = [student.Fullname for student in students]

    # Create a dictionary containing the chart data
    chart_data = {
        'data': age_data,
        'labels': labels,      
    }
    return render(request, 'chart.html', {'chart_data': json.dumps(chart_data)})

# chart code end 

# this method is using function and use filter by name 
def filter_data(request):
    if request.method == "POST":
        namequery = request.POST.get("namesearchquery")
        new = student.objects.filter(Fullname = namequery).order_by("-DOB")
        context = {"students":new, "namequery" : namequery}
        return render(request,'index.html', context = context)






