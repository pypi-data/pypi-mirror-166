"""
Versioned schema repository for http specifications
"""
from typing import Callable

from cerberus.validator import DocumentError
from chk.infrastructure.exception import err_message
from chk.modules.http.constants import RequestConfigNode
from chk.modules.http.validation_rules import request_schema


class RequestValueHandler:
    """ Handle variables and values regarding request """

    @staticmethod
    def request_fill_val(document: dict, symbol_table: dict, replace_method: Callable[[dict, dict], dict]):
        """Convert request block variables"""

        request_document = document.get(RequestConfigNode.ROOT, {})
        import copy; request_document = copy.deepcopy(request_document)

        return replace_method(request_document, symbol_table)

    @staticmethod
    def request_get_return(document: dict, response: dict) -> dict:
        """Return request block variables"""
        returnable = response
        returnable['have_all'] = True

        if req := document.get(RequestConfigNode.ROOT, {}):
            if ret := req.get(RequestConfigNode.RETURN):
                ret = str(ret)
                if not ret.startswith('.'):
                    raise ValueError('Unsupported key format in request.return')

                ret = ret.lstrip('.')
                if ret not in ('version', 'code', 'reason', 'headers', 'body'):
                    raise ValueError('Unsupported key in request.return')

                fx = lambda k, v: None if k != ret else v
                returnable = {key: fx(key, value) for key, value in response.items()}
                returnable['have_all'] = False

        return returnable


class RequestMixin(object):
    """ Mixin for request spec. for v0.7.2"""

    def request_validated(self) -> dict[str, dict]:
        """Validate the schema against config"""
        try:
            request_doc = self.request_as_dict()
            if not self.validator.validate(request_doc, request_schema):
                raise SystemExit(err_message('fatal.V0006', extra=self.validator.errors))
        except DocumentError as doc_err:
            raise SystemExit(err_message('fatal.V0001', extra=doc_err)) from doc_err
        else:
            return request_doc  # or is a success

    def request_as_dict(self) -> dict[str, dict]:
        """Get version string"""
        if not hasattr(self, 'validator') or not hasattr(self, 'document'):
            raise SystemExit(err_message('fatal.V0005'))

        try:
            return {key: self.document[key] for key in (RequestConfigNode.ROOT,) if key in self.document}
        except Exception as ex:
            raise SystemExit(err_message('fatal.V0005', extra=ex))
