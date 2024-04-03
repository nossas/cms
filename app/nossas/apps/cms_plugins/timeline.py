from itertools import zip_longest
from collections import defaultdict

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from ..forms.timeline import TimelineFilterForm
from ..models.timeline import TimelineEvent


@plugin_pool.register_plugin
class TimelinePlugin(CMSPluginBase):
    name = "Linha do Tempo"
    module = "NOSSAS"
    render_template = "nossas/timeline/plugins/timeline_plugin.html"

    def prepare_timeline_events(self, events_world, events_nossas):
        # Organiza eventos por ano e mês
        events_by_year_month_world = defaultdict(lambda: defaultdict(list))
        events_by_year_month_nossas = defaultdict(lambda: defaultdict(list))
        
        for event in events_world:
            events_by_year_month_world[event.year][event.month].append(event)
        
        for event in events_nossas:
            events_by_year_month_nossas[event.year][event.month].append(event)

        unique_years_months = set(events_by_year_month_world.keys()) | set(events_by_year_month_nossas.keys())
        for year in unique_years_months:
            months_world = set(events_by_year_month_world[year].keys())
            months_nossas = set(events_by_year_month_nossas[year].keys())
            all_months = months_world | months_nossas
            
            for month in sorted(all_months):
                if month not in months_world:
                    events_by_year_month_world[year][month] = []
                if month not in months_nossas:
                    events_by_year_month_nossas[year][month] = []

        sorted_events_world = sorted(
            [(year, month, events_by_year_month_world[year][month]) for year in events_by_year_month_world for month in sorted(events_by_year_month_world[year])],
            key=lambda x: (x[0], x[1])
        )
        sorted_events_nossas = sorted(
            [(year, month, events_by_year_month_nossas[year][month]) for year in events_by_year_month_nossas for month in sorted(events_by_year_month_nossas[year])],
            key=lambda x: (x[0], x[1])
        )

        # Mantem os eventos alinhados entre as categorias
        aligned_events_world, aligned_events_nossas = zip(*zip_longest(sorted_events_world, sorted_events_nossas, fillvalue=(None, None, [])))

        return aligned_events_world, aligned_events_nossas

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        request = context.get("request")
        form = TimelineFilterForm(request.GET)
        event_filter = {}

        if form.is_valid():
            year = form.cleaned_data['year']
            if year:
                event_filter.update({"year": year})

        events_world = TimelineEvent.on_site.filter(event_context="mundo", **event_filter).order_by("year", "month", "day")
        events_nossas = TimelineEvent.on_site.filter(event_context="nossas", **event_filter).order_by("year", "month", "day")

        if len(events_nossas) > 0 and len(events_world) > 0:
            aligned_events_world, aligned_events_nossas = self.prepare_timeline_events(events_world, events_nossas)
        else:
            aligned_events_world, aligned_events_nossas = [], []

        context.update({
            "aligned_events_world": aligned_events_world,
            "aligned_events_nossas": aligned_events_nossas,
            "form": form,
        })

        return context