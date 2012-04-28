# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django.core.handlers import wsgi

from django.template.base import TemplateDoesNotExist

from django.utils.log import getLogger

from django.core import signals

from django.template import loader

from dhp import utils

from django import http

import os

logger = getLogger('django.request')

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

    def handle_uncaught_exception(self, request, exc_info):
        """
        Processing for any otherwise uncaught exceptions (those that will
        generate HTTP 500 responses). Can be overridden by subclasses who want
        customised 500 handling.

        Be *very* careful when overriding this because the error could be
        caused by anything, so assuming something like the database is always
        available would be an error.

        And of course it is overriden, to get rid of resolver ;)
        """

        from django.conf import settings

        if settings.DEBUG_PROPAGATE_EXCEPTIONS:
            raise

        logger.error('Internal Server Error: %s', request.path,
            exc_info=exc_info,
            extra={
                'status_code': 500,
                'request': request
            }
        )

        if settings.DEBUG:
            from django.views import debug
            return debug.technical_500_response(request, *exc_info)

        from django.views import defaults
        return defaults.server_error(request)

    def get_response(self, request):
        from django.core import exceptions
        from django.conf import settings

        self.dhp_root = request.dhp_root = settings.DHP_ROOT
        dhp_config = os.environ['DHP_CONFIG']

        file_to_serve = utils.get_file_to_serve(request)

        try:
            if dhp_config.endswith(file_to_serve):
                raise exceptions.PermissionDenied()

            if not file_to_serve.endswith('.dhp'):
                file_to_serve = '%s.dhp' % file_to_serve

            try:
                args = [file_to_serve]
                kwargs = {
                    'dictionary': {
                    }
                }

                response = http.HttpResponse(loader.render_to_string(*args, **kwargs), mimetype='text/html')
            except TemplateDoesNotExist:
                raise http.Http404()

        except http.Http404, e:
            logger.warning('Not Found: %s', request.path,
                        extra={
                            'status_code': 404,
                            'request': request
                        })
            if settings.DEBUG:
                from dhp.views import debug
                response = debug.technical_404_response(request, e)
            else:
                from django.views import defaults
                try:
                    #template = os.path.join(self.dhp_root, '404.html')
                    response = defaults.page_not_found(request)#, template_name=template)
                except:
                    import sys
                    try:
                        # Similar to the base one, but leave out resolver
                        response = self.handle_uncaught_exception(request, sys.exc_info())
                    finally:
                        signals.got_request_exception.send(sender=self.__class__, request=request)

                signals.got_request_exception.send(sender=self.__class__, request=request)

        except exceptions.PermissionDenied:
            from django.views import defaults

            logger.warning(
                'Forbidden (Permission denied): %s', request.path,
                extra={
                    'status_code': 403,
                    'request': request
                })
            try:
                response = defaults.permission_denied(request)
            except:
                try:
                    response = self.handle_uncaught_exception(request, sys.exc_info())
                finally:
                    signals.got_request_exception.send( sender=self.__class__, request=request)

        except SystemExit:
            # Allow sys.exit() to actually exit. See tickets #1023 and #4701
            raise
        except: # Handle everything else, including SuspiciousOperation, etc.
            import sys
            # Get the exception info now, in case another exception is thrown later.
            signals.got_request_exception.send(sender=self.__class__, request=request)
            response = self.handle_uncaught_exception(request, sys.exc_info())

        return response

# EOF

