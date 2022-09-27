# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-09-25 11:25:52
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-26 12:49:12

import os
from pathlib import Path
from fabric import Connection
from invoke import task, Responder


@task
def orb_vcn(c):
    cert = (Path(os.getcwd()) / "lnorb_com.cer").as_posix()
    with Connection(
        "lnorb.com", connect_kwargs={"key_filename": cert}, user="ubuntu"
    ) as con:
        con.run("mkdir -p /tmp/asdf")
        with con.cd("/tmp/asdf"):
            con.put("images/orb-256x256.png", "/tmp/asdf/orb-256x256.png")
            con.put("images/orb-128x128.png", "/tmp/asdf/orb-128x128.png")
            con.put("images/orb-48x48.png", "/tmp/asdf/orb-48x48.png")
            con.put("images/orb-32x32.png", "/tmp/asdf/orb-32x32.png")
            con.put("images/orb-16x16.png", "/tmp/asdf/orb-16x16.png")
            con.put("images/orb-16x16.png", "/tmp/asdf/orb-16x16.png")
            con.put("build_system/pcmanfm.conf", "/tmp/asdf/pcmanfm.conf")
            con.put("build_system/orb.desktop", "/tmp/asdf/orb.desktop")
            con.put("build_system/dockerfile.vnc", "/tmp/asdf/dockerfile.vnc")
            con.put("build_system/startup.sh", "/tmp/asdf/startup.sh")
            con.put("images/bg.jpeg", "/tmp/asdf/bg.jpeg")
            con.run("docker build -t lnorb/orb-vnc:0.21.13 -f dockerfile.vnc .")
            con.run("docker tag lnorb/orb-vnc:0.21.13 lnorb/orb-vnc:latest")
            con.run("docker push lnorb/orb-vnc:latest")
            con.run("docker rm -f orb-vnc")
            # startup = """-e OPENBOX_ARGS='--startup "/usr/bin/firefox http://menziess.github.io"'"""
            # startup = """-e OPENBOX_ARGS='--startup "/home/ubuntu/orb/venv/bin/python3 /home/ubuntu/orb/main.py"'"""
            con.run(
                f"docker run -d --name orb-vnc -p 6080:80 -e USER=ubuntu -e HTTP_PASSWORD=moneyprintergobrrr -v /dev/shm:/dev/shm lnorb/orb-vnc"
            )
            con.run("docker logs -f orb-vnc")
