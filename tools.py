def aggregate_time(period,log):
    aggregatedTime = {}
    for event in log:
        aggregateTimeEvent = event["date"].replace(second=0,microsecond=0)
        if period=="year" :
            aggregateTimeEvent = event["date"].replace(month=0, day=0, hour = 0, minute=0,second=0,microsecond=0)
        elif period=="month":
             aggregateTimeEvent = event["date"].replace(day=0, hour = 0, minute=0,second=0,microsecond=0)
        elif period=="day":
             aggregateTimeEvent = event["date"].replace(hour = 0, minute=0,second=0,microsecond=0)
        elif period=="hour":
             aggregateTimeEvent = event["date"].replace(minute=0,second=0,microsecond=0)

        stringAggregateTimeEvent = aggregateTimeEvent.strftime("%Y-%m-%d %H:%M:%S")
        if stringAggregateTimeEvent in aggregatedTime:
            aggregatedTime[stringAggregateTimeEvent] += 1
        else:
            aggregatedTime[stringAggregateTimeEvent] = 1
    return aggregatedTime
