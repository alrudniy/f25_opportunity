from django.test import SimpleTestCase
from django.urls import reverse, resolve
from budget.views import project_list, project_detail, ProjectCreateView



class TestUrls(SimpleTestCase):

    def test_list_url_is_resolves(self):
        url = reverse('list')
        print(resolve(url))
        self.assertEquals(resolve(url).func, project_list)



    def test_project_create_url_resolves(self):
        url = reverse('add')
        print(resolve(url))
        self.assertEquals(resolve(url).func, ProjectCreateView)

    def test_detail_url_resolves(self):
        url = reverse('detail', args=['test-slug'])
        print(resolve(url))
        self.assertEquals(resolve(url).func, project_list)
    