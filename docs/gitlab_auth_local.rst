GITLAB AUTH
===========

1. Create .env file with `ZOO_GITLAB_URL=https://gitlab.com/`
2. Go to https://gitlab.com/ -> Settings -> Applications
3. Create an application with:
	- read_user scope
	- redirect uri - http://localhost:20966/accounts/gitlab/login/callback/
4. Copy client id and secret
5. Go to http://localhost:20966/admin
6. Go to `Site` model and set `Domain name` to `localhost`
7. Go to `Social Applications` and create an entry for Gitlab with client id and secret
8. Profit





