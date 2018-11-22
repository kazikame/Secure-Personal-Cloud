"""Copyright Askbot SpA 2014, Licensed under GPLv3 license."""
import os
from django.conf import settings
from django.core.exceptions import PermissionDenied, ImproperlyConfigured
from django.urls import reverse
from django.http import StreamingHttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render

try:
    from django.utils.module_loading import import_string as import_module
except ImportError:
    from django.utils.module_loading import import_by_path as import_module


# utils functions
def check_access(request):
    """Returns true if user has access to the directory"""
    access_mode = getattr(settings, 'DIRECTORY_ACCESS_MODE', 'public')
    if access_mode == 'public':
        return True
    elif access_mode == 'use-perms':
        if request.user.is_anonymous():
            return False
        else:
            return request.user.has_perm('directory.read')
    elif access_mode == 'custom':
        check_perm = settings.DIRECTORY_ACCESS_FUNCTION
        if isinstance(check_perm, basestring):
            check_perm = import_module(check_perm)
        elif not hasattr(check_perm, '__call__'):
            raise ImproperlyConfigured('DIRECTORY_ACCESS_FUNCTION must either be a function or python path')
        return check_perm(request)
    else:
        raise ImproperlyConfigured(
            "Invalid setting DIRECTORY_ACCESS_MODE: only values "
            "'public', 'use-perms', and 'custom' are allowed"
        )


def get_file_names(directory):
    """Returns list of file names within directory"""
    contents = os.listdir(directory)
    files = list()
    for item in contents:
        if os.path.isfile(os.path.join(directory, item)):
            files.append(item)
    return files


def read_file_chunkwise(file_obj):
    """Reads file in 32Kb chunks"""
    while True:
        data = file_obj.read(32768)
        if not data:
            break
        yield data


# view functions below
def index(request):
    return HttpResponseRedirect(reverse('directory_list', args=(".",)))


def list_directory(request, d_name="."):
    """default view - listing of the directory"""
    if request.user.is_authenticated:
        directory = os.path.join(settings.CLOUD_DIR, request.user.username, d_name)
        if not os.path.exists(directory):
            template = getattr(settings, 'DEFAULT_DIR_TEMPLATE', 'directory/default.html')
            return render(request, template)
        data = {'user': request.user.username, 'directory_name': d_name,
                'files': [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))],
                'subdirs': ["{0}/".format(d) for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
                }
        template = getattr(settings, 'DIRECTORY_TEMPLATE', 'directory/list.html')
        return render(request, template, data)

    else:
        raise PermissionDenied()


def download_file(request, dir_name, file_name="", *args, **kwargs):
    """allows authorized user to download a given file"""
    # dir_name = file_tuple[0]
    # file_name = file_tuple[1]
    if file_name == "":
        file_name = dir_name
        dir_name = "."
    if os.path.sep in file_name:
        raise PermissionDenied()

    if request.user.is_authenticated:
        directory = os.path.join(settings.CLOUD_DIR, request.user.username)
        # make sure that file exists within current directory

        file_path = os.path.join(directory, dir_name, file_name)
        if os.path.isfile(file_path):
            response = StreamingHttpResponse(content_type='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename=%s' % file_name
            file_obj = open(file_path, 'rb')
            response.streaming_content = read_file_chunkwise(file_obj)
            return response
        else:
            raise Http404(file_path)
    else:
        raise Http404


def view_file(request, dir_name, file_name="", *args, **kwargs):
    """allows user to view the file"""
    if file_name == "":
        file_name = dir_name
        dir_name = "."

    if os.path.sep in file_name:
        raise PermissionDenied()

    if request.user.is_authenticated:
        directory = os.path.join(settings.CLOUD_DIR, request.user.username)

        file_path = os.path.join(directory, dir_name, file_name)
        if os.path.isfile(file_path) and os.path.getsize(file_path) < 2.5* (10**7):
            file_obj = open(file_path, 'r')
            b64_str = file_obj.read()
            return render(request, 'view.html', {'file_str': b64_str, 'file_name': file_name})
        else:
            raise Http404(file_path)
    else:
        raise Http404
