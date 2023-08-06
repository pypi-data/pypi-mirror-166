
from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Team1_CT6'
LONG_DESCRIPTION = 'Team1_CT6'

# Setting up
setup(
    name="fristPackge",
    version=VERSION,
    author="Kayzit",
    author_email="<tihonbebe123@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['opencv-python', 'pyautogui', 'pyaudio'],
    keywords=['python', 'video', 'stream',
              'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
