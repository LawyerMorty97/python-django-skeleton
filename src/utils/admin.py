import json

from django.contrib import admin
from django.db.models import Count
from django.utils.safestring import mark_safe

JSON_TRUE = json.dumps(True)
JSON_FALSE = json.dumps(False)


class ReadOnlyTabularInline(admin.TabularInline):
    can_delete = False
    show_change_link = True

    def has_add_permission(self, request, obj=None):  # noqa
        "Don't allow adding inline"
        return False

    def has_change_permission(self, request, obj=None):  # noqa
        "Don't allow changing inline"
        return False


def link_tag(url, obj_or_text):
    """
    Returns an HTML link to `url` with the
    text `obj_or_text`. Remember to call
    mark_safe()!
    """
    return mark_safe('<a href="%s">%s</a>' % (url, obj_or_text))


class OnlyUsedChoicesFilter(admin.FieldListFilter):
    def expected_parameters(self):
        return [self.field.name]

    def choices(self, changelist):
        value = self.used_parameters.get(self.field.name)

        yield {
            "selected": value is None,
            "query_string": changelist.get_query_string(remove=[self.field.name]),
            "display": "All",
        }
        values = self.field.model.objects.values_list(
            self.field.name, flat=True
        ).distinct()
        choices = dict(self.field.choices)
        for v in values:
            yield {
                "selected": value == v,
                "query_string": changelist.get_query_string({self.field.name: v}),
                "display": choices[v],
            }


class HasRelatedFilter(admin.FieldListFilter):
    def query_parameter(self):
        """
        Default query parameter, for example "has_matches".
        """
        return "has_%s" % self.field.name

    def annotate_kwarg(self):
        """
        The name to use for the annotated `Count()`, e.g. `"match_count"`
        """
        return "%s_count" % self.field.name

    def expected_parameters(self):
        return [self.query_parameter()]

    def value(self):
        """
        The value of the query string parameter. Accepts the
        strings ``"true"` or `"false"`, anything else is treated
        as `None`.
        """
        val = self.used_parameters.get(self.query_parameter(), None)
        if val == JSON_TRUE:
            return True
        elif val == JSON_FALSE:
            return False
        else:
            return None

    def choices(self, changelist):
        value = self.value()

        yield {
            "selected": value is None,
            "query_string": changelist.get_query_string(
                remove=[self.query_parameter()]
            ),
            "display": "All",
        }
        yield {
            "selected": value is False,
            "query_string": changelist.get_query_string(
                {self.query_parameter(): JSON_FALSE}
            ),
            "display": "0",
        }
        yield {
            "selected": value is True,
            "query_string": changelist.get_query_string(
                {self.query_parameter(): JSON_TRUE}
            ),
            "display": ">= 1",
        }

    def queryset(self, request, queryset):
        value = self.value()
        if value is None:
            return queryset

        # Annotate the query set with a "_count" aggregation
        # for the related field we're interested in
        annotate_kwarg = self.annotate_kwarg()
        queryset = queryset.annotate(**{annotate_kwarg: Count(self.field.name)})

        if value is True:
            # Filter the queryset to include only instances
            # whose `"_count"` value is > 0
            gte_kwarg = "%s__gte" % annotate_kwarg
            return queryset.filter(**{gte_kwarg: 1})
        else:
            return queryset.filter(**{annotate_kwarg: 0})
