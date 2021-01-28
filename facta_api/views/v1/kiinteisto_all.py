from rest_framework.views import APIView  # pip install django-rest-framework
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, \
    HttpResponseNotFound, HttpResponseForbidden, HttpResponseServerError
from drf_spectacular.openapi import AutoSchema
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
import logging
import lxml.etree as etree
from ..serializers.v1 import KiinteistonDataV1Serializer
from facta_api import hel_facta
from .kiinteisto import KiinteistoAPI

log = logging.getLogger(__name__)


class API(KiinteistoAPI):
    serializer_class = KiinteistonDataV1Serializer

    def get(self, request, kiinteistotunnus=None):
        if not kiinteistotunnus:
            return HttpResponseBadRequest("Need kiinteistotunnus!")

        ktunnus_to_use = self._format_kiinteistotunnus(kiinteistotunnus)
        if not ktunnus_to_use:
            return HttpResponseBadRequest("Need valid kiinteistotunnus!")
        if not request.auth:
            return HttpResponse(status=401)
        facta_creds = request.auth.access_facta
        if not facta_creds:
            return HttpResponseForbidden("No access!")

        # Confirmed access to Facta Oracle SQL.
        # Go get the data!
        f_ko = hel_facta.KiinteistonOmistajat(facta_creds.username,
                                              facta_creds.credential,
                                              facta_creds.host_spec)
        rows = f_ko.get_by_kiinteistotunnus(ktunnus_to_use)
        if not rows:
            return HttpResponseNotFound()

        # Process result:
        owner_rows = []
        occupant_rows = []
        if rows:
            for row in rows:
                # KiinteistonOmistajaV1Serializer.OWNER_TYPES
                if row[14] == '10': # C_LAJI
                    # Helsinki
                    owner_type = 'H'
                elif row[14] in ['8', '11']: # C_LAJI
                    # Govt. of Finland
                    owner_type = 'F'
                else:
                    # Private
                    owner_type = 'P'

                owner = {
                    'kiinteistotunnus': row[2], # KIINTEISTOTUNNUS
                    'address': self._extract_omistaja_address(row),
                    'owner_home_municipality': row[17], # C_KOTIKUNT
                    'land_owner_type': owner_type
                }
                owner_rows.append(owner)

        f_kh = hel_facta.KiinteistonHaltijat(facta_creds.username,
                                              facta_creds.credential,
                                              facta_creds.host_spec)
        rows = f_kh.get_by_kiinteistotunnus(ktunnus_to_use)

        # Process result:
        if rows:
            for row in rows:
                occupant = {
                    'kiinteistotunnus': row[2], # KIINTEISTOTUNNUS
                    'address': self._extract_haltija_address(row),
                }
                occupant_rows.append(occupant)

        kiinteisto_data = {
            'kiinteistotunnus': ktunnus_to_use,
            'omistajat': owner_rows,
            'haltijat': occupant_rows,
        }

        # Go validate the returned data.
        # It needs to be verifiable by serializer rules. Those are published in Swagger.
        serializer = self.serializer_class(data=kiinteisto_data)
        if not serializer.is_valid():
            log.error("Errors: %s" % str(serializer.errors))

            return HttpResponseServerError("Data not formatted correctly!")

        return JsonResponse(serializer.validated_data)
