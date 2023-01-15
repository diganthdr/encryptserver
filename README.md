[![crypto-server pipeline](https://github.com/woven-planet-security-hiring/diganthdr-dast-challenge/actions/workflows/python-app.yml/badge.svg)](https://github.com/woven-planet-security-hiring/diganthdr-dast-challenge/actions/workflows/python-app.yml)

# Crypto server

## Introduction
Crypto server helps to encrypt and decrypt text files. It also can generate hash for a given password string.
A CLI provides interface to access services

## Services
- Encryption
- Decryption
- Password hashing

### Limitations, constraints
- Currently only text files are supported for encryption.
  Note that, text files with extention '.txt' are supported. Autodetection based on MIME types will be supported in https://github.com/woven-planet-security-hiring/diganthdr-dast-challenge/issues/30
- Maximum size of text file is 10MB for encryption.
- Max length of password for hashing supported is 20 chars.<br>
  (_Decision is based on an article which indicates an average password length is about 9.6 chars long https://resources.infosecinstitute.com/topic/beyond-password-length-complexity/_)

## Design

### Server design
![alt text](https://github.com/woven-planet-security-hiring/diganthdr-dast-challenge/blob/main/crypto%20server%20design.001.jpeg)

#### Design choices
1. Single process server
2. Multiple process or async server

It makes sense for second option because, server can get busy and subsequent requests have to wait until the request is served. In order to support multiple requests at a time, worker processes are created. These worker processes pick up task from task queue and work in the background. Client queries the job for completion.

File name collision problem: It is natural for client users to automate CLI in thier workflow. There could be collisions when multiple users/CLIs upload file with same filename. To takle this, every file is saved at server with timestamp suffix (can be changed to even robust, UUID instead of timestamp) and processed further.

So, three processes make up a a complete working server.
1. Applicaition server (Python flask framework)
2. Task queue (Redis server. Which has in memory no-sql database which can be leveraged as queue)
3. Worker processes (Celery library)


### CLI Client design
![alt text](https://github.com/woven-planet-security-hiring/diganthdr-dast-challenge/blob/main/cli-server%20enc-dec%20workflow.001.jpeg)

CLI is wrapper around REST APIs exposed by server. It sends request for encryption/decryption to the server and waits (maximum 10 seconds) for response. 
However, for password hashing, it's immediate. As constraint for password is maximum 20 chars. Which should be processed quickly.

#### Design choices
1. Either wait until the job is finished. (blocking call, which can be annoying at times) or
2. Quickly exit with "PENDING" status if job is still going on.

Looking at an average time taken for a an average file size (around 100kB) to be encrypted/decrypted, it should take few seconds. 
So, it would be reasonable to combine both approaches. In future, command line args to _--nowait_ or _--wait_ to behave either way.

#### Error handling
Most of the errors/constraints are handled at server. However, it makes sense to have constraint _'file size check'_ at client as well because sending a file more than specified size would be redundant.

## Usage

### Setup and installation

#### Pre-requisite
- Python 3.9.4 (tested version)
- Install redis-server (needed for task queue)
    See installation on linux: https://redis.io/docs/getting-started/installation/install-redis-on-linux/
 
#### Installing source code 
- Download source code <br>
    `git clone https://github.com/woven-planet-security-hiring/diganthdr-dast-challenge.git`
    
#### Wheel installation (via .whl) _(Yet to be implemented)_ (See: https://github.com/woven-planet-security-hiring/diganthdr-dast-challenge/issues/20)
~~- Download <release>.whl~~
~~- pip install crypt.whl~~
  
### Bring up server
  cd into code root dir `cd diganthdr-dast-challenge`<br>
  1. run setup.sh which sets up libraries in virtual env and
  `source setup.sh`<br>
  2. run deploy.sh which spins up a server on port 5000 _(you can change if you want to see CONTRIBUTING.md)_
  
  One-liner : `cd diganthdr-dast-challenge && source setup.sh && source deploy.sh` 
  
  If server is already running, you can clean-up process before bringing it up using shutdown-server.sh script. <br>
  One-liner: `cd diganthdr-dast-challenge && source shutdown-server.sh && source setup.sh && source deploy.sh`
  
  Note: logs of these processes are are stored in root dir of code `ls --lrt` and look for `.log` files. They have obvious filenames.
  
  What happens when you run these commands is explained below in _"Steps to bring-up server"_ section. In case you want to run manually for some reason, you can follow the section.
  
### Shutdown server
  Kill processes which make up server. That is, redis-server, celery workers and application server<br>
  CAUTION: Make sure you do not have any of those processes running on your system already for some other purposes, then kill them manually.<br>
  `source shutdown-server.sh`
  
### Steps to bring-up server manually

1. Install required python libraries
  
    `pip install -r requirements.txt`
  
    Note: It is recomended to create python virual environment for isolated enviroment. Although not necessary<br>
    `python3 -m venv <any name for virtual env>`
        
2. Run redis server in the background or in separate terminal.<br>
   `redis-server` <br>
    It opens up port number 6397, make sure that is not already being used by any other process <br>
    Note: It can be run as service too. Please refer: _https://phoenixnap.com/kb/install-redis-on-ubuntu-20-04_
    
3. Run celery workers <br>
    ` cd server/src && celery -A celeryapp.celery  worker --loglevel=info & `
    
4. Bring up python application server<br>
    ` cd server/src && python3 server.py ` <br>
    default port is 5000 on localhost. To change host and port number use python3 server.py --host <ip> --port <port><br>
    Note: This spins up non-production server as of now. That should do the job as of now. In real prod environment, we put up actual wsgi.


### Command line interface, crypt-cli<br>
Basic command is <br> `crypto-api <operation> <filename_if_required_by_command> --server <server IP/hostname> --port <port number>`<br><br>
By default hostname is `localhost` port is set to `5000`. So, it can be used without --server and --port args if on localhost
    
#### Commands supported<br>
Note: Please cd in to client source dir (`cd client/src`) dir for accessing CLI. (At the moment it is not available globally, yet to add to PATH)<br>
- **Encryption**<br>
    _**./crypto-api --encrypt <filename>**_<br>
    Input: filename
    Output: encrypted file in current dir, with suffix '.encrypt' added.
    
    Common errors:
    - File not found
    - File too large
    - Only text files are supported.
    - Server unreachable 
    
    Example:<br>
    `./crypto-api --encrypt /home/projects/woven-planet/diganthdr-dast-challenge/LICENSE.txt` <br>
    A file named `LICENSE.txt.encrypt` gets saved in current working dir
    
- **Decryption**<br>
    _**crypto-api --decrypt <filename>**_ <br>
    Input: filename
    Output: decrypted file in current dir, with `.decrypt` suffix added.
    
    Example:<br>
    `./crypto-api --decrypt /home/projects/woven-planet/diganthdr-dast-challenge/LICENSE.txt.encrypt` <br>
    
    A file named `LICENSE.txt.encrypt.decrypt` gets saved in current working dir
    
- **Password hash**<br>
    _**crypto-api --password-hash <password>**_ <br>
    Input: password string (expected max 20 chars)
    Output: Hash string (binary string literal)
    
    Example:<br>
    `#./crypto-api --password-hash test@123
    {'hash': "b'hiLw9pyRgZEZqKz2CiSNezb9t8z4V7qPhc9/J2f/gmU='"}`
  
    
## Bug reporting<br>
  Please provide following information<br>  
  - release version
  - operation
  - result or errors seen
  - logs (client/src/crypto-client-cli.log)
  - optionally, include env info such as OS, environment variables (Since test is done on mac and ubuntu, this is TODO)

  
### email<br>
    bug-report@w-p.com
   
## Development notes
### Please refer CONTRIBUTING.md
   _ https://github.com/woven-planet-security-hiring/diganthdr-dast-challenge/blob/main/CONTRIBUTING.md_


## License
   MIT 
