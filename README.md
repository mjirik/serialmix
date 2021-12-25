# serialmix
Web application for audio mix control

# Install on Raspberry Pi 

```bash
sudo pip3 install flask_cors flask serial
git clone https://github.com/mjirik/serialmix.git
sudo cp serialmix/systemd/serialmix.service /lib/systemd/system/
sudo chmod 644 /lib/systemd/system/serialmix.service

sudo systemctl daemon-reload
sudo systemctl enable serialmix.service
```

Check the ip of the device and restarat
```bash
ifconfig
sudo reboot
```

after

Serial port message calculator
https://support.biamp.com/Audia-Nexia/Control/Audia-Nexia_command_string_calculator?fbclid=IwAR2jkVR19XUBua7yoSb9My9W9Np6GKJOU8cXyc6UaRtSI1RSVpYwiWMZB0w