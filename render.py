from jinja2 import Template, FileSystemLoader
from jinja2.environment import Environment
from shutil import copyfile
import os
import json
from collections import OrderedDict

# Create the build dir if it does not exist.
if not os.path.exists('build'):
    os.makedirs('build')

# Copy static files.
copyfile('style.css',os.path.join('build', 'style.css'))
copyfile('hciLogoSmall.png',os.path.join('build', 'hciLogoSmall.png'))

# Load the repos db.
repo_db = json.load(open('repo_db.json','r'))
repo_db = OrderedDict(sorted(repo_db.items()))

# Load authors db.
auth_db = json.load(open('authors_db.json','r'))

# Render the references.
refs_counter = 0
for _ in repo_db:
    if 'refs' in repo_db[_]:
        repo_db[_]['refs'] = [r'<a href="' + ref[1] + r'">[' + str(ref[0]) + r']</a>' for ref in enumerate(repo_db[_]['refs'],refs_counter)]
        refs_counter += len(repo_db[_]['refs'])

# Render authors.
for _ in repo_db:
    repo_db[_]['authors'] = [a if (not a in auth_db or a == 'others') else r'<a href="' + auth_db[a] + r'">' + a + r'</a>' for a in repo_db[_]['authors']]
    if 'others' in repo_db[_]['authors']:
        repo_db[_]['authors'].remove('others')
        repo_db[_]['authors'].append('others')

env = Environment()
env.loader = FileSystemLoader('.')

def render(name,**kwargs):
    filename = name+'.html'
    open(os.path.join('build', filename),'w').write(env.get_template(filename).render(**kwargs))

render('index', repo_db=repo_db)
render('repos', repo_db=repo_db, auth_db=auth_db)
