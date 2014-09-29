# -*- mode: python -*-
a = Analysis(['recipes.py'],
             pathex=['/home/dan/Dropbox/programs/python/recipes'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='recipes',
          debug=False,
          strip=None,
          upx=True,
          console=False )
a.datas+=[("database.db",'/home/dan/Dropbox/programs/python/recipes/database.db', 'DATA')]
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='recipes')
