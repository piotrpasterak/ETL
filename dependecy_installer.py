import subprocess
# TODO: Unfortunately you will need to manually add path to firefox.exe into system PATH

modules = [
    ['--upgrade', 'pip', 'wheel', 'setuptools'],
    ['docutils'],
    ['pygments'],
    ['pypiwin32'],
    ['kivy.deps.glew'],
    ['kivy.deps.angle'],
    ['kivy.deps.sdl2'],
    ['kivy'],
    ['requests'],
    ['BeautifulSoup4'],
    ['selenium'],
    ['webdriverdownloader'],
    ['lxml'],
    ['pony'],
    ['pymysql']
]

scripts = [
    ['install_scripts/webdriver_installer.py'],
    ['install_scripts/database_setup.py']]


def install_step(install_args):
    arguments = ["python", '-m', 'pip', 'install']
    arguments.extend(install_args)

    subprocess.call(arguments)


def call_step(call_args):
    arguments = ['python']
    arguments.extend(call_args)

    subprocess.call(arguments)


if __name__ == '__main__':

    for module_name in modules:
        install_step(module_name)

    for script_name in scripts:
        call_step(script_name)
