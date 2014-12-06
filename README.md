LogLock.backend
===============


# installation
```bash
$ apt-get install python-magic XOR brew install libmagic
$ (sudo)? make install
```

# endpoints
	GET  / 
		=> text/plain
		=> Hello world
	
	POST /auth
		=> application/javascript
		=> get param: ?callback=my_tasty_callback
		=> post params: ip, geo, os & browser 
		=> my_tasty_callback({ "safe": [ 1, "123", "madrid", "mac", "chrome" ] })

	GET /config
	
	POST /config
		
	
# dev server (port 5000)
```
$ make
```

# 'production' server
(sudo gem install foreman)
```
$ foreman start
```