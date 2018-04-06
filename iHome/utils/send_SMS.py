# coding=gbk

# coding=utf-8

# -*- coding: UTF-8 -*-

from iHome.libs.CloudConnectSDK.CCPRestSDK import REST

# 主帐号
accountSid = '8a216da8627648690162843848320291'

# 主帐号Token
accountToken = '62164fc602904a3cb67732eec6308977'

# 应用Id
appId = '8a216da86276486901628438488b0297'

# 请求地址，格式如下，不需要写http://
serverIP = 'app.cloopen.com'

# 请求端口
serverPort = '8883'

# REST版本号
softVersion = '2013-12-26'

# 测试代码

# 发送模板短信
# @param to 手机号码
# @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
# @param $tempId 模板Id

# def sendTemplateSMS(to, datas, tempId):
#
#     # 初始化REST SDK
#     rest = REST(serverIP, serverPort, softVersion)
#     rest.setAccount(accountSid, accountToken)
#     rest.setAppId(appId)
#
#     result = rest.sendTemplateSMS(to, datas, tempId)
#     for k, v in result.iteritems():
#
#         if k == 'templateSMS':
#             for k, s in v.iteritems():
#                 print '%s:%s' % (k, s)
#         else:
#             print '%s:%s' % (k, v)
#
#
# # sendTemplateSMS('13189719899', {'12580', '5'}, '1')


class SendSMS(REST, object):
    # 重写__new__方法实现初始化单例
    def __new__(cls, *args, **kwargs):
        # print type(SendSMS)
        # print type(cls)
        if not hasattr(cls, '_instance'):
            cls._instance = super(SendSMS, cls).__new__(cls, *args, **kwargs)
        # print type(cls._instance)
        return cls._instance  # 返回classobj，用于创建实例对象

    def __init__(self):
        # REST.__init__(self, serverIP, serverPort, softVersion)
        # print type(self)
        super(SendSMS, self).__init__(serverIP, serverPort, softVersion)
        self.setAccount(accountSid, accountToken)
        self.setAppId(appId)

    def send_template_sms(self, to, code, expires, temp_id):
        print {code, expires}
        # result = self.sendTemplateSMS(to, {code, expires}, temp_id)
        result = {'statusCode': '000000'}
        if result.get('statusCode') == '000000':
            return 0
        else:
            for k, v in result.iteritems():
                if k == 'templateSMS':
                    for k, s in v.iteritems():
                        print '%s:%s' % (k, s)
                else:
                    print '%s:%s' % (k, v)
            return 1

    def check(self):
        print 'ok', self.ServerIP, self.SoftVersion


# 发送短信测试SDK
if __name__ == '__main__':
    # SendSMS().send_template_sms('13189719899', {'12580', '5'}, '1')
    SendSMS().check()
