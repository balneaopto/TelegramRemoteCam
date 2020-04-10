# Remote cam with Telegram

Connect one or more webcams to your Raspberry (or any PC with Linux distro), download this simple project, and you will be able to get snapshots from inside your home directly on your phone from anywhere.


### Prerequisites
* Python 3.5+
* Create your personal Telegram bot with BotFather.  
* telegram-send. See https://pythonhosted.org/telegram-send/.
```
sudo pip3 install telegram-send
```

### Usage

In config.py set the time interval between two snapshots.
The bash script remotecam.sh runs remotecam3x.py as daemon / service, with usual parameters:
```
./remotecam.sh start, stop, status
```
You can activate the remote control by running the bash script go.sh
```
go.sh
```
on your Raspberry at startup. The daemon starts; after a time interval set by user, the daemon stops and a command safely shut down your Raspberry.

In order to run this bash script on your Raspberry at startup:
```
sudo nano /home/pi/.bashrc
```
Go to the last line of the script and add:
```
remotecam/go.sh
```
