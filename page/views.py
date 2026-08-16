from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserForm
from .models import FileUpload,AceessRequest
import requests
# Create your views here.

def signup_view(request):
    
    if request.method=="POST":
        
        form = UserForm(request.POST)
        
        if form.is_valid():
            
            form.save()
            return redirect('login')
        else:
            print("Not valid")
            return render(request,'signup.html',{'form':form,'error':form.errors.as_text})
    form = UserForm()
    return render(request,'signup.html',{'form':form})

def login_view(request):
    
    if request.method=='POST':
        
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        user=authenticate(request,username=username,password=password)
        
        if user:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Invalid username or password.")
    return render(request,'login.html')
@login_required
def home(request):
    
    files= FileUpload.objects.all()
    files_requests=AceessRequest.objects.filter(file__user=request.user)
    my_requests=AceessRequest.objects.filter(requester=request.user)
    if request.method=='POST':
        
        file= request.FILES.get('file')
        visibility =request.POST.get('access')
        is_public = visibility == 'True'
        #print(is_public)

        if file:
            
            cid=ipfs_upload(file) 
            FileUpload.objects.create(user=request.user,file=file,cid=cid,is_public=is_public)
        
        return redirect('home')
    return render(request,'home.html',{'files':files,'file_requests':files_requests,'my_requests':my_requests})

def ipfs_upload(file):
    
    #local_ipfs_url url="http://127.0.0.1:5001/api/v0/add"
    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    
    headers={
        
            'pinata_api_key': 'api key',
            'pinata_secret_api_key': 'api secret'
            }   
    
    files={
        'file':(file.name,file.read())
    }
    
    try:
        response= requests.post(url,files=files,headers=headers)
        response.raise_for_status()
        cid=response.json()['IpfsHash']
        return cid
    except requests.exceptions.HTTPError as error:
        
        print("http error occured",error)
    except requests.exceptions.ConnectionError:
        print("Network error: Could not connect to the server.")
        
        
def request_view(request,file_id):
    
    file=FileUpload.objects.get(id=file_id)
    print(file)
    #print("Inserted.............")
    object,created=AceessRequest.objects.update_or_create(file=file,requester=request.user,
                                                          defaults={"status":"pending"})
    
    return redirect('home')

def grant_access(request,requester_id,file_id):
    file=FileUpload.objects.get(id=file_id)
    if file.user == request.user:
        user = User.objects.get(id=requester_id)
        #print(user)
        #print('Valid..............')
        
        file.accessble_users.add(user)
        file = AceessRequest.objects.filter(requester=requester_id,file=file_id).update(status="approved")
        return redirect('home')

def revoke_access(request,requester_id,file_id):
    file=FileUpload.objects.get(id=file_id)
    if file.user == request.user:
        #print('Valid..............')
        file = AceessRequest.objects.filter(requester=requester_id,file=file_id).update(status='Rejected')
        
        return redirect('home')

    

def logout_view(request):
    logout(request)
    
    return redirect('login')
