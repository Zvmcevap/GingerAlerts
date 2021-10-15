from app import db, twilio
from flask import current_app
from app.models import User, Client, SmsTemplate, SentSms, Appointment
from datetime import datetime, timedelta
from sqlalchemy import func
from twilio.base.exceptions import TwilioRestException


print('Starting le file')
def send_daily():
    with current_app:
        print('Starting send_daily()')
        today = datetime.now()
        tomorrow = datetime.now() + timedelta(days=1)
        print(today.date(), tomorrow.date())
        todays_appointments = Appointment.query.filter(
            (func.date(Appointment.time_of_appointment) == today.date()) & (Appointment.same_day_sms == 1)).all()
        tomorrows_appointments = Appointment.query.filter(
            (func.date(Appointment.time_of_appointment) == tomorrow.date()) & (Appointment.day_before_sms == 1)).all()
        print(todays_appointments)
        if todays_appointments:
            for appointment in todays_appointments:
                print(f'appointment: {appointment}')
                user = User.query.filter(User.id == client.user_id).first()
                client = Client.query.filter(Client.id == appointment.client_id).first()
                if user.send_SMS:
                    if client.sms_template_id:
                        sms_template = SmsTemplate.query.filter(SmsTemplate.id == client.sms_template_id).first()
                    else:

                        sms_template = SmsTemplate.query.filter(SmsTemplate.id == user.sms_template_id).first()

                    sms_text = sms_template.template.replace('{ime_stranke}', client.name)
                    sms_text = sms_text.replace('{čas_termina}',
                                                appointment.time_of_appointment.strftime('Danes %d.%m.%Y ob: %H:%M'))
                    try:
                        twilio.message(sms_text, to=client.phone)

                        new_sent_sms = SentSms(
                            appointment_id=appointment.id,
                            sms_type_id=2,
                            sms_text=sms_text,
                            sent_at_datetime=datetime.now()
                        )
                        db.session.add(new_sent_sms)
                        appointment.same_day_sms = 2
                    except TwilioRestException:
                        print('Slaba Telefonska')
        print(tomorrows_appointments)
        if tomorrows_appointments:
            for appointment in tomorrows_appointments:
                client = Client.query.filter(Client.id == appointment.client_id).first()
                user = User.query.filter(User.id == client.user_id).first()
                print(user.send_SMS)
                if user.send_SMS:
                    if client.sms_template_id:
                        sms_template = SmsTemplate.query.filter(SmsTemplate.id == client.sms_template_id).first()
                    else:
                        sms_template = SmsTemplate.query.filter(SmsTemplate.id == user.sms_template_id).first()

                    sms_text = sms_template.template.replace('{ime_stranke}', client.name)
                    sms_text = sms_text.replace('{čas_termina}',
                                                appointment.time_of_appointment.strftime('Jutri %d.%m.%Y ob: %H:%M'))
                    try:
                        twilio.message(sms_text, to=client.phone)

                        new_sent_sms = SentSms(
                            appointment_id=appointment.id,
                            sms_type_id=3,
                            sms_text=sms_text,
                            sent_at_datetime=datetime.now()
                        )
                        db.session.add(new_sent_sms)
                        appointment.day_before_sms = 2
                    except TwilioRestException:
                        print('Slaba Telefonska')

        db.session.commit()


if __name__ == '__main__':
    send_daily()
