from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Informe, Area, SatImage
from .forms import InformeForm, InformeUpdateForm
from django.http import HttpResponseRedirect
from django.shortcuts import render

class InformeListView(ListView):
    model = Informe 
    template_name = 'reports/informe_list.html'
    ### default context name is ‘object_list’. To change it, enter  context_object_name = 'informe'
    
class InformeDetailView(DetailView): 
    model = Informe    ## Or, queryset = Informe.objects.all()
    template_name = 'reports/informe_detail.html' 

    def get_context_data(self, **kwargs):
        context = super(InformeDetailView, self).get_context_data(**kwargs)
        informe_selected = Informe.objects.get(id=self.kwargs['pk'])   # pk is from the url 
        areaset = Area.objects.filter(event__id=informe_selected.event.id) 
        context['areaset'] = areaset
        superficie_total=hectarea_total=percentage_total=0
        for area in areaset:
            superficie_total += area.superficie
            hectarea_total += area.hectarea 
            percentage_total += area.percentage 
        if len(areaset): 
            percentage_average = percentage_total / len(areaset)
        context['superficie_total'] = superficie_total
        context['hectarea_total'] = hectarea_total
        context['percentage_average'] = percentage_average
        return context


    # # Initialize attributes shared by all view methods.
    # def setup(self, request, *args, **kwargs): 
    #     super().setup(request, *args, **kwargs)
    #     # get the Area objects using object ids passed by SESSION
    #     # this list will be sent to the template by the get_context_data() below
    #     if request.session._session:
    #         self.areas = [Area.objects.get(id=id) for id in request.session['affected_areas']] 


class InformeCreateView(CreateView): 
    form_class = InformeForm 
    template_name = 'reports/informe_form.html'

class InformeUpdateView(UpdateView):
    model = Informe      ## for UpdateView, this line is needed. 
    form_class = InformeUpdateForm
    template_name = 'reports/informe_update_form.html'

class InformeDeleteView(DeleteView):
    model = Informe
    template_name = 'reports/informe_delete.html'
    success_url = reverse_lazy('informe_list')

def load_satimages(request):
    event_id = request.GET.get('event') 
    satimages = SatImage.objects.filter(event__id=event_id).order_by('fecha')
    return render(request, 'reports/satimage_dropdown_list_options.html', {'satimages':satimages}) 

def load_satimages1(request):
    event_id = request.GET.get('event') 
    satimage1_id = request.GET.get('satimage1')
    if satimage1_id: 
        satimage1_id = int(satimage1_id)
    satimages = SatImage.objects.filter(event__id=event_id).order_by('fecha')
    return render(request, 'reports/satimage_dropdown_list_options1.html', {'satimages':satimages, 'satimage1_id':satimage1_id }) 

def load_satimages2(request):
    event_id = request.GET.get('event') 
    satimage2_id = request.GET.get('satimage2')
    if satimage2_id: 
        satimage2_id = int(satimage2_id)
    satimages = SatImage.objects.filter(event__id=event_id).order_by('fecha')
    return render(request, 'reports/satimage_dropdown_list_options2.html', {'satimages':satimages, 'satimage2_id':satimage2_id }) 