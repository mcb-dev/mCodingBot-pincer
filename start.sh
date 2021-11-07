if [[ -d .git ]]
then
    git pull
fi

python -m venv venv
venv/bin/pip install -U --target /home/container/venv/lib/python3.8/site-packages/ -r requirements.txt

cd /home/container/

venv/bin/pip install -e /home/container
/home/container/venv/bin/python /home/container/mcoding_bot/__main__.py
