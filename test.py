import hashlib, hmac, subprocess, sys, os, shlex
import unittest


class WebhookTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_sig(self):
        body = '{"eventKey":"repo:refs_changed","date":"2018-02-15T23:50:44+1100","actor":{"name":"admin",' \
               '"emailAddress":"victorlin21@gmail.com","id":1,"displayName":"Admin","active":true,"slug":"admin",' \
               '"type":"NORMAL"},"repository":{"slug":"alpha","id":1,"name":"alpha","scmId":"git",' \
               '"state":"AVAILABLE","statusMessage":"Available","forkable":true,"project":{"key":"TEST","id":1,' \
               '"name":"TEST","public":false,"type":"NORMAL"},"public":false},"changes":[{"ref":{' \
               '"id":"refs/heads/master","displayId":"master","type":"BRANCH"},"refId":"refs/heads/master",' \
               '"fromHash":"d18f7ac3fc1442e62cc29418cae498d2f35e91fa",' \
               '"toHash":"1e88ff54ed80e2cf5d0463e16e12280ec032c3e8","type":"UPDATE"}]}'
        out = hmac.new('hello', body, hashlib.sha256).hexdigest()
        print 'test_sig: ' + out
        # X-Hub-Signature: sha256=8e4a9bed436468cb73badf81029e9ed0526bac10326011da2893d2d7ac1b483d
        self.assertEquals('8e4a9bed436468cb73badf81029e9ed0526bac10326011da2893d2d7ac1b483d', out)

    @staticmethod
    def test_pipeline():
        working_dir = os.path.dirname(os.path.realpath(__file__))
        print 'working_dir: ' + working_dir
        cmd = shlex.split('bash pipeline.sh')
        process = subprocess.Popen(cmd, cwd=working_dir, stdout=subprocess.PIPE)
        for c in iter(lambda: process.stdout.read(1), ''):
            sys.stdout.write(c)


if __name__ == '__main__':
    unittest.main(failfast=True)
