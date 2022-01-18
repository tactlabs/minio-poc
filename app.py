from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from minio import Minio
import os

LOCAL_FILE_PATH = os.environ.get('LOCAL_FILE_PATH')
ACCESS_KEY = os.environ.get('ACCESS_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')

MINIO_API_HOST = "http://localhost:9000"

MINIO_CLIENT = Minio(
        "localhost:9000", access_key=ACCESS_KEY, secret_key=SECRET_KEY, secure=False   
    )

BUCKET_NAME = "first"



app = Flask(__name__)

def get_all_images():

    images = []
    #videos=[]

    for single_object in MINIO_CLIENT.list_objects(BUCKET_NAME, recursive=True):

        if single_object.object_name.endswith((".jpg", ".png", ".jpeg",)):

            images.append(single_object.object_name)
        #elif single_object.object_name.endswith((".mp4")):
            #videos.append(single_object.object_name)


    images = [f"{MINIO_API_HOST}/{BUCKET_NAME}/{image}" for image in images]
   # videos = [f"{MINIO_API_HOST}/{BUCKET_NAME}/{video}" for video in videos]
    print(images)
    #print(videos)
    return images

def get_all_videos():

    
    videos=[]

    for single_object in MINIO_CLIENT.list_objects(BUCKET_NAME, recursive=True):

        if single_object.object_name.endswith((".mp4")):
            videos.append(single_object.object_name)


   
    videos = [f"{MINIO_API_HOST}/{BUCKET_NAME}/{video}" for video in videos]
    
    print(videos)
    return videos
def main():
 

    # Make 'first' bucket if not exist.
    found = MINIO_CLIENT.bucket_exists("first")
    if not found:
        MINIO_CLIENT.make_bucket("first")
    else:
        print("Bucket 'first' already exists")

    # Upload '/home/ramanathan/Downloads/bbb.jpg' as object name
    # 'bbb.jpg' to bucket 'first'.
    MINIO_CLIENT.fput_object(
        "first", "desk.mp4", LOCAL_FILE_PATH, 
    )
    print(
       "It is successfully uploaded as "
        "object 'bbb.jpg' to bucket 'first'."
    )

@app.route('/', methods = ['GET', 'POST'])
def index():
    main()
    all_images = get_all_images()
    all_videos = get_all_videos()

    return render_template('index.html', images = all_images, videos =all_videos)

if __name__ == "__main__":
    
    app.run(debug=True)

# MINIO_ROOT_USER=talha MINIO_ROOT_PASSWORD=12345678 minio server ./data1 ./data2 ./data3 ./data4 ./data5 --console-address :9001

# http://192.168.0.103:9000/altair/137.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=F6DX5PBV3EQXPL26VBCJ%2F20211226%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20211226T140417Z&X-Amz-Expires=604800&X-Amz-Security-Token=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NLZXkiOiJGNkRYNVBCVjNFUVhQTDI2VkJDSiIsImV4cCI6MTY0MDUyODYxNywicGFyZW50IjoidGFsaGEifQ.vqt-LQ-j05_VJxIoFHogiSiQIgSvwZrFoho5KxsTtVhBIts7Sey_vs8R-frKFXY3MWlOY1PSIx9kc5mnUGaDaQ&X-Amz-SignedHeaders=host&versionId=null&X-Amz-Signature=3fcc43e213948e8076081a03035498811d66cd61ba95f6ce56cc29022401440d