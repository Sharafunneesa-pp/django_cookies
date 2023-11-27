from django.shortcuts import render
from . models import movies
from . forms import MovieForm
from django.contrib.auth.decorators import login_required
# Create your views here.


def create(request):
    frm=MovieForm()
    if request.POST:
        frm=MovieForm(request.POST)
        if frm.is_valid():
            frm.save()
        else:
            frm=MovieForm()    

       

    return render(request,'create.html',{'frm':frm})



# how cookies work
def list(request):
    print(request.COOKIES)
    visits=int(request.COOKIES.get('visits',0))
    visits=visits+1
    # movie_set=movies.objects.all()
    movie_set=movies.objects.filter(year=1990)
    print(movie_set)
    response=render(request,'list.html',{'movies':movie_set,'visits':visits})
    response.set_cookie('visits',visits)
    return response



def edit(request,pk):
    
    instance_to_be_edited = movies.objects.get(pk=pk)
    if request.POST:
        frm=MovieForm(request.POST,instance=instance_to_be_edited)
        if frm.is_valid():
            instance_to_be_edited.save()
    else:
        recent_visits=request.session.get('recent_visits',[])
        recent_visits.insert(0,pk)
        request.session['recent_visits']=recent_visits
        
        frm=MovieForm(instance=instance_to_be_edited)
    return render(request,'create.html',{'frm':frm})

        


def delete(request,pk):
    instance=movies.objects.get(pk=pk)
    instance.delete()
    movie_set=movies.objects.all()
    print(movie_set)
    return render(request,'list.html',{'movies':movie_set})


