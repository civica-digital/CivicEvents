def aggregate_time(period,log):
    aggregatedTime = {}
    for event in log:
        aggregateTimeEvent = event["created_at"].replace(second=0,microsecond=0)
        if period=="year" :
            aggregateTimeEvent = event["created_at"].replace(month=0, day=0, hour = 0, minute=0,second=0,microsecond=0)
        elif period=="month":
             aggregateTimeEvent = event["created_at"].replace(day=0, hour = 0, minute=0,second=0,microsecond=0)
        elif period=="day":
             aggregateTimeEvent = event["created_at"].replace(hour = 0, minute=0,second=0,microsecond=0)
        elif period=="hour":
             aggregateTimeEvent = event["created_at"].replace(minute=0,second=0,microsecond=0)

        stringAggregateTimeEvent = aggregateTimeEvent.strftime("%Y-%m-%d %H:%M:%S")
        if stringAggregateTimeEvent in aggregatedTime:
            aggregatedTime[stringAggregateTimeEvent] += 1
        else:
            aggregatedTime[stringAggregateTimeEvent] = 1
    return aggregatedTime
