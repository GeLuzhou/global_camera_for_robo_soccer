from setuptools import setup
import os
from glob import glob

package_name = 'image_saver_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),  # 添加launch文件路径

    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='coastz',
    maintainer_email='coastz@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'image_saver = image_saver_pkg.image_saver:main',
        ],
    },
)
