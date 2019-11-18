CREATE USER 'www'@'%' IDENTIFIED WITH mysql_native_password BY '$3cureUS';
CREATE DATABASE cs4260;
GRANT ALL ON cs4260.* to 'www'@'%';