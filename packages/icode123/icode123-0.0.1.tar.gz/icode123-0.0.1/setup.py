from setuptools import setup, find_packages

setup(
    name='icode123',
    version='0.0.1',
    keywords='check',
    description='一个本地开发环境检测库。',
    license='MIT License',
    url='https://icode123.cn',
    author='学航',
    author_email='xuehang00126@126.com',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    long_description=open('README.md', encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'requests~=2.28.1',
        'PyJWT~=2.4.0',
    ],
)
