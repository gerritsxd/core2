### In Plesk, execute with:
### bash _deploy.sh >> deployment.log 2>&1
### Cran job for executing every hour with logging
### @hourly bash ~/deploy_stab.opens.science/deploy.sh >> ~/deploy_stab.opens.science/deployment.log 2>&1
### https://www.cyberciti.biz/faq/how-do-i-add-jobs-to-cron-under-linux-or-unix-oses/
### To edit the cron file with nano instead of vim:
### export VISUAL=nano; crontab -e

echo - - - STARTING DEPLOYMENT SCRIPT at $(date) - - -

echo Setting variables:

quartoDir = "/usr/local/bin/quarto"
extraPathDirs = "/opt/plesk/phpenv/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin"
httpDir = "~/httpdocs"
renderDir = "public"
repoDir = "core"
deployDir = "~/deploy_core"

echo quartoDir = $quartoDir
echo extraPathDirs = $extraPathDirs
echo httpDir = $httpDir
echo renderDir = $renderDir
echo repoDir = $repoDir
echo deployDir = $deployDir

PATH=$PATH:$extraPathDirs

echo Updated $PATH to also include $extraPathDirs

### Go to directory with cloned git repo
cd $deployDir

echo Running Quarto in deployment directory $deployDir...

### Render the site
if $quartoDir render; then

# https://unix.stackexchange.com/questions/22726/how-to-conditionally-do-something-if-a-command-succeeded-or-failed

  echo Done with Quarto. Deleting old directories and files from $httpDir...
  
  ### Delete all contents in public HTML directory
  rm -rf $httpDir/*.*
  rm -rf $httpDir/*
  #rm -f $httpDir/.htaccess
  rm -f $httpDir/$repoDir/.htaccess
  
  echo Done deleting old directories and files. Copying over new website from $deployDir/$renderDir to $httpDir...
  
  ### Copy website: "httpdocs" should be changed to
  ### the directory the website is served from
  cp -RT $renderDir $httpDir
  
  ### Copy .htaccess
  #cp .htaccess ~/comms.opens.science/core
  cp $repoDir/.htaccess $httpDir/$repoDir

  echo Done copying over new website.

else

  echo ERROR: Quarto failed, doing nothing!

fi

echo - - - ENDING DEPLOYMENT SCRIPT at $(date) - - -
