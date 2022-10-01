# CF3

*Fingerprinting censors, one blockpage at a time.*

## What

This tool attempts to extract unique features in blockpages in a compact way.

```
❯ for f in corpus/*; do cf3 $f hash; done > hashes
❯ wc -l hashes
136 hashes
❯ uniq hashes | wc -l
135
# almost! but there are two blockpages that are essentially the same :)
```

## Install

```
pip3 install cf3
```

## Hash

```
curl -L --silent https://example.com | cf3
```

## Verbose

```
❯ cf3 corpus/prod_comodo_securedns_warning.html
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

## Dynamic content

The algorithm tries to be invariant under pages that share a well-defined structure but for which dynamic content, js nonces and other quirks result in highly variable content. YMMV.

```
❯ for i in {1..10}; do curl -L --silent https://youtube.com | cf3; done
9a0edf442a37fbb0fb6e28a122d33e56
9a0edf442a37fbb0fb6e28a122d33e56
9a0edf442a37fbb0fb6e28a122d33e56
9a0edf442a37fbb0fb6e28a122d33e56
9a0edf442a37fbb0fb6e28a122d33e56
9a0edf442a37fbb0fb6e28a122d33e56
9a0edf442a37fbb0fb6e28a122d33e56
9a0edf442a37fbb0fb6e28a122d33e56
9a0edf442a37fbb0fb6e28a122d33e56
9a0edf442a37fbb0fb6e28a122d33e56
```

## Notes

Under development! The fingerprinting algorithm might change.

# License

This code is deposited in the public domain.
