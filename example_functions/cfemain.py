import json

from pulsar import Function


class EchoFunction(Function):
    def __init__(self):
        self.output_topic = "persistent://cfe-tenant/example-namespace/output-topic"

    @staticmethod
    def is_working(item):
        return True

    def process(self, item, context):
        context.publish(self.output_topic, "Function executing...")
        if self.is_working(item):
            item_json_str = None
            if isinstance(item, str):
                item_json_str = item
            if isinstance(item, bytes):
                try:
                    item_json_str = item.decode("utf-8")
                except Exception as e:
                    warning = f"The {item} had the following exception:\n{e}"
                    context.get_logger().warn(warning)
            if item_json_str:
                data = None
                try:
                    data = json.loads(item_json_str)
                except Exception as e:
                    warning = f"JSON String {item_json_str} had the following exception:\n{e}"
                    context.get_logger().warn(warning)
                if data is not None:
                    context.publish(self.output_topic, json.dumps(data))
                else:
                    invalid_data = {'message': "Input data was not a function"}
                    invalid_data_json = json.dump(invalid_data)
                    context.publish(self.output_topic, f"{invalid_data_json}".encode("utf-8"))
        else:
            warning = "The item {0} is neither a fruit nor a vegetable".format(item)
            context.get_logger().warn(warning)
