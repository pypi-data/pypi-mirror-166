class Map:
    JUNCTION = "junction"
    ROAD = "road"
    LANE = "lane"

    def __init__(self, hd_map_path):
        self.road_dict = {}
        self.junction_dict = {}

        import xml.etree.ElementTree as ET
        hd_map = open(hd_map_path, 'r')
        hd_map_str = hd_map.read()
        hd_map.close()

        sim_map_tree = ET.fromstring(hd_map_str)

        for junction in sim_map_tree.findall("junction"):
            self.junction_dict[junction.get("id")] = self.Junction(junction.get("id"), {}, {})

        for road in sim_map_tree.findall("road"):
            lane_dict = {}
            if road.get("junction") == "-1":
                for lanes in road.findall("lanes"):
                    for lane_section in lanes.findall("laneSection"):
                        if lane_section.find("left") is not None:
                            for lane in lane_section.find("left").findall("lane"):
                                lane_dict[lane.get("id")] = self.Lane(lane.get("id"), lane.get("type"), road.get("id"))
                        # if lane_section.find("center") is not None:
                        #     for lane in lane_section.find("center").findall("lane"):
                        #         lane_dict.append(self.Lane(lane.get("id"), lane.get("type"), road.get("id")))
                        if lane_section.find("right") is not None:
                            for lane in lane_section.find("right").findall("lane"):
                                lane_dict[lane.get("id")] = self.Lane(lane.get("id"), lane.get("type"), road.get("id"))

                self.road_dict[road.get("id")] \
                    = self.Road(road.get("id"), lane_dict,
                                road.find("link").find("predecessor").get("elementType"),
                                road.find("link").find("predecessor").get("elementId"),
                                road.find("link").find("successor").get("elementType"),
                                road.find("link").find("successor").get("elementId"))

            else:
                for lanes in road.findall("lanes"):
                    for lane_section in lanes.findall("laneSection"):
                        if lane_section.find("left") is not None:
                            for lane in lane_section.find("left").findall("lane"):
                                lane_dict[lane.get("id")] \
                                    = self.JunctionLane(lane.get("id"), lane.get("type"), road.get("id"),
                                                        lane.find("link").find("predecessor").get("id"),
                                                        lane.find("link").find("successor").get("id"))
                        if lane_section.find("right") is not None:
                            for lane in lane_section.find("right").findall("lane"):
                                lane_dict[lane.get("id")] \
                                    = self.JunctionLane(lane.get("id"), lane.get("type"), road.get("id"),
                                                        lane.find("link").find("predecessor").get("id"),
                                                        lane.find("link").find("successor").get("id"))

                self.road_dict[road.get("id")] \
                    = self.JunctionRoad(road.get("id"), lane_dict, road.get("junction"),
                                        road.find("link").find("predecessor").get("elementType"),
                                        road.find("link").find("predecessor").get("elementId"),
                                        road.find("link").find("successor").get("elementType"),
                                        road.find("link").find("successor").get("elementId"))

                self.junction_dict[road.get("junction")].child[road.get("id")] = self.road_dict[road.get("id")]

            if road.find("link").find("predecessor").get("elementType") == "junction":
                self.junction_dict[road.find("link").find("predecessor").get("elementId")] \
                    .connection[road.get("id")] = self.road_dict[road.get("id")]

            if road.find("link").find("successor").get("elementType") == "junction":
                self.junction_dict[road.find("link").find("successor").get("elementId")] \
                    .connection[road.get("id")] = self.road_dict[road.get("id")]

    class Junction:
        def __init__(self, j_id, child_road_dict, conn_dict):
            self.id = j_id
            self.child = child_road_dict
            self.connection = conn_dict

    class Road:
        def __init__(self, r_id, lane_list, prev_type, prev_id, next_type, next_id):
            self.id = r_id
            self.prev_type = prev_type
            self.prev_id = prev_id
            self.next_type = next_type
            self.next_id = next_id
            self.child = lane_list

    class JunctionRoad:
        def __init__(self, r_id, lane_dict, junction_id, prev_type, prev_id, next_type, next_id):
            self.id = r_id
            self.parent = junction_id
            self.prev_type = prev_type
            self.prev_id = prev_id
            self.next_type = next_type
            self.next_id = next_id
            self.child = lane_dict

    class Lane:
        def __init__(self, l_id, l_type, road_id):
            self.id = l_id
            self.type = l_type
            self.parent = road_id

    class JunctionLane:
        def __init__(self, l_id, l_type, road_id, prev_lane_id, next_lane_id):
            self.id = l_id
            self.type = l_type
            self.parent = road_id
            self.prev = prev_lane_id
            self.next = next_lane_id


# road_graph = Map("/home/dk-kling/Projects/HDMap2RoadGraph/HD-Map/Town02.xodr")
road_graph = Map("/HD-Map/Town02.xodr")
print("bp")
