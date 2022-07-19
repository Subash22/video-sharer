
from django.urls import path
from .views import VideoStoreView, AllVideosView, VideoStorePriceView

urlpatterns = [
    path('store/', VideoStoreView.as_view(), name="video_store"),
    path('all-videos/', AllVideosView.as_view(), name="all_videos"),
    path('get-price/', VideoStorePriceView.as_view(), name="video_price"),
]
