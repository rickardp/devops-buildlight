import qhue
import sys

def add_args(parser):
    parser.add_argument('--hue-username', metavar='USERNAME', dest='hue_username', type=str,
                        help='the username to use when connecting to the bridge')
    parser.add_argument('--hue-lights', metavar='ARRAY', dest='hue_lights', type=str, default="1",
                        help='the light(s) to change')


def get_target(args):
    if not args.hue_username and args.hue:
        print("Need to create the username")
        from qhue import create_new_username
        username = create_new_username(args.hue)
        print("Add '--hue-username %s' to the command line and restart" % username)
        sys.exit(0)
    print("Will control Philips Hue @ %s" % args.hue)
    b = qhue.Bridge(args.hue, args.hue_username)
    lights = list(map(int, args.hue_lights.split(',')))
    def set_lights(inProgress, failed):
        bri = 127
        alert = "select"
        if not failed:
            hue = 25500
        else:
            hue = 0
            bri = 255
        if inProgress:
            alert = "lselect"
        #for light in lights:
        #    b.lights[light].state(bri=bri//2, hue=hue, alert="none")
        for light in lights:
            b.lights[light].state(bri=bri, hue=hue, alert=alert)
    return set_lights
