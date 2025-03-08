"""
Simple script to generate a PyInstaller spec file
"""

import os

# Get the current directory
current_dir = os.path.abspath(os.getcwd())

# Check if icon exists
icon_path = os.path.join(current_dir, 'timer_icon.ico')
if os.path.exists(icon_path):
    icon_option = f", icon=r'{icon_path}'"
    print(f"Using icon: {icon_path}")
else:
    icon_option = ""
    print("No icon file found")

# Create the spec file content
spec_content = f"""# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['sans_timer.py'],
    pathex=[r'{current_dir}'],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={{}},
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
    entitlements_file=None{icon_option}
)
"""

# Write the spec file
with open('simple.spec', 'w') as f:
    f.write(spec_content)

print("Created simple.spec file")
print("You can now run: pyinstaller --clean simple.spec") 