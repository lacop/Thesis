ds = ['statictree', 'orderedfile', 'cobtree']
lang = ['en', 'sk']

with open('template.html', 'r') as tf:
    template = tf.read()

for d in ds:
    for l in lang:
        with open('applet_'+d+'_'+l+'.html', 'w') as of:
            of.write(template.replace('!!DS!!', d).replace('!!LANG!!', l))