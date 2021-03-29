class ReadHostConfig:
    def __init__(self):
        self.__endpoints = []
        self.read_host_cofig_file()

    def read_host_cofig_file(self):
        lines = []
        with open("host.config", "r") as H:
            lines = H.readlines()
        
        for line in lines:
            name, os, key, ip, port = line
            self.__endpoints.append({"endpoint": name, "os": os, "key": key, "ip": ip, "port": port})
    
    def get_key_table(self):
        table = {}
        for line in self.__endpoints:
            table[line["key"]] = line["name"]
        return table


