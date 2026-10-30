from pathlib import Path
from urllib.request import Request, urlopen
from concurrent.futures import ThreadPoolExecutor
import re, shutil

root=Path(__file__).parent/'dist'/'assets'
(root/'icons').mkdir(exist_ok=True)
def download(url, target):
    req=Request(url,headers={'User-Agent':'Mozilla/5.0'})
    with urlopen(req,timeout=40) as r: target.write_bytes(r.read())
    return target.name
icons={'aws':'amazonwebservices/amazonwebservices-original.svg','terraform':'terraform/terraform-original.svg','ansible':'ansible/ansible-original.svg','docker':'docker/docker-original.svg','kubernetes':'kubernetes/kubernetes-original.svg','linux':'linux/linux-original.svg','githubactions':'githubactions/githubactions-original.svg','jenkins':'jenkins/jenkins-original.svg','gitlab':'gitlab/gitlab-original.svg','prometheus':'prometheus/prometheus-original.svg','grafana':'grafana/grafana-original.svg','nginx':'nginx/nginx-original.svg','python':'python/python-original.svg','bash':'bash/bash-original.svg','java':'java/java-original.svg','spring':'spring/spring-original.svg','git':'git/git-original.svg','postgresql':'postgresql/postgresql-original.svg'}
with ThreadPoolExecutor(max_workers=8) as pool:
    jobs=[pool.submit(download,'https://raw.githubusercontent.com/devicons/devicon/master/icons/'+p,root/'icons'/f'{n}.svg') for n,p in icons.items() if not (root/'icons'/f'{n}.svg').exists()]
    for job in jobs: print(job.result())
fonts=[('Manrope:wght@200..800','manrope.woff2'),('Instrument+Serif:ital@1','instrument-serif-italic.woff2'),('IBM+Plex+Mono','plex-mono.woff2')]
for family,name in fonts:
    req=Request('https://fonts.googleapis.com/css2?family='+family+'&display=swap',headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})
    css=urlopen(req,timeout=40).read().decode()
    urls=re.findall(r'url\((https://[^)]+)\)',css)
    download(urls[-1],root/name)
    print(name)
sources=[('EN','4e1993a8-cf53-4750-83f5-f0d539b71ef8'),('FR','0e40db4a-0179-4a66-aea9-da53bf80c947')]
for lang,folder in sources:
    source=Path('C:/Users/Utilisateur/.codex/attachments')/folder/'Texte collé.txt'
    target=root/f'Anas-Gara-CV-{lang}.tex'
    if not target.exists():
        shutil.copyfile(source,target)
print('All static assets ready')

