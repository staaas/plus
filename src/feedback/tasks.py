from sleekxmpp import ClientXMPP
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.conf import settings


class FeedbackBot(ClientXMPP):

    """
    A basic SleekXMPP bot that will log in, send a message,
    and then log out.
    """

    def __init__(self, message):
        ClientXMPP.__init__(self, settings.FEEDBACK_SENDER_JID,
                            settings.FEEDBACK_SENDER_PWD)

        self.msg = message

        # The session_start event will be triggered when
        # the bot establishes its connection with the server
        # and the XML streams are ready for use. We want to
        # listen for this event so that we we can intialize
        # our roster.
        self.add_event_handler("session_start", self.start)

    def start(self, event):
        self.send_presence()
        self.get_roster()

        for jid in settings.FEEDBACK_RECIPIENT_JIDS:
            self.send_message(mto=jid, mbody=self.msg, mtype='chat')

        # Using wait=True ensures that the send queue will be
        # emptied before ending the session.
        self.disconnect(wait=True)

def send_xmpp(text):
    xmpp = FeedbackBot(text)
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0199') # XMPP Ping
    if xmpp.connect():
        xmpp.process(threaded=False)
    else:
        raise Exception('Couldn\'t send feedback via XMPP')

class FeedbackTask(object):
    queue = 'messaging'

    @staticmethod
    def perform(name, email, text):
        current_site = Site.objects.get_current()
        domain = current_site.domain.upper()

        jabber_text = '[FEEDBACK / %s]\nFrom: %s <%s>\n%s' % (
            domain, name, email, text)
        send_xmpp(jabber_text)

        subj = '[FEEDBACK / %s] %s' % (domain, name)
        email_acc = '%s@%s ' % (settings.EMAIL_HOST_USER,
                                settings.EMAIL_HOST)
        mail_text = 'Feedback from %(sender)s\n'\
            '-----------------------\n%(text)s' % {
            'text': text, 'sender': "%s <%s>" % (name, email)}
        EmailMessage(subj, mail_text, email_acc,
            settings.FEEDBACK_RECIPIENT_EMAILS, [],
            headers = {'Reply-To': email}).send()

