import random


def random_mac():
    mac = [
        0x00, 0x16, 0x3e,
        random.randint(0x00, 0x7f),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff)
    ]
    return ':'.join(map(lambda x: "%02x" % x, mac))


class MacIpTable(object):
    free_table = []
    used_table = []

    def __init__(self):
        self.free_table = self.generate_table()

    def generate_table(self):
        table = []
        for i in range(2, 255):
            table.append({
                'ip': '192.168.201.{0}'.format(i),
                'mac': '{1}'.format(i, random_mac())
            })

        return table

    def get_free_mac(self):
        try:
            raw = self.free_table.pop()
        except IndexError:
            raise Exception("Table is empty")

        self.used_table.append(raw)

        return raw["mac"]

    def get_ip(self, mac):
        raw = self.find_raw_by_mac(self.used_table, mac)
        return raw['ip']

    def find_raw_by_mac(self, table, mac):
        for raw in table:
            if raw['mac'] == mac:
                return raw

        raise ValueError("no mac %s in table %s" % (repr(mac), repr(table)))

    def append_free_mac(self, mac):
        try:
            raw = self.find_raw_by_mac(self.used_table, mac)
            self.used_table.remove(raw)
        except IndexError:
            raise Exception("Table is empty")

        self.free_table.append(raw)
