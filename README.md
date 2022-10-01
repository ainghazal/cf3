# CF3

*fingerprinting censors, one blockpage at a time.*

## what

This tool attempts to extract unique features in blockpages in a compact way.

```
❯ for f in corpus/*; do ./cf3 $f hash; done > hashes
❯ wc -l hashes
136 hashes
❯ uniq hashes | wc -l
135
# almost! :)
```

## verbose

```
❯ ./cf3 corpus/prod_comodo_securedns_warning.html
title size: 17
meta: 2
script: 2
head size: 2048
body size: 1024
total size: 4096
tag vector summary: 88
tag vector: html,head,title,link,style,meta,meta,body,div,img,div,img,div,button,div,div,h1,h2,p,br,ul,li,a,img,br,br,p,a,div,div,p,script,script

CF3: 17-2-2-33-88-2048-1024-4096
md5: 12c27a55433b1813c02a8a92dd4b3bff
```

## dynamic content

The algorithm tries to be invariant under pages that share a well-defined structure but for which dynamic content, js nonces and other quirks result in highly variable content. YMMV.

```
❯ mkdir tmp && cd tmp
❯ for i in {1..10}; do curl -L --silent https://www.youtube.com/ > yt$i.html; done
❯ for f in *; do ../cf3 $f hash; done
993522ccea4b8e11857ff4bb1917a77d
993522ccea4b8e11857ff4bb1917a77d
993522ccea4b8e11857ff4bb1917a77d
993522ccea4b8e11857ff4bb1917a77d
993522ccea4b8e11857ff4bb1917a77d
993522ccea4b8e11857ff4bb1917a77d
993522ccea4b8e11857ff4bb1917a77d
993522ccea4b8e11857ff4bb1917a77d
993522ccea4b8e11857ff4bb1917a77d
993522ccea4b8e11857ff4bb1917a77d
```

# license

This code is deposited in the public domain.



