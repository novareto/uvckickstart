sudo apt-get install python-dev python-virtualenv python-setuptools subversion git libxml2-dev libssl-dev libxslt1-dev git libreadline-dev wv poppler-utils libjpeg62-dev build-essential
virtualenv playground vim
playground/bin/easy_install -f http://dev.bg-kooperation.de/pypi/simple uvckickstart

pp=${PWD}/playground/bin
export PATH="$pp:$PATH"
