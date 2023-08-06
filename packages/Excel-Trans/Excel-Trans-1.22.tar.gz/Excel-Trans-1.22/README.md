## Excel_Trans

Developed by Quvonchbek Bobojonov (c) 2022

## Examples of How To Use (Buggy Alpha Version)

Uzbek Translate

```python
from Excel_Trans import Translator

trans = Translator()

#Uzbek Translate

trans.UzbekTranslate(file='test.xlsx', to_variant='latin', save_file='test1.xlsx')

#['latin','cyrillic']

```

Global Translate
```python
from Excel_Trans import Translator
trans = Translator()

#Global Translate

trans.GlobalTranslate(file='test.xls', target='ru', save_file='test1.xlsx')

#get supported languages

trans.get_supported_languages(as_dict=True)

```

