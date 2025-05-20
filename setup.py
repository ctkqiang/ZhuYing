from setuptools import setup

APP = ["main.py"]
DATA_FILES = [
    ("assets", ["assets/icon.png"]),
    (
        "src",
        ["src/translator.py", "src/video_processing.py", "src/database_handler.py"],
    ),
]
OPTIONS = {
    "argv_emulation": False,
    "packages": ["cv2", "sv_ttk", "PIL", "tkinter"],
    "includes": ["PIL", "cv2", "sv_ttk", "tkinter", "threading"],
    "excludes": ["matplotlib", "numpy", "pandas"],
    "iconfile": "assets/icon.icns",
    "plist": {
        "CFBundleName": "ZhuYing",
        "CFBundleDisplayName": "ZhuYing",
        "CFBundleGetInfoString": "Video Transcription Tool",
        "CFBundleVersion": "1.0.0",
        "CFBundleShortVersionString": "1.0.0",
    },
    "resources": ["assets", "src"],
    "site_packages": True,
    "optimize": 2,
    "arch": "x86_64",
    "strip": False,
    "prefer_ppc": False,
}

setup(
    app=APP,
    name="ZhuYing",
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
