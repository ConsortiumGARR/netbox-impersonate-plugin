from netbox.tables.columns import TemplateColumn
from users.tables import UserTable
from utilities.tables import register_table_column

# The table sits inside the bulk-action form, so the button borrows it (and its CSRF
# token) through formaction instead of nesting a form of its own.
IMPERSONATE_BUTTON = """
{% if request.real_user.is_superuser and record.is_active and not record.is_superuser %}
<button type="submit" class="btn btn-sm btn-orange" title="Impersonate" formnovalidate
  formmethod="post"
  formaction="{% url 'plugins:netbox_impersonate_plugin:impersonate_start' uid=record.pk %}">
  <i class="mdi mdi-account-switch"></i>
</button>
{% endif %}
"""

register_table_column(
    TemplateColumn(
        template_code=IMPERSONATE_BUTTON,
        verbose_name="Impersonate",
        orderable=False,
        exclude_from_export=True,
    ),
    "impersonate",
    UserTable,
)

# NetBox offers no API for this: it applies to users who never customized the table.
UserTable.Meta.default_columns = (*UserTable.Meta.default_columns, "impersonate")
