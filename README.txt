What does this script?
This script creates an ipsec tunnels both pri and sec.
It creates remote network in prisma INET tenant and locate a network and register to men and mice. 
Not all the process is automated therefore some steps must be done manually.

In "get_ip()" function the "ref='10.255.2.0/24'" object must be controlled that is not full net and there is /31 net available.

In the info cite information the remote site "region" and "spn" must configure manually. 

How to run this script?

The script will go through every row in the "info.csv" file and will creat a remote network and ipsec tunnel.
We start to add the RN information in the info.csv file. The need inforamtion is:
site: the site id ex. C3241192
city: The city of the site ex. Gothenburg
region: this informatio need to be brougt from the prisma remote network location. ex 'mexico-central' 
spn: this is IPSEC Termination Node and it's depende on with location.
function: This is which tenant this RN belongs to. 

When this inforamtion are written, we can run the "Main-program INET-IPSEC.py" and the remote site will be created. 

API KEY
