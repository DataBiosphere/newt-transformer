# standard library
import unittest
import os

# dependencies
import git

# local
from transform import main


class TestSheepdogGen3Transforming(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.git_repo = git.Repo(os.getcwd(), search_parent_directories=True)
        cls.project_path = cls.git_repo.git.rev_parse('--show-toplevel')
        cls.test_file = f'{cls.project_path}/tests/test_data/topmed-public.json'

    def test_sheepdog_gen3_transorming(self):
        args = [self.test_file]
        main(args)
