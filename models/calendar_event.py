from odoo import fields, models, api
from odoo.exceptions import UserError
import pytz


class Meeting(models.Model):
    _inherit = 'calendar.event'

    meeting_room_id = fields.Many2one('meeting.room')

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            if values.get('meeting_room_id', False) and values.get('start', False) and values.get('stop', False):
                user_tz = pytz.timezone(self.env.context.get('tz') or 'UTC')
                room = self.env['meeting.room'].browse(values['meeting_room_id'])
                start = fields.Datetime.from_string(values['start'])
                stop = fields.Datetime.from_string(values['stop'])
                conflicts = self.env['calendar.event'].search([('meeting_room_id', '=', room.id)]).filtered(
                    lambda e: e.start <= start < e.stop or e.start <= stop < e.stop
                )
                # in case room is busy raise error
                if conflicts:
                    start = pytz.utc.localize(start).astimezone(user_tz).replace(tzinfo=None)
                    stop = pytz.utc.localize(stop).astimezone(user_tz).replace(tzinfo=None)
                    conflict_start = pytz.utc.localize(conflicts[0].start).astimezone(user_tz).replace(tzinfo=None)
                    conflict_stop = pytz.utc.localize(conflicts[0].stop).astimezone(user_tz).replace(tzinfo=None)
                    raise UserError("You may not be able to book the meeting room {} "
                                    "for the event {} start at: {} and stop at: {} "
                                    "while it is currently booked for the event {} start at: {} and stop at: {}."
                                    " You may shift your event to another time or contact {} who is the owner of the event {}"
                                    " if you want to convince her or him to give you this slot.".format(
                        room.name, values['name'], start, stop, conflicts[0].name,conflict_start, conflict_stop, conflicts[0].user_id.name, conflicts[0].name
                    ))
        meetings = super(Meeting, self).create(vals_list)
        return meetings

    def write(self, vals):
        if vals.get('meeting_room_id', False) or vals.get('start', False) or vals.get('stop', False):
            user_tz = pytz.timezone(self.env.context.get('tz') or 'UTC')
            room = self.env['meeting.room'].browse(vals['meeting_room_id']) if vals.get('meeting_room_id', False) else self.meeting_room_id
            start = fields.Datetime.from_string(vals['start']) if vals.get('start', False) else self.start
            stop = fields.Datetime.from_string(vals['stop']) if vals.get('stop', False) else self.stop
            conflicts = self.env['calendar.event'].search([('meeting_room_id', '=', room.id), ('id', '!=', self.id)]).filtered(
                lambda e: e.start <= start < e.stop or e.start <= stop < e.stop
            )
            # in case room is busy raise error
            if conflicts:
                start = pytz.utc.localize(start).astimezone(user_tz).replace(tzinfo=None)
                stop = pytz.utc.localize(stop).astimezone(user_tz).replace(tzinfo=None)
                conflict_start = pytz.utc.localize(conflicts[0].start).astimezone(user_tz).replace(tzinfo=None)
                conflict_stop = pytz.utc.localize(conflicts[0].stop).astimezone(user_tz).replace(tzinfo=None)
                raise UserError("You may not be able to book the meeting room {}"
                                " for the event {} start at: {} and stop at: {} while it is currently booked for the "
                                "event {} start at: {} and stop at: {}. You may shift your event to another time or "
                                "contact {} who is the owner of the event {} if you want to convince her or him "
                                "to give you this slot.".format(room.name, self.name, start, stop, conflicts[0].name,
                                                                conflict_start, conflict_stop, conflicts[0].user_id.name,
                                                                conflicts[0].name)
                                )
        res = super(Meeting, self).write(vals)
        return res
