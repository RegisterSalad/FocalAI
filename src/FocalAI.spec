# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['frontend_build/mainwindow.py'],
             pathex=['.'],
             binaries=[],
             datas=[],
             hiddenimports=[
                 'api_caller',
                 'conda_env',
                 'database',
                 'database_util',
                 'GPT_caller',
                 'repo',
                 'secret',
                 'frontend_build.adapter',
                 'frontend_build.file_drop_widget',
                 'frontend_build.file_list_widget',
                 'frontend_build.installed_window',
                 'frontend_build.install_page',
                 'frontend_build.menu_bar',
                 'frontend_build.model_page',
                 'frontend_build.model_player',
                 'frontend_build.model_uis',
                 'frontend_build.script_builder',
                 'frontend_build.styler',
                 'frontend_build.terminal_widget',
                 'frontend_build.vertical_menu',
                 'frontend_build.worker'
             ],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='FocalAI',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,  # Change to False if you don't want a console window
          icon=None)

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='FocalAI')