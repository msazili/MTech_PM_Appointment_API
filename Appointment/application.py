from flask import Flask, make_response, request, jsonify
from flask_mongoengine import MongoEngine
from constants import mongodb_password, datetime_format, mongodb_uri, mongodb_name
import datetime

app = Flask(__name__)

DB_URI = mongodb_uri.format(mongodb_password, mongodb_name)
app.config["MONGODB_HOST"] = DB_URI

db = MongoEngine()
db.init_app(app)

##### Patient Medical Data #####


class PatientMedicalData(db.Document):
    PatientId = db.StringField()
    Symptom = db.StringField()
    PreferredDate = db.DateTimeField()
    PreferredTime = db.StringField()

    def to_json(self):
        return {
            "PatientId": self.PatientId,
            "Symptom": self.Symptom,
            "PreferredDate": self.PreferredDate,
            "PreferredTime": self.PreferredTime
        }


@app.route('/api/patient_medical_data/populate', methods=['POST'])
def patient_populate():
    obj1 = PatientMedicalData(PatientId="1", Symptom="fever,running nose",
                              PreferredDate=datetime.datetime(2021, 3, 27, 0, 0), PreferredTime="10:00am")
    obj2 = PatientMedicalData(PatientId="2", Symptom="headache,vommit", PreferredDate=datetime.datetime(
        2021, 4, 5, 0, 0), PreferredTime="03:00pm")
    obj3 = PatientMedicalData(PatientId="3", Symptom="amnesia,headache,",
                              PreferredDate=datetime.datetime(2021, 3, 30, 0, 0), PreferredTime="05:30pm")
    obj4 = PatientMedicalData(PatientId="4", Symptom="flu,headache,muscle pain",
                              PreferredDate=datetime.datetime(2021, 4, 20, 0, 0), PreferredTime="12:00pm")
    obj5 = PatientMedicalData(PatientId="5", Symptom="vommit,cough", PreferredDate=datetime.datetime(
        2021, 4, 11, 0, 0), PreferredTime="09:30am")

    obj1.save()
    obj2.save()
    obj3.save()
    obj4.save()
    obj5.save()

    return make_response("Populated successfully", 201)


@app.route('/api/patient_medical_datas', methods=['GET', 'POST'])
def api_patient_med_data():
    if request.method == "GET":
        datas = []
        for data in PatientMedicalData.objects:
            datas.append(data)

        return make_response(jsonify(datas), 200)

    elif request.method == "POST":
        content = request.json

        data = PatientMedicalData(PatientId=content['PatientId'], Symptom=content['Symptom'], PreferredDate=datetime.datetime.strptime(
            content['PreferredDate'], datetime_format), PreferredTime=content['PreferredTime'])
        data.save()

        return make_response("Inserted successfully", 201)


@app.route('/api/patient_medical_datas/<patient_id>', methods=['GET', 'PUT', 'DELETE'])
def api_each_patient_med_data(patient_id):
    if request.method == "GET":
        obj = PatientMedicalData.objects(PatientId=patient_id).first()
        if obj:
            return make_response(jsonify(obj.to_json()), 200)
        else:
            return make_response("Data not found", 404)

    elif request.method == "PUT":
        content = request.json
        obj = PatientMedicalData.objects(PatientId=patient_id).first()
        obj.update(Symptom=content['Symptom'], PreferredDate=datetime.datetime.strptime(
            content['PreferredDate'], datetime_format), PreferredTime=content['PreferredTime'])

        return make_response("Updated successfully", 204)

    elif request.method == "DELETE":
        obj = PatientMedicalData.objects(PatientId=patient_id).first()
        obj.delete()

        return make_response("Deleted successfully", 204)

##### DoctorSpeciality #####


class DoctorSpeciality(db.Document):
    DoctorId = db.StringField()
    HandledSymptoms = db.StringField()
    AvailableDay = db.StringField()
    AvailableTime = db.StringField()
    Rating = db.IntField()
    ChargeRate = db.FloatField()

    def to_json(self):
        return {
            "DoctorId": self.DoctorId,
            "HandledSymptoms": self.HandledSymptoms,
            "AvailableDay": self.AvailableDay,
            "AvailableTime": self.AvailableTime,
            "Rating": self.Rating,
            "ChargeRate": self.ChargeRate
        }


@app.route('/api/doctor_speciality/populate', methods=['POST'])
def doctor_populate():
    obj1 = DoctorSpeciality(DoctorId="1", HandledSymptoms="fever,vommit",
                            AvailableDay="Saturday,Sunday", AvailableTime="07:00pm", Rating=3, ChargeRate=40.5)
    obj2 = DoctorSpeciality(DoctorId="2", HandledSymptoms="headache,amnesia",
                            AvailableDay="Sunday", AvailableTime="10:00am", Rating=1, ChargeRate=50)
    obj3 = DoctorSpeciality(DoctorId="3", HandledSymptoms="muscle pain,headache,",
                            AvailableDay="Monday,Wednesday", AvailableTime="03:00pm", Rating=5, ChargeRate=60)
    obj4 = DoctorSpeciality(DoctorId="4", HandledSymptoms="flu,running nose,headache",
                            AvailableDay="Saturday", AvailableTime="04:00pm", Rating=4, ChargeRate=25)
    obj5 = DoctorSpeciality(DoctorId="5", HandledSymptoms="fever,cough",
                            AvailableDay="Friday,Saturday", AvailableTime="06:30pm", Rating=3, ChargeRate=30)

    obj1.save()
    obj2.save()
    obj3.save()
    obj4.save()
    obj5.save()

    return make_response("Populated successfully", 201)


@app.route('/api/doctor_speciality_datas', methods=['GET', 'POST'])
def api_doctor_spec_data():
    if request.method == "GET":
        datas = []
        for data in DoctorSpeciality.objects:
            datas.append(data)

        return make_response(jsonify(datas), 200)

    elif request.method == "POST":
        content = request.json

        data = DoctorSpeciality(DoctorId=content['DoctorId'], HandledSymptoms=content['HandledSymptoms'], AvailableDay=content['AvailableDay'],
                                AvailableTime=content['AvailableTime'], Rating=content['Rating'], ChargeRate=content['ChargeRate'])
        data.save()

        return make_response("Inserted successfully", 201)


@app.route('/api/doctor_speciality_datas/<doctor_id>', methods=['GET', 'PUT', 'DELETE'])
def api_each_doctor_spec_data(doctor_id):
    if request.method == "GET":
        obj = DoctorSpeciality.objects(DoctorId=doctor_id).first()
        if obj:
            return make_response(jsonify(obj.to_json()), 200)
        else:
            return make_response("Data not found", 404)

    elif request.method == "PUT":
        content = request.json
        obj = DoctorSpeciality.objects(DoctorId=doctor_id).first()
        obj.update(HandledSymptoms=content['HandledSymptoms'], AvailableDay=content['AvailableDay'],
                   AvailableTime=content['AvailableTime'], Rating=content['Rating'], ChargeRate=content['ChargeRate'])

        return make_response("Updated successfully", 204)

    elif request.method == "DELETE":
        obj = DoctorSpeciality.objects(DoctorId=doctor_id).first()
        obj.delete()

        return make_response("Deleted successfully", 204)

####################
##### appointment api ####


class MedicalAppointment(db.Document):
    AppointmentId = db.StringField()
    AppointmentNumber = db.StringField()
    PatientId = db.StringField()
    DoctorId = db.StringField()
    AppointmentDate = db.DateTimeField()

    def to_json(self):
        return {
            "AppointmentId": self.AppointmentId,
            "AppointmentNumber": self.AppointmentNumber,
            "PatientId": self.PatientId,
            "DoctorId": self.DoctorId,
            "AppointmentDate": self.AppointmentDate
        }


@app.route('/api/medicalappointment/populate', methods=['POST'])
def patient_populate():
    obj1 = MedicalAppointment(AppointmentId="1", AppointmentNumber="10",
                              PatientId="1", DoctorId="1" AppointmentTime="10:00am")
    obj2 = MedicalAppointment(AppointmentId="2", AppointmentNumber="20",
                              PatientId="2", DoctorId="2", AppointmentTime="03:00pm")
    obj3 = MedicalAppointment(AppointmentId="3", AppointmentNumber="30",
                              PatientId="3", DoctorId="3", AppointmentTime="05:30pm")
    obj4 = MedicalAppointment(AppointmentId="4", AppointmentNumber="40",
                              PatientId="4", DoctorId="4", AppointmentTime="12:00pm")
    obj5 = MedicalAppointment(AppointmentId="5", AppointmentNumber="50",
                              PatientId="5", DoctorId="5", AppointmentTime="09:30am")

    obj1.save()
    obj2.save()
    obj3.save()
    obj4.save()
    obj5.save()

    return make_response("PatientMedicalData populated successfully", 201)


@app.route('/api/medicalappointments', methods=['GET', 'POST'])
def api_medicalappointments_data():
    if request.method == "GET":
        datas = []
        for data in MedicalAppointment.objects:
            datas.append(data)

        return make_response(jsonify(datas), 200)

    elif request.method == "POST":
        content = request.json

        data = MedicalAppointment(AppointmentId=content['AppointmentId'], AppointmentNumber=content['AppointmentNumber'], PatientId=content['PatientId'], DoctorId=content['DoctorId'], AppointmentTime=datetime.datetime.strptime(
            content['AppointmentTime'], datetime_format))
        data.save()

        return make_response("Inserted successfully", 201)


@app.route('/api/medicalappointments/<patient_id>', methods=['GET', 'PUT', 'DELETE'])
def api_each_patient_med_data(patient_id):
    if request.method == "GET":
        obj = MedicalAppointment.objects(PatientId=patient_id).first()
        if obj:
            return make_response(jsonify(obj.to_json()), 200)
        else:
            return make_response("Data not found", 404)

    elif request.method == "PUT":
        content = request.json
        obj = MedicalAppointment.objects(PatientId=patient_id).first()
        obj.update(AppointmentId=content['AppointmentId'], AppointmentNumber=content['AppointmentNumber'], PatientId=content['PatientId'], DoctorId=content['DoctorId'], AppointmentTime=datetime.datetime.strptime(
            content['AppointmentTime'], datetime_format))

        return make_response("Updated successfully", 204)

    elif request.method == "DELETE":
        obj = MedicalAppointment.objects(PatientId=patient_id).first()
        obj.delete()

        return make_response("Deleted successfully", 204)


if __name__ == '__main__':
    app.run()
