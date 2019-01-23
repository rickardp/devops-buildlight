import argparse
import sys, time

import source_azuredevops
import target_homey
import target_hue

parser = argparse.ArgumentParser(description='Azure DevOps buildlight for Athom Homey and Philips Hue.')
parser.add_argument('--azure', metavar='ORGANIZATION', type=str,
                    help='use Azure DevOps with the specified organization')
source_azuredevops.add_args(parser)
parser.add_argument('--interval', dest='interval', metavar="SECONDS", default=15, type=int,
                    help='polling interval')

parser.add_argument('--homey', dest='homey', metavar="ID", type=str,
                    help='control Athom Homey (ID e.g. 0123456789abcdef12345678)')
target_homey.add_args(parser)
parser.add_argument('--hue', dest='hue', metavar="IP", type=str,
                    help='control Philips Hue bridge (IP e.g. 192.168.1.11)')
target_hue.add_args(parser)
args = parser.parse_args()
if args.azure:
    source = source_azuredevops.get_source(args)
else:
    print("No valid source specified", file=sys.stderr)
    sys.exit(1)

targets = []
if args.homey:
    targets.append(target_homey.get_target(args))
if args.hue:
    targets.append(target_hue.get_target(args))
if not targets:
    print("No valid target specified", file=sys.stderr)
    sys.exit(1)

try:
    while True:
        t0 = time.time()
        hasInProgress, hasFailed = source()
        print("in progress: %s, has failed: %s" % (hasInProgress, hasFailed))
        sys.stdout.flush()
        for tgt in targets:
            tgt(hasInProgress, hasFailed)
        time.sleep(args.interval - max(0, time.time() - t0))
except KeyboardInterrupt:
    pass
