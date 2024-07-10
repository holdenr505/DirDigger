# DirDigger
DirDigger is a command-line tool developed entirely in Python 3 that uses a brute-force approach to enumerate exposed directory listings.
## Features
1. Multithreading support allows the user to specify the number of threads (up to 64) used
2. File extensions can be supplied at the command line to perform additional searches
3. Recursion (WIP)

### Installation
1. Clone the repo
2. Run the program
```
git clone https://github.com/holdenr505/DirDigger
```
### Usage
DirDigger currently takes three positional arguments: thread count, wordlist path, url

```
python3 ./DirDigger.py 64 ./path-to-wordlist https://yoururl.com
```
You may also add the optional '-e' flag to add a list of file extensions to search for

```
python3 ./DirDigger .py 64 ./path-to-wordlist https://www.yoururl.com -e .php .js
```
