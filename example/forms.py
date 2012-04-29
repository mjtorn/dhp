# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django import forms

class HelloForm(forms.Form):
    """Test form
    """

    name = forms.fields.CharField(max_length=80)

    def save(self):
        """Fake save
        """

        f = open('/dev/null', 'wb')
        f.write(self.cleaned_data['name'])
        f.close()

        return self.cleaned_data['name']

# EOF

