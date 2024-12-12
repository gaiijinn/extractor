from api.db.models import WebsiteInfo


class DataWriter:
    def __init__(self, db, fields, model, field_map, field_aliases=None):
        self.db = db
        self.fields = fields
        self.model = model
        self.field_map = field_map
        self.field_aliases = field_aliases or {}


    def get_field_name(self):
        model_name = self.model.__name__.lower()
        return self.field_aliases.get(model_name, model_name)


    def write_to_db(self, rows):
        for row in rows:
            uuid = row.get(self.fields[self.field_map["uuid"]])
            field_name = self.get_field_name()
            value = row.get(self.fields[self.field_map[field_name]])

            if not uuid or not value:
                continue

            website = self.db.query(WebsiteInfo).filter(WebsiteInfo.uuid == uuid).first()

            if not website:
                continue

            existing_entry = self.db.query(self.model).filter(
                getattr(self.model, self.model.__name__.lower()) == value
            ).first()

            if not existing_entry:
                new_entry = self.model(
                    **{
                        self.model.__name__.lower(): value,
                        "related_website_id": website.uuid,
                    }
                )
                self.db.add(new_entry)
        self.db.commit()