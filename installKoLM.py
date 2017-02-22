# Install KoLM package by locating kolm directory to user's site-packages path
import os
import site; path = site.getsitepackages()[0]
os.system('cp -rf kolm ' + path)