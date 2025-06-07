### In Plesk, execute with:
### bash _deploy.sh >> deployment.log 2>&1
### Cran job for executing every hour with logging
### @hourly bash ~/deploy_stab.opens.science/deploy.sh >> ~/deploy_stab.opens.science/deployment.log 2>&1
### https://www.cyberciti.biz/faq/how-do-i-add-jobs-to-cron-under-linux-or-unix-oses/
### To edit the cron file with nano instead of vim:
### export VISUAL=nano; crontab -e

echo ----------
echo $(date)

PATH=$PATH:/opt/plesk/phpenv/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin

### Go to directory with cloned git repo
cd ~/deploy_core

echo Running Quarto...

### Render the site
if /usr/local/bin/quarto render; then

# https://unix.stackexchange.com/questions/22726/how-to-conditionally-do-something-if-a-command-succeeded-or-failed

  echo Done with Quarto. Deleting old directories and files...
  
  ### Delete all contents in public HTML directory
  rm -rf ~/core/*.*
  rm -rf ~/core/*
  #rm -f ~/core/.htaccess
  rm -f ~/core/core/.htaccess
  
  echo Done deleting old directories and files. Copying over new website...
  
  ### Copy website
  cp -RT public ~/core
  
  ### Copy .htaccess
  #cp .htaccess ~/comms.opens.science/core
  cp core/.htaccess ~/core/core

  echo Done copying over new website.

else

  echo ERROR: Quarto failed, doing nothing!

fi

echo ----------
