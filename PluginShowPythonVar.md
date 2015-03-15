# Introduction #

![http://clipboard-modifier.googlecode.com/svn/trunk/doc/show_python-shot.png](http://clipboard-modifier.googlecode.com/svn/trunk/doc/show_python-shot.png)

This badly named plugin changes the clipboard based on a template.

The use-case was that I wanted to quickly (and temporarily) output some variables in my python program. I'd put the variable name in the clipboard, like:
```
myvar
```
and the plugin would output:
```
print "myvar = %s" % str(myvar)
```

The template it uses is:
```
print '%(var)s = %%s' %% str(%(var)s)
```

But this code is much more general that this since you can change the template to anything.