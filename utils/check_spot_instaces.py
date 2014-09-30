"""
Author: Cristian Spoiala (scristian@gmail.com)
Description:
  This script is intended for users of AWS autoscalling and spot instances
  Will get current open spot request and if are requests with price too low
  will update autoscale group configuration with another launch configuration
Usage: */1 * * * * /usr/bin/python /script.py &> /var/log/spot.log

TODO:
   - sort launch configuration by using a tag Priority (when a launch
    configuration is created to specify on this tag the priority, 1 is higher)
   - send email if if not found any suitable launch configuration
"""

import boto.ec2
import boto.ec2.autoscale
from time import strftime

REGION = 'eu-west-1'
AZ = 'eu-west-1a'
SCALE_GROUP = 'spot'

#mail settings
TO_EMAIL = 'cristi@assist.ro'
FROM_EMAIL = 'zeusdev@english-attack.com'

def process_launch_configuration():
    """get all launch configurations and return instance types
    and spot prices for each
    """
    autoscale = boto.ec2.autoscale.connect_to_region(REGION)
    existing_confs = autoscale.get_all_launch_configurations()
    options = {}
    for conf in existing_confs:
        options[conf.name] = [conf.instance_type, conf.spot_price]

    return options
    #return {'c3.xlarge':'0.045','m3.xlarge':'0.045','r3.xlarge':'0.045'}

def sendmail(subject, content):
    import smtplib
    from email.mime.text import MIMEText

    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = FROM_EMAIL
    msg['To'] = TO_EMAIL
    s = smtplib.SMTP('localhost')
    s.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())
    s.quit()

def get_best_option():
    """Get launch configuration that has the price higher than current
    spot price for that instance. Then update autoscale group with
    this new launch configuration
    """
    ec2 = boto.ec2.connect_to_region(REGION)
    options = process_launch_configuration()
    for name, option in options.iteritems():
        instance_type = option[0]
        price = option[1]
        print "Option: instance type: %s; price: %s" % (instance_type, price)
        now = strftime('%Y-%m-%dT%H:%M:%S.000Z')
        current_price = ec2.get_spot_price_history(availability_zone=AZ,
            instance_type=instance_type,
            end_time=now,
            product_description='Linux/UNIX',
            max_results=1)
        # if desired price is higher than current price,
        # then we can use this launch configuration
        print "Current spot price: instance type: %s price: %s" \
                % (current_price[0].instance_type, current_price[0].price)
        if price > current_price[0].price:
            print "Updating autoscale group: %s with launch config: %s "\
                 % (SCALE_GROUP, name)
            #update_group with new launchconf
            update_group(name)

            #send mail
            content = "Updated autoscale group: %s with launch config: %s"\
                     % (SCALE_GROUP, name)
            sendmail("Updated autoscale group", content)

            #cancel_open_spot_requests()
            #launch an instance spot request ?
            break

    #send mail if not launch configurations found
    #content = "Updated autoscale group: %s with launch configuration: %s" \
    #           % (SCALE_GROUP, name)
    #sendmail("[Critical] No launch configuration found", content)

def update_group(launch_configuration):
    """Update auto scalling group with the new launch configuration"""
    autoscale = boto.ec2.autoscale.connect_to_region(REGION)
    group = autoscale.get_all_groups(names=[SCALE_GROUP])[0]
    setattr(group, 'launch_config_name', launch_configuration)
    group.update()
    print "Updated autoscale group: " + group.name

def cancel_open_spot_requests():
    """cancel current open spot requests"""

def check_spot_requests():
    ec2 = boto.ec2.connect_to_region(REGION)
    spot_requests = ec2.get_all_spot_instance_requests(
                        filters={'status-code':'price-too-low', 'state':'open'}
                        )
    #spot_requests = ec2.get_all_spot_instance_requests(
    #                filters={
    #                    'status-code':'instance-terminated-by-price',
    #                    'state':'closed'})
    print spot_requests
    # if are spot instances with state on price too low then go forward
    if len(spot_requests) > 0:
        get_best_option()
    else:
        print "No open spot requests with status code price-too-low"


check_spot_requests()
