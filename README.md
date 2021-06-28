shelter
===
Upgrade of bashShelter password manager, but written in Python3. Program uses gpg encryption to keep your data save.

# Usage
## download 
```
git clone https://github.com/RandomGuy090/shelter
sudo chmod +x run.py
```
## help
```
 ./shelter.py <options>
           -f --file        file location
           -r --recipient   recipient       
           -s --secret      import secret key
           -p --public      import public key
```
## symmetric encryption
```
./run.py -f <encrypted file>
```
![sym](https://user-images.githubusercontent.com/64653975/123689517-99412280-d853-11eb-8e60-0d8ffca72c2c.gif)

## asymmetric enctyption
```
if keys are already loaded
./run.py -f <encrypted file>
if keys arent loaded
./run.py -f <encrypted file> -s <secret key> -p <public key>
```
![asym](https://user-images.githubusercontent.com/64653975/123689591-a9590200-d853-11eb-9699-76e486d44ecf.gif)

#### to save with new recipient add flag ```-r```
e.g.
```
./run.py -f <encrypted file> -r <new recipient>
```
#### to download encrypted file from http site use:
```
./ run.py -f <url of plaintext http site> -s <secret key> -p <public key>
```
![http](https://user-images.githubusercontent.com/64653975/123689952-1ff5ff80-d854-11eb-9506-b571bac4f7be.gif)
