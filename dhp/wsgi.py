# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django.core.handlers import wsgi

from django import http

import os

class WSGIHandler(wsgi.WSGIHandler):
    def __call__(self, environ, start_response):
        dhp_config = environ['DHP_CONFIG']

        os.environ['DJANGO_SETTINGS_MODULE'] = self.get_django_conf(dhp_config)

        return super(WSGIHandler, self).__call__(environ, start_response)

    def get_django_conf(self, dhp_config):
        """Mangle the name
        """

        dhp_config_file = dhp_config.rsplit('.', 1)[0]
        dhp_config_file = dhp_config_file.rsplit('/', 3)[-2:]
        dhp_config_module = '.'.join(dhp_config_file)

        return dhp_config_module

    def get_response(self, request):
        from django.conf import settings

        self.dhp_root = request.dhp_root = settings.DHP_ROOT
        dhp_config = os.environ['DHP_CONFIG']

        path_to_serve = self.get_path_to_serve(request)

        if os.path.exists(path_to_serve) and path_to_serve == dhp_config:
            status = '403'
            output = 'Do not access config'
        elif os.path.exists(path_to_serve):
            status = '200 OK'
            # XXX: chunks?
            output = open(path_to_serve, 'rb').read()
        else:
            status = '404'
            output = 'Not found: %s' % path_to_serve

        res = http.HttpResponse(content=output, mimetype='text/plain', status=status)

        return res

# EOF

