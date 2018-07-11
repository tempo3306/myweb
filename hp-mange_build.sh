cd /home/zs/Projects/myweb/hp-manage
npm run build

cd /home/zs/Projects/myweb
 /home/zs/.pyenv/shims/python manage.py collectstatic --no-input
sudo supervisorctl reload
