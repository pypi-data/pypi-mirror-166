from setuptools import setup, find_packages

readme = open("./README.md", "r")


setup(
    name='easily_quiz',
    packages=['easily_quiz'],  # this must be the same as the name above
    version='1.3',
    description='easily_quiz is a spanish api that you can create simple quiz!',
    long_description=readme.read(),
    long_description_content_type='text/markdown',
    author='PinaYT',
    author_email='contacto.pinayt@gmail.com',
    # use the URL to the github repo
    url='https://github.com/PinaYTTT/easily_quiz',
    download_url='https://github.com/PinaYTTT/easily_quiz',
    install_requires=['colorama'],
    keywords=['easily_quiz', 'quiz', 'truefalse'],
    classifiers=[ ],
    license='MIT',
    include_package_data=True
)