from rest_framework_csv.renderers import CSVRenderer


class NotNestedMixin(object):

    def nest_flat_item(self, flat_item, prefix):
            """
            Returns the naked header instead of
            the prefixed version.
            You have to be certain that no header
            names collide
            """
            nested_item = {}
            for header, val in flat_item.items():
                nested_header = header if header else prefix
                nested_item[nested_header] = val
            return nested_item


class NotNestedCSVRenderer(NotNestedMixin, CSVRenderer):
    format = 'csv2'


class TSVRenderer(CSVRenderer):
    format = 'tsv'

    def render(self, data, media_type=None, renderer_context={}, writer_opts=None):
        renderer_context['writer_opts'] = {'dialect': 'excel-tab'}
        return super().render(data, media_type, renderer_context, writer_opts)


class NotNestedTSVRenderer(NotNestedMixin, TSVRenderer):
    format = 'tsv2'
