from datetime import datetime
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from pandas import read_json

from common.exceptions import MainError
from constants.urls import URL_VERSIONS, MIN_VERSION
from models.versions import VersionListModel, VersionModel
from schemas import VersionSchema


blp = Blueprint("Versions", __name__, description="Operation with versions", url_prefix='/api/admin/static')


@blp.route("/versions")
class Versions(MethodView):
    @blp.response(200, VersionSchema(many=True))
    def get(self):
        try:
            result = VersionListModel(search={}, sort=[("number", -1)])
            return result.find()

        except MainError as e:
            abort(500, code=e.code, message=e.message)


@blp.route("/versions/upload")
class VersionsUpload(MethodView):
    @blp.response(200, VersionSchema(many=True))
    def post(self):
        try:
            list_versions = read_json(URL_VERSIONS)[0].to_list()
            list_versions = list_versions[0:(list_versions.index(MIN_VERSION) + 1)]

            insert_versions = []

            for v in list_versions:
                version = VersionModel(number=v)
                if not version.find():
                    insert_versions.append(
                        {
                            "number": v,
                            "dateUpload": datetime.utcnow(),
                            "status": False
                        }
                    )

            if len(insert_versions) > 0:
                versions = VersionListModel(data=insert_versions)
                return versions.insert()
            else:
                return []

        except MainError as e:
            abort(500, code=e.code, message=e.message)
