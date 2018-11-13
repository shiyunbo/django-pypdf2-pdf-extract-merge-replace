from django.shortcuts import render
from django.http import FileResponse
from .forms import PdfExtractForm, PdfMergeForm, PdfReplaceForm
import os
import PyPDF2
import zipfile


# Create your views here.
def pdf_single_page_extract(request):
    if request.method == 'POST':
        # 如果用户通过POST提交
        form = PdfExtractForm(request.POST, request.FILES)
        if form.is_valid():
            # 获取上传的文件
            f = form.cleaned_data['file']
            # 转化为PDF文件对象
            pdfFileObj = PyPDF2.PdfFileReader(f)

            # 获取需提取页面列表
            page_num_list = form.cleaned_data['page'].split(',')

            #创建zipfile对象, 生成提取文件压缩包
            zf = zipfile.ZipFile(os.path.join('media', 'extracted_pages.zip'), 'w')

            for page_num in page_num_list:
            # pdf文档页码对象编码是从0开始，所以减一
                page_index = int(page_num) - 1

            # 利用PyPDF2提取页码对象
                pageObj = pdfFileObj.getPage(page_index) # 从0编码
            # 利用PyPDF2创建新的Pdf Writer
                pdfWriter = PyPDF2.PdfFileWriter()
            # 添加已读取的页面对象
                pdfWriter.addPage(pageObj)

            # pdf文件路径
                pdf_file_path = os.path.join('media', 'extracted_page_{}.pdf'.format(page_num))
            # 将提取页面写入新的PDF文件
                with open(pdf_file_path, 'wb') as pdfOutputFile:
                    pdfWriter.write(pdfOutputFile)
            # 写入zip文件
                zf.write(pdf_file_path)
            zf.close()

            # 给用户返回zip压缩包
            response = FileResponse(open(os.path.join('media', 'extracted_pages.zip'), 'rb'))
            response['content_type'] = "application/zip"
            response['Content-Disposition'] = 'attachment; filename="extracted_pages.zip"'
            return response

    else:
        # 如果用户没有通过POST，提交生成空表单
        form = PdfExtractForm()

    return render(request, 'pdf/pdf_extract.html', {'form': form})


def pdf_range_extract(request):
    if request.method == 'POST':
        # 如果用户通过POST提交
        form = PdfExtractForm(request.POST, request.FILES)
        if form.is_valid():
            # 获取上传的文件
            f = form.cleaned_data['file']
            # 转化为PDF文件对象
            pdfFileObj = PyPDF2.PdfFileReader(f)

            page_range = form.cleaned_data['page'].split('-')
            page_start = int(page_range[0])
            page_end = int(page_range[1])

            # Extracted pdf file path
            pdf_file_path = os.path.join('media', 'extracted_page_{}-{}.pdf'.format(page_start, page_end))
            pdfOutputFile = open(pdf_file_path, 'ab+')

            # 利用PyPDF2创建新的Pdf Writer
            pdfWriter = PyPDF2.PdfFileWriter()

            for page_num in range(page_start, page_end + 1):
                # pdf文档页码对象编码是从0开始，所以减一
                page_index = int(page_num) - 1

                # 利用PyPDF2提取页码对象
                pageObj = pdfFileObj.getPage(page_index) # 从0编码

                # 添加已读取的页面对象
                pdfWriter.addPage(pageObj)

            pdfWriter.write(pdfOutputFile)
            pdfOutputFile.close()

            extractedPage = open(pdf_file_path, 'rb')
            response = FileResponse(extractedPage)
            response['content_type'] = "application/octet-stream"
            response['Content-Disposition'] = 'attachment; filename="extracted_pages.pdf"'

            return response
    else:
        # 如果用户没有通过POST，提交生成空表单
        form = PdfExtractForm()

    return render(request, 'pdf/pdf_range_extract.html', {'form': form})


# Create your views here.
def pdf_merge(request):
    if request.method == 'POST':
        # 如果用户通过POST提交
        form = PdfMergeForm(request.POST, request.FILES)
        if form.is_valid():
            # 获取上传的文件1
            f1 = form.cleaned_data['file1']
            # 获取上传的文件2
            f2 = form.cleaned_data['file2']
            # 获取上传的文件3
            f3 = form.cleaned_data['file3']
            # 获取上传的文件4
            f4 = form.cleaned_data['file4']
            # 获取上传的文件5
            f5 = form.cleaned_data['file5']

            f_list = [f1, f2, f3, f4, f5]

            # 创建PDF文件合并对象，添加合并文件
            pdfMerger = PyPDF2.PdfFileMerger()

            # 转化为PDF文件对象
            for f in f_list:
                if f:
                    pdfFileObj = PyPDF2.PdfFileReader(f)
                    pdfMerger.append(pdfFileObj)

            # 将合并文件对象写入到merged_file.pdf
            with open(os.path.join('media', 'merged_file.pdf'), 'wb') as pdfOutputFile:
                pdfMerger.write(pdfOutputFile)

            # 打开合并的merged_file.pdf，通过FileResponse输出
            response = FileResponse(open(os.path.join('media', 'merged_file.pdf'), 'rb'))
            response['content_type'] = "application/octet-stream"
            response['Content-Disposition'] = 'attachment; filename="merged_file.pdf"'

            return response

        else:
            # 如果通过POST提交，但表单未通过验证
            form = PdfMergeForm()

    else:
        # 如果用户没有通过POST，提交生成空表单
        form = PdfMergeForm()

    return render(request, 'pdf/pdf_merge.html', {'form': form})


def pdf_replace(request):
    if request.method == 'POST':
        # 如果用户通过POST提交
        form = PdfReplaceForm(request.POST, request.FILES)
        if form.is_valid():
            # 获取需要插入的PDF页面文件1
            f1 = form.cleaned_data['file1']
            # 获取需要被替换的文件2
            f2 = form.cleaned_data['file2']
            # 获取替换页码数
            page = form.cleaned_data['page']

            # 获取文件2总页数
            pdfFileObj = PyPDF2.PdfFileReader(f2)
            total_page = pdfFileObj.getNumPages()


            # 获取文件2第一部分-人为可读页码
            page_start = 1
            page_end = page - 1

            pdfOutputFile1 = open(os.path.join('media', 'part_1.pdf'), 'wb+')
            # 利用PyPDF2创建新的Pdf Writer
            pdfWriter = PyPDF2.PdfFileWriter()

            for page_num in range(page_start, page_end + 1):
                # pdf文档页码对象编码是从0开始，所以减一
                page_index = int(page_num) - 1

                # 利用PyPDF2提取页码对象
                pageObj = pdfFileObj.getPage(page_index)  # 从0编码

                # 添加已读取的页面对象
                pdfWriter.addPage(pageObj)

            pdfWriter.write(pdfOutputFile1)
            pdfOutputFile1.close()

            # 获取文件2第2部分-人为可读页码
            page_start = page + 1
            page_end = total_page

            pdfOutputFile2 = open(os.path.join('media', 'part_2.pdf'), 'wb+')
            # 利用PyPDF2创建新的Pdf Writer
            pdfWriter = PyPDF2.PdfFileWriter()

            for page_num in range(page_start, page_end + 1):
                # pdf文档页码对象编码是从0开始，所以减一
                page_index = int(page_num) - 1

                # 利用PyPDF2提取页码对象
                pageObj = pdfFileObj.getPage(page_index)  # 从0编码

                # 添加已读取的页面对象
                pdfWriter.addPage(pageObj)

            pdfWriter.write(pdfOutputFile2)
            pdfOutputFile2.close()

            f2_part_1 = open(os.path.join('media', 'part_1.pdf'), 'rb+')
            f2_part_2 = open(os.path.join('media', 'part_2.pdf'), 'rb+')

            # 创建PDF文件合并对象，添加合并文件
            pdfMerger = PyPDF2.PdfFileMerger()
            pdfMerger.append(PyPDF2.PdfFileReader(f2_part_1))
            pdfMerger.append(PyPDF2.PdfFileReader(f1))
            pdfMerger.append(PyPDF2.PdfFileReader(f2_part_2))

            # 将合并文件对象写入到replaced_file.pdf
            with open(os.path.join('media', 'replaced_file.pdf'), 'wb') as pdfOutputFile:
                pdfMerger.write(pdfOutputFile)

            # 打开合并的replaced_file.pdf，通过HttpResponse输出
            response = FileResponse(open(os.path.join('media', 'replaced_file.pdf'), 'rb'))
            response['content_type'] = "application/octet-stream"
            response['Content-Disposition'] = 'attachment; filename="replaced_file.pdf"'

            return response

        else:
            # 如果通过POST提交，但表单未通过验证
            form = PdfReplaceForm()

    else:
        # 如果用户没有通过POST，提交生成空表单
        form = PdfReplaceForm()

    return render(request, 'pdf/pdf_replace.html', {'form': form})