#!/usr/bin/python

from phue import Bridge

import tornado.ioloop
import tornado.web
import tornado.httpclient

from tornado.options import define, options, parse_command_line

define("port", default=8801, help="run on the given port", type=int)

main = None


class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def post(self):
        light = self.get_argument('light', '')
        status = self.get_argument('status', '')
        main["b"].set_group(int(light), 'on', int(status) == 1)
        self.write(light + ":" + status)
        self.get()

    @tornado.web.asynchronous
    def get(self):
        self.set_header('Content-Type', 'text/html; charset=utf-8')
        self.write('<html>')
        self.write('<head>')

        self.write('<script language="JavaScript">')
        self.write('function fclick(f, light, status) {document.f.light.value = light; document.f.status.value = status; document.f.submit()}')
        self.write('</script>')

        self.write('</head><body>')

        self.write("caca<br />")

        groups = b.get_group()
        main["groups"] = groups
        self.write("<form name='f' action='/' method='post'>")
        for group in main["groups"]:
            self.write("<input type='button' value='On'  onclick='fclick(this, " + group + ", 1)'/>")
            self.write("<input type='button' value='Off' onclick='fclick(this, " + group + ", 0)'/>")
            the_group = main["groups"][group]
            print(str(the_group) + "\n")
            name = the_group["name"]
            on = the_group["action"]["on"]
            bri = the_group["action"]["bri"]
            self.write(name + " : " + str(on) + "(" + str(bri) + ")<br />")

        self.write("<input type='text' name='light' value='l'></input>")
        self.write("<input type='text' name='status' value='s'></input>")

        self.write("</form></body></html>")
        self.flush()
        self.finish()

if __name__ == "__main__":

    main = {}
    b = Bridge('192.168.1.56')
    main["b"] = b

    # If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
    b.connect()

    # Get the bridge state (This returns the full dictionary that you can explore)
    b.get_api()

    # Prints if light 1 is on or not
    b.get_light(1, 'on')

    light_names = b.get_light_objects('name')
    main["lights"] = light_names

    groups = b.get_group()
    main["groups"] = groups

    app = tornado.web.Application([
        (r'/', IndexHandler),
    ])

    parse_command_line()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


