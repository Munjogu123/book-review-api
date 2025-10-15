#!/bin/bash

apt update -y
apt install -y postgresql postgresql-contrib
systemctl start postgresql
systemctl enable postgresql
