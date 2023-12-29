import codecs, grpc, os
# Generate the following 2 modules by compiling the lightning.proto with the grpcio-tools.
# See https://github.com/lightningnetwork/lnd/blob/master/docs/grpc/python.md for instructions.
from lnd_depend import lightning_pb2 as lnrpc, lightning_pb2_grpc as lightningstub

GRPC_HOST = 'localhost:10009'
MACAROON_PATH = '???'
TLS_PATH = '???'

# create macaroon credentials
macaroon = codecs.encode(open(MACAROON_PATH, 'rb').read(), 'hex')
def metadata_callback(context, callback):
  callback([('macaroon', macaroon)], None)
auth_creds = grpc.metadata_call_credentials(metadata_callback)
# create SSL credentials
os.environ['GRPC_SSL_CIPHER_SUITES'] = 'HIGH+ECDSA'
cert = open(TLS_PATH, 'rb').read()
ssl_creds = grpc.ssl_channel_credentials(cert)
# combine macaroon and SSL credentials
combined_creds = grpc.composite_channel_credentials(ssl_creds, auth_creds)
# make the request
channel = grpc.secure_channel(GRPC_HOST, combined_creds)
stub = lightningstub.LightningStub(channel)
channel_point = lnrpc.ChannelPoint(
    funding_txid_str="????",
    output_index=?
)
request = lnrpc.CloseChannelRequest(
  channel_point=channel_point,
  force=False,
  sat_per_vbyte=5,
  max_fee_per_vbyte=200,
)
for response in stub.CloseChannel(request):
  print(response)
# {
#    "close_pending": <PendingUpdate>,
#    "chan_close": <ChannelCloseUpdate>,
# }
