# coding=gbk

# coding=utf-8

# -*- coding: UTF-8 -*-

from iHome.libs.CloudConnectSDK.CCPRestSDK import REST

# ���ʺ�
accountSid = '8a216da8627648690162843848320291'

# ���ʺ�Token
accountToken = '62164fc602904a3cb67732eec6308977'

# Ӧ��Id
appId = '8a216da86276486901628438488b0297'

# �����ַ����ʽ���£�����Ҫдhttp://
serverIP = 'app.cloopen.com'

# ����˿�
serverPort = '8883'

# REST�汾��
softVersion = '2013-12-26'

# ���Դ���

# ����ģ�����
# @param to �ֻ�����
# @param datas �������� ��ʽΪ���� ���磺{'12','34'}���粻���滻���� ''
# @param $tempId ģ��Id

# def sendTemplateSMS(to, datas, tempId):
#
#     # ��ʼ��REST SDK
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
    # ��д__new__����ʵ�ֳ�ʼ������
    def __new__(cls, *args, **kwargs):
        # print type(SendSMS)
        # print type(cls)
        if not hasattr(cls, '_instance'):
            cls._instance = super(SendSMS, cls).__new__(cls, *args, **kwargs)
        # print type(cls._instance)
        return cls._instance  # ����classobj�����ڴ���ʵ������

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


# ���Ͷ��Ų���SDK
if __name__ == '__main__':
    # SendSMS().send_template_sms('13189719899', {'12580', '5'}, '1')
    SendSMS().check()
