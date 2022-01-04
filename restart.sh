#!/bin/bash

sudo systemctl stop serialmixrest.service
sudo systemctl stop serialmixweb.service
sudo systemctl start serialmixrest.service
sudo systemctl start serialmixweb.service
