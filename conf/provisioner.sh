if ! grep -q "cd /vagrant" ~/.bashrc ; then 
    echo "cd /vagrant/repository" >> ~/.bashrc 
fi 