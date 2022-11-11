from django.shortcuts import render
from .forms import SimpleUploadForm,ImageUploadForm
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .cv_functions import cv_detect_face

# Create your views here.
def first_view(request):
    return render(request, 'opencv_webapp/first_view.html', {})

def simple_upload(request):

    # print(request.method)  # 'POST'
    if request.method == 'POST':



        # print('/n/n/n')
        # print(request.POST)
        # print(request.FILES)
        # print('/n/n/n')

        # request.POST # title
        # request.FILES # image

        form = SimpleUploadForm(request.POST, request.FILES)

        if form.is_valid():
            myfile =request.FILES['image'] # 메모리에 업로드된 유저이미지

            fs = FileSystemStorage()
            # fs.save('파일 이름', 파일 객체 자체)
            filename = fs.save(myfile.name, myfile)

            uploaded_file_url = fs.url(filename) # 저장 끝난 파일로 접근가능 url

            context = {'form':form, 'uploaded_file_url':uploaded_file_url}

            return render(request, 'opencv_webapp/simple_upload.html', context)



            # fs.save() / fs.url() / fs.delete()  fs에서 주로 사용하는 3가지..



    else:
        form = SimpleUploadForm()

        context = {'form':form}

        return render(request, 'opencv_webapp/simple_upload.html', context)


#Detect face with OpenCV

def detect_face(request):


    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)

        if form.is_valid():

            post = form.save(commit=False)  #중간저장기능 commit=False 하나의 행을 받아낸다. 받아내서 각각의행에 후처리를 할 수 있다.
            # post.description = papago.translate(post.description)  # 이런식으로후처리해서 덮어쓸수있다.
            post.save()

            # form.save()


            # document : ImageUploadModel Class에 선언되어 있는 “document”에 해당
            imageURL = settings.MEDIA_URL + form.instance.document.name
            # == form.instance.document.url  //  form.instance form 자체를 말한다.
            # == post.document.url    // 임시저장한 post 하나의 행의 url
            # == '/media/images/2021/10/29/ses_XQAftn4.jpg'
            # print(form.instance, form.instance.document.name, form.instance.document.url)
            cv_detect_face(settings.MEDIA_ROOT_URL + imageURL) # 추후 구현 예정


            # saved_models/cnn_basic.h5
            # saved_models/main_data.xlsx

            # 위와 같은 모델파일을 저장한다고 하면 saved_models폴더에...  그것을 가져와서 사용하는방법 settings에 넣어주면
            # 초기에 로드한다.
            # import tensorflow as tf
            # loaded_model = tf.keras.models.loaded_model('./saved_models/cnn_basic.h5')




            return render(request, 'opencv_webapp/detect_face.html', {'form':form, 'post':post})

    else:
        #GET 요청처리 -> 단순히 127.0.0.1/detect_face 로 접속하는경우는 GET요청이다. 그때는 어떻게 반응할지를 설정하는것
        form = ImageUploadForm() # empty form
        return render(request, 'opencv_webapp/detect_face.html', {'form':form})
