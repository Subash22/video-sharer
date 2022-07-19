from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from main.serializers import VideoSerializer
from .models import Video


# Create your views here.
class VideoStoreView(APIView):

    def post(self, *args, **kwargs):
        video_file = self.request.data['video']
        name = self.request.data['name']

        video = Video()
        video.video = video_file
        video.name = name
        video.save()

        duration = video.get_duration()
        size = video.get_size()

        if duration <= 600 and size <= 1024 and video.check_extension():
            video.video_length = duration
            video.video_size = size
            video.save()
        else:
            video.delete()

            context = {
                "message": "Video duration must be less then 10 minutes, size should be less then 1GB and video extension should be either mp4 or mkv."
            }
            return Response(context, status=status.HTTP_200_OK)

        context = {
            "message": "Video uploaded successfully."
        }
        return Response(context, status=status.HTTP_200_OK)
    

class AllVideosView(APIView):

    def get(self, *args, **kwargs):
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')

        size_from = self.request.GET.get('size_from')
        size_to = self.request.GET.get('size_to')

        length_from = self.request.GET.get('length_from')
        length_to = self.request.GET.get('length_to')

        videos = Video.objects.all()

        if date_from != None and date_to != None:
            videos = videos.filter(uploaded_on__range=[date_from, date_to])
        elif date_from != None:
            videos = videos.filter(uploaded_on__gte=date_from)
        elif date_to != None:
            videos = videos.filter(uploaded_on__lte=date_to)
        else:
            pass
        
        if size_from != None and size_to != None:
            videos = videos.filter(video_size__range=[size_from, size_to])
        elif size_from != None:
            videos = videos.filter(video_size__gte=size_from)
        elif size_to != None:
            videos = videos.filter(video_size__lte=size_to)
        else:
            pass

        if length_from != None and length_to != None:
            videos = videos.filter(video_length__range=[length_from, length_to])
        elif length_from != None:
            videos = videos.filter(video_length__gte=length_from)
        elif length_to != None:
            videos = videos.filter(video_length__lte=length_to)
        else:
            pass

        # serializers
        videos_serializers = VideoSerializer(videos, many=True).data

        context = {
            "message": "success",
            "videos": videos_serializers,
        }
        return Response(context, status=status.HTTP_200_OK)
    

class VideoStorePriceView(APIView):

    def post(self, *args, **kwargs):
        video_size = float(self.request.data['size'])  # MB
        video_length = int(self.request.data['length'])  # Seconds
        price = 0
        
        if video_size < 500:
            price = 5
        elif video_size >= 500 and video_size <= 1024:
            price = 12.5
        else:
            context = {
                "message": "Video size cannot be more than 1GB.",
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
        if video_length < 378:
            price += 12.5
        elif video_length >= 378 and video_length <= 600:
            price += 20
        else:
            context = {
                "message": "Video length cannot be more than 10 minutes.",
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        context = {
            "message": "success",
            "price": "$"+str(price)
        }
        return Response(context, status=status.HTTP_200_OK)
    