from tests import test_setup_fixture


class RecommendationApiTests(test_setup_fixture.TestFixture):

    def test_ping_returns_200(self):
        split_url = "/".join(self.recommendation_url.split("/", 3)[:3])
        sut = split_url + '/ping'
        response = self.get_without_auth_header(sut)
        self.assertEqual(200, response.status_code)

    def test_should_be_able_to_get_beveragegroups(self):
        sut = self.recommendation_url + 'beveragegroups/'
        response = self.get_without_auth_header(sut)
        self.assertEqual(200, response.status_code)
        nodes = response.json()['nodes']
        self.assertTrue(len(nodes) > 1)

    def test_should_be_able_to_get_more_details_for_beveragegroups(self):
        sut = self.recommendation_url + 'beveragegroups/'
        response = self.get_without_auth_header(sut)
        self.assertEqual(200, response.status_code)
        nodes = response.json()['nodes']
        for node in nodes:
            sut = self.recommendation_url + 'categories?kind=' + node['title']
            response = self.get_without_auth_header(sut)
            self.assertEqual(200, response.status_code)
