# -*- mode: python ; coding: utf-8 -*-
import os
import sys

# Determine the base directory for the application
try:
    # When running as a script
    if '__file__' in globals():
        basedir = os.path.dirname(os.path.abspath(__file__))
    # When running as frozen executable
    elif getattr(sys, 'frozen', False):
        basedir = os.path.dirname(sys.executable)
    # When running directly with PyInstaller
    else:
        basedir = os.path.abspath(os.getcwd())
except Exception:
    # Fallback to current directory
    basedir = os.path.abspath(os.getcwd())

# Check if icon exists
icon_file = os.path.join(basedir, 'timer_icon.ico')
if not os.path.exists(icon_file):
    icon_file = None
    print("Warning: timer_icon.ico not found. The executable will use the default icon.")
else:
    print(f"Using icon file: {icon_file}")

block_cipher = None

a = Analysis(
    ['sans_timer.py'],
    pathex=[basedir],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(
    a.pure, 
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SANS_Timer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_file,
) 