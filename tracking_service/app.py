from spyne import *
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server
import requests

BASE_URL = 'http://127.0.0.1:9999/'

ComplexModel.Attributes.declare_order = "declared"

class TrackingRequest(ComplexModel):
    secret_key = String
    order_unique_id = String


class TrackingResponse(ComplexModel):
    status = String
    current_location = String
    additional_detail = String


class TrackingService(ServiceBase):
    @rpc(Iterable(TrackingRequest), _returns=TrackingResponse)
    def get_tracking(ctx, tracking_request):
        tracking_request = list(tracking_request)
        response = requests.get(BASE_URL + "order/" + tracking_request[0].order_unique_id, headers={'Authorization' : tracking_request[0].secret_key}).json()
        all_points = [x for x in response['points']]
        points = list(filter(lambda x: x['status'], [x for x in response['points']]))
        if response.get('error'):
            return TrackingResponse(
                status = "Fail: "+response.get('error'),
                current_location = "error",
                additional_detail = "error"
            )
        else:
            return TrackingResponse(
                status = str(len(points))+"/"+str(len(all_points))+" have been delivered",
                current_location = "{"+str(response['points'][0]['to_lat'])+"}, {"+str(response['points'][0]['to_lng'])+"}",
                additional_detail = response['points'][0]['status']
            )


tracking_app = Application([TrackingService],
                              tns='soa.logistic.tracking',
                              in_protocol=Soap11(validator='lxml'),
                              out_protocol=Soap11()
)

wsgi_tracking = WsgiApplication(tracking_app)
tracking_server = make_server('0.0.0.0', 5007, wsgi_tracking)