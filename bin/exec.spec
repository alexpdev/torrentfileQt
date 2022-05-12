# -*- mode: python ; coding: utf-8 -*-

block_cipher = None
import os
from os.path import join, dirname, relpath

assets = join(dirname(os.getcwd()), 'torrentfileQt', 'assets')
assets = os.path.relpath(assets,'.')
lst = []
for i in [os.path.join(assets,i) for i in os.listdir(assets)]:
    lst.append((i, 'torrentfileQt/assets'))

a = Analysis(['exec'],
             pathex=['../torrentfileQt'],
             binaries=None,
             datas=lst,
             hiddenimports=None,
             hookspath=[],
             hooksconfig={},
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
          name='torrentfileQt',
          icon='../assets/torrentfile.ico',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
