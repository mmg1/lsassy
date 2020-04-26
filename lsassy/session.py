import logging
from impacket.smbconnection import SMBConnection


class Session:
    def __init__(self, smb_session=None):
        self.smb_session = smb_session
        self.address = ""
        self.target_ip = ""
        self.port = 445
        self.username = ""
        self.password = ""
        self.lmhash = ""
        self.nthash = ""
        self.domain = ""
        self.aesKey = ""
        self.dc_ip = ""
        self.kerberos = False

    def get_session(self, address, target_ip="", port=445, username="", password="", lmhash="", nthash="", domain="", aesKey="", dc_ip="", kerberos=False):
        try:
            self.smb_session = SMBConnection(address, target_ip, sess_port=port, timeout=5)
            if kerberos is True:
                self.smb_session.kerberosLogin(username, password, domain, lmhash, nthash, aesKey, dc_ip)
            else:
                self.smb_session.login(username, password, domain, lmhash, nthash)
            logging.info("SMB session opened")
        except Exception as e:
            logging.warning("Connexion error", exc_info=True)
            self.smb_session = None
            return None

        try:
            self.smb_session.connectTree("C$")
        except Exception:
            if username:
                logging.error("User '{}' can not access admin shares on {}".format(username, address))
            else:
                logging.error("Can not access admin shares on {}".format(address))
            self.smb_session = None
            return None

        self.address = address
        self.target_ip = target_ip
        self.port = port
        self.username = username
        self.password = password
        self.lmhash = lmhash
        self.nthash = nthash
        self.domain = domain
        self.aesKey = aesKey
        self.dc_ip = dc_ip
        self.kerberos = kerberos

        logging.success("Authentication successful")
