from django.urls import path, re_path
from . import views

# namespace
app_name = 'pdf'

urlpatterns = [
    # 上传pdf，用户输入需要提取的页面, 返回需要提取的页面
    path('extract/single/', views.pdf_single_page_extract, name='pdf_single_page_extract'),
    path('extract/range/', views.pdf_range_extract, name='pdf_range_extract'),
    path('merge/', views.pdf_merge, name='pdf_merge'),
    path('replace/', views.pdf_replace, name='pdf_replace'),
]