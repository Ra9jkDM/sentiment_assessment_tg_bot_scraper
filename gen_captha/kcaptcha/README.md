### install

sudo apt install php-common libapache2-mod-php php-cli
sudo apt install php8.*-gd # for images

### use
php -S localhost:9009 -t kcaptcha/
http://localhost:9009/index.php

http://localhost:9009/form_example.php

kcaptcha.php:49 - set static capcha