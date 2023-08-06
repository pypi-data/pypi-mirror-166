from odoo import models, fields

class PhotovoltaicPowerStation(models.Model):
    _inherit = "photovoltaic.power.station"

    tecnical_memory_link = fields.Char(string="Enlace memoria técnica")