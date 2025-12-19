```cd "C:\Users\riche\Desktop\Abdelrahim\QIX\avant"; mprof run -o "..\stats\avant\mprofile.dat" --include-children python .\QIX_Raphael_DAVIOT_Nael_AIT_AISSI.py```
```cd "C:\Users\riche\Desktop\Abdelrahim\QIX"; python -c "from pathlib import Path; import statistics; p=Path(r'C:\\Users\\riche\\Desktop\\Abdelrahim\\QIX\\stats\\avant\\mprofile.dat'); s=p.read_text(); vals=[float(l.split()[1]) for l in s.splitlines() if l.startswith('MEM')]; print('samples',len(vals)); print('max',max(vals)); print('mean',statistics.mean(vals)); print('last',vals[-1])"```

### Résultat
```samples 216
max 57.050781
mean 50.07049312962963
last 51.097656
```


```cd "C:\Users\riche\Desktop\Abdelrahim\QIX\après"; mprof run -o "..\stats\après\mprofile_apres.dat" --include-children python .\QIX_Raphael_DAVIOT_Abdelrahim_RICHE.py```
```cd "C:\Users\riche\Desktop\Abdelrahim\QIX"; python -c "from pathlib import Path; import statistics; p=Path(r'C:\\Users\\riche\\Desktop\\Abdelrahim\\QIX\\stats\\après\\mprofile_apres.dat'); s=p.read_text(); vals=[float(l.split()[1]) for l in s.splitlines() if l.startswith('MEM')]; print('samples',len(vals)); print('max',max(vals)); print('mean',statistics.mean(vals)); print('last',vals[-1])"```

### Résultat
```samples 126
max 48.789062
mean 42.83937861111111
last 44.152344
```

