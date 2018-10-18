# ETL
extract, transform, load (ETL) project - semester work

# Dependencies:

## Kivy

Now that python is installed, open the Command line and make sure python is available by typing python --version. Then, do the following to install.

Ensure you have the latest pip and wheel:

python -m pip install --upgrade pip wheel setuptools
Install the dependencies (skip gstreamer (~120MB) if not needed, see Kivy’s dependencies):

python -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew
python -m pip install kivy.deps.gstreamer
Note

If you encounter a MemoryError while installing, add after pip install an option –no-cache-dir.

For Python 3.5+, you can also use the angle backend instead of glew. This can be installed with:

python -m pip install kivy.deps.angle
Install kivy:

python -m pip install kivy
(Optionally) Install the kivy examples:

python -m pip install kivy_examples
The examples are installed in the share directory under the root directory where python is installed.

That’s it. You should now be able to import kivy in python or run a basic example if you installed the kivy examples:

python share\kivy-examples\demo\showcase\main.py
Note

If you encounter any permission denied errors, try opening the Command prompt as administrator and trying again.

## BeautifulSoup4
pip install requests BeautifulSoup4

## Pony ORM
if we want to put data to database:
https://ponyorm.com

# References
https://realpython.com/python-web-scraping-practical-introduction/
