# Introduction #

Converts some text into a Java String.


# Details #

It can do multiple lines which will will look something like:
```
"This is the first line"
+ "This is the second line"
```

Quotes will be properly escaped so that
```
"Hello"
```
Becomes
```
"\"Hello\""
```
.

# Nice to Haves #

Would be nice to escape Unicode character and to have easy to modify options like the indentation, whether the plus is at the start or the end, etc.