# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8 filetype=python

__doc__ = """
Because we get called by execfile() and its globals, we can access os and environ
"""

home = os.path.expanduser('~')

environ['DHP_ROOT'] = os.path.join(home, 'src', 'git_checkouts', 'dhp', 'example')

# EOF

