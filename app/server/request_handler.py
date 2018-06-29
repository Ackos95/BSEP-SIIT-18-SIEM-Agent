#!/usr/env/bin python
# -*- coding: utf-8 -*-

import json
import http.server

from app.networking.ssl import get_common_name, get_ssl_request_ip
from app.networking.api import post_check_agent
from app.siem_notifier.notifier import post_logs
from app.logger.logger import get_logger


def get_configured_FirewallRequestHandler(config):
    class FirewallRequestHandler(http.server.BaseHTTPRequestHandler):

        def do_POST(self):
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)

            common_name = get_common_name(self.connection.getpeercert())
            request_ip = get_ssl_request_ip(self.request)

            res = post_check_agent(config['static']['authorizationServerIpAndPort'], config['static']['cert'], {
                'cn': common_name,
                'requestIp': request_ip,
            })

            if res.status != 200:
                get_logger().error('Unauthorized submit attempt from: {} at {}'.format(common_name, request_ip))

                self.send_response(403)
                self.end_headers()
                self.wfile.write(b'Not Authorized')
            else:
                submit_body = json.loads(body.decode('utf-8'), encoding='utf-8')
                res_body = json.loads(res.read().decode('utf-8'), encoding='utf-8')

                if 'firewall' not in res_body or ('firewall' in res_body and len(submit_body) and submit_body[0]['personalLog']):
                    for log in submit_body:
                        log['cn'] = common_name
                        log['personalLog'] = False

                post_res = post_logs(config['static']['authorizationServerIpAndPort'], config['static']['cert'], submit_body)

                self.send_response(post_res.status)
                self.end_headers()
                self.wfile.write(post_res.read())

    return FirewallRequestHandler
