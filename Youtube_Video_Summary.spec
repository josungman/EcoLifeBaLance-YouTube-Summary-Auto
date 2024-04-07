# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['Main\\Auto_Main_job.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\SungmanCho\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\site-packages\\autoit\\lib\\AutoItX3_x64.dll', './autoit/lib')],
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
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Youtube_Video_Summary',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
