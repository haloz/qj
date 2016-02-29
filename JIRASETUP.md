JIRA OAuth setup
=================
> This describes how to enable an application like a python script to access a JIRA instance using OAuth authentication.


JIRA & keys
---------------
> Create an application link in JIRA and generate the needed private/public key pair

* Create a new JIRA user. This user will be used for the application to access JIRA.

* Login as a JIRA admin

* Go to Administration / Applications / Integrations / Application links

* Add a new application link with a fake URL (as we won't do any outside connections to the application, JIRA will just receive access from the application). Example: http://127.0.0.1/queryjira

* Ignore the "No response was received from the URL you entered" warning and hit Continue

* Application name is just a name of your choice for your app. Example: queryjira

* Application Type: Generic Application

* Leave all other fields here empty. But check the "Create incoming link" option. Then hit continue

* Enter a comsumer key. This is basically a unique name of the application to access JIRA. The oauth dance of the application has to use the same consumer key - for example via jirashell.py. Example: queryjira

* Consumer Name: A string with the name of the consumer application. Example: John's Query JIRA Script

* public key: this is the PUBLIC (.pub) key of a generated openssh key pair. This can be created via the openssl command line (I did this with my unbuntu 15.10 Virtualbox VM):

```
openssl genrsa -out privkey.pem
openssl rsa -pubout -in privkey.pem -out pubkey.pem
cat pubkey.pem
```

Copy the public key into the Public Key field in the JIRA's Link applications dialog. I tried to do this using puttygen but it won't accept the key :/

* The application link should be created. Click on Edit and go to incoming Authentication. Unfortunately we can't edit the settings here, so click on Delete. Enter the data again for Consumer Key (queryjira), Consumer Name (John's Query JIRA Script) and the Public Key. Make sure you check the "Allow 2-Legged OAuth" option. In the "Execute as" field use the username of the user you specifically created for the application access.



jirashell.py
---------------
> jirashell.py cares for the "oauth" dance to estiablish & accept the connection and gets you the access tokens

* Next you need jirashell.py. You can find it in jira/jirashell.py of the github repo: https://github.com/pycontribs/jira.git. To get it installed you need a hell lot of pip modules beforehand:

```
pip install pycrypto
(for Windows try this as binary: https://github.com/sfbahr/PyCrypto-Wheels)

pip install winrandom
(only for Windows. You might need this workaround: http://www.devdungeon.com/content/installing-pycryptoparamiko-python3-x64-windows)

pip install jwt
pip install pyjwt
pip install cryptography
pip install IPython

pip install -e .
(in the pycontribs/jira directory - main directory of the git clone)
```

* Fire up jirashell.py:

```
python jirashell.py -s http://192.168.3.14:8080 -od -ck queryjira -k C:\path\to\oauth-keys\jira.ppk -pt
```

Where http://192.168.3.14:8080 is the URL to your JIRA installation and the jira.ppk is the PRIVATE key of the key pair you created above via openssl genrsa

* The jirashell.py should output some request tokens:

```
Request token:        XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
Request token secret: YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY
```

* jirashell will also prompt you with

```
Please visit this URL to authorize the OAuth request:
http://192.168.3.14:8080/plugins/servlet/oauth/authorize?oauth_token=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

Put this URL on in your browser and push accept. The return to the jirashell and answer with "y" for the question there "Have you authorized this program to connect on your behalf to..."

* You should get the access tokens:

```
Access tokens received.
    Access token:        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    Access token secret: BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
```

* We're in IPython shell on the JIRA server. Try to create a JIRA ticket with your Webbrowser and give it a summary (=ticket name). Then access it in the shell:

ABC-1 is your ticket key. The shell should output the summary of the ticket :)

```
issue = jira.issue('ABC-1')
issue.fields.summary
```


Ready!
---------------
> Now you can use the jira ("jira-python") package to write a scripts for automated JIRA queries. The workflow is described here: http://skjira.readthedocs.org/en/latest/quickstart.html#authentication



Sources
---------------
* JIRA documentation "Allowing OAuth Access" https://confluence.atlassian.com/jira/allowing-oauth-access-200213098.html#AllowingOAuthAccess-issuingaccesstokens
* JIRA REST API example https://developer.atlassian.com/jiradev/jira-apis/jira-rest-apis/jira-rest-api-tutorials/jira-rest-api-example-oauth-authentication
* jirashell source https://github.com/pycontribs/jira/blob/master/jira/jirashell.py
* workaround for Windows to get pycrypto package to find winrandom http://www.devdungeon.com/content/installing-pycryptoparamiko-python3-x64-windows
* jira python package documentation http://skjira.readthedocs.org/
* pycrypto binaries for Windows https://github.com/sfbahr/PyCrypto-Wheels