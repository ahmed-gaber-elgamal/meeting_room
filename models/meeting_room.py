from odoo import fields, models, api


class MeetingRoom(models.Model):
    _name = 'meeting.room'
    _description = 'Meeting Room'

    name = fields.Char(string='Meeting Room', required=True)
    capacity = fields.Integer(required=True)
    active = fields.Boolean(default=True)
