import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Youtube_Video_Audio_Downloader",
    version="0.2.15",
    author="Alex Au",
    author_email="AlexXianZhenYuAu@gmail.com",
    description="A Simple GUI interface to help download videos and audio files from Youtube using Youtube-dl and FFMPEG",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Alex-Au1/Youtube_Downloader",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "Pillow",
        "pyperclip",
        "yt-dlp",
        "youtube-search-python",
        "mutagen",
        "requests",
        "validators"
    ],
    python_requires='>=3.6',
)
