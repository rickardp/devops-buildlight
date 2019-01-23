# bluegreen-lamp

Visualize the state of blue/green deployment using the Athom Homey or Philips Hue.


## How to use it

To build and run, use


     # Control Homey using Azure Traffic Manager as source
     docker run -it $(docker build -q .) --dns my-site.trafficmanager.net --homey 12345abcde

     # Ditto Philips Hue
     docker run -it $(docker build -q .) --dns my-site.trafficmanager.net --hue 192.168.0.1 --hue-lights 1,3,6

     # my-site.com is cname to traffic manager
     docker run -it $(docker build -q .) --dns my-site.com --cname 1 --hue 192.168.0.1 --hue-username xxxxxxx
     

### How to control Homey

Homey supports webhooks from the cloud API. You can control the event names in the webhooks by adjusting `--homey-*-event`. Create a flow for each event you want to support. In this flow you can adjust lamps, lightstrips, change LED ring color, speak, or whatever.

You can either have the webhook sent with every poll, or only when it is changed (the latter is the default).

### How to control Hue

Hue support is very basic. Specify the IP and username, and which lamps to control. The colors are hard coded.

#### Note about the Philips hue and username creation
The first time you run it, you have to create a username. To do this, just leave out the --hue-username parameter. Press the button on the Hue when requested and note down the generated username. Then add this to the `--hue-username` parameter to authenticate.

The easiest way to have it run as a service is probably to create a `docker-compose.yml` file and run it with `docker-compose up --build -d`. Set restart policy to `always` to have it start up automatically after a reboot.

## Usage

    usage: main.py [-h] [--dns hostname] [--dns-match-blue regex]
               [--dns-match-green regex] [--cname NUMLEVELS]
               [--interval SECONDS] [--homey ID] [--homey-blue-event EVENT]
               [--homey-green-event EVENT] [--homey-mix-event EVENT]
               [--homey-mix-error EVENT] [--homey-webhook-repeat] [--hue IP]
               [--hue-username USERNAME] [--hue-lights ARRAY]

    Blue/Green deployment publish to Philips Hue.

    optional arguments:
      -h, --help            show this help message and exit
      --dns hostname        use DNS approach
      --dns-match-blue regex
                            the DNS response that matches Blue (default is "blue")
      --dns-match-green regex
                            the DNS response that matches Blue (default is
                            "green")
      --cname NUMLEVELS     pre-resolves NUMLEVELS levels of CNAME
      --interval SECONDS    polling interval
      --homey ID            control Athom Homey (ID e.g. 0123456789abcdef12345678)
      --homey-blue-event EVENT
                            the webhook event to send when blue
      --homey-green-event EVENT
                            the webhook event to send when green
      --homey-mix-event EVENT
                            the webhook event to send when both blue and green
                            (gradual rollout)
      --homey-mix-error EVENT
                            the webhook event to send when indeterminate
      --homey-webhook-repeat
                            repeat the webhook (default is to only run when
                            changed)
      --hue IP              control Philips Hue bridge (IP e.g. 192.168.1.11)
      --hue-username USERNAME
                            the username to use when connecting to the bridge
      --hue-lights ARRAY    the light(s) to change
