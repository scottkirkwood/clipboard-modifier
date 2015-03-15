# Introduction #

Say your clipboard looks like this:
```
9
8
3
5
1
```

![http://clipboard-modifier.googlecode.com/svn/trunk/doc/sample-sort-shot.png](http://clipboard-modifier.googlecode.com/svn/trunk/doc/sample-sort-shot.png)

After running with the program "sort" and parameter "-n" you should get the output:
```
1
3
5
8
9
```

# Details #

You can enter any program that on your path (or give the full pathname).  It needs to accept input from stdin and output to stdout.
This can be much faster than saving to a file and running the the program from the command line and then copying and pasting the text.