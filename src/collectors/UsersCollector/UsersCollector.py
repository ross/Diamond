import diamond.collector
from subprocess import check_output

class UsersCollector(diamond.collector.Collector):

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        return {'path': 'users'}

    def collect(self):
        """
        Overrides the Collector.collect method
        """

        users = {}
        for line in check_output(['w', '-hsf']).split('\n'):
            if not line:
                continue
            user = line.split(' ', 1)[0]
            try:
                users[user] += 1
            except KeyError:
                users[user] = 1

        total = 0
        for user, count in users.items():
            self.publish(self.get_metric_path('logged_in.%s' % user), count)
            total += count

        self.publish(self.get_metric_path('logged_in_total'), total)


    def publish(self, name, value):
        print '%s=%s' % (name, value)


uc = UsersCollector({'collectors': {'default': {}}, 'server':
                     {'collectors_config_path': ''}}, [])
uc.collect()
