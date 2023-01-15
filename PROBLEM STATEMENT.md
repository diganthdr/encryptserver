# 
## Challenge Statement

This challenge is about creating a simple cryptography server and a command line client to encrypt, decrypt, or cryptographic hash a plain-text data sent from the client.

### Challenge Details
You are tasked to implement a simple cryptography server and a command line client, this server should support the following functions:

1. Encrypt a file
    ```
    Input(s): A plain-text file
    Output: An encrypted file
    ```
1. Decrypt a file
    ```
    Input(s): An encrypted file
    Output: A plain-text file
    ```
1. Hash a password into a secure cryptographic hash
    ```
    Input(s): A string 
    Output: A hashed password in Base64 encoding
    ```

#### Server

To simplify the design of this cryptography server, all clients will use the same secret key for encryption and decryption. 
The server may be written in a language and framework of your choosing.
If you wish to use a different interface (or different non-HTTP/REST protocol), you may do so as long as it supports the three functions listed above (the inputs, outputs, and types are just suggestions to get started).

#### Command Line Interface

After you have completed the server, please implement a command line interface (CLI) to interact with the server.
The CLI should support the same three functions as the server,
- crypto-api encrypt <input_file>
- crypto-api decrypt <input_file>
- crypto-api password-hash <password_string>
We suggest using existing CLI frameworks to handle the needed boilerplate.

#### Additional Guidance

When working on this challenge, be sure to implement your solution as if you were in a production setting (think about how real production code is set up and managed). 
You are allowed to make a decision about the runtime environment of both the server and the command line, and please document it in the README file. 
Specifically, some things to think about including:

- Proving correctness of the code (and ensuring future code changes don’t break CLI / Server interaction)
- CLI design and ease of use
- Project tooling and reproducible builds (what tooling or checks would you need in place in an OSS project, for example)
- Installation (how would you distribute the software to a user)

### Expectations

1. Please work on this git repository as if it were a real project at work.
1. The git repository should include a README file containing build and instructions. 
Feel free to move, rename, or replace this instruction README.
1. Once you have completed the challenge, please inform us by email.
In your email response, please let us know roughly how many hours you spent on this challenge.
We will not grade you based on this answer -- it is helpful for us to normalize the difficulty of challenges.
