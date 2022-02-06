# python driver for hacking wechat on macOS

## init sqlcipher

```shell
LIBCRYPTO=/usr/local/Cellar/openssl@3/3.0.1/lib/libcrypto.a
```

```shell

git clone https://github.com/sqlcipher/sqlcipher
cd sqlcipher
 
./configure --enable-tempstore=yes CFLAGS="-DSQLITE_HAS_CODEC" \
	LDFLAGS=$LIBCRYPTO --with-crypto-lib=none
	
make && make install

cd ..
```

## init pysqlcipher

```shell
SQLCIPHER=$(pwd)/sqlcipher
```

```shell

git clone https://github.com/rigglemania/pysqlcipher3
cd pysqlcipher3

mkdir amalgamation
cp $SQLCIPHER/sqlite3.[hc] amalgamation/
mkdir src/python3/sqlcipher
cp  amalgamation/sqlite3.h src/python3/sqlcipher/

python setup.py build_amalgamation
python setup.py install

cd ..
```

## monitor wechat database keys

```shell
# monitor in the terminal
pgrep -f '^/Applications/WeChat.app/Contents/MacOS/WeChat' | xargs sudo wechat-decipher-macos/macos/dbcracker.d -p

# monitor into log file
pgrep -f '^/Applications/WeChat.app/Contents/MacOS/WeChat' | xargs sudo wechat-decipher-macos/macos/dbcracker.d -p > data/dbcracker.log
```