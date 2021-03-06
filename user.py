import time


class BannedUser:
    """ Class representing a banned user. """
    def __init__(self, **kwargs):
        self.ban_id = kwargs.get('id', 0)
        self.nick = kwargs.get('nick', '')
        self.req_id = kwargs.get('req', 0)
        self.success = kwargs.get('success', False)
        self.account = kwargs.get('username', '')
        self.banned_by = kwargs.get('moderator', '')
        self.reason = kwargs.get('reason', '')
        self.ban_time = time.time()


class User:
    """ Class representing a user. """
    def __init__(self, **kwargs):
        self.id = kwargs.get('handle')
        self.nick = kwargs.get('nick', '')
        self.account = kwargs.get('username', '')
        self.giftpoints = kwargs.get('giftpoints', 0)
        self.featured = kwargs.get('featured', False)
        self.subscription = kwargs.get('subscription', 0)
        self.achievement_url = kwargs.get('achievement_url', '')
        self.avatar = kwargs.get('avatar', '')
        self.is_lurker = kwargs.get('lurker', False)
        self.is_mod = kwargs.get('mod', False)
        self.is_owner = kwargs.get('owner', False)
        self.is_broadcasting = False
        self.is_waiting = False
        #
        self.user_level = 5
        self.join_time = time.time()
        self.tinychat_id = None
        self.last_login = None
        self.last_msg = None
        self.msg_time = 0.0


class Users:
    """ Class for doing various user related operations. """
    def __init__(self):
        """
        Initialize the Users class.
        
        Creating a dictionary for users and one for banned users.
        """
        self._users = dict()
        self._banned_users = dict()

    @property
    def all(self):
        """
        Returns a dictionary of all the users.
        
        :return: A dictionary where the key is the user ID and the value is User.
        :rtype: dict
        """
        return self._users

    @property
    def mods(self):
        """
        Returns a list of all the moderators.
        
        :return: A list of moderator User.
        :rtype: list
        """
        _mods = []
        for user in self.all:
            if self.all[user].is_mod:
                _mods.append(self.all[user])
        return _mods

    @property
    def signed_in(self):
        """
        Returns a list of all signed in users.
        
        :return: A list of all the signed in User
        :rtype: list
        """
        _signed_ins = []
        for user in self.all:
            if self.all[user].account:
                _signed_ins.append(self.all[user])
        return _signed_ins

    @property
    def lurkers(self):
        """
        Returns a list of the lurkers.
        
        :return: A list of lurkers User.
        :rtype: list
        """
        _lurkers = []
        for user in self.all:
            if self.all[user].is_lurker:
                _lurkers.append(self.all[user])
        return _lurkers

    @property
    def norms(self):
        """
        Returns a list of all normal users, e.g users that are not moderators or lurkers.
        
        :return: A list of all normal User.
        :rtype: list
        """
        _regulars = []
        for user in self.all:
            if not self.all[user].is_mod and not self.all[user].is_lurker:
                _regulars.append(self.all[user])
        return _regulars

    @property
    def broadcaster(self):
        """
        Returns a list of all broadcasting users.
        
        :return: A list of all the broadcasting User.
        :rtype: list
        """
        _broadcasters = []
        for user in self.all:
            if self.all[user].is_broadcasting:
                _broadcasters.append(self.all[user])
        return _broadcasters

    def clear(self):
        """ Clear the user dictionary. """
        self._users.clear()

    def add(self, user_info):
        """
        Add a user to the user dictionary.
        
        :param user_info: User information data.
        :type user_info: dict
        :return: The user as User.
        :rtype: User
        """
        if user_info['handle'] not in self.all:
            self._users[user_info['handle']] = User(**user_info)
        return self.all[user_info['handle']]

    def delete(self, handle_id):
        """
        Delete a user from the user dictionary.
        
        :param handle_id: The id (handle) of the user to delete.
        :type handle_id: int
        :return: The User of the deleted user or None if the ID was not found.
        :rtype: User | None
        """
        if handle_id in self.all:
            user = self._users[handle_id]
            del self._users[handle_id]
            return user
        return None

    def search(self, handle_id):
        """
        Search the user dictionary by ID.
        
        This is the primary search method, since the user ID (handle) is
        present in all(?) user related events.
        
        :param handle_id: The ID of the user to find.
        :type handle_id: int
        :return: The User or None if not found.
        :rtype: User | None
        """
        if handle_id in self.all:
            return self.all[handle_id]
        return None

    def search_by_nick(self, nick):
        """
        Search the user dictionary by nick name.
        
        :param nick: The nick name of the user to search for.
        :type nick: str
        :return: The User or None if not found.
        :rtype: User | None
        """
        for user in self.all:
            if self.all[user].nick == nick:
                return self.all[user]
        return None

    def search_containing(self, contains):
        """
        Search the user dictionary for nick names matching the search string.
        
        :param contains: The search string to search for in the nick names.
        :type contains: str
        :return: A list of User matching the search string.
        :rtype: list
        """
        _users_containing = []
        for user in self.all:
            if str(contains) in self.all[user].nick:
                _users_containing.append(self.all[user])
        return _users_containing

    # Ban related. This is still a work in progress.
    # It has not been fully implemented in the code.
    @property
    def banlist(self):
        """
        Returns a dictionary of all banned users.
        
        :return: A dictionary where the key is the ban ID and the value is BannedUser.
        :rtype: dict
        """
        return self._banned_users

    @property
    def banned_accounts(self):
        """
        Returns a list of BannedUser account name.
        
        :return: A list of BannedUser containing account name. 
        :rtype: list
        """
        _accounts = []
        for ban_id in self.banlist:
            if self.banlist[ban_id].account:
                _accounts.append(self.banlist[ban_id])
        return _accounts

    def add_banned_user(self, ban_info):
        """
        Add a user to the banned user dictionary.
        
        :param ban_info: The banned user's ban information.
        :type ban_info: dict
        :return: A BannedUser.
        :rtype: BannedUser
        """
        # if not ban_info['id']:
        #     ban_info['id'] = 0
        if ban_info['id'] not in self.banlist:
            self._banned_users[ban_info['id']] = BannedUser(**ban_info)
        return self.banlist[ban_info['id']]

    def delete_banned_user(self, ban_info):  # TODO: Maybe change this to delete by ban id only.
        """
        Delete a banned user from the banned user dictionary.
        
        :param ban_info: The banned user's ban information.
        :type ban_info: dict
        :return: The BannedUser or None if not in the dictionary.
        :rtype: BannedUser | None
        """
        if ban_info['id'] in self.banlist:
            banned_user = self.banlist[ban_info['id']]
            del self._banned_users[ban_info['id']]
            return banned_user
        return None

    def clear_banlist(self):
        """ Clear the ban list. """
        self._banned_users.clear()

    def search_banlist(self, ban_id):
        """
        Search the banlist dictionary by ban ID.
        
        :param ban_id: The ban ID to search for.
        :type ban_id: int
        :return: A BannedUser or None if not found.
        :rtype: BannedUser | None
        """
        if ban_id in self.banlist:
            return self.banlist[ban_id]
        return None

    def search_banlist_by_nick(self, nick):
        pass

    def search_banlist_by_req_id(self, req_id):
        """
        Search the banned user dictionary by req ID.
        
        :param req_id: The req ID to search for.
        :type req_id: int
        :return: A BannedUser matching the req ID or None if not found.
        :rtype: BannedUser | None
        """
        for ban_id in self.banlist:
            if self.banlist[ban_id].req_id == req_id:
                return self.banlist[ban_id]
        return None
