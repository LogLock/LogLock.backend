LogLock.backend
===============


# installation
```bash
$ apt-get install python-magic XOR brew install libmagic
$ (sudo)? make install
```

# endpoints
	GET  / 
		=> application/json
		=> all routes
	
	POST /auth
		=> application/javascript
		=> get param: ?callback=my_tasty_callback
		=> post params: {longitude:longitude, latitude:latitude, screen: screenSize, browser: browser, browserVersion: browserVersion, mobile: isMobile, os: os, osVersion: osVersion}
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