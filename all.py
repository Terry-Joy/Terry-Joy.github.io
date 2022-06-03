import os

os.system('git pull')
os.system('git add .')
os.system('git commit -m "update"')
os.system('hexo clean && hexo g && hexo d')
os.system('git push')
