from django.http import JsonResponse
from django.views.generic.base import View
from django.views.decorators.csrf import csrf_exempt
from participa.settings import SEFAZ_API_URL
from participa.auth_sefaz.tasks import auth_token
from participa.report.models import Report
from .models import User
from django.db.models import Count

import requests
import json


class ParticipaSefazRequest(object):

    def _request(self, url, method='GET', data=None, headers=None):
        try:
            if method == 'POST':
                return requests.post(url, data=data, headers=headers)
            elif method == 'PUT':
                return requests.put(url, data=data, headers=headers)
            else:
                return requests.get(url, headers=headers)
        except:
            pass

    def get_request_headers(self, token=None):

        headers = {
            "Content-Type": "application/json"
        }
        if token:
            headers.update({"Authorization": token})

        return headers

    def send_report(self, body, token):
        url = "%s/sfz-nfcidada-api/api/public/denuncia/incluir" % SEFAZ_API_URL
        response = self._request(url, method='POST', data=body, headers=self.get_request_headers(token))

        if response.status_code == 200:
            return response
        else:
            return None

    def get_raffles(self, token):
        url = "%s/sfz-nfcidada-api/api/public/sorteio" % SEFAZ_API_URL
        response = self._request(url, headers=self.get_request_headers(token))

        if response.status_code == 200:
            return response.text
        else:
            return None

    def get_credits(self, user, token):
        url = "%s/sfz-nfcidada-api/api/public/consultarCredito/%s" % (SEFAZ_API_URL, user.cpf)
        response = self._request(url, headers=self.get_request_headers(token))

        if response.status_code == 200:
            return response.text
        else:
            return None

    def get_tickets_by_seq(self, seq, user, token):
        url = "%s/sfz-nfcidada-api/api/public/bilhete" % SEFAZ_API_URL
        body = json.dumps({
            "documento": user.cpf,
            "sequencialSorteio": seq
        })
        response = self._request(url, method='POST', data=body, headers=self.get_request_headers(token))

        if response.status_code == 200:
            return response.text
        else:
            return None

    def get_notes_by_date(self, date_comp, user, token):
        url = "%s/sfz-nfcidada-api/api/public/notas" % SEFAZ_API_URL
        body = json.dumps({
            "numeroDestinatario": user.cpf,
            "dataCompetencia": date_comp
        })
        response = self._request(url, method='POST', data=body, headers=self.get_request_headers(token))

        if response.status_code == 200:
            return response.text
        else:
            return None


class BaseView(View, ParticipaSefazRequest):

    def success_recive(self):
        return JsonResponse({"status": 200})

    def error_recive(self):
        return JsonResponse({"status": 401}, status=401)

    @csrf_exempt
    @auth_token
    def dispatch(self, *args, **kwargs):
        return super(BaseView, self).dispatch(*args, **kwargs)


class SefazApiFacilitate(BaseView):

    def get_last_raffle(self, token):
        raffles = json.loads(self.get_raffles(token), None)
        return max(raffles, key=lambda item: item['sequencial'])

    def get_points(self, user):
        return Report.objects.filter(user=user, status='2').count()

    def post(self, *args, **kwargs):
        data = json.loads(str(self.request.body, "utf_8"))
        user = User.objects.filter(cpf=data.get("cpf", None)).first()
        token = self.request.META['HTTP_AUTHORIZATION']
        if user and token:

            points = self.get_points(user)
            credits = json.loads(self.get_credits(user, token), None).get('valorCredito', None)
            last_raffle = self.get_last_raffle(token)

            date_comp = last_raffle.get('dataRealizacao', None)[:7].replace("-", "")
            notes = json.loads(self.get_notes_by_date(date_comp, user, token), None)
            notes_to_new_ticket = len(notes)%10

            total_tickets = len(json.loads(self.get_tickets_by_seq(last_raffle.get('sequencial', None), user, token))) # talvez isso esteja errado, consultar os cara da api

            final_object = {
                "points": points,
                "credits": credits,
                "last_raffle": last_raffle,
                "notes": notes_to_new_ticket,
                "number_of_tickets": total_tickets 
            }

            return JsonResponse(final_object)

        else:
            return self.error_recive()


class SefazApiSetNewUser(BaseView):

    def post(self, *args, **kwargs):
        data = json.loads(str(self.request.body, "utf_8"))
        if not User.objects.filter(cpf=data.get("cpf", None)).first():
            new_user = User(cpf=data.get("cpf", None), name=data.get("name", None))
            new_user.save()
            if new_user:
                return self.success_recive()
        else:
            return JsonResponse({"status": 401, "msg": "Usuário já registrado."}, status=401)

        return self.error_recive()

class SefazApiRanking(BaseView):
    def get_ranking(self, user):
        ranking = Report.objects.values("user__id").filter(status="2").annotate(points=Count("user__id")).order_by("-points")
        for i, r in enumerate(ranking):
            r["position"] = i+1
        top_five = ranking[:5]
        for r_user in ranking:
            if r_user["user__id"] == user.id:
                current_user = r_user
                break
        if current_user in top_five:
            current_user.update({"current_user": True})
            top_five[top_five.index(current_user)] = current_user
        else:
            current_user.update({"current_user": True})
            top_five.push(current_user)
    
        return top_five

    def post(self, *args, **kwargs):
        data = json.loads(str(self.request.body, "utf_8"))
        user = User.objects.filter(cpf=data.get("cpf", None)).first()
        if user:
            ranking = self.get_ranking(user)
            return JsonResponse(dict(ranking=list(ranking)))

        return self.error_recive()