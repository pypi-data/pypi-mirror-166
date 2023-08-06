# Mastodonplus.py  
Fork of Python wrapper for the Mastodon (<https://github.com/tootsuite/mastodon/> ) API.  
The goal of this fork is to add all 'new' Mastodon API's endpoints to the excellent [halcy's wrapper](https://github.com/halcy/Mastodon.py).

#### Register your app! This only needs to be done once. Uncomment the code and substitute in your information.

```
from mastodon import Mastodon

Mastodon.create_app(
	'pytooterapp',
	api_base_url = 'https://your-mastodon.server'
	to_file = 'pytooter_clientcred.secret'
	)
```
#### Then login. This can be done every time, or use persisted.  

```
from mastodon import Mastodon

mastodon = Mastodon(
	client_id = 'pytooter_clientcred.secret',
	api_base_url = 'https://your-mastodon.server'
	)  
mastodon.log_in(  
	'my_login_email@example.com',  
	'incrediblygoodpassword',  
	to_file = 'pytooter_usercred.secret'
	)
```  
#### To post, create an actual API instance.  

```
from mastodon import Mastodon  

 mastodon = Mastodon(  
	access_token = 'pytooter_usercred.secret',  
	api_base_url = 'https://your-mastodon.server>'  
	)  
mastodon.toot('Tooting from python using #mastodonpy !')  
```  
You can install Mastodonplus.py via pypi:  

```
# Python 3
pip3 install Mastodonplus.py
```  
#### New features  
  
* 26.8.2022. Mastodon v3.5.x. Added New endpoints: /api/v1/admin/domain_blocks (list,show by id, delete and create)  
* 27.8.2022. Mastodon v3.1.4. Added 'remote" param to GET /api/v1/timelines/public REST API
* 27.8.2022. Mastodon v3.1.4. Added GET /api/v1/streaming/public/remote (Mastodon.stream_remote())
* 06.9.2022. Mastodon v3.2.0. Added POST /api/v1/accounts/:account_id/note with comment param. (Mastodon.accounts_note(id=account_id, comment='comment')
* 06.9.2022. Mastodon v3.5.x. Added GET /api/v1/admin/ip_blocks (Mastodon.admin_ip_blocks_list(max_id=None, min_id=None, since_id=None, limit=None)
* 06.9.2022. Mastodon v3.5.x. Added DELETE /api/v1/admin/ip_blocks/:id (Mastodon.admin_ip_blocks_delete(id=None)
* 06.9.2022. Mastodon v3.5.x. Added POST /api/v1/admin/ip_blocks (Mastodon.admin_ip_blocks_create(self, ip=None, severity=None, comment=None, expires_in=None)  
		severity possible values:
+            		sign_up_requires_approval
+            		sign_up_block
+            		no_access
