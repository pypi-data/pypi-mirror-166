## Deploy package

Create a distribution:

```bash
rm -rf dist/
python setup.py sdist
python setup.py bdist_wheel
```

Upload to [Test PyPI](https://packaging.python.org/en/latest/guides/using-testpypi/) and verify things look right:

```bash
twine upload -r testpypi dist/*
```

Twine will prompt for your username and password.

Upload to [PyPI](https://pypi.org/):

```bash
twine upload dist/*
```

Create a git tag and a github release associated to this distribution.
