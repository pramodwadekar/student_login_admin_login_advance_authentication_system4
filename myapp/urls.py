from django.urls import path, include
from .import views

urlpatterns = [
    # main page urls
    path("",views.mainpage, name = 'mainpage'),

    # student reistration and logout code urls
    path("registerpage/",views.Register_page, name = 'register_page'),
    path('register/', views.User_Register, name = "register"),
    path("loginpage/", views.loginpage, name = "loginpage"),
    path("loginuser/", views.LoginUser, name = "login"),
    path("fpassword/", views.forgot_pass, name = "forgot"),
    path('change_pass/', views.fpassword, name = "fpassword"),
    path("homepage/", views.homepage, name = "home"),


    # #update student data by student
    path("Edit_students_data/", views.Edit_student_data, name = "edit_student"),
    path("update_students_data/", views.update_student_data, name = "update_student"),


    # database code urls
    path("index/",views.index, name = 'index'),
    path("chart/", views.pie_chart, name = 'chart'),
    path("filterbyname/", views.filter_data, name = 'name'),
    
    # adminpage code urls
    path("adminloginpage/", views.AdminLoginPage, name = 'admin'),
    path('logout_page/', views.LogoutPage, name = "logout"),
 
]