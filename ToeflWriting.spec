# -*- mode: python -*-

block_cipher = None


a = Analysis(['ToeflWriting.py'],
             pathex=['D:\\Desktop\\Web\\mobile\\git\\rgap_toefl_writing'],
             binaries=[],
             datas=[],
             hiddenimports=['wx._html', 'wx._xml'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='ToeflWriting',
          debug=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='ToeflWriting')
