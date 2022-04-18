from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.contrib import messages

from .forms import UploadFileForm
from .models import Transactions, History

from .aux_funcs import validate_transactions


def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():

            f = request.FILES['file']
            dates = History.objects.values_list('date_transactions', flat=True)
            new_transactions, h, msg = validate_transactions(f, dates)

            for m in msg:
                messages.info(request, m)

            if new_transactions:
                Transactions.objects.bulk_create(new_transactions,batch_size=None)
                h.save()

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else: 
        form = UploadFileForm()
        history = History.objects.all()

        args = {'form': form, 'history': history}

        return render(request, 'index.html', args)