sudo apt-get install python-dev python-virtualenv python-setuptools subversion git libxml2-dev libssl-dev libxslt1-dev git libreadline-dev wv poppler-utils libjpeg62-dev build-essential
virtualenv playground
playground/bin/easy_install -f http://dev.bg-kooperation.de/pypi/simple uvckickstart

pp=${PWD}/playground/bin
echo $pp
PATH=$pp:$PATH
echo $PATH
export PATH
