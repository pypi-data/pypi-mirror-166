# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mextractor']

package_data = \
{'': ['*']}

install_requires = \
['opencv-python>=4.6.0,<5.0.0',
 'pydantic-numpy>=1.3.0,<2.0.0',
 'pydantic>=1.9.2,<2.0.0',
 'ruamel.yaml>=0.17.21,<0.18.0',
 'setuptools']

extras_require = \
{':python_version >= "3.7" and python_version < "3.8"': ['numpy>=1.21.0,<2.0.0'],
 ':python_version >= "3.8" and python_version < "3.11"': ['numpy'],
 'video-extract': ['ffmpeg-python>=0.2.0,<0.3.0']}

setup_kwargs = {
    'name': 'mextractor',
    'version': '2.0.0',
    'description': 'mextractor can extract media metadata to YAML and read them',
    'long_description': '# mextractor: media metadata extractor\n\nVideos and images can be large. \n\n## Installation\n\nDownload and install from PyPi with `pip`:\n\n```shell\npip install mextractor\n```\n\n## Usage\n\n### Extract and dump metadata\n\n#### Video\n\n```python\nfrom mextractor.workflow import extract_and_dump_video\n\nmetadata = extract_and_dump_video(dump_dir, path_to_video, include_image, greyscale, lossy_compress_image)\n```\n\n#### Image\n\n```python\nfrom mextractor.workflow import extract_and_dump_image\n\nmetadata = extract_and_dump_image(dump_dir, path_to_image, include_image, greyscale, lossy_compress_image)\n```\n\n### Load media\n\n#### Video\n\n```python\nimport mextractor\n\nvideo_metadata = mextractor.load(mextractor_dir)\n\nprint(video_metadata.average_fps)\nprint(video_metadata.frames)\nprint(video_metadata.resolution)\nprint(video_metadata.video_length_in_seconds)\n```\n\n#### Image\n\n```python\nimport mextractor\n\nimage_metadata = mextractor.load(mextractor_dir)\n\nprint(image_metadata.resolution)\n```\n',
    'author': 'Can H. Tartanoglu',
    'author_email': 'canhtart@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pypi.org/project/mextractor/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
