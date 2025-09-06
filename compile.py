import PyInstaller.__main__

PyInstaller.__main__.run([
    'core/compiler.py',
    '--onedir',
    '--name','lumen',
    '--icon','lumen.ico',
    '--clean',
    '--noconfirm'
])