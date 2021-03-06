import collections
from mnm.instances.influxdb_client import get_client


class Stat(object):

    def get(self, **kwargs):
        raise NotImplementedError

    def get_results(self, query):
        return get_client().query(query)


class InstanceFieldStat(Stat):
    query = """
        SELECT sum("{field}")
        FROM instances_hourly
        WHERE time > now() - 24h
        GROUP BY time(1h)"""

    def get(self):
        query = self.query.format(field=self.field)
        results = list(self.get_results(query)['instances_hourly'])
        return {
            'total': results[-1]['sum'],
            '1h': results[-1]['sum'] - results[-2]['sum'],
            '24h': results[-1]['sum'] - results[1]['sum'],
        }


class UsersStat(InstanceFieldStat):
    code = 'users'
    field = "users"

    description = 'Users-related metrics'


class StatusesStat(InstanceFieldStat):
    code = 'statuses'
    field = "statuses"

    description = 'Statuses-related metrics'


class InstancesStat(InstanceFieldStat):
    code = 'instances'
    field = "instances"

    description = 'Instances-related metrics'


stats = collections.OrderedDict()
stats['users'] = UsersStat()
# stats['instances'] = InstancesStat()
stats['statuses'] = StatusesStat()
