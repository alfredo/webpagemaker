from urlparse import urlparse

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.utils import simplejson as json
from django.http import HttpResponse, HttpResponseBadRequest

from . import models
from . import sanitize

@csrf_exempt
@require_POST
def publish_page(request):
    if not request.POST.get('html', ''):
        return HttpResponseBadRequest("HTML body expected.")
    if len(request.POST['html']) > settings.MAX_PUBLISHED_PAGE_SIZE:
        return HttpResponse("Request Entity Too Large", status=413)
    if request.POST.get('original-url', ''):
        parsed = urlparse(request.POST['original-url'])
        if parsed.scheme not in ['http', 'https']:
            return HttpResponseBadRequest("Invalid origin URL.")
    trunc = models.Page._meta.get_field_by_name('original_url')[0].max_length
    original_url = request.POST.get('original-url', '')[:trunc]
    page = models.Page(html=request.POST['html'],
                       original_url=original_url)
    page.save()
    response = HttpResponse('/p/%d' % page.id, content_type="text/plain")
    response['Access-Control-Allow-Origin'] = '*'
    return response

def get_sanitizer_config(request):
    cfg = {
        'allowed_tags': sanitize.ALLOWED_TAGS,
        'allowed_attributes': sanitize.ALLOWED_ATTRS
    }
    response = HttpResponse(json.dumps(cfg), content_type="application/json")
    response['Access-Control-Allow-Origin'] = '*'
    return response

def get_page(request, page_id):
    # the code_flag allows the api to display the santized html without nofollow, and as plain
    # text for remixing.
    code_flag = request.GET.get('code', False)
    if code_flag:
        nofollow = False
        mimetype= 'text/plain; charset=utf-8'
    else:
        nofollow = True
        mimetype = 'text/html; charset=utf-8'
    page = get_object_or_404(models.Page, pk=page_id)
    response = HttpResponse(sanitize.sanitize(page.html,nofollow=nofollow), mimetype=mimetype)
    if page.original_url:
        response['X-Original-URL'] = page.original_url
    response['Access-Control-Allow-Origin'] = '*'
    return response
