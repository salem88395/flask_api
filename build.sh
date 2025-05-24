#!/bin/bash

# تحديث النظام وتثبيت المتطلبات
apt-get update
apt-get install -y curl gnupg apt-transport-https

# إضافة مستودع Microsoft
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/debian/12/prod.list > /etc/apt/sources.list.d/mssql-release.list

# تحديث وتثبيت ODBC Driver 17
apt-get update
ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev
