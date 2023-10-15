from twisted.internet import protocol, reactor, endpoints
from twisted.protocols import ftp
from twisted.cred.portal import Portal
from twisted.cred.checkers import AllowAnonymousAccess, FilePasswordDB, InMemoryUsernamePasswordDatabaseDontUse
from twisted.conch import error, ssh
from twisted.conch.ssh import factory, keys, session
from twisted.python import log
import sys

# Initialize logging
log.startLogging(sys.stdout)


class FakeFTPServer(ftp.FTP):
    def ftp_USER(self, params):
        self.sendLine('331 Password required')
        return True

    def ftp_PASS(self, params):
        self.sendLine('530 Authentication failed')
        return True


class FakeSSHServer(ssh.SSHServerTransport):

    def verifyPassword(self, password):
        # More sophisticated authentication mechanism here if desired
        return False

    def verifyKey(self, key):
        return False

    def ssh_USERAUTH_REQUEST(self, packet):
        user = self.parsePacket(packet, 's')[0]
        if user == "root":
            self.transport.write(error.ConchError())
            self.transport.loseConnection()
        else:
            super(FakeSSHServer, self).ssh_USERAUTH_REQUEST(packet)


class SimpleSSHRealm:
    def requestAvatar(self, avatarId, mind, *interfaces):
        return session.SSHSession, session.SSHSession(), lambda: None


def run_servers(ftp_port=2121, ssh_port=2222, pub_key="YOUR_PUBLIC_KEY", priv_key="YOUR_PRIVATE_KEY"):

    # FTP Server
    ftp_factory = protocol.Factory()
    ftp_factory.protocol = FakeFTPServer
    ftp_portal = Portal(ftp_factory)
    ftp_portal.registerChecker(AllowAnonymousAccess())
    ftp_factory.portal = ftp_portal
    reactor.listenTCP(ftp_port, ftp_factory)

    # SSH Server
    ssh_factory = factory.SSHFactory()
    ssh_factory.portal = Portal(SimpleSSHRealm(), [InMemoryUsernamePasswordDatabaseDontUse(admin="password")])  # Basic user/pass check
    ssh_factory.publicKeys = {
        "ssh-rsa": keys.Key.fromString(data=pub_key)
    }
    ssh_factory.privateKeys = {
        "ssh-rsa": keys.Key.fromString(data=priv_key)
    }
    reactor.listenTCP(ssh_port, ssh_factory)

    reactor.run()


if __name__ == "__main__":
    run_servers()
