import os
from flask import Flask
from ip2Region import Ip2Region

ip2region = Flask(__name__)

dbFileName = 'ip2region.db'
if (not os.path.isfile(dbFileName)) or (not os.path.exists(dbFileName)):
    print('{} file not found, Can not start server.'.format(dbFileName))
    exit()

dbFile = os.path.join(os.getcwd(), dbFileName)
searcher = Ip2Region(dbFile)


@ip2region.route('/', methods=['GET'])
def index():
    return """
    <h1>IP address to Region, 准确率99.9%的离线IP地址定位, 基于开源项目Ip2region</h1>
    <hr>
    <h2>Usage: http://10.2.67.166:6666/ipaddr/your-ip-address </h2>
    <h2>Return: 国家|区域|省份|城市|ISP</h2>
    <h2>Description: 中国的数据精确到了城市，国外数据定位到国家</h2>
    <hr>
    <h2>Example: http://10.2.67.166:6666/ipaddr/202.108.103.122 </h2>
    <h2>Return: 中国|0|北京|北京市|联通</h2>
    <h2>Example: http://10.2.67.166:6666/ipaddr/8.8.8.8 </h2>
    <h2>Return: 美国|0|0|0|Level3</h2>
    """


@ip2region.route('/ipaddr', methods=['GET'])
@ip2region.route('/ipaddr/', methods=['GET'])
def noipaddr():
    return 'IP address is empty!'


@ip2region.route('/ipaddr/<ip>', methods=['GET'])
def ipaddr(ip):

    result = 'IP address is invaild!'

    if searcher.isip(ip):
        try:
            result = searcher.btreeSearch(ip)['region'].decode('utf-8')
        except Exception as ex:
            result = 'IP2Region search error: ' + str(ex)
        finally:
            return result
    else:
        return result


if __name__ == '__main__':
    ip2region.run(host='0.0.0.0', port='8080', debug=False)

