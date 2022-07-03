# python driver for cracking/hacking wechat on macOS

- version: 0.0.2 
- date: 2022/07/04
- author: markshawn

## environment preparation

### init sqlcipher

1. check where is your `libcrypto.a`

```shell
find /usr/local/Cellar -name libcrypto.a
```

2. use the libcrypto.a with openssl version >= 3
```shell
LIBCRYPTO={YOUR-libcrypto.a}
```

3. install

```shell

git clone https://github.com/sqlcipher/sqlcipher
cd sqlcipher
 
./configure --enable-tempstore=yes CFLAGS="-DSQLITE_HAS_CODEC" \
	LDFLAGS=$LIBCRYPTO --with-crypto-lib=none
	
make && make install

cd ..
```

### init pysqlcipher

```shell

git clone https://github.com/rigglemania/pysqlcipher3
cd pysqlcipher3

mkdir amalgamation && cp ../sqlcipher/sqlite3.[hc] amalgamation/
mkdir src/python3/sqlcipher && cp  amalgamation/sqlite3.h src/python3/sqlcipher/

python setup.py build_amalgamation
python setup.py install

cd ..
```

### disable SIP, otherwise the dtrace can't be used

```shell
# check SIP
csrutil status

# disable SIP, need in recovery mode (hold on shift+R when rebooting)
csrutil disable
```

## hook to get wechat database secret keys

> comparing to `wechat-decipher-macos`, I make the script more robust.

```shell
# monitor into log file, so that to be read by our programme
pgrep -f '^/Applications/WeChat.app/Contents/MacOS/WeChat' | xargs sudo wechat-decipher-macos/macos/dbcracker.d -p > data/dbcracker.log
```

## run analysis

### python environment preparation

```shell
pip install virtualenv
virtualenv venv
source venv/bin/python
pip install -r requirements.txt
```

### test all the database keys

```shell
python src2/main.py
```

## ref

- https://github.com/nalzok/wechat-decipher-macos
- https://github.com/sqlcipher/sqlcipher
- https://github.com/rigglemania/pysqlcipher3
- [Mac终端使用Sqlcipher加解密基础过程详解_Martin.Mu `s Special Column-CSDN博客_mac sqlcipher](https://blog.csdn.net/u011195398/article/details/85266214)
