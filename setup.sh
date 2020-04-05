rm -r build dist transformers_finetuning.egg-info
python setup.py sdist bdist_wheel
python -m twine upload dist/*