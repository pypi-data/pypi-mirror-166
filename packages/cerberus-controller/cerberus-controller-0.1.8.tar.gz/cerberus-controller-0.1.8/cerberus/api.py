import traceback

from json import JSONDecodeError

from cerberus.exceptions import *
from ryu.app.wsgi import ControllerBase, route
from webob import Response, Request

class api(ControllerBase):
    """ API front end for Cerberus.

        Builds on top of Ryu's built in wsgi to
        provide basic API endpoint for Cerberus
    """
    def __init__(self, req, link, data, **config):
        super(api, self).__init__(req, link, data, **config)
        self.app = data['cerberus_main']


    # TODO: Remove this once cerberus becomes more stable
    @route("cerberus", "/api/hello_world", methods=['GET'])
    def hello_world(self, req: Request, **kwargs) -> Response:
        """ Hello world API call for testing purposes

        Args:
            req (Request): Empty GET request

        Returns:
            Response: Test data to retrieve from cerberus main
        """
        self.app.logger.info(f"Hello world was called by:\t{req.host}")
        return Response(content_type='application/json',
                        json=self.app.hello_world())


    @route("cerberus", "/api/switches", methods=['GET'])
    def switches(self, req: Request, **kwargs )-> Response:
        """ GET all the switch objects from cerberus and how they are configured

        Args:
            req (Request): Empty GET request object

        Returns:
            Response: JSON object containing switch objects
        """
        self.app.logger.info(f"Request for switches was called by:\t{req.host}")
        return Response(content_type='application/json',
                        json=self.app.get_switches())


    @route("cerberus", "/api/push_config", methods=['PUT'])
    def push_new_config(self, req: Request, **kwargs) -> Response:
        """ PUT request that contains new configuration to be used in cerberus

        Args:
            req (Request): Request containing candidate config file as JSON

        Returns:
            Response: If any changes were made and if they were applied successfully
        """
        self.app.logger.info(f"A config update was sent in by:\t{req.host}")
        try:
            if not req.body:
                err_msg = ("The request body was empty. Ensure that the new "
                           "configuration is attached to your PUT Request. "
                           "There was no configuration pushed to the network.")
                raise EmptyConfigError(err_msg)
            return Response(content_type='application/json',
                            json=self.app.push_new_config(req.body))
        except EmptyConfigError as err:
            return Response(status=500, json={"error": str(err)})
        except:
            return Response(status=500,
                            json={"error": traceback.format_exc()})


    @route("cerberus", "/api/get_config", methods=['GET'])
    def get_running_config(self, req: Request, **kwargs) -> Response:
        """ Get the current running configuration file

        Args:
            req (Request): Get request

        Returns:
            Response: JSON response of config file
        """
        self.app.logger.info(f"Request for switches was called by:\t{req.host}")
        try:
            return Response(content_type='application/json',
                            json=self.app.get_running_config_file())
        except:
            return Response(status=500, json={"error": traceback.format_exc()})


    @route("cerberus", "/api/get_full_config", methods=['GET'])
    def get_full_config(self, req: Request, **kwargs) -> Response:
        """ Returns the full config. Primarily for debugging purposes.

        Args:
            req (Request): Get Request

        Returns:
            Response: Response containing the full config in cerberus
        """
        self.app.logger.info(f"Request for full config was called by:\t{req.host}")
        try:
            return Response(content_type='application/json',
                            json=self.app.get_running_config())
        except:
            return Response(status=500, json={"error": traceback.format_exc()})


    @route("cerberus", "/api/rollback_to_last_config")
    def rollback_to_last_config(self, req: Request, **kwargs) -> Response:

        self.app.logger.info(f"Request to rollback to last config was called by:\t{req.host}")
        try:
            return Response(content_type='application/json',
                            json=self.app.api_rollback_to_last_config())
        except:
            return Response(status=500, json={"error": traceback.format_exc()})


    @route("cerberus", "/api/set_debug_flow_state", methods=['PUT'])
    def set_debug_packet_flow_state(self, req: Request, **kwargs) -> Response:

        self.app.logger.info(f"Request to set debug packet flow was called"
                             f" by:\t{req.host}")

        try:
            return Response(content_type='application/json',
                            json=self.app.set_debug_packet_flow_state(req.json))
        except JSONDecodeError:
            self.app.logger.info(f"Failed to set debug packet flow from "
                                 f"{req.host} due to a JSONDecodeError. "
                                 f"The request sent was {req.text}")
            return Response(status=500, json={
                "error": "Ensure that request is in a json format"})
        except:
            return Response(status=500, json={"error": traceback.format_exc()})