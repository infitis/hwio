from threading import Thread

import tornado.httpserver
import tornado.ioloop
import tornado.web

class HttpServerThread(Thread):
    
    def __init__ (self, hwio):
        Thread.__init__(self)
        self.hwio = hwio
        self.setName('hwio http server')
    
    def run(self):
        self.http_server = tornado.httpserver.HTTPServer(HttpApplication(self.hwio))
        self.http_server.listen(self.hwio.settings['http_port'])
        
        tornado.ioloop.IOLoop.instance().start()
    
    def finish(self):
        tornado.ioloop.IOLoop.instance().stop()


class HttpApplication(tornado.web.Application):
    def __init__(self, hwio):
        handlers = [
            (r'/', MainHandler),
            (r'/device/([-\w_]*)', DeviceHandler),
            (r'/signal/([-\w_]*)', SignalHandler),
        ]
        settings = dict(
            #template_path=os.path.join(os.path.dirname(__file__), "templates"),
            #static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug = hwio.settings['debug'],
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        
        self.hwio = hwio



class MainHandler(tornado.web.RequestHandler):
    
    def get(self):
        self.write('whio http server/{0} : {1}<br /><br />\n'.format(hwio.VERSION, self.application.hwio.name))
        self.write('<a href="/device/">devices</a>\n')
        self.write('<ul>\n')
        for device in self.application.hwio.devices:
            self.write('<li><a href="/device/{0}">{0}</a></li>\n'.format(device))
        self.write('</ul>\n')
        self.write('<a href="/signal/">signals</a>\n')
        self.write('<ul>\n')
        for signal in self.application.hwio.signals:
            self.write('<li><a href="/signal/{0}">{0}</a></li>\n'.format(signal))
        self.write('</ul>\n')



class SignalHandler(tornado.web.RequestHandler):
    
    def get(self, signal_id):
        if signal_id:
            if signal_id in self.application.hwio.signals:
                # write signal state
                self.write(str(self.application.hwio.signals[signal_id].state))
            else:
                raise tornado.web.HTTPError(404)
        else:
            # write signal list
            self.write(', '.join([signal for signal in self.application.hwio.signals.keys()]))


class DeviceHandler(tornado.web.RequestHandler):
    
    def get(self, device_id):
        if device_id:
            if device_id in self.application.hwio.devices:
                # write signal state
                self.write(str(self.application.hwio.devices[device_id].model))
            else:
                raise tornado.web.HTTPError(404)
        else:
            # write device list
            self.write(', '.join([device for device in self.application.hwio.devices.keys()]))

