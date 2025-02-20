#!/bin/bash
set -e

# Configuration
APP_NAME="竹影"
VERSION="1.0.0"

# Clean previous builds
echo "清理旧构建..."
rm -rf build dist

# Build using spec file
echo "构建应用程序..."
pyinstaller --clean 竹影.spec

# Create DMG
if [ -d "dist/${APP_NAME}.app" ]; then
    echo "创建 DMG 安装包..."
    create-dmg \
        --volname "${APP_NAME} Installer" \
        --volicon "assets/icon.icns" \
        --window-pos 200 120 \
        --window-size 800 400 \
        --icon-size 100 \
        --icon "${APP_NAME}.app" 200 190 \
        --hide-extension "${APP_NAME}.app" \
        --app-drop-link 600 185 \
        "dist/${APP_NAME}-${VERSION}.dmg" \
        "dist/${APP_NAME}.app"
fi
