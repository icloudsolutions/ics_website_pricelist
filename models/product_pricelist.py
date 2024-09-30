# -*- coding: utf-8 -*-
from odoo import models, api, _

class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    @api.model
    def _check_website_pricelist(self):
        for website in self.env['website'].search([]):
            # sudo() to be able to read pricelists/website from another company
            if not website.sudo().pricelist_ids:
                # Créer une liste de prix par défaut au lieu de lever une erreur
                default_pricelist = self.env['product.pricelist'].create({
                    'name': _('Default Pricelist for %s') % website.name,
                    'currency_id': website.company_id.currency_id.id,
                    'website_id': website.id,
                    'selectable': True
                })
                website.pricelist_ids = [(4, default_pricelist.id)]

    @api.model
    def update_pricelists_website_id(self):
        # Sélectionner le site web que vous voulez associer aux listes de prix
        website = self.env['website'].search([('name', '=', 'You can')], limit=1)
        if not website:
            raise ValueError(_("Le site web 'You can' n'existe pas."))

        # Rechercher les listes de prix qui n'ont pas de website_id
        pricelists = self.env['product.pricelist'].search([('website_id', '=', False)])

        # Compteur pour suivre le nombre de listes de prix mises à jour
        count = 0
        # Mettre à jour le champ website_id pour toutes les listes de prix trouvées
        for pricelist in pricelists:
            pricelist.write({'website_id': website.id})
            count += 1

        # Retourner une confirmation avec le nombre de listes de prix mises à jour
        return _('Mise à jour de %d liste(s) de prix avec le site web "You can".') % count
