import os
from django.http import FileResponse, HttpResponse
from django.shortcuts import redirect, render
from django.core.files.storage import FileSystemStorage
from .forms import UploadFileForm
from .diff_parser import DifflibParser, DiffCode

def upload_and_compare_files(request):
    fs = FileSystemStorage()
    if request.method == 'POST':
        if 'delete_files' in request.POST:
            file1_name = request.POST.get('file1_name')
            file2_name = request.POST.get('file2_name')
            if file1_name:
                file_path = os.path.join(fs.location, file1_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            if file2_name:
                file_path = os.path.join(fs.location, file2_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            return redirect('upload_and_compare_files')

        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file1 = request.FILES.get('file1')
            file2 = request.FILES.get('file2')

            filename1 = filename2 = None
            content1 = content2 = ''

            if file1:
                filename1 = fs.save(file1.name, file1)
                with fs.open(filename1) as f1:
                    content1 = f1.read().decode('utf-8').splitlines()

            if file2:
                filename2 = fs.save(file2.name, file2)
                with fs.open(filename2) as f2:
                    content2 = f2.read().decode('utf-8').splitlines()

            if content1 and content2:
                diff_parser = DifflibParser(content1, content2)
                differences = list(diff_parser)
                return render(request, 'diff_result.html', {
                    'differences': differences,
                    'file1_name': filename1,
                    'file2_name': filename2,
                    'DiffCode': DiffCode,
                })
    else:
        form = UploadFileForm()

    return render(request, 'upload.html', {'form': form})

def delete_files(request):
    fs = FileSystemStorage()
    if request.method == 'POST':
        file1_name = request.POST.get('file1_name')
        file2_name = request.POST.get('file2_name')
        if file1_name:
            file_path = os.path.join(fs.location, file1_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        if file2_name:
            file_path = os.path.join(fs.location, file2_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
    return redirect('upload_and_compare_files')


def generate_and_download_diff(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file1 = request.FILES.get('file1')
            file2 = request.FILES.get('file2')

            content1 = content2 = ''
            if file1:
                content1 = file1.read().decode('utf-8').splitlines()
            if file2:
                content2 = file2.read().decode('utf-8').splitlines()

            if content1 and content2:
                diff_parser = DifflibParser(content1, content2)
                file_path = os.path.join(os.path.dirname(__file__), 'results.txt')
                save_diff_to_file(diff_parser, file_path)

                if os.path.exists(file_path):
                    try:
                        with open(file_path, 'rb') as file:
                            response = HttpResponse(file.read(), content_type='text/plain')
                            response['Content-Disposition'] = 'attachment; filename=results.txt'
                            return response
                    except Exception as e:
                        return render(request, 'diff_result.html', {'error': 'Error reading file: {}'.format(str(e))})
                else:
                    return render(request, 'diff_result.html', {'error': 'File not found'})

    elif request.method == 'GET':

            file_path = os.path.join(os.path.dirname(__file__), 'results.txt')

            if os.path.exists(file_path):
                try:
                    with open(file_path, 'rb') as file:
                        response = HttpResponse(file.read(), content_type='text/plain')
                        response['Content-Disposition'] = 'attachment; filename=results.txt'
                        return response
                except Exception as e:
                    return render(request, 'diff_result.html', {'error': 'Error reading file: {}'.format(str(e))})
            else:
                return render(request, 'diff_result.html', {'error': 'File not found'})

    return redirect('upload_and_compare_files')

def save_diff_to_file(diff_parser, filename):
    print(diff_parser)
    try:
        with open(filename, 'w') as file:
            for diff in diff_parser:
                if diff['code'] == DiffCode.SIMILAR:
                    file.write(f"  {diff['line']}\n")
                elif diff['code'] == DiffCode.LEFTONLY:
                    file.write(f"- {diff['line']}\n")
                elif diff['code'] == DiffCode.RIGHTONLY:
                    file.write(f"+ {diff['line']}\n")
                elif diff['code'] == DiffCode.CHANGED:
                    file.write(f"- {diff['line']}\n")
                    if 'leftchanges' in diff and diff['leftchanges'] is not None:
                        file.write("? " + ''.join(['^' if i in diff['leftchanges'] else ' ' for i in range(len(diff['line']))]) + "\n")
                    file.write(f"+ {diff['newline']}\n")
                    if 'rightchanges' in diff and diff['rightchanges'] is not None:
                        file.write("? " + ''.join(['^' if i in diff['rightchanges'] else ' ' for i in range(len(diff['newline']))]) + "\n")
        print("save_diff_to_file completed:", filename)
    except Exception as e:
        print(f"Error occurred: {str(e)}")