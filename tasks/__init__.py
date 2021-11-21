"""Here we import the different task submodules/ collections"""
from invoke import Collection

from . import app, test

# pylint: disable=invalid-name
# as invoke only recognizes lower case
namespace = Collection()
namespace.add_collection(test)
namespace.add_collection(app)
