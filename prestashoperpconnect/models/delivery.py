# -*- coding: utf-8 -*-
##############################################################################
#
#    Authors: Guewen Baconnier, Sébastien Beau, David Béal
#    Copyright (C) 2010 BEAU Sébastien
#    Copyright 2011-2013 Camptocamp SA
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import logging
from openerp.osv import fields, orm

_logger = logging.getLogger(__name__)


class prestashop_delivery_carrier(orm.Model):
    _name = 'prestashop.delivery.carrier'
    _inherit = 'prestashop.binding'
    _inherits = {'delivery.carrier': 'openerp_id'}
    _description = 'Prestashop Carrier'

    _columns = {
        'openerp_id': fields.many2one(
            'delivery.carrier',
            string='Delivery carrier',
            required=True,
            ondelete='cascade'
        ),
        'id_reference': fields.integer(
            'Id reference',
            help="In Prestashop, carriers with the same 'id_reference' are "
                 "some copies from the first one id_reference (only the last "
                 "one copied is taken account ; and the only one which "
                 "synchronized with erp)"
        ),
        'name_ext': fields.char(
            'External name',
            size=64
        ),
        'active_ext': fields.boolean(
            'External active', help="... in prestashop"
        ),
        'export_tracking': fields.boolean(
            'Export tracking numbers',
            help=" ... in prestashop"
        ),
    }

    _defaults = {
        'export_tracking': False,
    }

    _sql_constraints = [
        ('prestashop_uniq', 'unique(backend_id, prestashop_id)',
         'A delivry carrier with the same ID on PrestaShop already exists.'),
    ]


class delivery_carrier(orm.Model):
    _inherit = "delivery.carrier"
    _columns = {
        'prestashop_bind_ids': fields.one2many(
            'prestashop.delivery.carrier',
            'openerp_id',
            string='PrestaShop Bindings',),
        'company_id': fields.many2one(
            'res.company', 'Company', select=1, required=True
        ),
    }
