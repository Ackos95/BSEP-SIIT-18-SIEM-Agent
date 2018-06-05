#!/usr/env/bin python
# -*- coding: utf-8 -*-

import ssl
import OpenSSL

from os.path import exists
from app.utils.path import get_in_config_folder


def check_certs(cert_config):
    return exists(get_in_config_folder('certs/' + cert_config['name'] + '.p12')) and\
           exists(get_in_config_folder('certs/trusted_ca.crt'))


def _generate_agent_pem_files(p12):
    # Where type is FILETYPE_PEM or FILETYPE_ASN1 (for DER).
    type_ = OpenSSL.crypto.FILETYPE_PEM

    private_key = OpenSSL.crypto.dump_privatekey(type_, p12.get_privatekey())
    cert = OpenSSL.crypto.dump_certificate(type_, p12.get_certificate())

    private_key_path = get_in_config_folder('certs/generated/agent-key.pem')
    cert_path = get_in_config_folder('certs/generated/agent.pem')

    with open(private_key_path, 'wb') as f:
        f.write(private_key)
        f.flush()

    with open(cert_path, 'wb') as f:
        f.write(cert)
        f.flush()

    return cert_path, private_key_path


def get_agent_ssl_context(cert_config):
    ctx = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
    ctx.verify_mode = ssl.CERT_REQUIRED
    ctx.options |= ssl.OP_NO_TLSv1_2

    ctx.load_verify_locations(get_in_config_folder('certs/trusted_ca.crt'))

    # TODO: handle configuration error (missing or invalid certificate)
    with open(get_in_config_folder('certs/' + cert_config['name'] + '.p12'), 'rb') as f:
        p12 = OpenSSL.crypto.load_pkcs12(f.read(), cert_config['password'])
        ctx.load_cert_chain(*_generate_agent_pem_files(p12))

    return ctx


def get_common_name(cert):
    for t1 in cert['subject']:
        for t2 in t1:
            if t2[0] == 'commonName':
                return t2[1]


def get_ssl_request_ip(sock):
    addr = sock.getpeername()

    return addr[0] + ':' + str(addr[1])
