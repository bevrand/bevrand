from flask_script import Manager, Server
import unittest
from api.setup import app

manager = Manager(app)


@manager.command
def test():
    """Runs the tests without code coverage."""
    tests = unittest.TestLoader().discover('api/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    manager.run()
