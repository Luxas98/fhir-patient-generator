from fhir_fastavro import avroutil
import random
import string
import json
from faker import Faker
fake = Faker()


def random_date():
    return fake.date_time().astimezone().strftime("%Y-%m-%dT%H:%M:%S+01:00")


def generate_string(context=None):
    """Generate a random string of fixed length """
    context = context or {}
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(8))


def generate_generic(type_, context=None):
    context = context or {}

    if isinstance(type_, dict):
        return generate(type_['items'], context)

    if type_ == "boolean":
        return random.randint(1, 10) > 3
        # return random.choice([True, False])

    if type_ == "datetime":
        return random_date()

    if type_ == "gender":
        return random.choice(['female', 'male'])

    if type_ == "name":
        return {
            "family": fake.last_name(),
            "given": fake.first_name
        }

    if type_ == "string":
        return generate_string(context)

    if type_ == "null":
        return None

    return None


def generate_primitive(resourceType, context=None):
    context = context or {}
    if not resourceType:
        return {}

    schema = avroutil.get_fastavro_schema(resourceType)
    resource = {}

    for field in schema['fields']:
        field_types = field['type']
        field_name = field['name']

        if isinstance(field_types, list):
            field_value = generate_generic(random.choice(field_types), context)
        else:
            field_value = generate_generic(field_types, context)

        if field_value:
            resource[field_name] = field_value

    return resource


def generate(type_, context=None):
    context = context or {}
    if '.' in type_:
        resourceType = type_.split('.')[-1]
        return generate_primitive(resourceType, context)
    else:
        return generate_generic(type_, context)


def generate_resource(resource_name, context=None):
    context = context or {}
    schema = avroutil.get_fastavro_schema(resource_name)
    resource = {}

    for field in schema['fields']:
        types = field['type']
        field_name = field['name']

        if 'types' in context and field_name in context['types']:
            types = context['types'][field_name]

        if 'fields' in context and field_name in context['fields']:
            # TODO: Generate from context, maybe provide some probability function aswell
            field_value = context['fields'][field_name]
        else:
            field_value = generate(random.choice(types), context)

        if field_value:
            resource[field_name] = field_value

    if not 'id' in resource:
        resource['id'] = generate_string(context)
    resource['resourceType'] = resource_name
    return resource


def generate_multiple(resource_name, count, context):
    return [generate_resource(resource_name, context) for _ in range(count)]


def _reference(referenced_object):
    # TODO: test if there is identifier or display values
    # TODO: implement display and identifier values
    return {
        "reference": referenced_object['id']
    }


def generate_bundle():
    items = []

    # Patient
    patient = generate_resource('Patient', {
        "types": {
            "birthDate": ["datetime", "null"],
            "deceasedDateTime": ["datetime", "null"],
            "gender": ["gender", "null"],
            # "name": ["name", "null"] # TODO: missing in avro schema
        }
    })

    # Practitioner
    practitioner = generate_resource('Practitioner', {
        "types": {
            "birthDate": ["datetime", "null"]
        }
    })

    # Allergy generation
    encounter_allergy = generate_resource('Encounter', {
        "fields": {"subject": _reference(patient)}})
    allergy_intolerance = generate_resource('AllergyIntolerance', {
        "fields": {"patient": _reference(patient),
                   "encounter": _reference(encounter_allergy)}})


    # Encounter general
    encounter_general = generate_resource('Encounter', {
        "fields": {"subject": _reference(patient)}})

    diagnostic_report = generate_resource('DiagnosticReport', {
        "fields": {"subject": _reference(patient),
                   "context": _reference(encounter_general)},
        "types": {
            "effectiveDateTime": ["datetime", "null"],
            "issued": ["datetime", "null"]
        }

    })

    goal = generate_resource('Goal', {
        "fields": {"subject": _reference(patient)},
        "types": {
          "statusDate": ["datetime", "null"]
        }
    })

    # Observations
    observations = generate_multiple('Observation', 8, {
        "fields": {"encounter": _reference(encounter_general)}})

    # Procedure/Condition/Complications
    condition = generate_resource('Condition', {
        "fields": {
            "subject": _reference(patient),
            "context": _reference(encounter_general),
            "ons3tDateTime": ["datetime", "null"]
        }
    })

    procedure_request = generate_resource("ProcedureRequest", {
        "fields": {
            "subject": _reference(patient),
            "context": _reference(encounter_general)

        }
    })

    procedure = generate_resource('Procedure', {
        "fields": {
            "subject": _reference(patient),
            "context": _reference(encounter_general),
            "report": _reference(diagnostic_report),
            "complicationDetail": _reference(condition),
            # TODO: this can be empty
            "reasonReference": _reference(random.choice(observations)),
            "basedOn": [_reference(procedure_request)]
            # TODO: this can be observation or condition and multiple
        },
        "types": {
            "performedDateTime": "datetime"
        }
    })

    # Appointment for procedure
    appointment = generate_resource('Appointment', {
        "fields": {
            "indication": [_reference(procedure)]
        },
        "types": {
            "created": ["datetime"]
        }

    })

    # Medication Resources
    medication = generate_resource('Medication', {

    })
    medication_administration = generate_resource('MedicationAdministration', {
        "fields": {
            "medicationReference": _reference(medication),
            "context": _reference(encounter_general),
            "partOf": _reference(procedure)

        },
    })

    medication_request = generate_resource('MedicationRequest', {
        "fields": {
            "subject": _reference(patient),
            "context": _reference(encounter_general),
            "medicationReference": _reference(medication)
        }
    })

    medication_dispense = generate_resource('MedicationDispense', {
        "fields": {
            "medicationReference": _reference(medication),
            "subject": _reference(patient),
            "context": _reference(encounter_general),
            "authorizingPrescription": [_reference(medication_request)],
            "receiver": [_reference(patient)]
        }
    })

    medication_statement = generate_resource('MedicationStatement', {
        "fields": {
            "context": _reference(encounter_general),
            "subject": _reference(patient),
            "reasonReference": [_reference(condition), _reference(random.choice(observations))],
            "basedOn": [_reference(medication_request)],
            "partOf": [_reference(medication_dispense)]
        }
    })

    # Nutrition Order
    nutrition_order = generate_resource('NutritionOrder', {
        "fields": {
            "patient": _reference(patient),
            "encounter": _reference(encounter_general)
        },
        "types": {
            "dateTime": ["null", "datetime"]
        }
    })

    items.append(encounter_general)
    items.append(encounter_allergy)
    items.append(allergy_intolerance)
    items.append(appointment)
    items.append(condition)
    items.append(diagnostic_report)
    items.append(goal)
    items.append(patient)
    items.append(practitioner)
    items.append(procedure)
    items.append(procedure_request)
    items.append(medication_administration)
    items.append(medication_dispense)
    items.append(medication_statement)
    items.append(nutrition_order)
    items.extend(observations)

    return {
        "resourceType": "Bundle",
        "type": "transaction",
        "entry": items
    }

# for i in range(1):
#     print(json.dumps(generate_bundle(), indent=4, sort_keys=True))
