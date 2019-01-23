from vsts.vss_connection import VssConnection
from msrest.authentication import BasicAuthentication
import random, sys, re

def add_args(parser):
    parser.add_argument('--azure-match', metavar='REGEX', dest='azmatch', type=str, default='.+',
                        help='Regex on build name to match')
    parser.add_argument('--azure-key', metavar='TOKEN', dest='azkey', type=str, default='.+',
                        help='PAT token to use')
    parser.add_argument('--azure-project', metavar='NAME', dest='azproject', type=str,
                        help='Project to use')
    parser.add_argument('--azure-branch', metavar='REGEX', dest='azbranch', type=str, default='refs/heads/master',
                        help='Branch name to match (default to master)')

def get_source(args):
    org = args.azure
    if not org: raise ValueError()
    proj = args.azproject
    if not proj: raise ValueError("Azure DevOps project not specified")
    key = args.azkey
    if not key: raise ValueError("Azure DevOps PAT token not specified")
    mname = re.compile(args.azmatch)
    mbranch = re.compile(args.azbranch)
    credentials = BasicAuthentication('', key)
    connection = VssConnection(base_url='https://dev.azure.com/%s' % org, creds=credentials)
    #core_client = connection.get_client('vsts.core.v4_0.core_client.CoreClient')
    build_client = connection.get_client('vsts.build.v4_1.build_client.BuildClient')
    #projects = core_client.get_projects()
    builds = build_client.get_builds(proj)

    def scan():
        hasInProgress = False
        hasFailed = False
        last = {}
        # Show details about each project in the console
        for build in builds:
            branch = build.source_branch
            if not branch or not mbranch.search(branch):
                continue
            name = build.definition.name
            if not mname.search(name):
                continue
            if build.status == "inProgress":
                hasInProgress = True
            elif build.status == "completed":
                lastBuild = last.get(name)
                if not lastBuild or lastBuild.finish_time < build.finish_time:
                    last[name] = build
        for _, build in sorted(last.items()):
            print("%s - %s - %s - %s" % (build.definition.name, build.source_branch, build.result, build.finish_time))
            if build.result != "succeeded":
                hasFailed = True
        return (hasFailed, hasInProgress)
    return scan
