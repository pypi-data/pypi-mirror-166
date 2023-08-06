# mait: package manager for text adventure games.
[![test-mait.gif](https://i.postimg.cc/XYYy4Xpp/test-mait.gif)](https://postimg.cc/F7wKxrb4)

### Installing is by the PIP manager [Linux]
```commandline
pip3 install mait-manager
```
### Similar for [Windows]
```commandline
py -m pip install mait-manager
```
***You invoke mait via CLI by using the following:***
```commandline
mait --help
```

# uploading.
[![upload-mait.gif](https://i.postimg.cc/BvKq5Gjq/upload-mait.gif)](https://postimg.cc/B8J9sk5y)
The above demonstrates how to upload a single file **(You cannot upload multiple files at this time.)**
### Uploading.
```commandline
mait upload
```
Code must be source code! Compiled sources are not allowed!
### Providing a JSON.
```json
{
  "exec": "python3 donut.py"
}
```
A JSON provides the command to compile/or interpret the code & is required.

**Uploading requires for the file to be reviewed since malicious code can easily be run.** 
Allow up to 48 hours for me to review (I'm a one-man band y'know). If you think the review process is 
being prolonged, contact me at `saynemarsh9@gmail.com`
