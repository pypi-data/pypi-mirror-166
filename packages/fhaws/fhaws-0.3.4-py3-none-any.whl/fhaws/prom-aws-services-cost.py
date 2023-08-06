import boto3
import datetime
import random
import os

def promrpt(profile, promfile):
    now = datetime.datetime.now()
    start = (now - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    end = now.strftime('%Y-%m-%d')

    session = boto3.session.Session(profile_name=profile)
    cd = session.client('ce', 'us-east-1')
    results = []
    token = None
    while True:
        if token:
            kwargs = {'NextPageToken': token}
        else:
            kwargs = {}
        #data = cd.get_cost_and_usage(TimePeriod={'Start': start, 'End':  end}, Granularity='DAILY', Metrics=['UnblendedCost'], GroupBy=[{'Type': 'DIMENSION', 'Key': 'LINKED_ACCOUNT'}, {'Type': 'DIMENSION', 'Key': 'SERVICE'}], **kwargs)
        data = cd.get_cost_and_usage(TimePeriod={'Start': start, 'End':  end}, Granularity='DAILY', Metrics=['UnblendedCost'], GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}], **kwargs)
        results += data['ResultsByTime']
        token = data.get('NextPageToken')
        if not token:
            break

    report = []
    report.append("# TYPE org_service_daily_spend gauge")
    total = 0
    for result_by_time in results:
        for group in result_by_time['Groups']:
            amount = group['Metrics']['UnblendedCost']['Amount']
            total += float(amount)
            if float(amount) < 0.01:
                continue
            unit = group['Metrics']['UnblendedCost']['Unit']
            report.append("org_service_daily_spend{root=\"%s\",service=\"%s\"} %0.2f" % 
                        (profile, group['Keys'][0].lower().replace(" ", "_").replace("-", "").replace("(","").replace(")","")
                        .replace("__","_"),
                        float(amount)))
            #print(result_by_time['TimePeriod']['Start'], '\t', '\t'.join(group['Keys'][0]), '\t', amount)

    prom = promfile + ".prom"
    promtmp = prom + "." + "".join([str(random.randint(0,9)) for x in range(8)])
    out = open(promtmp, 'w')
    out.write("\n".join(report) + '\n')
    out.flush(); out.close()
    os.rename(promtmp, prom)


if __name__ == '__main__':
    promrpt('hdc-aws', './hdc-aws-org-service-spend')