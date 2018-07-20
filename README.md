Dovecot
=========

Simple role for configuring Dovecot pop3/imap server on ubuntu xenial and centos 7.

With this role you can configure Dovecot in sorts of ways: 

* simple dovecot with pam authentication
* Dovecot with sql authentication and service.
* Dovecot with quota
* Dovecot with sieve and managesieve

**warning: Some part of role like sieve and managesieve not fully tested. Be careful**

## To Do

* add ldap authentication support
* add custom config documentation

Requirements
------------

#### Ubuntu:
**The below requirements are needed on the host that executes this module.**
* python
* python-apt

Role Variables
--------------

If you dont change any variable dovecot will configured with simple pam authentication looking for mails in /var/mail/%u.

|  name | default | description | acceptable values |
|---|---|---|---|
| dovecot_local_auth_enable |  yes | enable pam authentication |   |
| dovecot_local_userdb_disable |  no | disable pam userdb. this is useful when you want use static userdb |   |
| dovecot_pop_enable |  yes | enable dovecot pop3 protocol |   |
| dovecot_imap_enable |  yes | enable dovecot imap protocol |   |
| dovecot_ssl_enable |  no | enable SSL |   |
| dovecot_ssl_cert |  /etc/ssl/certs/ssl-cert-snakeoil.pem | path to SSL certificate. (**default value is not valid in Centos**) |   |
| dovecot_ssl_key |  /etc/ssl/private/ssl-cert-snakeoil.key | path to SSL private key. (**default value is not valid in Centos**) |   |
| dovecot_sql_auth_enable |  no | enable sql authentication |   |
| dovecot_sql_userdb_disable |  no | disable pam userdb. this is useful when you want use static userdb |   |
| dovecot_sql_driver |  mysql | sql driver | mysql, sqlite, postgres |
| dovecot_sql_host |  localhost | database hostname address. in case of sqlite this variable should be path to sqlite database file |   |
| dovecot_sql_port |  '3306' | sql database port |   |
| dovecot_sql_user |  dovecot | udatabase username |   |
| dovecot_sql_password |  dovecot | database password |   |
| dovecot_sql_database |  vmail | database name |   |
| dovecot_sql_user_query |  SELECT home, uid, gid FROM users WHERE username = '%n' AND domain = '%d' | query used to retrive user data.  |   |
| dovecot_sql_password_query |  SELECT password FROM users WHERE username = '%n' AND domain = '%d' | query used to check password of user. see [dovecot sql authdatabase](https://wiki2.dovecot.org/AuthDatabase/SQL) |   |
| dovecot_sql_iterate_query |  SELECT home, uid, gid FROM users WHERE username = '%n' AND domain = '%d' |   |   |
| dovecot_sql_default_pass_scheme |  PLAIN | schema of saved passwords |   |
| dovecot_static_userdb_enable |  no | enable static user database |   |
| dovecot_static_userdb_home |  /var/mail/virtual/%Ld/%Ln | static userdb home  |   |
| dovecot_static_userdb_mail |  "~/Mail" | path of static users mailbox |   |
| dovecot_auth_service_enable |  no | enable dovecot auth service |   |
| dovecot_auth_service_path |  /var/spool/postfix/private/dovecot-auth | auth service socket path |   |
| dovecot_auth_service_mode | "0660" | auth service socket file mode |  |
| dovecot_auth_service_user |  postfix | auth service socket owner |   |
| dovecot_auth_service_group |  postfix | auth service socket group |   |
| dovecot_lmtp_service_enable |  no | enable dovecot lmtp (server) service |   |
| dovecot_lmtp_postmaster | root@localhost | postmaster address |  |
| dovecot_lmtp_service_path |  /var/spool/postfix/private/dovecot-lmtp | lmtp service socket path |   |
| dovecot_lmtp_service_mode |  "0660" | lmtp socket file mode |   |
| dovecot_lmtp_service_user |  dovecot | lmtp socket file owner  |   |
| dovecot_lmtp_service_group |  postfix | lmtp socket file group |   |
| dovecot_quota_enable |  no | enable dovecot quota |   |
| dovecot_quota_driver |  file | dovecot quota backend |   |
| dovecot_quota_storage_limit |  10M | quota storage limit |   |
| dovecot_quota_messages_limit |  1000 | quota message limit |   |
| dovecot_quota_sql_path |  /etc/dovecot/quota-dict.conf | path of sql file for quota.**You probably does need to change this** |   |
| dovecot_quota_sql_table |  quota | name of quota table in database |   |
| dovecot_quota_grace_enable | yes | enable quota grace. default is true but it only enabled with quota itself |  |
| dovecot_quota_grace_percent |  10 | quota grace percent |  |
| dovecot_quota_service_enable |  yes | enable quota grace service. |   |
| dovecot_quota_service_port |  12302 | quota grace service port |   |
| dovecot_quota_service_client_limit |  1 | quota grace service client limit |   |
| dovecot_sieve_enable |  no | enable sieve |   |
| dovecot_managesieve_enable |  yes | enable managesieve server |   |
| dovecot_sieve_script_max_size |  1M | dovecot managesive max script size |   |


Example Playbook
----------------

#### example 1:

```yaml
---
# simple dovecot pop3/imap configuration
- hosts: mail
  roles:
    - role: ghobadimhd.dovecot
```
#### example 2:

dovecot with only sql authentication that revieve mail through dovecot lmtp service with quota enabled.

default configuration use database named *vmail* that contains *users* table like below.

sql:
```sql
create table if not exists users  (
  id int,
  username nvarchar(80),
  domain nvarchar(80),
  password nvarchar(512),
  uid int NULL,
  gid int NULL,
  home nvarchar(500) NULL
);
CREATE TABLE quota (
  username varchar(100) not null,
  bytes bigint not null default 0,
  messages integer not null default 0,
  primary key (username)
);
grant all on vmail.* to 'dovecot'@'localhost' identified by 'dovecot' ;


```
playbook.yml:

```yaml
---
- hosts: mail
  roles:
    - role: ghobadimhd.dovecot
      dovecot_local_auth_enable: no
      dovecot_sql_auth_enable: yes
      dovecot_lmtp_service_enable: yes
      dovecot_quota_enable: yes
      dovecot_quota_driver: sql

```
License
-------

MIT

Author Information
------------------

Mohammad Ghobadi

Email: ghobadimhd@gmail.com
