# Symmetric Encryption Algorithm by Mattyw&MeBeiM

*NB: this project has been discontinued and is now superseded by [`mbc`][mbc-link].*

*Version: 2.0*

___________________________________________________________________________________________

SYNTAX:

```
usage: mbencrypter [-h] (-e | -d) [-k <string>] [-i <path>] [-o [<path>]] [-hex] [-v] [-q] [--version]

This program will help you encrypting or decrypting
some data or a file using MB's algorithm.
You can also send a SIGUSR1 to this process to get
its progress status.

Note: if no parameter is specified the program will
run in interactive mode.

optional arguments:
  -h, --help   show this help message and exit
  -e           run in encode mode.
  -d           run in decode mode.
  -k <string>  specify the key from a string. If no key is specified it will
               be asked via password prompt after the OEF of input data.
  -i <path>    specify the input file. Default to <stdin>.
  -o [<path>]  specify the output file. Leave empty to use the same path of
               the input file, adding/removing the .mbc extension. Default to
               <stdout>.
  -hex         input/output data in base16.
  -v           run in verbose mode.
  -q           don't log progress status.
  --version    show program's version number and exit
```


## Algorithm v2.0: ##

- Input data is splitted in chunks of max 20kiB

### Per-Byte XOR encoding ###
- If the key is shorter than data, it will be repeated until the end of the data.
- If the key is longer than the data, the key will be XORed against itself, to make it fit with the data.
- Each byte of the data is then XORed with each byte of the key.

### Octal Mixing Encoding, by MeBeiM ###
- The key is converted in an octal array.
- Each pair of numbers in the array indicate to swap the corrispective nth bits of each byte of the data.
- A longer key makes the algorithm more effective.

____________________________________________________________________________________________

*Copyright © 2015 Matteo Bernardini & Marco Bonelli*


[mbc-link]: https://github.com/mttbernardini/mbc
