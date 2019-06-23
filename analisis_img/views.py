from django.shortcuts import render
from django.http import HttpResponse
from .controllers.imageController import color_filter
from .forms import UploadFileForm
# Create your views here.
def index(request):
	#dosomething()
	return render(request, 'analisis_imagen.html')

def _upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            form.save()
            
    return HttpResponse("home")

def upload(request):
    print(request.FILES)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        print('valid', form.is_valid())
        #if form.is_valid():
        fname = handle_uploaded_file(request.FILES['myFile'])
        color_filter(fname)
    #else:
     #   form = UploadFileForm()
    #return render(request, 'upload.html', {'form': form})
    return render(request, 'analisis_imagen_resultados.html')

def handle_uploaded_file(f):
    print('f',f)
    with open(f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    return f.name