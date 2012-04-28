# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django.utils.encoding import smart_str

from django.http import HttpResponseNotFound

from django.template import Template, Context

from django.views import debug

from dhp import utils

class FakePattern(object):
    """Look a bit like a regexp
    """

    def __init__(self, path):
        """Display regex.pattern like this
        """

        self.pattern = path


class FakeUrlPattern(object):
    """Embodies a ``FakePattern``
    XXX: Not exactly sure why length needs to look like 2 here...
    """

    def __init__(self, path):
        """To fake a ``path``
        """

        self.regex = FakePattern(path)
        self.iterate = 2

    def __len__(self):
        return 2

    def __iter__(self):
        return self

    def next(self):
        if self.iterate > 0:
            self.iterate -= 1
            return self
        else:
            raise StopIteration()


def technical_404_response(request, exception):
    """Create a technical 404 error response. The exception should be the Http404.
    Based on Django.
    """

    fake_url_pattern = FakeUrlPattern(utils.get_path_to_serve(request))

    t = Template(debug.TECHNICAL_404_TEMPLATE, name='Technical 404 template')
    c = Context({
        'urlconf': 'DHP',
        'root_urlconf': 'N/A',
        'request_path': request.path_info[1:], # Trim leading slash
        'urlpatterns': fake_url_pattern,
        'reason': smart_str(exception, errors='replace'),
        'request': request,
        'settings': debug.get_safe_settings(),
    })
    return HttpResponseNotFound(t.render(c), mimetype='text/html')

# EOF

