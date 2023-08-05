import pathlib
import shutil
import unittest

from autocomp import classname_completions, methodname_completions, module_completions


build_dir = pathlib.Path(__file__).parent.joinpath('../build/')
if build_dir.exists():
    shutil.rmtree(build_dir)


class MethodnameCompletionTestCase(unittest.TestCase):

    def test_completion_with_empty_partial(self):
        partial = ''
        completions = list(methodname_completions(partial))
        expected = []

        self.assertEqual(completions, expected)

    def test_completion_with_only_folder_or_module(self):
        for partial in ('test', 'test.', 'test..', 'test...'):
            completions = list(methodname_completions(partial))
            expected = []

            self.assertEqual(completions, expected)

    def test_completion_with_missing_classname(self):
        for partial in ('test.test_completions', 'test.test_completions.', 'test_utils'):
            completions = list(methodname_completions(partial))
            expected = []

            self.assertEqual(completions, expected)

    def test_completion_with_only_classname(self):
        for partial in (
            'test.test_completions.ModuleCompletionTestCase.',
            'test.test_completions.ModuleCompletionTestCase..',
        ):
            completions = list(methodname_completions(partial))
            expected = ['test.test_completions.ModuleCompletionTestCase.test_completion_with_empty_partial',
                        'test.test_completions.ModuleCompletionTestCase.test_completion_with_half_folder_name',
                        'test.test_completions.ModuleCompletionTestCase.test_completion_with_half_folder_name_non_existent',
                        'test.test_completions.ModuleCompletionTestCase.test_completion_with_full_folder_name',
                        'test.test_completions.ModuleCompletionTestCase.test_completion_with_half_file_name',
                        'test.test_completions.ModuleCompletionTestCase.test_completion_with_full_file_name',
                        'test.test_completions.ModuleCompletionTestCase.test_completion_with_trailing_dots',
                        'test.test_completions.ModuleCompletionTestCase.test_completion_with_classname']

            self.assertEqual(completions, expected)

    def test_completion_with_only_classname_and_half_method_name(self):
        for partial in (
            'test.test_completions.ModuleCompletionTestCase.test',
            'test.test_completions.ModuleCompletionTestCase.test_completion',
            'test.test_completions.ModuleCompletionTestCase.test_completion_with',
        ):
            completions = list(methodname_completions(partial))
            expected = ['test.test_completions.ModuleCompletionTestCase.test_completion_with_empty_partial',
                        'test.test_completions.ModuleCompletionTestCase.test_completion_with_half_folder_name',
                        'test.test_completions.ModuleCompletionTestCase.test_completion_with_half_folder_name_non_existent',
                        'test.test_completions.ModuleCompletionTestCase.test_completion_with_full_folder_name',
                        'test.test_completions.ModuleCompletionTestCase.test_completion_with_half_file_name',
                        'test.test_completions.ModuleCompletionTestCase.test_completion_with_full_file_name',
                        'test.test_completions.ModuleCompletionTestCase.test_completion_with_trailing_dots',
                        'test.test_completions.ModuleCompletionTestCase.test_completion_with_classname']

            self.assertEqual(completions, expected)

    def test_completion_with_only_full_method_name(self):
        partial = 'test.test_completions.ModuleCompletionTestCase.test_completion_with_classname'
        completions = list(methodname_completions(partial))
        expected = [partial, ]

        self.assertEqual(completions, expected)


class ClassnameCompletionTestCase(unittest.TestCase):
    def test_completion_with_empty_partial(self):
        partial = ''
        completions = list(classname_completions(partial))
        expected = []

        self.assertEqual(completions, expected)

    def test_completion_with_missing_trailing_dot(self):
        partial = 'test.test_completions'
        completions = list(classname_completions(partial))
        expected = []

        self.assertEqual(completions, expected)

    def test_completion_with_trailing_dot(self):
        partial = 'test.test_completions.'
        completions = list(classname_completions(partial))
        expected = [
            'test.test_completions.MethodnameCompletionTestCase',
            'test.test_completions.ClassnameCompletionTestCase',
            'test.test_completions.ModuleCompletionTestCase'
        ]

        self.assertEqual(completions, expected)

    def test_completion_with_full_module_but_invalid_classname(self):
        partial = 'test.test_completions.Foo'
        completions = list(classname_completions(partial))
        expected = []

        self.assertEqual(completions, expected)

    def test_completion_with_full_module_and_half_classname(self):
        partial = 'test.test_completions.Classname'
        completions = list(classname_completions(partial))
        expected = ['test.test_completions.ClassnameCompletionTestCase', ]

        self.assertEqual(completions, expected)


class ModuleCompletionTestCase(unittest.TestCase):

    def test_completion_with_empty_partial(self):
        """An empty string should yield all test case files"""
        partial = ''
        completions = list(module_completions(partial))
        expected = ['test.test_completions', 'test.test_utils']

        self.assertEqual(completions, expected)

    def test_completion_with_half_folder_name(self):
        """Half of the folder name should yield all test cases in folder"""
        partial = 'te'
        completions = list(module_completions(partial))
        expected = ['test.test_completions', 'test.test_utils']

        self.assertEqual(completions, expected)

    def test_completion_with_half_folder_name_non_existent(self):
        """If the folder name has not test cases nothing is returned"""
        partial = 'ab'
        completions = list(module_completions(partial))
        expected = []

        self.assertEqual(completions, expected)

    def test_completion_with_full_folder_name(self):
        """If the full folder name is given, all test files are returned"""
        partial = 'test'
        completions = list(module_completions(partial))
        expected = ['test.test_completions', 'test.test_utils']

        self.assertEqual(completions, expected)

    def test_completion_with_half_file_name(self):
        partial = 'test.test_uti'
        completions = list(module_completions(partial))
        expected = ['test.test_utils', ]

        self.assertEqual(completions, expected)

    def test_completion_with_full_file_name(self):
        partial = 'test.test_utils'
        completions = list(module_completions(partial))
        expected = ['test.test_utils', ]

        self.assertEqual(completions, expected)

    def test_completion_with_trailing_dots(self):
        for partial in ('test.test_utils.', 'test.test_utils..'):
            completions = list(module_completions(partial))
            expected = []

            self.assertEqual(completions, expected)

    def test_completion_with_classname(self):
        partial = 'test.test_utils.TestCase'
        completions = list(module_completions(partial))
        expected = []

        self.assertEqual(completions, expected)
