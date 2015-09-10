import json
from time import time

import rules
from ipware.ip import get_real_ip

from .models import Limit


@rules.predicate
def is_same_person(user, target_user):
    return user == target_user


def rate_limit_by_cookie(action, limit=1, seconds=3600):
    @rules.predicate(bind=True)
    def request_rate_limit_by_cookie(self, user, request):
        if user.is_authenticated():
            self.skip()
        now = time()
        key = "{}:{}".format(action, request.path)
        try:
            last_action = json.loads(request.session.get(key))
            assert ((now - last_action["timestamp"]) <= seconds)
        except:
            last_action = {
                "count": 0,
                "timestamp": time()
            }

        if last_action["count"] >= limit:
            return False

        last_action["count"] += 1
        request.session[key] = json.dumps(last_action)
        return True

    return request_rate_limit_by_cookie


def rate_limit_by_user(action, limit=1, seconds=3600):
    @rules.predicate(bind=True)
    def request_rate_limit_by_user(self, user, request):
        if not user.is_authenticated():
            self.skip()

        now = time()
        key = "{}:{}".format(action, request.path)
        try:
            user_action = Limit.objects.get(action=key, user=user)
            seconds_since_last_executon = now - user_action.last_executed_timestamp
            if seconds_since_last_executon > seconds:
                user_action.count = 0
                user_action.last_executed_timestamp = time()
        except:
            user_action = Limit(action=key, user=user, last_executed_timestamp=time(), count=0)

        if user_action.count >= limit:
            return False

        user_action.count += 1
        user_action.save()
        return True

    return request_rate_limit_by_user


def rate_limit_by_ip(action, limit=1, seconds=3600):
    @rules.predicate(bind=True)
    def request_rate_limit_by_ip(self, user, request):
        if user.is_authenticated():
            self.skip()
        ip = get_real_ip(request)
        if ip is None:
            self.skip()

        now = time()
        try:
            user_action = Limit.objects.get(action=action, ip=ip)
            seconds_since_last_executon = now - user_action.last_executed_timestamp
            if seconds_since_last_executon > seconds:
                user_action.count = 0
                user_action.last_executed_timestamp = time()
        except:
            user_action = Limit(action=action, ip=ip, last_executed_timestamp=time(), count=0)

        if user_action.count >= limit:
            return False

        user_action.count += 1
        user_action.save()
        return True

    return request_rate_limit_by_ip
