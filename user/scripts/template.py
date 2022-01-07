# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-06 20:23:12
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-07 08:10:15


try:
    import codecs, grpc, os
    from grpc_generated import lightning_pb2 as lnrpc
    from grpc_generated import lightning_pb2_grpc as lightningstub
except:
    pass

from orb.misc.prefs import hostname, cert, macaroon, grpc_port
from orb.misc.plugin import Plugin


class GRPCExample(Plugin):
    def main(self):
        os.environ["GRPC_SSL_CIPHER_SUITES"] = "HIGH+ECDSA"
        ssl_creds = grpc.ssl_channel_credentials(cert())
        channel = grpc.secure_channel(f"{hostname()}:{grpc_port()}", ssl_creds)
        stub = lightningstub.LightningStub(channel)
        print(stub)

    @property
    def menu(self):
        return "examples > GRPCExample"

    @property
    def uuid(self):
        return "3f8ee0be-15a4-47dd-8205-a464cae77c9e"
