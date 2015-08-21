# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2014 credativ Ltd
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

from openerp.osv import orm, fields, osv

class SaleOrder(orm.Model):
    _inherit = "sale.order"

    _columns = {
        'requested_delivery_date': fields.date('Requested Delivery Date', select=True, help="Date on which customer has requested delivery.", readonly=True, states={'draft':[('readonly',False)]},),
    }

class SaleOrderLine(orm.Model):
    _inherit = "sale.order.line"

    def _bots_exported_rate(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            moves_exported, moves_total = 0, 0
            for move in line.move_ids:
                if move.state == 'cancel':
                    continue
                moves_total += move.product_qty
                if move.bots_test_exported().get('exported'):
                    moves_exported += move.product_qty
            res[line.id] = "%d / %d" % (moves_exported, moves_total)
        return res

    _columns = {
        'requested_delivery_date': fields.date('Requested Delivery Date', select=True, help="Date on which customer has requested delivery.", readonly=True, states={'draft':[('readonly',False)]},),
        'bots_exported_rate': fields.function(_bots_exported_rate, type='char', string='Exported to 3PL', readonly=True, help="Quantity of products which have been exported to 3PL/Bots"),
    }
