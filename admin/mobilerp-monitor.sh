export PATH="/home/mobilerp/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

SOFTWARE_PATH='/home/mobilerp/mobilerp-server/'

echo 'Software Path set at' $SOFTWARE_PATH

echo 'Setting environment...'
cd $SOFTWARE_PATH
echo 'Launching app...'
pyenv activate env && python app.py

