# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src/frontend_build/mainwindow.py'],
    pathex=['./src/'],
    binaries=[],
    datas=[('src/frontend_build', 'frontend_build')],
    hiddenimports=[],
    hookspath=['./hooks/'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='FocalAI',
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
)
