import PyInstaller.__main__

PyInstaller.__main__.run([
    'core/compiler.py',
    '--onefile',
    '--name lumen'
])