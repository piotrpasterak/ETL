import subprocess

if __name__ == '__main__':
#kikvy part
    subprocess.check_call(["python", '-m', 'pip', 'install', '--upgrade', 'pip', 'wheel', 'setuptools'])
    subprocess.check_call(["python", '-m', 'pip', 'install', 'docutils'])
    subprocess.check_call(["python", '-m', 'pip', 'install', 'pygments'])
    subprocess.check_call(["python", '-m', 'pip', 'install', 'pypiwin32'])
    subprocess.check_call(["python", '-m', 'pip', 'install', 'kivy.deps.glew'])
    subprocess.check_call(["python", '-m', 'pip', 'install', 'kivy.deps.angle'])
    subprocess.check_call(["python", '-m', 'pip', 'install', 'kivy.deps.sdl2'])
    subprocess.check_call(["python", '-m', 'pip', 'install', 'kivy'])
#BeautifulSoup4 part
    subprocess.check_call(["python", '-m', 'pip', 'install', 'requests'])
    subprocess.check_call(["python", '-m', 'pip', 'install', 'BeautifulSoup4'])
#Pony ORM
    subprocess.check_call(["python", '-m', 'pip', 'install', 'pony'])

