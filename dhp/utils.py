# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

import os

def get_file_to_serve(request):
    """Get just the file
    """

    environ = request.environ

    file_to_serve = environ.get('PATH_INFO', '/index.dhp')
    file_to_serve = file_to_serve[1:]

    return file_to_serve

def get_path_to_serve(request):
    """To keep get_response simpler
    """

    file_to_serve = get_file_to_serve(request)

    path_to_serve = os.path.join(request.dhp_root, file_to_serve)

    return path_to_serve


# EOF

