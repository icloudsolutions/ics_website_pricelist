# -*- coding: utf-8 -*-
from odoo import models, api

class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    @api.model
    def _check_website_pricelist(self):
        for website in self.env['website'].search([]):
            # sudo() to be able to read pricelists/website from another company
            if not website.sudo().pricelist_ids:
                # Créer une liste de prix par défaut au lieu de lever une erreur
                default_pricelist = self.env['product.pricelist'].create({
                    'name': 'Default Pricelist for %s' % website.name,
                    'currency_id': website.company_id.currency_id.id,
                    'website_id': website.id,
                    'selectable': True
                })
                website.pricelist_ids = [(4, default_pricelist.id)]
