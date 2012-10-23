import setuptools

setup_params = dict(
    name="pmxbot-sed-correcter",
    version = "0.1",
    packages=setuptools.find_packages(),
    entry_points=dict(
        pmxbot_handlers = [
            'sed_correcter = pmxbot_sed_correcter.sedcorrecter:SedCorrecter.initialize',
        ]
    ),
    description="Allows pmx bot to correct you with the syntax s/find/replace/",
    license = 'MIT',
    author="Chris Jowett",
    author_email="cryptk@gmail.com",
    maintainer = 'Chris Jowett',
    maintainer_email = 'cryptk@gmail.com',
    url = 'https://www.cryptkcoding.com',
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
