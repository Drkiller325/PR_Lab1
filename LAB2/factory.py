from player import Player
import json
import xml.etree.ElementTree as ET

class PlayerFactory:
    def to_json(self, players):
        '''
            This function should transform a list of Player objects into a list with dictionaries.
        '''
        Json_list = []
        for player in players:
            player.date_of_birth = player.date_of_birth.strftime("%Y-%m-%d")
            player_dict = {
                "nickname": player.nickname
                , "email": player.email
                , "date_of_birth": player.date_of_birth
                , "xp": player.xp
                , "class": player.cls
            }
            Json_list.append(player_dict)
        return Json_list
        pass

    def from_json(self, list_of_dict):
        '''
            This function should transform a list of dictionaries into a list with Player objects.
        '''
        player_list = []
        for d in list_of_dict:
            player = Player(d["nickname"], d["email"], d["date_of_birth"], d["xp"], d["class"])
            player_list.append(player)
        return player_list
        pass

    def from_xml(self, xml_string):
        '''
            This function should transform a XML string into a list with Player objects.
        '''

        root = ET.fromstring(xml_string)

        def xml_element_to_dict(element):
            result = {}
            for sub_element in element:
                if len(sub_element) > 0:
                    result[sub_element.tag] = xml_element_to_dict(sub_element)
                else:
                    result[sub_element.tag] = sub_element.text
            return result

        result_list = [xml_element_to_dict(item) for item in root.findall(".//player")]

        player_list = []
        for d in result_list:
            player = Player(d["nickname"], d["email"], d["date_of_birth"], int(d["xp"]), d["class"])
            player_list.append(player)
        return player_list

    def to_xml(self, list_of_players):
        '''
            This function should transform a list with Player objects into a XML string.
        '''

        def dict_to_xml(dictionary, root_name='player'):
            root = ET.Element(root_name)
            for key, value in dictionary.items():
                if isinstance(value, dict):
                    element = dict_to_xml(value, key)
                else:
                    element = ET.Element(key)
                    element.text = str(value)
                root.append(element)
            return root

        dict_list = []
        for player in list_of_players:
            player.date_of_birth = player.date_of_birth.strftime("%Y-%m-%d")
            player_dict = {
                "nickname": player.nickname
                , "email": player.email
                , "date_of_birth": player.date_of_birth
                , "xp": player.xp
                , "class": player.cls

            }
            dict_list.append(player_dict)

        root = ET.Element("data")
        for data_dict in dict_list:
            root.append(dict_to_xml(data_dict))

        xml_string = ET.tostring(root, encoding="utf-8").decode("utf-8")

        return xml_string

    def from_protobuf(self, binary):
        '''
            This function should transform a binary protobuf string into a list with Player objects.
        '''
        import player_pb2

        players = player_pb2.PlayersList()

        players.ParseFromString(binary)

        player_list = []
        for player in players.player:
            p = Player(player.nickname,player.email,player.date_of_birth,player.xp,player.cls)
            if player.cls == 0:
                p.cls = "Berserk"
            elif player.cls == 1:
                p.cls = "Tank"
            elif player.cls == 3:
                p.cls = "Paladin"
            elif player.cls == 4:
                p.cls = "Mage"
            player_list.append(p)

        return player_list


    def to_protobuf(self, list_of_players):
        '''
            This function should transform a list with Player objects intoa binary protobuf string.
        '''
        import player_pb2

        players = player_pb2.PlayersList()
        for object in list_of_players:
            player = players.player.add()
            player.nickname = object.nickname
            player.email = object.email
            player.date_of_birth = object.date_of_birth.strftime("%Y-%m-%d")
            player.xp = object.xp
            player.cls = object.cls

        serialized_data = players.SerializeToString()


        return serialized_data



        pass
