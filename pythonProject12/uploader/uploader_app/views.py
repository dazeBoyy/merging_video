import os

from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_protect
from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.io.VideoFileClip import VideoFileClip

from .forms import BlogForm
from .models import Blog
import moviepy.editor

from .utilitis import *


@csrf_protect
def UploadFile(request):
    if request.method == 'POST':

        form = BlogForm(request.POST, request.FILES)
        videos = request.FILES.getlist('file')
        if form.is_valid():
            destination_folder = create_destination_folder()
            print("REQUEST ----> ", request)
            print("VIDEOS ----> ", videos)
            for video_number, video in enumerate(videos, 1):
                upload_original_videos(video, video_number, destination_folder)
            task = merge_videos(destination_folder)
            final_video = task.split('\\')

            my_video = form.save(commit=False)
            my_video.file = final_video[-2]
            my_video.save()
            context = {
                'video': str(final_video[-2]),
            }
            return render(request, 'clipVideo.html', context)
    else:
        form = BlogForm()
        context = {
            'form': form,
        }
    return render(request, 'index.html', context)


def ViewFile(request):
    form = BlogForm()

    blog_info = Blog.objects.all()

    context = {'all_info': blog_info, 'form': form}
    return render(request, 'ImageUpload.html', context)


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username is already taken')
                return redirect(register)
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email is already taken')
                return redirect(register)
            else:
                user = User.objects.create_user(username=username, password=password,
                                                email=email, first_name=first_name, last_name=last_name)
                user.save()

                return redirect('login_user')


        else:
            messages.info(request, 'Both passwords are not matching')
            return redirect(register)


    else:
        return render(request, 'registration.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect('login_user')



    else:
        return render(request, 'login.html')


def logout_user(request):
    auth.logout(request)
    return redirect('home')


def clear_database(request):
    for blog in Blog.objects.all():
        blog.delete()
    return redirect(request.POST.get('next'))

def view_video(request,name):
    video = name
    context = {'video': video}
    return render(request,'clipVideo.html', context)