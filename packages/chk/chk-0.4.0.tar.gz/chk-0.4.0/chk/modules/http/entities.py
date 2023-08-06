from cerberus import Validator
from chk.infrastructure.file_loader import FileContext
from chk.infrastructure.work import WorkerContract, RequestProcessorContract, handle_request
from chk.modules.http.request_helper import RequestProcessorMixin_PyRequests
from chk.modules.http.support import RequestMixin
from chk.modules.variables.support import VariableMixin
from chk.modules.version.support import VersionMixin
from chk.modules.variables.constants import LexicalAnalysisType
from chk.modules.version.constants import DocumentType


class HttpSpec(
    RequestProcessorMixin_PyRequests,
    VersionMixin,
    RequestMixin,
    VariableMixin,
    WorkerContract,
    RequestProcessorContract
):

    def __init__(self, file_ctx: FileContext):
        self.file_ctx, self.document, self.validator = file_ctx, file_ctx.document, Validator()

    def __work__(self) -> dict:
        self.version_validated(DocumentType.HTTP)
        self.request_validated()
        self.variable_validated()

        ctx_document = self.variable_process(LexicalAnalysisType.REQUEST)
        out_response = handle_request(self, ctx_document)
        return self.variable_assemble_values(ctx_document, out_response)
