import password as pw
class Memory:
    def __init__(self,name):
        self.name=name
        self.__data={}
    def add(self,datas):
        for i,j in datas.items():
            self.__data[i]=j
    def remove(self,*key):
        for i in key:
            self.__data.pop(i)
    def get(self):
        return self.__data
    def clear(self):
        self.__data={}
class razo_p:
    password = pw.Password(method='sha512', hash_encoding='base64')
if __name__=='__main__':
    from razo import __main__ as main
    main.start()