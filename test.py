"""
test MOSS
"""
from typing import NoReturn
from unittest import TestCase, main

import validators

from service import moss


class BaseTestCase(TestCase):
    """
    Test case for python
    """
    def test_moss_python(self) -> NoReturn:
        """
        test python
        """

        result = moss.file_check(
            "python_test", "python3", [
                {"name": "1", "content": '''print('hello world')'''},
                {"name": "2", "content": '''print('hello world')\n'''},
            ]
        )
        self.assertEqual(True,validators.url(result))

if __name__ == '__main__':
    main()
