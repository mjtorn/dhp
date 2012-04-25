# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

import os

class WSGIHandler():
    def __call__(self, environ, start_response):
        dhp_config = environ['DHP_CONFIG']
        execfile(dhp_config)

        dhp_root = environ['DHP_ROOT']

        file_to_serve = environ.get('PATH_INFO', '/index.dhp')
        file_to_serve = file_to_serve[1:]
        path_to_serve = os.path.join(dhp_root, file_to_serve)

        if os.path.exists(path_to_serve) and path_to_serve == dhp_config:
            status = '403 FORBIDDEN'
            output = 'Do not access config'
        elif os.path.exists(path_to_serve):
            status = '200 OK'
            # XXX: chunks?
            output = open(path_to_serve, 'rb').read()
        else:
            status = '404 NOT FOUND'
            output = 'Not found: %s' % file_to_serve

        response_headers = [
            ('Content-Type', 'text/plain'),
            ('Content-Length', len(output)),
        ]

        start_response(status, response_headers)

        return output

# EOF

