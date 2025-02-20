from setuptools import setup

setup(
    name="竹影",
    app=['main.py'],
    version='1.0.0',
    setup_requires=['py2app'],
    options={
        'py2app': {
            'argv_emulation': True,
            'packages': ['PIL', 'numpy', 'cv2', 'torch', 'whisper'],
            'includes': ['tkinter'],
            'resources': ['assets'],
            'iconfile': 'assets/icon.icns',
            'plist': {
                'CFBundleName': "竹影",
                'CFBundleDisplayName': "竹影",
                'CFBundleIdentifier': "com.钟智强.竹影",
                'CFBundleVersion': "1.0.0",
                'CFBundleShortVersionString': "1.0.0",
            }
        }
    }
)
