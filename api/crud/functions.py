from api.db.models import WebsiteInfo, Email


# def write_emails_to_db(rows, fields, db):
#     field_map = {field_name: index for index, field_name in enumerate(fields)}
#     for row in rows:
#         uuid = row.get(fields[field_map["uuid"]])
#         email = row.get(fields[field_map["emails"]])
#
#         if not uuid or not email:
#             continue
#
#         website = db.query(WebsiteInfo).filter(WebsiteInfo.uuid == uuid).first()
#
#         if not website:
#             continue
#
#         existing_email = db.query(Email).filter(Email.email == email).first()
#
#         if not existing_email:
#             new_email = Email(email=email, related_website_id=website.uuid)
#             db.add(new_email)
#
#
# def write_phones_to_db():
#     field_map = {field_name: index for index, field_name in enumerate(fields)}
#     for row in rows:
#         uuid = row.get(fields[field_map["uuid"]])
#         phones = row.get(fields[field_map["phones"]])
#
#         if not uuid or not phones:
#             continue
#
#         website = db.query(WebsiteInfo).filter(WebsiteInfo.uuid == uuid).first()
#
#         if not website:
#             continue
#
#         existing_phones = db.query(Phones).filter(Phones.phones == phones).first()
#
#         if not existing_phones:
#             new_phones = Email(phones=phones, related_website_id=website.uuid)
#             db.add(new_phones)