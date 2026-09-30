import unittest
from recursive_json_search import json_search
from test_data import key1, key2, data

class json_search_test(unittest.TestCase):
    '''test module to test search function in `recursive_json_search.py`'''

    def test_search_found(self):
        '''key should be found, return list should not be empty'''
        self.assertNotEqual([], json_search(key1, data, role="viewer"))

    def test_search_not_found(self):
        '''key should not be found, should return an empty list'''
        self.assertEqual([], json_search(key2, data, role="admin"))

    def test_is_a_list(self):
        '''Should return a list'''
        self.assertIsInstance(json_search(key1, data, role="viewer"), list)

    def test_wrong_role_cannot_read_secret(self):
        '''SR-1: viewer and operator must not read apiKey'''
        self.assertEqual([], json_search("apiKey", data, role="viewer"))
        self.assertEqual([], json_search("apiKey", data, role="operator"))

    def test_no_role_or_unknown_role_denied(self):
        '''SR-2: role=None or unknown role is denied (fail-closed)'''
        self.assertEqual([], json_search("apiKey", data))
        self.assertEqual([], json_search("apiKey", data, role="hacker"))
        self.assertEqual([], json_search("managementIpAddress", data, role="viewer"))

    def test_no_secret_leak_via_parent_key(self):
        '''SR-3: searching a parent key must not leak apiKey to low roles'''
        result = json_search("deviceDetails", data, role="viewer")
        self.assertNotIn("SNMP-COMMUNITY-STRING", str(result))
        self.assertNotIn("10.10.20.21", str(result))

    def test_allowed_roles_can_read(self):
        '''Allowed roles still get their data'''
        self.assertNotEqual([], json_search("apiKey", data, role="admin"))
        self.assertNotEqual([], json_search("managementIpAddress", data, role="operator"))

if __name__ == '__main__':
    unittest.main()
