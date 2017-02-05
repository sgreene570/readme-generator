import sys
import unittest

from context import converter


def run_tests():
    class __unit_tests__(unittest.TestCase):
        def setUp(self):
            """
            Setup for tests. Not yet implemented.
            """
            pass

        def test_clean_line(self):
            """
            Test the clean_line method.
            """
            line = "<br>"
            self.assertEqual(converter.clean_line(line), "")


        def test_get_languages(self):
            """
            Test the get_languages method with the readme-generator respository.
            """
            # FIXME: This is a sketchy test.
            languages = converter.get_languages("https://api.github.com/repos/sgreene570/readme-generator")
            self.assertIn("##Languages Used\n<br>\n<ul>\n<li>Python", languages)


        def test_get_contributors(self):
            """
            Test the get_languages method with the readme-generator respository.
            """
            contributors = converter.get_contributors("https://api.github.com/repos/sgreene570/readme-generator")
            self.assertIn(
                    "\n<br>\n##Contributors\n<br>\n<ul>\n<li><a href='"
                    + "https://github.com/sgreene570'>sgreene570</a></li>\n<li>"
                    + "<a href='https://github.com/mattgd'>mattgd</a></li>\n</ul>"
            , contributors)


        def test_get_repo_url(self):
            """
            Test the get_repo_url method with the readme-generator respository.
            """
            self.assertEqual(converter.get_repo_url(), "https://github.com/sgreene570/readme-generator.git")


        def test_get_api_url(self):
            """
            Test the get_api_url method with the readme-generator respository.
            """
            self.assertEqual(converter.get_api_url(
                            "https://github.com/sgreene570/readme-generator.git"),
                            "https://api.github.com/repos/sgreene570/readme-generator")


    suite = unittest.TestLoader().loadTestsFromTestCase(__unit_tests__)
    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
    if 'test' in sys.argv[1:]:
        run_tests()
        sys.exit(0)
