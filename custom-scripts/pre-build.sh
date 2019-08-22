#!/bin/sh
  
cp $BASE_DIR/../custom-scripts/S41network-config $BASE_DIR/target/etc/init.d
chmod +x $BASE_DIR/target/etc/init.d/S41network-config
cp $BASE_DIR/../custom-scripts/simple_http_server.py $BASE_DIR/target/usr/bin/
chmod +x $BASE_DIR/target/usr/bin/simple_http_server.py
cp $BASE_DIR/../custom-scripts/S42server-config $BASE_DIR/target/etc/init.d
chmod +x $BASE_DIR/target/etc/init.d/S42server-config

