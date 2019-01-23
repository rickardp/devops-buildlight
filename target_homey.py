import requests

def add_args(parser):
    parser.add_argument('--homey-inprogress-event', metavar='EVENT', dest='homey_inprogress_event', type=str, default="build_inprogress",
                        help='the webhook event to send when build in progress stage changed')
    parser.add_argument('--homey-failed-event', metavar='EVENT', dest='homey_failed_event', type=str, default="build_failed",
                        help='the webhook event to send when build failed state changed')
    parser.add_argument('--homey-webhook-repeat', dest='homey_repeat', action="store_true",
                        help='repeat the webhook (default is to only run when changed)')

last_inprogress = None
last_failed = None
def get_target(args):
    id = args.homey
    print("Will control Athom Homey @ %s" % id)
    def send_webhook(inProgress, failed):
        global last_inprogress, last_failed
        if args.homey_repeat or last_inprogress != inProgress:
            last_inprogress = inProgress
            wh = 'https://%s.connect.athom.com/api/manager/logic/webhook/%s?tag=%s' % (args.homey, args.homey_inprogress_event, inProgress)
            print("Sending webhook %s" % wh)
            try:
                requests.get(wh, timeout=10.0)
            except requests.exceptions.Timeout:
                print("timeout sending webhook")
        if args.homey_repeat or last_failed != failed:
            last_failed = failed
            state = args.homey_inprogress_event
            wh = 'https://%s.connect.athom.com/api/manager/logic/webhook/%s?tag=%s' % (args.homey, args.homey_failed_event, failed)
            print("Sending webhook %s" % wh)
            try:
                requests.get(wh, timeout=10.0)
            except requests.exceptions.Timeout:
                print("timeout sending webhook")
    return send_webhook
