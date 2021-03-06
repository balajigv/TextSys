# Copyright 2013, Big Switch Networks
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import logging

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon.utils import memoized

from openstack_dashboard import api
from openstack_dashboard.dashboards.networking.routers.extensions.routerrules\
    import forms as rrforms


LOG = logging.getLogger(__name__)


class AddRouterRuleView(forms.ModalFormView):
    form_class = rrforms.AddRouterRule
    template_name = 'networking/routers/extensions/routerrules/create.html'
    success_url = 'horizon:networking:routers:detail'
    failure_url = 'horizon:networking:routers:detail'
    page_title = _("Add Router Rule")

    def get_success_url(self):
        return reverse(self.success_url,
                       args=(self.kwargs['router_id'],))

    @memoized.memoized_method
    def get_object(self):
        try:
            router_id = self.kwargs["router_id"]
            return api.neutron.router_get(self.request, router_id)
        except Exception:
            redirect = reverse(self.failure_url, args=[router_id])
            msg = _("Unable to retrieve router.")
            exceptions.handle(self.request, msg, redirect=redirect)

    def get_context_data(self, **kwargs):
        context = super(AddRouterRuleView, self).get_context_data(**kwargs)
        context['router'] = self.get_object()
        return context

    def get_initial(self):
        router = self.get_object()
        # store the router in the request so the rule manager doesn't have
        # to request it again from the API
        self.request.META['router'] = router
        return {"router_id": self.kwargs['router_id'],
                "router_name": router.name}
