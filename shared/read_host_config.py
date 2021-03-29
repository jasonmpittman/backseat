class ReadHostConfig:
    def __init__(self):
        self.endpoints = []
        self.read_host_cofig_file()

    def read_host_cofig_file(self):
        lines = []
        with open("host.config", "r") as H:
            lines = H.readlines()
        
        for line in lines:
            line = line.replace(" ", "")
            line = line.replace("\n", "")
            print("-line-")
            print(line)
            endpoint, os, key, ip, port = line.split(",")
            self.endpoints.append({"endpoint": endpoint, "os": os, "key": key, "ip": ip, "port": port})
    
    def get_key_table(self):
        table = {}
        for line in self.endpoints:
            table[line["key"]] = line["endpoint"]
        print(table)
        return table


