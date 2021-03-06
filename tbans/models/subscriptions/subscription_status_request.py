from google.appengine.api import urlfetch

from tbans.models.subscriptions.subscription_status import SubscriptionStatus
from tbans.utils.auth_utils import get_firebase_messaging_access_token


class SubscriptionStatusRequest:
    """ Represents a request to Firebase's Instance ID API to get the subscription status for a subscriber

    https://developers.google.com/instance-id/reference/server#get_information_about_app_instances

    Attributes:
        token (string): The Instance ID token for the subscriber.
    """

    def __init__(self, token):
        """
        Args:
            token (string): The Instance ID token for the subscriber - this is the same token as FCM tokens.
        """
        if not isinstance(token, basestring):
            raise ValueError('SubscriptionStatusRequest token option must be a string')

        self.token = token

    def __str__(self):
        return 'SubscriptionStatusRequest(token={})'.format(self.token)

    @property
    def _iid_info_url(self):
        return "https://iid.googleapis.com/iid/info/{}?details=true".format(self.token)

    def send(self):
        """ Attempt to send SubscriptionStatusRequest

        Return:
            SubscriptionStatus
        """
        headers = {
            'Authorization': 'Bearer ' + get_firebase_messaging_access_token(),
        }
        try:
            response = urlfetch.fetch(
                url=self._iid_info_url,
                method='GET',
                headers=headers
            )
            return SubscriptionStatus(response=response)
        except Exception, e:
            # https://cloud.google.com/appengine/docs/standard/python/refdocs/google.appengine.api.urlfetch_errors
            return SubscriptionStatus(error=str(e))
