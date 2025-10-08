import os
from pathlib import Path
p = Path(r'd:/lab2_25099433g/database/app.db')
d = p.parent
print('Database dir:', d)
print('Files before:')
for f in d.iterdir():
    try:
        print(f.name, f.stat().st_size)
    except Exception:
        print(f.name, '?')

bak = p.with_suffix(p.suffix + '.bak')
if p.exists():
    if not bak.exists():
        p.rename(bak)
        print(f'Renamed {p.name} to {bak.name}')
    else:
        print(f'Backup already exists: {bak.name}')
else:
    print('No app.db found to backup')

# create an empty app.db (zero bytes) to ensure code reading the file gets an empty DB
p.touch()
print('Created empty', p.name)

print('\nFiles after:')
for f in d.iterdir():
    try:
        print(f.name, f.stat().st_size)
    except Exception:
        print(f.name, '?')
