# localslackirc
# Copyright (C) 2021 Antonio Terceiro
#
# localslackirc is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest

from msgparsing import preblocks, split_tokens, SpecialItem, Itemkind


class TestMsgParsing(unittest.TestCase):

    def test_preblocks(self):
        assert list(preblocks('')) == [('', False)]
        assert list(preblocks('asd')) == [('asd', False)]
        assert list(preblocks('a ```a``` a')) == [('a ', False), ('a', True), (' a', False)]
        assert list(preblocks('```a``` a')) == [('', False), ('a', True), (' a', False)]
        assert list(preblocks('```a')) == [('', False), ('a', True)]

    def test_split_tokens(self):
        assert list(split_tokens('a b c d')) == ['a b c d']
        assert list(split_tokens('a <b> <c> d')) == ['a ', SpecialItem('<b>'), ' ', SpecialItem('<c>'), ' d']

    def test_special_item(self):
        c = SpecialItem('<@ciccio>')
        assert c.kind == Itemkind.MENTION
        assert c.human is None
        assert c.val == 'ciccio'

        c = SpecialItem('<http://ciccio|link>')
        assert c.kind == Itemkind.OTHER
        assert c.human == 'link'
        assert c.val == 'http://ciccio'

        c = SpecialItem('<#ciccio>')
        assert c.kind == Itemkind.CHANNEL
        assert c.human is None
        assert c.val == 'ciccio'

        c = SpecialItem('<!here>')
        assert c.kind == Itemkind.GROUPMENTION
        assert c.human is None
        assert c.val == 'here'
