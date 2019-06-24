from django.shortcuts import render
from django.http import HttpResponse

from .controllers.imageController import color_filter, size_filter
from .forms import UploadFileForm
# Create your views here.

savePath = "arduino/static/"

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
        myFile = request.FILES['myFile']
        fname = handle_uploaded_file(myFile)
        colorObj = color_filter(savePath+fname)
        print('colorObj', colorObj)
        lstObjs = size_filter(savePath+fname)
        print("lstObjs", lstObjs)
    #else:
     #   form = UploadFileForm()
    #return render(request, 'upload.html', {'form': form})
    return render(request, 'analisis_imagen_resultados.html', {"colorObj": colorObj, "lstObjs": lstObjs, "fileName": fname})

def handle_uploaded_file(f):
    print('f',f)
    with open(savePath+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    return f.name