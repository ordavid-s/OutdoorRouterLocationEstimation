from setuptools import setup, find_packages

# class PostInstallCommand(install):
#     """Post-installation for installation mode."""
#     def run(self):
#         print('[+] Running make services')
#         os.system('./install_services.sh')
#         install.run(self)
#         print('Done')


setup(
    name='capture',
    version='0.1',
    packages=find_packages(),
    url='',
    license='',
    # cmdclass={
        # 'install': PostInstallCommand,
    # },
    install_requires=['pynmea2', 'serial', 'folium'],
)
