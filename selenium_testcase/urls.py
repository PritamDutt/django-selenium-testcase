from django.conf import settings
from django.conf.urls import url
from django.views.generic import TemplateView

TEST_TEMPLATES = getattr(settings, 'SELENIUM_TESTCASE_TEMPLATES', [])

urlpatterns = [
    url(path, TemplateView.as_view(template_name=template))
    for path, template in TEST_TEMPLATES
]
