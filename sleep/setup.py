import setuptools

setup_params = dict(
    name="pmxbot-sleep",
    version = "0.1",
    packages=setuptools.find_packages(),
    entry_points=dict(
        pmxbot_handlers = [
            'sleep = pmxbot_sleep',
        ]
    ),
    description="Sleep enforcer for Coders beyond their useful amount of time to code",
    license = 'MIT',
    author="Tom King",
    author_email="ka6xox@gmail.com",
    maintainer = 'Tom King',
    maintainer_email = 'ka6sox@gmail.com',
    url = 'none',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Communications :: Chat',
        'Topic :: Communications :: Chat :: Internet Relay Chat',
    ],
)

if __name__ == '__main__':
    setuptools.setup(**setup_params)
