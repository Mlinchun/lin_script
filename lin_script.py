
import os
path = os.path.expanduser('~')

sppath = path + "/maya/scripts/xiaolin_script/__main__.py"
print(sppath)
exec(compile(open(sppath).read(), sppath , 'exec'))


