source ~/OneDrive/sms2/sms/Scripts/activate
python ~/OneDrive/sms2/manage.py shell

python ~/OneDrive/sms2/manage.py makemigrations && python ~/OneDrive/sms2/manage.py migrate
python ~/OneDrive/sms2/manage.py check_permissions
from books.models import Profile
from django.contrib.auth.models import User
zzm = User.objects.get(username = "zzm")
Profile.objects.get(user = zzm)



p = Profile.objects.create(user = zzm,token=0)

pip install python-alipay-sdk --upgrade

pip freeze > requirements.txt

cd /home/zzm/sms && workon sms
sudo rm -r -f pathname

About Git:
pull:
git pull && sudo service apache2 restart    
loading last save:
git revert HEAD -m 'loading' && git push


remote ubuntu:
cd /home/zzm/sms && workon sms && python manage.py makemigrations && python manage.py migrate