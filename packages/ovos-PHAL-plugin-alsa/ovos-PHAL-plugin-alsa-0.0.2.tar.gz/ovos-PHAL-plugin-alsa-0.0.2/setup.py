#!/usr/bin/env python3
import os

from setuptools import setup


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


PLUGIN_ENTRY_POINT = 'ovos-PHAL-plugin-alsa=ovos_PHAL_plugin_alsa:AlsaVolumeControlPlugin'
setup(
    name='ovos-PHAL-plugin-alsa',
    version='0.0.2',
    description='A volume control plugin for OpenVoiceOS hardware abstraction layer',
    url='https://github.com/OpenVoiceOS/ovos-PHAL-plugin-alsa',
    author='JarbasAi',
    author_email='jarbasai@mailfence.com',
    license='Apache-2.0',
    packages=['ovos_PHAL_plugin_alsa'],
    package_data={'': package_files('ovos_PHAL_plugin_alsa')},
    install_requires=[
        "ovos-plugin-manager~=0.0",
        "json_database~=0.7",
        "pyalsaaudio~=0.9"],
    zip_safe=True,
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: Linguistic',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    entry_points={'ovos.plugin.phal': PLUGIN_ENTRY_POINT}
)
