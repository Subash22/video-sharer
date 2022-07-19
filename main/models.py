import os
from django.db import models
import cv2

# Create your models here.
class Video(models.Model):
    name = models.CharField(max_length=100)
    video_length = models.IntegerField(help_text="Please specify video length in seconds.", blank=True, null=True)
    video_size = models.FloatField(help_text="Please specify video length in MB's.", blank=True, null=True)
    video = models.FileField(upload_to='videos/')
    uploaded_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def check_extension(self):
        name, extension = os.path.splitext(self.video.name)
        if extension == ".mp4" or extension == ".mkv":
            return True
        else:
            return False
                
    def get_duration(self):
        video = cv2.VideoCapture(self.video.path)

        fps = video.get(cv2.CAP_PROP_FPS)
        frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
        duration = frame_count/fps
        seconds = int(duration)

        return seconds

    def get_size(self):
        video_size = self.video.size
        video_mb = round(video_size / (1024 * 1024), 2)

        return video_mb
    
    def delete(self, using=None, keep_parents=False):
        self.video.storage.delete(self.video.name)
        super().delete()
