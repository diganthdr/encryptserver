# How to contribute

## Download code
clone repository
`git clone https://github.com/woven-planet-security-hiring/diganthdr-dast-challenge.git`

since we are following trunk based development, feel free to make changes in 'main' branch.

## Create development environment:
### Install pre-requisites
1. Python 3.9.4 (tested version, should work for 3.7 to 3.9)
2. Install redis-server
   - On apt based linux(tesed on githubActions): `sudo apt update ; sudo apt install redis`
   - On Mac (tested): brew install redis<br>
   For moresee : https://redis.io/docs/getting-started/installation/
3. Create virtual env
  `python3 -m venv <env-name>` example, `python3 -venv wp-venv`
4. Activate virtual env
   `source <path_to_activate_script>`. Example `source /documents/projects/woven-planet/wp-venv/wp-venv/bin/activate`
5. Install required libraries
  `pip install requirements.txt`

run `setup.sh` which does steps #3 to #5

### Bring up server with prerequisites 'redis' and 'celery'

run `deploy.sh`, this brings up server and client
deploy.sh, does the same thing.

Refer README.md for one-liners to setup and bring up server.

### run tests
  - client unittest (sort of integration test, triggers actual server APIs)<br>
   `cd src/client; python -m unittest discover`
  - server unittest <br>
   `cd src/server; python -m unittest discover`

 
 ## Architecture/Design
  
   ![alt text](https://github.com/woven-planet-security-hiring/diganthdr-dast-challenge/blob/main/crypto-server-architecture.001.jpeg)
  
 ## Code dir structure.
 
    - client
        - src
           - (subdirs)
        - tests
             
    - server<br>
        - src
            - (subdirs)
        - tests
    - README.md
    - CONTRIBUTING.md
    - LICENSE.txt
    - setup.sh
    - deploy.sh
    - shutdown-server.sh
    - (other files)

  Thoughts: Initially, I had started with src/server and src/client with single test folder for both, but I thought it would be good idea to separate tests and code. Perhaps they get moved to different repos in future.
   
 ## Test strategy
 ### server tests
   
- server algo tests, 
   - encryption/decryption and 
   - hashing  
- server multiple clients/requests (send many cli requests, automation needed)
- server constraints test  (built to unittest of server)
- server stress test (yet to do)

 
 ### client tests
 - client code unittest (basic and corner tests)
 - client args test (#TODO. Yet to be done. since args are few, its is manually tested as of now. Feel free to contribute.)
 - client-server end to end integration test (uses unittest for simplicity)
 - utilities for testing: test file generation
      maketestfile.py : creates file with required file size. This helps to test constraint  `file size support`
      makefiletype.py : Creates file with required MIME type #TODO, not there yet. (feel free to contribute)
 
## How to make code changes?
### How to insert a new algorithm for enc/dec feature?
  create <youralgo>.py,
  inherit from baseclass `Crypt` ./server/src/encdec/crypt.py
  add driver code (refer aes.py and mimic structure)
  add driver code function to `./server/src/driver.py` request_router.
  add command line arg --algo at client and send it via requests. #TODO: genric change, one time.

#### Additionally, make sure of following:
  - add unitttest with code coverage at server side
  - add regression with code coverage test at client side.
  - Update README.md and other documetations if necessary.
 
#### Code sanity:
  - run autopep8 autofix for formatting `autopep8 --in-place --aggressive --aggressive --recursive`
  - coding style is PEP8
  - run unittests for both client and server.
  
### Submit your code
Trunk based development, do all changes in main branch and raise a pull request!
  This will automatically run github-actions which has tests with pre-requisites
  Voila! One step closer for your code to move to production. 
  Code review will be done by other contributers.
  
### Release and Distribution
#### Wheel distribution creation [On going]
  
  - update `.version` file with release version (make sure its only one line file)
  - command `python setup.py bdist_wheel` (make sure you are in virtual environment)
  will create file crypto_server.<release_version>-py3-none-any.whl example: `crypto_server-0.0.1-py3-none-any.whl`
  - This 'wheel' file can be distributed and installed using command `pip install <wheel-file-name>` #TODO Add server and client-cli to bin dir to be accessed on terminal.
  
  
### Feature requests and bug:
  Please create new issue mentioning in detail about feature/bug.
  
  
