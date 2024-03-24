#
#   Copyright 2020 The SpaceONE Authors.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


from setuptools import setup, find_packages

with open('VERSION', 'r') as f:
    VERSION = f.read().strip()
    f.close()

setup(
    name='plugin-naver-cloud-inven-collector',
    version=VERSION,
    description='Collector plugin for Naver Cloud',
    long_description='',
    url='https://cloudforet.io/',
    author='Naevis Team',
    author_email='elsd0326@naver.com',
    license='Apache License 2.0',
    packages=find_packages(),
    install_requires=[
        'spaceone-core==2.0.77',
        'spaceone-api==2.0.135',
        'spaceone-tester==1.11.0'
    ],
    package_data={"inventory": ["metadata/spaceone/*/*.yaml"]},
    zip_safe=False,
)
