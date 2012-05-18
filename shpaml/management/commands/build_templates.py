'''
Created on 07.05.2012

@author: alekam
'''
from django.conf import settings
from django.core.management.base import BaseCommand
from shpaml import shpaml
import os


class Command(BaseCommand):
    help = "Find SHPAML templates and compile its to HTML Django templates."
    requires_model_validation = False

    def handle(self, filename=None, force=False, **options):
        self.force = force
        if filename is None:
            for pathname in settings.TEMPLATE_DIRS:
                self.process_dir(pathname)
        else:
            if not filename.endswith('.shpaml'):
                print u'File "%s" is not shpaml template' % filename
            for dirname in settings.TEMPLATE_DIRS:
                file_name = os.path.join(dirname, filename)
                if os.path.exists(file_name):
                    self.process_file(dirname, filename)
                else:
                    print u'File "%s" is not found' % file_name


    def process_dir(self, pathname):
        for dirname, dirnames, filenames in os.walk(pathname):
            for subdirname in dirnames:
                self.process_dir(os.path.join(dirname, subdirname))
            for filename in filenames:
                if filename.endswith('.shpaml'):
                    self.process_file(dirname, filename)

    def process_file(self, pathname, filename):
                    html_filename = os.path.join(pathname, u"%s.html" % filename[:-7])
                    f = open(os.path.join(pathname, filename))
                    if os.path.exists(html_filename):
                        if not self.force:
                            print u"File %s already exists and will be skipped" % html_filename
                            return
                        os.remove(html_filename)
                    html_f = open(html_filename, 'w+')
                    html_f.write(shpaml.convert_text(f.read()))
                    f.close()
                    html_f.close()
                    print u"Write file %s" % html_filename
